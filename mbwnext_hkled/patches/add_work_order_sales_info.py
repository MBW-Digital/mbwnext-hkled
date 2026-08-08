# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Khách Hàng + Nhân Viên Bán Hàng trên Lệnh sản xuất, lấy từ Đơn Bán Hàng (PM-TASK-00050).

`Khách Hàng` dùng `fetch_from` được vì chỉ chép nguyên một trường.

`Nhân Viên Bán Hàng` thì KHÔNG: trên site này Đơn Bán Hàng có **hai** trường cùng nghĩa, cùng nhãn
"Sales Person", cùng do app `mbwnext_advanced_selling` tạo — `sales_person` và `custom_sales_person`.
Lúc làm (08/08/2026) cả 8 đơn đều để trống cả hai nên không suy ra được, hook thử cả hai.

✅ HKLED đã chốt cùng ngày (anh Thắng, PM-TASK-00050): **chỉ dùng `sales_person`**. Hook
`controllers/python_hook/work_order.py::set_sales_info` giờ đọc đúng trường đó.

Vẫn giữ cách điền bằng hook thay vì `fetch_from`, để nếu sau này bên lõi gộp/đổi tên hai trường thì
chỉ phải sửa một chỗ trong code, không phải sửa định nghĩa field rồi chạy lại migrate trên mọi site.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

MODULE = "MBWNext HKLed"


def execute():
	create_custom_fields(
		{
			"Work Order": [
				{
					"fieldname": "custom_customer",
					"label": "Khách Hàng",
					"fieldtype": "Link",
					"options": "Customer",
					"insert_after": "sales_order",
					"read_only": 1,
					"fetch_from": "sales_order.customer",
				},
				{
					"fieldname": "custom_sales_person",
					"label": "Nhân Viên Bán Hàng",
					"fieldtype": "Link",
					"options": "Sales Person",
					"insert_after": "custom_customer",
					"read_only": 1,
					"description": "Lấy từ Đơn Bán Hàng của lệnh này.",
				},
			]
		},
		ignore_validate=True,
	)

	for fieldname in ("custom_customer", "custom_sales_person"):
		name = frappe.db.get_value(
			"Custom Field", {"dt": "Work Order", "fieldname": fieldname}, "name"
		)
		if name:
			frappe.db.set_value("Custom Field", name, "module", MODULE, update_modified=False)

	frappe.db.commit()
