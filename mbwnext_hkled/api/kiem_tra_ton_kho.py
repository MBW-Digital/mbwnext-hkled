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
from frappe.utils import flt


# Hai nhóm kho bị loại khỏi mọi phép tính tồn (mục 3 của đầu bài).
#
# ⚠ Lấy kho con bằng `lft/rgt` của cây Warehouse, KHÔNG so tên: tên có hậu tố công ty
# ("- HKL") và sẽ khác khi lên site khác. Tên ở đây chỉ để TÌM nút gốc; tìm không thấy thì
# bỏ qua nhóm đó chứ không throw — site mới chưa dựng cây kho vẫn phải chạy được.
NHOM_KHO_LOAI = ("Nhóm kho lỗi", "Nhóm kho trung chuyển")


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


def boc_dinh_muc(nhu_cau, da_tham=None, canh_bao=None):
	"""Bóc {mã: số lượng} xuống NVL lá. Trả về {mã NVL: tổng số lượng}.

	Mặt hàng *Mua hàng* (hoặc bỏ trống Phương pháp bổ sung — coi như Mua hàng) là lá: chính nó
	là thứ phải mua. Mặt hàng *Sản xuất / Gia công* thì bóc tiếp theo BOM mặc định.

	⚠ Gom hết rồi mới trừ tồn MỘT LẦN ở ngoài, không trừ tại từng nhánh — trừ sớm thì cùng một
	  lượng tồn bị đếm cho nhiều nhánh (bước 4 của đầu bài).
	⚠ `da_tham` chặn BOM lặp vòng. Khách khẳng định không có, nhưng đó là **tình trạng dữ liệu**
	  chứ không phải ràng buộc hệ thống — một BOM vòng làm treo cả tiến trình, không phải báo lỗi.
	"""
	da_tham = da_tham if da_tham is not None else set()
	canh_bao = canh_bao if canh_bao is not None else []
	ket = {}

	ma = [m for m, sl in nhu_cau.items() if flt(sl) > 0]
	if not ma:
		return ket

	pp = {
		r["name"]: (r.get("custom_replenishment_method") or "").strip()
		for r in frappe.get_all(
			"Item", filters={"name": ["in", ma]},
			fields=["name", "custom_replenishment_method"],
		)
	}
	bom_cua = _bom_mac_dinh([m for m in ma if pp.get(m) in ("Sản xuất", "Gia công")])

	for m in ma:
		sl = flt(nhu_cau[m])
		if pp.get(m) not in ("Sản xuất", "Gia công"):
			ket[m] = ket.get(m, 0) + sl          # Mua hàng, hoặc trống -> là lá
			continue
		if m in da_tham:
			canh_bao.append(f"{m}: định mức lặp vòng, dừng bóc tại đây")
			ket[m] = ket.get(m, 0) + sl
			continue
		ten_bom = bom_cua.get(m)
		if not ten_bom:
			# Chưa có BOM. KHÔNG tự sinh ở đây: `auto_create_bom` submit chứng từ thật và gỡ
			# cờ is_default của BOM cũ — việc đó phải qua một cú bấm rõ ràng, không được xảy ra
			# lúc người dùng chỉ bấm xem tồn kho.
			canh_bao.append(f"{m}: chưa có định mức, tạm coi như phải mua")
			ket[m] = ket.get(m, 0) + sl
			continue

		con = {}
		for nvl, dinh_muc in _dong_bom(ten_bom):
			con[nvl] = con.get(nvl, 0) + dinh_muc * sl
		for nvl, sl_con in boc_dinh_muc(con, da_tham | {m}, canh_bao).items():
			ket[nvl] = ket.get(nvl, 0) + sl_con

	return ket


def ghim_boi_don_khac(tru_don=None):
	"""{mã: số lượng đang bị các đơn KHÁC giữ chỗ}, đã tính cả NVL bóc từ định mức của họ.

	⚠ Đọc thẳng `custom_so_luong_giu_cho`, KHÔNG suy từ `qty − delivered_qty`. Từ 03/09 ghim là
	  một con số người dùng nhập: đơn giữ 1 trên dòng 5 cái thì chỉ chiếm 1.
	⚠ Cũng KHÔNG trừ `delivered_qty` ở đây. Giao hàng đã làm `Bin.actual_qty` giảm thật rồi; trừ
	  thêm lần nữa là trừ hai lần.
	"""
	don = frappe.get_all(
		"Sales Order",
		filters={
			"docstatus": 1,
			"custom_ghim_ton_kha_dung": 1,
			"status": ["not in", ["Closed", "Completed", "Cancelled"]],
			**({"name": ["!=", tru_don]} if tru_don else {}),
		},
		pluck="name",
	)
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
	gian_tiep = boc_dinh_muc(_con_mot_cap(truc_tiep, canh_bao), canh_bao=canh_bao)

	# Thành phẩm bị giữ trực tiếp VÀ nguyên vật liệu của nó đều bị giữ — hai thứ nằm ở hai kho
	# khác nhau nên cộng cả hai là đúng. Chỉ có mã mua ngoài mới không được cộng lặp, và
	# `_con_mot_cap` đã loại chúng khỏi nhánh gián tiếp.
	tong = dict(gian_tiep)
	for m, sl in truc_tiep.items():
		tong[m] = tong.get(m, 0) + sl
	return tong, canh_bao


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


def _gom_nhu_cau(don):
	"""Bước 1 — {mã: số lượng cần} trên đơn, cộng dồn vì một đơn có thể lặp mặt hàng."""
	nhu_cau = {}
	for d in frappe.get_all(
		"Sales Order Item", filters={"parent": don}, fields=["item_code", "qty"]
	):
		nhu_cau[d["item_code"]] = nhu_cau.get(d["item_code"], 0) + flt(d["qty"])
	return nhu_cau


def _ngay_hang_ve(ma_hang):
	"""{mã: (ngày về sớm nhất, số lượng chưa nhận của ĐÚNG dòng đó)} — mục 8.2.

	⚠ Số lượng phải lấy của **chính dòng đơn mua đã cho ra ngày**, không phải tổng mọi đơn mua.
	  Khách hỏi 27/08 và anh Thắng xác nhận: *"lấy theo đơn mua sắm về nhất"*.
	⚠ Không có dòng nào thoả thì trả None để nơi gọi ghi **"chưa có đơn mua"**. Cố ý không để
	  trống: ô trống đọc như "về ngay", đúng kiểu sai im lặng mà cả tính năng này sinh ra để chặn.
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
		  and poi.schedule_date >= CURDATE()
		order by poi.item_code, poi.schedule_date
		""",
		{"ma": tuple(ma_hang)},
		as_dict=True,
	)
	ket = {}
	for r in rows:
		if r["item_code"] not in ket:      # đã order by schedule_date -> dòng đầu là sớm nhất
			ket[r["item_code"]] = (r["schedule_date"], flt(r["con_lai"]))
	return ket


@frappe.whitelist()
def kiem_tra(sales_order):
	"""Điểm vào của nút *Kiểm Tra Tồn Kho*. Trả về dữ liệu cho Bảng 1 và Bảng 2.

	⚠ **Chỉ ĐỌC.** Không ghim vào đơn, không sinh Yêu Cầu Mặt Hàng hay Lệnh sản xuất, không
	  đụng Stock Ledger — chốt 19/08, và là lý do hàm này không gọi `auto_create_bom`.
	"""
	don = frappe.get_doc("Sales Order", sales_order)
	don.check_permission("read")

	kho = _kho_hop_le(don.company)
	nhu_cau = _gom_nhu_cau(don.name)
	ghim, canh_bao = ghim_boi_don_khac(tru_don=don.name)

	# Một query Bin cho TẤT CẢ mã liên quan. Bóc định mức trước để biết đủ tập mã, rồi mới hỏi
	# tồn một lần — hỏi trong vòng lặp là bẫy N+1 kinh điển.
	thieu_b1 = {}
	ton_b1 = _ton_thuc_te(set(nhu_cau) | set(ghim), kho)
	bang1 = []
	for ma, can in sorted(nhu_cau.items()):
		ton = flt(ton_b1.get(ma, 0))
		kha_dung = ton - flt(ghim.get(ma, 0))
		thieu = max(0.0, can - kha_dung)
		if thieu:
			thieu_b1[ma] = thieu
		bang1.append({
			"ma": ma,
			"can": can,
			"ton_thuc_te": ton,
			"ton_kha_dung": kha_dung,
			"dang_ghim": flt(ghim.get(ma, 0)),
			"thieu": thieu,
		})

	# Bước 3+4: chỉ bóc phần CÒN THIẾU, gom hết rồi mới trừ tồn một lần.
	nvl = boc_dinh_muc(thieu_b1, canh_bao=canh_bao)
	ton_b2 = _ton_thuc_te(set(nvl), kho)
	ve = _ngay_hang_ve(set(nvl))
	bang2 = []
	for ma, can in sorted(nvl.items()):
		ton = flt(ton_b2.get(ma, 0))
		kha_dung = ton - flt(ghim.get(ma, 0))
		ngay, sl_ve = ve.get(ma, (None, None))
		bang2.append({
			"ma": ma,
			"can": can,
			"ton_thuc_te": ton,
			"ton_kha_dung": kha_dung,
			"dang_ghim": flt(ghim.get(ma, 0)),
			"thieu": max(0.0, can - kha_dung),
			"ngay_hang_ve": ngay,
			"sl_ve": sl_ve,
		})

	return {
		"don": don.name,
		"so_kho_tinh_ton": len(kho),
		"bang1": bang1,
		"bang2": bang2,
		"canh_bao": canh_bao,
	}
