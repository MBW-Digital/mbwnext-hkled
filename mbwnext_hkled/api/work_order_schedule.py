# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Lịch sản xuất thông minh — PHẦN III tài liệu nghiệp vụ HKLED.

Tự động tính Thời Gian Bắt Đầu / Giới Hạn Tham Gia / Kết Thúc cho từng nhân sự
tham gia Work Order, và Thời Gian Kết Thúc Dự Kiến / Tổng Thời Gian Dự Kiến của
cả Work Order, dựa trên Employee Schedule (lịch làm việc) và Employee Allocation
(các cam kết ở Work Order khác) hiện có. Dòng nào bị Khóa Bắt Đầu / Khóa Kết Thúc
thì giữ nguyên giá trị người dùng nhập, không tính lại.
"""

from datetime import timedelta

import frappe
from frappe import _
from frappe.utils import flt, get_datetime

LOOKAHEAD_DAYS = 60
MAX_ITER = 500


def get_window_containing_or_after(employee, after_dt):
	"""Employee Schedule window sớm nhất có end_time > after_dt (đang chứa after_dt hoặc kế tiếp)."""
	rows = frappe.get_all(
		"Employee Schedule",
		filters={"employee_name": employee, "end_time": [">", after_dt]},
		fields=["name", "start_time", "end_time"],
		order_by="start_time asc",
		limit=1,
	)
	return rows[0] if rows else None


def find_conflicting_allocation_at(employee, at_dt, exclude_work_order):
	rows = frappe.get_all(
		"Employee Allocation",
		filters={
			"employee_name": employee,
			"work_order": ["!=", exclude_work_order],
			"start_time": ["<=", at_dt],
			"end_time": [">", at_dt],
		},
		fields=["name", "work_order", "end_time"],
		limit=1,
	)
	return rows[0] if rows else None


def get_next_conflicting_allocation(employee, after_dt, exclude_work_order):
	rows = frappe.get_all(
		"Employee Allocation",
		filters={
			"employee_name": employee,
			"work_order": ["!=", exclude_work_order],
			"start_time": [">", after_dt],
		},
		fields=["name", "work_order", "start_time", "end_time"],
		order_by="start_time asc",
		limit=1,
	)
	return rows[0] if rows else None


def compute_employee_start(employee, wo_start, wo_name):
	"""Thời điểm sớm nhất >= wo_start, nằm trong 1 khoảng làm việc hợp lệ,
	và không trùng Employee Allocation nào khác của nhân sự."""
	candidate = get_datetime(wo_start)
	for _i in range(MAX_ITER):
		window = get_window_containing_or_after(employee, candidate)
		if not window:
			frappe.throw(
				_("Không tìm thấy Lịch làm việc (Employee Schedule) cho nhân sự {0} kể từ {1}").format(
					frappe.bold(employee), candidate
				)
			)
		if window.start_time > candidate:
			candidate = window.start_time

		conflict = find_conflicting_allocation_at(employee, candidate, wo_name)
		if conflict:
			candidate = conflict.end_time
			continue

		return candidate

	frappe.throw(_("Không thể xác định Thời Gian Bắt Đầu cho nhân sự {0}").format(employee))


def compute_available_until(employee, start_dt, wo_name):
	"""Giới hạn tham gia: nếu nhân sự đã có 1 Employee Allocation khác bắt đầu
	sau start_dt, giới hạn = thời điểm kết thúc của khoảng lịch làm việc cuối
	cùng còn nằm trước cam kết đó. Không có cam kết nào khác -> không giới hạn (None)."""
	next_conflict = get_next_conflicting_allocation(employee, start_dt, wo_name)
	if not next_conflict:
		return None

	cursor = start_dt
	last_end = None
	for _i in range(MAX_ITER):
		window = get_window_containing_or_after(employee, cursor)
		if not window or window.start_time >= next_conflict.start_time:
			break
		if window.end_time <= next_conflict.start_time:
			last_end = window.end_time
			cursor = window.end_time
		else:
			last_end = next_conflict.start_time
			break
	return last_end


def build_employee_intervals(employee, start_dt, hard_cap):
	"""Danh sách (start, end) các khoảng nhân sự thực sự làm việc, tính từ
	start_dt, giới hạn bởi hard_cap (Giới Hạn Tham Gia hoặc Khóa Kết Thúc) nếu có."""
	intervals = []
	cursor = start_dt
	horizon = start_dt + timedelta(days=LOOKAHEAD_DAYS)

	for _i in range(MAX_ITER):
		if cursor >= horizon:
			break
		window = get_window_containing_or_after(employee, cursor)
		if not window:
			break

		w_start = window.start_time if window.start_time > cursor else cursor
		w_end = window.end_time

		if hard_cap and w_start >= hard_cap:
			break
		if hard_cap and w_end > hard_cap:
			intervals.append((w_start, hard_cap))
			break

		intervals.append((w_start, w_end))
		cursor = w_end

	return intervals


def simulate_workload(employees, remaining_workload):
	"""Sweep-line qua các mốc thời gian của tất cả nhân sự, cộng dồn Năng Lực
	(tổng performance_factor/100 của nhân sự đang hoạt động) để tiêu thụ dần
	khối lượng công việc chuẩn còn lại. Trả về (end_time, total_minutes)."""
	breakpoints = set()
	for e in employees:
		for s, en in e["intervals"]:
			breakpoints.add(s)
			breakpoints.add(en)
	breakpoints = sorted(breakpoints)

	total_minutes = 0.0
	end_time = None

	for i in range(len(breakpoints) - 1):
		t1, t2 = breakpoints[i], breakpoints[i + 1]
		if t2 <= t1:
			continue

		active = [e for e in employees if any(s <= t1 and en >= t2 for s, en in e["intervals"])]
		capacity = sum(e["capacity"] for e in active)
		if capacity <= 0:
			continue

		duration = (t2 - t1).total_seconds() / 60.0
		processed = duration * capacity

		if processed >= remaining_workload - 1e-9:
			final_duration = remaining_workload / capacity
			end_time = t1 + timedelta(minutes=final_duration)
			total_minutes += final_duration
			remaining_workload = 0
			break

		remaining_workload -= processed
		total_minutes += duration

	if remaining_workload > 1e-6:
		frappe.throw(
			_(
				"Không đủ Lịch làm việc của nhân sự để hoàn thành khối lượng công việc. "
				"Vui lòng bổ sung thêm nhân sự hoặc Lịch làm việc."
			)
		)

	return end_time, total_minutes


def final_end_for_employee(intervals, wo_end_time):
	relevant = [(s, e) for s, e in intervals if s < wo_end_time]
	if not relevant:
		return wo_end_time
	last_start, last_end = relevant[-1]
	return min(last_end, wo_end_time)


def sync_employee_allocation(row, wo_name, start_dt, end_dt):
	if row.allocation_record and frappe.db.exists("Employee Allocation", row.allocation_record):
		alloc = frappe.get_doc("Employee Allocation", row.allocation_record)
		alloc.start_time = start_dt
		alloc.end_time = end_dt
		alloc.save(ignore_permissions=True)
	else:
		alloc = frappe.get_doc(
			{
				"doctype": "Employee Allocation",
				"employee_name": row.employee,
				"work_order": wo_name,
				"start_time": start_dt,
				"end_time": end_dt,
			}
		)
		alloc.insert(ignore_permissions=True)
		row.allocation_record = alloc.name


def validate_no_duplicate_employee(wo_doc):
	seen = set()
	for row in wo_doc.custom_work_order_employee:
		if not row.employee:
			continue
		if row.employee in seen:
			frappe.throw(
				_("Row #{0}: Nhân sự {1} bị trùng trong Bảng Nhân Công Tham Gia").format(
					row.idx, frappe.bold(row.employee)
				)
			)
		seen.add(row.employee)


@frappe.whitelist()
def recalculate_schedule(work_order):
	wo = frappe.get_doc("Work Order", work_order)
	# `frappe.get_doc` KHÔNG tự kiểm quyền, mà bên dưới lại ghi bằng ignore_permissions —
	# thiếu dòng này thì bất kỳ user đăng nhập nào cũng sửa được lịch của mọi Lệnh sản xuất.
	wo.check_permission("write")

	if not wo.custom_start_time:
		frappe.throw(_("Vui lòng nhập Thời Gian Bắt Đầu cho Work Order"))
	if not wo.custom_work_order_employee:
		frappe.throw(_("Chưa có nhân sự nào trong Bảng Nhân Công Tham Gia"))

	validate_no_duplicate_employee(wo)

	time_per_unit = flt(frappe.db.get_value("Item", wo.production_item, "custom_time_to_manufacture"))
	if not time_per_unit:
		frappe.throw(
			_("Mặt hàng {0} chưa thiết lập Thời Gian Sản Xuất (Phút)").format(frappe.bold(wo.production_item))
		)
	remaining_workload = flt(wo.qty) * time_per_unit

	employees = []
	for row in wo.custom_work_order_employee:
		if not row.employee:
			continue

		if row.lock_start:
			if not row.start_time:
				frappe.throw(_("Row #{0}: đã Khóa Bắt Đầu nhưng chưa nhập Bắt Đầu").format(row.idx))
			start_dt = get_datetime(row.start_time)
			conflict = find_conflicting_allocation_at(row.employee, start_dt, wo.name)
			if conflict:
				frappe.throw(
					_("Row #{0}: Nhân sự {1} đã có lịch ở Work Order {2} vào thời điểm này").format(
						row.idx, frappe.bold(row.employee), frappe.bold(conflict.work_order)
					)
				)
		else:
			start_dt = compute_employee_start(row.employee, wo.custom_start_time, wo.name)

		if row.lock_end:
			if not row.end_time:
				frappe.throw(_("Row #{0}: đã Khóa Kết Thúc nhưng chưa nhập Kết Thúc").format(row.idx))
			hard_cap = get_datetime(row.end_time)
			available_until = None
		else:
			available_until = compute_available_until(row.employee, start_dt, wo.name)
			hard_cap = available_until

		capacity = flt(row.performance_factor_) / 100.0
		if capacity <= 0:
			frappe.throw(
				_("Row #{0}: Nhân sự {1} chưa có Nguồn Lực (%) hợp lệ").format(row.idx, frappe.bold(row.employee))
			)

		intervals = build_employee_intervals(row.employee, start_dt, hard_cap)
		if not intervals:
			frappe.throw(
				_("Row #{0}: Không tìm thấy khoảng thời gian làm việc hợp lệ nào cho nhân sự {1}").format(
					row.idx, frappe.bold(row.employee)
				)
			)

		employees.append(
			{
				"row": row,
				"capacity": capacity,
				"start_time": start_dt,
				"available_until": available_until,
				"intervals": intervals,
			}
		)

	wo_end_time, total_minutes = simulate_workload(employees, remaining_workload)

	for e in employees:
		row = e["row"]
		row.start_time = e["start_time"]
		row.available_until = e["available_until"]
		if not row.lock_end:
			row.end_time = final_end_for_employee(e["intervals"], wo_end_time)
		sync_employee_allocation(row, wo.name, row.start_time, row.end_time)

	wo.custom_end_time = wo_end_time
	wo.custom_estimated_completion_time_minutes = round(total_minutes)
	wo.save(ignore_permissions=True)

	return {
		"end_time": wo.custom_end_time,
		"estimated_completion_time_minutes": wo.custom_estimated_completion_time_minutes,
	}
