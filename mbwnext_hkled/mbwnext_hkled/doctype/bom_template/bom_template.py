# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


def variant_matches(cond_attrs, variant_attrs):
	"""AND giữa các thuộc tính, OR trong `values` (spec §7.1).

	cond_attrs: [{"name": "Công suất", "values": ["50", "100"]}]
	variant_attrs: {"Công suất": "50", "Kiểu lắp": "Dọc", ...}
	"""
	for cond in cond_attrs:
		if variant_attrs.get(cond.get("name")) not in (cond.get("values") or []):
			return False
	return True


def describe_cond(cond_attrs):
	"""Chuỗi tóm tắt điều kiện để đọc trên lưới: 'Công suất: 50, 100 · Kiểu lắp: Dọc'."""
	return " · ".join(
		"{0}: {1}".format(c.get("name"), ", ".join(c.get("values") or [])) for c in cond_attrs
	)


def get_variant_attr_map(item_template):
	"""{mã biến thể: {thuộc tính: giá trị}} cho toàn bộ biến thể của item_template."""
	variants = frappe.get_all("Item", filters={"variant_of": item_template}, pluck="name")
	if not variants:
		return {}

	attr_map = {v: {} for v in variants}
	for row in frappe.get_all(
		"Item Variant Attribute",
		filters={"parent": ["in", variants]},
		fields=["parent", "attribute", "attribute_value"],
	):
		attr_map[row.parent][row.attribute] = row.attribute_value
	return attr_map


class BOMTemplate(Document):
	def validate(self):
		self.validate_item_template()
		self.validate_unique_components()
		self.resolve_rules()
		self.validate_rule_items()
		self.validate_single_active_template()

	def resolve_rules(self):
		"""Tính biến thể khớp cho từng rule, chặn 2 rule cùng thành phần phủ trùng nhau (spec §7.1).

		Rule để ở bảng `bom_rules` của chính BOM Template (phương án B, spec §5) và phân biệt
		nhau bằng `bom_component`. ⚠ KHÔNG dùng được phương án A (rule là con của BOM Component
		Table): Frappe không hỗ trợ bảng con lồng 2 cấp — `load_from_db` không đệ quy nên dòng
		cháu không được nạp mà cũng không được ghi xuống DB. Đã thử và xác nhận trên site.

		Kết quả cache vào `matched_variants` / `matched_count` / `cond_label` để hiển thị. Cache
		chỉ là phụ — Server Script vẫn tra bằng cond_attrs thật, nên cache lệch cũng không làm
		BOM ra sai.
		"""
		attr_map = get_variant_attr_map(self.item_template)

		rule_components = set()
		seen_by_component = {}

		for rule in self.bom_rules:
			if not rule.bom_component:
				frappe.throw(_("Rule #{0} chưa chọn Thành Phần BOM").format(rule.idx))

			cond_attrs = frappe.parse_json(rule.cond_attrs) or []
			if not cond_attrs:
				frappe.throw(
					_("Rule #{0} ({1}) chưa chọn thuộc tính điều kiện nào").format(
						rule.idx, frappe.bold(rule.bom_component)
					)
				)

			rule_components.add(rule.bom_component)
			if not rule.rule_id:
				rule.rule_id = "rule_{0}".format(rule.idx)
			rule.cond_label = describe_cond(cond_attrs)

			matched = [v for v, attrs in attr_map.items() if variant_matches(cond_attrs, attrs)]
			rule.matched_variants = frappe.as_json(sorted(matched))
			rule.matched_count = len(matched)

			# Chặn trùng: 1 biến thể chỉ được đúng 1 rule quyết định NVL, nếu không thì kết quả
			# phụ thuộc thứ tự dòng — sai âm thầm, không ai phát hiện.
			seen = seen_by_component.setdefault(rule.bom_component, {})
			for variant in matched:
				if variant in seen:
					frappe.throw(
						_(
							"Thành Phần BOM {0}: rule #{1} và rule #{2} cùng phủ biến thể {3}."
							" Mỗi biến thể chỉ được khớp đúng một rule."
						).format(
							frappe.bold(rule.bom_component), seen[variant], rule.idx, frappe.bold(variant)
						)
					)
				seen[variant] = rule.idx

		# Thành phần khai "Theo Rule" mà không có rule nào thì lúc tạo BOM mới lòi ra lỗi —
		# chặn ngay từ lúc lưu template cho người dùng biết sớm.
		for comp in self.bom_component_table:
			if comp.component_type == "Theo Rule" and comp.bom_component not in rule_components:
				frappe.throw(
					_("Thành Phần BOM {0} đang là “Theo Rule” nhưng chưa có rule nào").format(
						frappe.bold(comp.bom_component)
					)
				)

	def validate_item_template(self):
		if not frappe.db.get_value("Item", self.item_template, "has_variants"):
			frappe.throw(
				_("Mặt Hàng Cha {0} phải là mặt hàng Template (Has Variants)").format(
					frappe.bold(self.item_template)
				)
			)

	def validate_unique_components(self):
		seen = set()
		for row in self.bom_component_table:
			if row.bom_component in seen:
				frappe.throw(
					_("Row #{0}: Thành Phần BOM {1} bị trùng trong Bảng Thành Phần BOM").format(
						row.idx, frappe.bold(row.bom_component)
					)
				)
			seen.add(row.bom_component)

	def validate_rule_items(self):
		"""NVL đầu ra luôn phải là item lá (spec §7.3). Link filter chỉ chặn ở giao diện —
		gọi qua API hoặc import dữ liệu thì không qua filter đó, nên phải kiểm cả ở server."""
		for comp in self.bom_component_table:
			if comp.component_type != "Theo Rule" and comp.item:
				if frappe.db.get_value("Item", comp.item, "has_variants"):
					frappe.throw(
						_("Row #{0}: Mặt hàng {1} không được là mặt hàng Template").format(
							comp.idx, frappe.bold(comp.item)
						)
					)

		for rule in self.bom_rules:
			if frappe.db.get_value("Item", rule.item, "has_variants"):
				frappe.throw(
					_("Rule #{0} ({1}): Nguyên Vật Liệu {2} không được là mặt hàng Template").format(
						rule.idx, frappe.bold(rule.bom_component), frappe.bold(rule.item)
					)
				)

	def validate_single_active_template(self):
		if not self.is_active:
			return

		duplicate = frappe.db.exists(
			"BOM Template",
			{
				"item_template": self.item_template,
				"is_active": 1,
				"name": ["!=", self.name],
			},
		)
		if duplicate:
			frappe.throw(
				_("Mặt hàng cha {0} đã có BOM Template {1} đang hoạt động").format(
					frappe.bold(self.item_template), frappe.bold(duplicate)
				)
			)


# Field `rule_group` đã bỏ (chốt của TungDA 07/08 trên PM-FEAT-00007): khoá tra công thức
# giờ là chính Mặt Hàng Cha. Bảng suy bộ công thức từ mã mặt hàng cha nằm trong Server Script
# `hkled_resolve_bom_qty` (FORMULA_GROUP_BY_TEMPLATE + PREFIX_GROUPS) để HKLED sửa được ngay
# mà không cần deploy app — xem mbwnext_hkled/server_scripts/bom_qty.py.


@frappe.whitelist()
def get_condition_attributes(item_template):
	"""Thuộc tính + giá trị dùng cho hộp thoại "Chọn Điều Kiện".

	**Thuộc tính** lấy từ chính bảng đặc tính khai trên Mặt Hàng Cha, giữ nguyên thứ tự người
	dùng khai — mỗi mặt hàng cha một bộ khác nhau (DP01S có 7, DD11S/DPVDS/DXHBC có 5).

	**Giá trị** trả về TOÀN BỘ giá trị trong danh mục Item Attribute, kèm `used_values` là
	những giá trị đang thật sự có biến thể dùng tới.

	⚠ Trước đây chỉ trả giá trị đã có biến thể, với lập luận "chọn giá trị chưa biến thể nào
	dùng thì rule vô nghĩa". Khách báo sai (PM-TASK-00105): họ cần đặt rule TRƯỚC cho những
	giá trị sắp có hàng. Với DP01S thì cách cũ giấu mất 11/24 mức Công suất, 6/10 Chip LED,
	8/18 Nguồn. Giờ hiện hết, nhưng đánh dấu cái nào chưa có biến thể để người dùng không
	tick nhầm mà tưởng đang phủ hàng thật.

	Không xử lý đặc tính kiểu số (`numeric_values`) vì site không dùng — có thì phải sinh giá
	trị từ from_range/to_range/increment thay vì đọc danh mục.
	"""
	if not frappe.db.exists("Item", item_template):
		return {"total_variants": 0, "attributes": []}

	khai_bao = frappe.get_all(
		"Item Variant Attribute",
		filters={"parent": item_template, "parenttype": "Item"},
		pluck="attribute",
		order_by="idx",
	)
	if not khai_bao:
		return {"total_variants": 0, "attributes": []}

	variants = frappe.get_all("Item", filters={"variant_of": item_template}, pluck="name")

	dang_dung = {}
	if variants:
		for row in frappe.get_all(
			"Item Variant Attribute",
			filters={"parent": ["in", variants], "parenttype": "Item"},
			fields=["attribute", "attribute_value"],
			distinct=True,
			limit_page_length=0,
		):
			dang_dung.setdefault(row.attribute, set()).add(row.attribute_value)

	attributes = []
	for attr in khai_bao:
		values = frappe.get_all(
			"Item Attribute Value",
			filters={"parent": attr},
			pluck="attribute_value",
			order_by="idx",
			limit_page_length=0,
		)
		co_bien_the = dang_dung.get(attr, set())
		# Giá trị chỉ có trên biến thể mà không còn trong danh mục (bị xoá khỏi danh mục sau
		# khi đã sinh biến thể) vẫn phải hiện, nếu không rule cũ trỏ vào nó sẽ không sửa được.
		values += sorted(v for v in co_bien_the if v not in values)
		attributes.append(
			{"name": attr, "values": values, "used_values": sorted(co_bien_the)}
		)

	return {"total_variants": len(variants), "attributes": attributes}


@frappe.whitelist()
def count_matched_variants(item_template, cond_attrs):
	"""Đếm biến thể khớp điều kiện — để hộp thoại hiện số ngay khi người dùng đang tick."""
	cond = frappe.parse_json(cond_attrs) or []
	if not cond:
		return {"matched": 0, "sample": []}

	attr_map = get_variant_attr_map(item_template)
	matched = sorted(v for v, attrs in attr_map.items() if variant_matches(cond, attrs))
	return {"matched": len(matched), "sample": matched[:5]}
