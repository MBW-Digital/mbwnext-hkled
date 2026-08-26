# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Trỏ lại `variant_of` cho biến thể đang treo nhầm mặt hàng cha.

VÌ SAO CẦN PATCH RIÊNG, BỘ NẠP KHÔNG TỰ CHỮA ĐƯỢC

`nhap_item._tao_item()` thoát ngay ở dòng đầu khi mã đã tồn tại — nó **không bao giờ
sờ tới `variant_of`**. Chủ ý là vậy: bộ nạp không được phép giẫm lên thứ khách đã sửa
tay. Hệ quả là khi file khai `XOP-DDG-380x160x60mm` thuộc cha `XOP-DDG` mà trên site
nó đang thuộc `XOP-GOC`, `bench migrate` sẽ tạo cha `XOP-DDG` rồi **bỏ qua cả 4 biến
thể** — để lại một mặt hàng cha RỖNG, còn 4 biến thể vẫn nằm sai chỗ.

Đó là kiểu hỏng tệ nhất: nhìn vào tưởng đã sửa xong.

PHẠM VI ĐÃ ĐO, KHÔNG PHẢI ƯỚC LƯỢNG

Soi toàn bộ 2.296 cặp cha–biến thể khai trong `data/danh_muc/` + `data/thanh_pham/`
đối chiếu với site (26/08/2026): `hkled.com` lệch đúng 4 mã (cả 4 là XOP-DDG),
`test.com` lệch 0. Site dựng từ trắng luôn đúng ngay từ đầu — patch này chỉ để gỡ vết
cũ trên site đã chạy, và là no-op ở mọi nơi khác.

BỐN RÀO, THIẾU MỘT LÀ BỎ QUA CHỨ KHÔNG SỬA

1) Cha khai trong file phải TỒN TẠI và `has_variants=1`.
2) Cha đó phải khai đủ những đặc tính mà biến thể đang mang — trỏ sang cha thiếu đặc
   tính là đẻ ra biến thể không mở được form.
3) Biến thể phải KHÔNG có tham chiếu nào: tồn kho, bút toán, BOM Rule, bảng thành
   phần, đơn bán, đơn mua, bảng giá. Còn dấu vết nghiệp vụ thì đổi cha là đổi nghĩa
   của số liệu cũ — việc đó phải người quyết, không phải patch.
4) Cha cũ và cha mới phải khác nhau (khỏi ghi thừa).

Dùng `db.set_value` chứ không `doc.save`: `variant_of` là trường chỉ-đặt-một-lần,
`save` sẽ bị validate chặn. Đây là sửa dữ liệu có chủ đích, đã rào ở trên.
"""

import frappe


# Liệt kê tường minh chứ không dò động từ `DocField`: danh sách này là thứ người sau
# phải đọc được và cãi lại được. Dò động thì đúng hơn về lý thuyết nhưng biến rào an
# toàn thành hộp đen, và mỗi phiên bản Frappe lại cho ra một tập khác nhau.
#
# ⚠ Bổ sung `BOM Item` và 6 bảng chứng từ sau khi phiên cozy-dev-a2 soi phía BOM và
# chỉ ra rằng bản đầu thiếu chúng. Với 4 mã XOP thì cả 7 bảng cũ lẫn 7 bảng mới đều
# ra 0 nên kết quả không đổi — nhưng patch chạy trên mọi site, và một biến thể đang
# nằm trong BOM chuẩn ERPNext thì tuyệt đối không được đổi cha.
BANG_THAM_CHIEU = (
	("Stock Ledger Entry", "item_code"),
	("Bin", "item_code"),
	("BOM Rule", "item"),
	("BOM Component Table", "item"),
	("BOM Item", "item_code"),
	("BOM", "item"),
	("Work Order Item", "item_code"),
	("Stock Entry Detail", "item_code"),
	("Delivery Note Item", "item_code"),
	("Purchase Receipt Item", "item_code"),
	("Sales Invoice Item", "item_code"),
	("Purchase Invoice Item", "item_code"),
	("Sales Order Item", "item_code"),
	("Purchase Order Item", "item_code"),
	("Item Price", "item_code"),
)


def _cap_cha_bien_the():
	"""{mã biến thể: mã cha} theo file nguồn. Bỏ mã khai ở hai cha khác nhau."""
	import os

	from mbwnext_hkled.data.nhap_item import (
		THU_MUC_NGUON,
		_doc_csv,
		_khoa_bien_the,
		thu_muc_du_lieu,
	)

	theo_ma = {}
	for ten_thu_muc in THU_MUC_NGUON:
		thu_muc = thu_muc_du_lieu(ten_thu_muc)
		if not os.path.isdir(thu_muc):
			continue
		for f in sorted(os.listdir(thu_muc)):
			if not f.endswith(".csv"):
				continue
			dong = _doc_csv(os.path.join(thu_muc, f))
			if not dong:
				continue
			kbt = _khoa_bien_the(dong)
			for r in dong:
				bt = (r.get(kbt) or "").strip()
				cha = (r.get("Mã sản phẩm") or "").strip()
				if bt and cha:
					theo_ma.setdefault(bt, set()).add(cha)
	return {bt: next(iter(c)) for bt, c in theo_ma.items() if len(c) == 1}


def _dac_tinh_cua(ma):
	return {
		r.attribute
		for r in frappe.get_all(
			"Item Variant Attribute", filters={"parent": ma}, fields=["attribute"]
		)
	}


def _con_tham_chieu(ma):
	"""Đếm dấu vết nghiệp vụ. Bảng chưa có trên site thì bỏ qua, không để vỡ migrate.

	Site không cài đủ app (hoặc bản Frappe khác) có thể thiếu một vài bảng trong danh
	sách. Đếm thẳng vào bảng không tồn tại là `OperationalError` giữa chừng migrate —
	đúng kiểu hỏng đắt nhất, vì nó dừng cả loạt patch phía sau.
	"""
	dau_vet = {}
	for dt, truong in BANG_THAM_CHIEU:
		if not frappe.db.table_exists(dt):
			continue
		n = frappe.db.count(dt, {truong: ma})
		if n:
			dau_vet[dt] = n
	return dau_vet


def execute():
	da_sua, bo_qua = [], []

	for bt, cha_file in _cap_cha_bien_the().items():
		cha_site = frappe.db.get_value("Item", bt, "variant_of")
		if cha_site is None or cha_site == cha_file:
			continue  # mã chưa có trên site, hoặc đã đúng cha

		if not frappe.db.exists("Item", cha_file):
			bo_qua.append((bt, f"cha {cha_file} chưa tồn tại"))
			continue
		if not frappe.db.get_value("Item", cha_file, "has_variants"):
			bo_qua.append((bt, f"cha {cha_file} không phải mặt hàng cha"))
			continue

		thieu = _dac_tinh_cua(bt) - _dac_tinh_cua(cha_file)
		if thieu:
			bo_qua.append((bt, f"cha {cha_file} thiếu đặc tính {', '.join(sorted(thieu))}"))
			continue

		dau_vet = _con_tham_chieu(bt)
		if dau_vet:
			bo_qua.append(
				(bt, "còn " + ", ".join(f"{n} {dt}" for dt, n in dau_vet.items()))
			)
			continue

		frappe.db.set_value("Item", bt, "variant_of", cha_file, update_modified=False)
		da_sua.append((bt, cha_site, cha_file))

	if da_sua:
		frappe.db.commit()
		print(f"[mbwnext_hkled] Trỏ lại mặt hàng cha cho {len(da_sua)} biến thể:")
		for bt, cu, moi in da_sua:
			print(f"    {bt}: {cu} -> {moi}")
	if bo_qua:
		print(f"[mbwnext_hkled] BỎ QUA {len(bo_qua)} biến thể lệch cha (cần người xử lý):")
		for bt, ly_do in bo_qua:
			print(f"    {bt}: {ly_do}")
