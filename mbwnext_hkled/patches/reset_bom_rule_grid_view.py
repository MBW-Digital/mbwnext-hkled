"""Xoá bố cục lưới `BOM Rule` mà người dùng đã lưu, để cột "Không Sử Dụng" hiện ra.

Frappe lưu bố cục lưới bảng con vào `__UserSettings` theo TỪNG NGƯỜI DÙNG
(`GridView` -> tên doctype con -> danh sách field + độ rộng). Bố cục đã lưu **đè lên**
`in_list_view` / `columns` khai trong DocType — nên thêm field mới vào lưới thì người
đã từng chỉnh lưới sẽ KHÔNG thấy, còn người chưa chỉnh thì thấy. Rất khó đoán vì phụ
thuộc từng tài khoản.

Chỉ gỡ đúng khoá "BOM Rule", giữ nguyên phần cài đặt khác của người dùng (bộ lọc, sắp
xếp, chế độ xem) — xoá cả bản ghi là người dùng mất hết tuỳ chỉnh không liên quan.

Chạy một lần. Sau này ai tự bỏ cột đi thì đó là lựa chọn của họ, không ép lại.
"""

import json

import frappe


def execute():
	rows = frappe.db.sql(
		"""select user, doctype, data from `__UserSettings` where data like %s""",
		("%BOM Rule%",),
		as_dict=True,
	)
	da_sua = 0
	for row in rows:
		try:
			data = json.loads(row.data or "{}")
		except ValueError:
			continue
		grid = data.get("GridView")
		if not isinstance(grid, dict) or "BOM Rule" not in grid:
			continue
		grid.pop("BOM Rule")
		if not grid:
			data.pop("GridView", None)
		frappe.db.sql(
			"""update `__UserSettings` set data = %s where user = %s and doctype = %s""",
			(json.dumps(data), row.user, row.doctype),
		)
		da_sua += 1

	if da_sua:
		print(f"  Đã gỡ bố cục lưới BOM Rule đã lưu của {da_sua} người dùng")
