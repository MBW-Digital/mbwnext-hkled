# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Cho bên sản xuất quyền ĐỌC hồ sơ Nhân sự, để dùng được các tính năng theo Đội Sản Xuất.

Vì sao cần: hộp thoại "Tạo Nhanh" lịch làm việc (GAP-2) và "Thêm Đội Sản Xuất" (GAP-6) đều phải
liệt kê nhân sự của đội. Trên site HKLED, `Employee` chỉ cấp cho `Employee` / `HR Manager` /
`HR User`, nên người phân ca (vai trò sản xuất) bị chặn ngay và tính năng vô dụng với họ.

Chỉ cấp **read**, không cấp write/create/delete — bên sản xuất không sửa hồ sơ nhân sự.

⚠ CẠM BẪY của Frappe phải biết trước khi sửa file này:
`Meta.set_custom_permissions()` — nếu một DocType có BẤT KỲ bản ghi `Custom DocPerm` nào thì
Frappe **thay thế sạch** danh sách DocPerm chuẩn bằng đúng các dòng Custom đó
(`frappe/model/meta.py`: `if custom_perms: self.permissions = [...]`).
Tức là tự tay tạo 2 dòng Custom DocPerm cho `Employee` sẽ **xoá luôn** quyền của HR Manager,
HR User và Employee — hỏng toàn bộ phân hệ nhân sự.

Vì vậy phải dùng `frappe.permissions.add_permission()`: hàm này gọi `setup_custom_perms()` trước,
sao chép toàn bộ DocPerm chuẩn sang Custom DocPerm rồi mới thêm dòng mới. Không tự `insert`.

⚠ Cố ý KHÔNG khai `Custom DocPerm` vào `fixtures`: fixtures sẽ chụp lại **toàn bộ** quyền của
`Employee` trên site này rồi áp sang site khác khi cài app — tức là áp mô hình phân quyền nhân sự
của HKLED lên bất kỳ site nào. Patch thì chỉ thêm đúng phần cần, không đụng phần còn lại.
"""

import frappe
from frappe.permissions import add_permission

DOCTYPE = "Employee"
ROLES = ("Manufacturing Manager", "Manufacturing User")


def execute():
	for role in ROLES:
		if not frappe.db.exists("Role", role):
			continue
		# Đã có dòng cho role này rồi thì thôi — patch phải chạy lại được nhiều lần.
		if frappe.db.exists(
			"Custom DocPerm", {"parent": DOCTYPE, "role": role, "permlevel": 0, "if_owner": 0}
		):
			continue
		# add_permission tự lo việc sao chép quyền chuẩn sang Custom DocPerm trước.
		add_permission(DOCTYPE, role, 0, "read")

	frappe.clear_cache(doctype=DOCTYPE)
