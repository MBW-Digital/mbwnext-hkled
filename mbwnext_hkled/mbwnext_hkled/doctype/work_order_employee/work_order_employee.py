# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class WorkOrderEmployee(Document):
	def validate(self):
		if self.employee and frappe.db.get_value("Employee", self.employee, "custom_employee_type") != "Công nhân":
			frappe.throw(
				_("Row #{0}: Nhân Sự {1} phải là Công nhân").format(self.idx, frappe.bold(self.employee))
			)
