# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Hai việc chạy ở `Sales Order.validate`:

- `fill_item_production_note` — Ghi Chú Sản Xuất của đơn chảy xuống từng dòng hàng (PM-TASK-00046)
- `chan_giu_cho_vuot_ton` — chặn Số Lượng Giữ Chỗ vượt tồn khả dụng (PM-FEAT-00023)

Vì sao cả hai phải có ở server dù client script đã làm:
client script chỉ chạy khi người dùng thao tác trên giao diện. Đơn tạo bằng API, bằng Data Import
hay bằng script đều lọt — đúng bài học C1 ở `python_hook/employee.py` (`mandatory_depends_on` của
Frappe cũng chỉ chạy phía client).
"""

import frappe
from frappe import _
from frappe.utils import flt


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


def chan_giu_cho_vuot_ton(doc, method=None):
	"""Không cho *Số Lượng Giữ Chỗ* vượt tồn khả dụng (anh Thắng chốt 02/09 12:40).

	Vì sao phải có ở server: cùng bài học C1 ở `python_hook/employee.py` — giao diện có chặn thì
	đơn tạo bằng API / Data Import / script vẫn lọt. Mà con số này KHÔNG chỉ nằm trên đơn của
	mình: `api.kiem_tra_ton_kho.ghim_boi_don_khac` đọc thẳng nó rồi TRỪ khỏi tồn khả dụng của mọi
	đơn khác. Một dòng ghim 99 trên tồn 31 làm các đơn còn lại thấy thiếu ảo 68 cái và đi mua
	hàng không cần mua.

	⚠ **Chỉ chặn khi người dùng TĂNG số.** Tồn có thể tụt sau khi đơn đã lưu (đơn khác ghim thêm,
	  hàng xuất đi), lúc đó giá trị cũ tự nhiên vượt trần. Chặn cứng theo trần hiện tại sẽ khoá
	  luôn những sửa đổi chẳng liên quan gì tới ghim — đúng cái bẫy `validate_schedule_date` của
	  lõi đã giăng ở Yêu Cầu Mặt Hàng (8/8 đơn trên site có ngày giao quá khứ).

	⚠ Chỉ chạy khi ô *Ghim Tồn Khả Dụng* đang tích. Bỏ tích thì con số vẫn nằm đó nhưng không
	  đơn nào bị trừ theo — đúng như mô tả của trường.
	"""
	if doc.doctype != "Sales Order" or not doc.get("custom_ghim_ton_kha_dung"):
		return

	dong = [r for r in (doc.get("items") or []) if flt(r.get("custom_so_luong_giu_cho")) > 0]
	if not dong:
		return

	from mbwnext_hkled.api.kiem_tra_ton_kho import (
		_kha_dung,
		_kho_hop_le,
		_so,
		_ton_thuc_te,
		ghim_boi_don_khac,
	)

	cu = {}
	if not doc.is_new():
		cu = dict(
			frappe.get_all(
				"Sales Order Item",
				filters={"parent": doc.name},
				fields=["name", "custom_so_luong_giu_cho"],
				as_list=True,
			)
		)

	ma_hang = {r.item_code for r in dong}
	kho = _kho_hop_le(doc.company)
	ton = _ton_thuc_te(ma_hang, kho)
	# ⚠ KHÔNG đặt tên biến bỏ đi là `_` ở đây: `_` đang là hàm dịch của Frappe, gán đè lên
	#   nó thì `_("...")` phía dưới nổ `'list' object is not callable` — mà chỗ nổ lại nằm
	#   trong nhánh CHẶN, nên nhìn từ ngoài vẫn thấy "đã chặn", chỉ sai câu thông báo.
	ghim_khac, _canh_bao = ghim_boi_don_khac(tru_don=doc.name)

	# Nhiều dòng cùng một mã thì ăn chung MỘT lượng tồn — phải cộng dồn theo mã, không xét
	# từng dòng độc lập. Xét riêng lẻ thì đơn 3 dòng x 20 cái trên tồn 20 sẽ lọt cả ba.
	da_dung = {}
	for row in dong:
		moi = flt(row.custom_so_luong_giu_cho)
		if moi <= flt(cu.get(row.name, 0)):
			# Không tăng: giữ nguyên phần người dùng không đụng tới, nhưng vẫn tính vào
			# lượng đã dùng để dòng TĂNG ở sau không mượn lại chỗ này.
			da_dung[row.item_code] = da_dung.get(row.item_code, 0) + moi
			continue

		# Dùng CHUNG `_kha_dung` với màn hình Kiểm Tra Tồn Kho — bốn chỗ trong tính năng này
		# từng chép lại cùng một phép trừ, và lỗi anh Thắng bắt 03/09 16:34 là hậu quả trực tiếp.
		#
		# 📌 Nói cho đúng: riêng chỗ NÀY hành vi không đổi. `kha_dung` âm rồi cũng bị `max(0, …)`
		#    che ở cả ngưỡng chặn lẫn câu thông báo, nên trước hay sau đều ra "tối đa 0" — mà 0
		#    là đúng, vì hàng trong kho đã có đơn khác giữ hết. Đổi ở đây là để **không còn công
		#    thức thứ tư**: lần sau ai sửa luật giữ chỗ chỉ phải sửa một hàm, không phải đi tìm
		#    xem còn sót chỗ nào chép lại.
		kha_dung, _hl, _vuot = _kha_dung(ton.get(row.item_code, 0), ghim_khac.get(row.item_code, 0))
		con_lai = kha_dung - da_dung.get(row.item_code, 0)
		tran = min(flt(row.qty), con_lai)

		if moi > tran:
			frappe.throw(
				_(
					"Dòng {0} — {1}: chỉ giữ chỗ được tối đa <b>{2}</b>, không được {3}.<br><br>"
					"Tồn khả dụng còn {4} (đã trừ phần các đơn khác đang giữ), đơn này cần {5}."
				).format(
					row.idx,
					row.item_code,
					_so(max(0.0, tran)),
					_so(moi),
					_so(max(0.0, con_lai)),
					_so(flt(row.qty)),
				),
				title=_("Giữ chỗ vượt tồn khả dụng"),
			)

		da_dung[row.item_code] = da_dung.get(row.item_code, 0) + moi
