# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Nạp BOM Template theo file khách gửi (PM-TASK-00110).

Đặc tả ở `data/bom_template/spec.json`, sinh từ file Excel bằng `data/doc_bom_sheet.py`.
Phần dựng bản ghi ở `data/nhap_bom_template.py`.

⚠ Patch **không ghi** sheet nào còn cặp (biến thể × thành phần) không tra được NVL: engine
`find_rule_item` throw khi không rule nào khớp, nên ghi vào là BOM hỏng hàng loạt lúc chạy
thật chứ không phải cảnh báo nhẹ. Sheet hỏng được in ra để xử lý dữ liệu rồi chạy lại.

Chạy lại được nhiều lần: template nhận diện theo `item_template`, mỗi lần chạy ghi đè
toàn bộ bảng thành phần và bảng rule của template đó (chốt của Thắng 18/08: ghi đè bản cũ).
"""

import frappe

from mbwnext_hkled.data.nhap_bom_template import nhap_tat_ca


def execute():
	bao = nhap_tat_ca()

	for ten, loi in (bao.get("bo_qua_sheet") or {}).items():
		print(f"[mbwnext_hkled] ⚠ BỎ QUA sheet {ten}: {loi}")

	for s in bao["sheets"]:
		if s.get("loi"):
			print(f"[mbwnext_hkled] ⚠ {s['sheet']}: {s['loi']}")
			continue
		if not s.get("da_ghi"):
			print(
				f"[mbwnext_hkled] ⚠ KHÔNG ghi {s['sheet']}: {s['so_cap_hong']} cặp"
				f" (biến thể × thành phần) không tra được NVL"
			)
			continue
		print(
			f"[mbwnext_hkled] {s['ten']}: {s['so_rule']} rule cho {s['so_bien_the']} biến thể"
			f"; thêm {len(s.get('component_moi') or [])} Thành Phần BOM"
		)
		if s.get("so_cap_co_y"):
			print(
				f"    {s['so_cap_co_y']} cặp cố ý không có rule (khách ghi \"Không sử dụng\")"
			)
		if s.get("so_cap_chua_co_du_lieu"):
			print(
				f"    ⚠ {s['so_cap_chua_co_du_lieu']} cặp khách chưa khai NVL"
				f" — xem CHUA_CO_DU_LIEU trong data/nhap_bom_template.py"
			)
		for g in s.get("sl_thieu") or []:
			chi_tiet = f" ({g['ghi_trong_sheet']!r})" if g["ly_do"] != "chưa khai số lượng" else ""
			print(f"    ⚠ {g['tp']}: {g['ly_do']}{chi_tiet} — đang tạm để 1, xem PM-TASK-00110")

	frappe.db.commit()
