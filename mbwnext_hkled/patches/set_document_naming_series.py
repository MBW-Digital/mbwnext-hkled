# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Đổi cấu trúc mã chứng từ theo bảng HKLED gửi (PM-TASK-00054).

Bảng gốc: Google Sheet đính trong PM-TASK-00054, 9 loại chứng từ, dạng `XX-YY-#####`
(mã viết tắt tiếng Việt + 2 chữ số năm + số thứ tự 5 chữ số).

    Đơn hàng bán            SAL-ORD-.YYYY.-  ->  SO-.YY.-
    Kế hoạch sản xuất       MFG-PP-.YYYY.-   ->  KSX-.YY.-
    Lệnh sản xuất           MFG-WO-.YYYY.-   ->  LSX-.YY.-
    Chứng từ kho nội bộ     MAT-STE-.YYYY.-  ->  KNB-.YY.-
    Phiếu xuất kho hàng bán MAT-DN-.YYYY.-   ->  PXK-.YY.-
    Phiếu nhập kho hàng mua MAT-PRE-.YYYY.-  ->  PNK-.YY.-
    Yêu cầu mặt hàng        MAT-MR-.YYYY.-   ->  YCM-.YY.-
    Đơn mua hàng            PUR-ORD-.YYYY.-  ->  PO-.YY.-
    Báo giá                 SAL-QTN-.YYYY.-  ->  BG-.YY.-

## Những điều PHẢI biết trước khi sửa file này

**Chứng từ cũ giữ nguyên mã.** Đổi series chỉ ảnh hưởng chứng từ tạo MỚI. Trên site sẽ tồn tại
song song `SAL-ORD-2026-00019` và `SO-26-00001`. Đây là hành vi đúng — đổi tên chứng từ cũ sẽ
làm lệch mọi bản in đã phát hành và mọi tham chiếu bên ngoài hệ thống.

**Số thứ tự bắt đầu lại từ 00001** cho mỗi tiền tố mới, vì bộ đếm trong bảng `tabSeries` gắn theo
tiền tố. Không có cách nào "nối tiếp" số cũ mà không tự đặt lại bộ đếm bằng tay.

**Chỉ đổi 9 loại có trong bảng.** `Delivery Note` và `Purchase Receipt` còn một series hàng trả lại
(`MAT-DN-RET-`, `MAT-PR-RET-`) mà bảng KHÔNG nhắc tới — cố ý giữ nguyên, không tự đặt mã mới cho
chúng. Đang chờ HKLED xác nhận (xem bình luận trên PM-TASK-00054).

⚠ **Đây là app KHÁCH (tầng 4)**: Property Setter tạo ra chỉ nằm trên site HKLED. Tuyệt đối không
chuyển đoạn này sang app lõi — mã chứng từ là quy ước riêng từng khách.

⚠ **Thứ tự nạp app**: trong `sites/apps.txt`, `mbwnext_hkled` nằm TRƯỚC `mbwnext_advanced_accounting`,
`mbwnext_advanced_selling` và cả `erpnext`. Nếu sau này một app nạp sau ship Property Setter cho
cùng `naming_series` của 9 doctype này thì nó sẽ ĐÈ lên cấu hình ở đây. Đã kiểm 08/08/2026: chưa
app nào đụng tới 9 doctype này.
"""

import frappe

MODULE = "MBWNext HKLed"

# (DocType, series mới, các series khác cần GIỮ LẠI trong danh sách chọn)
MA_CHUNG_TU = [
	("Sales Order", "SO-.YY.-", []),
	("Production Plan", "KSX-.YY.-", []),
	("Work Order", "LSX-.YY.-", []),
	("Stock Entry", "KNB-.YY.-", []),
	("Delivery Note", "PXK-.YY.-", ["MAT-DN-RET-.YYYY.-"]),
	("Purchase Receipt", "PNK-.YY.-", ["MAT-PR-RET-.YYYY.-"]),
	("Material Request", "YCM-.YY.-", []),
	("Purchase Order", "PO-.YY.-", []),
	("Quotation", "BG-.YY.-", []),
]


def _dat(doctype, thuoc_tinh, gia_tri, kieu):
	"""Tạo hoặc cập nhật một Property Setter, không tạo trùng khi chạy lại."""
	ten = frappe.db.get_value(
		"Property Setter",
		{"doc_type": doctype, "field_name": "naming_series", "property": thuoc_tinh},
		"name",
	)
	if ten:
		doc = frappe.get_doc("Property Setter", ten)
	else:
		doc = frappe.new_doc("Property Setter")
		doc.doctype_or_field = "DocField"
		doc.doc_type = doctype
		doc.field_name = "naming_series"
		doc.property = thuoc_tinh

	doc.property_type = kieu
	doc.value = gia_tri
	doc.module = MODULE
	doc.save(ignore_permissions=True)


def execute():
	for doctype, series_moi, giu_lai in MA_CHUNG_TU:
		if not frappe.db.exists("DocType", doctype):
			continue

		danh_sach = "\n".join([series_moi, *giu_lai])
		_dat(doctype, "options", danh_sach, "Text")
		_dat(doctype, "default", series_moi, "Text")

	# 8/9 doctype trên đã có sẵn `no_copy` cho `naming_series` trong ERPNext lõi, riêng Production
	# Plan thì không. Hệ quả: bấm **Duplicate** một Kế hoạch sản xuất cũ sẽ chép luôn
	# `MFG-PP-.YYYY.-` sang bản mới, đẻ ra `MFG-PP-2026-00015` theo mã CŨ. Frappe không chặn được:
	# `_validate_selects()` (frappe/model/base_document.py) bỏ qua đúng trường `naming_series`, nên
	# không có thông báo lỗi nào — chỉ âm thầm sai định dạng. Đặt `no_copy` cho khớp 8 loại còn lại.
	if frappe.db.exists("DocType", "Production Plan"):
		_dat("Production Plan", "no_copy", "1", "Check")

	frappe.clear_cache()
	frappe.db.commit()
	print(f"[mbwnext_hkled] Đã đổi mã chứng từ cho {len(MA_CHUNG_TU)} loại phiếu.")
