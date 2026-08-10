# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tạo Kế Hoạch Sản Xuất thẳng từ Đơn Bán Hàng (PM-TASK-00047).

ERPNext v15 KHÔNG có sẵn đường này: `Sales Order` không có mục Kế Hoạch Sản Xuất trong nút *Create*
(đã kiểm `erpnext/selling/doctype/sales_order/sales_order.js`). Cách làm sẵn có là mở Kế Hoạch Sản
Xuất rồi *Get Items From > Sales Order* rồi tự tìm lại đơn — đúng thứ khách muốn bỏ.

Dùng `get_mapped_doc` thay vì tự dựng doc rồi trả `as_dict()`: hàm này lo phần đặt tên tạm và cờ
`__islocal` để `frappe.model.open_mapped_doc` phía client mở được form chưa lưu, giống hệt mọi nút
Create khác của ERPNext — không phải tự chế cơ chế riêng.
"""

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc

from mbwnext_hkled.controllers.python_hook.production_plan import combine_delivery_datetime


@frappe.whitelist()
def make_production_plan(source_name, target_doc=None):
	"""Đơn Bán Hàng → Kế Hoạch Sản Xuất, kéo sẵn dòng hàng và thông tin sản xuất."""

	def postprocess(source, target):
		target.company = source.company
		target.get_items_from = "Sales Order"

		# Bảng Đơn Bán Hàng của kế hoạch: điền luôn các trường sản xuất thay vì trông vào
		# `fetch_from`. Doc này CHƯA lưu nên vòng fetch của Frappe (chạy trong `_validate_links`
		# lúc insert) chưa xảy ra — người dùng sẽ thấy các ô trống ngay khi form vừa mở.
		# Cùng họ với bẫy đã ghi ở `python_hook/work_order.py`.
		target.append(
			"sales_orders",
			{
				"sales_order": source.name,
				"sales_order_date": source.transaction_date,
				"customer": source.customer,
				"grand_total": source.grand_total,
				"custom_start_time": source.get("custom_start_time"),
				"custom_required_completion_date_time": combine_delivery_datetime(
					source.get("delivery_date"), source.get("custom_time")
				),
				"custom_note": source.get("custom_note"),
			},
		)

		# Kéo dòng hàng của đơn vào bảng Assembly Items (`po_items`).
		target.get_items()

		if not target.get("po_items"):
			frappe.throw(
				_(
					"Đơn Bán Hàng {0} không có dòng hàng nào cần sản xuất. "
					"Kiểm tra lại: mặt hàng đã có Định Mức Nguyên Vật Liệu (BOM) đang hoạt động chưa, "
					"và số lượng đã được tạo Lệnh sản xuất hết chưa."
				).format(source.name)
			)

		_fill_item_note(source, target)

	return get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Production Plan",
				"validation": {"docstatus": ["=", 1]},
			}
		},
		target_doc,
		postprocess,
	)


def _fill_item_note(source, target):
	"""Chép Ghi Chú Sản Xuất của từng dòng hàng sang đúng dòng Assembly Items (PM-TASK-00046).

	`get_so_items()` của ERPNext điền `sales_order_item` = tên dòng `Sales Order Item`, nên ghép
	được chính xác theo từng dòng chứ không phải áp chung ghi chú đầu đơn cho cả bảng.
	"""
	ghi_chu_theo_dong = {}
	for row in source.get("items") or []:
		if row.get("custom_note"):
			ghi_chu_theo_dong[row.name] = row.custom_note

	mac_dinh = source.get("custom_note")

	for row in target.get("po_items") or []:
		if row.get("custom_note"):
			continue
		row.custom_note = ghi_chu_theo_dong.get(row.get("sales_order_item")) or mac_dinh
