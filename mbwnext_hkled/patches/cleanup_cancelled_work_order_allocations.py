# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Dọn Phân Công còn sót của các Lệnh sản xuất đã HUỶ (PM-TASK-00045, chốt C6 ngày 08/08/2026).

Từ nay trở đi hook `Work Order.on_cancel` / `on_trash` lo việc này
(`controllers/python_hook/work_order.py::cleanup_employee_allocation`), nhưng dữ liệu phát sinh
TRƯỚC khi có hook thì vẫn còn nguyên — patch này dọn một lần cho sạch.

Vì sao đáng dọn chứ không chỉ để đó: `find_conflicting_allocation_at()` và
`get_next_conflicting_allocation()` trong `api/work_order_schedule.py` chỉ lọc theo nhân sự và
thời gian, KHÔNG xét trạng thái Work Order. Một Phân Công mồ côi của lệnh đã huỷ vẫn chiếm chỗ
của nhân sự, làm `recalculate_schedule` trả về thời điểm bắt đầu muộn hơn thực tế — sai âm thầm,
không báo lỗi gì.

Phạm vi có chủ ý — chỉ dọn lệnh **Cancelled** (`docstatus = 2`) và lệnh **đã bị xoá hẳn**:

- Lệnh còn **Nháp** thì GIỮ. Nháp là kế hoạch sắp tới, vẫn nên giữ chỗ của nhân sự. Anh Thắng
  chưa nói tới ca này khi chốt C6 nên đây là giả định đang áp dụng, ghi rõ để còn sửa nếu sai.
- Lệnh đã **Completed / In Process** thì đương nhiên giữ.
"""

import frappe


def execute():
	rows = frappe.db.sql(
		"""
		select a.name, a.work_order, w.name as wo_exists, w.docstatus
		from `tabEmployee Allocation` a
		left join `tabWork Order` w on w.name = a.work_order
		where w.name is null or w.docstatus = 2
		""",
		as_dict=True,
	)
	if not rows:
		return

	names = []
	for row in rows:
		names.append(row.name)

	# Xoá link trước rồi mới xoá bản ghi — `Work Order Employee.allocation_record` là Link tới
	# Employee Allocation nên `delete_doc` sẽ ném LinkExistsError. Lý do không dùng `force=True`
	# xem chú thích trong cleanup_employee_allocation().
	frappe.db.set_value(
		"Work Order Employee",
		{"allocation_record": ["in", names]},
		"allocation_record",
		None,
		update_modified=False,
	)

	deleted = 0
	for name in names:
		if not frappe.db.exists("Employee Allocation", name):
			continue
		frappe.delete_doc("Employee Allocation", name, ignore_permissions=True)
		deleted += 1

	frappe.db.commit()
	print(f"[mbwnext_hkled] Đã dọn {deleted} Phân Công mồ côi của Lệnh sản xuất đã huỷ/đã xoá.")
