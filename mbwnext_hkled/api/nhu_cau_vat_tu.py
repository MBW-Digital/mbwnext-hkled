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
from mbwnext_hkled.api.kiem_tra_ton_kho import (
	_kha_dung,
	_kho_hop_le,
	_ton_thuc_te,
	ghim_boi_don_khac,
)

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
				# Hai ca khác hẳn nhau, hiện cùng bị bỏ:
				#   • về SAU kỳ cuối -> bỏ là đúng, nó không giúp gì cho khoảng đang tính;
				#   • KHÔNG CÓ NGÀY  -> đó là lỗ hổng dữ liệu, đáng nói ra chứ không đáng bỏ lặng.
				# Ca thứ hai hiện KHÔNG tới được: `Purchase Order Item.schedule_date` là `reqd = 1`,
				# và đo 04/09 có 0 dòng thiếu cả hai ngày. Ngày nào ai bỏ `reqd` thì tách nhánh này
				# ra và cho vào khối cảnh báo — đừng để nó im lặng.
				continue
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

	⚠ Đệm này KHÔNG phải tối ưu cho vui. `safe_exec` của Frappe **biên dịch lại toàn bộ Server
	Script ở mỗi lần gọi**, mà script định mức của HKLED dài ~500 dòng. Đệm theo `(mã, template)`
	sống trong MỘT lần gọi `tinh_nhu_cau`: cùng một bán thành phẩm xuất hiện dưới nhiều thành phẩm,
	và cả cây được nổ lại ở từng kỳ.

	Trần hiệu năng còn lại đã được gỡ ở `api/bom.py::resolve_qty_batch` (03/09): hỏi Server Script
	MỘT lần cho cả lô thành phần của một biến thể, thay vì một lần mỗi thành phần. Đo trên 8012:
	300 biến thể từ **43,9 s xuống 12,8 s**, định mức ra y hệt (0/60 biến thể lệch).
	"""
	template = get_active_template(ma)
	if not template:
		return None
	khoa = (ma, template)
	if khoa not in bo_nho:
		bo_nho[khoa] = resolve_components(ma, template)
	return bo_nho[khoa]


def no_dinh_muc(nhu_cau, canh_bao=None, chua_no_duoc=None, gia_cong=None, da_tham=None, bo_nho=None,
				kho=None, ghim=None, be=None, da_dung=None):
	"""Nổ {mã: SL} xuống nguyên vật liệu lá. Trả về {mã NVL: tổng SL}.

	Thứ tự tra định mức đúng theo đầu bài mục 4.2 — anh Thắng chốt 02/09 11:14:

	    có BOM                            -> dùng BOM
	    chưa có BOM nhưng có BOM Template -> nổ theo BOM Template
	    không có cả hai                   -> liệt kê ra cho người dùng kiểm

	⚠ Nhánh giữa gọi `resolve_components` — hàm **chỉ đọc**, KHÔNG gọi `auto_create_bom`. Tạo BOM
	  thật submit chứng từ và gỡ cờ `is_default` của BOM cũ; việc đó phải qua một cú bấm rõ ràng,
	  không được xảy ra lúc người dùng chỉ bấm Tính toán.

	🔒 **ĐỔI 05/09/2026 — TRỪ BÁN THÀNH PHẨM ĐANG CÓ TRONG KHO.** Anh Thắng chốt 10:52:
	*"Phần V cũng tính như bảng 2 em nhé, mình cứ đưa cho họ con số chính xác, còn họ sẽ tự cân
	đối việc mua hàng số lượng như nào"* — tức bác luôn lý lẽ "tính dư cho an toàn".

	Trước đó hàm nổ **thẳng xuống lá**, tồn chỉ trừ một lần ở tầng lá, nên hệ thống bảo đi mua
	nguyên vật liệu để làm ra thứ đang nằm sẵn trong kho. Nay mỗi mã **Sản xuất/Gia công** được
	trừ phần tồn khả dụng của chính nó trước, chỉ phần **còn phải làm** mới bóc xuống.

	⚠ Vẫn giữ luật cũ ở dạng khác: **bể `be` dùng chung cho cả cây VÀ cả các kỳ**, trừ dần chứ
	  không trừ lại từ đầu ở mỗi nhánh — trừ riêng từng nhánh thì cùng một lượng tồn che được
	  nhiều nhánh. Ở Phần V còn thêm một chiều nữa: một cái bán thành phẩm trong kho chỉ che
	  được **một kỳ**, và phải là **kỳ sớm nhất**, nên `be` phải sống qua cả vòng lặp kỳ.

	⚠ `da_dung` ghi lại phần tồn đã tiêu để che bán thành phẩm. Chỗ gọi **phải trừ nó khỏi tồn
	  tầng lá**, nếu không một mã vừa là bán thành phẩm vừa là hàng mua sẽ được tính tồn hai lần.

	⚠ `kho = None` thì KHÔNG trừ gì — giữ nguyên hành vi cũ cho mọi chỗ gọi khác.

	⚠ `da_tham` chặn định mức lặp vòng. Khách khẳng định không có, nhưng đó là *tình trạng dữ liệu*
	  chứ không phải ràng buộc hệ thống — một vòng lặp làm treo tiến trình chứ không báo lỗi.
	"""
	canh_bao = canh_bao if canh_bao is not None else []
	chua_no_duoc = chua_no_duoc if chua_no_duoc is not None else []
	gia_cong = gia_cong if gia_cong is not None else {}
	da_tham = da_tham if da_tham is not None else set()
	bo_nho = bo_nho if bo_nho is not None else {}
	ghim = ghim or {}
	be = be if be is not None else {}
	da_dung = da_dung if da_dung is not None else {}
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
		# ── Trừ tồn khả dụng của CHÍNH mã này trước khi bóc xuống (chốt 05/09) ──
		if kho:
			if m not in be:
				ton_m = flt(_ton_thuc_te([m], kho).get(m, 0))
				be[m] = max(0.0, _kha_dung(ton_m, ghim.get(m, 0))[0])
			dung = min(sl, flt(be[m]))
			if dung > 0:
				be[m] = flt(be[m]) - dung
				da_dung[m] = flt(da_dung.get(m, 0)) + dung
				sl = sl - dung
			if sl <= 1e-9:
				# Kho đủ che phần này — không phải làm, nên cũng không phải mua vật tư cho nó.
				continue

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
		sau = no_dinh_muc(con, canh_bao, chua_no_duoc, gia_cong, da_tham | {m}, bo_nho,
						  kho=kho, ghim=ghim, be=be, da_dung=da_dung)
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
		# Tách riêng đơn ĐANG GHIM mà trống mốc thời gian. Đây là ca dễ bị đọc nhầm thành lỗi nhất:
		# đơn đó bị TRỪ ở vế Tồn (vì đang giữ chỗ) nhưng KHÔNG BAO GIỜ được cộng ở vế Nhu cầu (vì
		# không xếp được vào kỳ nào). Nhìn từ màn hình thì thành ra "tự nhiên thiếu hàng mà không
		# thấy đơn nào cần". Đúng luật — hàng đang bị giữ thật — nhưng phải nói ra, không thì người
		# đọc đi tìm một lỗi không tồn tại.
		dang_ghim = set(
			frappe.get_all(
				"Sales Order",
				filters={"name": ["in", thieu_moc], "custom_ghim_ton_kha_dung": 1},
				pluck="name",
			)
		)
		khong_ghim = sorted(set(thieu_moc) - dang_ghim)
		if khong_ghim:
			canh_bao.append(
				_("{0} đơn bán đã duyệt bị bỏ qua vì trống Thời Gian Bắt Đầu — không xếp được vào kỳ nào: {1}")
				.format(len(khong_ghim), ", ".join(khong_ghim))
			)
		if dang_ghim:
			canh_bao.append(
				_("{0} đơn ĐANG GHIM nhưng trống Thời Gian Bắt Đầu: {1}. Phần hàng các đơn này giữ"
				  " VẪN bị trừ khỏi tồn khả dụng ở mọi kỳ, nhưng nhu cầu của chúng KHÔNG được tính"
				  " vào kỳ nào — nên bảng có thể báo thiếu mà không thấy đơn tương ứng. Điền Thời"
				  " Gian Bắt Đầu cho các đơn này là hết.")
				.format(len(dang_ghim), ", ".join(sorted(dang_ghim)))
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
	bao_tien_do=None,
):
	"""Tính nhu cầu vật tư cần mua. **Chỉ đọc** — không tạo BOM, không tạo đơn mua.

	Kiểu 1 (theo đơn hàng): dùng `loai_ky` + `so_ky`, nhu cầu lấy từ đơn bán rơi vào từng kỳ.
	Kiểu 2 (theo kết quả bán trước đó): dùng `tu_ngay` + `den_ngay` + `lui_thang`, MỘT kỳ duy nhất.

	Kết quả **chỉ mang tính tham khảo tại thời điểm bấm Tính toán**, không chốt cứng (đầu bài mục 1).
	"""
	kieu = str(kieu)
	canh_bao, chua_no_duoc, gia_cong = [], [], {}
	bao = bao_tien_do or (lambda pt, mo_ta: None)
	bao(5, _("Đang dựng kỳ và gom nhu cầu"))
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

	# 🔒 Chốt 05/09: nổ định mức phải TRỪ bán thành phẩm đang có trong kho, nên tập kho và phần
	# giữ chỗ phải biết TRƯỚC vòng lặp kỳ — trước đây hai thứ này tính ở bước 3, sau khi nổ xong.
	#
	# ⚠ `be` và `da_dung` khai NGOÀI vòng lặp: một cái bán thành phẩm trong kho chỉ che được MỘT
	#   kỳ, và vòng lặp chạy từ kỳ sớm nhất nên kỳ sớm được che trước — đúng luật "kéo tồn qua kỳ"
	#   mà bước 3 đang áp cho tầng lá.
	kho = _kho_hop_le(company)
	if kieu == KIEU_THEO_DON:
		giu_cho, cb_ghim = _ghim_ngoai_ky(don_trong_ky)
	else:
		giu_cho, cb_ghim = ghim_boi_don_khac()
	canh_bao.extend(cb_ghim or [])
	be_ton, da_dung_ton = {}, {}

	for i in range(so_ky_that):
		mot_ky = {}
		for m, sl in nhu_cau_tp.items():
			if flt(sl[i]) > 0:
				mot_ky[m] = sl[i]
		if not mot_ky:
			continue
		# Nổ định mức chiếm gần hết thời gian chạy, nên thanh tiến độ phải nhích ở ĐÂY. Báo theo
		# số kỳ đã xong chứ không theo số mã: người dùng đọc được "kỳ 2/4", không đọc được "137 mã".
		bao(10 + int(75 * i / so_ky_that), _("Nổ định mức kỳ {0}/{1}").format(i + 1, so_ky_that))
		for nvl, sl in no_dinh_muc(
			mot_ky, canh_bao, chua_no_duoc, gia_cong, None, bo_nho,
			kho=kho, ghim=giu_cho, be=be_ton, da_dung=da_dung_ton,
		).items():
			nhu_cau_nvl.setdefault(nvl, [0.0] * so_ky_that)
			nhu_cau_nvl[nvl][i] += sl

	if not nhu_cau_nvl:
		# 🔴 `co_nhu_cau = False` để màn hình phân biệt HAI trạng thái rỗng khác hẳn nghĩa nhau:
		#   • KHÔNG CÓ NHU CẦU  — kỳ này chẳng ai đặt gì, hệ thống chưa tính gì cả;
		#   • ĐỦ HÀNG HẾT       — có nhu cầu, tính xong, không mã nào thiếu.
		# Trước 05/09 cả hai đều hiện *"Không có vật tư nào thiếu trong khoảng đã chọn"* — câu đó
		# ở trạng thái đầu là **nói sai**: người lập kế hoạch đọc thành "tồn đủ", trong khi thật ra
		# chưa có gì để tính. Cùng họ với lỗi `"chưa có đơn mua"` của Phần IV (vá 04/09): chỗ nguy
		# hiểm không phải phép tính mà là **câu khẳng định đè lên chỗ trống**.
		return {
			"kieu": kieu, "company": company, "cac_ky": cac_ky, "dong": [],
			"co_nhu_cau": False,
			"canh_bao": canh_bao + [_("Không có nhu cầu nào trong khoảng đã chọn")],
			"chua_no_duoc": chua_no_duoc, "gia_cong": [],
			"khoang_tham_chieu": khoang_tham_chieu,
		}

	ma_hang = list(nhu_cau_nvl)

	# ── 3. Tồn khả dụng — cùng một cơ sở với Phần IV (đầu bài mục 5) ─────────
	bao(88, _("Trừ tồn và kéo tồn qua kỳ"))
	# `kho` và `giu_cho` đã tính ở trên (phép nổ cần chúng). Kiểu 2 lấy TOÀN BỘ phần ghim vì nhu
	# cầu là lịch sử bán, không trùng đơn hiện tại; Kiểu 1 chỉ lấy phần của đơn ngoài kỳ.
	ton = _ton_thuc_te(ma_hang, kho)

	# 🔴 Phần tồn đã tiêu để che bán thành phẩm ở tầng giữa PHẢI trừ khỏi tồn tầng lá. Một mã vừa
	# là bán thành phẩm vừa là hàng mua ngoài (site có mã như vậy) sẽ được tính tồn HAI LẦN nếu
	# quên bước này — và tính hai lần thì ra số cần mua thấp hơn thực tế, tức thiếu hàng thật.
	if da_dung_ton:
		ton = {m: max(0.0, flt(sl) - flt(da_dung_ton.get(m, 0))) for m, sl in ton.items()}

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
	ghim_vuot_ton = {}
	for m in ma_hang:
		# ⚠ KHÔNG trừ thẳng `tồn − ghim`: phần giữ chỗ có thể LỚN HƠN số đang có trong kho, và số
		# âm đó đi vào `_tinh_mot_ma` làm lượng cần mua phồng lên — mua thừa đúng bằng phần thiếu
		# của đơn khác. Anh Thắng bắt lỗi này ở Phần IV ngày 03/09 16:34; Phần V là bản chép thứ
		# bảy của cùng phép trừ. Dùng chung `_kha_dung` để cả app chỉ còn MỘT định nghĩa.
		# Ca thật trên 8012: `NVL 3` tồn 7, `SO-26-00011` ghim 9 -> thô ra −2, kẹp về 0.
		ton_dau, _hieu_luc, ghim_vuot = _kha_dung(ton.get(m, 0.0), giu_cho.get(m, 0.0))
		if ghim_vuot > 0:
			ghim_vuot_ton[m] = ghim_vuot
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

	# Nói ra chỗ con số bị kẹp, thay vì lặng lẽ đổi kết quả. Ghim vượt tồn là dấu hiệu dữ liệu
	# đang lệch — người dùng cần biết để đi tìm nguyên nhân, không phải chỉ nhận một con số đẹp.
	if ghim_vuot_ton:
		chi_tiet = []
		for m in sorted(ghim_vuot_ton):
			chi_tiet.append("%s (%s)" % (m, round(ghim_vuot_ton[m], 4)))
		canh_bao.append(
			_("{0} mặt hàng đang bị ghim NHIỀU HƠN số có trong kho; phần vượt đã bỏ qua để không"
			  " sinh nhu cầu mua ảo: {1}").format(len(ghim_vuot_ton), ", ".join(chi_tiet))
		)

	return {
		"kieu": kieu,
		"company": company,
		"cac_ky": cac_ky,
		"khoang_tham_chieu": khoang_tham_chieu,
		"co_nhu_cau": True,      # có nhu cầu và đã tính xong — xem chú thích ở nhánh rỗng phía trên
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


# ── Chạy nền (đầu bài mục 6.2 — quy mô 250–350 dòng mỗi kỳ) ───────────────────
#
# Vì sao không gọi thẳng `tinh_nhu_cau` từ trình duyệt: chi phí tuyến tính theo số BIẾN THỂ khác
# nhau, đo 03/09 là ~0,15 s mỗi biến thể, tức 300 biến thể ≈ 44 giây. Quá ngưỡng timeout của
# gateway, và kể cả không quá thì để người dùng ngồi nhìn màn hình đứng im 44 giây là hỏng.
#
# ⚠ Kết quả đi qua `frappe.cache()` — nhưng đây KHÔNG phải cái đệm đã bị gỡ ở `_thanh_phan_theo_template`.
# Ở đó là đệm dữ liệu dẫn xuất, sống lâu, và rủi ro là trả SỐ CŨ. Ở đây là chỗ gửi kết quả của
# đúng một lần bấm sang cho đúng lần bấm đó lấy: khoá sinh mới mỗi lần, không ai đọc lại lần thứ hai.

TIEN_DO = "hkled_nhu_cau_tien_do"
XONG = "hkled_nhu_cau_xong"


def _khoa_ket_qua(ma_phien):
	return "hkled_nhu_cau_kq:%s" % ma_phien


def _khoa_tien_do(ma_phien):
	return "hkled_nhu_cau_td:%s" % ma_phien


@frappe.whitelist()
def tinh_nen(**tham_so):
	"""Đẩy phép tính sang hàng đợi, trả về mã phiên để trình duyệt lắng nghe.

	Trình duyệt nghe hai sự kiện realtime rồi gọi `lay_ket_qua(ma_phien)`.
	"""
	tham_so.pop("cmd", None)
	ma_phien = frappe.generate_hash(length=12)
	frappe.enqueue(
		"mbwnext_hkled.api.nhu_cau_vat_tu._chay_nen",
		queue="short",
		# 44 giây là ca xấu nhất đo được; để 600 s cho dữ liệu thật lớn hơn mà vẫn có trần rõ ràng,
		# thay vì chạy vô hạn khi cây định mức có gì đó bất thường.
		timeout=600,
		ma_phien=ma_phien,
		tham_so=tham_so,
		nguoi_dung=frappe.session.user,
	)
	return {"ma_phien": ma_phien}


def _chay_nen(ma_phien, tham_so, nguoi_dung):
	"""Chạy trong worker. Mọi lỗi phải ĐI TỚI trình duyệt, không được chết lặng trong log.

	Job chết mà không báo gì thì màn hình quay mãi ở 5% — người dùng không biết nên chờ hay bấm lại.
	"""
	def bao(phan_tram, mo_ta):
		# GHI VÀO CACHE TRƯỚC, phát realtime sau. Realtime là đường nhanh; cache là đường chắc.
		#
		# ⚠ Không được chỉ dựa vào realtime: đo 03/09 trên chính bench này, socketio chạy ở cổng
		# 9006 còn site vào qua 8012, nên trình duyệt báo "Error connecting to socket.io: timeout"
		# và trang treo vĩnh viễn ở 3% — job đã chạy xong, chỉ là không ai báo cho màn hình biết.
		# Bản đầu của hàm này chỉ có realtime, và đó là lỗi thiết kế: một tính năng không được hỏng
		# hoàn toàn chỉ vì một kênh phụ không nối được.
		frappe.cache().set_value(
			_khoa_tien_do(ma_phien), {"phan_tram": phan_tram, "mo_ta": mo_ta}, expires_in_sec=1800
		)
		frappe.publish_realtime(
			TIEN_DO, {"ma_phien": ma_phien, "phan_tram": phan_tram, "mo_ta": mo_ta},
			user=nguoi_dung,
		)

	try:
		kq = tinh_nhu_cau(bao_tien_do=bao, **tham_so)
		kq["ma_phien"] = ma_phien
	except Exception:
		frappe.log_error(title="Tính nhu cầu vật tư thất bại", message=frappe.get_traceback())
		kq = {"loi": frappe.get_traceback(with_context=False).strip().splitlines()[-1]}

	frappe.cache().set_value(_khoa_ket_qua(ma_phien), kq, expires_in_sec=1800)
	frappe.publish_realtime(XONG, {"ma_phien": ma_phien}, user=nguoi_dung)


@frappe.whitelist()
def lay_ket_qua(ma_phien):
	"""Lấy kết quả của một lần bấm. Hết hạn (30 phút) thì báo rõ để người dùng bấm lại."""
	kq = frappe.cache().get_value(_khoa_ket_qua(ma_phien))
	if kq is None:
		frappe.throw(_("Kết quả đã hết hạn hoặc chưa tính xong — bấm Tính toán lại"))
	return kq


@frappe.whitelist()
def trang_thai(ma_phien):
	"""Tiến độ + đã xong chưa — đường hỏi vòng, dùng khi realtime không tới được.

	Trả `xong=True` ngay khi kết quả đã nằm trong cache, kể cả khi trình duyệt bỏ lỡ mọi sự kiện
	realtime. Rẻ: hai lần đọc Redis, không đụng database.
	"""
	if frappe.cache().get_value(_khoa_ket_qua(ma_phien)) is not None:
		return {"xong": True}
	td = frappe.cache().get_value(_khoa_tien_do(ma_phien)) or {}
	return {"xong": False, "phan_tram": td.get("phan_tram"), "mo_ta": td.get("mo_ta")}
