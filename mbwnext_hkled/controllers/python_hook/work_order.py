# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Đồng bộ Employee Allocation khi Lệnh sản xuất được Finish thực sự (PHẦN III, mục 7.9).

Hook ở điểm nào và VÌ SAO — đây là chỗ dễ mắc lỗi:

Work Order KHÔNG có method `on_update`, và status chuyển sang "Completed" bằng
`self.db_set("status", ...)` bên trong `WorkOrder.update_status()` (erpnext work_order.py).
`db_set` không chạy doc hook nào cả; ngoài ra WO lúc đó đã submit nên Frappe chỉ gọi
`on_update_after_submit`, không gọi `on_update`. Vì vậy đăng ký ở `on_update` là code chết.

Điểm hook thật sự chạy: `Stock Entry.update_work_order()` gọi
`pro_doc.run_method("update_status")` (cả khi submit lẫn cancel Stock Entry).
`run_method` có compose doc_events hook, và hook chạy SAU method gốc — tức là lúc handler
này chạy thì `doc.status` đã là "Completed".

Kèm theo đó: `set_actual_dates()` được gọi SAU `update_status()` trong cùng luồng, nên
`doc.actual_end_date` lúc này vẫn là giá trị CŨ. Không đọc thẳng field đó — phải tự tính
thời điểm hoàn thành từ chứng từ như `set_actual_dates()` làm.
"""

import frappe
from frappe import _
from frappe.utils import flt, get_datetime, now_datetime

FINISH_PURPOSES = ("Material Transfer for Manufacture", "Manufacture")


def get_actual_finish_time(doc):
	"""Thời điểm hoàn thành thực tế của Work Order.

	Bám theo cách `WorkOrder.set_actual_dates()` tính, nhưng tính ngay tại đây vì
	`set_actual_dates()` chạy sau hook này nên `doc.actual_end_date` còn là giá trị cũ.
	"""
	if doc.get("operations"):
		end_times = [row.actual_end_time for row in doc.operations if row.actual_end_time]
		if end_times:
			return get_datetime(max(end_times))

	rows = frappe.get_all(
		"Stock Entry",
		fields=["timestamp(posting_date, posting_time) as posting_datetime"],
		filters={"work_order": doc.name, "docstatus": 1, "purpose": ["in", FINISH_PURPOSES]},
	)
	posting_datetimes = [row.posting_datetime for row in rows if row.posting_datetime]
	if posting_datetimes:
		return get_datetime(max(posting_datetimes))

	return get_datetime(doc.actual_end_date) if doc.actual_end_date else now_datetime()


def sync_employee_allocation_on_finish(doc, method=None, *args, **kwargs):
	"""Co Employee Allocation về thời điểm WO kết thúc thật, để nhân sự không bị giữ chỗ
	theo lịch dự kiến khi Lệnh sản xuất hoàn thành sớm hơn tính toán."""
	if doc.doctype != "Work Order":
		return
	if doc.status != "Completed" or not doc.get("custom_work_order_employee"):
		return

	finish_time = get_actual_finish_time(doc)

	for row in doc.custom_work_order_employee:
		if not row.allocation_record:
			continue

		start_time = frappe.db.get_value("Employee Allocation", row.allocation_record, "start_time")
		# Không ghi ra khoảng ngược đầu: WO kết thúc trước khi nhân sự này kịp bắt đầu thì
		# giữ nguyên bản ghi, để người dùng tự xử lý thay vì tạo dữ liệu hỏng âm thầm.
		if start_time and finish_time < get_datetime(start_time):
			continue

		frappe.db.set_value("Employee Allocation", row.allocation_record, "end_time", finish_time)


# ══════════════════════════════════════════════════════════════════════════════
# GAP-5 — thừa hưởng thời gian + đội sản xuất từ Kế Hoạch Sản Xuất
# ══════════════════════════════════════════════════════════════════════════════

def _work_team_members(work_team):
	"""Nhân sự Công nhân đang Active của một đội, kèm Bậc Thợ và Nguồn Lực.

	⚠ Phải lấy sẵn `custom_employee_level` + `custom_performance_factor_` chứ KHÔNG trông vào
	`fetch_from` của bảng Nhân Công Tham Gia. Lý do nằm ở thứ tự trong `Document.insert()`:

	    self._validate_links()            <- fetch_from được áp Ở ĐÂY (qua get_invalid_links)
	    self.check_permission("create")
	    self.run_method("before_insert")  <- hook này mới append dòng, tức là SAU

	Dòng thêm ở `before_insert` không bao giờ đi qua vòng fetch, nên Bậc Thợ để trống và
	Nguồn Lực = 0 → `recalculate_schedule` báo "chưa có Nguồn Lực (%) hợp lệ", không tính được lịch.
	Đây là lỗi anh Thắng báo ngày 03/08.
	"""
	if not work_team:
		return []
	return frappe.get_all(
		"Employee",
		filters={
			"custom_work_team": work_team,
			"custom_employee_type": "Công nhân",
			"status": "Active",
		},
		fields=[
			"name",
			"custom_employee_level as employee_level",
			"custom_performance_factor_ as performance_factor_",
		],
		order_by="employee_name asc",
	)


def _plan_row_for(doc):
	"""Dòng Kế Hoạch Sản Xuất tương ứng với WO này: ưu tiên bán thành phẩm, rồi tới item chính.

	Trả về ``(start_time, required_completion, work_team)``; thiếu gì thì để None.
	"""
	# Bán thành phẩm: đội lấy thẳng từ dòng PP Sub Assembly Item.
	if doc.get("production_plan_sub_assembly_item"):
		team = frappe.db.get_value(
			"Production Plan Sub Assembly Item",
			doc.production_plan_sub_assembly_item,
			"custom_work_team",
		)
		if team:
			return None, None, team

	# Item chính: tra ngược dòng Đơn Bán Hàng của kế hoạch qua sales_order của WO.
	if not doc.get("production_plan"):
		return None, None, None

	filters = {"parent": doc.production_plan}
	if doc.get("sales_order"):
		filters["sales_order"] = doc.sales_order

	rows = frappe.get_all(
		"Production Plan Sales Order",
		filters=filters,
		fields=["custom_start_time", "custom_required_completion_date_time", "custom_work_team"],
		limit=1,
	)
	if not rows:
		return None, None, None

	r = rows[0]
	return r.custom_start_time, r.custom_required_completion_date_time, r.custom_work_team


def set_sales_info(doc, method=None):
	"""Điền Khách Hàng + Nhân Viên Bán Hàng từ Đơn Bán Hàng của lệnh (PM-TASK-00050).

	Khách Hàng đã có `fetch_from` nên Frappe tự điền khi lưu qua giao diện; gán lại ở đây để lệnh
	tạo bằng script/API cũng đầy đủ (cùng lý do đã ghi ở `python_hook/production_plan.py`).

	Nhân Viên Bán Hàng KHÔNG dùng `fetch_from` được, dù chỉ chép một trường: Đơn Bán Hàng trên site
	này có HAI trường cùng nghĩa, cùng nhãn "Sales Person", cùng của app `mbwnext_advanced_selling`
	— `sales_person` và `custom_sales_person`.

	✅ HKLED đã chốt (anh Thắng, 08/08/2026, PM-TASK-00050): **chỉ dùng `sales_person`**.
	Vì vậy ở đây đọc đúng một trường đó. Trước khi có câu trả lời, hàm này thử cả hai — đã bỏ nhánh
	dự phòng cho gọn, vì đoán mò lâu dài sẽ che mất trường hợp nhập sai ô.

	⚠ Trường `custom_sales_person` trên **Sales Order** vẫn còn trên màn hình nhưng KHÔNG được dùng.
	Nó thuộc app lõi `mbwnext_advanced_selling` (dùng chung mọi khách) nên app khách không được tự
	gỡ — muốn bỏ phải đề xuất bên lõi. Đừng nhầm nó với `Work Order.custom_sales_person` là trường
	của chính app này.
	"""
	if doc.doctype != "Work Order":
		return
	if not doc.get("sales_order"):
		return

	so = frappe.db.get_value(
		"Sales Order",
		doc.sales_order,
		["customer", "sales_person"],
		as_dict=True,
	)
	if not so:
		return

	if not doc.get("custom_customer"):
		doc.custom_customer = so.customer
	if not doc.get("custom_sales_person"):
		doc.custom_sales_person = so.sales_person


def clear_copied_allocation_record(doc, method=None):
	"""Lệnh mới tạo bằng Sửa đổi/Nhân bản không được mang theo Bản Ghi Phân Công của lệnh cũ.

	`Work Order Employee.allocation_record` đã đặt `no_copy = 1`, nhưng thế VẪN CHƯA ĐỦ:
	`frappe.model.copy_doc` phía client cố ý bỏ qua `no_copy` khi đang Sửa đổi —
	`const is_no_copy = !from_amend && df && cint(df.no_copy) == 1`
	(frappe/public/js/frappe/model/create_new.js). Tức là `no_copy` chỉ chặn nút **Nhân bản**,
	không chặn nút **Sửa đổi**. Mà chính Sửa đổi mới là đường sinh ra dữ liệu bẩn đã thấy trên
	site: `MFG-WO-2026-00022-1` mang link trỏ vào Phân Công của `MFG-WO-2026-00022` đã huỷ.

	Hậu quả nếu để nguyên: `sync_employee_allocation()` thấy `allocation_record` đã có thì
	CẬP NHẬT bản ghi đó thay vì tạo mới — nghĩa là lịch của lệnh mới bị ghi đè lên bản ghi
	Phân Công vẫn mang `work_order` của lệnh cũ.
	"""
	if doc.doctype != "Work Order":
		return

	for row in doc.get("custom_work_order_employee") or []:
		if row.allocation_record:
			row.allocation_record = None


def inherit_from_production_plan(doc, method=None):
	"""WO tạo từ Kế Hoạch Sản Xuất thì thừa hưởng thời gian và nhân sự của đội (mục IV.1, IV.4).

	Hook ở `before_insert` thay vì override `make_work_order` của erpnext: hook áp dụng được cho
	cả tạo tay lẫn tạo hàng loạt, và không phụ thuộc chữ ký hàm của app lõi.
	"""
	if doc.doctype != "Work Order":
		return
	if not doc.get("production_plan"):
		return

	start_time, required_completion, work_team = _plan_row_for(doc)

	# Chỉ điền chỗ còn trống — người dùng đã nhập tay thì tôn trọng.
	if start_time and not doc.get("custom_start_time"):
		doc.custom_start_time = start_time
	if required_completion and not doc.get("custom_required_completion_date__time"):
		doc.custom_required_completion_date__time = required_completion

	# PM-TASK-00046: Ghi Chú Sản Xuất lấy từ đúng dòng Assembly Items sinh ra lệnh này.
	# `Work Order.production_plan_item` là Data chứa TÊN dòng `Production Plan Item`, không phải Link
	# — nên tra bằng db.get_value theo tên, và không trông vào fetch_from.
	if not doc.get("custom_note") and doc.get("production_plan_item"):
		doc.custom_note = frappe.db.get_value(
			"Production Plan Item", doc.production_plan_item, "custom_note"
		)


def ensure_start_time(doc, method=None):
	"""Lệnh sản xuất KHÔNG được phép ra đời mà thiếu Thời Gian Bắt Đầu (lỗi Thắng báo 08/08).

	`Work Order.custom_start_time` là trường **bắt buộc**, nhưng ERPNext tạo lệnh hàng loạt từ Kế
	Hoạch Sản Xuất bằng `flags.ignore_mandatory = True` (xem `ProductionPlan.make_work_order`). Kết
	quả: lệnh được ghi vào CSDL với ô bắt buộc bỏ trống — và từ đó **mọi lần Lưu đều báo lỗi**
	*"Value missing for Work Order: Thời Gian Bắt Đầu"*, người dùng không sửa được gì nữa.

	Hệ quả dây chuyền: `set_sales_info` chạy ở `validate` nên cũng không bao giờ ghi được giá trị,
	làm ô Nhân Viên Bán Hàng trống. Mà Frappe **ẩn hẳn** trường chỉ-đọc đang rỗng, nên nhìn trên
	màn hình cứ như tính năng chưa được làm. Đó chính là thứ anh Thắng nhìn thấy ở MFG-WO-2026-00037.

	Thứ tự lấy giá trị, dừng ở cái đầu tiên có:
	  1. Kế Hoạch Sản Xuất / Đơn Bán Hàng — đã lo ở `inherit_from_production_plan`
	  2. `Sales Order.custom_start_time` của đơn gắn thẳng vào lệnh
	  3. `planned_start_date` — ngày ERPNext tự tính cho lệnh
	  4. thời điểm hiện tại

	⚠ Cố ý KHÔNG bỏ ràng buộc bắt buộc của trường: người dùng nhập tay vẫn phải điền. Chỉ bảo đảm
	đường máy tạo tự động luôn có giá trị, để không sinh ra chứng từ không lưu nổi.
	"""
	if doc.doctype != "Work Order":
		return
	if doc.get("custom_start_time"):
		return

	if doc.get("sales_order"):
		gio_don = frappe.db.get_value("Sales Order", doc.sales_order, "custom_start_time")
		if gio_don:
			doc.custom_start_time = gio_don
			return

	doc.custom_start_time = get_datetime(doc.get("planned_start_date")) if doc.get(
		"planned_start_date"
	) else now_datetime()

	if not work_team or doc.get("custom_work_order_employee"):
		return

	for member in _work_team_members(work_team):
		doc.append(
			"custom_work_order_employee",
			{
				"employee": member.name,
				# Điền tay vì fetch_from đã chạy xong trước before_insert — xem _work_team_members.
				"employee_level": member.employee_level,
				"performance_factor_": member.performance_factor_,
			},
		)


# ══════════════════════════════════════════════════════════════════════════════
# GAP-7 — Sản Lượng Nhân Viên
# ══════════════════════════════════════════════════════════════════════════════

def split_employee_production_on_finish(doc, method=None, *args, **kwargs):
	"""Chia sản lượng cho nhân công khi WO hoàn thành: phần nguyên cho tất cả, phần dư dồn dòng đầu.

	Ví dụ tài liệu: 10 cái cho A/B/C → 4 / 3 / 3.

	⚠ Chỉ chia khi bảng đang TRỐNG. Đã chia rồi mà chia đè thì xoá mất phần người dùng sửa tay,
    mà C12 (chốt 02/08) cho phép sửa tay sau khi Finish.
	"""
	if doc.doctype != "Work Order" or doc.status != "Completed":
		return
	if doc.get("custom_employee_production"):
		return

	workers = [r.employee for r in doc.get("custom_work_order_employee") or [] if r.employee]
	produced = int(flt(doc.get("produced_qty")))
	if not workers or produced <= 0:
		return

	base, remainder = divmod(produced, len(workers))
	rows = []
	for idx, employee in enumerate(workers):
		qty = base + (remainder if idx == 0 else 0)
		if qty <= 0:
			continue
		rows.append({"employee": employee, "qty": qty})

	if not rows:
		return

	# Dùng db_insert qua doc.append + db_update vì WO đã submit; ghi thẳng cho gọn và
	# không kích hoạt lại vòng validate giữa luồng update_status của Stock Entry.
	for row in rows:
		child = frappe.get_doc(
			{
				"doctype": "Employee Production",
				"parent": doc.name,
				"parenttype": "Work Order",
				"parentfield": "custom_employee_production",
				"idx": rows.index(row) + 1,
				**row,
			}
		)
		child.insert(ignore_permissions=True)

	doc.reload()


def validate_employee_production(doc, method=None):
	"""Tổng Sản Lượng Nhân Viên phải bằng Số Lượng Đã Sản Xuất của lệnh (C12, chốt 02/08).

	Đăng ký ở CẢ `validate` lẫn `before_update_after_submit`: với document đã submit, Frappe
	không gọi `validate` nữa (chỉ `before_update_after_submit`), mà C12 lại cho sửa tay sau
	khi Finish — thiếu hook thứ hai là ràng buộc này không chạy đúng lúc cần nhất.
	"""
	if doc.doctype != "Work Order":
		return

	rows = doc.get("custom_employee_production") or []
	if not rows:
		return

	total = sum(int(flt(r.qty)) for r in rows)
	produced = int(flt(doc.get("produced_qty")))
	if total == produced:
		return

	diff = total - produced
	frappe.throw(
		_(
			"Tổng Sản Lượng Nhân Viên ({0} cái) phải bằng Số Lượng Đã Sản Xuất ({1} cái). Đang {2} {3} cái."
		).format(total, produced, _("vượt") if diff > 0 else _("thiếu"), abs(diff))
	)


# ══════════════════════════════════════════════════════════════════════════════
# PM-TASK-00045 — dọn Employee Allocation khi Lệnh sản xuất bị HUỶ hoặc XOÁ
# ══════════════════════════════════════════════════════════════════════════════

def cleanup_employee_allocation(doc, method=None):
	"""Huỷ/xoá Lệnh sản xuất thì xoá luôn Phân Công của nó (chốt C6, 08/08/2026).

	Đây KHÔNG chỉ là chuyện hiển thị trên biểu đồ. `find_conflicting_allocation_at()` và
	`get_next_conflicting_allocation()` trong `api/work_order_schedule.py` lọc theo nhân sự và
	thời gian, KHÔNG xét trạng thái Work Order — nên một lệnh đã huỷ vẫn chiếm chỗ của nhân sự
	và đẩy lùi thời điểm bắt đầu của mọi lệnh tính sau đó.

	Dọn tại nguồn thay vì lọc lúc đọc: chỉ cần sửa một chỗ, và mọi nơi đang đọc bảng
	Employee Allocation (engine tính lịch, biểu đồ, báo cáo sau này) đều đúng luôn — không phải
	nhớ thêm điều kiện lọc ở từng chỗ đọc.
	"""
	if doc.doctype != "Work Order":
		return

	names = frappe.get_all("Employee Allocation", filters={"work_order": doc.name}, pluck="name")
	if not names:
		return

	# ⚠ Phải xoá LINK trước, xoá BẢN GHI sau.
	# `Work Order Employee.allocation_record` là Link tới Employee Allocation, nên
	# `frappe.delete_doc` sẽ ném LinkExistsError (`check_if_doc_is_linked` trong
	# frappe/model/delete_doc.py). Với `on_trash` càng chắc chắn dính: dòng con của WO vẫn còn
	# nguyên trong DB tại thời điểm hook này chạy.
	# KHÔNG dùng `force=True` để né — cờ đó tắt luôn MỌI kiểm tra liên kết khác, tức là che mất
	# cả những ràng buộc mình thật sự muốn giữ, chỉ để qua được đúng một chỗ đã biết trước.
	frappe.db.set_value(
		"Work Order Employee",
		{"allocation_record": ["in", names]},
		"allocation_record",
		None,
		update_modified=False,
	)

	for name in names:
		# Để mặc định (không `delete_permanently`) nên Frappe vẫn lưu một bản Deleted Document —
		# thao tác này xoá dữ liệu nên giữ đường lùi là đáng, số lượng bản ghi cũng rất nhỏ.
		frappe.delete_doc("Employee Allocation", name, ignore_permissions=True)
