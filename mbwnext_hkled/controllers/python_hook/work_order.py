# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Đồng bộ Employee Allocation khi Lệnh sản xuất được Finish thực sự (PHẦN III, mục 7.9)."""

import frappe
from frappe.utils import now_datetime


def sync_employee_allocation_on_finish(doc, method=None):
	if doc.status != "Completed" or not doc.get("custom_work_order_employee"):
		return

	finish_time = doc.actual_end_date or now_datetime()

	for row in doc.custom_work_order_employee:
		if not row.allocation_record:
			continue
		frappe.db.set_value("Employee Allocation", row.allocation_record, "end_time", finish_time)
