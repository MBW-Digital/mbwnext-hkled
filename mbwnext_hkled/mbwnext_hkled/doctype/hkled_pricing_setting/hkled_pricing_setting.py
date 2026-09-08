# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Hai tỷ lệ dùng chung toàn hệ thống khi tính giá niêm yết (PM-FEAT-00045).

⚠ **Vì sao là DocType riêng của app khách, không thêm trường vào `MBWNext System Setting`.**
Màn hình đó thuộc app lõi `mbwnext_localization`, dùng chung cho mọi khách MBWNext — thêm hai ô
riêng của HKLED vào đó là bắt khách khác nhìn thấy thứ không liên quan, và muốn sửa thì phải xin
phép bên lõi. Anh Thắng chốt 08/09 16:21: *"nên tạo 1 màn hình cài đặt riêng cho HKLED"*.

Hai tỷ lệ CÒN LẠI (`R&D`, `lợi nhuận`) cố ý **không** nằm ở đây mà nằm trên từng mặt hàng — cũng
là chốt của anh Thắng, ghi trong trường `notes` của PM Feature.
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class HKLedPricingSetting(Document):
	def validate(self):
		# 🔴 Tỷ lệ này là SỐ CHIA trong công thức giá niêm yết. Để 0 thì phép chia nổ
		#    ZeroDivisionError ở giữa vòng lặp 62 nghìn mặt hàng — chặn ngay từ đây rẻ hơn nhiều.
		if flt(self.ty_le_tinh_gia_niem_yet) <= 0:
			frappe.throw(
				_(
					"<b>Tỷ Lệ Tính Giá Niêm Yết</b> phải lớn hơn 0.<br><br>"
					"Đây là số <b>chia</b> trong công thức: giá niêm yết = (giá vốn + lãi) ÷ tỷ lệ này × 100. "
					"Để 0 thì không tính được giá nào cả."
				)
			)
		if flt(self.ty_le_tinh_gia_niem_yet) > 100:
			frappe.throw(
				_(
					"<b>Tỷ Lệ Tính Giá Niêm Yết</b> đang là {0}%, lớn hơn 100%.<br><br>"
					"Nghĩa là giá niêm yết <b>thấp hơn</b> cả giá vốn cộng lãi. Kiểm lại giúp — "
					"thường tỷ lệ này nằm trong khoảng 25–40%."
				).format(flt(self.ty_le_tinh_gia_niem_yet))
			)
		if flt(self.ty_le_hao_phi) < 0:
			frappe.throw(_("<b>Tỷ Lệ Hao Phí</b> không được âm."))
