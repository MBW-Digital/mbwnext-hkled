# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""PM-TASK-00143 — Nhân sự lấy Phòng Ban theo Đội Sản Xuất của mình.

🔒 **Anh Thắng yêu cầu 07/09/2026 10:55:**

> *"Anh muốn khi chọn đội cho nhân sự thì phòng ban của đội đó được gán vào nhân sự đó luôn có
> được không, vì dễ có trường hợp nhân sự thuộc đội 1, đội 1 thuộc phòng kĩ thuật nhưng ở nhân
> sự mình lại gán nhầm sang phòng kcs"*

Đây là chỗ **một sự thật khai hai nơi** — kiểu dữ liệu bao giờ cũng lệch. Cách chữa là chọn một
nơi làm gốc rồi suy ra nơi kia, chứ không phải đi kiểm tra chéo. Anh Thắng chọn **Đội là gốc**:
đội thuộc phòng nào thì người của đội thuộc phòng đó.

⚠ **Cố ý GHI ĐÈ, không phải chỉ điền chỗ trống.** Khác với các hook thừa hưởng khác của app này
(`inherit_department`, `inherit_from_production_plan`, `sales_order.py`) vốn tôn trọng giá trị
người dùng nhập tay. Ở đây nếu chỉ điền chỗ trống thì **đúng cái sai anh Thắng mô tả sẽ không bao
giờ được sửa**: người đã bị gán nhầm sang Phòng KCS sẽ ở lại đó vĩnh viễn vì ô không trống.

⚠ Chỉ ghi đè khi **đội có khai phòng ban**. Đội chưa khai thì không suy ra được gì, và xoá phòng
của người ta để đổi lấy ô trống là tệ hơn hiện trạng. Đo 07/09 11:0x: **2/2 đội chưa khai phòng
ban** — nên hôm nay hook này chưa đổi một ai; nó chỉ có hiệu lực sau khi anh Thắng khai ô
*Phòng Ban* trên hai bản ghi Đội Sản Xuất.
"""

import frappe


def sync_department_from_team(doc, method=None):
	"""`validate` — Phòng Ban của nhân sự bám theo Đội Sản Xuất.

	Không dùng `fetch_from` được: `fetch_from` chỉ điền khi ô đích còn trống và chỉ chạy phía
	client, nên vừa không sửa được bản ghi đã gán nhầm, vừa lọt đường script/API — đúng hai chỗ
	đã bẫy app này rồi (xem C1 ở `python_hook/employee.py`, và `set_sales_info` ở `work_order.py`).
	"""
	if doc.doctype != "Employee":
		return
	if not doc.get("custom_work_team"):
		return

	phong_cua_doi = frappe.db.get_value("Work Team", doc.custom_work_team, "custom_department")
	if not phong_cua_doi:
		return

	if doc.get("department") == phong_cua_doi:
		return

	cu = doc.get("department")
	doc.department = phong_cua_doi

	# Nói ra khi có thứ bị đổi. Đổi âm thầm ô phòng ban của một người là đúng loại "số đổi mà
	# không ai đụng gì" mà cả dự án này đang đi săn — người lưu phải thấy mình vừa gây ra gì.
	if cu:
		frappe.msgprint(
			frappe._(
				"Đã đổi Phòng Ban của <b>{0}</b> từ <b>{1}</b> sang <b>{2}</b> — theo phòng ban "
				"của đội <b>{3}</b>. Muốn phòng khác thì đổi ở Đội Sản Xuất, hoặc bỏ đội khỏi "
				"nhân sự này."
			).format(doc.get("employee_name") or doc.name, cu, phong_cua_doi, doc.custom_work_team),
			title=frappe._("Phòng Ban lấy theo Đội Sản Xuất"),
			indicator="orange",
		)
