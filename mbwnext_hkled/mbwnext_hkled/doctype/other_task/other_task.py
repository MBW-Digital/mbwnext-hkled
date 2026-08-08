# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-8 — Công Việc Khác: ghi nhận việc ngoài lệnh sản xuất để tính lương nhân công (mục IV.5, IV.6).

Chốt C5: chia đều chỉ là **giá trị gợi ý ban đầu** — người dùng sửa tay từng dòng được, nhưng
chỉ lưu được khi tổng thời gian các dòng khớp Tổng Thời Gian chung.
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class OtherTask(Document):
	def validate(self):
		self.distribute_time_if_needed()
		self.calculate_wages()
		self.validate_total_time()

	def distribute_time_if_needed(self):
		"""Chia đều khi số dòng đổi hoặc Tổng Thời Gian đổi — chỉ GỢI Ý, không đè lên sửa tay.

		Nhận biết "người dùng đã sửa tay" bằng cách so tổng hiện tại với tổng chung: còn khớp thì
		không đụng vào; đã lệch thì mới coi là cần chia lại (thêm/bớt dòng hoặc đổi tổng).
		"""
		rows = self.get("employees") or []
		if not rows or not self.total_time:
			return

		current_total = sum(flt(r.time) for r in rows)
		if current_total and abs(current_total - flt(self.total_time)) < 0.001:
			return  # đang khớp — giữ nguyên phần người dùng đã sửa

		# Chỉ chia đều khi các dòng còn trống hoặc vừa thêm/bớt dòng.
		if current_total and all(flt(r.time) for r in rows):
			return

		share = flt(self.total_time) / len(rows)
		for row in rows:
			if not flt(row.time):
				row.time = share

	def calculate_wages(self):
		"""Lương nhân công = lương mỗi phút của bậc thợ × thời gian. Tính lại mỗi lần lưu."""
		total = 0.0
		for row in self.get("employees") or []:
			rate = flt(row.earnings_per_minute)
			if not rate and row.employee_level:
				rate = flt(
					frappe.db.get_value("Employee Level", row.employee_level, "earnings_per_minute")
				)
				row.earnings_per_minute = rate
			row.labor_wage = rate * flt(row.time)
			total += flt(row.labor_wage)
		self.total_labor_wage = total

	def validate_total_time(self):
		"""C5 — chặn lưu nếu tổng các dòng không bằng Tổng Thời Gian."""
		rows = self.get("employees") or []
		if not rows:
			return

		total = sum(flt(r.time) for r in rows)
		if abs(total - flt(self.total_time)) < 0.001:
			return

		diff = total - flt(self.total_time)
		frappe.throw(
			_(
				"Tổng thời gian các dòng ({0} phút) phải bằng Tổng Thời Gian ({1} phút). Đang {2} {3} phút."
			).format(
				flt(total, 2),
				flt(self.total_time, 2),
				_("vượt") if diff > 0 else _("thiếu"),
				flt(abs(diff), 2),
			)
		)
