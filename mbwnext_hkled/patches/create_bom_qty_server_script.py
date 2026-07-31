# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Cài Server Script `hkled_resolve_bom_qty` lần đầu (mục 3 tài liệu thiết kế).

CỐ Ý KHÔNG GHI ĐÈ script đã tồn tại: theo thiết kế, HKLED sửa công thức trực tiếp trên
Server Script và có hiệu lực ngay. Nếu patch ghi đè, mỗi lần `bench migrate` sẽ xoá sạch
chỉnh sửa của họ. Muốn nạp lại bản gốc thì xoá/đổi tên script trên site rồi chạy lại patch.
"""

import frappe

from mbwnext_hkled.server_scripts.bom_qty import SCRIPT, SCRIPT_NAME


def execute():
	if frappe.db.exists("Server Script", SCRIPT_NAME):
		return

	frappe.get_doc(
		{
			"doctype": "Server Script",
			"name": SCRIPT_NAME,
			"script_type": "API",
			"api_method": SCRIPT_NAME,
			"allow_guest": 0,
			"module": "MBWNext HKLed",
			"script": SCRIPT,
		}
	).insert(ignore_permissions=True)
