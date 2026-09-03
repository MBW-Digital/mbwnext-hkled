# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tính nhu cầu vật tư cần mua theo kỳ — Phần V (PM-FEAT-00030).

Đầu bài: `docs/features/phan-v-tinh-toan-nhu-cau-vat-tu-can-mua-theo-ky.md`.

Module này là **bước 2** của thứ tự làm trong đầu bài: engine tính, **CHỈ ĐỌC**.
Không tạo BOM, không tạo đơn mua, không ghi một bản ghi nào. Việc tạo chứng từ
nằm ở tab Lập kế hoạch (bước 4), phải qua một cú bấm rõ ràng của người dùng.

## Bốn bước, đúng thứ tự

1. Dựng các kỳ  →  2. Gom nhu cầu theo kỳ  →  3. Nổ định mức  →  4. Trừ tồn + kéo tồn qua kỳ.

## Ba chỗ dễ sai nhất, đều đã có ví dụ kiểm chứng trong đầu bài

- **Kéo tồn qua kỳ (mục 3.2).** Từ 2 kỳ trở lên KHÔNG được tính mỗi kỳ độc lập từ cùng một tồn
  ban đầu — nhu cầu kỳ trước đã ăn vào tồn. Ví dụ của tài liệu: min 50, tồn 60, nhu cầu 30/tuần,
  2 tuần → đúng là **50**, tính độc lập ra **40**, tức mua thiếu 10 và tuần 2 tụt dưới mức tối
  thiểu mà không có gì báo.
- **Chống trừ trùng (mục 3.3).** Ở Kiểu 1, đơn bán vừa là nguồn *Nhu cầu* vừa là thứ đang giữ chỗ
  *Tồn*. Mỗi đơn chỉ được tính đúng MỘT vế — xem `_ghim_ngoai_ky`.
- **Thứ tự nổ định mức (mục 4.2).** BOM → BOM Template → liệt kê cho người dùng. Nhánh giữa là
  điểm khác của HKLED: khách không nuôi BOM sẵn.

## Vì sao dùng lại hàm của `kiem_tra_ton_kho`

Phần IV đã giải đúng ba bài toán mà Phần V cần y hệt: kho nào được tính tồn (`_kho_hop_le`), tồn
thực tế gom một query (`_ton_thuc_te`), và **ghim lan xuống NVL mà không đếm hai lần**
(`ghim_boi_don_khac`). Cái thứ ba từng sai một lần ở Phần IV — đơn giữ 20 thì hệ thống hiểu 40 —
nên chép lại là gần như chắc chắn sai lại.

Riêng phần miễn trừ đơn thì dùng đúng tham số `tru_don` có sẵn, chứ không tự trừ ra ở ngoài: giữ
cho toàn bộ nhánh "ghim lan xuống nguyên vật liệu" chỉ có MỘT bản duy nhất trong cả app.

⚠ Đổi lại là Phần V phụ thuộc chữ ký ba hàm đó. Đổi chữ ký thì chỗ này gãy ngay lúc import — gãy
ồn ào, chấp nhận được hơn nhiều so với hai bản logic lệch nhau âm thầm ra hai con số khác nhau.
"""

import frappe
from frappe import _
from frappe.utils import add_days, add_months, flt, get_datetime, getdate, nowdate

from mbwnext_hkled.api.bom import get_active_template, resolve_components
from mbwnext_hkled.api.kiem_tra_ton_kho import _kho_hop_le, _ton_thuc_te, ghim_boi_don_khac

# ── Hằng số ───────────────────────────────────────────────────────────────────

KIEU_THEO_DON = "1"
KIEU_THEO_LICH_SU = "2"

# Đầu bài mục 2: Kiểu 1 chia nhiều kỳ, Kiểu 2 là MỘT khoảng duy nhất (Thắng chốt 19/08 12:52).
LOAI_KY = ("Ngày", "Tuần", "Tháng")

# Chặn quét quá dài. Tính theo SỐ KỲ chứ không theo tổng số ngày: 52 kỳ tuần là một năm, đủ cho
# mọi ca lập kế hoạch khách nêu, mà vẫn giữ bảng ở kích thước người đọc được.
MAX_SO_KY = 52

PP_CHE_BIEN = ("Sản xuất", "Gia công")

# Đầu bài mục 4.1: mặt hàng Gia công sinh THÊM một dòng đơn mua dịch vụ, Finished Good = mặt hàng
# đó. Mã dịch vụ đã có sẵn trên site (`item_group` = Dịch vụ, không quản kho). Không tìm thấy thì
# vẫn trả kết quả nhưng kèm cảnh báo — thiếu mã dịch vụ không được làm hỏng cả bảng nhu cầu.
MA_DICH_VU_GIA_CONG = "dịch vụ gia công"


# ── Kỳ ────────────────────────────────────────────────────────────────────────


def _cac_ky(loai_ky, so_ky, tu_ngay=None):
	"""[(chỉ số, ngày đầu, ngày cuối)] — các kỳ liên tiếp, không hở ngày, không chồng ngày.

	Ngày cuối là ngày **cuối cùng thuộc kỳ**, không phải ngày đầu kỳ sau: xếp đơn vào kỳ bằng
	`ngay_dau <= mốc <= ngay_cuoi` nên hai kỳ liền nhau mà dùng chung một mốc là đơn bị đếm hai lần.
	"""
	so_ky = int(so_ky or 1)
	if loai_ky not in LOAI_KY:
		frappe.throw(_("Loại kỳ {0} không hợp lệ — chỉ nhận: {1}").format(loai_ky, ", ".join(LOAI_KY)))
	if so_ky < 1:
		frappe.throw(_("Số kỳ phải từ 1 trở lên"))
	if so_ky > MAX_SO_KY:
		frappe.throw(_("Tối đa {0} kỳ, đang chọn {1}").format(MAX_SO_KY, so_ky))

	moc = getdate(tu_ngay or nowdate())
	ky = []
	for i in range(so_ky):
		if loai_ky == "Ngày":
			dau, cuoi = moc, moc
			moc = add_days(moc, 1)
		elif loai_ky == "Tuần":
			dau, cuoi = moc, add_days(moc, 6)
			moc = add_days(moc, 7)
		else:
			dau = moc
			moc = add_months(moc, 1)
			cuoi = add_days(moc, -1)
		ky.append({"chi_so": i + 1, "tu": str(dau), "den": str(cuoi)})
	return ky


def _ky_cua(moc, cac_ky):
	"""Chỉ số kỳ (0-based) chứa mốc thời gian này; None nếu rơi ngoài toàn bộ khoảng."""
	if not moc:
		return None
	ngay = getdate(moc)
	for i, k in enumerate(cac_ky):
		if getdate(k["tu"]) <= ngay <= getdate(k["den"]):
			return i
	return None


# ── Dữ liệu nền ───────────────────────────────────────────────────────────────


def _ton_toi_thieu(ma_hang, company):
	"""{mã: mức tồn tối thiểu ở công ty này} — `Item Default` (PM-FEAT-00037).

	⚠ Lọc theo **company**, và mặt hàng không có dòng cho công ty đó thì coi mức tối thiểu = 0.
	Tuyệt đối không lấy dòng đầu tiên: chốt 03/09 của anh Thắng là mức tối thiểu lưu **theo từng
	công ty**, nên lấy bừa dòng của công ty khác là ra số sai mà không có gì báo — đúng loại lỗi
	âm thầm mà đầu bài mục 10 cảnh báo.
	"""
	if not ma_hang:
		return {}
	rows = frappe.get_all(
		"Item Default",
		filters={"parent": ["in", list(ma_hang)], "company": company},
		fields=["parent", "custom_ton_kho_kha_dung_toi_thieu as toi_thieu"],
	)
	return {r["parent"]: flt(r["toi_thieu"]) for r in rows if flt(r["toi_thieu"]) > 0}


def _po_chua_ve(ma_hang, cac_ky):
	"""{mã: [số lượng về ở từng kỳ]} — hàng đã đặt mua nhưng chưa nhận.

	⚠ Xếp đúng kỳ theo **ngày dự kiến nhận**, không dồn hết vào kỳ 1 (đầu bài mục 3.2). Dồn vào
	kỳ 1 là hệ thống tưởng hàng về sớm hơn thực tế → báo đủ ở kỳ đầu rồi thiếu ở kỳ sau.

	Hàng lẽ ra đã về mà chưa về (ngày dự kiến đã qua) thì tính vào **kỳ đầu tiên**: nó đang trên
	đường, bỏ hẳn đi là báo thiếu ảo. Hàng dự kiến về SAU kỳ cuối thì bỏ — nó không giúp gì cho
	khoảng đang tính.
	"""
	trong = {}
	if not ma_hang or not cac_ky:
		return trong

	dong = frappe.get_all(
		"Purchase Order Item",
		filters={
			"item_code": ["in", list(ma_hang)],
			"docstatus": 1,
			"parent": ["in", frappe.get_all(
				"Purchase Order",
				filters={"docstatus": 1, "status": ["not in", ["Closed", "Completed"]]},
				pluck="name",
			) or [""]],
		},
		fields=["item_code", "qty", "received_qty", "schedule_date", "expected_delivery_date"],
	)

	ngay_dau = getdate(cac_ky[0]["tu"])
	for d in dong:
		con_lai = flt(d["qty"]) - flt(d["received_qty"])
		if con_lai <= 0:
			continue
		ngay = d.get("expected_delivery_date") or d.get("schedule_date")
		if ngay and getdate(ngay) < ngay_dau:
			i = 0                                   # quá hạn nhận -> vẫn đang về, tính kỳ đầu
		else:
			i = _ky_cua(ngay, cac_ky)
			if i is None:
				continue                            # về sau kỳ cuối, hoặc không có ngày -> bỏ
		trong.setdefault(d["item_code"], [0.0] * len(cac_ky))
		trong[d["item_code"]][i] += con_lai
	return trong


# ── Nổ định mức: BOM -> BOM Template -> liệt kê (đầu bài mục 4.2) ─────────────


def _bom_mac_dinh(ma_hang):
	"""{mã: tên BOM mặc định} — một query cho cả tập."""
	if not ma_hang:
		return {}
	rows = frappe.get_all(
		"BOM",
		filters={"item": ["in", list(ma_hang)], "is_active": 1, "is_default": 1, "docstatus": 1},
		fields=["name", "item"],
	)
	return {r["item"]: r["name"] for r in rows}


def _dong_bom(ten_bom):
	"""[(mã NVL, định mức cho MỘT đơn vị thành phẩm)]."""
	bom = frappe.get_cached_doc("BOM", ten_bom)
	sl = flt(bom.quantity) or 1.0
	return [(d.item_code, flt(d.stock_qty or d.qty) / sl) for d in bom.items]


def _thanh_phan_theo_template(ma, bo_nho):
	"""[{item_code, qty}] cho MỘT đơn vị, tra qua BOM Template. `None` nếu mã không có Template.

	⚠ Có bộ nhớ đệm là **bắt buộc**, không phải tối ưu cho vui. `resolve_qty_by_formula` chạy một
	Server Script cho **từng thành phần của từng biến thể** — đo trên 8012: 0,0225 s/thành phần,
	tức 0,4 s cho mỗi mặt hàng thành phẩm. Quy mô Thắng chốt là 250–350 dòng mỗi kỳ (mục 6.2), nên
	không đệm thì một lần bấm Tính toán mất khoảng **2 phút** — đo thật, 300 mã chạy quá 120 s.

	Đệm theo `(mã, template)`, sống trong MỘT lần gọi `tinh_nhu_cau`: cùng một bán thành phẩm xuất
	hiện dưới nhiều thành phẩm, và cả cây được nổ lại ở từng kỳ. Đo được: 40 mã từ 15,6 s xuống
	5,9 s.

	⚠ **Đệm này KHÔNG gỡ được trần hiệu năng.** Mỗi biến thể vẫn phải chạy Server Script riêng, nên
	chi phí tuyến tính theo SỐ BIẾN THỂ KHÁC NHAU: đo 03/09 trên 8012 là **~0,15 s/biến thể**, tức
	300 biến thể ≈ **44 giây**. Đã thử thêm một tầng đệm sống xuyên request (Redis, khoá gắn dấu
	vân tay của BOM Template + BOM Rule + Server Script) và **bỏ đi**: nó không rút được lần bấm
	ĐẦU — mà đó mới là lần người dùng phải chờ — trong khi mở thêm đường trả số cũ nếu dấu vân tay
	sót nguồn nào.

	➜ Chỗ phải sửa nằm ở `resolve_qty_by_formula` của `api/bom.py`: `run_script` **biên dịch lại
	Server Script cho từng thành phần từng biến thể**. Đo bằng cProfile trên 60 mã: 2,6 s ở
	`builtins.compile` + 10,4 s đi bộ cây AST, trên tổng 17,9 s. Gọi Server Script MỘT lần cho cả
	lô thành phần sẽ rút được phần lớn — và rút cho cả Phần I. Nhưng `api/bom.py` dùng chung với
	Phần I nên **không tự sửa**; đã nêu để chốt.
	"""
	template = get_active_template(ma)
	if not template:
		return None
	khoa = (ma, template)
	if khoa not in bo_nho:
		bo_nho[khoa] = resolve_components(ma, template)
	return bo_nho[khoa]


def no_dinh_muc(nhu_cau, canh_bao=None, chua_no_duoc=None, gia_cong=None, da_tham=None, bo_nho=None):
	"""Nổ {mã: SL} xuống nguyên vật liệu lá. Trả về {mã NVL: tổng SL}.

	Thứ tự tra định mức đúng theo đầu bài mục 4.2 — anh Thắng chốt 02/09 11:14:

	    có BOM                            -> dùng BOM
	    chưa có BOM nhưng có BOM Template -> nổ theo BOM Template
	    không có cả hai                   -> liệt kê ra cho người dùng kiểm

	⚠ Nhánh giữa gọi `resolve_components` — hàm **chỉ đọc**, KHÔNG gọi `auto_create_bom`. Tạo BOM
	  thật submit chứng từ và gỡ cờ `is_default` của BOM cũ; việc đó phải qua một cú bấm rõ ràng,
	  không được xảy ra lúc người dùng chỉ bấm Tính toán.

	⚠ Gom hết rồi mới trừ tồn MỘT LẦN ở ngoài, không trừ tại từng nhánh — trừ sớm thì cùng một
	  lượng tồn bị đếm cho nhiều nhánh của cây định mức.

	⚠ `da_tham` chặn định mức lặp vòng. Khách khẳng định không có, nhưng đó là *tình trạng dữ liệu*
	  chứ không phải ràng buộc hệ thống — một vòng lặp làm treo tiến trình chứ không báo lỗi.
	"""
	canh_bao = canh_bao if canh_bao is not None else []
	chua_no_duoc = chua_no_duoc if chua_no_duoc is not None else []
	gia_cong = gia_cong if gia_cong is not None else {}
	da_tham = da_tham if da_tham is not None else set()
	bo_nho = bo_nho if bo_nho is not None else {}
	ket = {}

	ma = [m for m, sl in nhu_cau.items() if flt(sl) > 0]
	if not ma:
		return ket

	pp = {}
	for r in frappe.get_all(
		"Item", filters={"name": ["in", ma]}, fields=["name", "custom_replenishment_method"]
	):
		pp[r["name"]] = (r.get("custom_replenishment_method") or "").strip()

	che_bien = [m for m in ma if pp.get(m) in PP_CHE_BIEN]
	bom_cua = _bom_mac_dinh(che_bien)

	for m in ma:
		sl = flt(nhu_cau[m])

		# Mua hàng, hoặc bỏ trống Phương pháp bổ sung -> chính nó là thứ phải mua.
		if pp.get(m) not in PP_CHE_BIEN:
			ket[m] = ket.get(m, 0.0) + sl
			continue

		# Gia công sinh THÊM một dòng dịch vụ, rồi vẫn nổ định mức như hàng sản xuất: ERPNext bắt
		# công ty cấp NVL cho nhà cung cấp gia công (phần Supplied Items). Nên đây là nhánh thứ
		# BA, không phải nhánh con của Sản xuất — khách nói "giống cả dạng sản xuất lẫn mua hàng".
		if pp.get(m) == "Gia công":
			gia_cong[m] = gia_cong.get(m, 0.0) + sl

		if m in da_tham:
			canh_bao.append(_("{0}: định mức lặp vòng, dừng nổ tại đây").format(m))
			ket[m] = ket.get(m, 0.0) + sl
			continue

		thanh_phan = None
		ten_bom = bom_cua.get(m)
		if ten_bom:
			thanh_phan = [{"item_code": c, "qty": dm} for c, dm in _dong_bom(ten_bom)]
		else:
			# `resolve_components` trả định mức cho MỘT đơn vị thành phẩm, cùng chuẩn với
			# `_dong_bom` ở trên — hai nhánh phải cùng chuẩn thì nhân với `sl` mới đúng.
			thanh_phan = _thanh_phan_theo_template(m, bo_nho)

		if not thanh_phan:
			# Không có cả BOM lẫn BOM Template. KHÔNG coi như phải mua chính nó: với hàng sản xuất
			# thì mua thành phẩm là sai hẳn nghiệp vụ. Liệt kê ra để người dùng xử lý — đúng
			# nhánh thứ ba của mục 4.2.
			chua_no_duoc.append(
				{"ma": m, "so_luong": sl, "ly_do": _("chưa có BOM lẫn BOM Template")}
			)
			continue

		con = {}
		for tp in thanh_phan:
			con[tp["item_code"]] = con.get(tp["item_code"], 0.0) + flt(tp["qty"]) * sl
		sau = no_dinh_muc(con, canh_bao, chua_no_duoc, gia_cong, da_tham | {m}, bo_nho)
		for nvl, sl_con in sau.items():
			ket[nvl] = ket.get(nvl, 0.0) + sl_con

	return ket


# ── Nhu cầu ───────────────────────────────────────────────────────────────────


def _nhu_cau_kieu_1(cac_ky, canh_bao):
	"""{mã thành phẩm: [SL từng kỳ]} từ đơn bán, xếp kỳ theo *Thời Gian Bắt Đầu*.

	Trả thêm danh sách tên đơn được tính, để `_ghim_ngoai_ky` biết đơn nào đã nằm ở vế Nhu cầu.

	⚠ Đầu bài mục 6.1: 9/16 đơn đã duyệt đang để TRỐNG ô *Thời Gian Bắt Đầu*. Đơn để trống không
	  rơi vào kỳ nào — phải nêu **đích danh số đơn** trong cảnh báo, tuyệt đối không bỏ lặng lẽ.
	  Bỏ im là mặt hàng của đơn đó biến mất khỏi mọi con số mà không ai biết.

	⚠ Chỉ lấy nhu cầu từ đơn bán, KHÔNG cộng thêm từ Lệnh sản xuất (đầu bài mục 4.4 + checklist
	  mục 7): một đơn đã sinh Lệnh sản xuất mà cộng cả hai nguồn là đếm trùng.
	"""
	don = frappe.get_all(
		"Sales Order",
		filters={"docstatus": 1, "status": ["not in", ["Closed", "Completed", "Cancelled"]]},
		fields=["name", "custom_start_time"],
	)
	if not don:
		return {}, []

	trong_ky, thieu_moc = {}, []
	for d in don:
		if not d.get("custom_start_time"):
			thieu_moc.append(d["name"])
			continue
		i = _ky_cua(get_datetime(d["custom_start_time"]).date(), cac_ky)
		if i is not None:
			trong_ky[d["name"]] = i

	if thieu_moc:
		canh_bao.append(
			_("{0} đơn bán đã duyệt bị bỏ qua vì trống Thời Gian Bắt Đầu — không xếp được vào kỳ nào: {1}")
			.format(len(thieu_moc), ", ".join(sorted(thieu_moc)))
		)

	if not trong_ky:
		return {}, []

	nhu_cau = {}
	for r in frappe.get_all(
		"Sales Order Item",
		filters={"parent": ["in", list(trong_ky)], "docstatus": 1},
		fields=["parent", "item_code", "qty", "delivered_qty"],
	):
		# Phần đã giao không còn là nhu cầu tương lai — nó đã làm `Bin.actual_qty` giảm thật rồi.
		con_lai = flt(r["qty"]) - flt(r["delivered_qty"])
		if con_lai <= 0:
			continue
		i = trong_ky[r["parent"]]
		nhu_cau.setdefault(r["item_code"], [0.0] * len(cac_ky))
		nhu_cau[r["item_code"]][i] += con_lai

	return nhu_cau, list(trong_ky)


def _nhu_cau_kieu_2(tu_ngay, den_ngay, lui_thang, canh_bao):
	"""{mã: SL} — lượng bán thật của khoảng cùng độ dài, lùi về trước `lui_thang` tháng.

	⚠ Kiểu 2 KHÔNG chia kỳ (Thắng chốt 19/08 12:52). Khoảng tham chiếu luôn **cùng độ dài** với
	  khoảng đích nên **lấy thẳng tổng lượng bán**, không quy bình quân/ngày rồi nhân lại — quy
	  bình quân chỉ đúng khi hai khoảng khác độ dài, mà ở đây thì không.
	"""
	tu, den = getdate(tu_ngay), getdate(den_ngay)
	if den < tu:
		frappe.throw(_("Đến Ngày phải từ Từ Ngày trở đi"))

	tham_tu = add_months(tu, -int(lui_thang))
	tham_den = add_months(den, -int(lui_thang))

	don = frappe.get_all(
		"Sales Order",
		filters={
			"docstatus": 1,
			"status": ["not in", ["Cancelled"]],
			"transaction_date": ["between", [str(tham_tu), str(tham_den)]],
		},
		pluck="name",
	)
	if not don:
		canh_bao.append(
			_("Khoảng tham chiếu {0} → {1} không có đơn bán nào — không tính được nhu cầu Kiểu 2")
			.format(tham_tu, tham_den)
		)
		return {}, (str(tham_tu), str(tham_den))

	nhu_cau = {}
	for r in frappe.get_all(
		"Sales Order Item",
		filters={"parent": ["in", don], "docstatus": 1},
		fields=["item_code", "qty"],
	):
		nhu_cau[r["item_code"]] = nhu_cau.get(r["item_code"], 0.0) + flt(r["qty"])
	return nhu_cau, (str(tham_tu), str(tham_den))


# ── Chống trừ trùng (đầu bài mục 3.3) ─────────────────────────────────────────


def _ghim_ngoai_ky(don_trong_ky):
	"""{mã: SL bị giữ chỗ} — CHỈ tính đơn ghim nằm NGOÀI các kỳ đang tính.

	Đây là mục 3.3 của đầu bài, và là chỗ dễ sai nhất sau phần kéo tồn. Ở Kiểu 1, nhu cầu tương
	lai **cũng lấy từ đơn bán**. Một đơn vừa bị trừ ở vế Tồn (vì đang ghim) vừa được cộng ở vế
	Nhu cầu là **trừ hai lần**:

	    tồn 100 · đơn #1 ghim 20 (bắt đầu trong kỳ) · đơn #2 ghim 30 (ngoài kỳ)
	    đúng : Nhu cầu kỳ 1 = 20 · Tồn khả dụng = 100 − 30 = 70 · Khả dụng = 70 − 20 = 50
	    sai  : trừ cả #1 vào tồn -> 30

	> Mỗi đơn bán chỉ được tính đúng MỘT vế.

	Miễn trừ bằng chính tham số `tru_don` của Phần IV — nó nhận cả một tên lẫn một DANH SÁCH tên
	(HkLed2 mở rộng cho PM-FEAT-00034). Nhờ vậy toàn bộ phần **ghim lan xuống nguyên vật liệu**
	vẫn do đúng một hàm lo. Bản đầu của hàm này tự dựng lại nhánh đó rồi trừ ra — chạy đúng, nhưng
	là bản thứ hai của đoạn logic từng đếm hai lần ở Phần IV, tức là chỗ chờ sẵn để lệch về sau.
	"""
	return ghim_boi_don_khac(tru_don=list(don_trong_ky) if don_trong_ky else None)


# ── Trừ tồn + kéo tồn qua kỳ (đầu bài mục 3.1 và 3.2) ─────────────────────────


def _tinh_mot_ma(ton_dau, toi_thieu, nhu_cau_ky, po_ky, bo_qua_po=False):
	"""Chạy công thức kéo tồn qua từng kỳ cho MỘT mặt hàng.

	    Khả dụng    = Tồn đầu kỳ + PO về trong kỳ − Nhu cầu trong kỳ
	    Cần mua     = max(0, Tồn tối thiểu − Khả dụng)
	    Tồn cuối kỳ = Khả dụng + Cần mua          -> chính là Tồn đầu kỳ sau

	`bo_qua_po=True` chạy lại đúng công thức đó nhưng coi như chưa đặt mua gì. Đầu bài mục 8 cần
	cả hai con số: hiển thị **"120 (70)"** — 120 là phần phải mua nếu chưa đặt gì, 70 là phần còn
	phải mua thêm sau khi trừ hàng đang về. Không phải hai công thức khác nhau, chỉ là cùng công
	thức chạy hai lần.
	"""
	ket, ton = [], flt(ton_dau)
	for i in range(len(nhu_cau_ky)):
		ve = 0.0 if bo_qua_po else flt(po_ky[i])
		nhu_cau = flt(nhu_cau_ky[i])
		kha_dung = ton + ve - nhu_cau
		can_mua = max(0.0, flt(toi_thieu) - kha_dung)
		ton_cuoi = kha_dung + can_mua
		ket.append({
			"ton_dau_ky": round(ton, 4),
			"po_ve": round(ve, 4),
			"nhu_cau": round(nhu_cau, 4),
			"kha_dung": round(kha_dung, 4),
			"can_mua": round(can_mua, 4),
			"ton_cuoi_ky": round(ton_cuoi, 4),
		})
		ton = ton_cuoi
	return ket


# ── Đầu vào chính ─────────────────────────────────────────────────────────────


@frappe.whitelist()
def tinh_nhu_cau(
	kieu=KIEU_THEO_DON,
	company=None,
	loai_ky="Tuần",
	so_ky=4,
	tu_ngay=None,
	den_ngay=None,
	lui_thang=12,
):
	"""Tính nhu cầu vật tư cần mua. **Chỉ đọc** — không tạo BOM, không tạo đơn mua.

	Kiểu 1 (theo đơn hàng): dùng `loai_ky` + `so_ky`, nhu cầu lấy từ đơn bán rơi vào từng kỳ.
	Kiểu 2 (theo kết quả bán trước đó): dùng `tu_ngay` + `den_ngay` + `lui_thang`, MỘT kỳ duy nhất.

	Kết quả **chỉ mang tính tham khảo tại thời điểm bấm Tính toán**, không chốt cứng (đầu bài mục 1).
	"""
	kieu = str(kieu)
	canh_bao, chua_no_duoc, gia_cong = [], [], {}
	company = company or frappe.defaults.get_user_default("Company") or frappe.db.get_value(
		"Company", {}, "name"
	)
	if not company:
		frappe.throw(_("Chưa xác định được Công ty — mức tồn tối thiểu lưu theo từng công ty"))

	# ── 1. Kỳ + nhu cầu thành phẩm ───────────────────────────────────────────
	khoang_tham_chieu = None
	if kieu == KIEU_THEO_DON:
		cac_ky = _cac_ky(loai_ky, so_ky, tu_ngay)
		nhu_cau_tp, don_trong_ky = _nhu_cau_kieu_1(cac_ky, canh_bao)
	elif kieu == KIEU_THEO_LICH_SU:
		if not (tu_ngay and den_ngay):
			frappe.throw(_("Kiểu 2 phải nhập Từ Ngày và Đến Ngày"))
		cac_ky = [{"chi_so": 1, "tu": str(getdate(tu_ngay)), "den": str(getdate(den_ngay))}]
		mot_ky, khoang_tham_chieu = _nhu_cau_kieu_2(tu_ngay, den_ngay, lui_thang, canh_bao)
		nhu_cau_tp = {m: [sl] for m, sl in mot_ky.items()}
		don_trong_ky = []
	else:
		frappe.throw(_("Kiểu tính {0} không hợp lệ — chỉ nhận 1 hoặc 2").format(kieu))

	# ── 2. Nổ định mức từng kỳ ───────────────────────────────────────────────
	# Nổ theo TỪNG kỳ chứ không nổ tổng rồi chia: định mức không tuyến tính theo kỳ khi một mặt
	# hàng chỉ xuất hiện ở vài kỳ. Nổ tổng rồi chia đều là rải nhu cầu sang những kỳ vốn không có.
	so_ky_that = len(cac_ky)
	nhu_cau_nvl = {}
	# MỘT bộ nhớ đệm cho cả vòng lặp: cây định mức được nổ lại ở từng kỳ, và cùng một bán thành
	# phẩm xuất hiện dưới nhiều thành phẩm — không dùng chung thì trả giá Server Script mỗi lần.
	bo_nho = {}
	for i in range(so_ky_that):
		mot_ky = {}
		for m, sl in nhu_cau_tp.items():
			if flt(sl[i]) > 0:
				mot_ky[m] = sl[i]
		if not mot_ky:
			continue
		for nvl, sl in no_dinh_muc(mot_ky, canh_bao, chua_no_duoc, gia_cong, None, bo_nho).items():
			nhu_cau_nvl.setdefault(nvl, [0.0] * so_ky_that)
			nhu_cau_nvl[nvl][i] += sl

	if not nhu_cau_nvl:
		return {
			"kieu": kieu, "company": company, "cac_ky": cac_ky, "dong": [],
			"canh_bao": canh_bao + [_("Không có nhu cầu nào trong khoảng đã chọn")],
			"chua_no_duoc": chua_no_duoc, "gia_cong": [],
			"khoang_tham_chieu": khoang_tham_chieu,
		}

	ma_hang = list(nhu_cau_nvl)

	# ── 3. Tồn khả dụng — cùng một cơ sở với Phần IV (đầu bài mục 5) ─────────
	kho = _kho_hop_le(company)
	ton = _ton_thuc_te(ma_hang, kho)

	if kieu == KIEU_THEO_DON:
		giu_cho, cb_ghim = _ghim_ngoai_ky(don_trong_ky)
	else:
		# Kiểu 2: nhu cầu là lịch sử bán, không trùng đơn hiện tại -> trừ TOÀN BỘ phần ghim.
		giu_cho, cb_ghim = ghim_boi_don_khac()
	canh_bao.extend(cb_ghim or [])

	toi_thieu = _ton_toi_thieu(ma_hang, company)
	po = _po_chua_ve(ma_hang, cac_ky)

	# ⚠ "Chưa khai mức tối thiểu" KHÁC "mức tối thiểu = 0" — phải nói ra, không được để 0 trôi
	# lặng vào công thức. Đo 03/09: 0/62.055 mặt hàng đã khai. Với mức 0 thì công thức chỉ còn báo
	# thiếu khi tồn tụt xuống ÂM, tức mất hẳn phần đệm an toàn mà cả tính năng này sinh ra để lo.
	# Bảng vẫn ra số đúng theo dữ liệu đang có, nhưng người đọc phải biết mình đang đọc cái gì.
	if not toi_thieu:
		canh_bao.append(
			_("Chưa mặt hàng nào trong bảng được khai Tồn Kho Khả Dụng Tối Thiểu cho công ty {0} —"
			  " kết quả chỉ phản ánh phần thiếu so với nhu cầu, KHÔNG có phần đệm tồn an toàn")
			.format(frappe.bold(company))
		)

	# ── 4. Chạy công thức ────────────────────────────────────────────────────
	ten_hang = {}
	for r in frappe.get_all(
		"Item", filters={"name": ["in", ma_hang]},
		fields=["name", "item_name", "stock_uom", "custom_replenishment_method"],
	):
		ten_hang[r["name"]] = r

	dong = []
	for m in ma_hang:
		ton_dau = flt(ton.get(m, 0.0)) - flt(giu_cho.get(m, 0.0))
		po_ky = po.get(m) or [0.0] * so_ky_that
		theo_ky = _tinh_mot_ma(ton_dau, toi_thieu.get(m, 0.0), nhu_cau_nvl[m], po_ky)
		khong_po = _tinh_mot_ma(
			ton_dau, toi_thieu.get(m, 0.0), nhu_cau_nvl[m], po_ky, bo_qua_po=True
		)
		tong_can_mua = sum(k["can_mua"] for k in theo_ky)
		if tong_can_mua <= 0 and sum(k["can_mua"] for k in khong_po) <= 0:
			continue                                  # không thiếu ở kỳ nào -> không đưa vào bảng

		info = ten_hang.get(m) or {}
		dong.append({
			"ma": m,
			"ten": info.get("item_name"),
			"don_vi": info.get("stock_uom"),
			"pp_bo_sung": (info.get("custom_replenishment_method") or "").strip() or None,
			"ton_kha_dung": round(ton_dau, 4),
			"ton_toi_thieu": round(flt(toi_thieu.get(m, 0.0)), 4),
			# Cho màn hình phân biệt được "khai là 0" với "chưa khai" — hai thứ này ra cùng một
			# con số nhưng nghĩa hoàn toàn khác nhau.
			"da_khai_toi_thieu": m in toi_thieu,
			"ky": theo_ky,
			# Mục 8: "120 (70)" — trước ngoặc là phần phải mua nếu chưa đặt gì, trong ngoặc là
			# phần CÒN phải mua thêm sau khi trừ hàng đang về.
			"tong_can_mua": round(sum(k["can_mua"] for k in khong_po), 4),
			"con_phai_mua": round(tong_can_mua, 4),
		})

	dong.sort(key=lambda d: (-flt(d["con_phai_mua"]), d["ma"]))

	return {
		"kieu": kieu,
		"company": company,
		"cac_ky": cac_ky,
		"khoang_tham_chieu": khoang_tham_chieu,
		"dong": dong,
		"gia_cong": _dong_gia_cong(gia_cong, canh_bao),
		"chua_no_duoc": chua_no_duoc,
		"canh_bao": canh_bao,
	}


def _dong_gia_cong(gia_cong, canh_bao):
	"""Dòng đơn mua dịch vụ gia công — mục 4.1, Thắng chốt 24/08 01:10.

	Mỗi mặt hàng Gia công sinh **một** dòng: mặt hàng = *dịch vụ gia công*, Finished Good = chính
	nó. Phần nguyên vật liệu đã nằm trong bảng chính (ERPNext bắt công ty cấp NVL cho nhà cung cấp
	gia công), nên ở đây chỉ trả phần dịch vụ — trả cả NVL lần nữa là đếm hai lần.
	"""
	if not gia_cong:
		return []
	if not frappe.db.exists("Item", MA_DICH_VU_GIA_CONG):
		canh_bao.append(
			_("Chưa có mặt hàng {0} nên không lập được dòng đơn mua gia công cho: {1}")
			.format(frappe.bold(MA_DICH_VU_GIA_CONG), ", ".join(sorted(gia_cong)))
		)
		return []
	ket = []
	for m, sl in sorted(gia_cong.items()):
		ket.append({
			"ma_dich_vu": MA_DICH_VU_GIA_CONG,
			"finished_good": m,
			"so_luong": round(flt(sl), 4),
		})
	return ket


@frappe.whitelist()
def gop_lap_ke_hoach(kieu=KIEU_THEO_DON, **tham_so):
	"""Gộp tổng các kỳ thành MỘT dòng mỗi vật tư — đầu vào của tab Lập kế hoạch (mục 7).

	⚠ Gộp tổng là đúng **với điều kiện từng kỳ đã tính bằng kéo tồn qua kỳ**. Nếu mỗi kỳ tính độc
	  lập thì con số từng kỳ đã sai, gộp lại càng sai — nên hàm này cố ý gọi lại `tinh_nhu_cau`
	  chứ không nhận bảng do client gửi lên.

	*Số lượng đặt* mặc định bằng phần còn phải mua; người dùng sửa được để mua theo lô tối thiểu,
	mua tròn thùng, hoặc cho về 0 để bỏ dòng. Lúc lập đơn phải dùng **số người dùng chốt**, không
	dùng số thiếu hụt gốc.
	"""
	kq = tinh_nhu_cau(kieu=kieu, **tham_so)
	gop = []
	for d in kq["dong"]:
		gop.append({
			"ma": d["ma"],
			"ten": d["ten"],
			"don_vi": d["don_vi"],
			"ton_kha_dung": d["ton_kha_dung"],
			"ton_toi_thieu": d["ton_toi_thieu"],
			"thieu_hut": d["con_phai_mua"],
			"so_luong_dat": d["con_phai_mua"],
			"da_khai_toi_thieu": d["da_khai_toi_thieu"],
		})
	kq["lap_ke_hoach"] = gop
	return kq
