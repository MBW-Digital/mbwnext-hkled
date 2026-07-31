# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class BOMTemplate(Document):
	def validate(self):
		self.validate_item_template()
		self.validate_unique_components()
		self.validate_unique_rules()
		self.validate_rule_items()
		self.validate_single_active_template()

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

	def validate_unique_rules(self):
		seen = set()
		for row in self.bom_rule:
			key = (row.bom_component, row.condition_value)
			if key in seen:
				frappe.throw(
					_(
						"Row #{0}: Công Thức BOM bị trùng cho Thành Phần BOM {1} và Giá Trị Điều Kiện {2}"
					).format(row.idx, frappe.bold(row.bom_component), frappe.bold(row.condition_value))
				)
			seen.add(key)

	def validate_rule_items(self):
		for row in self.bom_rule:
			if frappe.db.get_value("Item", row.item, "has_variants"):
				frappe.throw(
					_("Row #{0}: Nguyên Vật Liệu {1} không được là mặt hàng Template").format(
						row.idx, frappe.bold(row.item)
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


# Đặc tính quyết định việc chọn NVL cho thành phần "Theo Rule".
# Trên site hkled.com đặc tính này tên là "Nguồn" (tài liệu thiết kế gọi là "Loại nguồn").
CONDITION_ATTRIBUTE = "Nguồn"

# Gợi ý Nhóm Công Thức theo prefix mã Item Template (mục 2.2 tài liệu thiết kế).
# Chỉ dùng để điền sẵn cho người dùng, người dùng vẫn sửa được.
RULE_GROUP_BY_PREFIX = (
	(("DP01", "DP02", "DP03"), "P01_P03"),
	(("DD01", "DD02", "DD03", "DD04", "DD05"), "D01_D05"),
	(("DPTC", "DPTR", "DPXH", "DPTV", "DPVL", "DPKD"), "PTX"),
	(("DXHB",), "XHB"),
	(("DDQL",), "DQL"),
	(("DD11", "DD12", "DD13", "DD14", "DD15"), "D11_D15"),
)


@frappe.whitelist()
def get_rule_condition_values(item_template):
	"""Trả về danh sách giá trị đặc tính điều kiện (Nguồn) đang thực sự được dùng bởi
	các biến thể của item_template — dùng để sinh sẵn dòng BOM Rule (mục 2.4 tài liệu thiết kế).

	Không sinh ma trận toàn bộ biến thể: mỗi giá trị "Nguồn" chỉ cần 1 dòng.
	Nếu item cha chưa có biến thể nào, lấy toàn bộ giá trị khai báo trong Item Attribute.
	"""
	variants = frappe.get_all("Item", filters={"variant_of": item_template}, pluck="name")
	values = []
	if variants:
		values = frappe.get_all(
			"Item Variant Attribute",
			filters={"parent": ["in", variants], "attribute": CONDITION_ATTRIBUTE},
			pluck="attribute_value",
			distinct=True,
		)
	if not values:
		values = frappe.get_all(
			"Item Attribute Value",
			filters={"parent": CONDITION_ATTRIBUTE},
			pluck="attribute_value",
			order_by="idx",
		)

	return {"attribute": CONDITION_ATTRIBUTE, "values": sorted(set(values))}


@frappe.whitelist()
def suggest_rule_group(item_template):
	"""Gợi ý Nhóm Công Thức từ prefix mã Item Template. None nếu chưa có nhóm nào phù hợp."""
	for prefixes, rule_group in RULE_GROUP_BY_PREFIX:
		if item_template.startswith(prefixes):
			return rule_group if frappe.db.exists("BOM Rule Group", rule_group) else None
	return None
