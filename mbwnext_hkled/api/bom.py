# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tạo BOM tự động dựa trên BOM Template + BOM Rule (PHẦN I tài liệu nghiệp vụ HKLED)."""

import frappe
from frappe import _
from frappe.utils import flt


def get_active_template(item_code):
	"""Trả về tên BOM Template đang hoạt động của item cha item_code, hoặc None nếu không có."""
	variant_of = frappe.db.get_value("Item", item_code, "variant_of")
	if not variant_of:
		return None

	return frappe.db.get_value("BOM Template", {"item_template": variant_of, "is_active": 1})


def resolve_components(item_code, template_name):
	"""Đọc BOM Template + BOM Rule để xác định danh sách NVL/số lượng cho item_code."""
	template = frappe.get_cached_doc("BOM Template", template_name)
	components = []

	for row in template.bom_component_table:
		if row.component_type == "Cố Định":
			components.append({"item_code": row.item, "qty": row.qty})
			continue

		rule = frappe.get_all(
			"BOM Rule",
			filters={
				"parent": template_name,
				"item_to_manufacture": item_code,
				"bom_component": row.bom_component,
			},
			fields=["item", "qty"],
			limit=1,
		)
		if not rule:
			frappe.throw(
				_(
					"Không tìm thấy BOM Rule cho Mặt Hàng {0}, Thành Phần BOM {1} (BOM Template {2})"
				).format(frappe.bold(item_code), frappe.bold(row.bom_component), frappe.bold(template_name))
			)
		components.append({"item_code": rule[0].item, "qty": rule[0].qty})

	return components


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
