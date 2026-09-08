# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Hai tỷ lệ tính giá niêm yết khai trên TỪNG mặt hàng (PM-FEAT-00045).

Chốt của anh Thắng, ghi trong trường `notes` của PM Feature: bốn tỷ lệ chia làm hai cấp —
*hao phí* và *tỷ lệ tính giá niêm yết* dùng chung toàn hệ thống (nằm ở `HKLed Pricing Setting`),
còn *chi phí R&D* và *lợi nhuận* thì **mỗi mặt hàng một con số**.

⚠ **Không đặt `default`.** Để trống có nghĩa riêng: *"mặt hàng này chưa ai khai tỷ lệ"*. Đặt
`default = 0` thì mọi mặt hàng chưa khai sẽ lặng lẽ tính ra giá niêm yết **thiếu phần lãi** — mà
con số đó trông y hệt một con số đúng. Màn hình bảng giá đọc `flt()` nên trống vẫn tính được, chỉ
là bằng 0; chỗ cần nói ra là màn hình, không phải cái default.

⚠ Đặt sau `custom_replenishment_method` — cùng cụm "thông tin để tính giá và mua hàng" mà
PM-TASK-00067 đã mở trên form Mặt hàng, thay vì đẻ thêm một mục mới ở cuối form.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

TRUONG = {
	"Item": [
		{
			"fieldname": "custom_ty_le_rnd",
			"label": "Tỷ Lệ Chi Phí R&D",
			"fieldtype": "Percent",
			"insert_after": "custom_replenishment_method",
			"description": (
				"Phần trăm chi phí nghiên cứu phát triển cộng vào giá vốn khi tính giá niêm yết. "
				"Để trống nghĩa là chưa khai — khi đó tính như 0."
			),
			"module": "MBWNext HKLed",
		},
		{
			"fieldname": "custom_ty_le_loi_nhuan",
			"label": "Tỷ Lệ Lợi Nhuận",
			"fieldtype": "Percent",
			"insert_after": "custom_ty_le_rnd",
			"description": (
				"Phần trăm lợi nhuận cộng vào giá vốn khi tính giá niêm yết. "
				"Để trống nghĩa là chưa khai — khi đó tính như 0."
			),
			"module": "MBWNext HKLed",
		},
	]
}


def execute():
	create_custom_fields(TRUONG, update=True)
	frappe.db.commit()

	# Dựng bản ghi Single với hai tỷ lệ mặc định, để màn hình bảng giá chạy được ngay sau khi cài
	# mà không phải bắt người dùng vào khai trước. Số lấy đúng ví dụ khách đang dùng (3% và 30%).
	#
	# ⚠ Chỉ đặt khi CHƯA có giá trị. Chạy lại patch trên site đã khai là ghi đè con số của khách —
	#   đúng loại lỗi im lặng: không ai báo, và giá niêm yết cả nhà máy đổi theo.
	if not frappe.db.get_single_value("HKLed Pricing Setting", "ty_le_tinh_gia_niem_yet"):
		doc = frappe.get_single("HKLed Pricing Setting")
		doc.ty_le_hao_phi = 3
		doc.ty_le_tinh_gia_niem_yet = 30
		doc.flags.ignore_permissions = True
		doc.save()
		frappe.db.commit()
		print("[mbwnext_hkled] HKLed Pricing Setting: đặt mặc định hao phí 3%, tỷ lệ niêm yết 30%")
