# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-2 + GAP-6 — nhân sự theo Đội Sản Xuất và tạo nhanh Lịch làm việc hàng loạt.

GAP-2 (mục III.2, chốt C10 + C10b): tạo lịch cho cả đội theo một khoảng "Từ Ngày – Đến Ngày",
kèm tick chọn thứ trong tuần — chỉ ngày khớp thứ đã tick mới sinh bản ghi.
Ví dụ HKLED nêu: chọn 01/08–10/08 nhưng chỉ tick T2–T7 thì 2 ngày Chủ nhật không tạo lịch.
"""

import json

import frappe
from frappe import _
from frappe.utils import add_days, cint, format_datetime, get_datetime, getdate

# Chặn quét quá dài: tính theo TỔNG số ngày của khoảng, không phải số ngày khớp thứ —
# nếu tính theo số ngày khớp thì người dùng quét cả năm rồi tick 1 thứ là lách được.
MAX_RANGE_DAYS = 62

# Python: Monday=0 … Sunday=6. Giao diện gửi lên theo chuẩn JS: Sunday=0 … Saturday=6.
JS_DOW_BY_PYTHON = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}


def _as_list(value):
	"""Tham số từ frappe.call có thể là list thật hoặc chuỗi JSON — nhận cả hai."""
	if not value:
		return []
	if isinstance(value, str):
		try:
			value = json.loads(value)
		except ValueError:
			return [v.strip() for v in value.split(",") if v.strip()]
	return list(value or [])


@frappe.whitelist()
def get_team_members(work_team, exclude=None, start=None, end=None, exclude_work_order=None):
	"""Nhân sự Công nhân đang Active của một đội, kèm cờ đã có trong bảng của người gọi.

	⚠ Dùng `frappe.get_list` chứ KHÔNG dùng `frappe.get_all`: chỉ `get_list` mới áp
	User Permission. Dùng `get_all` ở đây từng làm lộ nhân sự ngoài phạm vi — user bị
	giới hạn chỉ được thấy 1 người vẫn nhận về cả 3. `frappe.has_permission(...)` không
	cứu được: nó chỉ trả lời "có được xem loại dữ liệu này không", không trả lời
	"được xem những bản ghi nào".
	"""
	frappe.has_permission("Work Team", "read", throw=True)

	excluded = set(_as_list(exclude))
	rows = frappe.get_list(
		"Employee",
		filters={
			"custom_work_team": work_team,
			"custom_employee_type": "Công nhân",
			"status": "Active",
		},
		fields=[
			"name as employee",
			"employee_name",
			"custom_employee_level as employee_level",
			"custom_performance_factor_ as performance_factor",
		],
		order_by="employee_name asc",
		limit_page_length=0,
		ignore_permissions=False,
	)
	for row in rows:
		row["already_added"] = row["employee"] in excluded

	ket_qua = {"members": rows}

	# PM-TASK-00049: có khoảng thời gian thì tính luôn thời gian rảnh, để hộp thoại chỉ phải
	# gọi MỘT lần thay vì gọi thêm vòng thứ hai.
	if start and end:
		ket_qua.update(tinh_thoi_gian_ranh(rows, start, end, exclude_work_order))

	return ket_qua


def _giao_phut(a_tu, a_den, b_tu, b_den):
	"""Số phút giao nhau của hai khoảng; 0 nếu rời nhau."""
	tu = max(a_tu, b_tu)
	den = min(a_den, b_den)
	return (den - tu).total_seconds() / 60.0 if den > tu else 0.0


def tinh_thoi_gian_ranh(members, start, end, exclude_work_order=None):
	"""Thời gian rảnh của từng nhân sự và của cả đội trong khoảng [start, end] — PM-TASK-00049.

	    Tổng thời gian  = phần Lịch làm việc nằm trong khoảng
	    Thời gian bận   = phần Phân Công GIAO VỚI Lịch làm việc, rồi cắt vào khoảng
	    Thời gian rảnh  = tổng − bận
	    % rảnh cả đội   = tổng rảnh cả đội / tổng thời gian cả đội

	⚠ Phải giao Phân Công với Lịch làm việc trước, KHÔNG lấy thẳng khoảng của bản ghi Phân Công:
	mỗi bản ghi chỉ có 2 đầu mút của cả quá trình tham gia nên trùm cả giờ nghỉ trưa và ban đêm
	(xem `api/employee_timeline.py`). Lấy thẳng sẽ tính dư thời gian bận, ra % rảnh thấp hơn thực tế.

	`exclude_work_order`: bỏ qua Phân Công của chính Lệnh sản xuất đang mở — người dùng đang cân
	nhắc thêm đội vào lệnh này, nếu tính cả phần lệnh này đang giữ thì đội luôn trông như đã kín chỗ.
	"""
	tu = get_datetime(start)
	den = get_datetime(end)
	if den <= tu:
		# Lệnh ĐÃ điền đủ 2 mốc nhưng mốc kết thúc lại không sau mốc bắt đầu -> không có
		# khoảng nào để tính. Phải nói đúng lý do: trước đây chỗ này trả None trơn nên hộp
		# thoại hiện nhầm câu "điền 2 trường vào", người dùng nhìn thấy 2 trường đã có sẵn
		# thì tưởng chức năng hỏng (khách báo 11/08).
		return {
			"free_time": None,
			"free_time_note": _(
				"Thời Điểm Cần Hoàn Thành ({0}) không sau Thời Gian Bắt Đầu ({1})"
				" nên không có khoảng thời gian nào để tính. Sửa lại hai mốc này trên lệnh."
			).format(frappe.bold(format_datetime(den)), frappe.bold(format_datetime(tu))),
		}

	ma_nhan_su = []
	for m in members:
		ma_nhan_su.append(m["employee"])
	if not ma_nhan_su:
		return {"free_time": {"total_minutes": 0, "free_minutes": 0, "free_percent": 0}}

	lich = frappe.get_list(
		"Employee Schedule",
		filters={
			"employee_name": ["in", ma_nhan_su],
			"start_time": ["<", den],
			"end_time": [">", tu],
		},
		fields=["employee_name", "start_time", "end_time"],
		limit_page_length=0,
	)

	loc_pc = {
		"employee_name": ["in", ma_nhan_su],
		"start_time": ["<", den],
		"end_time": [">", tu],
	}
	if exclude_work_order:
		loc_pc["work_order"] = ["!=", exclude_work_order]

	phan_cong = frappe.get_list(
		"Employee Allocation",
		filters=loc_pc,
		fields=["employee_name", "start_time", "end_time"],
		limit_page_length=0,
	)

	lich_theo_nguoi = {}
	for row in lich:
		lich_theo_nguoi.setdefault(row.employee_name, []).append(row)
	pc_theo_nguoi = {}
	for row in phan_cong:
		pc_theo_nguoi.setdefault(row.employee_name, []).append(row)

	tong_doi = 0.0
	ranh_doi = 0.0

	for m in members:
		tong = 0.0
		ban = 0.0
		for ca in lich_theo_nguoi.get(m["employee"], []):
			ca_tu = max(ca.start_time, tu)
			ca_den = min(ca.end_time, den)
			if ca_den <= ca_tu:
				continue
			tong += (ca_den - ca_tu).total_seconds() / 60.0
			for pc in pc_theo_nguoi.get(m["employee"], []):
				ban += _giao_phut(ca_tu, ca_den, pc.start_time, pc.end_time)

		# Hai phân công chồng nhau (dữ liệu hỏng) có thể đẩy `ban` vượt `tong` — chặn về 0 thay vì
		# trả ra số phút rảnh âm.
		ranh = max(0.0, tong - ban)
		m["total_minutes"] = round(tong)
		m["free_minutes"] = round(ranh)
		m["free_percent"] = round(ranh / tong * 100) if tong else 0
		tong_doi += tong
		ranh_doi += ranh

	return {
		"free_time": {
			"total_minutes": round(tong_doi),
			"free_minutes": round(ranh_doi),
			"free_percent": round(ranh_doi / tong_doi * 100) if tong_doi else 0,
		}
	}


def _assert_employees_permitted(employees):
	"""Chặn tạo lịch cho nhân sự ngoài phạm vi user được phép.

	Danh sách nhân sự do CLIENT gửi lên, nên không được tin: người dùng sửa được nó ngay
	trên trình duyệt. Đối chiếu với đúng tập `frappe.get_list` trả về dưới quyền user đó.

	⚠ Giao rỗng thì phải CHẶN, tuyệt đối không coi là "không lọc" rồi cho qua hết —
	đó là đường lách quyền dễ nhất.
	"""
	if not employees:
		return

	permitted = set(
		frappe.get_list(
			"Employee",
			filters={"name": ["in", list(employees)]},
			pluck="name",
			limit_page_length=0,
		)
	)
	outside = [e for e in employees if e not in permitted]
	if outside:
		frappe.throw(
			_("Bạn không có quyền tạo lịch cho nhân sự: {0}").format(frappe.bold(", ".join(outside))),
			frappe.PermissionError,
		)


def _dates_in_range(from_date, to_date, weekdays):
	"""Các ngày trong khoảng khớp thứ đã chọn. `weekdays` theo chuẩn JS (CN=0)."""
	allowed = {cint(d) for d in weekdays}
	cursor = getdate(from_date)
	last = getdate(to_date)
	result = []
	while cursor <= last:
		if JS_DOW_BY_PYTHON[cursor.weekday()] in allowed:
			result.append(cursor)
		cursor = add_days(cursor, 1)
	return result


@frappe.whitelist()
def bulk_create_schedule(
	work_team,
	from_date,
	to_date,
	weekdays,
	employees,
	shift_type=None,
	is_over_time=0,
	start=None,
	end=None,
):
	"""Tạo hàng loạt Lịch làm việc cho các nhân sự được chọn, trong khoảng ngày + thứ đã chọn.

	Tạo **từng bản ghi một** qua `insert()` chứ không chèn thẳng SQL, để validate chống trùng
	của Employee Schedule chạy đủ. Bản ghi trùng thì bỏ qua đúng dòng đó và báo lại danh sách,
	không để một dòng làm hỏng cả lô — phân ca tuần sau chồng lên vài ngày đã tạo là chuyện
	thường ngày.
	"""
	frappe.has_permission("Employee Schedule", "create", throw=True)

	weekdays = _as_list(weekdays)
	employees = _as_list(employees)
	is_over_time = cint(is_over_time)

	if not employees:
		frappe.throw(_("Chưa chọn nhân sự nào"))
	if not weekdays:
		frappe.throw(_("Chưa chọn thứ nào trong tuần"))

	# Danh sách nhân sự đến từ client — phải soi lại theo quyền của chính user gọi.
	_assert_employees_permitted(employees)
	if getdate(to_date) < getdate(from_date):
		frappe.throw(_("Đến Ngày phải từ Từ Ngày trở đi"))

	span = (getdate(to_date) - getdate(from_date)).days + 1
	if span > MAX_RANGE_DAYS:
		frappe.throw(
			_("Khoảng {0} ngày, vượt quá {1} ngày cho phép").format(span, MAX_RANGE_DAYS)
		)

	if is_over_time:
		if not (start and end):
			frappe.throw(_("Tăng ca phải nhập Bắt Đầu và Kết Thúc"))
	elif not shift_type:
		frappe.throw(_("Vui lòng chọn Ca Làm Việc"))

	dates = _dates_in_range(from_date, to_date, weekdays)
	if not dates:
		frappe.throw(_("Không ngày nào trong khoảng khớp thứ đã chọn"))

	# Tự tra giờ từ Ca Làm Việc thay vì trông vào `fetch_from`: fetch chỉ chạy trong `_validate()`,
	# tức là SAU `validate()` của Employee Schedule — mà `validate()` lại cần start/end để tính
	# start_time/end_time. Tạo bằng script mà để trống là hỏng ngay.
	if not is_over_time:
		shift = frappe.db.get_value("Shift Type", shift_type, ["start_time", "end_time"], as_dict=True)
		if not shift:
			frappe.throw(_("Không tìm thấy Ca Làm Việc {0}").format(frappe.bold(shift_type)))
		start, end = shift.start_time, shift.end_time

	created, skipped = [], []
	for date in dates:
		for employee in employees:
			payload = {
				"doctype": "Employee Schedule",
				"employee_name": employee,
				"date": date,
				"is_over_time": is_over_time,
				"start": start,
				"end": end,
			}
			if not is_over_time:
				payload["shift_type"] = shift_type

			# Savepoint cho từng dòng: insert lỗi mà không rollback thì cả transaction
			# bị hỏng, các dòng sau cũng chết theo dù dữ liệu hợp lệ.
			save_point = "hkled_bulk_schedule"
			frappe.db.savepoint(save_point)

			# `frappe.throw` của validate GHI VÀO message_log TRƯỚC KHI raise. Nuốt exception
			# không xoá được message đó — nó vẫn theo response về trình duyệt. Không cắt lại
			# thì phân ca chồng 1 tuần là người dùng lãnh nguyên bức tường mấy chục dòng lỗi
			# thay vì một dòng tóm tắt. Lỗi này chỉ lộ ra khi test trên giao diện thật.
			log_depth = len(frappe.local.message_log or [])
			try:
				doc = frappe.get_doc(payload)
				doc.insert(ignore_permissions=True)
				created.append(doc.name)
			except Exception as exc:
				frappe.db.rollback(save_point=save_point)
				frappe.local.message_log = (frappe.local.message_log or [])[:log_depth]
				skipped.append(
					{
						"employee": employee,
						"date": str(date),
						"ly_do": str(exc)[:160],
					}
				)

	return {
		"created": len(created),
		"skipped": skipped,
		"so_ngay": len(dates),
		"so_nhan_su": len(employees),
	}
