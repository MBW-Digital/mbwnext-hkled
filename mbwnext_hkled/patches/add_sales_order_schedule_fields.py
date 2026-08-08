# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-4 — trường lịch sản xuất trên Đơn Bán Hàng và Kế Hoạch Sản Xuất (mục IV.2, IV.3).

`Sales Order.custom_time` là trường thêm theo câu C4: Thời Điểm Cần Hoàn Thành = `delivery_date`
(Date, không có giờ) **ghép** với `custom_time` (Time). Vì phải ghép 2 trường nên
`custom_required_completion_date_time` bên Production Plan Sales Order **không dùng được**
`fetch_from` — giá trị do code tính, xem `controllers/python_hook/production_plan.py`.

⚠ Sales Order đã có 26 custom field của các app khác (advanced_selling, integration_dms…).
Đã đối chiếu: không trùng fieldname nào, và HKLed chỉ THÊM trường chứ không doc_events trên
Sales Order nên không va chạm ghi dữ liệu với app nào.
"""

import frappe

SALES_ORDER_FIELDS = [
	{
		"fieldname": "custom_hkled_production_section",
		"label": "Thông Tin Sản Xuất",
		"fieldtype": "Section Break",
		"insert_after": "delivery_date",
		"collapsible": 1,
	},
	{
		"fieldname": "custom_start_time",
		"label": "Thời Gian Bắt Đầu",
		"fieldtype": "Datetime",
		"insert_after": "custom_hkled_production_section",
	},
	{
		"fieldname": "custom_time",
		"label": "Giờ Cần Hoàn Thành",
		"fieldtype": "Time",
		"insert_after": "custom_start_time",
		"description": "Ghép với Ngày Giao Hàng thành Thời Điểm Cần Hoàn Thành. Trống thì lấy 00:00.",
	},
	{
		"fieldname": "custom_hkled_column_break",
		"fieldtype": "Column Break",
		"insert_after": "custom_time",
	},
	{
		"fieldname": "custom_note",
		"label": "Ghi Chú Sản Xuất",
		"fieldtype": "Small Text",
		"insert_after": "custom_hkled_column_break",
	},
]

PP_SALES_ORDER_FIELDS = [
	{
		"fieldname": "custom_start_time",
		"label": "Thời Gian Bắt Đầu",
		"fieldtype": "Datetime",
		"insert_after": "sales_order_date",
		"fetch_from": "sales_order.custom_start_time",
		"read_only": 1,
	},
	{
		"fieldname": "custom_required_completion_date_time",
		"label": "Thời Điểm Cần Hoàn Thành",
		"fieldtype": "Datetime",
		"insert_after": "custom_start_time",
		"read_only": 1,
		"description": "Ngày Giao Hàng + Giờ Cần Hoàn Thành của đơn bán. Tính bằng code, không fetch.",
	},
	{
		"fieldname": "custom_work_team",
		"label": "Đội Sản Xuất",
		"fieldtype": "Link",
		"options": "Work Team",
		"insert_after": "custom_required_completion_date_time",
	},
	{
		"fieldname": "custom_note",
		"label": "Ghi Chú Sản Xuất",
		"fieldtype": "Small Text",
		"insert_after": "custom_work_team",
		"fetch_from": "sales_order.custom_note",
		"read_only": 1,
	},
]

PP_SUB_ASSEMBLY_FIELDS = [
	{
		"fieldname": "custom_work_team",
		"label": "Đội Sản Xuất",
		"fieldtype": "Link",
		"options": "Work Team",
		"insert_after": "bom_no",
	},
]


def _create(doctype, fields):
	for spec in fields:
		name = f"{doctype}-{spec['fieldname']}"
		if frappe.db.exists("Custom Field", name):
			continue
		doc = frappe.get_doc(
			{"doctype": "Custom Field", "dt": doctype, "module": "MBWNext HKLed", **spec}
		)
		doc.insert(ignore_permissions=True)


def execute():
	_create("Sales Order", SALES_ORDER_FIELDS)
	_create("Production Plan Sales Order", PP_SALES_ORDER_FIELDS)
	_create("Production Plan Sub Assembly Item", PP_SUB_ASSEMBLY_FIELDS)

	for dt in ("Sales Order", "Production Plan Sales Order", "Production Plan Sub Assembly Item"):
		frappe.clear_cache(doctype=dt)
