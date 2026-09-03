# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Ghim tồn khả dụng trên Đơn Bán — ô tích ở cấp đơn, số lượng ở từng dòng (PM-FEAT-00023).

Hai trường, cố ý ở HAI cấp khác nhau (anh Thắng chốt 02/09 12:32):

- `Sales Order.custom_ghim_ton_kha_dung` — CÔNG TẮC chung. Tích một cái là hệ thống điền mức
  tối đa cho MỌI dòng; đơn 20 dòng không phải gõ 20 ô.
- `Sales Order Item.custom_so_luong_giu_cho` — con số THẬT bị trừ khỏi tồn khả dụng của đơn khác.

## Vì sao không dùng `Stock Reservation Entry` của lõi

Chốt 25/08 (PM-FEAT-00034): cơ chế lõi chỉ tính tồn theo **một kho** và chỉ giữ chỗ được **mặt
hàng trên đơn**, không giữ được NVL trong định mức — HKLED cần cả hai. Đo thêm 28/08 trong
`accounts_controller.py::update_child_qty_rate`: sửa số lượng trên đơn đã duyệt thì lõi **huỷ
sạch phần giữ chỗ rồi tạo lại**, và nếu đơn đã soạn hàng (`per_picked > 0`) thì **huỷ mà không
tạo lại** — mất trắng, không báo gì.

## Vì sao là số lượng chứ không phải ô tích như bản đầu

Khách nêu 27/08 tình huống A nhường một phần hàng cho B. Với ô tích, A chỉ nhả được **cả đơn**:
chạy đúng ví dụ anh Thắng đưa thì A định nhường 4 cái *item 1* lại mất luôn 2 cái *item 2*, và
còn phải gọi điện nhờ người thứ ba ghim lại. Với ô số lượng: A sửa 5 xuống 1, hết.

⚠ **KHÔNG cho nhập vượt tồn khả dụng** (anh Thắng chốt 02/09 12:40). Phần chênh không mất đi:
nó nằm ở cột *Thiếu* của Bảng 1.

⚠ **`custom_so_luong_giu_cho` KHÔNG dùng để tính cột *Thiếu***. `thiếu = cần − tồn khả dụng`,
độc lập với phần đã giữ — anh Thắng chốt 02/09 13:15, xem mục 5b của đầu bài. Cột *Thiếu* là
đầu vào để lập Yêu Cầu Mặt Hàng; trừ theo phần đã giữ thì sale đi mua hàng đang nằm sẵn trong
kho.

⚠ Thuộc tính lâu dài phải nằm trong `fixtures/custom_field.json`, patch chỉ tạo lần đầu —
`sync_fixtures` chạy SAU patches nên fixtures thắng. Đã vấp ở C1 (`mandatory_depends_on` bị
fixtures ghi đè về rỗng ngay trong cùng lần migrate). Sửa xong nhớ:

    bench --site hkled.com export-fixtures --app mbwnext_hkled
"""

import frappe


SALES_ORDER_FIELDS = [
	{
		"fieldname": "custom_ghim_ton_kha_dung",
		"label": "Ghim Tồn Khả Dụng",
		"fieldtype": "Check",
		"insert_after": "custom_note",
		"default": "0",
		"description": (
			"Tích ô này thì số lượng chưa giao của đơn được giữ chỗ, các đơn khác không dùng "
			"vào phần tồn đó nữa. Không tích thì hàng vẫn coi là rảnh để cấp cho đơn gấp hơn."
		),
	},
]

SALES_ORDER_ITEM_FIELDS = [
	{
		"fieldname": "custom_so_luong_giu_cho",
		"label": "Số Lượng Giữ Chỗ",
		"fieldtype": "Float",
		# Neo sau `qty`: đây là con số đi kèm số lượng, đọc cạnh nhau mới có nghĩa.
		# Không neo vào field của app khác (`qty_sv`, `custom_item_group`…) — app đó gỡ field
		# thì field này rơi về cuối form mà không ai biết.
		"insert_after": "qty",
		"default": "0",
		"non_negative": 1,
		"depends_on": "eval:parent.custom_ghim_ton_kha_dung",
		"description": "Không vượt quá tồn khả dụng. Bỏ tích Ghim thì số vẫn giữ nguyên, chỉ ngừng áp dụng.",
	},
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


def execute():
	them = _create("Sales Order", SALES_ORDER_FIELDS)
	them += _create("Sales Order Item", SALES_ORDER_ITEM_FIELDS)

	for dt in ("Sales Order", "Sales Order Item"):
		frappe.clear_cache(doctype=dt)

	if them:
		print(f"[mbwnext_hkled] Ghim tồn khả dụng: tạo {len(them)} trường — {', '.join(them)}")
	else:
		print("[mbwnext_hkled] Ghim tồn khả dụng: trường đã có, không tạo lại")
