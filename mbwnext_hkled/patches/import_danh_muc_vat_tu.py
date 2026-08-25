# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Nạp toàn bộ danh mục vật tư HKLED — 11 sheet (PM-TASK-00061).

Thay cho patch `import_oc_vit_bulong` (chỉ nạp 1 sheet). Toàn bộ phần xử lý nằm ở
`mbwnext_hkled/data/nhap_item.py` — đọc docstring ở đó trước khi sửa, nhất là mục
*"THÀ BỎ QUA CÒN HƠN ĐOÁN"*.

⚠ Idempotent theo kiểu "có rồi thì bỏ qua": khách **xoá một mã trên giao diện thì lần
`bench migrate` sau nó sống lại**. Muốn bỏ hẳn phải xoá dòng trong `data/danh_muc/*.csv`.
"""

import frappe

from mbwnext_hkled.data.nhap_item import nhap_tat_ca


def execute():
	bao_cao = nhap_tat_ca()

	cha = bien_the = don_le = lap = 0
	nhom = []
	bo_trung = bo_lech = bo_thieu = bo_dung = 0
	bo_nhom = []
	for b in bao_cao:
		cha += b["cha_moi"]
		bien_the += b["bien_the_moi"]
		don_le += b["hang_don_le"]
		lap += b["lap_y_het"]
		nhom.extend(b["nhom_moi"])
		bo_trung += len(b["bo_qua"]["trung_ma_khac_noi_dung"])
		bo_lech += len(b["bo_qua"]["cha_lech_dac_tinh"])
		bo_thieu += b["bo_qua"]["thieu_ma"]
		bo_dung += len(b["bo_qua"]["dung_to_hop_dac_tinh"])
		bo_nhom.extend(b["bo_qua"]["thieu_nhom"])

	frappe.db.commit()
	print(
		f"[mbwnext_hkled] Danh mục vật tư: {cha} mặt hàng cha, {bien_the} biến thể, "
		f"{don_le} hàng đơn lẻ, {len(nhom)} nhóm mới."
	)
	if bo_nhom:
		print(
			f"[mbwnext_hkled] BỎ QUA vì THIẾU NHÓM SẢN PHẨM ({len(bo_nhom)} mã cha, kèm mọi biến thể "
			f"của chúng): {', '.join(sorted(set(bo_nhom)))}"
		)
	if bo_trung or bo_lech or bo_thieu or bo_dung:
		print(
			f"[mbwnext_hkled] BỎ QUA (cần HKLED sửa bảng nguồn): {bo_trung} mã trùng khác nội dung, "
			f"{bo_lech} mặt hàng cha lệch bộ đặc tính, {bo_dung} mã đụng tổ hợp đặc tính, "
			f"{bo_thieu} dòng thiếu mã."
		)
