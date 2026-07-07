# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, get_time

OVER_TIME_EARLIEST_START = "17:01:00"
OVER_TIME_LATEST_END = "23:59:00"


class EmployeeSchedule(Document):
	def validate(self):
		self.validate_over_time_window()
		self.set_datetime_fields()
		self.validate_unique_schedule()

	def validate_over_time_window(self):
		if not self.is_over_time:
			return

		if get_time(self.start) < get_time(OVER_TIME_EARLIEST_START):
			frappe.throw(_("Khi Tăng Ca, Bắt Đầu chỉ được tính từ 17h01"))
		if get_time(self.end) > get_time(OVER_TIME_LATEST_END):
			frappe.throw(_("Khi Tăng Ca, Kết Thúc chỉ được tính đến 23h59"))

	def set_datetime_fields(self):
		self.start_time = get_datetime(f"{self.date} {self.start}")
		self.end_time = get_datetime(f"{self.date} {self.end}")

	def validate_unique_schedule(self):
		duplicate_start = frappe.db.exists(
			"Employee Schedule",
			{
				"employee_name": self.employee_name,
				"start_time": self.start_time,
				"name": ["!=", self.name],
			},
		)
		if duplicate_start:
			frappe.throw(
				_("Nhân sự {0} đã có Lịch làm việc khác bắt đầu cùng thời điểm {1}").format(
					frappe.bold(self.employee_name), self.start_time
				)
			)

		duplicate_end = frappe.db.exists(
			"Employee Schedule",
			{
				"employee_name": self.employee_name,
				"end_time": self.end_time,
				"name": ["!=", self.name],
			},
		)
		if duplicate_end:
			frappe.throw(
				_("Nhân sự {0} đã có Lịch làm việc khác kết thúc cùng thời điểm {1}").format(
					frappe.bold(self.employee_name), self.end_time
				)
			)
