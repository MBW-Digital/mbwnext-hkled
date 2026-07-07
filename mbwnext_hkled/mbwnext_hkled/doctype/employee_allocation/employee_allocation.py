# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class EmployeeAllocation(Document):
	def validate(self):
		self.validate_no_overlap()

	def validate_no_overlap(self):
		if not (self.start_time and self.end_time):
			return

		overlapping = frappe.db.sql(
			"""
			select name, work_order, start_time, end_time
			from `tabEmployee Allocation`
			where employee_name = %(employee_name)s
				and name != %(name)s
				and start_time < %(end_time)s
				and end_time > %(start_time)s
			limit 1
			""",
			{
				"employee_name": self.employee_name,
				"name": self.name or "",
				"start_time": self.start_time,
				"end_time": self.end_time,
			},
			as_dict=True,
		)
		if overlapping:
			row = overlapping[0]
			frappe.throw(
				_(
					"Nhân sự {0} đã được phân công vào Lệnh sản xuất {1} từ {2} đến {3}, trùng thời gian"
				).format(
					frappe.bold(self.employee_name),
					frappe.bold(row.work_order),
					row.start_time,
					row.end_time,
				)
			)
