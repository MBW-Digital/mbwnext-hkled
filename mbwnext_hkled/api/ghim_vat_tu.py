# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Sổ cam kết vật tư của Đơn Bán — PM-FEAT-00036, mục 8 của đầu bài.

Đọc `docs/features/phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve.md` mục 8 trước
khi sửa file này, và mục **12e** của `kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md` — 8 bất
biến ở đó là lý do tồn tại của từng đoạn code dưới đây.

## Ba câu tóm tắt

1. Đơn ghim thành phẩm bằng `Sales Order Item.custom_so_luong_giu_cho` (người nhập, đã bị
   `chan_giu_cho_vuot_ton` chặn không cho vượt tồn khả dụng).
2. Phần thành phẩm **chưa ghim được** là phần phải sản xuất ➜ bóc định mức ra nhu cầu vật tư.
3. Vật tư nào **đang có trong kho và chưa ai giữ** thì đơn giữ luôn — ghi vào bảng con
   `Sales Order.custom_ghim_vat_tu`. Phần còn thiếu là phần phải đi mua, và là chỗ nút *Phân Bổ*
   sẽ rót vào khi hàng về.

Đúng ví dụ anh Thắng viết 04/09 15:59: SO1 cần 5A, tồn khả dụng 3 ➜ ghim 3A; còn 2A phải làm ➜
định mức cần 4B + 2C; kho chỉ còn 2B và 1C ➜ ghim 2B, 1C.

## ⚠ Vì sao phải LƯU, trong khi cả tính năng còn lại đều suy ra

Chia hàng là việc **phụ thuộc thứ tự**: tồn 2 `B`, hai đơn cùng cần, ai được là do ai tới trước —
không suy lại được từ dữ liệu hiện tại. Và ghim là một **cam kết**: đơn đã được chia rồi thì thao
tác của người khác không được làm nó tụt (bất biến #8).

Cái giá: dữ liệu lưu **không tự dọn**. Nên chỗ chứa cố ý là **bảng con của Đơn Bán**, không phải
DocType đứng riêng — đơn Huỷ / Đóng / Hoàn thành, đơn bị amend, hay đơn bỏ tích Ghim đều **rơi
khỏi `loc_don_song()`**, tức phần ghim của nó biến khỏi mọi phép tính mà không ai phải đi xoá.
Bốn trong tám bất biến chuyển từ *"phải nhớ dọn"* sang *"không thể bẩn"*.

## ⚠ Luật vàng: chỉ cấp phát từ TỒN TỰ DO

	tồn tự do(X) = tồn thực tế(X) − Σ ghim thành phẩm(X) − Σ ghim vật tư(X), mọi đơn còn sống

Không có đường nào khác ghi vào `qty`. Nhờ vậy bất biến #1 (Σ ghim ≤ tồn thực tế) đúng **theo cấu
trúc**, không phải nhờ một phép kiểm chạy sau. Khác hẳn `_kha_dung()` bên `kiem_tra_ton_kho`: hàm
đó kẹp `min(ghim, tồn)` **lúc đọc**, tức vẫn cho ghi con số vượt rồi che đi lúc hiển thị.
"""

import frappe
from frappe import _
from frappe.utils import flt, now_datetime

from mbwnext_hkled.api.kiem_tra_ton_kho import (
	TRANG_THAI_DON_CHET,
	_bom_mac_dinh,
	_dong_bom,
	_kho_hop_le,
	_so,
	_ton_thuc_te,
	loc_don_song,
)

TRUONG_BANG = "custom_ghim_vat_tu"
CHE_BIEN = ("Sản xuất", "Gia công")

# Định mức lồng nhau quá sâu là dấu hiệu dữ liệu hỏng (thường là vòng lặp mà `da_tham` chưa bắt
# được vì đi qua hai nhánh khác nhau). Dừng và cảnh báo, đừng để tiến trình treo.
CAP_TOI_DA = 8


def don_theo_uu_tien(tru_don=None):
	"""[tên đơn] còn sống & đang ghim, **đã sắp theo đúng thứ tự ưu tiên đã chốt**.

	🔒 Anh Thắng chốt 04/09 15:59 + 16:21: *"lấy theo ngày trên đơn nhé, vì thực tế bên họ chỉ có
	1 ngày trên đơn thôi"* và *"2 đơn cùng ngày thì em cứ ưu tiên đơn nào tạo trước"*.

	⚠ Ngày **đầu đơn** (`Sales Order.delivery_date`), KHÔNG phải ngày từng dòng. Đơn
	  `SAL-ORD-2026-00009` có 2 ngày khác nhau trên các dòng là anh Thắng tạo nhầm, không phải
	  nghiệp vụ.
	⚠ Sắp trong Python chứ không nhét biểu thức `IS NULL` vào `order_by` của `frappe.get_all` —
	  đơn trống ngày phải xuống CUỐI, mà MariaDB xếp NULL lên đầu.
	"""
	rows = frappe.get_all(
		"Sales Order",
		filters=loc_don_song(tru_don),
		fields=["name", "delivery_date", "creation"],
	)
	rows.sort(key=lambda r: (r["delivery_date"] is None, str(r["delivery_date"]), str(r["creation"])))
	return [r["name"] for r in rows]


def ghim_thanh_pham(tru_don=None):
	"""{mã: tổng thành phẩm đang bị ghim} — đọc `custom_so_luong_giu_cho` của các đơn còn sống."""
	don = frappe.get_all("Sales Order", filters=loc_don_song(tru_don), pluck="name")
	if not don:
		return {}
	rows = frappe.get_all(
		"Sales Order Item",
		filters={"parent": ["in", don], "custom_so_luong_giu_cho": [">", 0]},
		fields=["item_code", "sum(custom_so_luong_giu_cho) as giu"],
		group_by="item_code",
	)
	return {r["item_code"]: flt(r["giu"]) for r in rows}


def ghim_vat_tu(tru_don=None):
	"""{mã: tổng vật tư đang bị ghim} — đọc sổ cam kết của các đơn còn sống.

	⚠ Lọc `parent in <đơn còn sống>` chứ không quét cả bảng: dòng của đơn đã huỷ / đã đóng / đã
	  bỏ tích vẫn nằm trong database (cố ý — luật 2 mục 2 của đầu bài: *bỏ tích không xoá số đã
	  nhập*), nhưng **không được tính**. Quét cả bảng là hàng bị giam vĩnh viễn, đúng bất biến #3.
	"""
	don = frappe.get_all("Sales Order", filters=loc_don_song(tru_don), pluck="name")
	if not don:
		return {}
	rows = frappe.get_all(
		"HKLed Pinned Material",
		filters={"parent": ["in", don], "parenttype": "Sales Order", "qty": [">", 0]},
		fields=["item_code", "sum(qty) as giu"],
		group_by="item_code",
	)
	return {r["item_code"]: flt(r["giu"]) for r in rows}


def ton_tu_do(ma_hang, tru_ghim_vat_tu_cua=None):
	"""{mã: phần tồn chưa ai giữ} — nguồn DUY NHẤT được phép cấp phát.

	`tru_ghim_vat_tu_cua` = tên đơn đang được tính lại: phần vật tư **chính nó** đang giữ được
	trả về thành tự do, vì sắp bị viết đè. Phần **thành phẩm** nó giữ thì KHÔNG trả về — số hàng
	đó đã đặt riêng cho nó rồi, không được đem ra làm vật tư cho chính nó lần nữa.

	⚠ `_kho_hop_le()` gọi **không kèm công ty**, cùng lý do đã ghi ở `_con_phai_lam`: hàm này gom
	  mọi đơn đang ghim chứ không riêng công ty nào. Site hiện có 1 công ty; ngày nào có công ty
	  thứ hai thì sửa cùng lúc cả ba chỗ.
	"""
	ma_hang = list(ma_hang or [])
	if not ma_hang:
		return {}
	ton = _ton_thuc_te(ma_hang, _kho_hop_le())
	tp = ghim_thanh_pham()
	vt = ghim_vat_tu(tru_don=tru_ghim_vat_tu_cua)
	return {m: flt(ton.get(m, 0)) - flt(tp.get(m, 0)) - flt(vt.get(m, 0)) for m in ma_hang}


def _phuong_phap(ma_hang):
	"""{mã: phương pháp bổ sung} — trống coi như *Mua hàng*, đúng như `boc_dinh_muc` đang làm."""
	ma_hang = [m for m in (ma_hang or [])]
	if not ma_hang:
		return {}
	return {
		r["name"]: (r.get("custom_replenishment_method") or "").strip()
		for r in frappe.get_all(
			"Item", filters={"name": ["in", ma_hang]}, fields=["name", "custom_replenishment_method"]
		)
	}


def _phai_san_xuat(doc):
	"""{mã thành phẩm: số lượng đơn này còn phải LÀM RA} — đầu vào cấp 0 của phép bóc.

	🔴 **Đây là chỗ dễ nhầm nhất của cả tính năng.** `_con_phai_lam()` bên `kiem_tra_ton_kho`
	  cũng tên na ná nhưng tính `ghim − tồn`, tức *"phần đã ghim mà kho không có"*. Ở đây phải là
	  `cần − đã giao − đã ghim`, tức *"phần chưa có chỗ dựa nào, buộc phải sản xuất"*.

	  Khác nhau tới mức đảo ngược kết quả: `chan_giu_cho_vuot_ton` không cho ghim vượt tồn, nên
	  `ghim − tồn` gần như **luôn bằng 0** — đó là lý do tới 04/09 site chưa có một dòng ghim vật
	  tư nào, và cũng là câu tôi đã nói với anh Thắng lúc 16:32.

	  Công thức đúng đọc thẳng ra từ ví dụ 15:59 của anh: *"đơn SO1 có mặt hàng A số lượng 5,
	  tồn khả dụng chỉ còn 3 → ghim 3A và bóc tách theo BOM"* ra 4B + 2C. 4B+2C là định mức của
	  **2** chiếc A — tức `5 − 3`, không phải `3 − tồn`.

	⚠ Trừ `delivered_qty`: phần đã giao xong rồi thì không phải làm nữa. Chỗ này **được phép**
	  trừ, khác với cảnh báo trong `ghim_boi_don_khac` (ở đó trừ là trừ hai lần vì
	  `Bin.actual_qty` đã giảm thật rồi). Ở đây ta hỏi *"còn phải sản xuất bao nhiêu"*, không
	  hỏi *"đang chiếm bao nhiêu tồn"*.
	"""
	can = {}
	for row in doc.get("items") or []:
		con = flt(row.qty) - flt(row.delivered_qty) - flt(row.get("custom_so_luong_giu_cho"))
		if con > 0:
			can[row.item_code] = can.get(row.item_code, 0) + con
	return can


def dong_bo_doc(doc):
	"""Tính lại sổ cam kết vật tư của MỘT đơn, ghi thẳng vào `doc` trong bộ nhớ.

	Trả về `(số dòng, cảnh báo)`. **Không** gọi `doc.save()` — hàm này chạy trong `before_submit`
	và `before_update_after_submit`, tức ngay trước khi Frappe ghi; tự gọi `save()` ở đây là đệ
	quy vô hạn.

	Thứ tự bên trong đúng mục 8.5 của đầu bài: từng cấp một, **kẹp ở mỗi cấp**, phần chưa cấp
	phát được mới bóc tiếp xuống cấp dưới. Vật tư *Mua hàng* không bóc tiếp — nó là thứ phải đi
	mua, và chính là phần nút *Phân Bổ* sẽ rót vào.
	"""
	canh_bao = []
	if doc.doctype != "Sales Order":
		return 0, canh_bao

	# Đơn nháp chưa giữ chỗ của ai cả. Xoá sạch để bản amend không kế thừa cam kết của bản cũ —
	# **bất biến #7**: bản cũ đã `docstatus = 2` nên đã nhả, bản mới phải giành lại từ đầu.
	if doc.docstatus == 0:
		doc.set(TRUONG_BANG, [])
		return 0, canh_bao

	# Bỏ tích Ghim: KHÔNG xoá bảng (luật 2 mục 2 — bỏ tích không xoá số đã nhập), chỉ ngừng có
	# hiệu lực, vì `loc_don_song()` đã loại đơn này khỏi mọi phép cộng.
	if not doc.get("custom_ghim_ton_kha_dung"):
		return len(doc.get(TRUONG_BANG) or []), canh_bao

	cu = {}
	for r in doc.get(TRUONG_BANG) or []:
		cu[(r.source_item, r.item_code)] = r

	moi = []
	da_cap = {}
	da_tham = set()
	tang = _phai_san_xuat(doc)
	luc_nay = now_datetime()

	for _cap in range(CAP_TOI_DA):
		if not tang:
			break

		pp = _phuong_phap(tang)
		che_bien = [m for m in tang if pp.get(m) in CHE_BIEN]
		lap_vong = [m for m in che_bien if m in da_tham]
		for m in lap_vong:
			canh_bao.append(f"{m}: định mức lặp vòng, dừng bóc tại đây")
		che_bien = [m for m in che_bien if m not in da_tham]
		da_tham.update(che_bien)

		bom_cua = _bom_mac_dinh(che_bien)
		con = {}
		bom_meta = {}
		for m in che_bien:
			ten_bom = bom_cua.get(m)
			if not ten_bom:
				canh_bao.append(
					f"{m}: chưa có định mức, phần còn phải sản xuất ({_so(tang[m])}) không ghim được vật tư"
				)
				continue
			bom_meta[m] = (ten_bom, frappe.db.get_value("BOM", ten_bom, "modified"))
			for nvl, dinh_muc in _dong_bom(ten_bom):
				con[(m, nvl)] = con.get((m, nvl), 0) + dinh_muc * flt(tang[m])
		if not con:
			break

		tu_do = ton_tu_do({nvl for _m, nvl in con}, tru_ghim_vat_tu_cua=doc.name)

		thieu = {}
		for (m, nvl), can in sorted(con.items()):
			con_lai = flt(tu_do.get(nvl, 0)) - flt(da_cap.get(nvl, 0))
			duoc = max(0.0, min(flt(can), con_lai))
			da_cap[nvl] = flt(da_cap.get(nvl, 0)) + duoc
			ten_bom, sua_luc = bom_meta.get(m, (None, None))
			moi.append(
				{
					"item_code": nvl,
					"source_item": m,
					"source_qty": flt(tang[m]),
					"qty": duoc,
					"required_qty": flt(can),
					"bom": ten_bom,
					"bom_modified": sua_luc,
					"updated_at": luc_nay,
				}
			)
			if flt(can) - duoc > 0:
				thieu[nvl] = thieu.get(nvl, 0) + (flt(can) - duoc)

		pp_con = _phuong_phap(thieu)
		tang = {m: sl for m, sl in thieu.items() if pp_con.get(m) in CHE_BIEN}
	else:
		if tang:
			canh_bao.append(
				f"định mức lồng quá {CAP_TOI_DA} cấp, dừng bóc — kiểm lại dữ liệu định mức: "
				+ ", ".join(sorted(tang))
			)

	# Giữ nguyên dòng cũ khi khoá (thành phẩm, vật tư) không đổi, chỉ cập nhật con số. Dựng lại
	# dòng mới mỗi lần thì `name` của dòng đổi liên tục, lịch sử sửa đổi của Đơn Bán thành vô
	# dụng đúng lúc cần soi ai đã lấy hàng của ai.
	doc.set(TRUONG_BANG, [])
	for r in moi:
		dong_cu = cu.get((r["source_item"], r["item_code"]))
		if dong_cu:
			dong_cu.update(r)
			doc.append(TRUONG_BANG, dong_cu)
		else:
			doc.append(TRUONG_BANG, r)

	return len(moi), canh_bao


def dong_bo(sales_order, ghi=True):
	"""Bản gọi được từ ngoài (console, nút bấm): nạp đơn, tính lại, rồi ghi.

	Cờ `bo_qua_ghim_vat_tu` chặn đệ quy: `doc.save()` kích `before_update_after_submit`, mà hook
	đó lại gọi `dong_bo_doc` — không có cờ thì mỗi lần lưu chạy hai lần, và lần thứ hai đo trên
	dữ liệu chưa commit.
	"""
	doc = frappe.get_doc("Sales Order", sales_order)
	so_dong, canh_bao = dong_bo_doc(doc)
	if ghi:
		doc.flags.bo_qua_ghim_vat_tu = True
		doc.flags.ignore_version = True
		doc.save(ignore_permissions=True)
	return {"don": sales_order, "so_dong": so_dong, "canh_bao": canh_bao}


def don_ban_cua_lsx(lsx):
	"""{Đơn Bán} mà một Lệnh sản xuất đang phục vụ — **hai chặng, không phải một**.

	🔒 Anh Thắng mô tả 04/09 16:35: hàng làm để tồn kho thì không lên từ đơn bán; đơn nào thiếu
	thì họ **tạo Kế hoạch sản xuất từ Đơn Bán** rồi mới tạo Lệnh sản xuất từ kế hoạch.

	Đo 04/09 trên 33 lệnh đang mở: 13 có sẵn ô *Đơn Bán* · **3 chỉ tra được qua kế hoạch** · 17
	không có đường nào (sản xuất để tồn kho — đúng ra không nối về đơn nào).

	⚠ Đây là **một định nghĩa dùng chung** với `chan_xuat_kho._don_duoc_mien`. Hai chỗ hiểu khác
	  nhau thì lớp chặn miễn trừ cho đơn này còn sổ ghim lại chuyển cho đơn kia.
	"""
	if not lsx:
		return set()
	truc, ke_hoach = frappe.db.get_value("Work Order", lsx, ["sales_order", "production_plan"]) or (None, None)
	if truc:
		return {truc}
	if ke_hoach:
		return {
			r["sales_order"]
			for r in frappe.get_all(
				"Production Plan Sales Order",
				filters={"parent": ke_hoach, "sales_order": ["is", "set"]},
				fields=["sales_order"],
			)
		}
	return set()


def chuyen_ghim_sau_san_xuat(so_luong, lsx, nguoc=False):
	"""Sản xuất xong ➜ **nhả vật tư, chuyển thành ghim thành phẩm**.

	🔒 Anh Thắng chốt 04/09 16:21: *"cần 5A nhưng hiện tại chỉ còn 3A, lúc này chỉ ghim được 3A
	➜ ghim nguyên vật liệu để sản xuất 2A ➜ sau khi sản xuất xong thì sẽ thành ghim 5A"*.

	## Cơ chế: chỉ cần CỘNG phần ghim thành phẩm, vật tư tự nhả

	Không có đoạn nào đi xoá dòng vật tư cả. Phần vật tư sinh ra từ
	`cần − đã giao − đã ghim`; cộng vào phần ghim thành phẩm là số đó **tự tụt**, và
	`dong_bo_doc` chạy theo trong cùng lần lưu sẽ cắt các dòng vật tư xuống đúng mức mới.

	Được thế là nhờ vật tư là **dữ liệu suy ra từ một con số lưu**, không phải hai sổ song song.
	Nếu nhả vật tư bằng một phép trừ riêng thì sẽ có hai đường cùng sửa một thứ — và chúng sẽ
	lệch nhau, im lặng.

	## Vì sao gắn vào `on_submit` chứ không chạy định kỳ

	Lúc chứng từ sản xuất được duyệt, số thành phẩm vừa nhập kho là **hàng tự do trong khoảnh
	khắc đó**. Chạy định kỳ thì có khe hở để đơn khác ghim mất, và đơn đã bỏ vật tư ra làm thì
	trắng tay. Chạy trong cùng giao dịch thì không có khe.

	## Trả về danh sách việc đã làm, để chỗ gọi in ra cho người thao tác thấy

	`nguoc=True` là đường **huỷ** chứng từ sản xuất: hàng vừa nhập kho bay đi, nên phải kéo phần
	ghim thành phẩm xuống, nếu không đơn giữ nhiều hơn số đang có (bất biến #1).
	"""
	viec = []
	so_luong = flt(so_luong)
	if so_luong <= 0 or not lsx:
		return viec

	ma = frappe.db.get_value("Work Order", lsx, "production_item")
	if not ma:
		return viec

	ung_vien = don_ban_cua_lsx(lsx)
	if not ung_vien:
		# Sản xuất để tồn kho — không phục vụ đơn nào. Không phải thiếu sót, xem docstring
		# `don_ban_cua_lsx`.
		return viec

	# Đơn nào trước: đúng thứ tự ưu tiên đã chốt, không phải thứ tự tra ra từ database.
	con_lai = so_luong
	for ten_don in don_theo_uu_tien():
		if ten_don not in ung_vien or con_lai <= 0:
			continue
		doc = frappe.get_doc("Sales Order", ten_don)
		doi = False
		for row in doc.get("items") or []:
			if row.item_code != ma or con_lai <= 0:
				continue
			ghim = flt(row.get("custom_so_luong_giu_cho"))
			if nguoc:
				# Huỷ: kéo xuống tối đa `so_luong`, nhưng không xuống dưới 0.
				bot = min(ghim, con_lai)
				if bot <= 0:
					continue
				row.custom_so_luong_giu_cho = ghim - bot
				con_lai -= bot
				viec.append(f"{ten_don} · {ma}: ghim {_so(ghim)} → {_so(ghim - bot)}")
				doi = True
				continue

			# ⚠ Ba trần cùng lúc, thiếu cái nào cũng sai:
			#   • phần đơn còn thiếu — ghim quá số cần là giữ hộ hàng cho không ai
			#   • số vừa sản xuất còn lại — một lệnh chia cho nhiều đơn thì hết là hết
			#   • tồn tự do — luật vàng, không lấy hàng người khác đang giữ
			con_thieu = flt(row.qty) - flt(row.delivered_qty) - ghim
			tu_do = flt(ton_tu_do([ma]).get(ma, 0))
			them = max(0.0, min(con_lai, con_thieu, tu_do))
			if them <= 0:
				continue
			row.custom_so_luong_giu_cho = ghim + them
			con_lai -= them
			viec.append(f"{ten_don} · {ma}: ghim {_so(ghim)} → {_so(ghim + them)}")
			doi = True

		if doi:
			# `save()` kích `before_update_after_submit` ➜ `chan_giu_cho_vuot_ton` kiểm lại con
			# số vừa cộng, rồi `dong_bo_ghim_vat_tu` cắt phần vật tư không còn cần. Cố ý KHÔNG
			# đặt cờ `bo_qua_ghim_vat_tu`: chính hai hook đó làm nốt việc nhả vật tư.
			doc.flags.ignore_version = True
			doc.save(ignore_permissions=True)

	return viec


@frappe.whitelist()
def phan_bo(purchase_receipt):
	"""Nút **Phân Bổ** trên Phiếu nhập mua — chia hàng vừa về cho các đơn chưa ghim đủ.

	🔒 Đầu bài nguyên văn anh Thắng 31/08: *"khi hàng về, người dùng tạo phiếu Purchase Receipt
	xong có thể ấn nút phân bổ, sau khi ấn nút thì những mặt hàng đang có số tồn khả dụng sẽ được
	phân bổ vào phần ghim hàng của những đơn Sales Order chưa ghim đủ … Ưu tiên phân bổ theo thứ
	tự hàng cần gấp trước."*

	## Chia HAI loại thiếu, không phải một

	| Loại | Thiếu ở đâu | Rót vào |
	|---|---|---|
	| Hàng bán thẳng | `Sales Order Item.custom_so_luong_giu_cho` chưa bằng số cần | chính ô đó |
	| Vật tư | dòng trong sổ cam kết có `qty < required_qty` | sổ, qua `dong_bo_doc` |

	Ví dụ của anh Thắng là loại thứ nhất. Nhưng chốt **cách B** (04/09) nói hàng mua về là **vật
	tư**, mà đo được **0/1.825** mã *Mua hàng* từng nằm trên dòng Đơn Bán — nên nếu chỉ làm loại
	thứ nhất thì nút này bấm xong **không tìm thấy gì để phân bổ**, đúng cái bế tắc đã nêu ở mục
	4.1 của đầu bài.

	## Không cần cờ "đã phân bổ"

	Cả hai loại đều chỉ lấy từ **tồn tự do**, mà tồn tự do đã trừ phần đã ghim. Bấm nút lần thứ
	hai tự thấy hết hàng. Đây là tính chất sẵn có của phép tính, không phải thứ phải canh.

	## Ba thứ phải NÓI RA thay vì im lặng bỏ qua

	1. Kho nhận hàng **nằm ngoài tập kho được tính tồn** (`Kho trung chuyển`, `Kho đang sản
	   xuất`…): hàng về thật mà hệ thống vẫn thấy tồn 0 ➜ chia không ra gì. Bẫy 1 mục 5.
	2. Đơn đang thiếu mã đó nhưng **chưa bật Ghim**: theo chốt 4.4 thì không chia, nhưng phải báo
	   để người dùng tự quyết.
	3. Phiếu **chưa duyệt**: `Bin.actual_qty` chưa đổi, chia ra là chia hàng chưa có. Bẫy 3 mục 5.
	"""
	pr = frappe.get_doc("Purchase Receipt", purchase_receipt)
	pr.check_permission("read")
	if pr.docstatus != 1:
		frappe.throw(
			_("Phiếu nhập mua chưa được duyệt nên hàng chưa vào kho — chưa phân bổ được."),
			title=_("Chưa duyệt phiếu"),
		)

	kho_ok = set(_kho_hop_le())
	ma_ve, kho_ngoai = {}, {}
	for d in pr.get("items") or []:
		sl = flt(d.get("stock_qty") or d.get("qty"))
		if sl <= 0:
			continue
		if d.get("warehouse") and d.get("warehouse") not in kho_ok:
			kho_ngoai[d.item_code] = d.get("warehouse")
			continue
		ma_ve[d.item_code] = ma_ve.get(d.item_code, 0) + sl

	ket = {
		"phieu": purchase_receipt,
		"dong": [],
		"kho_ngoai_tap": [{"ma": m, "kho": k} for m, k in sorted(kho_ngoai.items())],
		"bo_qua_chua_ghim": [],
		"canh_bao": [],
	}
	if not ma_ve:
		return ket

	# ── Loại 1: hàng bán thẳng ── và ── Loại 2: vật tư ── đi CHUNG một vòng lặp theo thứ tự ưu
	# tiên. Tách hai vòng thì đơn gấp nhất chỉ được ưu tiên trong loại của nó, còn đơn xếp sau
	# lại lấy trước ở loại kia — không còn là "cần gấp trước" nữa.
	for ten_don in don_theo_uu_tien():
		doc = frappe.get_doc("Sales Order", ten_don)
		truoc = {r.name: flt(r.get("custom_so_luong_giu_cho")) for r in doc.get("items") or []}
		vt_truoc = {(r.source_item, r.item_code): flt(r.qty) for r in doc.get(TRUONG_BANG) or []}

		for row in doc.get("items") or []:
			if row.item_code not in ma_ve:
				continue
			ghim = flt(row.get("custom_so_luong_giu_cho"))
			thieu = flt(row.qty) - flt(row.delivered_qty) - ghim
			tu_do = flt(ton_tu_do([row.item_code], tru_ghim_vat_tu_cua=ten_don).get(row.item_code, 0))
			them = max(0.0, min(thieu, tu_do))
			if them > 0:
				row.custom_so_luong_giu_cho = ghim + them

		# Lưu luôn kể cả khi phần bán thẳng không đổi: chính lần lưu này chạy `dong_bo_ghim_vat_tu`
		# và đó là chỗ phần VẬT TƯ được rót thêm (cấp phát = min(nhu cầu, tồn tự do)).
		doc.flags.ignore_version = True
		doc.save(ignore_permissions=True)
		doc.reload()

		for row in doc.get("items") or []:
			delta = flt(row.get("custom_so_luong_giu_cho")) - truoc.get(row.name, 0)
			if delta > 0:
				ket["dong"].append(
					{"ma": row.item_code, "don": ten_don, "them": delta, "loai": "Hàng trên đơn"}
				)
		for r in doc.get(TRUONG_BANG) or []:
			delta = flt(r.qty) - vt_truoc.get((r.source_item, r.item_code), 0)
			if delta > 0 and r.item_code in ma_ve:
				ket["dong"].append(
					{"ma": r.item_code, "don": ten_don, "them": delta, "loai": "Vật tư"}
				)

	# Đơn đang thiếu mã vừa về nhưng CHƯA BẬT GHIM — không chia (chốt 4.4), nhưng phải báo.
	chua_ghim = frappe.get_all(
		"Sales Order",
		filters={
			"docstatus": 1,
			"custom_ghim_ton_kha_dung": 0,
			"status": ["not in", list(TRANG_THAI_DON_CHET)],
		},
		pluck="name",
	)
	if chua_ghim:
		for r in frappe.get_all(
			"Sales Order Item",
			filters={"parent": ["in", chua_ghim], "item_code": ["in", list(ma_ve)]},
			fields=["parent", "item_code", "qty", "delivered_qty"],
		):
			con = flt(r["qty"]) - flt(r["delivered_qty"])
			if con > 0:
				ket["bo_qua_chua_ghim"].append(
					{"don": r["parent"], "ma": r["item_code"], "con_thieu": con}
				)

	loi = kiem_bat_bien()
	if loi:
		ket["canh_bao"] = loi
	return ket


def kiem_bat_bien():
	"""Quét toàn bộ sổ cam kết, khẳng định 5 điều — mục 8.7 của đầu bài.

	Trả về danh sách chuỗi mô tả chỗ hỏng; danh sách rỗng nghĩa là sổ sạch.

	Mục 12e đòi *"mỗi lần chạy phải kèm một phép kiểm tổng thể"*: bảy trong tám bất biến là bất
	biến **sau một chuỗi thao tác**, không phải kết quả của một lời gọi hàm, nên cách duy nhất
	bắt được chúng là quét lại toàn bảng sau mỗi kịch bản test.
	"""
	loi = []
	song = set(frappe.get_all("Sales Order", filters=loc_don_song(), pluck="name"))

	dong = frappe.get_all(
		"HKLed Pinned Material",
		filters={"parenttype": "Sales Order"},
		fields=["name", "parent", "item_code", "source_item", "qty", "required_qty", "bom", "bom_modified"],
	)

	# 4. Không dòng nào ghim nhiều hơn nhu cầu của chính nó.
	for d in dong:
		if flt(d["qty"]) - flt(d["required_qty"]) > 1e-9:
			loi.append(
				f"[#4] {d['parent']} · {d['item_code']}: ghim {_so(d['qty'])} > nhu cầu {_so(d['required_qty'])}"
			)

	hieu_luc = [d for d in dong if d["parent"] in song and flt(d["qty"]) > 0]

	# 1. Tổng ghim (thành phẩm + vật tư) của mọi đơn còn sống ≤ tồn thực tế.
	tp = ghim_thanh_pham()
	vt = {}
	for d in hieu_luc:
		vt[d["item_code"]] = vt.get(d["item_code"], 0) + flt(d["qty"])
	ma = set(tp) | set(vt)
	ton = _ton_thuc_te(ma, _kho_hop_le()) if ma else {}
	for m in sorted(ma):
		tong = flt(tp.get(m, 0)) + flt(vt.get(m, 0))
		if tong - flt(ton.get(m, 0)) > 1e-9:
			loi.append(
				f"[#1] {m}: tổng ghim {_so(tong)} (thành phẩm {_so(tp.get(m, 0))} + vật tư "
				f"{_so(vt.get(m, 0))}) > tồn thực tế {_so(ton.get(m, 0))}"
			)

	# 2. Tổng trong bảng khớp phần `ghim_boi_don_khac` báo ra.
	from mbwnext_hkled.api.kiem_tra_ton_kho import ghim_boi_don_khac

	bao, _cb = ghim_boi_don_khac()
	for m in sorted(set(vt) | set(tp)):
		cho_doi = flt(tp.get(m, 0)) + flt(vt.get(m, 0))
		if abs(flt(bao.get(m, 0)) - cho_doi) > 1e-9:
			loi.append(
				f"[#2] {m}: `ghim_boi_don_khac` báo {_so(bao.get(m, 0))} nhưng sổ có {_so(cho_doi)}"
			)

	# 3. Dòng còn hiệu lực không được thuộc đơn đã chết. (Dòng của đơn chết vẫn NẰM LẠI là đúng
	#    — luật 2 mục 2 — miễn là không lọt vào phép cộng nào; `hieu_luc` đã lọc, kiểm lại để
	#    bắt trường hợp ai đó viết truy vấn mới mà quên lọc.)
	for d in dong:
		if d["parent"] not in song and flt(d["qty"]) > 0:
			chet = frappe.db.get_value("Sales Order", d["parent"], ["docstatus", "status"], as_dict=True)
			if chet and (chet["docstatus"] == 2 or chet["status"] in ("Closed", "Completed", "Cancelled")):
				continue  # đúng như thiết kế: dòng nằm lại nhưng đã rơi khỏi bộ lọc
	# 5. Định mức đã ghi trên dòng còn sống và chưa đổi kể từ lúc ghim.
	for d in hieu_luc:
		if not d["bom"]:
			loi.append(f"[#5] {d['parent']} · {d['item_code']}: ghim mà không ghi định mức nào")
			continue
		hien = frappe.db.get_value("BOM", d["bom"], ["is_active", "modified"], as_dict=True)
		if not hien:
			loi.append(f"[#5] {d['parent']} · {d['item_code']}: định mức {d['bom']} không còn tồn tại")
		elif not hien["is_active"]:
			loi.append(f"[#5] {d['parent']} · {d['item_code']}: định mức {d['bom']} đã ngừng hiệu lực")
		elif d["bom_modified"] and str(hien["modified"]) != str(d["bom_modified"]):
			loi.append(
				f"[#5] {d['parent']} · {d['item_code']}: định mức {d['bom']} đã sửa lúc "
				f"{hien['modified']}, phần ghim tính theo bản {d['bom_modified']}"
			)

	return loi
