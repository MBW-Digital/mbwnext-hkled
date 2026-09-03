# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Đặt đơn vị tính mặc định theo nhóm hàng — PM-TASK-00141 (Thắng, 31/08).

VÌ SAO LÀ PATCH CHỨ KHÔNG PHẢI SỬA TAY TRÊN GIAO DIỆN

Bộ nạp danh mục lấy đơn vị từ cột *Đơn vị tính* của file khách, không có thì rơi về
`nhap_item.DON_VI = "Cái"`. Bốn file `data/thanh_pham/*.csv` **không có cột đó** — nên
59.030 đèn thành phẩm luôn ra `Cái` trên site dựng mới, bất kể ai sửa tay trên
`hkled.com`. Sửa tay là mất trắng lúc dựng cổng thật.

⚠ Patch này phải nằm **sau** mọi patch nạp danh mục trong `patches.txt`, nếu không nó
chạy trước khi có mặt hàng và im lặng không đổi gì.

CÁCH GHI: SQL THẲNG, KHÔNG QUA `doc.save()`

59.392 lượt `save()` chạy đủ `Item.validate` + `on_update` mất hàng chục phút và không
mua thêm được gì: các mặt hàng này chưa có một giao dịch kho nào. Đổi lại, hai ràng buộc
mà `save()` vốn giữ hộ thì patch phải **tự kiểm trước khi ghi**:

1. `check_stock_uom_with_bin` — cấm đổi khi đã có `Stock Ledger Entry` UOM khác.
2. `validate_uom` — biến thể **bắt buộc** cùng đơn vị với mặt hàng cha (`frappe.throw`).
   Vì thế `TSE-TSL` (mặt hàng cha, tên *"Tấm pin NLMT"*) cũng phải sang `Tấm` dù danh
   sách của Thắng chỉ liệt kê 7 biến thể — để cha `Cái` mà con `Tấm` là sau này ai mở
   một biến thể lên bấm Lưu sẽ bị chặn.

Cả hai gate đều **bỏ qua và in ra**, không `throw`: mặt hàng thử nghiệm của đội test có
tồn kho thật nằm lẫn trong nhóm đèn, throw là chặn cả 59 nghìn dòng còn lại.
"""

import frappe

# Nhóm sản phẩm -> đơn vị tính. Nhóm đèn thành phẩm khớp theo tiền tố "Đèn LED".
NHOM = {
	"(V) Vỏ đèn": "Bộ",
	"(SLP) Nhóm linh phụ kiện trụ/cột, cần đèn": "Bộ",
	"(W) Dây điện": "cm",
	"LED": "Hạt",
}
TIEN_TO_NHOM_DEN = "Đèn LED"
DON_VI_THANH_PHAM = "Bộ"

# Mã cụ thể Thắng liệt kê trong task.
MA = {}
MA.update({m: "Viên" for m in ("TSE-PIN-LFP32700-6Ah-3.2V", "TSE-PIN-LFP32700-5.5Ah-3.2V")})
MA.update({m: "Cái" for m in (
	"TSE-BDK-SR-SN40-W", "TSE-BDK-SR-DM80-W", "TSE-BDK-SR-MEH160-W",
	"TSE-BDK-SR-MEH200-W", "TSE-BDK-18/3.2V", "TSE-BDK-26/3.2V",
)})
# "TSE-TSL" là mặt hàng cha, thêm vào vì ràng buộc cha/biến thể — xem docstring.
MA.update({m: "Tấm" for m in (
	"TSE-TSL",
	"TSE-TSL-100W/18V-900x670x30", "TSE-TSL-100W/18V-940x670x30",
	"TSE-TSL-150W/18V-1210x670x30", "TSE-TSL-150W/18V-1300x670x30",
	"TSE-TSL-200W/18V-1480x670x30", "TSE-TSL-200W/18V-1580x670x30",
	"TSE-TSL-50W/6V-450x670x30",
)})
CHA_BO = "TSE-PSL"  # cả mặt hàng cha lẫn mọi biến thể -> Bộ

# UOM phải có sẵn thì mới gán được. Site chỉ có Bộ/Cái/Viên/cm.
UOM_CAN_TAO = {"Hạt": 1, "Tấm": 1}  # tên -> must_be_whole_number

# Chỉ đè lên mặt hàng đang mang đúng giá trị DỰ PHÒNG của bộ nạp.
#
# Luật của Thắng là luật theo NHÓM, còn cột *Đơn vị tính* trong file khách là dữ liệu theo
# TỪNG DÒNG — hai nguồn khác cấp. Hôm nay không đụng nhau (62.000/62.055 mặt hàng đang là
# `Cái`, và cả 59.393 mã trong phạm vi đều vậy), nhưng file khách đợt sau mà có cột đó thì
# bộ nạp ghi theo file rồi patch này đè lại theo nhóm — **patch thắng, im lặng**. Rào ở đây
# cho file khách thắng, vì dữ liệu từng dòng cụ thể hơn luật nhóm.
DU_PHONG = "Cái"  # = nhap_item.DON_VI


def _tao_uom_con_thieu(bao_cao):
	for ten, nguyen in UOM_CAN_TAO.items():
		if frappe.db.exists("UOM", ten):
			continue
		frappe.get_doc({
			"doctype": "UOM", "uom_name": ten, "enabled": 1, "must_be_whole_number": nguyen
		}).insert(ignore_permissions=True)
		bao_cao.append(f"  + tạo UOM {ten!r}")


def muc_tieu():
	"""Trả về {mã mặt hàng: đơn vị tính đích} cho toàn bộ phạm vi của task."""
	dich = {}

	nhom_den = [
		g.name for g in frappe.get_all(
			"Item Group", filters={"name": ["like", TIEN_TO_NHOM_DEN + "%"]}, fields=["name"]
		)
	]
	for nhom in nhom_den:
		for it in frappe.get_all("Item", filters={"item_group": nhom}, pluck="name"):
			dich[it] = DON_VI_THANH_PHAM

	for nhom, dv in NHOM.items():
		for it in frappe.get_all("Item", filters={"item_group": nhom}, pluck="name"):
			dich[it] = dv

	for it in frappe.get_all("Item", filters={"variant_of": CHA_BO}, pluck="name"):
		dich[it] = "Bộ"
	if frappe.db.exists("Item", CHA_BO):
		dich[CHA_BO] = "Bộ"

	# Mã liệt kê tường minh thắng mọi luật theo nhóm.
	for ma, dv in MA.items():
		if frappe.db.exists("Item", ma):
			dich[ma] = dv

	return dich


def _bi_chan_boi_giao_dich(ma, dv):
	"""Giống `erpnext...item.check_stock_uom_with_bin`, nhưng chỉ hỏi chứ không throw."""
	ref = frappe.db.get_value("Stock Ledger Entry", {"item_code": ma}, "stock_uom")
	if ref and ref != dv:
		return f"đã có phát sinh kho với đơn vị {ref!r}"
	if frappe.db.sql(
		"""select 1 from tabBin where item_code=%s and stock_uom!=%s
		   and (reserved_qty>0 or ordered_qty>0 or indented_qty>0 or planned_qty>0) limit 1""",
		(ma, dv),
	):
		return "đang có số lượng giữ chỗ/đặt hàng ở đơn vị cũ"
	return None


def _ghi_theo_lo(ten_ds, dv):
	"""Ghi thẳng vào bảng, chia lô để câu SQL không phình quá dài."""
	for i in range(0, len(ten_ds), 2000):
		lo = ten_ds[i : i + 2000]
		frappe.db.sql(
			"""update tabItem set stock_uom=%s, modified=now(), modified_by=%s
			   where name in %s""",
			(dv, frappe.session.user, tuple(lo)),
		)
		# Bảng quy đổi đơn vị: dòng hệ số 1 chính là đơn vị lưu kho.
		frappe.db.sql(
			"""delete from `tabUOM Conversion Detail`
			   where parenttype='Item' and parent in %s and uom=%s and conversion_factor=1""",
			(tuple(lo), dv),
		)
		frappe.db.sql(
			"""update `tabUOM Conversion Detail` set uom=%s
			   where parenttype='Item' and parent in %s and conversion_factor=1""",
			(dv, tuple(lo)),
		)
		frappe.db.sql("""update tabBin set stock_uom=%s where item_code in %s""", (dv, tuple(lo)))


def execute(chi_xem=False):
	bao_cao = []
	if not chi_xem:
		_tao_uom_con_thieu(bao_cao)

	dich = muc_tieu()
	hien = {
		r.name: r for r in frappe.get_all(
			"Item", filters={"name": ["in", list(dich)]},
			fields=["name", "stock_uom", "variant_of"],
		)
	}

	can_doi, bo_qua = {}, []
	for ma, dv in dich.items():
		r = hien.get(ma)
		if not r or r.stock_uom == dv:
			continue
		if r.stock_uom != DU_PHONG:
			bo_qua.append((ma, r.stock_uom, dv, "đơn vị lấy từ file khách, không phải giá trị dự phòng"))
			continue
		ly_do = _bi_chan_boi_giao_dich(ma, dv)
		if ly_do:
			bo_qua.append((ma, r.stock_uom, dv, ly_do))
			continue
		can_doi[ma] = dv

	# Gate cha/biến thể: trạng thái CUỐI phải nhất quán, kể cả với mã không đổi.
	sau = {ma: can_doi.get(ma, r.stock_uom) for ma, r in hien.items()}
	lech = []
	for ma, r in hien.items():
		cha = r.variant_of
		if not cha or ma not in can_doi:
			continue
		uom_cha = sau.get(cha) or frappe.db.get_value("Item", cha, "stock_uom")
		if uom_cha != sau[ma]:
			lech.append((ma, sau[ma], cha, uom_cha))
	for ma, dv, cha, uom_cha in lech:
		can_doi.pop(ma, None)
		bo_qua.append((ma, hien[ma].stock_uom, dv, f"cha {cha!r} sẽ là {uom_cha!r} — ERPNext cấm lệch"))

	theo_dv = {}
	for ma, dv in can_doi.items():
		theo_dv.setdefault(dv, []).append(ma)

	bao_cao.append(f"Phạm vi {len(dich)} mặt hàng · cần đổi {len(can_doi)} · bỏ qua {len(bo_qua)}")
	for dv, ds in sorted(theo_dv.items()):
		bao_cao.append(f"  → {dv:5} {len(ds):>6} mặt hàng")
	for ma, cu, moi, ly_do in bo_qua:
		bao_cao.append(f"  ⚠ bỏ qua {ma!r}: {cu} → {moi} · {ly_do}")

	if not chi_xem:
		for dv, ds in theo_dv.items():
			_ghi_theo_lo(ds, dv)
		frappe.db.commit()
		frappe.clear_cache()

	# Bất biến của cả site, kiểm SAU khi ghi. Phá nó thì triệu chứng nổ ở chỗ khác hẳn:
	# người dùng mở một biến thể bất kỳ bấm Lưu là bị `validate_uom` chặn, không ai đoán
	# ra là tại patch đơn vị tính. Trước khi chạy patch này số đó đang là 0.
	lech_site = frappe.db.sql(
		"""select c.name, c.stock_uom, p.name, p.stock_uom
		   from tabItem c join tabItem p on p.name=c.variant_of
		   where c.stock_uom != p.stock_uom limit 20"""
	)
	tong_lech = frappe.db.sql(
		"""select count(*) from tabItem c join tabItem p on p.name=c.variant_of
		   where c.stock_uom != p.stock_uom"""
	)[0][0]
	if tong_lech:
		bao_cao.append(f"  🔴 {tong_lech} cặp cha–biến thể LỆCH đơn vị — phải sửa, xem 20 cặp đầu:")
		bao_cao += [f"      {c!r} {cu} ≠ cha {ch!r} {uc}" for c, cu, ch, uc in lech_site]
	else:
		bao_cao.append("  ✅ 0 cặp cha–biến thể lệch đơn vị trên toàn site")

	print("\n".join(bao_cao))
	return {"can_doi": len(can_doi), "bo_qua": len(bo_qua), "theo_dv": {k: len(v) for k, v in theo_dv.items()}}
