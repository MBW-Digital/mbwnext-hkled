# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Dữ liệu cho màn hình "Tình hình làm việc của nhân sự" (PM-FEAT-00009).

Toàn bộ phần khó của tính năng nằm ở ĐÂY, không nằm ở phần vẽ:

`Employee Allocation` KHÔNG phải là các đoạn làm việc thật. Mỗi cặp (nhân sự, Lệnh sản xuất) chỉ có
MỘT bản ghi, `start_time`/`end_time` là hai đầu mút của cả quá trình tham gia — xem
`api/work_order_schedule.py::sync_employee_allocation`. Khoảng đó **bao trùm cả giờ nghỉ trưa và ban
đêm**: trên site có bản ghi chạy từ 29/07 08:00 tới 30/07 08:28.

Vẽ thẳng bản ghi đó lên trục giờ sẽ tô "đang làm việc" vào lúc 12h trưa và 3h sáng. Nên:

    Đoạn BẬN  = Employee Allocation  ∩  Employee Schedule
    Đoạn RẢNH = Employee Schedule    −  Employee Allocation
    Vùng XÁM  = ngoài mọi Employee Schedule của ngày (phần nền, không phải đoạn)

⚠ Dùng `frappe.get_list` chứ KHÔNG dùng `frappe.get_all`: chỉ `get_list` mới áp User Permission.
Đây đúng loại dữ liệu đã gây lỗi rò rỉ nhân sự ở PM-FEAT-00008 (dialog chọn đội trả về cả người
ngoài quyền). `frappe.has_permission` không cứu được vì nó chỉ trả lời "có được xem loại dữ liệu
này không", không trả lời "được xem những bản ghi nào".
"""

from datetime import datetime, time, timedelta

import frappe
from frappe import _
from frappe.utils import getdate

# Trục giờ cố định 08:00 → 24:00 (chốt C3, 08/08/2026). Không co giãn theo dữ liệu.
TRUC_TU = 8 * 60
TRUC_DEN = 24 * 60

# ⚠ Options thật trên site là "Công nhân / Bán hàng / Kế toán" (chữ n THƯỜNG), khác tài liệu
# nghiệp vụ viết hoa "Công Nhân". So sai chuỗi thì biểu đồ trống trơn mà không báo lỗi gì.
CONG_NHAN = "Công nhân"


def _phut(dt, moc_ngay):
	"""Số phút tính từ 00:00 của ngày đang xem. Cắt vào trong trục giờ."""
	delta = (dt - moc_ngay).total_seconds() / 60.0
	return max(TRUC_TU, min(TRUC_DEN, delta))


def _hhmm(phut):
	return f"{int(phut) // 60:02d}:{int(phut) % 60:02d}"


def _giao(a_tu, a_den, b_tu, b_den):
	"""Phần giao của hai khoảng, None nếu không giao nhau."""
	tu = max(a_tu, b_tu)
	den = min(a_den, b_den)
	return (tu, den) if den > tu else None


def _doan(loai, tu, den, **extra):
	if den - tu < 0.5:  # dưới nửa phút thì không vẽ nổi, bỏ cho đỡ rác
		return None
	return {"loai": loai, "tu": _hhmm(tu), "den": _hhmm(den), "tu_phut": tu, "den_phut": den, **extra}


@frappe.whitelist()
def get_timeline(date=None, work_teams=None):
	"""Trả về dữ liệu đã tính sẵn cho biểu đồ của MỘT ngày.

	:param date: ngày cần xem (mặc định hôm nay)
	:param work_teams: JSON list mã Đội Sản Xuất. Rỗng/không truyền = tất cả công nhân (chốt C2).
	"""
	ngay = getdate(date) if date else getdate()
	doi_chon = frappe.parse_json(work_teams) if work_teams else []

	moc_ngay = datetime.combine(ngay, time.min)
	het_ngay = moc_ngay + timedelta(days=1)

	# ── Nhân sự ──────────────────────────────────────────────────────────────
	# Chốt C2 (08/08): chỉ Loại Nhân Sự = "Công nhân". Người KHÔNG có lịch ngày đó vẫn hiện,
	# nên không lọc theo lịch ở đây.
	loc = {"status": "Active", "custom_employee_type": CONG_NHAN}
	if doi_chon:
		loc["custom_work_team"] = ["in", doi_chon]

	nhan_su = frappe.get_list(
		"Employee",
		filters=loc,
		fields=[
			"name",
			"employee_name",
			"custom_employee_level as bac_tho",
			"custom_work_team as doi",
		],
		order_by="employee_name asc",
		limit_page_length=0,
	)
	if not nhan_su:
		return {"ngay": str(ngay), "truc_tu": TRUC_TU, "truc_den": TRUC_DEN, "nhan_su": []}

	ma_nhan_su = [e.name for e in nhan_su]

	# ── Lịch làm việc của đúng ngày đó ───────────────────────────────────────
	lich = frappe.get_list(
		"Employee Schedule",
		filters={"employee_name": ["in", ma_nhan_su], "date": ngay},
		fields=["employee_name", "shift_type", "is_over_time", "start_time", "end_time"],
		order_by="start_time asc",
		limit_page_length=0,
	)

	# ── Phân công GIAO với ngày đó ───────────────────────────────────────────
	# Điều kiện giao khoảng, KHÔNG phải `date = ngay`: một bản ghi có thể trải nhiều ngày.
	# Không cần lọc trạng thái Lệnh sản xuất — PM-TASK-00045 đã dọn tại nguồn (hook on_cancel/
	# on_trash), nên bảng này luôn sạch. Lọc thêm ở đây là vá triệu chứng và che lỗi ở engine.
	phan_cong = frappe.get_list(
		"Employee Allocation",
		filters={
			"employee_name": ["in", ma_nhan_su],
			"start_time": ["<", het_ngay],
			"end_time": [">", moc_ngay],
		},
		fields=["employee_name", "work_order", "start_time", "end_time"],
		order_by="start_time asc",
		limit_page_length=0,
	)

	# Thông tin Lệnh sản xuất để hiện khi rê chuột. get_list để tôn trọng quyền: người không được
	# xem Lệnh sản xuất thì chỉ thấy mã, không thấy mặt hàng/số lượng.
	#
	# PM-TASK-00051: thêm Khách Hàng và Nhân Viên Bán Hàng. Hai trường này đã có sẵn trên Work Order
	# từ PM-TASK-00050 nên chỉ cần đọc thêm, KHÔNG truy ngược sang Đơn Bán Hàng.
	ma_lenh = list({p.work_order for p in phan_cong if p.work_order})
	thong_tin_lenh = {}
	if ma_lenh:
		for wo in frappe.get_list(
			"Work Order",
			filters={"name": ["in", ma_lenh]},
			fields=[
				"name",
				"production_item",
				"qty",
				"status",
				"custom_customer",
				"custom_sales_person",
			],
			limit_page_length=0,
		):
			thong_tin_lenh[wo.name] = wo

	lich_theo_nguoi = {}
	for row in lich:
		lich_theo_nguoi.setdefault(row.employee_name, []).append(row)

	pc_theo_nguoi = {}
	for row in phan_cong:
		pc_theo_nguoi.setdefault(row.employee_name, []).append(row)

	# ── Dựng đoạn cho từng người ─────────────────────────────────────────────
	ket_qua = []
	for e in nhan_su:
		cac_ca = lich_theo_nguoi.get(e.name, [])
		cac_pc = pc_theo_nguoi.get(e.name, [])

		nen_ca = []
		doan = []

		for ca in cac_ca:
			ca_tu = _phut(ca.start_time, moc_ngay)
			ca_den = _phut(ca.end_time, moc_ngay)
			if ca_den <= ca_tu:
				continue  # ca nằm hoàn toàn ngoài trục 08:00–24:00

			nen_ca.append({"tu": _hhmm(ca_tu), "den": _hhmm(ca_den), "tu_phut": ca_tu, "den_phut": ca_den})

			ban = []
			for pc in cac_pc:
				g = _giao(ca.start_time, ca.end_time, pc.start_time, pc.end_time)
				if g:
					ban.append((_phut(g[0], moc_ngay), _phut(g[1], moc_ngay), pc))
			ban.sort(key=lambda x: x[0])

			con_tro = ca_tu
			for tu, den, pc in ban:
				if tu > con_tro:
					d = _doan("ranh", con_tro, tu, ca=ca.shift_type, tang_ca=bool(ca.is_over_time))
					if d:
						doan.append(d)
				wo = thong_tin_lenh.get(pc.work_order) or {}
				# Hai phân công chồng nhau (dữ liệu hỏng) thì đoạn sau bị cắt về con_tro thay vì
				# vẽ đè lên nhau — nhìn ra ngay là có gì đó sai, thay vì im lặng chồng thanh.
				d = _doan(
					"ban",
					max(tu, con_tro),
					den,
					work_order=pc.work_order,
					mat_hang=wo.get("production_item"),
					so_luong=wo.get("qty"),
					trang_thai=wo.get("status"),
					khach_hang=wo.get("custom_customer"),
					nhan_vien_ban=wo.get("custom_sales_person"),
					ca=ca.shift_type,
				)
				if d:
					doan.append(d)
				con_tro = max(con_tro, den)

			if con_tro < ca_den:
				d = _doan("ranh", con_tro, ca_den, ca=ca.shift_type, tang_ca=bool(ca.is_over_time))
				if d:
					doan.append(d)

		ket_qua.append(
			{
				"employee": e.name,
				"ten": e.employee_name or e.name,
				"bac_tho": e.bac_tho,
				"doi": e.doi,
				"co_lich": bool(nen_ca),
				"nen_ca": nen_ca,
				"doan": doan,
			}
		)

	return {
		"ngay": str(ngay),
		"truc_tu": TRUC_TU,
		"truc_den": TRUC_DEN,
		"nhan_su": ket_qua,
	}


@frappe.whitelist()
def get_work_teams():
	"""Danh sách Đội Sản Xuất đang hoạt động, cho ô lọc nhiều lựa chọn."""
	return frappe.get_list(
		"Work Team",
		filters={"is_active": 1},
		fields=["name"],
		order_by="name asc",
		limit_page_length=0,
	)
