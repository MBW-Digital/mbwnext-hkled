# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-1 — Đội Sản Xuất trên Nhân Sự, kèm ràng buộc Bậc Thợ của câu C1.

C1 (Thắng chốt 31/07): Công nhân **bắt buộc** phải có Bậc Thợ. Trước đây chỉ cảnh báo mềm
vì bench cũ có 33/38 nhân sự thiếu dữ liệu; dữ liệu khách restore 31/07 chỉ còn 3 nhân sự
và cả 3 đều đã có Bậc Thợ nên bật ràng buộc cứng được ngay, không phải dọn dữ liệu trước.

Dùng `mandatory_depends_on` chứ không phải `reqd`: Bậc Thợ chỉ bắt buộc với Công nhân,
nhân sự Bán hàng / Kế toán vẫn để trống được.
"""

import frappe

WORK_TEAM_FIELD = "Employee-custom_work_team"
LEVEL_FIELD = "Employee-custom_employee_level"
MANDATORY_CONDITION = 'eval:doc.custom_employee_type=="Công nhân"'


def execute():
	if not frappe.db.exists("Custom Field", WORK_TEAM_FIELD):
		frappe.get_doc(
			{
				"doctype": "Custom Field",
				"dt": "Employee",
				"fieldname": "custom_work_team",
				"label": "Đội Sản Xuất",
				"fieldtype": "Link",
				"options": "Work Team",
				"insert_after": "custom_employee_level",
				"module": "MBWNext HKLed",
				"in_standard_filter": 1,
			}
		).insert(ignore_permissions=True)

	# C1 — bật ràng buộc cứng. Không đụng `reqd` để nhân sự không phải Công nhân vẫn trống được.
	if frappe.db.exists("Custom Field", LEVEL_FIELD):
		frappe.db.set_value(
			"Custom Field",
			LEVEL_FIELD,
			"mandatory_depends_on",
			MANDATORY_CONDITION,
			update_modified=False,
		)

	frappe.clear_cache(doctype="Employee")
