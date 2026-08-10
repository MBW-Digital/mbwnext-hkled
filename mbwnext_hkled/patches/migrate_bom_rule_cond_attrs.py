# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Chuyển BOM Rule sang cấu trúc cond_attrs (chốt của TungDA 07/08 trên PM-FEAT-00007).

Ba việc, đều idempotent:

1. **Đổi tên bảng chứa**: parentfield `bom_rule` -> `bom_rules` (tên theo spec §5, phương án B).
   ⚠ Không dùng phương án A (rule là con của BOM Component Table) dù spec ưu tiên: Frappe không
   hỗ trợ bảng con lồng 2 cấp, dòng cháu không được nạp mà cũng không được ghi xuống DB.
2. **Chuyển điều kiện**: `condition_value` (1 giá trị của riêng thuộc tính "Nguồn")
   -> `cond_attrs` JSON `[{"name": "Nguồn", "values": [<condition_value>]}]`.
3. **Điền `component_code`** cho danh mục BOM Component sẵn có.

⚠ Đọc/ghi bằng `frappe.db` chứ không qua Document: `condition_value` đã bị gỡ khỏi DocType JSON
nên `frappe.get_doc` không còn thấy field đó, nhưng cột trong DB vẫn còn.
"""

import json

import frappe

# Tên tiếng Việt có dấu -> mã ASCII. Mã này mới là khoá bền để Server Script tra công thức;
# tên tiếng Việt lệch một dấu là vỡ mapping (spec §3).
COMPONENT_CODES = {
	"Module": "MODULE",
	"Ốc vít cố định module": "OC_VIT_MODULE",
	"Cầu đấu": "CAU_DAU",
	"Dây điện cấp nguồn": "DAY_DIEN_CAP_NGUON",
	"Chip LED": "CHIP_LED",
	"Ốc vít bắt chip": "OC_VIT_BAT_CHIP",
	"Dây điện đấu chip - Đỏ": "DAY_DIEN_DAU_CHIP_DO",
	"Dây điện đấu chip - Đen": "DAY_DIEN_DAU_CHIP_DEN",
	"Lens": "LENS",
	"Gioăng chip": "GIOANG_CHIP",
	"Ốc vít bắt lens": "OC_VIT_BAT_LENS",
	"Nguồn": "NGUON",
	"Bộ vỏ đèn": "BO_VO_DEN",
	"Hộp carton": "HOP_CARTON",
	"Xốp góc": "XOP_GOC",
}

CONDITION_ATTRIBUTE = "Nguồn"


def execute():
	fill_component_codes()
	migrate_rules_to_component_table()


def fill_component_codes():
	"""Chỉ điền cho bản ghi đang trống — không ghi đè mã người dùng tự đặt."""
	if not frappe.db.has_column("BOM Component", "component_code"):
		return

	for name, code in COMPONENT_CODES.items():
		if not frappe.db.exists("BOM Component", name):
			continue
		if frappe.db.get_value("BOM Component", name, "component_code"):
			continue
		# Mã unique: bản ghi khác đã chiếm mã này thì bỏ qua, để người dùng tự xử.
		if frappe.db.exists("BOM Component", {"component_code": code}):
			continue
		frappe.db.set_value("BOM Component", name, "component_code", code, update_modified=False)


def migrate_rules_to_component_table():
	if not frappe.db.has_column("BOM Rule", "cond_attrs"):
		return

	# Chỉ những dòng còn treo ở cha cũ. Chạy lại lần 2 thì không còn dòng nào -> no-op.
	old_rows = frappe.db.sql(
		"""
		SELECT name, parent, bom_component, item,
		       {condition_value} AS condition_value
		FROM `tabBOM Rule`
		WHERE parenttype = 'BOM Template' AND parentfield = 'bom_rule'
		ORDER BY parent, idx
		""".format(
			condition_value=(
				"condition_value"
				if frappe.db.has_column("BOM Rule", "condition_value")
				else "NULL"
			)
		),
		as_dict=True,
	)
	if not old_rows:
		return

	moved, no_condition = 0, []

	for row in old_rows:
		if row.condition_value:
			cond_attrs = [{"name": CONDITION_ATTRIBUTE, "values": [row.condition_value]}]
		else:
			# Không có giá trị điều kiện thì không dựng nổi cond_attrs. Không đoán: để nguyên
			# parentfield cũ cho dòng đó lộ ra, người dùng tự xử bằng nút Tạo Rule.
			no_condition.append(row.name)
			continue

		frappe.db.set_value(
			"BOM Rule",
			row.name,
			{
				"parentfield": "bom_rules",
				"cond_attrs": json.dumps(cond_attrs, ensure_ascii=False),
				"rule_id": "rule_{0}".format(row.name),
			},
			update_modified=False,
		)
		moved += 1

	frappe.db.commit()

	print(f"  BOM Rule: đã chuyển {moved} dòng sang cond_attrs")
	if no_condition:
		print(
			f"  ⚠ {len(no_condition)} rule không có Giá Trị Điều Kiện nên không chuyển được,"
			f" cần tạo lại bằng nút Tạo Rule: {', '.join(no_condition[:10])}"
		)
