# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""C1 — Công nhân bắt buộc phải có Bậc Thợ (mục II.3 tài liệu nghiệp vụ).

VÌ SAO phải có hook này chứ không chỉ `mandatory_depends_on`:
`mandatory_depends_on` của Frappe **chỉ chạy phía client** — cài đặt nằm ở
`frappe/public/js/frappe/form/save.js` và `layout.js`, không có một dòng Python nào
kiểm nó. Nghĩa là form trên trình duyệt thì bị chặn, nhưng lưu bằng script, API,
Data Import hay từ app khác thì vẫn lọt.

Điều đó quan trọng vì engine tính lịch đọc `custom_performance_factor_` (fetch từ
Bậc Thợ). Công nhân thiếu Bậc Thợ lọt vào bảng Nhân Công Tham Gia sẽ làm
`recalculate_schedule` throw "chưa có Nguồn Lực (%) hợp lệ" — lỗi nổ ở chỗ khác hẳn
nơi dữ liệu bị nhập sai, rất khó lần ra.
"""

import frappe
from frappe import _

WORKER_TYPE = "Công nhân"


def validate_employee_level(doc, method=None):
	"""Chặn lưu Nhân sự loại Công nhân mà chưa gán Bậc Thợ."""
	if doc.doctype != "Employee":
		return
	if doc.get("custom_employee_type") != WORKER_TYPE:
		return
	if doc.get("custom_employee_level"):
		return

	frappe.throw(
		_("Nhân sự {0} là Công nhân nên bắt buộc phải có Bậc Thợ").format(
			frappe.bold(doc.get("employee_name") or doc.name)
		),
		title=_("Thiếu Bậc Thợ"),
	)
