# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Một dòng sổ cam kết vật tư của Đơn Bán (PM-FEAT-00036, mục 8.3 của đầu bài).

⚠ **Bảng này do MÁY ghi, không phải người.** Mọi trường đều `read_only`, và trường bảng trên
Đơn Bán cũng `read_only` — người dùng nhả hàng bằng cách bỏ tích *Ghim Tồn Khả Dụng* hoặc sửa
*Số Lượng Giữ Chỗ*, không phải bằng cách sửa tay bảng này. Sửa tay được là bất biến #1
(Σ ghim ≤ tồn thực tế) mất chỗ dựa, vì phép cấp phát chỉ lấy từ phần tồn chưa ai giữ.

Nơi ghi duy nhất: `mbwnext_hkled.api.ghim_vat_tu`.
"""

from frappe.model.document import Document


class HKLedPinnedMaterial(Document):
	pass
