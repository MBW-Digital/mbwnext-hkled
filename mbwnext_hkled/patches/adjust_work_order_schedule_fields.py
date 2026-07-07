# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Align pre-existing Work Order schedule custom fields with PHẦN III spec:
mandatory Start Time, and allow editing Start/End/Estimated/Employee table
after submit since mid-course recalculation happens on live Work Orders."""

import frappe

FIELD_UPDATES = {
	"Work Order-custom_start_time": {"reqd": 1},
	"Work Order-custom_end_time": {"allow_on_submit": 1},
	"Work Order-custom_estimated_completion_time_minutes": {"allow_on_submit": 1},
	"Work Order-custom_work_order_employee": {"allow_on_submit": 1},
}


def execute():
	for cf_name, changes in FIELD_UPDATES.items():
		if not frappe.db.exists("Custom Field", cf_name):
			continue
		for fieldname, value in changes.items():
			frappe.db.set_value("Custom Field", cf_name, fieldname, value, update_modified=False)

	frappe.clear_cache(doctype="Work Order")
