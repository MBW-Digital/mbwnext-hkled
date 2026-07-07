# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Gán module 'MBWNext HKLed' cho các Custom Field thuộc phạm vi dự án này,
để bench export-fixtures xuất đúng và nhất quán."""

import frappe

CUSTOM_FIELDS = [
	"Production Plan Item-custom_create_bom",
	"Item-custom_time_to_manufacture",
	"Employee-custom_employee_type",
	"Employee-custom_employee_level",
	"Employee-custom_performance_factor_",
	"Work Order-custom_start_time",
	"Work Order-custom_end_time",
	"Work Order-custom_estimated_completion_time_minutes",
	"Work Order-custom_required_completion_date__time",
	"Work Order-custom_nhân_công",
	"Work Order-custom_work_order_employee",
]


def execute():
	for name in CUSTOM_FIELDS:
		if frappe.db.exists("Custom Field", name):
			frappe.db.set_value("Custom Field", name, "module", "MBWNext HKLed", update_modified=False)
