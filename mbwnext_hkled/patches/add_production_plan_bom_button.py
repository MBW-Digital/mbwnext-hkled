# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe


def execute():
	if frappe.db.exists("Custom Field", {"dt": "Production Plan Item", "fieldname": "custom_create_bom"}):
		return

	frappe.get_doc(
		{
			"doctype": "Custom Field",
			"dt": "Production Plan Item",
			"fieldname": "custom_create_bom",
			"label": "Tạo BOM Tự Động",
			"fieldtype": "Button",
			"insert_after": "bom_no",
			"in_list_view": 1,
		}
	).insert(ignore_permissions=True)
