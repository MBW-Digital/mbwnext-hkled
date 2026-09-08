# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tính và xuất bảng giá niêm yết — PM-FEAT-00045.

Đầu bài: `docs/features/xuat-bang-gia-niem-yet.md`. Mockup: `docs/mockups/xuat-bang-gia-niem-yet.html`.

## Công thức — chép từ trường `notes` của PM Feature, không suy diễn

    cost         = Mua hàng          ➜ giá của ĐƠN MUA GẦN NHẤT
                   Sản xuất/Gia công ➜ giá thành của BOM MẶC ĐỊNH
    Cộng         = cost × (100 + hao phí + R&D + lợi nhuận) / 100
    Giá niêm yết = làm tròn tới bội 5.000 GẦN NHẤT của ( Cộng / tỷ lệ tính giá niêm yết × 100 )

Ba chỗ dễ đọc sai, đã kiểm chéo bốn nguồn (số trong file khách · `notes` · ảnh khách đính chính
anh Thắng · file báo giá) — cả bốn khớp:

1. **`tỷ lệ tính giá niêm yết` là số CHIA, không phải số nhân.** Giá vốn cộng lãi chỉ chiếm ~30%
   giá niêm yết. Nhân thay vì chia là ra con số nhỏ hơn giá vốn, mà vẫn trông như một con số tiền
   bình thường.
2. **Đổi tỷ lệ thì TỬ SỐ giữ nguyên.** Khách nói thẳng: *"giá niêm yết 100k ⇒ trước khi chia là
   30k ⇒ chỉnh tỷ lệ thành 25% ⇒ 30.000/0,25 = 120.000đ"*. Không phải nhân giá niêm yết cũ với gì.
3. **Làm tròn GẦN NHẤT, không phải làm tròn lên** — anh Thắng chốt 08/09 16:39: *"Làm tròn gần
   nhất em nhé"*. `2.947.247 ➜ 2.945.000`, không phải 2.950.000.

## ⚠ Hôm nay gần như không có cost để tính

Đo trên cổng 8012 ngày 08/09: mặt hàng *Mua hàng* có 1.828 mã nhưng chỉ **3** mã có giá mua gần
nhất; *Sản xuất/Gia công* có 59.749 mã nhưng chỉ **1** BOM mặc định có giá thành khác 0. Tức tính
được giá cho khoảng **4 trên 62.061** mặt hàng.

Đó là dữ liệu nghiệp vụ khách phải nạp, không phải lỗi code — nhưng nó quyết định cách viết ở đây:
**mặt hàng không tính được thì trả `None` kèm `ly_do`, KHÔNG trả 0**. Trả 0 là biến "chưa biết"
thành "miễn phí", và con số đó chảy thẳng ra bảng giá gửi cho đại lý.
"""

import frappe
from frappe import _
from frappe.utils import flt

BOI_LAM_TRON = 5000
BANG_GIA_BAN = "Standard Selling"

# Chốt của anh Thắng 08/09 16:39: *"ghi vào bảng giá Standard Selling em nhé"*. Đây cũng là bảng
# giá mặc định của Đơn Bán Hàng trên cổng 8012 (cả 40 đơn đều dùng), nên ghi vào đây là sales mở
# đơn lên thấy ngay ở cột *Đơn giá theo bảng giá* — không phải đổi cấu hình gì thêm.

MUA_HANG = "Mua hàng"
TU_LAM = ("Sản xuất", "Gia công")


def lam_tron_5000(x):
	"""Làm tròn tới bội 5.000 **gần nhất**.

	⚠ Không dùng `round()` trần của Python cho số chia hết đôi: `round(2.5)` ra 2 (làm tròn về số
	chẵn), nên `2.502.500` sẽ ra `2.500.000` thay vì `2.505.000`. Tiền thì phải nhất quán — cộng
	nửa bội rồi cắt sàn cho ra đúng "một nửa trở lên thì lên".
	"""
	if x is None:
		return None
	return int((flt(x) + BOI_LAM_TRON / 2) // BOI_LAM_TRON) * BOI_LAM_TRON


def ty_le_chung():
	"""Hai tỷ lệ dùng chung toàn hệ thống. Trả `(hao_phi, ty_le_niem_yet)`."""
	doc = frappe.get_cached_doc("HKLed Pricing Setting")
	return flt(doc.ty_le_hao_phi), flt(doc.ty_le_tinh_gia_niem_yet)


def _gia_don_mua_gan_nhat(ma_hang):
	"""Giá trên dòng hàng của **đơn mua đã duyệt gần nhất** — quy về đơn vị kho.

	⚠ Đọc `Purchase Order Item` chứ không đọc `Item.last_purchase_rate`. Trường đó của lõi được
	  cập nhật ở vài đường khác nhau và có thể mang giá của một đơn đã huỷ; ở đây cần đúng một
	  thứ: đơn mua **đã duyệt** mới nhất. Đo 08/09: `last_purchase_rate` có ở 3 mã, còn số mã từng
	  lên đơn mua đã duyệt là 5 — hai con số không bằng nhau, nên không thay nhau được.

	⚠ Nhân `conversion_factor`: `rate` đo bằng đơn vị MUA, còn giá niêm yết đo theo đơn vị kho.
	  Đơn mua theo Thùng mà kho tính theo Cái thì thiếu chỗ này là sai đúng bằng số lần quy đổi.
	"""
	dong = frappe.db.sql(
		"""
		select poi.base_rate, poi.conversion_factor
		from `tabPurchase Order Item` poi
		join `tabPurchase Order` po on po.name = poi.parent
		where poi.item_code = %s and po.docstatus = 1
		order by po.transaction_date desc, po.creation desc
		limit 1
		""",
		ma_hang,
		as_dict=True,
	)
	if not dong:
		return None
	cf = flt(dong[0].conversion_factor) or 1
	gia = flt(dong[0].base_rate)
	if gia <= 0:
		return None
	return gia / cf


def _gia_thanh_bom(ma_hang):
	"""Giá thành của **BOM mặc định đang hoạt động**, quy về một đơn vị thành phẩm.

	⚠ Chia `quantity`: BOM có thể lập cho lô (làm 10 cái một mẻ) — `total_cost` khi đó là giá của
	  cả mẻ. Không chia là giá niêm yết cao gấp `quantity` lần.
	"""
	bom = frappe.db.get_value(
		"BOM",
		{"item": ma_hang, "is_default": 1, "is_active": 1, "docstatus": 1},
		["total_cost", "quantity"],
		as_dict=True,
	)
	if not bom:
		return None
	sl = flt(bom.quantity) or 1
	tong = flt(bom.total_cost)
	if tong <= 0:
		return None
	return tong / sl


def cost_cua(ma_hang, phuong_phap):
	"""`(cost, ly_do_neu_khong_co)` — rẽ nhánh theo *Phương pháp bổ sung*.

	Trả `(None, "câu giải thích")` chứ không trả `(0, …)`: xem lý do ở docstring đầu file.
	"""
	if phuong_phap == MUA_HANG:
		gia = _gia_don_mua_gan_nhat(ma_hang)
		if gia is None:
			return None, _("Chưa có đơn mua nào đã duyệt cho mặt hàng này")
		return gia, None

	if phuong_phap in TU_LAM:
		gia = _gia_thanh_bom(ma_hang)
		if gia is None:
			return None, _("Chưa có định mức mặc định, hoặc định mức chưa có giá thành")
		return gia, None

	return None, _("Mặt hàng chưa khai Phương pháp bổ sung")


def tinh_gia(cost, rnd, loi_nhuan, hao_phi, ty_le_ny):
	"""`(cong, gia_niem_yet)` từ giá vốn và bốn tỷ lệ. `cost` rỗng thì trả `(None, None)`."""
	if cost is None:
		return None, None
	cong = flt(cost) * (100 + flt(hao_phi) + flt(rnd) + flt(loi_nhuan)) / 100
	if flt(ty_le_ny) <= 0:
		return cong, None
	return cong, lam_tron_5000(cong / flt(ty_le_ny) * 100)


def _gia_dang_ap_dung(ma_hang_list):
	"""{mã: giá đang nằm trong `Item Price` của bảng giá bán} — con số sales đang nhìn thấy."""
	if not ma_hang_list:
		return {}
	rows = frappe.get_all(
		"Item Price",
		filters={"item_code": ["in", ma_hang_list], "price_list": BANG_GIA_BAN},
		fields=["item_code", "price_list_rate"],
		limit_page_length=0,
	)
	return {r.item_code: flt(r.price_list_rate) for r in rows}


def ma_co_nguon_cost():
	"""Tập mã **có thể** tính được giá vốn — hai truy vấn SQL, không lặp từng mặt hàng.

	🔴 **Vì sao phải có hàm này thay vì lọc sau khi lấy dữ liệu.** Bộ lọc *"chỉ dòng tính được giá"*
	nếu áp SAU khi đã cắt `gioi_han` dòng đầu thì nó chỉ soi trong phần đã cắt — và trả về rỗng
	kèm câu *"không mặt hàng nào tính được giá"*, trong khi thực tế có. Đo 08/09 trên cổng 8012:
	site có 4 mã tính được, tên đều bắt đầu bằng *"Test…"* nên nằm ngoài 200 dòng đầu theo thứ tự
	chữ cái ➜ màn hình báo **0**, sai hoàn toàn mà không có dấu hiệu nào.

	Đúng loại "cắt bớt dữ liệu im lặng": kết quả bị cắt trông y hệt kết quả đầy đủ. Nên bộ lọc phải
	đứng **trước** phép cắt, tức phải nằm trong truy vấn.

	Tập này là điều kiện **cần**, chưa phải đủ: mã có đơn mua nhưng `base_rate = 0` vẫn lọt vào
	đây rồi bị `cost_cua()` loại sau. Đó là hướng an toàn — thà lấy dư rồi loại, còn hơn cắt nhầm.
	"""
	mua = frappe.db.sql_list(
		"""
		select distinct poi.item_code
		from `tabPurchase Order Item` poi
		join `tabPurchase Order` po on po.name = poi.parent
		where po.docstatus = 1 and ifnull(poi.base_rate, 0) > 0
		"""
	)
	tu_lam = frappe.db.sql_list(
		"""
		select distinct item from `tabBOM`
		where is_default = 1 and is_active = 1 and docstatus = 1 and ifnull(total_cost, 0) > 0
		"""
	)
	return set(mua) | set(tu_lam)


@frappe.whitelist()
def bang_gia(nhom_hang=None, mat_hang_cha=None, chi_tinh_duoc=0, chi_lech=0, gioi_han=200):
	"""Dữ liệu cho màn hình **Bảng Giá Niêm Yết**.

	⚠ `gioi_han` có mặc định và **màn hình phải nói ra khi bị cắt**. Site có 62.061 mặt hàng; dựng
	  hết một lượt là treo trình duyệt. Nhưng một bảng bị cắt trông y hệt một bảng đầy đủ — nên
	  hàm trả kèm `tong` và `bi_cat` để giao diện hiện *"đang xem N trên tổng M"*.
	"""
	hao_phi, ty_le_ny = ty_le_chung()

	loc = {"has_variants": 0, "disabled": 0}
	if nhom_hang:
		loc["item_group"] = nhom_hang
	if mat_hang_cha:
		loc["variant_of"] = mat_hang_cha

	# ⚠ Lọc "tính được" / "đang lệch" phải vào TRUY VẤN, không được lọc sau khi cắt — xem
	#   docstring của `ma_co_nguon_cost()`. Cả hai bộ lọc đều chỉ có nghĩa trên tập mã có giá vốn.
	if frappe.utils.cint(chi_tinh_duoc) or frappe.utils.cint(chi_lech):
		co_cost = ma_co_nguon_cost()
		if not co_cost:
			return {
				"dong": [],
				"tong": 0,
				"bi_cat": False,
				"hao_phi": hao_phi,
				"ty_le_niem_yet": ty_le_ny,
				"bang_gia": BANG_GIA_BAN,
			}
		loc["name"] = ["in", list(co_cost)]

	tong = frappe.db.count("Item", loc)
	ds = frappe.get_all(
		"Item",
		filters=loc,
		fields=[
			"name as ma_hang",
			"item_name as ten_hang",
			"custom_replenishment_method as phuong_phap",
			"custom_ty_le_rnd as rnd",
			"custom_ty_le_loi_nhuan as loi_nhuan",
		],
		order_by="name",
		limit_page_length=frappe.utils.cint(gioi_han) or 200,
	)

	dang_ap = _gia_dang_ap_dung([d.ma_hang for d in ds])
	ra = []
	for d in ds:
		cost, ly_do = cost_cua(d.ma_hang, d.phuong_phap)
		cong, gia = tinh_gia(cost, d.rnd, d.loi_nhuan, hao_phi, ty_le_ny)
		ap = dang_ap.get(d.ma_hang)
		ra.append(
			{
				"ma_hang": d.ma_hang,
				"ten_hang": d.ten_hang,
				"phuong_phap": d.phuong_phap,
				"cost": cost,
				"ly_do": ly_do,
				"rnd": flt(d.rnd),
				"loi_nhuan": flt(d.loi_nhuan),
				"cong": cong,
				"gia_niem_yet": gia,
				"dang_ap_dung": ap,
				"lech": gia is not None and ap is not None and gia != ap,
			}
		)

	if frappe.utils.cint(chi_tinh_duoc):
		ra = [r for r in ra if r["gia_niem_yet"] is not None]
	if frappe.utils.cint(chi_lech):
		ra = [r for r in ra if r["lech"]]

	return {
		"dong": ra,
		"tong": tong,
		"bi_cat": tong > len(ds),
		"hao_phi": hao_phi,
		"ty_le_niem_yet": ty_le_ny,
		"bang_gia": BANG_GIA_BAN,
	}


@frappe.whitelist()
def cap_nhat_gia(ma_hang):
	"""Đẩy giá niêm yết đã tính sang `Item Price` — **chỉ khi người dùng bấm nút**.

	🔴 Chốt trong `notes` của PM Feature: *"Giá niêm yết ở bảng này sẽ không được phép tự động cập
	nhật sang phần bán hàng… người dùng tích chọn item đó trên bảng rồi ấn nút cập nhật giá niêm
	yết thì nó mới cập nhật qua cho sales nhìn thấy, không được tự ý cập nhật"*.

	Lý do nghiệp vụ khách nêu: đổi giá niêm yết làm **lệch hoa hồng của những đơn đã phát sinh**.
	Nên đừng bao giờ gắn hàm này vào hook hay tác vụ nền — nó tồn tại để có một người bấm.
	"""
	if isinstance(ma_hang, str):
		ma_hang = frappe.parse_json(ma_hang)
	if not ma_hang:
		frappe.throw(_("Chưa chọn mặt hàng nào."))

	hao_phi, ty_le_ny = ty_le_chung()
	da_doi, bo_qua = [], []

	for ma in ma_hang:
		it = frappe.db.get_value(
			"Item",
			ma,
			["custom_replenishment_method", "custom_ty_le_rnd", "custom_ty_le_loi_nhuan", "stock_uom"],
			as_dict=True,
		)
		if not it:
			bo_qua.append({"ma_hang": ma, "ly_do": _("Không tìm thấy mặt hàng")})
			continue

		cost, ly_do = cost_cua(ma, it.custom_replenishment_method)
		_cong, gia = tinh_gia(cost, it.custom_ty_le_rnd, it.custom_ty_le_loi_nhuan, hao_phi, ty_le_ny)
		if gia is None:
			# Không đẩy một ô trống sang cho sales — thà để giá cũ còn hơn ghi đè bằng 0.
			bo_qua.append({"ma_hang": ma, "ly_do": ly_do or _("Không tính được giá")})
			continue

		ten = frappe.db.get_value(
			"Item Price", {"item_code": ma, "price_list": BANG_GIA_BAN}, "name"
		)
		if ten:
			cu = flt(frappe.db.get_value("Item Price", ten, "price_list_rate"))
			if cu == gia:
				continue
			doc = frappe.get_doc("Item Price", ten)
			doc.price_list_rate = gia
			doc.save(ignore_permissions=True)
			da_doi.append({"ma_hang": ma, "cu": cu, "moi": gia})
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Item Price",
					"item_code": ma,
					"price_list": BANG_GIA_BAN,
					"price_list_rate": gia,
					"uom": it.stock_uom,
				}
			)
			doc.insert(ignore_permissions=True)
			da_doi.append({"ma_hang": ma, "cu": None, "moi": gia})

	return {"da_doi": da_doi, "bo_qua": bo_qua, "bang_gia": BANG_GIA_BAN}


@frappe.whitelist()
def xuat_excel(ma_hang, ty_le_chiet_khau=0):
	"""File Excel 3 cột, cột *Giá bán* mang **công thức sống**.

	Chốt 08/09 16:21: *"chỉ riêng file xuất rút gọn còn 3 cột: cột mã mặt hàng và cột giá niêm
	yết, riêng cột giá bán thì để trống"* và *"em thêm 1 trường tỷ lệ chiết khấu trên file, khi họ
	điền số vào trường đó thì sẽ tự động tính giá bán, file xuất sẽ có công thức sống"*.

	Nên cột *Giá bán* **không ghi số** — ghi công thức trỏ về ô tỷ lệ chiết khấu. Người nhận đổi
	một ô là cả cột đổi theo, không phải xin xuất lại file.
	"""
	from openpyxl import Workbook
	from openpyxl.styles import Alignment, Font
	from openpyxl.utils import get_column_letter

	if isinstance(ma_hang, str):
		ma_hang = frappe.parse_json(ma_hang)
	if not ma_hang:
		frappe.throw(_("Chưa chọn mặt hàng nào để xuất."))

	hao_phi, ty_le_ny = ty_le_chung()

	wb = Workbook()
	ws = wb.active
	ws.title = "Bảng giá niêm yết"

	# Ô tỷ lệ chiết khấu đứng riêng trên đầu — đây là ô DUY NHẤT người nhận phải gõ.
	ws["A1"] = "Tỷ lệ chiết khấu"
	ws["A1"].font = Font(bold=True)
	ws["B1"] = flt(ty_le_chiet_khau) / 100
	ws["B1"].number_format = "0%"
	ws["C1"] = "← gõ số vào ô bên trái, cột Giá bán tự tính"
	ws["C1"].font = Font(italic=True, color="888888")

	tieu_de = ["Mã mặt hàng", "Giá niêm yết", "Giá bán"]
	for i, t in enumerate(tieu_de, start=1):
		o = ws.cell(row=3, column=i, value=t)
		o.font = Font(bold=True)
		o.alignment = Alignment(horizontal="center")

	dong = 4
	for ma in ma_hang:
		it = frappe.db.get_value(
			"Item",
			ma,
			["custom_replenishment_method", "custom_ty_le_rnd", "custom_ty_le_loi_nhuan"],
			as_dict=True,
		)
		if not it:
			continue
		cost, _ly_do = cost_cua(ma, it.custom_replenishment_method)
		_cong, gia = tinh_gia(cost, it.custom_ty_le_rnd, it.custom_ty_le_loi_nhuan, hao_phi, ty_le_ny)
		if gia is None:
			# Mặt hàng không tính được giá thì KHÔNG đưa vào file gửi đại lý — một dòng trống
			# trong bảng báo giá là một câu hỏi cho khách, không phải một thông tin.
			continue
		ws.cell(row=dong, column=1, value=ma)
		o_gia = ws.cell(row=dong, column=2, value=gia)
		o_gia.number_format = "#,##0"
		# CÔNG THỨC, không phải số: đổi B1 là cả cột đổi theo.
		o_ban = ws.cell(row=dong, column=3, value=f"=B{dong}*(1-$B$1)")
		o_ban.number_format = "#,##0"
		dong += 1

	ws.column_dimensions["A"].width = 32
	ws.column_dimensions["B"].width = 16
	ws.column_dimensions["C"].width = 34
	ws.freeze_panes = "A4"

	from io import BytesIO

	buf = BytesIO()
	wb.save(buf)

	ten_file = f"bang-gia-niem-yet-{frappe.utils.nowdate()}.xlsx"
	frappe.local.response.filename = ten_file
	frappe.local.response.filecontent = buf.getvalue()
	frappe.local.response.type = "binary"
