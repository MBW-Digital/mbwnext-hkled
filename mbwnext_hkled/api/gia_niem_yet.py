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

# Hai cách lấy giá vốn cho mặt hàng MUA HÀNG — anh Thắng chuyển yêu cầu của khách 09/09 15:56:
# "khách hàng đang muốn có 2 cách lấy giá vốn: lấy giá trên đơn mua gần nhất và giá vốn tồn kho
#  trung bình, họ muốn có thể lựa chọn được 1 trong 2 cách".
NGUON_DON_MUA = "Đơn mua gần nhất"
NGUON_TON_KHO = "Giá vốn tồn kho trung bình"
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


def luong_tren_phut():
	"""Đơn giá nhân công tính theo phút, khai ở `HKLed Pricing Setting`.

	Chốt của anh Thắng 09/09 17:03: *"bổ sung thêm cho anh ở trong phần cài đặt tỷ lệ 1 trường là
	Lương trên phút — giá vốn của mặt hàng sản xuất em cộng thêm cho anh phần chi phí sản xuất =
	lương trên phút x thời gian sản xuất (thiết lập trong item)"*.
	"""
	return flt(frappe.db.get_single_value("HKLed Pricing Setting", "luong_tren_phut"))


def _chi_phi_san_xuat(ma_hang):
	"""`(tiền công, lương/phút, số phút)` của một đơn vị thành phẩm.

	⚠ Thời gian lấy từ `custom_time_to_manufacture` — trường **đã có sẵn** trên Mặt hàng từ tính
	  năng bậc thợ, không dựng trường mới. Nhãn trên form là *Thời Gian Sản Xuất (Phút)*.

	📌 Đo 09/09 trên cổng 8012: **59.749** mặt hàng Sản xuất/Gia công nhưng chỉ **3 mã** khai thời
	  gian > 0. Nên với gần như mọi mặt hàng, phần này ra **0** và giá vốn không đổi — đó là đúng,
	  không phải hỏng. Chỗ cần nói ra là màn hình, không phải ở đây.
	"""
	phut = frappe.utils.cint(frappe.db.get_value("Item", ma_hang, "custom_time_to_manufacture"))
	luong = luong_tren_phut()
	return luong * phut, luong, phut


def nguon_gia_von_mac_dinh():
	"""Cách lấy giá vốn mặc định cho mặt hàng *Mua hàng*, khai ở `HKLed Pricing Setting`.

	⚠ Chưa khai thì trả `NGUON_DON_MUA` — giữ đúng hành vi đã chạy từ đợt 1, để bật tính năng
	  chọn nguồn KHÔNG âm thầm đổi giá niêm yết của mọi mặt hàng đang có.
	"""
	gt = frappe.db.get_single_value("HKLed Pricing Setting", "nguon_gia_von_mua_hang")
	return gt or NGUON_DON_MUA


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


def _gia_von_ton_kho(ma_hang):
	"""**Bình quân gia quyền** giá vốn tồn kho, gộp mọi kho — `Σ(tồn × giá vốn) / Σ(tồn)`.

	⚠ Phải gia quyền theo số lượng, KHÔNG được lấy trung bình cộng của `valuation_rate`. Một mã
	  nằm ở hai kho, kho A 1.000 cái giá 10.000 và kho B 1 cái giá 50.000: trung bình cộng ra
	  30.000, gia quyền ra 10.040. Trung bình cộng cho một con số **trông vẫn hợp lý** nên sai kiểu
	  này không lộ ra.
	  📌 Đo 09/09 trên cổng 8012: mỗi mã hiện chỉ nằm ở **một kho**, nên hôm nay hai cách ra số y
	  hệt nhau — chỗ khác nhau chỉ lộ khi khách dựng nhiều kho. Đừng lấy "đo thấy giống nhau" làm
	  bằng chứng rằng trung bình cộng cũng được.

	⚠ Bỏ qua dòng tồn ≤ 0. Tồn âm thì `valuation_rate` mất nghĩa, và để lọt vào mẫu số là kéo cả
	  bình quân đi lệch.
	"""
	r = frappe.db.sql(
		"""
		select sum(b.actual_qty * b.valuation_rate) as tu, sum(b.actual_qty) as mau
		from `tabBin` b
		where b.item_code = %s and b.actual_qty > 0 and b.valuation_rate > 0
		""",
		ma_hang,
		as_dict=True,
	)
	if not r or not flt(r[0].mau):
		return None
	gia = flt(r[0].tu) / flt(r[0].mau)
	return gia if gia > 0 else None


def _gia_thanh_bom(ma_hang):
	"""Giá thành của **BOM mặc định đang hoạt động**, quy về một đơn vị thành phẩm.

	⚠ Chia `quantity`: BOM có thể lập cho lô (làm 10 cái một mẻ) — `total_cost` khi đó là giá của
	  cả mẻ. Không chia là giá niêm yết cao gấp `quantity` lần.
	"""
	bom = frappe.db.get_value(
		"BOM",
		{"item": ma_hang, "is_default": 1, "is_active": 1, "docstatus": 1},
		["total_cost", "quantity", "operating_cost", "with_operations"],
		as_dict=True,
	)
	if not bom:
		return None
	sl = flt(bom.quantity) or 1
	tong = flt(bom.total_cost)

	# 🔴 CHỐNG CỘNG ĐÔI. `BOM.total_cost` đã bao gồm `operating_cost` khi định mức bật công đoạn.
	#    Từ 09/09 giá vốn còn cộng thêm *lương/phút × thời gian sản xuất*, nên định mức nào đã có
	#    chi phí công đoạn thì phải TRỪ nó ra, không thì tiền công tính hai lần.
	#    📌 Đo 09/09: 0/13 định mức trên cổng 8012 bật công đoạn, `operating_cost` đều bằng 0 — nên
	#    hôm nay nhánh này không chạy. Nhưng đó là chuyện của hôm nay; để nguyên là bom hẹn giờ.
	if bom.with_operations and flt(bom.operating_cost):
		tong -= flt(bom.operating_cost)

	if tong <= 0:
		return None
	return tong / sl


def cost_cua(ma_hang, phuong_phap, nguon=None):
	"""`(cost, ly_do_neu_khong_co)` — rẽ nhánh theo *Phương pháp bổ sung*.

	Trả `(None, "câu giải thích")` chứ không trả `(0, …)`: xem lý do ở docstring đầu file.

	`nguon` chỉ có nghĩa với mặt hàng **Mua hàng**, nhận `NGUON_DON_MUA` hoặc `NGUON_TON_KHO`;
	để rỗng thì lấy mặc định đã khai trong `HKLed Pricing Setting`.

	⚠ **Không tự động lấy nguồn kia khi nguồn đã chọn không có số.** Người dùng chọn "giá vốn tồn
	  kho" mà hệ thống lặng lẽ trả giá đơn mua thì con số ra **trông vẫn đúng**, chỉ là không phải
	  thứ họ chọn — và chênh lệch có thể rất lớn: đo 09/09, `Test NVL 1` ra 10.000 theo đơn mua và
	  6.000 theo tồn kho, tức giá niêm yết 35.000 so với 20.000. Thà báo "không tính được" kèm lý
	  do nêu rõ đang thiếu gì.
	"""
	if phuong_phap == MUA_HANG:
		if nguon is None:
			nguon = nguon_gia_von_mac_dinh()
		if nguon == NGUON_TON_KHO:
			gia = _gia_von_ton_kho(ma_hang)
			if gia is None:
				return None, _("Mặt hàng chưa có tồn kho nên chưa có giá vốn tồn kho trung bình")
			return gia, None
		gia = _gia_don_mua_gan_nhat(ma_hang)
		if gia is None:
			return None, _("Chưa có đơn mua nào đã duyệt cho mặt hàng này")
		return gia, None

	if phuong_phap in TU_LAM:
		gia = _gia_thanh_bom(ma_hang)
		if gia is None:
			return None, _("Chưa có định mức mặc định, hoặc định mức chưa có giá thành")
		cong, _luong, _phut = _chi_phi_san_xuat(ma_hang)
		return gia + cong, None

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


def ma_co_nguon_cost(nguon=None):
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
	# ⚠ Tập ứng viên của nhánh MUA HÀNG đổi theo nguồn giá vốn đang chọn. Giữ nguyên câu đơn mua
	#   trong khi người dùng đã chuyển sang "giá vốn tồn kho" là lọc theo một tập SAI: mã có đơn
	#   mua mà chưa nhập kho thì lọt vào rồi bị loại, còn mã có tồn mà chưa từng lên đơn mua thì
	#   bị bỏ sót hẳn — và bỏ sót thì không có dấu hiệu nào.
	if (nguon or nguon_gia_von_mac_dinh()) == NGUON_TON_KHO:
		mua = frappe.db.sql_list(
			"""
			select distinct item_code from `tabBin`
			where ifnull(actual_qty, 0) > 0 and ifnull(valuation_rate, 0) > 0
			"""
		)
	else:
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


def _dieu_kien(nhom_hang, mat_hang_cha, tim, ma_gioi_han=None):
	"""WHERE dùng CHUNG cho cả câu đếm lẫn câu lấy dữ liệu.

	🔴 Phải dùng chung, không được viết hai lần. Đếm một kiểu mà lấy một kiểu là ra
	*"trang 7/12"* rồi mở trang 7 thấy rỗng — lệch kiểu đó không có dấu hiệu nào, và trông y hệt
	*"hết dữ liệu"*.
	"""
	dk = ["it.has_variants = 0", "it.disabled = 0"]
	gt = {}
	if nhom_hang:
		dk.append("it.item_group = %(nhom)s")
		gt["nhom"] = nhom_hang
	if mat_hang_cha:
		dk.append("it.variant_of = %(cha)s")
		gt["cha"] = mat_hang_cha
	if tim:
		# Anh Thắng chốt 09/09 14:55: tìm theo CẢ mã lẫn tên, và gõ ĐOẠN GIỮA phải ra
		# ("b) có em nhé"). Nên là `%tim%` hai đầu chứ không phải `tim%` — mã của khách dạng
		# M30S050-…-8C-64LED-DD-…, gõ `64LED` phải ra hết.
		dk.append("(it.name like %(tim)s or it.item_name like %(tim)s)")
		gt["tim"] = "%" + str(tim).strip() + "%"
	if ma_gioi_han is not None:
		dk.append("it.name in %(ma_gh)s")
		gt["ma_gh"] = tuple(ma_gioi_han) or ("",)
	return " and ".join(dk), gt


def _dong_tho(dk, gt, limit_start=None, limit=None):
	sql = """
		select it.name as ma_hang, it.item_name as ten_hang,
		       it.custom_replenishment_method as phuong_phap,
		       it.custom_ty_le_rnd as rnd, it.custom_ty_le_loi_nhuan as loi_nhuan
		from `tabItem` it
		where {dk}
		order by it.name
	""".format(dk=dk)
	if limit is not None:
		sql += " limit %(_start)s, %(_len)s"
		gt = dict(gt, _start=frappe.utils.cint(limit_start), _len=frappe.utils.cint(limit))
	return frappe.db.sql(sql, gt, as_dict=True)


@frappe.whitelist()
def bang_gia(
	nhom_hang=None,
	mat_hang_cha=None,
	chi_tinh_duoc=0,
	chi_lech=0,
	tim=None,
	trang=1,
	moi_trang=100,
	gioi_han=None,
	nguon=None,
):
	"""Dữ liệu cho màn hình **Bảng Giá Niêm Yết**, có phân trang và ô tìm kiếm.

	⚠ Site có hơn 61 nghìn mặt hàng; dựng hết một lượt là treo trình duyệt. Nhưng một bảng bị cắt
	  trông y hệt một bảng đầy đủ — nên hàm luôn trả kèm `tong` / `trang` / `so_trang` để giao
	  diện nói ra *"đang xem trang X trên Y, tổng M"*.

	⚠ `gioi_han` là tên cũ, giữ lại cho script và tài liệu cũ gọi được; nó chính là `moi_trang`.
	"""
	hao_phi, ty_le_ny = ty_le_chung()
	# Rỗng thì lấy mặc định trong Cài đặt. Màn hình gửi giá trị lên khi người dùng đổi ô chọn
	# TẠM trên bảng — xem thử cách kia ra số bao nhiêu mà không phải sửa Cài đặt.
	nguon = nguon or nguon_gia_von_mac_dinh()
	if gioi_han:
		moi_trang = gioi_han
	moi_trang = frappe.utils.cint(moi_trang) or 100
	trang = max(1, frappe.utils.cint(trang) or 1)

	def tra(dong, tong):
		so_trang = max(1, -(-tong // moi_trang))
		return {
			"dong": dong,
			"tong": tong,
			"trang": min(trang, so_trang),
			"moi_trang": moi_trang,
			"so_trang": so_trang,
			"bi_cat": tong > len(dong),
			"hao_phi": hao_phi,
			"ty_le_niem_yet": ty_le_ny,
			"bang_gia": BANG_GIA_BAN,
			"nguon": nguon,
			"nguon_mac_dinh": nguon_gia_von_mac_dinh(),
		}

	# ⚠ Lọc "tính được" / "đang lệch" phải vào TRUY VẤN, không được lọc sau khi cắt — xem
	#   docstring của `ma_co_nguon_cost()`. Cả hai bộ lọc đều chỉ có nghĩa trên tập mã có giá vốn.
	dang_loc = bool(frappe.utils.cint(chi_tinh_duoc) or frappe.utils.cint(chi_lech))

	if dang_loc:
		co_cost = ma_co_nguon_cost(nguon)
		if not co_cost:
			return tra([], 0)
		# ⚠ KHÔNG cắt trang ở đây. `ma_co_nguon_cost()` mới là điều kiện CẦN — mã có đơn mua nhưng
		#   chưa khai Phương pháp bổ sung vẫn lọt vào rồi bị `cost_cua()` loại sau. Cắt trước khi
		#   loại là cắt nhầm đúng như lỗi đã sửa 08/09: tập ứng viên 6 mã mà chỉ 4 mã tính được.
		#   Tập này luôn nhỏ (số mã TỪNG lên đơn mua hoặc CÓ định mức) nên lấy hết là an toàn.
		dk, gt = _dieu_kien(nhom_hang, mat_hang_cha, tim, ma_gioi_han=list(co_cost))
		ds = _dong_tho(dk, gt)
		ra = _tinh_cac_dong(ds, hao_phi, ty_le_ny, nguon)
		if frappe.utils.cint(chi_tinh_duoc):
			ra = [r for r in ra if r["gia_niem_yet"] is not None]
		if frappe.utils.cint(chi_lech):
			ra = [r for r in ra if r["lech"]]
		tong = len(ra)
		dau = (min(trang, max(1, -(-tong // moi_trang))) - 1) * moi_trang
		return tra(ra[dau : dau + moi_trang], tong)

	dk, gt = _dieu_kien(nhom_hang, mat_hang_cha, tim)
	tong = frappe.db.sql(
		"select count(*) from `tabItem` it where {dk}".format(dk=dk), gt
	)[0][0]
	so_trang = max(1, -(-tong // moi_trang))
	dau = (min(trang, so_trang) - 1) * moi_trang
	ds = _dong_tho(dk, gt, limit_start=dau, limit=moi_trang)
	return tra(_tinh_cac_dong(ds, hao_phi, ty_le_ny, nguon), tong)


def _tinh_cac_dong(ds, hao_phi, ty_le_ny, nguon=None):
	"""Tính giá cho một tập dòng đã lấy sẵn — tách ra để hai nhánh phân trang dùng chung."""
	dang_ap = _gia_dang_ap_dung([d.ma_hang for d in ds])
	ra = []
	for d in ds:
		cost, ly_do = cost_cua(d.ma_hang, d.phuong_phap, nguon)
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
	return ra


@frappe.whitelist()
def cap_nhat_gia(ma_hang, nguon=None):
	"""Đẩy giá niêm yết đã tính sang `Item Price` — **chỉ khi người dùng bấm nút**.

	🔴 Chốt trong `notes` của PM Feature: *"Giá niêm yết ở bảng này sẽ không được phép tự động cập
	nhật sang phần bán hàng… người dùng tích chọn item đó trên bảng rồi ấn nút cập nhật giá niêm
	yết thì nó mới cập nhật qua cho sales nhìn thấy, không được tự ý cập nhật"*.

	Lý do nghiệp vụ khách nêu: đổi giá niêm yết làm **lệch hoa hồng của những đơn đã phát sinh**.
	Nên đừng bao giờ gắn hàm này vào hook hay tác vụ nền — nó tồn tại để có một người bấm.

	🔴 `nguon` phải nhận **đúng nguồn giá vốn màn hình đang hiển thị**, không được để hàm tự lấy
	mặc định. Người dùng xem tạm theo *giá vốn tồn kho* thấy 20.000 rồi bấm ghi, mà hàm này lại
	tính theo *đơn mua gần nhất* ra 35.000 — con số đẩy sang sales **khác con số họ vừa nhìn**, và
	không có gì trên màn hình cho thấy điều đó. Đo 09/09 trên `Test NVL 1`: đúng hai con số ấy.
	"""
	if isinstance(ma_hang, str):
		ma_hang = frappe.parse_json(ma_hang)
	if not ma_hang:
		frappe.throw(_("Chưa chọn mặt hàng nào."))

	hao_phi, ty_le_ny = ty_le_chung()
	nguon = nguon or nguon_gia_von_mac_dinh()
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

		cost, ly_do = cost_cua(ma, it.custom_replenishment_method, nguon)
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
def xuat_excel(ma_hang, ty_le_chiet_khau=0, nguon=None):
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

	nguon = nguon or nguon_gia_von_mac_dinh()
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
		cost, _ly_do = cost_cua(ma, it.custom_replenishment_method, nguon)
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


@frappe.whitelist()
def chi_tiet_bom(ma_hang):
	"""Bảng thành phần của một mặt hàng **Sản xuất / Gia công** — bung ra khi bấm vào dòng.

	Khách vẽ đúng bảng này trong ảnh anh Thắng gửi 09/09 17:03: bốn cột *Thành phần BOM* ·
	*Giá trị tồn kho* · *Số lượng* · *Thành tiền*, và **dòng cuối tên là “Sản xuất”** với
	`lương/phút × số phút`. Tổng của bảng phải bằng đúng ô *Giá thành* của dòng cha.

	⚠ Chia cho `BOM.quantity`. Định mức lập cho một mẻ 10 cái thì `qty`/`amount` của từng dòng con
	  là của cả mẻ; không chia là bảng con cao gấp `quantity` lần trong khi dòng cha đã chia rồi —
	  hai con số lệch nhau ngay trên cùng một màn hình.

	⚠ Cột *Giá trị tồn kho* là `BOM Item.rate`. Trên cổng 8012 cả 13 định mức đều đặt
	  `rm_cost_as_per = 'Valuation Rate'` nên `rate` ĐANG là giá trị tồn kho, đúng như tiêu đề khách
	  viết. Định mức nào đổi sang *Price List* hay *Last Purchase Rate* thì con số vẫn hiện ra bình
	  thường mà **không còn đúng tên cột** — nên hàm trả kèm `goc_gia` để màn hình nói ra.
	"""
	bom = frappe.db.get_value(
		"BOM",
		{"item": ma_hang, "is_default": 1, "is_active": 1, "docstatus": 1},
		["name", "quantity", "rm_cost_as_per", "operating_cost", "with_operations"],
		as_dict=True,
	)
	if not bom:
		return {"dong": [], "tong": None, "ly_do": _("Mặt hàng chưa có định mức mặc định")}

	sl = flt(bom.quantity) or 1
	dong = []
	for r in frappe.get_all(
		"BOM Item",
		filters={"parent": bom.name},
		fields=["item_code", "item_name", "qty", "rate", "amount", "stock_uom"],
		order_by="idx",
		limit_page_length=0,
	):
		dong.append(
			{
				"ma": r.item_code,
				"ten": r.item_name or r.item_code,
				"gia": flt(r.rate),
				"so_luong": flt(r.qty) / sl,
				"thanh_tien": flt(r.amount) / sl,
				"dvt": r.stock_uom,
				"la_cong": 0,
			}
		)

	tien_cong, luong, phut = _chi_phi_san_xuat(ma_hang)
	# Luôn hiện dòng Sản xuất, kể cả khi bằng 0 — mặt hàng CHƯA khai thời gian trông y hệt mặt
	# hàng làm xong trong 0 phút. Ẩn đi là giấu mất chỗ cần khai.
	dong.append(
		{
			"ma": None,
			"ten": _("Sản xuất"),
			"gia": luong,
			"so_luong": phut,
			"thanh_tien": tien_cong,
			"dvt": _("phút"),
			"la_cong": 1,
			"chua_khai": not phut,
		}
	)

	# 🔴 Bảng con và dòng cha PHẢI nói cùng một chuyện. Định mức có giá thành 0 (thành phần chưa có
	#    giá trị tồn kho) mà mặt hàng lại khai thời gian sản xuất thì bảng con cộng ra một số dương
	#    — trong khi dòng cha ghi "không tính được". Hai con số chọi nhau trên cùng màn hình, và
	#    người đọc không có cách nào biết bên nào đúng.
	#    Đo 09/09 với lương thử 820đ/phút: `Bán thành phẩm 1` cho bảng con **4.100** còn dòng cha
	#    **không tính được** — đúng ca này.
	#    Giữ nguyên luật cũ (định mức chưa có giá thành ⇒ không tính được) vì giá thành 0 nghĩa là
	#    *chưa khai giá vật tư*, không phải *vật tư miễn phí*; định giá bán chỉ dựa vào tiền công là
	#    sai xa hơn nhiều so với việc báo chưa tính được. Nhưng phải NÓI RA, nên trả kèm `ly_do_cha`.
	cost_cha, ly_do_cha = cost_cua(ma_hang, frappe.db.get_value("Item", ma_hang, "custom_replenishment_method"))

	return {
		"dong": dong,
		"tong": sum(flt(d["thanh_tien"]) for d in dong),
		"cost_cha": cost_cha,
		"ly_do_cha": ly_do_cha,
		"bom": bom.name,
		"goc_gia": bom.rm_cost_as_per,
		"co_cong_doan": bool(bom.with_operations and flt(bom.operating_cost)),
		"luong_tren_phut": luong,
	}
