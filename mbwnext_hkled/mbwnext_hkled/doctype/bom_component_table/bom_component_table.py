# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class BOMComponentTable(Document):
	def validate(self):
		if self.component_type == "Cố Định":
			if not self.item:
				frappe.throw(
					_("Row #{0}: Mặt Hàng bắt buộc khi Kiểu Thành Phần là Cố Định").format(self.idx)
				)
			if not self.qty or self.qty <= 0:
				frappe.throw(
					_("Row #{0}: Số Lượng phải lớn hơn 0 khi Kiểu Thành Phần là Cố Định").format(self.idx)
				)
		elif self.component_type == "Theo Rule":
			self.qty = None
			self.item = None
