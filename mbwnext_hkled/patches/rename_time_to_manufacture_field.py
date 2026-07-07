# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Fix the misspelled fieldname 'custom_time_to_manufature' (missing 'c') on Item,
carrying over existing data to the correctly-spelled 'custom_time_to_manufacture'."""

import frappe
from frappe.model.utils.rename_field import rename_field

OLD_FIELDNAME = "custom_time_to_manufature"
NEW_FIELDNAME = "custom_time_to_manufacture"


def execute():
	old_cf_name = f"Item-{OLD_FIELDNAME}"
	new_cf_name = f"Item-{NEW_FIELDNAME}"

	if not frappe.db.exists("Custom Field", old_cf_name):
		return
	if frappe.db.exists("Custom Field", new_cf_name):
		return

	old_cf = frappe.get_doc("Custom Field", old_cf_name)
	new_cf = frappe.copy_doc(old_cf)
	new_cf.fieldname = NEW_FIELDNAME
	new_cf.label = "Thời Gian Sản Xuất (Phút)"
	new_cf.insert(ignore_permissions=True)

	rename_field("Item", OLD_FIELDNAME, NEW_FIELDNAME)

	frappe.delete_doc("Custom Field", old_cf_name, force=True, ignore_permissions=True)
