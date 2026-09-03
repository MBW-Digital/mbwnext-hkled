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

	# Mặt hàng bị coi là lá NHƯNG lại có định mức — dấu hiệu khách quên khai Phương pháp bổ sung.
	# Đo 03/09: 487 mã đang để trống trường này (335 NULL + 152 chuỗi rỗng). Hiện chỉ 3 mã vừa
	# trống vừa có định mức, và cả 3 là dữ liệu thử. Nhưng nếu một thành phẩm thật rơi vào đó thì
	# hệ thống sẽ đi MUA CHÍNH NÓ thay vì mua nguyên vật liệu — sai hoàn toàn mà không báo gì.
	bom_cua_la = _bom_mac_dinh([m for m in ma if pp.get(m) not in ("Sản xuất", "Gia công")])

	for m in ma:
		sl = flt(nhu_cau[m])
		if pp.get(m) not in ("Sản xuất", "Gia công"):
			if m in bom_cua_la:
				canh_bao.append(
					f"{m}: Phương pháp bổ sung đang là {pp.get(m) or 'trống'} nên coi như phải mua, "
					f"nhưng mặt hàng này CÓ định mức ({bom_cua_la[m]}) — kiểm lại xem có phải hàng sản xuất"
				)
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
		"bang3": nguon_luc_nhan_su(don),
		"canh_bao": canh_bao,
	}


def _da_co_nguoi_lo(ma_hang):
	"""{mã: số lượng đã có người lo} = Yêu Cầu Mặt Hàng đang chờ + Đơn mua chưa về.

	⚠ Không trừ phần này thì bấm nút hai lần là đặt mua hai lần. Đây là chỗ tôi đã hứa với anh
	  Thắng 28/08: *"cần mua = đang thiếu − phiếu yêu cầu đang chờ − đơn mua chưa về"*.
	"""
	if not ma_hang:
		return {}
	ket = {}

	# Yêu Cầu Mặt Hàng đã duyệt, phần chưa được đặt mua
	for r in frappe.db.sql(
		"""
		select mri.item_code, sum(mri.stock_qty - mri.ordered_qty) as con
		from `tabMaterial Request Item` mri
		join `tabMaterial Request` mr on mr.name = mri.parent
		where mr.docstatus = 1 and mr.material_request_type = 'Purchase'
		  and mr.status not in ('Stopped', 'Cancelled')
		  and mri.item_code in %(ma)s and (mri.stock_qty - mri.ordered_qty) > 0
		group by mri.item_code
		""",
		{"ma": tuple(ma_hang)},
		as_dict=True,
	):
		ket[r["item_code"]] = ket.get(r["item_code"], 0) + flt(r["con"])

	# Đơn mua đã duyệt, phần chưa nhận — không lọc ngày ở đây: hàng về muộn vẫn là hàng đã đặt,
	# đặt thêm là mua thừa. Khác với mục 8.2 (cột *Ngày hàng về*) vốn chỉ hiện ngày trong tương lai.
	for r in frappe.db.sql(
		"""
		select poi.item_code, sum(poi.stock_qty - poi.received_qty) as con
		from `tabPurchase Order Item` poi
		join `tabPurchase Order` po on po.name = poi.parent
		where po.docstatus = 1 and po.status not in ('Closed', 'Completed', 'Cancelled')
		  and poi.item_code in %(ma)s and (poi.stock_qty - poi.received_qty) > 0
		group by poi.item_code
		""",
		{"ma": tuple(ma_hang)},
		as_dict=True,
	):
		ket[r["item_code"]] = ket.get(r["item_code"], 0) + flt(r["con"])

	return ket


def tinh_can_mua(sales_order):
	"""{mã: số lượng cần mua} + cảnh báo. Dùng chung cho nút *Tạo Yêu Cầu Mặt Hàng*.

	⚠ **KHÔNG cộng thẳng `thieu` của Bảng 1 với `thieu` của Bảng 2.** Hai bảng cùng trừ vào một
	  lượng tồn: mã vừa bán trên đơn vừa là thành phần của mã khác sẽ được tồn "che" hai lần, ra
	  số thiếu ÍT hơn thực tế. Ở đây gom **nhu cầu** theo mã trước, rồi mới trừ tồn MỘT LẦN.

	⚠ Chỉ lấy mặt hàng *Mua hàng* (hoặc trống — coi như Mua hàng), theo đúng mô tả PM-TASK-00140.
	  Mặt hàng *Sản xuất/Gia công* trên đơn không vào phiếu: phần thiếu của chúng đã được bóc
	  thành nguyên vật liệu ở Bảng 2 rồi, đưa cả hai vào là mua cả thành phẩm lẫn vật tư làm ra nó.
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

	nhu_cau = {}
	for d in kq["bang1"]:
		if pp.get(d["ma"]) in ("Sản xuất", "Gia công"):
			continue                                   # đã bóc thành NVL ở Bảng 2
		nhu_cau[d["ma"]] = nhu_cau.get(d["ma"], 0) + flt(d["can"])
	for d in kq["bang2"]:
		nhu_cau[d["ma"]] = nhu_cau.get(d["ma"], 0) + flt(d["can"])

	if not nhu_cau:
		return {}, canh_bao, kq

	kho = _kho_hop_le(frappe.db.get_value("Sales Order", sales_order, "company"))
	ton = _ton_thuc_te(set(nhu_cau), kho)
	# ⚠ KHÔNG đặt tên `_`: module này đã import `_` là hàm dịch của Frappe. Gán đè lên nó thì
	#   `_("...")` ở chỗ khác nổ `'list' object is not callable`.
	ghim, _cb = ghim_boi_don_khac(tru_don=sales_order)
	da_lo = _da_co_nguoi_lo(set(nhu_cau))

	can_mua = {}
	for ma, can in nhu_cau.items():
		kha_dung = flt(ton.get(ma, 0)) - flt(ghim.get(ma, 0))
		con_thieu = can - kha_dung - flt(da_lo.get(ma, 0))
		if con_thieu > 0:
			can_mua[ma] = con_thieu

	bo_qua = sorted(set(nhu_cau) - set(can_mua))
	if bo_qua:
		canh_bao.append(
			f"{len(bo_qua)} mã không đưa vào phiếu vì đã đủ tồn hoặc đã có phiếu/đơn mua lo: "
			+ ", ".join(bo_qua[:8]) + ("…" if len(bo_qua) > 8 else "")
		)
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
			"thong_bao": "Không có mặt hàng nào cần mua thêm — đơn này đủ tồn, "
			"hoặc phần thiếu đã có phiếu yêu cầu / đơn mua lo rồi.",
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

	# Đã có phiếu nào cho chính đơn này chưa — chỉ CẢNH BÁO, không chặn: người dùng có thể cố ý
	# tạo phiếu thứ hai cho phần mới phát sinh. Phần trùng đã bị trừ ở `_da_co_nguoi_lo`.
	phieu_cu = frappe.get_all(
		"Material Request Item",
		filters={"sales_order": don.name, "docstatus": ["<", 2]},
		fields=["parent"], group_by="parent", pluck="parent",
	)
	if phieu_cu:
		canh_bao.append(
			"Đơn này đã có phiếu yêu cầu mặt hàng: " + ", ".join(phieu_cu[:5])
			+ ". Phần đã nằm trong các phiếu đó không được tính lại."
		)

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
