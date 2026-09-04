# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Bảng lưu phần ghim vật tư trên Đơn Bán + mở khoá ô ghim sau khi duyệt (PM-FEAT-00036).

Ba việc, cố ý gộp một patch vì tách ra thì site chỉ chạy nửa đường là hỏng:

1. Tạo `Sales Order.custom_ghim_vat_tu` — bảng con `HKLed Pinned Material`, sổ cam kết vật tư.
2. Bật `allow_on_submit` cho `custom_ghim_ton_kha_dung` và `custom_so_luong_giu_cho`
   (anh Thắng chốt 04/09 15:59: *"Ô ghim em cho phép mở khóa khi đơn đã duyệt nhé"*).
3. Bật `allow_on_submit` cho chính bảng mới — nút *Phân Bổ* rót hàng vào đơn ĐÃ DUYỆT, không
   có cờ này thì `doc.save()` ném `Không được phép sửa sau khi duyệt`.

⚠ **Bật cờ thôi là THỦNG lớp chặn.** `chan_giu_cho_vuot_ton` đang treo ở sự kiện `validate`, mà
Frappe **không chạy `validate`** trên đường update-after-submit (`document.py` chọn nhánh
`_action = "update_after_submit"` → chỉ chạy `before_update_after_submit`). Nghĩa là mở khoá ô
ghim mà không hook thêm thì người dùng sửa *Số Lượng Giữ Chỗ* trên đơn đã duyệt sẽ **không bị
kiểm gì cả** — đúng con số bị trừ khỏi tồn khả dụng của mọi đơn khác. Hook bổ sung nằm ở
`hooks.py`, khối `Sales Order`; sửa patch này thì kiểm lại hook đó còn không.

⚠ Thuộc tính lâu dài phải nằm trong `fixtures/custom_field.json` — `sync_fixtures` chạy SAU
patches nên fixtures thắng. Sửa xong nhớ:

    bench --site hkled.com export-fixtures --app mbwnext_hkled
"""

import frappe


SALES_ORDER_FIELDS = [
	{
		"fieldname": "custom_ghim_vat_tu",
		"label": "Ghim Vật Tư",
		"fieldtype": "Table",
		"options": "HKLed Pinned Material",
		# Neo ngay dưới lưới hàng hoá: người đọc nhìn thấy phần vật tư bị giữ ngay cạnh phần
		# thành phẩm sinh ra nó. `items` là field lõi, không phải field của app khác nên
		# không sợ bị gỡ mất neo.
		"insert_after": "items",
		"allow_on_submit": 1,
		# Bảng do MÁY ghi. Cho sửa tay là mất chỗ dựa của bất biến "Σ ghim ≤ tồn thực tế":
		# phép cấp phát chỉ lấy từ phần tồn chưa ai giữ, sửa tay thì đi vòng qua nó.
		"read_only": 1,
		"depends_on": "eval:doc.custom_ghim_ton_kha_dung",
		"description": (
			"Máy tự ghi. Phần nguyên vật liệu đơn này đang giữ để sản xuất số hàng còn thiếu. "
			"Nhả ra bằng cách bỏ tích Ghim Tồn Khả Dụng hoặc giảm Số Lượng Giữ Chỗ."
		),
	},
]

# (doctype, fieldname) — trường đã có từ patch cũ, giờ mở khoá cho sửa sau khi duyệt.
MO_KHOA = [
	("Sales Order", "custom_ghim_ton_kha_dung"),
	("Sales Order Item", "custom_so_luong_giu_cho"),
]


def _create(doctype, fields):
	them = []
	for spec in fields:
		name = f"{doctype}-{spec['fieldname']}"
		if frappe.db.exists("Custom Field", name):
			continue
		frappe.get_doc(
			{"doctype": "Custom Field", "dt": doctype, "module": "MBWNext HKLed", **spec}
		).insert(ignore_permissions=True)
		them.append(spec["fieldname"])
	return them


def _mo_khoa():
	mo = []
	for doctype, fieldname in MO_KHOA:
		name = f"{doctype}-{fieldname}"
		if not frappe.db.exists("Custom Field", name):
			continue
		if frappe.db.get_value("Custom Field", name, "allow_on_submit"):
			continue
		frappe.db.set_value("Custom Field", name, "allow_on_submit", 1)
		mo.append(fieldname)
	return mo


def execute():
	if not frappe.db.exists("DocType", "HKLed Pinned Material"):
		frappe.reload_doc("mbwnext_hkled", "doctype", "hkled_pinned_material")

	them = _create("Sales Order", SALES_ORDER_FIELDS)
	mo = _mo_khoa()

	for dt in ("Sales Order", "Sales Order Item"):
		frappe.clear_cache(doctype=dt)

	print(
		f"[mbwnext_hkled] Ghim vật tư: tạo {len(them)} trường "
		f"({', '.join(them) or 'không có, đã tồn tại'}) · mở khoá sau duyệt {len(mo)} trường "
		f"({', '.join(mo) or 'không có, đã mở'})"
	)
