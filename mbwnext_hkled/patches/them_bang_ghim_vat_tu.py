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
		# ⚠ ĐỔI 05/09: bảng nay CHO SỬA cột *Đã Ghim* (anh Thắng 09:20 — *"có thể có trường hợp
		# các bạn nhường nhau 1 vài nguyên vật liệu trong đó"*). Bất biến "Σ ghim ≤ tồn thực tế"
		# vẫn giữ được vì phép cấp phát kẹp con số người gõ xuống phần tồn chưa ai giữ, và nói
		# ra khi phải kẹp. Các cột còn lại vẫn `read_only` ở mức DocType con.
		"read_only": 0,
		"depends_on": "eval:doc.custom_ghim_ton_kha_dung",
		"description": (
			"Máy tự điền. Phần nguyên vật liệu đơn này đang giữ để sản xuất số hàng còn thiếu. "
			"Sửa cột Đã Ghim để nhường bớt cho đơn khác; nhả hết thì bỏ tích Ghim Tồn Khả Dụng "
			"hoặc giảm Số Lượng Giữ Chỗ."
		),
	},
]

PURCHASE_RECEIPT_FIELDS = [
	{
		"fieldname": "custom_ghim_da_phan_bo",
		"label": "Đã Phân Bổ Cho",
		"fieldtype": "Small Text",
		"insert_after": "items",
		"read_only": 1,
		# 🔴 BẮT BUỘC `allow_on_submit`: nút *Phân Bổ* chỉ chạy trên phiếu ĐÃ DUYỆT, nên đây là
		# trường duy nhất được ghi sau khi duyệt. Thiếu cờ này thì nút chạy xong không ghi được
		# nhật ký, và lúc huỷ phiếu sẽ không biết đã chia cho ai.
		"allow_on_submit": 1,
		"description": (
			"Máy tự ghi khi bấm nút Phân Bổ. Huỷ phiếu thì hệ thống đọc đây để thu hồi đúng "
			"phần đã chia cho từng đơn."
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
	them += _create("Purchase Receipt", PURCHASE_RECEIPT_FIELDS)
	mo = _mo_khoa()
	mo_bang = _mo_khoa_bang_ghim()

	for dt in ("Sales Order", "Sales Order Item", "Purchase Receipt"):
		frappe.clear_cache(doctype=dt)

	print(
		f"[mbwnext_hkled] Ghim vật tư: tạo {len(them)} trường "
		f"({', '.join(them) or 'không có, đã tồn tại'}) · mở khoá sau duyệt {len(mo)} trường "
		f"({', '.join(mo) or 'không có, đã mở'})"
		+ (" · mở khoá sửa tay bảng ghim vật tư" if mo_bang else "")
	)


def _mo_khoa_bang_ghim():
	"""ĐỔI 05/09: cho sửa tay cột *Đã Ghim* — patch cũ đã tạo field với `read_only = 1`.

	Không gộp vào `_create` được vì trường đã tồn tại trên site từ 04/09, mà `_create` cố ý bỏ
	qua trường đã có (idempotent). Chỉ nắn khi nó vẫn đang khoá, người dùng tự đổi thì để yên.
	"""
	name = "Sales Order-custom_ghim_vat_tu"
	if not frappe.db.exists("Custom Field", name):
		return False
	if not frappe.db.get_value("Custom Field", name, "read_only"):
		return False
	frappe.db.set_value("Custom Field", name, "read_only", 0)
	return True
