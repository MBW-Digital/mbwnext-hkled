# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Nạp danh mục đèn thành phẩm — 4 file Nhóm I–IV, 59.023 mã (PM-TASK-00126).

**Vì sao cần patch này.** `data/thanh_pham/` đã có từ PM-TASK-00067 nhưng khi đó chỉ chép
3 cột (mã sản phẩm, mã biến thể, phương pháp bổ sung) — đủ để *gắn nhãn* Phương pháp bổ
sung cho mặt hàng khách tự import bằng Data Import, KHÔNG đủ để *tạo* mặt hàng. Hệ quả:
site cài mới chạy `bench migrate` xong có 2.972 mã vật tư mà thiếu toàn bộ 59.023 đèn.

Nó không hỏng ồn ào. `import_bom_template` tra biến thể bằng
`frappe.get_all("Item", filters={"variant_of": ...})`; không có biến thể nào thì sheet
`DP01S`/`DP03S` ra 0 rule, patch in cảnh báo rồi migrate vẫn báo thành công. Cổng thật sẽ
đứng ở trạng thái "cài xong" mà không có đèn nào và không có BOM nào.

Nay 4 file giữ đủ cột nên bộ nạp dựng lại được từ số 0. Đã đo: 20 MB thô, 0,64 MB sau nén.

⚠ Phải chạy **trước** `import_bom_template` trong `patches.txt` — xem lý do ở trên.

⚠ Cùng cái giá đã ghi ở patch danh mục vật tư: khách **xoá một mã trên giao diện thì lần
`bench migrate` sau nó sống lại**. Muốn bỏ hẳn phải xoá dòng trong `data/thanh_pham/*.csv`.
"""

import frappe

from mbwnext_hkled.data.nhap_item import cap_nhat_phuong_phap, nhap_tat_ca


def execute():
	bao_cao = nhap_tat_ca(ten_thu_muc="thanh_pham")

	cha = bien_the = don_le = lap = 0
	nhom = []
	bo_trung = bo_thieu = bo_dung = 0
	for b in bao_cao:
		cha += b["cha_moi"]
		bien_the += b["bien_the_moi"]
		don_le += b["hang_don_le"]
		lap += b["lap_y_het"]
		nhom.extend(b["nhom_moi"])
		bo_trung += len(b["bo_qua"]["trung_ma_khac_noi_dung"])
		bo_thieu += b["bo_qua"]["thieu_ma"]
		bo_dung += len(b["bo_qua"]["dung_to_hop_dac_tinh"])

	frappe.db.commit()

	# Gọi lại cho chắc: `add_item_replenishment_method` đã chạy trên site cũ khi 59.023 đèn
	# chưa có mã nào, nên nó đếm hết vào "không có trên site" rồi bỏ qua. Trên site cài mới
	# thứ tự đã đúng, đây là no-op.
	pp = cap_nhat_phuong_phap()
	frappe.db.commit()

	print(
		f"[mbwnext_hkled] Đèn thành phẩm: {cha} mặt hàng cha, {bien_the} biến thể, "
		f"{don_le} hàng không biến thể, {len(nhom)} nhóm mới."
	)
	print(
		f"[mbwnext_hkled] Phương pháp bổ sung: điền {pp['da_dat']}, giữ nguyên {pp['khong_doi']}, "
		f"xoá ở {pp['da_xoa_o_cha']} mặt hàng cha."
	)
	if bo_trung or bo_thieu or bo_dung:
		print(
			f"[mbwnext_hkled] BỎ QUA (cần HKLED sửa bảng nguồn): {bo_trung} mã trùng khác nội "
			f"dung, {bo_dung} mã đụng tổ hợp đặc tính, {bo_thieu} dòng thiếu mã."
		)
