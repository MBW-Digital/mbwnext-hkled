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
			key = (row.item_to_manufacture, row.bom_component)
			if key in seen:
				frappe.throw(
					_(
						"Row #{0}: Công Thức BOM bị trùng cho Mặt Hàng Sản Xuất {1} và Thành Phần BOM {2}"
					).format(row.idx, frappe.bold(row.item_to_manufacture), frappe.bold(row.bom_component))
				)
			seen.add(key)

	def validate_rule_items(self):
		for row in self.bom_rule:
			if not frappe.db.get_value("Item", row.item_to_manufacture, "variant_of"):
				frappe.throw(
					_("Row #{0}: Mặt Hàng Sản Xuất {1} phải là mặt hàng biến thể").format(
						row.idx, frappe.bold(row.item_to_manufacture)
					)
				)
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


@frappe.whitelist()
def get_template_attributes(item_template):
	"""Trả về danh sách đặc tính và toàn bộ giá trị đặc tính của item cha (Item Template)."""
	item = frappe.get_doc("Item", item_template)
	result = []
	for row in item.attributes:
		attr_doc = frappe.get_cached_doc("Item Attribute", row.attribute)
		result.append(
			{
				"attribute": row.attribute,
				"values": [v.attribute_value for v in attr_doc.item_attribute_values],
			}
		)
	return result


@frappe.whitelist()
def get_matching_variants(item_template, combos):
	"""Trả về danh sách item biến thể của item_template khớp với ít nhất 1 tổ hợp
	giá trị đặc tính trong combos (mỗi combo là dict {attribute: value})."""
	if isinstance(combos, str):
		combos = frappe.parse_json(combos)

	all_variants = frappe.get_all("Item", filters={"variant_of": item_template}, pluck="name")
	if not all_variants:
		return []

	matched_items = set()
	for combo in combos:
		if not combo:
			continue
		candidates = set(all_variants)
		for attribute, value in combo.items():
			matched_rows = frappe.get_all(
				"Item Variant Attribute",
				filters={
					"parent": ["in", list(candidates)],
					"attribute": attribute,
					"attribute_value": value,
				},
				pluck="parent",
			)
			candidates &= set(matched_rows)
			if not candidates:
				break
		matched_items |= candidates

	return sorted(matched_items)
