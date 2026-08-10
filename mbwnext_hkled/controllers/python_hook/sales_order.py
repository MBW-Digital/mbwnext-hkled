# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Ghi Chú Sản Xuất của đơn chảy xuống từng dòng hàng (PM-TASK-00046).

Vì sao phải chặn thêm ở server dù client script đã làm:
client script chỉ chạy khi người dùng thao tác trên giao diện. Đơn tạo bằng API, bằng Data Import
hay bằng script đều lọt — đúng bài học C1 ở `python_hook/employee.py` (`mandatory_depends_on` của
Frappe cũng chỉ chạy phía client).
"""


def fill_item_production_note(doc, method=None):
	"""Điền Ghi Chú Sản Xuất cho các dòng hàng CÒN TRỐNG.

	⚠ Chỉ điền dòng trống, KHÔNG ghi đè dòng đã có nội dung: khách yêu cầu rõ "người dùng có thể
	tự chỉnh sửa Ghi Chú Sản Xuất của từng dòng item". Ghi đè ở đây sẽ xoá mất phần họ vừa sửa mỗi
	lần bấm Lưu.

	Việc đồng bộ khi người dùng SỬA ghi chú ở đầu đơn do `controllers/js/sales_order.js` lo, vì chỉ
	phía client mới biết giá trị cũ để phân biệt "dòng chưa ai đụng vào" với "dòng đã sửa tay".
	"""
	if doc.doctype != "Sales Order":
		return

	ghi_chu = (doc.get("custom_note") or "").strip()
	if not ghi_chu:
		return

	for row in doc.get("items") or []:
		if not (row.get("custom_note") or "").strip():
			row.custom_note = ghi_chu
