# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Kiểm tra tồn kho và nguồn lực trên Đơn Bán — Phần IV (PM-FEAT-00023).

Đầu bài: `docs/features/kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md`.
Mockup khách đã duyệt 03/09: mục B của file `docs/mockups/` cùng tên.

## Bốn bước, ĐÚNG THỨ TỰ — đây là quy tắc nghiệp vụ, không phải chuyện tối ưu

1. Gom nhu cầu mặt hàng trên đơn (cộng dồn theo `item_code`, một đơn có thể lặp mặt hàng).
2. Trừ tồn cho mặt hàng trên đơn  →  **Bảng 1**.
3. Bóc định mức cho phần **CÒN THIẾU**, không bóc cả phần cần.
4. Gom toàn bộ nhu cầu NVL rồi mới trừ tồn **MỘT LẦN**  →  **Bảng 2**.

⚠ Bước 3 chỉ bóc phần thiếu: bóc cả `cần` là mua thừa đúng bằng phần đang có trong kho.
⚠ Bước 4 không trừ tồn ngay tại từng nhánh: trừ sớm thì cùng một lượng tồn bị đếm nhiều lần
  cho nhiều nhánh của cây định mức.

## Hai chỗ đọc dữ liệu dễ sai, đã ghi vào đầu bài

- **Phần tồn bị giữ chỗ đọc từ `Bin.reserved_stock`, KHÔNG cộng `Stock Reservation Entry`.**
  SRE đã huỷ vẫn giữ nguyên `reserved_qty` lịch sử — đo 26/08: SRE cộng ra 26 trong khi Bin
  ra 0. Ở đây ta không dùng cơ chế lõi, nhưng nguyên tắc giữ nguyên: đọc nơi ghi thật.
- **`frappe.get_all` chứ không `frappe.get_list`.** `get_list` áp User Permission; sale cần
  thấy tồn kho tổng chứ không phải phần mình được phép xem. Riêng danh sách đơn đang ghim
  (mục 7) thì cố ý **không** hiện tên khách hàng — che ở tầng dữ liệu, không dựa vào quyền.

## Hiệu năng

Quy mô đã chốt: 1–2 mặt hàng/đơn, định mức dưới 10 NVL, mục tiêu dưới 1 giây. Chỗ tốn không
nằm ở đơn hiện tại mà ở chỗ phải bóc định mức cho **mọi đơn đang ghim**. Nên mọi truy vấn tồn
đều gom `item_code IN (...)` một lần — bẫy N+1 của Frappe nằm đúng ở đây.
"""

import frappe
from frappe import _
from frappe.utils import flt, get_datetime, getdate, nowdate


# Hai nhóm kho bị loại khỏi mọi phép tính tồn (mục 3 của đầu bài).
#
# ⚠ Lấy kho con bằng `lft/rgt` của cây Warehouse, KHÔNG so tên: tên có hậu tố công ty
# ("- HKL") và sẽ khác khi lên site khác. Tên ở đây chỉ để TÌM nút gốc; tìm không thấy thì
# bỏ qua nhóm đó chứ không throw — site mới chưa dựng cây kho vẫn phải chạy được.
NHOM_KHO_LOAI = ("Nhóm kho lỗi", "Nhóm kho trung chuyển")


TRANG_THAI_DON_CHET = ("Closed", "Completed", "Cancelled")


def loc_don_song(tru_don=None):
	"""Bộ lọc *"Đơn Bán còn sống và đang bật ghim"* — **một định nghĩa cho cả tính năng**.

	Ba nơi phải hiểu giống hệt nhau, nếu không thì lệch âm thầm chứ không nổ lỗi:

	- `ghim_boi_don_khac` — số bị trừ khỏi tồn khả dụng của đơn đang xem
	- `api.ghim_vat_tu` — sổ cam kết vật tư (PM-FEAT-00036)
	- lớp chặn xuất kho PM-FEAT-00034, qua hai hàm trên

	Đây chính là chỗ giữ **bất biến #3** của mục 12e: đơn Huỷ / Đóng / Hoàn thành rơi khỏi bộ
	lọc này thì phần nó đang ghim biến mất khỏi mọi phép tính — không cần ai đi dọn bảng.
	Tách riêng ra hàm để không ai sửa một chỗ mà quên hai chỗ kia.

	`tru_don` nhận cả MỘT tên lẫn DANH SÁCH tên: PM-FEAT-00034 phải miễn trừ mọi Đơn Bán mà
	chứng từ xuất kho đang thực hiện, không chỉ một.
	"""
	loc = {
		"docstatus": 1,
		"custom_ghim_ton_kha_dung": 1,
		"status": ["not in", list(TRANG_THAI_DON_CHET)],
	}
	if isinstance(tru_don, (list, tuple, set)):
		if tru_don:
			loc["name"] = ["not in", list(tru_don)]
	elif tru_don:
		loc["name"] = ["!=", tru_don]
	return loc


def _kho_hop_le(company=None):
	"""Trả về danh sách kho được tính tồn. None = không loại kho nào (site chưa dựng cây)."""
	loc = {"is_group": 0}
	if company:
		loc["company"] = company
	tat_ca = frappe.get_all("Warehouse", filters=loc, pluck="name")
	if not tat_ca:
		return []

	bi_loai = set()
	for ten_goc in NHOM_KHO_LOAI:
		loc_goc = {"is_group": 1, "warehouse_name": ten_goc}
		if company:
			loc_goc["company"] = company
		for goc in frappe.get_all("Warehouse", filters=loc_goc, fields=["lft", "rgt"]):
			loc_con = {"lft": [">", goc.lft], "rgt": ["<", goc.rgt], "is_group": 0}
			if company:
				loc_con["company"] = company
			bi_loai.update(frappe.get_all("Warehouse", filters=loc_con, pluck="name"))

	return [w for w in tat_ca if w not in bi_loai]


def _ton_thuc_te(ma_hang, kho):
	"""{item_code: tồn thực tế} — MỘT query cho toàn bộ mặt hàng, không gọi trong vòng lặp."""
	if not ma_hang or not kho:
		return {}
	rows = frappe.get_all(
		"Bin",
		filters={"item_code": ["in", list(ma_hang)], "warehouse": ["in", kho]},
		fields=["item_code", "sum(actual_qty) as ton"],
		group_by="item_code",
	)
	return {r["item_code"]: flt(r["ton"]) for r in rows}


def _so(x):
	"""Số lượng cho người đọc, dùng chung cho mọi câu thông báo của Phần IV và IV.1.

	`frappe.format_value(x, {"fieldtype": "Float"})` cho ra **3 chữ số thập phân** — câu chặn
	hiện *"chỉ giữ chỗ được 0,000"*, đọc như số tiền chứ không như số cái đèn.

	⚠ Nhưng ép cứng 0 chữ số cũng sai. UOM `Kg` · `m` · `Lít` trên site đều để
	  `must_be_whole_number = 0`, tức số lẻ hợp lệ; ép 0 thì **2,5 hiện thành 3** — thay một câu
	  khó đọc bằng một câu **sai**, mà lại sai trong đúng câu đang báo cho người dùng biết họ
	  được giữ bao nhiêu. Hiện chưa mã nào lẻ (đã quét Bin/SO/BOM/PO ngày 04/09: 0 dòng), nên
	  đây là phòng trước chứ không phải sửa lỗi đang có.

	Nên: nguyên thì bỏ hẳn phần thập phân, lẻ thì giữ, chỉ cắt số 0 thừa ở đuôi.
	Bản JS tương ứng là `so()` trong `controllers/js/sales_order.js` — sửa một bên thì sửa cả hai.
	"""
	x = flt(x)
	if x == int(x):
		return frappe.format_value(x, {"fieldtype": "Float", "precision": 0})
	ra = frappe.format_value(x, {"fieldtype": "Float"})
	return ra.rstrip("0").rstrip(".,") if ("." in ra or "," in ra) else ra


def _kha_dung(ton, ghim_ma):
	"""Tồn khả dụng của một mã. Trả về `(kha_dung, ghim_hieu_luc, ghim_vuot)`.

	⚠ **Không ai giữ chỗ được nhiều hơn số đang có trong kho.** Ghim là đặt riêng ra một phần
	  hàng CÓ THẬT; ghim 3 khi kho có 1 thì phần trừ được chỉ là 1.

	  Trước 03/09 hàm gọi tính thẳng `kha_dung = ton - ghim`, cho ra số âm, rồi
	  `thieu = can - kha_dung` cộng luôn phần âm đó vào đơn đang xem. Anh Thắng bắt được
	  03/09 16:34 trên `Bán thành phẩm 2` (tồn 1, đơn khác ghim 3 → khả dụng −2): mọi đơn mở lên
	  sau đều bị cộng thêm 2 vào số cần mua, và số sai đó đi thẳng vào phiếu Yêu Cầu Mặt Hàng.
	  Đo trên `SO-26-00010`: `Bán thành phẩm 2` thiếu 173 thay vì 171.

	⚠ **Kẹp ở đây KHÔNG phải là sửa gốc rễ.** Gốc rễ là vì sao ghim lại vượt tồn:
	  `ghim_boi_don_khac` giữ chỗ cả thành phẩm LẪN nguyên vật liệu trong định mức của nó, kể cả
	  khi thành phẩm đã có sẵn trong kho và không phải sản xuất thêm cái nào. Ca thật:
	  `SO-26-00011` ghim 3 `Thành phẩm 1` trong khi kho đang có 31 — không cần sản xuất, nhưng
	  hệ thống vẫn giữ 3 `Bán thành phẩm 2` cho nó, mà kho chỉ có 1.
	  ➜ Sửa phần đó là **đổi cách hiểu nghiệp vụ**, phải hỏi anh Thắng. Hàm này chỉ đảm bảo phép
	  trừ không sinh ra nhu cầu mua ảo trong lúc chờ.

	⚠ Tồn ÂM thì giữ nguyên số âm, không kẹp về 0: đó là tồn kho thật sự lệch (hiện `hkled.com`
	  không có bản ghi nào), phải mua bù thật chứ không phải hiệu ứng của ghim.
	"""
	ton = flt(ton)
	ghim_ma = flt(ghim_ma)
	hieu_luc = min(ghim_ma, max(0.0, ton))
	return ton - hieu_luc, hieu_luc, ghim_ma - hieu_luc


def _bom_mac_dinh(ma_hang):
	"""{item_code: tên BOM mặc định} — một query cho cả tập, không hỏi từng mã."""
	if not ma_hang:
		return {}
	rows = frappe.get_all(
		"BOM",
		filters={"item": ["in", list(ma_hang)], "is_active": 1, "is_default": 1, "docstatus": 1},
		fields=["name", "item"],
	)
	return {r["item"]: r["name"] for r in rows}


def _dong_bom(ten_bom):
	"""[(mã NVL, số lượng cho 1 đơn vị thành phẩm)] của một BOM."""
	bom = frappe.get_cached_doc("BOM", ten_bom)
	sl_thanh_pham = flt(bom.quantity) or 1.0
	return [(d.item_code, flt(d.stock_qty or d.qty) / sl_thanh_pham) for d in bom.items]


CAP_BOC_TOI_DA = 8


def boc_dinh_muc_tru_ton(nhu_cau, kho, ghim=None, canh_bao=None):
	"""Bóc định mức xuống NVL lá, **TRỪ TỒN KHẢ DỤNG Ở TỪNG CẤP**.

	Trả về `(can_mua, nhu_cau_la)`: `can_mua` = {mã lá: số thật sự phải mua sau khi đã trừ hàng
	có sẵn ở mọi cấp}; `nhu_cau_la` = {mã lá: nhu cầu gộp} — kể cả mã đã đủ hàng, để Bảng 2 vẫn
	hiện đủ dòng chứ không âm thầm giấu những mã không phải mua.

	🔒 **Anh Thắng chốt 05/09/2026 09:20:**

	> *"Bảng 2 em cũng phải trừ bán thành phẩm đang có trong kho nhé… Ví dụ thiếu 2 bán thành
	> phẩm, 1 bán thành phẩm đã có sẵn tồn khả dụng rồi thì chỉ cần bóc nguyên vật liệu của 1
	> bán thành phẩm thôi."*

	Khác `boc_dinh_muc` ở đúng một điểm, và điểm đó đổi con số đi mua hàng: hàm kia bóc **thẳng
	xuống lá**, coi như trong kho không có bán thành phẩm nào. Đo trên `SO-26-00026` ngày 04/09:
	đơn phải làm 9 `Thành phẩm 1`, kho có sẵn 1 `Bán thành phẩm 2` nên chỉ phải làm 8 — hàm kia
	vẫn ra `NVL 3` cần **27**, đúng phải là **24**.

	## ⚠ Trừ theo BỂ CHUNG, không trừ riêng từng nhánh

	Cảnh báo trong `boc_dinh_muc` vẫn nguyên giá trị: *"trừ sớm thì cùng một lượng tồn bị đếm cho
	nhiều nhánh"*. Một mã có thể là con của nhiều thành phẩm; mỗi nhánh tự trừ tồn của nó thì 1
	cái hàng trong kho che được 3 nhánh.

	Nên `be` là **một bể dùng chung cho cả phép bóc**: mã nào lấy trước thì trừ đi, nhánh sau chỉ
	còn phần dư. Đi theo **từng cấp** thay vì đệ quy theo nhánh chính là để bể được chia đúng thứ
	tự.

	⚠ Trừ **tồn khả dụng** (đã trừ phần đơn khác ghim), không phải tồn thực tế — hàng người khác
	  đang giữ thì không dùng được, y như Bảng 1.
	"""
	ghim = ghim or {}
	canh_bao = canh_bao if canh_bao is not None else []
	can_mua = {}
	nhu_cau_la = {}
	be = {}
	da_tham = set()
	tang = {m: flt(sl) for m, sl in (nhu_cau or {}).items() if flt(sl) > 0}

	for _cap in range(CAP_BOC_TOI_DA):
		if not tang:
			break

		# Nạp bể cho mã lần đầu gặp — MỘT query cho cả cấp, không hỏi trong vòng lặp.
		chua_co = [m for m in tang if m not in be]
		if chua_co:
			ton = _ton_thuc_te(chua_co, kho)
			for m in chua_co:
				be[m] = max(0.0, _kha_dung(flt(ton.get(m, 0)), ghim.get(m, 0))[0])

		pp = {
			r["name"]: (r.get("custom_replenishment_method") or "").strip()
			for r in frappe.get_all(
				"Item", filters={"name": ["in", list(tang)]},
				fields=["name", "custom_replenishment_method"],
			)
		}
		che_bien = [m for m in tang if pp.get(m) in ("Sản xuất", "Gia công") and m not in da_tham]
		bom_cua = _bom_mac_dinh(che_bien)
		bom_cua_la = _bom_mac_dinh([m for m in tang if m not in che_bien])

		con = {}
		for m, sl in tang.items():
			dung = min(sl, flt(be.get(m, 0)))
			be[m] = flt(be.get(m, 0)) - dung
			thieu = sl - dung

			ten_bom = bom_cua.get(m)
			la = m not in che_bien or not ten_bom
			if la:
				# Là LÁ: chính nó là thứ phải mua. Ghi cả nhu cầu gộp lẫn phần còn thiếu.
				if m in che_bien and not ten_bom:
					canh_bao.append(f"{m}: chưa có định mức, tạm coi như phải mua")
				elif m not in che_bien and m in bom_cua_la:
					# Dấu hiệu khách quên khai Phương pháp bổ sung — hệ thống sẽ đi MUA CHÍNH NÓ
					# thay vì mua nguyên vật liệu, sai hoàn toàn mà không báo gì.
					canh_bao.append(
						f"{m}: Phương pháp bổ sung đang là {pp.get(m) or 'trống'} nên coi như phải mua, "
						f"nhưng mặt hàng này CÓ định mức ({bom_cua_la[m]}) — kiểm lại xem có phải hàng sản xuất"
					)
				if m in da_tham:
					canh_bao.append(f"{m}: định mức lặp vòng, dừng bóc tại đây")
				nhu_cau_la[m] = flt(nhu_cau_la.get(m, 0)) + sl
				if thieu > 1e-9:
					can_mua[m] = flt(can_mua.get(m, 0)) + thieu
				continue

			# Hàng sản xuất: chỉ bóc phần CÒN PHẢI LÀM xuống cấp dưới.
			if thieu <= 1e-9:
				continue
			for nvl, dinh_muc in _dong_bom(ten_bom):
				con[nvl] = con.get(nvl, 0) + dinh_muc * thieu

		da_tham.update(che_bien)
		tang = con
	else:
		if tang:
			canh_bao.append(
				f"định mức lồng quá {CAP_BOC_TOI_DA} cấp, dừng bóc — kiểm lại dữ liệu định mức: "
				+ ", ".join(sorted(tang))
			)

	return can_mua, nhu_cau_la


def ghim_boi_don_khac(tru_don=None):
	"""{mã: số lượng đang bị các đơn KHÁC giữ chỗ}, đã tính cả NVL bóc từ định mức của họ.

	⚠ Đọc thẳng `custom_so_luong_giu_cho`, KHÔNG suy từ `qty − delivered_qty`. Từ 03/09 ghim là
	  một con số người dùng nhập: đơn giữ 1 trên dòng 5 cái thì chỉ chiếm 1.
	⚠ Cũng KHÔNG trừ `delivered_qty` ở đây. Giao hàng đã làm `Bin.actual_qty` giảm thật rồi; trừ
	  thêm lần nữa là trừ hai lần.
	"""
	don = frappe.get_all("Sales Order", filters=loc_don_song(tru_don), pluck="name")
	if not don:
		return {}, []

	dong = frappe.get_all(
		"Sales Order Item",
		filters={"parent": ["in", don], "custom_so_luong_giu_cho": [">", 0]},
		fields=["item_code", "custom_so_luong_giu_cho as giu"],
	)
	truc_tiep = {}
	for d in dong:
		truc_tiep[d["item_code"]] = truc_tiep.get(d["item_code"], 0) + flt(d["giu"])

	# Ghim lan xuống NVL: mặt hàng Sản xuất/Gia công thì NVL trong định mức cũng bị giữ theo.
	#
	# ⚠ Phải bóc MỘT CẤP TRƯỚC rồi mới đệ quy, KHÔNG gọi thẳng `boc_dinh_muc(truc_tiep)`.
	#   `boc_dinh_muc` trả mặt hàng *Mua hàng* về nguyên dạng vì chúng là lá — cộng kết quả đó
	#   với `truc_tiep` là **đếm hai lần** đúng những mã mua ngoài. Bản đầu của hàm này mắc lỗi
	#   đó: đơn giữ 20 cái nguồn NHKP-250E thì hệ thống hiểu là 40, các đơn khác thấy thiếu ảo.
	#   Cùng họ với lỗi trừ hai lần mà câu hỏi của khách chỉ ra hôm 27/08.
	canh_bao = []
	# 🔒 **ĐỔI 04/09 tối — phần vật tư nay ĐỌC TỪ SỔ, không suy ra nữa** (PM-FEAT-00036, mục 8).
	#
	# Trước: `boc_dinh_muc(_con_mot_cap(_con_phai_lam(truc_tiep)))` — suy tại chỗ từ định mức.
	# Cách đó **không thể** giữ được điều anh Thắng chốt 04/09: chia hàng theo thứ tự ưu tiên là
	# việc phụ thuộc *ai tới trước*, và phần đã chia cho một đơn không được tụt vì thao tác của
	# đơn khác. Con số suy ra luôn là hàm của hiện tại nên không giữ nổi cam kết.
	#
	# ⚠ Và cách cũ gần như luôn ra **rỗng**: `_con_phai_lam` tính `ghim − tồn`, trong khi
	#   `chan_giu_cho_vuot_ton` không cho ghim vượt tồn — hai luật triệt tiêu nhau. Đo trên 8012
	#   ngày 04/09: 0 mã bị ghim gián tiếp. Công thức đúng là `cần − đã giao − đã ghim`, nằm ở
	#   `api.ghim_vat_tu._phai_san_xuat`.
	#
	# Nhập lại trong hàm chứ không ở đầu file: `ghim_vat_tu` import ngược lại module này.
	from mbwnext_hkled.api.ghim_vat_tu import ghim_vat_tu

	gian_tiep = ghim_vat_tu(tru_don)

	# Thành phẩm bị giữ trực tiếp VÀ nguyên vật liệu của nó đều bị giữ — hai thứ nằm ở hai kho
	# khác nhau nên cộng cả hai là đúng. Chỉ có mã mua ngoài mới không được cộng lặp, và
	# `_con_mot_cap` đã loại chúng khỏi nhánh gián tiếp.
	tong = dict(gian_tiep)
	for m, sl in truc_tiep.items():
		tong[m] = tong.get(m, 0) + sl
	return tong, canh_bao


def _con_phai_lam(truc_tiep):
	"""{mã: số lượng còn PHẢI SẢN XUẤT} = phần ghim trừ đi thành phẩm đã có sẵn trong kho.

	🔒 **Anh Thắng chốt 03/09 16:51: "Chọn cách B em nhé."**

	Trước đó, đơn ghim thành phẩm thì hệ thống giữ luôn bộ vật tư để làm ra nó — **kể cả khi
	thành phẩm đã nằm sẵn trong kho và không phải sản xuất thêm cái nào**. Ca thật đo được:
	`SO-26-00011` ghim 3 `Thành phẩm 1` trong khi kho có 31; đơn đó lấy hàng từ kho là xong,
	nhưng hệ thống vẫn giữ 3 bộ vật tư cho nó, trong khi `Bán thành phẩm 2` chỉ có 1 cái. Đó
	chính là **gốc rễ của chuyện ghim vượt tồn** mà anh Thắng bắt được lúc 16:34.

	Cách B: chỉ lan xuống vật tư cho phần **thật sự phải làm ra**.

	⚠ Trừ tồn ở mức TỔNG, không trừ theo từng đơn: nhiều đơn cùng ghim một mã thì chúng chia
	  nhau đúng một lượng tồn. Trừ từng đơn là mỗi đơn được "che" bởi cùng số hàng đó — cùng họ
	  với lỗi trừ hai lần ở bước 4 của đầu bài.

	🔴 **Cách B làm `tru_don` thành BẮT BUỘC, không còn là chuyện gọn gàng.**
	  `max(0, tổng_ghim − tồn)` là phép **không tuyến tính**, nên KHÔNG được suy "phần đơn X giữ"
	  bằng cách gọi hai lần rồi trừ ra. Ví dụ: tồn 10, đơn A ghim 8, đơn B ghim 8.
	  Tổng giữ = `max(0, 16−10)` = **6**. Hỏi "B giữ bao nhiêu": đúng là `max(0, 8−10)` = **0**,
	  còn trừ ra cho `6 − 0` = **6**. Lệch hẳn, và lệch âm thầm.
	  ➜ Luôn truyền `tru_don` **ngay từ đầu** cho `ghim_boi_don_khac` / `ghim_chi_tiet`.
	  (Phiên làm Phần V bản đầu đúng là cách trừ ra; đổi kịp trước khi cách B vào.)

	⚠ `_kho_hop_le()` gọi **không kèm công ty** — cố ý, vì hàm này gom mọi đơn đang ghim chứ
	  không riêng công ty nào, giống `ghim_boi_don_khac`. `hkled.com` hiện chỉ có **1 công ty**
	  (`HKLED`, 5 kho hợp lệ, lọc hay không ra cùng kết quả). Ngày nào site có công ty thứ hai
	  thì chỗ này cộng tồn của cả hai — phải xem lại cùng lúc với `ghim_boi_don_khac`, đừng sửa
	  lẻ một chỗ.
	"""
	ma = [m for m, sl in truc_tiep.items() if flt(sl) > 0]
	if not ma:
		return {}
	ton = _ton_thuc_te(ma, _kho_hop_le())
	con = {}
	for m in ma:
		phai_lam = flt(truc_tiep[m]) - flt(ton.get(m, 0))
		if phai_lam > 0:
			con[m] = phai_lam
	return con


def ghim_chi_tiet(tru_don=None):
	"""Ai đang giữ chỗ mã nào — dữ liệu cho Bảng 1b và Bảng 2b.

	Trả về `({mã: [dòng, ...]}, canh_bao)`. Mỗi dòng:
	`{don, nguoi, ngay, giu, tu_ma, tu_sl, dinh_muc}`. Dòng **không** có `tu_ma` là ghim
	**trực tiếp** (đơn kia bán đúng mã đó — Bảng 1b); dòng **có** `tu_ma` là ghim **gián tiếp**
	(mã này là vật tư trong định mức của thứ đơn kia bán — Bảng 2b).

	⚠ Tổng của các dòng ở đây **phải khớp** `ghim_boi_don_khac`. Từ 04/09 tối, cả hai đọc chung
	  một nguồn — số trực tiếp từ `custom_so_luong_giu_cho`, số gián tiếp từ bảng
	  `custom_ghim_vat_tu` — nên khớp theo **cấu trúc**, không còn phải trông vào việc hai công
	  thức được viết giống nhau. Phép kiểm ở chỗ gọi vẫn giữ: nó nay bắt lỗi *bộ lọc* lệch chứ
	  không còn bắt lỗi *công thức* lệch.
	"""
	don = frappe.get_all(
		"Sales Order",
		filters=loc_don_song(tru_don),
		fields=["name", "custom_sales_person", "owner", "delivery_date"],
	)
	if not don:
		return {}, []

	# Anh Thắng chốt trong mockup bản 6: cột là *Người phụ trách*, KHÔNG hiện tên khách hàng.
	# Người phụ trách lấy Nhân viên kinh doanh, chưa khai thì lấy người tạo đơn — để ô không bao
	# giờ trống, người đọc còn biết hỏi ai.
	ho_so = {
		d["name"]: {
			"nguoi": d.get("custom_sales_person") or d.get("owner") or "",
			"ngay": d.get("delivery_date"),
		}
		for d in don
	}

	dong = frappe.get_all(
		"Sales Order Item",
		filters={"parent": ["in", list(ho_so)], "custom_so_luong_giu_cho": [">", 0]},
		fields=["parent", "item_code", "custom_so_luong_giu_cho as giu"],
	)

	canh_bao = []
	chi_tiet = {}

	def them(ma, **kw):
		chi_tiet.setdefault(ma, []).append(dict(kw))

	dong = [d for d in dong if flt(d["giu"]) > 0]

	# ── Phần ghim TRỰC TIẾP: toàn bộ số người dùng nhập trên dòng đơn ──
	for d in sorted(dong, key=lambda r: (ho_so[r["parent"]]["ngay"] is None, ho_so[r["parent"]]["ngay"])):
		goc = ho_so[d["parent"]]
		them(d["item_code"], don=d["parent"], nguoi=goc["nguoi"], ngay=goc["ngay"],
			giu=flt(d["giu"]), tu_ma=None, tu_sl=None, dinh_muc=None)

	# ── Phần ghim GIÁN TIẾP: ĐỌC SỔ CAM KẾT, không bóc lại định mức ──
	#
	# 🔒 **ĐỔI 04/09 tối cùng lúc với `ghim_boi_don_khac`** (PM-FEAT-00036). Trước đây hàm này
	# tự chia tồn cho từng đơn rồi bóc định mức lại — một phép tính thứ hai, song song với phép
	# của `ghim_boi_don_khac`, và chỉ khớp được nhờ hai bên viết cùng một luật. Đó đúng là kiểu
	# **lệch âm thầm** mà bất biến #2 sinh ra để chặn.
	#
	# Nay cả hai đọc chung một chỗ: bảng `custom_ghim_vat_tu`. Khớp theo cấu trúc, không phải
	# nhờ hai công thức trùng nhau.
	giu_vt = frappe.get_all(
		"HKLed Pinned Material",
		filters={"parent": ["in", list(ho_so)], "parenttype": "Sales Order", "so_luong_ghim": [">", 0]},
		fields=["parent", "item_code", "source_item", "source_qty", "so_luong_ghim", "required_qty"],
	)
	for d in giu_vt:
		goc = ho_so[d["parent"]]
		them(
			d["item_code"], don=d["parent"], nguoi=goc["nguoi"], ngay=goc["ngay"],
			giu=flt(d["so_luong_ghim"]), tu_ma=d["source_item"], tu_sl=flt(d["source_qty"]),
			# ⚠ `dinh_muc` chia theo **nhu cầu**, không phải theo phần đã ghim được. Chia theo
			#   phần đã ghim thì cột này thành "trung bình mỗi cái được cấp bao nhiêu" — một con
			#   số vô nghĩa, và nó tụt xuống mỗi khi kho hết hàng. Đo thật 04/09: `Bán thành
			#   phẩm 1` cần 9, ghim được 1 ➜ chia theo ghim ra **0,111** thay vì định mức **1**.
			dinh_muc=(flt(d["required_qty"]) / flt(d["source_qty"])) if flt(d["source_qty"]) else None,
		)

	# Đơn có ngày lấy hàng xa nhất lên trước: đó là đơn dễ thương lượng nhả hàng nhất, nên là
	# thứ người bán cần nhìn đầu tiên (mockup bản 6).
	for ma in chi_tiet:
		chi_tiet[ma].sort(key=lambda r: (r["ngay"] is None, r["ngay"]), reverse=True)
	return chi_tiet, canh_bao


def _con_mot_cap(nhu_cau, canh_bao):
	"""Chỉ trả về CON TRỰC TIẾP trong định mức của mặt hàng Sản xuất/Gia công.

	Mặt hàng mua ngoài trả về rỗng — chúng đã được tính ở nhánh trực tiếp rồi.
	"""
	ma = [m for m, sl in nhu_cau.items() if flt(sl) > 0]
	if not ma:
		return {}
	pp = {
		r["name"]: (r.get("custom_replenishment_method") or "").strip()
		for r in frappe.get_all(
			"Item", filters={"name": ["in", ma]},
			fields=["name", "custom_replenishment_method"],
		)
	}
	che_bien = [m for m in ma if pp.get(m) in ("Sản xuất", "Gia công")]
	bom_cua = _bom_mac_dinh(che_bien)

	con = {}
	for m in che_bien:
		ten_bom = bom_cua.get(m)
		if not ten_bom:
			canh_bao.append(f"{m}: đơn khác đang ghim nhưng chưa có định mức, không lan xuống NVL")
			continue
		for nvl, dinh_muc in _dong_bom(ten_bom):
			con[nvl] = con.get(nvl, 0) + dinh_muc * flt(nhu_cau[m])
	return con


def _kho_mac_dinh(ma_hang, company):
	"""{mã: kho mặc định của mặt hàng đó ở công ty này} — bảng con `Item Default` của lõi.

	Lõi ERPNext **đã có sẵn** bảng này (`Item.item_defaults`, mỗi dòng một công ty), nên không
	dựng bảng mới: trên site đã có đủ 62.055 dòng, chỉ là cột kho đang trống. Việc khai kho là
	**PM-FEAT-00037**.

	Một query cho toàn bộ mã, không hỏi trong vòng lặp.
	"""
	if not ma_hang:
		return {}
	rows = frappe.get_all(
		"Item Default",
		filters={
			"parent": ["in", list(ma_hang)],
			"company": company,
			"default_warehouse": ["is", "set"],
		},
		fields=["parent", "default_warehouse"],
	)
	return {r["parent"]: r["default_warehouse"] for r in rows}


def _gom_nhu_cau(dong):
	"""Bước 1 — {mã: số lượng cần} trên đơn, cộng dồn vì một đơn có thể lặp mặt hàng.

	Nhận thẳng DANH SÁCH DÒNG chứ không nhận tên đơn: đơn chưa lưu thì không có dòng nào trong
	cơ sở dữ liệu để mà truy vấn. Xem `_lay_don`.
	"""
	nhu_cau = {}
	for d in dong or []:
		ma = d.get("item_code")
		if not ma:
			continue
		nhu_cau[ma] = nhu_cau.get(ma, 0) + flt(d.get("qty"))
	return nhu_cau


def _lay_don(sales_order=None, doc=None):
	"""Trả về (đơn, tên đơn thật hoặc None).

	⚠ Nút *Kiểm Tra Tồn Kho* và ô tích *Ghim* phải chạy được cả khi đơn **CHƯA LƯU LẦN NÀO**.
	  Anh Thắng báo 03/09 10:32: *"lúc mới tạo phiếu anh chọn sản phẩm xong tích ghim thì không
	  thấy nó tính"*. Nguyên nhân: client gửi `frm.doc.name` mà tên đó đang là `new-sales-order-…`
	  — một cái tên chưa có trong cơ sở dữ liệu, `frappe.get_doc` ném lỗi và người dùng chỉ thấy
	  ô số không nhúc nhích. Đúng kiểu **hỏng im lặng** mà cả tính năng này sinh ra để chặn.

	  Nên khi đơn chưa lưu, client gửi nguyên tài liệu sang; ở đây dựng lại tài liệu trong bộ nhớ.
	  Tên đơn trả về là **None** để `ghim_boi_don_khac` không đi trừ một cái tên không tồn tại.
	"""
	if doc:
		don = frappe.get_doc(frappe.parse_json(doc) if isinstance(doc, str) else doc)
		if don.doctype != "Sales Order":
			frappe.throw(_("Chỉ dùng được cho Đơn Bán Hàng."))
		# Chưa lưu thì chưa có gì để kiểm quyền trên bản ghi — kiểm quyền ở mức DocType.
		if not frappe.has_permission("Sales Order", "read"):
			frappe.throw(_("Không có quyền đọc Đơn Bán Hàng."), frappe.PermissionError)
		ten = don.name if don.name and frappe.db.exists("Sales Order", don.name) else None
		return don, ten

	don = frappe.get_doc("Sales Order", sales_order)
	don.check_permission("read")
	return don, don.name


def _ngay_hang_ve(ma_hang):
	"""{mã: (ngày về sớm nhất, số lượng chưa nhận của ĐÚNG dòng đó, số ngày quá hạn)} — mục 8.2.

	⚠ Số lượng phải lấy của **chính dòng đơn mua đã cho ra ngày**, không phải tổng mọi đơn mua.
	  Khách hỏi 27/08 và anh Thắng xác nhận: *"lấy theo đơn mua sắm về nhất"*.
	⚠ Không có dòng nào thoả thì trả None để nơi gọi ghi **"chưa có đơn mua"**. Cố ý không để
	  trống: ô trống đọc như "về ngay", đúng kiểu sai im lặng mà cả tính năng này sinh ra để chặn.

	## 🔴 Sửa 04/09 — bỏ `poi.schedule_date >= CURDATE()`

	Điều kiện đó **vứt bỏ mọi đơn mua đã tới hẹn mà hàng chưa về**. Nó không phải "chỉ hiện đơn
	gần nhất" — nó hiện đơn sớm nhất **trong số đơn còn hạn**, và giấu sạch phần quá hạn.

	Đo trên site ngày 04/09, lượng bị giấu so với tổng đang trên đường về:

	    NVL 3             giấu 7/9   (78%)   màn hình nói "về 2"
	    NVL 2             giấu 3/8   (38%)   màn hình nói "về 5"
	    Thành phẩm 1      giấu 6/6   (100%)  màn hình nói "CHƯA CÓ ĐƠN MUA"
	    dịch vụ gia công  giấu 1/1   (100%)  màn hình nói "CHƯA CÓ ĐƠN MUA"

	Hai dòng cuối là chỗ nặng nhất: câu dự phòng *"chưa có đơn mua"* — vốn được thêm vào để chống
	sai im lặng — **trở thành một câu sai thẳng thừng**, vì đơn mua có thật, chỉ là đã trễ hẹn.

	Đây là gốc thật của lời khách phản ánh 03/09 17:03 về `SO-26-00013`. Khách viết *"đơn mua gần
	nhất chỉ 2 cái về vẫn chưa đủ, vậy là đang có đơn mua…"* — họ **biết** còn đơn khác; màn hình
	mới là chỗ nói sai.

	Chốt 27/08 của anh Thắng (*"lấy theo đơn mua sắm về nhất"*) **không hề loại đơn quá hạn** —
	đơn quá hạn vẫn là đơn về sớm nhất. Nên đây là sửa lỗi, không phải đổi nghiệp vụ.

	Đơn quá hạn còn là đơn **đáng chú ý nhất**: đó là đơn người lập kế hoạch phải đi giục. Giấu
	nó đi là giấu đúng thứ cần hiện. Vì vậy trả thêm `tre` để giao diện ghi rõ "quá hạn N ngày".

	⚠ Cột này **chỉ tính Đơn Mua Hàng đã duyệt**, không gồm Yêu Cầu Mặt Hàng — YCM chưa phải
	  nguồn cung chắc chắn. Đã ghi vào tài liệu để không ai đọc nhầm cột này là "tất cả hàng sắp về".
	"""
	if not ma_hang:
		return {}
	rows = frappe.db.sql(
		"""
		select poi.item_code, poi.schedule_date, (poi.qty - poi.received_qty) as con_lai
		from `tabPurchase Order Item` poi
		join `tabPurchase Order` po on po.name = poi.parent
		where po.docstatus = 1
		  and po.status not in ('Closed', 'Completed', 'Cancelled')
		  and poi.item_code in %(ma)s
		  and (poi.qty - poi.received_qty) > 0
		order by poi.item_code, poi.schedule_date
		""",
		{"ma": tuple(ma_hang)},
		as_dict=True,
	)
	hom_nay = getdate()
	ket = {}
	for r in rows:
		if r["item_code"] not in ket:      # đã order by schedule_date -> dòng đầu là sớm nhất
			ngay = getdate(r["schedule_date"]) if r["schedule_date"] else None
			tre = (hom_nay - ngay).days if ngay and ngay < hom_nay else 0
			ket[r["item_code"]] = (r["schedule_date"], flt(r["con_lai"]), tre)
	return ket


# ══════════ Bảng 3 — nguồn lực nhân sự ══════════
#
# Cột theo mục 6 của đầu bài: Tổng theo lịch · Đã phân bổ · Còn lại · Đơn này cần · kết luận,
# kèm danh sách mặt hàng Sản xuất/Gia công **chưa khai Thời Gian Sản Xuất** (anh Thắng chốt 5.2).
#
# ⚠ ĐƠN VỊ CỦA MỌI CON SỐ Ở ĐÂY LÀ **PHÚT CHUẨN**, không phải phút đồng hồ.
#   Đầu bài mục 8.1: khối lượng = Σ(số lượng × Thời Gian Sản Xuất). Engine Phần III tiêu thụ
#   khối lượng đó với tốc độ Σ(Năng Lực/100). Nên muốn so hai vế thì **năng lực phải nhân vào
#   phía CUNG**: một người 90% ngồi 100 phút chỉ làm xong 90 phút chuẩn. Không nhân là so
#   phút đồng hồ với phút chuẩn — hai đơn vị khác nhau, và sai về phía "báo đủ".

TRANG_THAI_NHAN_SU_TINH = ("Active",)


def _phut_giao_nhau(a1, a2, b1, b2):
	"""Số phút hai khoảng thời gian chồng lên nhau. Không chồng thì 0."""
	dau = max(a1, b1)
	cuoi = min(a2, b2)
	if cuoi <= dau:
		return 0.0
	return (cuoi - dau).total_seconds() / 60.0


def _nang_luc():
	"""{tên nhân sự: hệ số năng lực} — chỉ nhân sự đang làm việc.

	Không khai Năng Lực thì coi là 100%: đó là mức "bình thường", đoán thấp hơn sẽ báo thiếu ảo.
	"""
	rows = frappe.get_all(
		"Employee",
		filters={"status": ["in", list(TRANG_THAI_NHAN_SU_TINH)]},
		fields=["name", "employee_name", "custom_performance_factor_"],
	)
	ra = {}
	for r in rows:
		he_so = flt(r.get("custom_performance_factor_")) or 100.0
		# Employee Schedule/Allocation nối bằng `employee_name`, không phải mã nhân sự.
		ra[r.get("employee_name") or r["name"]] = he_so / 100.0
	return ra


def nguon_luc_nhan_su(don):
	"""Bảng 3. Trả về dict; **không bao giờ tự nhận là "Đủ" khi chưa đo được**.

	⚠ Đây là chỗ rủi ro R2 của đầu bài nằm: *"Bảng 3 sẽ ra gần 0 phút và luôn kết luận Đủ —
	  sai mà không có gì báo. Loại lỗi tệ nhất: im lặng và ra số đẹp."* Đo trên site 03/09 cho
	  thấy nó còn tệ hơn dự đoán vì **CẢ HAI VẾ đều rỗng**:

	      Employee Schedule   149 dòng / 3 người, nhưng chỉ tới 31/08 → từ hôm nay: 0 dòng
	      Employee Allocation còn hiệu lực trong tương lai: 0
	      Mặt hàng Sản xuất/Gia công CHƯA khai Thời Gian Sản Xuất: 59.743 / 59.746

	  0 so với 0 thì mọi phép so sánh đều ra "đủ". Nên hàm này **tách bạch ba trạng thái**:
	  `du` · `khong_du` · `chua_tinh_duoc`, và chỉ trả `du` khi **cả hai vế thật sự đo được**.
	"""
	hom_nay = getdate(nowdate())
	den = getdate(don.delivery_date) if don.get("delivery_date") else hom_nay
	if den < hom_nay:
		# Ngày giao đã qua — cùng cách xử lý với ngày trên Yêu Cầu Mặt Hàng: kẹp về hôm nay và
		# NÓI RA, thay vì tính trên một khoảng âm rồi ra 0 phút.
		den = hom_nay
		ngay_bi_kep = True
	else:
		ngay_bi_kep = False

	tu_dt = get_datetime(f"{hom_nay} 00:00:00")
	den_dt = get_datetime(f"{den} 23:59:59")

	nang_luc = _nang_luc()

	# ── Vế CUNG: lịch làm việc trong kỳ, quy về phút chuẩn ─────────────────────────
	lich = frappe.get_all(
		"Employee Schedule",
		filters={"date": ["between", [hom_nay, den]]},
		fields=["employee_name", "start_time", "end_time"],
	)
	tong_theo_lich = 0.0
	nguoi_co_lich = set()
	for r in lich:
		hs = nang_luc.get(r["employee_name"])
		if hs is None:
			continue  # nhân sự đã nghỉ việc: có lịch cũ nhưng không còn là năng lực
		phut = _phut_giao_nhau(get_datetime(r["start_time"]), get_datetime(r["end_time"]), tu_dt, den_dt)
		if phut > 0:
			tong_theo_lich += phut * hs
			nguoi_co_lich.add(r["employee_name"])

	# ── Đã phân bổ: cam kết ở Work Order khác, tính phần CHỒNG LÊN kỳ đang xét ─────
	da_phan_bo = 0.0
	for r in frappe.get_all(
		"Employee Allocation",
		filters={"start_time": ["<", den_dt], "end_time": [">", tu_dt]},
		fields=["employee_name", "start_time", "end_time"],
	):
		hs = nang_luc.get(r["employee_name"])
		if hs is None:
			continue
		da_phan_bo += _phut_giao_nhau(
			get_datetime(r["start_time"]), get_datetime(r["end_time"]), tu_dt, den_dt
		) * hs

	con_lai = max(0.0, tong_theo_lich - da_phan_bo)

	# ── Vế CẦU: khối lượng đơn này cần ────────────────────────────────────────────
	nhu_cau = _gom_nhu_cau(don.get("items"))
	pp = {
		r["name"]: (r.get("custom_replenishment_method") or "").strip()
		for r in frappe.get_all(
			"Item", filters={"name": ["in", list(nhu_cau)]},
			fields=["name", "custom_replenishment_method"],
		)
	} if nhu_cau else {}
	phai_san_xuat = {m: sl for m, sl in nhu_cau.items() if pp.get(m) in ("Sản xuất", "Gia công")}

	tgsx = {}
	if phai_san_xuat:
		tgsx = {
			r["name"]: flt(r.get("custom_time_to_manufacture"))
			for r in frappe.get_all(
				"Item",
				filters={"name": ["in", list(phai_san_xuat)]},
				fields=["name", "custom_time_to_manufacture"],
			)
		}

	don_can = 0.0
	thieu_dinh_muc = []
	for ma, sl in sorted(phai_san_xuat.items()):
		phut = tgsx.get(ma, 0.0)
		if phut > 0:
			don_can += sl * phut
		else:
			thieu_dinh_muc.append(ma)

	# ── Kết luận: chỉ nói "Đủ" khi ĐO ĐƯỢC cả hai vế ──────────────────────────────
	ly_do = []
	if not phai_san_xuat:
		ket_luan = "khong_ap_dung"
		ly_do.append("Đơn này không có mặt hàng nào phải sản xuất hoặc gia công.")
	elif thieu_dinh_muc and not don_can:
		ket_luan = "chua_tinh_duoc"
		ly_do.append(
			f"Chưa mặt hàng nào trên đơn khai Thời Gian Sản Xuất "
			f"({len(thieu_dinh_muc)} mặt hàng), nên không tính được đơn này cần bao nhiêu công."
		)
	elif not nguoi_co_lich:
		ket_luan = "chua_tinh_duoc"
		ly_do.append("Chưa nhân sự nào được xếp lịch làm việc trong khoảng đang xét.")
	else:
		ket_luan = "du" if con_lai >= don_can else "khong_du"

	# Cảnh báo nói thêm, KHÔNG đổi kết luận — người đọc cần biết con số đang thiếu phần nào.
	if thieu_dinh_muc and don_can:
		ly_do.append(
			f"Con số 'đơn này cần' mới tính được phần đã khai; còn {len(thieu_dinh_muc)} mặt hàng "
			"chưa khai Thời Gian Sản Xuất nên thực tế sẽ CAO HƠN."
		)
	if ngay_bi_kep:
		ly_do.append("Ngày giao của đơn đã qua — tính trong đúng ngày hôm nay.")

	return {
		"tu_ngay": str(hom_nay),
		"den_ngay": str(den),
		"so_nhan_su_co_lich": len(nguoi_co_lich),
		"tong_theo_lich": tong_theo_lich,
		"da_phan_bo": da_phan_bo,
		"con_lai": con_lai,
		"don_can": don_can,
		"ket_luan": ket_luan,
		"ly_do": ly_do,
		"thieu_dinh_muc": thieu_dinh_muc,
	}


@frappe.whitelist()
def kiem_tra(sales_order=None, doc=None):
	"""Điểm vào của nút *Kiểm Tra Tồn Kho*. Trả về dữ liệu cho Bảng 1 và Bảng 2.

	⚠ **Chỉ ĐỌC.** Không ghim vào đơn, không sinh Yêu Cầu Mặt Hàng hay Lệnh sản xuất, không
	  đụng Stock Ledger — chốt 19/08, và là lý do hàm này không gọi `auto_create_bom`.
	"""
	don, ten = _lay_don(sales_order, doc)

	kho = _kho_hop_le(don.company)
	nhu_cau = _gom_nhu_cau(don.get("items"))
	ghim, canh_bao = ghim_boi_don_khac(tru_don=ten)
	chi_tiet, cb_ct = ghim_chi_tiet(tru_don=ten)
	canh_bao = list(canh_bao) + list(cb_ct)

	# Một query Bin cho TẤT CẢ mã liên quan. Bóc định mức trước để biết đủ tập mã, rồi mới hỏi
	# tồn một lần — hỏi trong vòng lặp là bẫy N+1 kinh điển.
	# Bảng 1b / Bảng 2b — bung ra xem ĐƠN NÀO đang giữ. Mockup bản 6/7, anh Thắng hỏi lại 03/09.
	lech_chi_tiet = []

	def _chi_tiet(ma, da_tru):
		ds = chi_tiet.get(ma) or []
		if not ds:
			return None
		tong_ghim = sum(flt(r["giu"]) for r in ds)
		# Lưới an toàn: bảng chi tiết và con số đã trừ đi hai đường tính khác nhau. Lệch thì
		# nói ra, đừng để người đọc tự cộng tay rồi phát hiện.
		if abs(tong_ghim - flt(ghim.get(ma, 0))) > 0.001:
			lech_chi_tiet.append((ma, tong_ghim, flt(ghim.get(ma, 0))))
		return {
			"dong": ds[:5],                 # 5 đơn có ngày lấy hàng xa nhất
			"con_lai": max(0, len(ds) - 5),
			"tong_ghim": tong_ghim,
			"da_tru": flt(da_tru),
		}

	thieu_b1 = {}
	ton_b1 = _ton_thuc_te(set(nhu_cau) | set(ghim), kho)
	# Mã mà đơn khác ghim nhiều hơn số đang có. Phải nói ra: sau khi kẹp, con số "Đơn khác giữ"
	# trên màn hình lớn hơn phần thật sự bị trừ, và người test sẽ tưởng máy tính sai.
	vuot_ton = []
	bang1 = []
	for ma, can in sorted(nhu_cau.items()):
		ton = flt(ton_b1.get(ma, 0))
		kha_dung, ghim_hl, ghim_vuot = _kha_dung(ton, ghim.get(ma, 0))
		thieu = max(0.0, can - kha_dung)
		if thieu:
			thieu_b1[ma] = thieu
		if ghim_vuot:
			vuot_ton.append((ma, flt(ghim.get(ma, 0)), ton, ghim_vuot))
		bang1.append({
			"ma": ma,
			"can": can,
			"ton_thuc_te": ton,
			"ton_kha_dung": kha_dung,
			"dang_ghim": flt(ghim.get(ma, 0)),
			"ghim_hieu_luc": ghim_hl,
			"ghim_vuot_ton": ghim_vuot,
			"chi_tiet_ghim": _chi_tiet(ma, ghim_hl),
			"thieu": thieu,
		})

	# Bước 3+4: bóc theo TỪNG CẤP, trừ tồn khả dụng ở mỗi cấp bằng một bể dùng chung.
	#
	# 🔒 **ĐỔI 05/09/2026** — anh Thắng chốt 09:20: *"Bảng 2 em cũng phải trừ bán thành phẩm đang
	# có trong kho nhé"*. Trước đó truyền `thieu_b1` vào `boc_dinh_muc`, tức chỉ trừ tồn ở CẤP 0
	# rồi bóc thẳng xuống lá — bán thành phẩm nằm sẵn trong kho không được tính, và hệ thống bảo
	# đi mua nguyên vật liệu để làm ra thứ đang có.
	#
	# Nay truyền `nhu_cau` NGUYÊN (chưa trừ) và để hàm tự trừ ở từng cấp; riêng cấp 0 nó ra đúng
	# `thieu_b1` vì cùng công thức `_kha_dung`.
	#
	# ⚠ Con số này chảy thẳng vào phiếu **Yêu Cầu Mặt Hàng** qua `tinh_can_mua` — sửa ở đây là
	#   đổi số đi mua hàng thật, không phải đổi hiển thị.
	_can_mua_la, nvl = boc_dinh_muc_tru_ton(nhu_cau, kho, ghim=ghim, canh_bao=canh_bao)
	ton_b2 = _ton_thuc_te(set(nvl), kho)
	ve = _ngay_hang_ve(set(nvl))
	bang2 = []
	for ma, can in sorted(nvl.items()):
		ton = flt(ton_b2.get(ma, 0))
		kha_dung, ghim_hl, ghim_vuot = _kha_dung(ton, ghim.get(ma, 0))
		if ghim_vuot:
			vuot_ton.append((ma, flt(ghim.get(ma, 0)), ton, ghim_vuot))
		ngay, sl_ve, tre_ngay = ve.get(ma, (None, None, 0))
		bang2.append({
			"ma": ma,
			"can": can,
			"ton_thuc_te": ton,
			"ton_kha_dung": kha_dung,
			"dang_ghim": flt(ghim.get(ma, 0)),
			"ghim_hieu_luc": ghim_hl,
			"ghim_vuot_ton": ghim_vuot,
			"chi_tiet_ghim": _chi_tiet(ma, ghim_hl),
			"thieu": max(0.0, can - kha_dung),
			"ngay_hang_ve": ngay,
			"sl_ve": sl_ve,
			"tre_ngay": tre_ngay,
		})

	# Cùng một mã có thể bị bóc định mức ở hai nhánh (nhánh ghim và nhánh Bảng 2) nên cảnh báo
	# giống hệt nhau lặp lại. Người đọc thấy hai dòng y nguyên sẽ tưởng là hai lỗi khác nhau.
	da_co = set()
	gon = []
	for c in canh_bao:
		if c not in da_co:
			da_co.add(c)
			gon.append(c)
	canh_bao = gon

	for ma, tong_ct, tong_ghim in sorted(set(lech_chi_tiet)):
		canh_bao.append(
			f"{ma}: bảng chi tiết cộng ra {tong_ct:g} nhưng phần đang trừ là {tong_ghim:g} — "
			f"báo đội kỹ thuật, đừng dựa vào bảng bung ra của mã này"
		)

	for ma, ghim_ma, ton_ma, vuot in sorted(set(vuot_ton)):
		canh_bao.append(
			f"{ma}: đơn khác đang ghim {ghim_ma:g} nhưng kho chỉ có {ton_ma:g} — chỉ trừ được {ton_ma:g}. "
			f"Phần {vuot:g} còn lại KHÔNG cộng vào đơn này; cộng vào là hai đơn cùng mua một lượng hàng"
		)

	return {
		"don": don.name,
		"so_kho_tinh_ton": len(kho),
		"bang1": bang1,
		"bang2": bang2,
		"bang3": nguon_luc_nhan_su(don),
		"canh_bao": canh_bao,
	}


def tinh_can_mua(sales_order):
	"""{mã: số lượng cần mua} + cảnh báo. Dùng chung cho nút *Tạo Yêu Cầu Mặt Hàng*.

	🔒 **Anh Thắng chốt 03/09 16:51 — lấy THẲNG cột `Thiếu`, không trừ gì thêm:**

	> *"em cứ cho tạo dựa theo số lượng ở cột thiếu em nhé, không cần phải tính trừ các đơn đã
	> đặt mua đâu. Vì phần này anh đã thống nhất với khách là đơn nào thiếu bao nhiêu thì tự đặt
	> yêu cầu mua bằng đó, rồi muốn xin người khác nhường ghim hay như nào thì tự xin sau"*

	⚠ **Đây là ĐẢO NGƯỢC luật chốt ngày 28/08** (*"cần mua = đang thiếu − phiếu YCM đang chờ −
	  đơn mua chưa về"*, PM-TASK-00140). Hàm `_da_co_nguoi_lo` dựng cho luật cũ đã bị gỡ.
	  Hệ quả phải biết, anh Thắng đã cân nhắc và vẫn chọn: **bấm nút hai lần trên cùng một đơn
	  sẽ ra hai phiếu cho cùng một phần thiếu.** Hệ thống không còn tự trừ phần đã có người lo;
	  việc điều phối giữa các đơn là thoả thuận giữa người với nhau.

	⚠ Chỉ lấy mặt hàng *Mua hàng* (hoặc trống — coi như Mua hàng). Mặt hàng *Sản xuất/Gia công*
	  trên đơn không vào phiếu: phần thiếu của chúng đã được bóc thành nguyên vật liệu ở Bảng 2,
	  đưa cả hai vào là mua cả thành phẩm lẫn vật tư làm ra nó.
	"""
	kq = kiem_tra(sales_order)
	canh_bao = list(kq["canh_bao"])

	ma_b1 = [d["ma"] for d in kq["bang1"]]
	pp = {
		r["name"]: (r.get("custom_replenishment_method") or "").strip()
		for r in frappe.get_all(
			"Item", filters={"name": ["in", ma_b1]} if ma_b1 else {"name": ""},
			fields=["name", "custom_replenishment_method"],
		)
	}

	can_mua = {}
	o_b1 = set()
	for d in kq["bang1"]:
		if pp.get(d["ma"]) in ("Sản xuất", "Gia công"):
			continue                                   # đã bóc thành NVL ở Bảng 2
		if flt(d["thieu"]) > 0:
			can_mua[d["ma"]] = can_mua.get(d["ma"], 0) + flt(d["thieu"])
			o_b1.add(d["ma"])
	for d in kq["bang2"]:
		if flt(d["thieu"]) > 0:
			can_mua[d["ma"]] = can_mua.get(d["ma"], 0) + flt(d["thieu"])

	# Mã xuất hiện ở CẢ HAI bảng: vừa bán thẳng trên đơn, vừa là vật tư của mã khác. Hai dòng
	# `Thiếu` của nó đều đã được cùng một lượng tồn che, nên cộng lại là đặt mua dôi ra đúng
	# phần tồn đó. Luật mới của anh Thắng là cộng thẳng, nên chỗ này KHÔNG tự trừ — chỉ nói ra.
	ca_hai = sorted(o_b1 & {d["ma"] for d in kq["bang2"] if flt(d["thieu"]) > 0})
	if ca_hai:
		canh_bao.append(
			f"{', '.join(ca_hai)}: có ở cả Bảng 1 và Bảng 2 nên số cần mua là tổng hai dòng Thiếu — "
			"phần tồn đang có đã được tính trừ ở cả hai, kiểm lại trước khi gửi phiếu"
		)

	if not can_mua:
		return {}, canh_bao, kq

	return can_mua, canh_bao, kq


@frappe.whitelist()
def tao_yeu_cau_mua_hang(sales_order):
	"""Dựng sẵn một Yêu Cầu Mặt Hàng từ phần còn thiếu (PM-TASK-00140).

	Trả về tài liệu **CHƯA LƯU** để client mở ra dạng form mới. Cố ý không `insert()`:

	- Bấm nút mà đẻ ngay chứng từ trong cơ sở dữ liệu là ngược với luật đã ghi ở `CLAUDE.md` —
	  chứng từ thật phải qua một cú bấm rõ ràng, có nhìn thấy nội dung trước.
	- Người dùng bấm rồi đổi ý thì không để lại phiếu nháp rác; không phải đi dọn.

	⚠ **Phải kẹp `schedule_date` về hôm nay nếu ngày giao đã lùi quá khứ.**
	  `buying_controller.validate_schedule_date` **throw** khi `schedule_date < transaction_date`.
	  Đo 03/09: **8/8 đơn mẫu trên site đều có ngày giao trong quá khứ** — không kẹp thì gần như
	  đơn nào cũng vỡ ngay lúc lưu, và lỗi hiện ra là "Row #1: Reqd by Date cannot be before
	  Transaction Date", người dùng không nối được về nút vừa bấm.
	"""

	can_mua, canh_bao, kq = tinh_can_mua(sales_order)
	if not can_mua:
		return {
			"co_phieu": False,
			"canh_bao": canh_bao,
			# ⚠ Câu cũ còn vế *"hoặc phần thiếu đã có phiếu yêu cầu / đơn mua lo rồi"*. Từ
			#   03/09 vế đó KHÔNG còn đúng: anh Thắng chốt lấy thẳng cột `Thiếu`, hệ thống
			#   không trừ phần đã có người lo nữa (mục 6d của đầu bài). Để nguyên câu cũ là
			#   nói dối người dùng — và chính câu đó đã làm khách hiểu nhầm hôm nay 17:03:
			#   màn hình báo thiếu 21 mà nút lại bảo "đã có người lo", khách đi tìm đơn mua
			#   nào phủ được 21 mà không thấy (thứ phủ nó là một Phiếu Yêu Cầu 60 cái đang
			#   chờ, và phiếu yêu cầu thì không hiện ở bảng nào cả).
			"thong_bao": "Không có mặt hàng nào cần mua thêm — mọi mặt hàng trên đơn "
			"và vật tư bóc ra đều đủ tồn khả dụng.",
		}

	don = frappe.get_doc("Sales Order", sales_order)
	hom_nay = nowdate()
	ngay_can = don.delivery_date
	if not ngay_can or getdate(ngay_can) < getdate(hom_nay):
		ngay_can = hom_nay

	mat_hang = {
		r["name"]: r
		for r in frappe.get_all(
			"Item", filters={"name": ["in", list(can_mua)]},
			fields=["name", "stock_uom", "is_stock_item"],
		)
	}
	don_vi = {m: r["stock_uom"] for m, r in mat_hang.items()}

	# Kho nhận hàng — `Material Request Item.warehouse` là BẮT BUỘC với hàng tồn kho
	# (`buying/utils.py::validate_stock_item_warehouse` throw). Không đặt thì phiếu vỡ ngay lúc
	# lưu với thông báo "Warehouse is mandatory for stock Item", người dùng không nối được về
	# nút vừa bấm.
	#
	# ⚠ Không gõ cứng tên kho ("Kho nguyên vật liệu - HKL"): tên mang hậu tố công ty và sẽ khác
	#   khi lên site khác.
	#
	# Thứ tự ưu tiên — anh Thắng chốt **cách A** ngày 03/09 11:12:
	#
	#     kho mặc định CỦA CHÍNH MẶT HÀNG (Item Default, theo công ty)
	#       → kho của Đơn Bán  → kho trên dòng hàng  → mặc định hệ thống
	#
	# Vì sao mặt hàng phải thắng đơn: phiếu này chủ yếu mua **vật tư** bóc ra từ định mức, mà kho
	# của Đơn Bán là **kho thành phẩm** — vật tư về kho thành phẩm là sai nghiệp vụ. Đo 03/09:
	# phiếu 13 dòng vật tư đều rơi vào "Kho thành phẩm" đúng vì lý do đó.
	#
	# ⚠ Hôm nay đổi thứ tự này **chưa ra kết quả khác**: 0/62.055 bản ghi `Item Default` có khai
	#   `default_warehouse`. Nó chỉ có tác dụng sau khi khách khai kho — phần khai nằm ở
	#   **PM-FEAT-00037** (bảng Kho mặc định + tồn kho tối thiểu). Viết trước để lúc khách khai
	#   xong là chạy đúng ngay, không phải nhớ quay lại sửa.
	#
	# ⚠ Cố ý KHÔNG đặt `mr.set_warehouse` ở đầu phiếu: đặt thì giá trị đó lan xuống MỌI dòng,
	#   kể cả dòng dịch vụ. Gán theo từng dòng mới tách được hàng tồn kho với dịch vụ.
	kho_du_phong = don.get("set_warehouse")
	if not kho_du_phong:
		for d in don.items:
			if d.warehouse:
				kho_du_phong = d.warehouse
				break
	if not kho_du_phong:
		kho_du_phong = frappe.db.get_single_value("Stock Settings", "default_warehouse")

	kho_theo_mat_hang = _kho_mac_dinh(set(can_mua), don.company)

	# Mã không tra được trong danh mục -> BỎ QUA có cảnh báo, đừng để lọt vào phiếu.
	# Không có `stock_uom` thì `uom` rỗng, mà đó là trường BẮT BUỘC của Material Request Item:
	# phiếu vỡ lúc lưu với thông báo về đơn vị tính, người dùng không nối được về mã nào gây ra.
	# Ca kiểm này do phiên cozy-dev-0c nêu ra; code tôi trước đó thiếu.
	thieu_don_vi = sorted(m for m in can_mua if not don_vi.get(m))
	if thieu_don_vi:
		canh_bao.append(
			f"{len(thieu_don_vi)} mã không có trong danh mục hoặc thiếu đơn vị tính, "
			f"đã bỏ khỏi phiếu: " + ", ".join(thieu_don_vi[:8])
			+ ("…" if len(thieu_don_vi) > 8 else "")
		)
		for m in thieu_don_vi:
			can_mua.pop(m, None)
	if not can_mua:
		return {
			"co_phieu": False,
			"canh_bao": canh_bao,
			"thong_bao": "Không dựng được phiếu: mọi mã cần mua đều không tra được trong danh mục.",
		}

	mr = frappe.new_doc("Material Request")
	mr.material_request_type = "Purchase"
	mr.company = don.company
	mr.transaction_date = hom_nay
	mr.schedule_date = ngay_can
	for ma, sl in sorted(can_mua.items()):
		mr.append("items", {
			"item_code": ma,
			"qty": sl,
			"uom": don_vi.get(ma),
			"stock_uom": don_vi.get(ma),
			"conversion_factor": 1,
			"schedule_date": ngay_can,
			# Chỉ gán kho cho HÀNG TỒN KHO. `dịch vụ gia công` (is_stock_item = 0, đang dùng
			# thật ở PO-26-00001/00002) lưu được nếu có kho, ERPNext không chặn — nhưng một
			# dòng dịch vụ mang tên kho là dữ liệu vô nghĩa, và Phần V còn sinh thêm dòng
			# "dịch vụ gia công" nữa (chốt của Thắng 24/08 trên PM-FEAT-00030).
			"warehouse": (kho_theo_mat_hang.get(ma) or kho_du_phong)
			if mat_hang.get(ma, {}).get("is_stock_item")
			else None,
			# Gắn về Đơn Bán: truy ngược được, và là cách rẻ nhất để biết đơn này đã tạo phiếu chưa.
			"sales_order": don.name,
		})

	# Đã có phiếu nào cho chính đơn này chưa — chỉ CẢNH BÁO, không chặn.
	#
	# ⚠ Từ 03/09 cảnh báo này QUAN TRỌNG HƠN TRƯỚC. Anh Thắng chốt lấy thẳng cột `Thiếu`, nên
	#   hệ thống KHÔNG còn tự trừ phần đã có phiếu/đơn mua lo. Bấm nút hai lần trên cùng một đơn
	#   là ra hai phiếu cho cùng một phần thiếu, và chỉ dòng cảnh báo này nói cho người dùng biết.
	# 🔴 **SỬA 05/09 — câu cảnh báo cũ NÓI NGƯỢC.** Nó ghi *"Phần đã nằm trong các phiếu đó
	#   không được tính lại"*, trong khi từ chốt 03/09 hệ thống **không trừ gì cả**. Anh Thắng
	#   đọc câu đó, bấm nút hai lần thấy số y hệt, và báo lúc 05/09 14:38 *"nó đang không trừ đi
	#   phiếu trước đó thì phải"* — anh ấy đúng về hiện tượng, chỉ là câu chữ của em đã hứa một
	#   điều hệ thống không làm.
	#
	#   Đây đúng loại lỗi cả Phần IV sinh ra để chặn: câu dự phòng thêm vào để chống sai âm thầm
	#   lại trở thành câu sai thẳng. Cùng họ với ca *"chưa có đơn mua"* đã vá 04/09.
	#
	# Nay nói ĐÚNG việc đang xảy ra, và nói luôn **từng mã đã xin bao nhiêu** để người dùng tự
	# quyết — không tự trừ (giữ chốt của anh Thắng), nhưng cũng không để họ mua trùng vì không
	# biết.
	dong_cu = frappe.get_all(
		"Material Request Item",
		filters={"sales_order": don.name, "docstatus": ["<", 2]},
		fields=["parent", "item_code", "qty"],
	)
	if dong_cu:
		theo_ma = {}
		for d in dong_cu:
			if d["item_code"] in can_mua:
				theo_ma[d["item_code"]] = theo_ma.get(d["item_code"], 0) + flt(d["qty"])
		phieu_cu = sorted({d["parent"] for d in dong_cu})
		cau = (
			"Đơn này đã có phiếu yêu cầu mặt hàng: " + ", ".join(phieu_cu[:5])
			+ ". Hệ thống KHÔNG tự trừ phần đã xin trong các phiếu đó (chốt 03/09) — "
			"bấm lần nữa là ra thêm một phiếu cho cùng phần thiếu."
		)
		if theo_ma:
			cau += " Đã xin rồi: " + " · ".join(
				f"{m} {_so(sl)}" for m, sl in sorted(theo_ma.items())
			) + ". Kiểm lại trước khi gửi để khỏi mua trùng."
		canh_bao.append(cau)

	return {
		"co_phieu": True,
		"phieu": mr.as_dict(),
		"so_dong": len(mr.items),
		"canh_bao": canh_bao,
		"ngay_bi_kep": bool(don.delivery_date and getdate(don.delivery_date) < getdate(hom_nay)),
		# Từ 03/09 kho lấy theo TỪNG MẶT HÀNG (cách A), nên không còn "một cái kho" cho cả phiếu.
		# Trả về danh sách kho thực tế đã dùng để nơi gọi vẫn nói được với người dùng.
		"kho_nhan": sorted({r.warehouse for r in mr.items if r.warehouse}),
		"kho_du_phong": kho_du_phong,
	}
