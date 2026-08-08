# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Ghi Chú Sản Xuất chảy từ Đơn Bán Hàng xuống tận Lệnh sản xuất (PM-TASK-00046).

Chuỗi truyền giá trị khách yêu cầu:

    Sales Order.custom_note            (ĐÃ CÓ từ GAP-4)
      → Sales Order Item.custom_note       (thêm ở đây) — sửa được từng dòng
        → Production Plan Item.custom_note (thêm ở đây) — bảng "Assembly Items"
          → Work Order.custom_note         (thêm ở đây)

⚠ "Bảng Assembly Items" trong yêu cầu của khách là `Production Plan.po_items`
(`Production Plan Item`) — đã kiểm nhãn thật trên site: `po_items` có label "Assembly Items",
còn `sub_assembly_items` để trống nhãn. Đừng nhầm sang bảng bán thành phẩm.

Dùng CÙNG một tên field `custom_note` ở cả 4 doctype cho dễ lần: `Production Plan Sales Order`
(GAP-4) cũng đang dùng tên này.

Patch chỉ tạo lần đầu. Thuộc tính lâu dài nằm trong `fixtures/custom_field.json` — theo bài học
đã ghi trong CLAUDE.md: `sync_fixtures` chạy SAU patches trong `bench migrate`, nên giá trị trong
fixtures thắng giá trị patch vừa set.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

LABEL = "Ghi Chú Sản Xuất"
MODULE = "MBWNext HKLed"


def execute():
	create_custom_fields(
		{
			"Sales Order Item": [
				{
					"fieldname": "custom_note",
					"label": LABEL,
					"fieldtype": "Small Text",
					"insert_after": "description",
					"description": "Tự nhận theo Ghi Chú Sản Xuất của đơn, sửa lại được cho từng dòng.",
				}
			],
			"Production Plan Item": [
				{
					"fieldname": "custom_note",
					"label": LABEL,
					"fieldtype": "Small Text",
					"insert_after": "description",
					"description": "Lấy từ dòng hàng tương ứng của Đơn Bán Hàng.",
				}
			],
			"Work Order": [
				{
					"fieldname": "custom_note",
					"label": LABEL,
					"fieldtype": "Small Text",
					"insert_after": "custom_required_completion_date__time",
					"description": "Lấy từ dòng Assembly Items tương ứng của Kế Hoạch Sản Xuất.",
				}
			],
		},
		ignore_validate=True,
	)

	# Gán module để `fixtures` (lọc theo module = "MBWNext HKLed") bắt được khi export.
	for dt in ("Sales Order Item", "Production Plan Item", "Work Order"):
		name = frappe.db.get_value("Custom Field", {"dt": dt, "fieldname": "custom_note"}, "name")
		if name:
			frappe.db.set_value("Custom Field", name, "module", MODULE, update_modified=False)

	frappe.db.commit()
