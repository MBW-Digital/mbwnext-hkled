# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Cứu các Lệnh sản xuất đang kẹt vì thiếu Thời Gian Bắt Đầu (lỗi anh Thắng báo 08/08/2026).

`Work Order.custom_start_time` là trường bắt buộc, nhưng ERPNext tạo lệnh hàng loạt từ Kế Hoạch Sản
Xuất bằng `flags.ignore_mandatory = True`. Những lệnh sinh ra trước khi có hook `ensure_start_time`
đang nằm trong CSDL với ô đó bỏ trống — **mọi lần Lưu đều báo lỗi**, người dùng không sửa được gì
nữa, kể cả điền tay chính ô đang thiếu (vì bấm Lưu là lỗi ngay).

Từ nay hook `controllers/python_hook/work_order.py::ensure_start_time` chặn ở đầu vào. Patch này
dọn phần đã lỡ sinh ra.

Ghi thẳng bằng `db_set`/`db.set_value` chứ KHÔNG `save()`: chính những chứng từ này đang không lưu
nổi, gọi `save()` là dính lại đúng lỗi cần sửa. Ở đây chỉ điền một ô còn trống nên ghi thẳng là an
toàn — không có logic nghiệp vụ nào phụ thuộc vào vòng validate ở bước này.
"""

import frappe
from frappe.utils import get_datetime, now_datetime


def execute():
	rows = frappe.db.sql(
		"""
		select name, sales_order, planned_start_date, creation
		from `tabWork Order`
		where (custom_start_time is null or custom_start_time = '') and docstatus < 2
		""",
		as_dict=True,
	)
	if not rows:
		return

	da_sua = 0
	for row in rows:
		gio = None

		if row.sales_order:
			gio = frappe.db.get_value("Sales Order", row.sales_order, "custom_start_time")

		if not gio and row.planned_start_date:
			gio = get_datetime(row.planned_start_date)

		# Không tra được nguồn nào thì lấy chính lúc lệnh được tạo — vẫn là mốc thật của chứng từ,
		# hơn hẳn việc để trống làm chứng từ không lưu được.
		if not gio:
			gio = get_datetime(row.creation) if row.creation else now_datetime()

		frappe.db.set_value("Work Order", row.name, "custom_start_time", gio, update_modified=False)
		da_sua += 1

	frappe.db.commit()
	print(f"[mbwnext_hkled] Đã điền Thời Gian Bắt Đầu cho {da_sua} Lệnh sản xuất đang bị kẹt.")
