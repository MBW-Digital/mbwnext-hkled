# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tạo BOM tự động dựa trên BOM Template + BOM Rule (PHẦN I tài liệu nghiệp vụ HKLED)."""

import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils.safe_exec import is_safe_exec_enabled, run_script

from mbwnext_hkled.server_scripts.bom_qty import SCRIPT_NAME as QTY_SCRIPT


def resolve_qty_by_formula(item_code, component_name, item_template, template_name):
	"""Gọi Server Script `hkled_resolve_bom_qty` để lấy số lượng (và NVL nếu là "Theo Rule").

	Công thức nằm ở Server Script chứ không ở đây là quyết định kiến trúc trong tài liệu
	thiết kế: HKLED phải sửa được công thức ngay, không cần build/deploy lại app.

	Khoá tra công thức là `item_template` (Mặt Hàng Cha) — chốt của TungDA 07/08. Trước đây
	là field `rule_group` người dùng tự chọn; field đó đã bỏ, Server Script tự suy.
	"""
	if not is_safe_exec_enabled():
		frappe.throw(
			_(
				"Server Script đang tắt nên không tính được công thức số lượng. "
				"Cần bật bằng: bench set-config -g server_script_enabled 1"
			)
		)
	if not frappe.db.exists("Server Script", QTY_SCRIPT):
		frappe.throw(
			_("Chưa cài Server Script {0} — chạy lại bench migrate để cài").format(
				frappe.bold(QTY_SCRIPT)
			)
		)

	flags = run_script(
		QTY_SCRIPT,
		item_code=item_code,
		component_name=component_name,
		item_template=item_template,
		bom_template=template_name,
	)
	result = (flags or {}).get("result")
	if not result:
		frappe.throw(
			_("Server Script {0} không trả về số lượng cho Thành Phần BOM {1}").format(
				frappe.bold(QTY_SCRIPT), frappe.bold(component_name)
			)
		)
	return result


def get_active_template(item_code):
	"""Trả về tên BOM Template đang hoạt động của item cha item_code, hoặc None nếu không có."""
	variant_of = frappe.db.get_value("Item", item_code, "variant_of")
	if not variant_of:
		return None

	return frappe.db.get_value("BOM Template", {"item_template": variant_of, "is_active": 1})


def resolve_components(item_code, template_name, warnings=None):
	"""Đọc BOM Template + BOM Rule để xác định danh sách NVL/số lượng cho item_code.

	3 kiểu thành phần (mục 2.3 tài liệu thiết kế):
	- "Cố Định": item + qty nhập tay trên BOM Template.
	- "Số Lượng Theo Công Thức": item nhập tay, qty do Server Script tính.
	- "Theo Rule": cả item (tra BOM Rule theo giá trị "Nguồn" của biến thể) và qty do Server Script.
	"""
	template = frappe.get_cached_doc("BOM Template", template_name)
	components = []
	if warnings is None:
		warnings = []

	for row in template.bom_component_table:
		if row.component_type == "Cố Định":
			components.append({"item_code": row.item, "qty": row.qty})
			continue

		resolved = resolve_qty_by_formula(
			item_code, row.bom_component, template.item_template, template_name
		)
		if resolved.get("qty_defaulted"):
			warnings.append(row.bom_component)
		qty = flt(resolved.get("qty"))
		# Công thức ra 0 nghĩa là biến thể này KHÔNG dùng thành phần đó (VD Cầu đấu ở mức <=50W).
		# Phải bỏ hẳn dòng: BOM Item không nhận qty = 0.
		if qty <= 0:
			continue

		# "Theo Rule" -> NVL do Server Script tra từ BOM Rule; còn lại dùng item khai trên Template.
		components.append({"item_code": resolved.get("item") or row.item, "qty": qty})

	return components


def find_missing_sub_assembly_boms(components):
	"""Trong danh sách thành phần vừa tra, tìm những cái tự nó là bán thành phẩm có BOM Template
	riêng (đèn -> vỏ + module, PM-FEAT-00007) nhưng CHƯA có BOM nào — ERPNext chỉ nối `bom_no` vào
	BOM đã có sẵn (`get_bom_material_detail`), không tự tạo, nên những dòng này bị bỏ sót nếu không
	nhắc riêng. Thắng phát hiện 24/08, TungDA chốt hướng cảnh báo + nút "Tạo BOM tự động" trên form.
	"""
	missing = []
	for comp in components:
		item_code = comp["item_code"]
		if not get_active_template(item_code):
			continue
		if frappe.db.get_value("Item", item_code, "default_bom"):
			continue
		missing.append(item_code)
	return missing


@frappe.whitelist()
def get_template_raw_materials(item_code):
	"""NVL + số lượng suy từ BOM Template cho một biến thể — dùng để điền sẵn bảng Nguyên Vật Liệu
	khi người dùng chọn Mặt Hàng trên form BOM (yêu cầu của TungDA 07/08 trên PM-FEAT-00007).

	Trả `{}` khi mặt hàng không có BOM Template đang hoạt động — lúc đó form BOM giữ nguyên hành vi
	mặc định của ERPNext, không đụng vào.

	Lỗi công thức KHÔNG throw: người dùng mới chỉ chọn mặt hàng, chưa lưu gì. Trả lỗi về cho client
	hiện cảnh báo rồi để họ tự nhập tay, chứ chặn form ở bước này thì không sửa được gì.
	"""
	if not frappe.has_permission("BOM Template", "read"):
		frappe.throw(_("Bạn không có quyền đọc BOM Template"), frappe.PermissionError)

	template_name = get_active_template(item_code)
	if not template_name:
		return {}

	warnings = []
	log_depth = len(frappe.local.message_log or [])
	try:
		components = resolve_components(item_code, template_name, warnings)
	except Exception as exc:
		# frappe.throw ghi vào message_log TRƯỚC khi raise — nuốt exception không đủ,
		# phải cắt log đi nếu không trình duyệt vẫn hiện nguyên cụm lỗi đỏ.
		messages = [m.get("message") for m in (frappe.local.message_log or [])[log_depth:]]
		frappe.local.message_log = (frappe.local.message_log or [])[:log_depth]
		return {
			"template": template_name,
			"items": [],
			"error": (messages[-1] if messages else str(exc)),
		}

	return {
		"template": template_name,
		"item_template": frappe.db.get_value("Item", item_code, "variant_of"),
		"items": components,
		"qty_defaulted": warnings,
		"missing_sub_assembly_boms": find_missing_sub_assembly_boms(components),
	}


def build_bom_tree(item_code, order, resolved_cache, visiting):
	"""Duyệt đệ quy cây BOM theo thứ tự bottom-up (con trước, cha sau).

	`order` được nối dòng theo post-order DFS nên BOM con luôn xuất hiện trước BOM cha.
	Item không có BOM Template (nguyên vật liệu mua ngoài) được xem là lá, không tạo BOM riêng.
	"""
	if item_code in resolved_cache:
		return
	if item_code in visiting:
		frappe.throw(_("Phát hiện vòng lặp trong cây BOM tại {0}").format(frappe.bold(item_code)))

	template_name = get_active_template(item_code)
	if not template_name:
		resolved_cache[item_code] = None
		return

	visiting.add(item_code)
	components = resolve_components(item_code, template_name)
	for comp in components:
		build_bom_tree(comp["item_code"], order, resolved_cache, visiting)
	visiting.discard(item_code)

	resolved_cache[item_code] = components
	order.append({"item_code": item_code, "components": components})


def get_default_bom_items(item_code):
	default_bom = frappe.db.get_value("BOM", {"item": item_code, "is_default": 1, "docstatus": 1}, "name")
	if not default_bom:
		return None, None

	rows = frappe.get_all("BOM Item", filters={"parent": default_bom}, fields=["item_code", "qty"])
	current = sorted((row.item_code, flt(row.qty)) for row in rows)
	return default_bom, current


def is_bom_tree_valid(item_code, order):
	"""So sánh BOM Default hiện tại (thành phẩm + toàn bộ cấp dưới) với cấu hình Template/Rule mới nhất."""
	if not order:
		return False

	for node in order:
		expected = sorted((c["item_code"], flt(c["qty"])) for c in node["components"])
		_default_bom, current = get_default_bom_items(node["item_code"])
		if current is None or expected != current:
			return False

	return True


def create_bom(item_code, components, company, currency, created_boms):
	bom = frappe.new_doc("BOM")
	bom.item = item_code
	bom.company = company
	bom.currency = currency
	bom.quantity = 1
	bom.is_active = 1
	bom.is_default = 1

	for comp in components:
		row = bom.append("items", {"item_code": comp["item_code"], "qty": comp["qty"]})
		if comp["item_code"] in created_boms:
			row.bom_no = created_boms[comp["item_code"]]

	bom.insert(ignore_permissions=True)
	bom.submit()

	frappe.db.set_value(
		"BOM",
		{"item": item_code, "is_default": 1, "docstatus": 1, "name": ["!=", bom.name]},
		"is_default",
		0,
	)

	return bom.name


@frappe.whitelist()
def auto_create_bom(item_code, company=None):
	"""Chức năng "Tạo BOM tự động" - PHẦN I mục 7 tài liệu nghiệp vụ HKLED.

	Kiểm tra BOM Default hiện tại có còn hợp lệ theo BOM Template/BOM Rule mới nhất không.
	Nếu hợp lệ -> giữ nguyên. Nếu không (hoặc chưa có) -> tạo lại toàn bộ cây BOM từ dưới lên
	và gán làm BOM Default mới.
	"""
	if not frappe.has_permission("BOM", "create"):
		frappe.throw(_("Bạn không có quyền tạo BOM"), frappe.PermissionError)

	variant_of = frappe.db.get_value("Item", item_code, "variant_of")
	if not variant_of:
		frappe.throw(_("Không xác định được Item cha cho {0}").format(frappe.bold(item_code)))

	if not frappe.db.exists("BOM Template", {"item_template": variant_of, "is_active": 1}):
		frappe.throw(
			_("Item cha {0} chưa được thiết lập BOM Template").format(frappe.bold(variant_of))
		)

	if not company:
		company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
			"Global Defaults", "default_company"
		)
	if not company:
		frappe.throw(_("Vui lòng xác định Company"))
	currency = frappe.get_cached_value("Company", company, "default_currency")

	order = []
	build_bom_tree(item_code, order, {}, set())

	if is_bom_tree_valid(item_code, order):
		default_bom, _current = get_default_bom_items(item_code)
		return {
			"status": "valid",
			"message": _("BOM hiện tại hợp lệ"),
			"bom": default_bom,
			"created_boms": [],
		}

	created_boms = {}
	for node in order:
		created_boms[node["item_code"]] = create_bom(
			node["item_code"], node["components"], company, currency, created_boms
		)

	return {
		"status": "created",
		"message": _("Đã tạo mới {0} BOM, BOM Default: {1}").format(
			len(created_boms), created_boms[item_code]
		),
		"bom": created_boms[item_code],
		"created_boms": list(created_boms.values()),
	}
