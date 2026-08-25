# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Nạp danh mục vật tư đợt 2 — 16 file (PM-TASK-00126).

Vì sao phải có patch RIÊNG thay vì sửa `import_danh_muc_vat_tu`:

Patch của Frappe **chỉ chạy một lần** — chạy xong là ghi vào bảng `Patch Log`, lần
`bench migrate` sau thấy có rồi thì bỏ qua. Patch đợt 1 đọc cả thư mục `data/danh_muc/`
nên về lý thuyết nó cuốn luôn 16 file mới, NHƯNG chỉ đúng với site **chưa từng chạy nó**.
Site nào đã chạy đợt 1 rồi thì thêm bao nhiêu file cũng vô ích: patch không chạy lại,
`bench migrate` vẫn báo thành công, và 910 mã **không bao giờ lên** — hỏng im lặng.

Patch mới thì mọi site đều chạy, không phụ thuộc `Patch Log` cũ. Gọi lại đúng
`nhap_tat_ca()`: bộ nạp idempotent kiểu "có rồi thì bỏ qua" nên 12 file đợt 1 chạy lại
vô hại, chỉ 16 file mới sinh bản ghi.

⚠ Cùng cái giá đã ghi ở patch đợt 1: khách **xoá một mã trên giao diện thì lần
`bench migrate` sau nó sống lại**. Muốn bỏ hẳn phải xoá dòng trong `data/danh_muc/*.csv`.
"""

import frappe

from mbwnext_hkled.data.nhap_item import (
	cap_nhat_phuong_phap,
	gia_tri_so_tran,
	nhap_tat_ca,
)


def _sua_cong_suat_con_don_vi():
	"""Đưa `Công suất` về số trần cho bản ghi đã lỡ tạo bằng bản code cũ.

	Site nào nạp 16 file đợt 2 TRƯỚC khi có `gia_tri_so_tran()` thì đang giữ `200W` trong
	khi phần còn lại của site giữ `200` — lọc báo cáo theo công suất sẽ sót một nửa mà
	không báo gì. Trên site nạp đúng ngay từ đầu thì đây là no-op.

	Chỉ đổi khi giá trị số trần tương ứng **đã có sẵn** trong danh mục đặc tính; không tự
	tạo giá trị mới, không đoán.
	"""
	rows = frappe.db.sql(
		"""select name, attribute_value from `tabItem Variant Attribute`
		   where attribute = 'Công suất' and attribute_value like '%%W'""",
		as_dict=True,
	)
	da_sua = 0
	for r in rows:
		moi = gia_tri_so_tran("Công suất", r["attribute_value"])
		if moi == r["attribute_value"]:
			continue
		if not frappe.db.exists(
			"Item Attribute Value", {"parent": "Công suất", "attribute_value": moi}
		):
			continue
		frappe.db.set_value(
			"Item Variant Attribute", r["name"], "attribute_value", moi, update_modified=False
		)
		da_sua += 1
	return da_sua


def execute():
	# Nạp cả thư mục, không lọc: bộ nạp bỏ qua mã đã có nên 12 file đợt 1 chạy lại vô hại.
	#
	# ⚠ Bản đầu của patch này CÓ lọc, vì chạy thử vỡ ngay ở `ItemVariantExistsError` — bản
	# CSV đợt 1 trong repo khi đó còn 56 mã module ghi B5 mà Loại LED là Bridgelux 3030,
	# đụng tổ hợp đặc tính với 56 mã B3 trên site. Đã thay `04-m-module.csv` bằng bản khách
	# sửa ngày 24/08 nên hết đụng; giữ lọc nữa chỉ che mất lỗi thật nếu sau này lại lệch.
	bao_cao = nhap_tat_ca()

	cha = bien_the = don_le = lap = 0
	nhom = []
	bo_trung = bo_lech = bo_thieu = bo_dung = 0
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

	frappe.db.commit()

	sua_cs = _sua_cong_suat_con_don_vi()
	pp = cap_nhat_phuong_phap()
	frappe.db.commit()

	print(
		f"[mbwnext_hkled] Danh mục vật tư đợt 2: {cha} mặt hàng cha, {bien_the} biến thể, "
		f"{don_le} hàng không biến thể, {len(nhom)} nhóm mới."
	)
	print(
		f"[mbwnext_hkled] Phương pháp bổ sung: điền {pp['da_dat']}, giữ nguyên {pp['khong_doi']}, "
		f"xoá ở {pp['da_xoa_o_cha']} mặt hàng cha."
	)
	if sua_cs:
		print(f"[mbwnext_hkled] Đưa Công suất về số trần: {sua_cs} bản ghi.")
	if bo_trung or bo_lech or bo_thieu or bo_dung:
		print(
			f"[mbwnext_hkled] BỎ QUA (cần HKLED sửa bảng nguồn): {bo_trung} mã trùng khác nội dung, "
			f"{bo_lech} mặt hàng cha lệch bộ đặc tính, {bo_dung} mã đụng tổ hợp đặc tính, "
			f"{bo_thieu} dòng thiếu mã."
		)
