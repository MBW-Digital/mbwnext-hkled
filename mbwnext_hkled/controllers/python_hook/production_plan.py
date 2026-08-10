# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-4 — tính Thời Điểm Cần Hoàn Thành cho từng dòng Đơn Bán Hàng của Kế Hoạch Sản Xuất.

Vì sao phải tính bằng code thay vì `fetch_from`:
Thời Điểm Cần Hoàn Thành = `Sales Order.delivery_date` (Date, không có giờ) **ghép** với
`Sales Order.custom_time` (Time). `fetch_from` chỉ chép được nguyên một trường, không ghép
được hai trường, nên phải tự tính.

Tính ở `validate` của Production Plan để giá trị luôn đúng dù người dùng thao tác qua giao diện
hay dữ liệu được tạo bằng script — không phụ thuộc client script chạy hay không.
"""

import frappe
from frappe.utils import get_datetime, getdate

# Đơn không khai giờ thì lấy 00:00 của ngày giao — giữ nguyên hành vi cũ, không tự đoán giờ tan ca.
DEFAULT_TIME = "00:00:00"


def combine_delivery_datetime(delivery_date, custom_time):
	"""Ghép Ngày Giao Hàng + Giờ Cần Hoàn Thành thành một mốc thời gian."""
	if not delivery_date:
		return None
	time_part = custom_time or DEFAULT_TIME
	# Time field đọc từ DB ra là timedelta, str() cho "8:00:00" — get_datetime parse được cả hai.
	return get_datetime(f"{getdate(delivery_date)} {time_part}")


def set_required_completion_time(doc, method=None):
	"""Điền Thời Điểm Cần Hoàn Thành cho mọi dòng trong bảng Đơn Bán Hàng của Kế Hoạch Sản Xuất."""
	if doc.doctype != "Production Plan":
		return

	for row in doc.get("sales_orders") or []:
		if not row.sales_order:
			continue

		so = frappe.db.get_value(
			"Sales Order",
			row.sales_order,
			["delivery_date", "custom_time", "custom_start_time", "custom_note"],
			as_dict=True,
		)
		if not so:
			continue

		row.custom_required_completion_date_time = combine_delivery_datetime(
			so.delivery_date, so.custom_time
		)
		# 2 trường dưới có fetch_from nên Frappe tự điền khi lưu qua giao diện; gán lại ở đây
		# để dữ liệu tạo bằng script cũng đầy đủ.
		row.custom_start_time = so.custom_start_time
		row.custom_note = so.custom_note


def set_item_production_note(doc, method=None):
	"""Ghi Chú Sản Xuất cho từng dòng bảng Assembly Items (`po_items`) — PM-TASK-00046.

	Lấy theo ĐÚNG dòng hàng của đơn: `get_so_items()` của ERPNext điền `sales_order_item` = tên dòng
	`Sales Order Item`, nên ghép được 1-1 thay vì áp chung ghi chú đầu đơn cho cả bảng. Dòng nào
	không tra được (kế hoạch lấy từ Yêu cầu vật tư, hoặc người dùng tự thêm) thì lùi về ghi chú đầu
	đơn nếu dòng đó có gắn Đơn Bán Hàng.

	Chỉ điền dòng CÒN TRỐNG — người dùng sửa tay trên kế hoạch thì giữ nguyên, cùng nguyên tắc với
	`python_hook/sales_order.py`.
	"""
	if doc.doctype != "Production Plan":
		return

	for row in doc.get("po_items") or []:
		if (row.get("custom_note") or "").strip():
			continue

		ghi_chu = None
		if row.get("sales_order_item"):
			ghi_chu = frappe.db.get_value("Sales Order Item", row.sales_order_item, "custom_note")
		if not ghi_chu and row.get("sales_order"):
			ghi_chu = frappe.db.get_value("Sales Order", row.sales_order, "custom_note")

		if ghi_chu:
			row.custom_note = ghi_chu
