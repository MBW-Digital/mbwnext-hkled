# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-3 + GAP-7 — cờ Đã Bắt Đầu Sản Xuất và bảng Sản Lượng Nhân Viên trên Lệnh sản xuất.

`custom_production_started` (GAP-3, chốt C8): cần một cờ RIÊNG để biết đã ấn nút hay chưa.
Không dùng được "custom_start_time trống hay không" vì trường đó là Mandatory nên luôn có giá
trị ngay từ lúc tạo lệnh (giờ dự kiến).

Cả hai đều `allow_on_submit = 1` vì đụng tới lệnh đã submit: nút Bắt Đầu Sản Xuất chỉ ấn khi
lệnh đang In Process, còn bảng sản lượng thì sửa tay sau khi Finish (C12).
"""

import frappe

WORK_ORDER_FIELDS = [
	{
		"fieldname": "custom_production_started",
		"label": "Đã Bắt Đầu Sản Xuất",
		"fieldtype": "Check",
		"insert_after": "custom_start_time",
		"read_only": 1,
		"allow_on_submit": 1,
		"description": "Bật khi ấn nút Bắt Đầu Sản Xuất. Chỉ ấn được một lần.",
	},
	{
		"fieldname": "custom_employee_production_section",
		"label": "Sản Lượng Nhân Viên",
		"fieldtype": "Section Break",
		"insert_after": "custom_work_order_employee",
		"allow_on_submit": 1,
	},
	{
		"fieldname": "custom_employee_production",
		"label": "Sản Lượng Nhân Viên",
		"fieldtype": "Table",
		"options": "Employee Production",
		"insert_after": "custom_employee_production_section",
		"allow_on_submit": 1,
	},
]


def execute():
	for spec in WORK_ORDER_FIELDS:
		name = f"Work Order-{spec['fieldname']}"
		if frappe.db.exists("Custom Field", name):
			# Đã có thì vẫn đảm bảo cờ allow_on_submit đúng — thiếu cờ này là chức năng
			# sửa sau submit vỡ, mà lỗi báo ra rất khó đoán ("Not allowed to change...").
			frappe.db.set_value("Custom Field", name, "allow_on_submit", 1, update_modified=False)
			continue

		frappe.get_doc(
			{"doctype": "Custom Field", "dt": "Work Order", "module": "MBWNext HKLed", **spec}
		).insert(ignore_permissions=True)

	frappe.clear_cache(doctype="Work Order")
