# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Đổi `HKLed Pinned Material.qty` ➜ `so_luong_ghim` (PM-FEAT-00036).

🔴 **Vì sao phải đổi — anh Thắng báo 05/09 10:56: *"anh thử sửa số ghim rồi ấn save thì không
được"*.**

Tên `qty` **trùng tên handler của ERPNext** trên form Đơn Bán. `frappe.model.set_value` trên một
dòng con gọi `frm.script_manager.trigger("qty", ...)`, mà `TransactionController` có sẵn một
phương thức tên `qty` — nó chạy phép tính tổng chứng từ trên một dòng **không có `rate` lẫn
`amount`**, kết quả là `in_words` bị xoá thành rỗng. Trường đó không cho sửa sau khi duyệt, nên
lần lưu tiếp theo bị chặn:

    Cannot Update After Submit — Not allowed to change In Words (Company Currency) after
    submission from "VND Hai Triệu Một Trăm Sáu Mươi Nghìn chẵn" to ""

Đo 05/09 để chắc chắn không đổ oan cho lõi: sửa một dòng **lưới hàng hoá** thì `in_words` giữ
nguyên và lưu được; sửa một dòng **bảng ghim** thì `in_words` thành rỗng. Khác biệt duy nhất là
tên trường.

⚠ `item_code` của bảng này **cũng trùng** một handler của `TransactionController`. Hiện không nổ
vì trường đó `read_only` nên người dùng không đổi được. Ngày nào mở khoá nó thì phải đổi tên luôn.

Bài học chung: **bảng con cắm vào chứng từ của lõi thì đừng đặt tên trường trùng tên trường của
lõi** — không có lỗi lúc dựng, chỉ nổ khi người dùng gõ vào ô.
"""

import frappe
from frappe.model.utils.rename_field import rename_field


def execute():
	if not frappe.db.exists("DocType", "HKLed Pinned Material"):
		return

	cot = frappe.db.get_table_columns("HKLed Pinned Material")
	if "so_luong_ghim" in cot:
		print("[mbwnext_hkled] Ghim vật tư: cột đã là `so_luong_ghim`, không đổi lại")
		return
	if "qty" not in cot:
		return

	frappe.reload_doc("mbwnext_hkled", "doctype", "hkled_pinned_material")
	rename_field("HKLed Pinned Material", "qty", "so_luong_ghim")
	frappe.clear_cache(doctype="Sales Order")
	print("[mbwnext_hkled] Ghim vật tư: đổi tên cột `qty` ➜ `so_luong_ghim` (tránh trùng handler ERPNext)")
