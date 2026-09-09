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
from frappe import _
from frappe.utils import flt, get_datetime, getdate

from mbwnext_hkled.api.kiem_tra_ton_kho import _so

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


def canh_bao_vuot_phan_thieu(doc, method=None):
	"""Nói ra khi kế hoạch đặt NHIỀU HƠN phần còn thiếu của đơn (PM-TASK-00188).

	## Vì sao cần, dù nút tạo kế hoạch đã trừ đúng

	Nút *Tạo ➜ Kế Hoạch Sản Xuất* trừ phần đã giữ chỗ **một lần, lúc tạo**. Nhưng trong màn hình
	Kế hoạch còn nút *Lấy mặt hàng* của ERPNext lõi, và nó **tính lại từ đầu bằng công thức của
	lõi** — không biết gì về giữ chỗ.

	🔴 Đo thật trên cổng 8012 ngày 08/09, `SO-26-00026` (đặt 40, giữ chỗ 31):

	    tạo kế hoạch từ đơn  ➜  Số Lượng Kế Hoạch = 9   ✅
	    bấm *Lấy mặt hàng*   ➜  Số Lượng Kế Hoạch = 40  ❌ không một lời nào

	Đúng loại hỏng mà cả Phần IV sinh ra để chặn: **con số sai trông y hệt con số đúng**. Người
	lập kế hoạch không có cách nào biết mình vừa mất phần trừ.

	## ⚠ CHỈ nói ra, KHÔNG tự sửa số

	Đặt nhiều hơn phần thiếu là chuyện **hợp lệ**: làm dôi ra để tồn kho, gộp lô cho đủ mẻ, hoặc
	cố ý bỏ qua phần giữ chỗ. Tự trừ ở đây là đè lên tay người dùng và làm hỏng cả những lần sửa
	có chủ ý. Cùng cách xử lý anh Thắng đã chọn cho phiếu Yêu Cầu Mặt Hàng: hệ thống nói ra, người
	quyết.
	"""
	if doc.doctype != "Production Plan" or doc.get("get_items_from") != "Sales Order":
		return

	from mbwnext_hkled.api.production_plan import chi_tiet_dong_don, tru_theo_dong

	po_items = doc.get("po_items") or []
	chi_tiet = chi_tiet_dong_don([r.get("sales_order_item") for r in po_items])
	if not chi_tiet:
		return

	refs = doc.get("prod_plan_references") or []
	giu = {k: v["giu"] for k, v in chi_tiet.items()}
	vuot = []
	for row in po_items:
		giu_dong = tru_theo_dong(row, refs, giu)
		if not giu_dong:
			continue

		d = chi_tiet.get(row.get("sales_order_item"))
		if not d:
			continue

		# ⚠ KHÔNG dùng `row.pending_qty` làm mốc. Trường đó của lõi nghĩa là *"phần của DÒNG KẾ
		#   HOẠCH này chưa sản xuất xong"* (`planned_qty − produced_qty`, production_plan.py:545),
		#   nên nút tạo kế hoạch đã hạ nó xuống cùng `planned_qty` — lấy nó trừ tiếp phần giữ chỗ
		#   là **trừ hai lần**. Đo 08/09: ca "đặt đúng 9 trên phần thiếu 9" vẫn nổ cảnh báo.
		#   Tính lại từ đơn gốc thì không phụ thuộc thứ tự ai ghi đè trường nào.
		#
		# `wo` đếm Lệnh sản xuất của MỌI kế hoạch; `ordered_qty` là phần lệnh do CHÍNH dòng này
		# đẻ ra. Không trừ đi thì lần lưu lại sau khi đã tạo lệnh sẽ tự tố cáo chính mình.
		wo_khac = flt(d["wo"]) - flt(row.get("ordered_qty"))
		da_co = max(wo_khac, flt(d["dl"]), 0)
		con_thieu = flt(d["qty"]) - da_co - giu_dong
		con_thieu = con_thieu if con_thieu > 0 else 0

		if flt(row.planned_qty) - con_thieu > 1e-9:
			vuot.append((row.idx, row.item_code, flt(row.planned_qty), con_thieu, giu_dong))

	if not vuot:
		return

	dong = "".join(
		f"<tr><td>{idx}</td><td>{ma}</td><td style='text-align:right'>{_so(dat)}</td>"
		f"<td style='text-align:right'>{_so(giu_cho)}</td><td style='text-align:right'><b>{_so(thieu)}</b></td></tr>"
		for idx, ma, dat, thieu, giu_cho in vuot
	)
	frappe.msgprint(
		_(
			"Kế hoạch đang đặt <b>nhiều hơn phần còn thiếu</b> của đơn bán. Phần chênh đã có hàng "
			"giữ chỗ trong kho, làm thêm là làm dôi ra.<br><br>"
			"<table class='table table-bordered'><thead><tr><th>STT</th><th>Mặt hàng</th>"
			"<th>Đang đặt</th><th>Đã giữ chỗ</th><th>Còn thiếu</th></tr></thead><tbody>{0}</tbody></table>"
			"Cố ý làm dôi thì bỏ qua câu này. Nếu vừa bấm <i>Lấy mặt hàng</i> thì số đã bị tính lại "
			"theo cách của hệ thống lõi — phần trừ giữ chỗ mất, sửa tay lại cột <i>Số lượng dự kiến</i>."
		).format(dong),
		title=_("Đặt nhiều hơn phần còn thiếu"),
		indicator="orange",
	)
