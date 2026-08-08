# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Xoá DocType `BOM Rule Group` — chốt của TungDA 07/08 trên PM-FEAT-00007: "Xóa Bom Rule Group
vì không dùng nữa".

Không còn ai tham chiếu: field `BOM Template.rule_group` đã gỡ cùng ngày, khoá tra công thức giờ
là Mặt Hàng Cha và bảng suy nhóm nằm trong Server Script `hkled_resolve_bom_qty`.

An toàn khi xoá:
- Rà lại Link field trỏ tới DocType này trước khi xoá. Còn field nào trỏ tới thì **dừng**, không
  xoá — thà để lại DocType thừa còn hơn làm hỏng một field đang dùng.
- Chỉ xoá đúng 6 mã nhóm do patch `seed_bom_rule_group` nạp. Bản ghi lạ do người dùng tự tạo thì
  giữ lại và dừng, vì không biết họ dùng vào việc gì.
"""

import frappe

SEEDED_GROUPS = ("P01_P03", "D01_D05", "PTX", "XHB", "DQL", "D11_D15")


def execute():
	if not frappe.db.exists("DocType", "BOM Rule Group"):
		return

	referencing = frappe.get_all(
		"DocField",
		filters={"fieldtype": "Link", "options": "BOM Rule Group"},
		fields=["parent", "fieldname"],
	) + frappe.get_all(
		"Custom Field",
		filters={"fieldtype": "Link", "options": "BOM Rule Group"},
		fields=["dt as parent", "fieldname"],
	)
	if referencing:
		where = ", ".join(f"{r.parent}.{r.fieldname}" for r in referencing)
		print(f"  ⚠ Bỏ qua xoá BOM Rule Group — vẫn còn field trỏ tới: {where}")
		return

	unexpected = [
		name
		for name in frappe.get_all("BOM Rule Group", pluck="name")
		if name not in SEEDED_GROUPS
	]
	if unexpected:
		print(
			f"  ⚠ Bỏ qua xoá BOM Rule Group — có bản ghi không nằm trong 6 nhóm seed:"
			f" {', '.join(unexpected)}"
		)
		return

	frappe.delete_doc("DocType", "BOM Rule Group", force=True, ignore_permissions=True)
	frappe.db.commit()
	print("  Đã xoá DocType BOM Rule Group và 6 bản ghi nhóm công thức")
