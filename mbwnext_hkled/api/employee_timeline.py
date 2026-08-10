# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Dữ liệu cho màn hình "Tình hình làm việc của nhân sự" (PM-FEAT-00009, PM-TASK-00051/00053).

Toàn bộ phần khó của tính năng nằm ở ĐÂY, không nằm ở phần vẽ:

`Employee Allocation` KHÔNG phải là các đoạn làm việc thật. Mỗi cặp (nhân sự, Lệnh sản xuất) chỉ có
MỘT bản ghi, `start_time`/`end_time` là hai đầu mút của cả quá trình tham gia — xem
`api/work_order_schedule.py::sync_employee_allocation`. Khoảng đó **bao trùm cả giờ nghỉ trưa và ban
đêm**: trên site có bản ghi chạy từ 29/07 08:00 tới 30/07 08:28.

Vẽ thẳng bản ghi đó lên trục giờ sẽ tô "đang làm việc" vào lúc 12h trưa và 3h sáng. Nên:

    Đoạn BẬN  = Employee Allocation  ∩  Employee Schedule
    Đoạn RẢNH = Employee Schedule    −  Employee Allocation
    Vùng XÁM  = ngoài mọi Employee Schedule (phần nền, không phải đoạn)

⚠ Dùng `frappe.get_list` chứ KHÔNG dùng `frappe.get_all`: chỉ `get_list` mới áp User Permission.
Đây đúng loại dữ liệu đã gây lỗi rò rỉ nhân sự ở PM-FEAT-00008 (dialog chọn đội trả về cả người
ngoài quyền). `frappe.has_permission` không cứu được vì nó chỉ trả lời "có được xem loại dữ liệu
này không", không trả lời "được xem những bản ghi nào".

## Trục thời gian nhiều ngày (PM-TASK-00053)

Mỗi ngày là một dải 08:00–24:00 (960 phút) NỐI LIỀN nhau, bỏ hẳn khoảng 00:00–08:00 vì không ai
làm việc. Chọn 3 ngày thì trục dài 2880 phút, không phải 3×24h = 4320.

Cắt bỏ phần đêm giữ cho thanh của một ca vẫn đủ rộng để nhìn: 7 ngày mà tính cả đêm thì mỗi ca
3h45 chỉ còn khoảng 2/3 bề rộng so với cách này.
"""

from datetime import datetime, time, timedelta

import frappe
from frappe import _
from frappe.utils import add_days, getdate

# Khung giờ hiển thị trong MỘT ngày — cố định 08:00 → 24:00 (chốt C3, 08/08/2026).
GIO_TU = 8 * 60
GIO_DEN = 24 * 60
PHUT_MOI_NGAY = GIO_DEN - GIO_TU

# Chặn khoảng quá dài: 31 ngày đã là 2 dòng ngày trên đầu biểu đồ và mỗi ca chỉ còn vài pixel.
# Cho chọn rộng hơn nữa thì màn hình vô dụng mà truy vấn cũng nặng thêm vô ích.
MAX_NGAY = 31

# ⚠ Options thật trên site là "Công nhân / Bán hàng / Kế toán" (chữ n THƯỜNG), khác tài liệu
# nghiệp vụ viết hoa "Công Nhân". So sai chuỗi thì biểu đồ trống trơn mà không báo lỗi gì.
CONG_NHAN = "Công nhân"


def _hhmm(phut_trong_ngay):
	return f"{int(phut_trong_ngay) // 60:02d}:{int(phut_trong_ngay) % 60:02d}"


def _giao(a_tu, a_den, b_tu, b_den):
	"""Phần giao của hai khoảng thời gian, None nếu rời nhau."""
	tu = max(a_tu, b_tu)
	den = min(a_den, b_den)
	return (tu, den) if den > tu else None


@frappe.whitelist()
def get_timeline(from_date=None, to_date=None, work_teams=None):
	"""Dữ liệu đã tính sẵn cho biểu đồ, từ `from_date` đến `to_date` (bao gồm cả hai đầu).

	:param from_date: ngày bắt đầu (mặc định hôm nay)
	:param to_date: ngày kết thúc (mặc định bằng `from_date`)
	:param work_teams: JSON list mã Đội Sản Xuất. Rỗng = tất cả công nhân (chốt C2).
	"""
	ngay_dau = getdate(from_date) if from_date else getdate()
	ngay_cuoi = getdate(to_date) if to_date else ngay_dau
	if ngay_cuoi < ngay_dau:
		ngay_dau, ngay_cuoi = ngay_cuoi, ngay_dau

	so_ngay = (ngay_cuoi - ngay_dau).days + 1
	if so_ngay > MAX_NGAY:
		frappe.throw(
			_("Khoảng ngày tối đa là {0} ngày. Đang chọn {1} ngày.").format(MAX_NGAY, so_ngay)
		)

	doi_chon = frappe.parse_json(work_teams) if work_teams else []

	moc_dau = datetime.combine(ngay_dau, time.min)
	het_cuoi = datetime.combine(ngay_cuoi, time.min) + timedelta(days=1)

	# ── Nhân sự ──────────────────────────────────────────────────────────────
	# Chốt C2 (08/08): chỉ Loại Nhân Sự = "Công nhân". Người KHÔNG có lịch vẫn hiện.
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

	cac_ngay = []
	for i in range(so_ngay):
		ng = add_days(ngay_dau, i)
		cac_ngay.append(
			{
				"ngay": str(ng),
				"nhan": ng.strftime("%d/%m"),
				"tu_phut": i * PHUT_MOI_NGAY,
				"den_phut": (i + 1) * PHUT_MOI_NGAY,
			}
		)

	khung = {
		"tu_ngay": str(ngay_dau),
		"den_ngay": str(ngay_cuoi),
		"so_ngay": so_ngay,
		"truc_tu": 0,
		"truc_den": so_ngay * PHUT_MOI_NGAY,
		"cac_ngay": cac_ngay,
		"gio_tu": GIO_TU,
		"gio_den": GIO_DEN,
	}
	if not nhan_su:
		khung["nhan_su"] = []
		return khung

	ma_nhan_su = []
	for e in nhan_su:
		ma_nhan_su.append(e.name)

	# ── Lịch làm việc trong khoảng ───────────────────────────────────────────
	lich = frappe.get_list(
		"Employee Schedule",
		filters={
			"employee_name": ["in", ma_nhan_su],
			"date": ["between", [str(ngay_dau), str(ngay_cuoi)]],
		},
		fields=["employee_name", "date", "shift_type", "is_over_time", "start_time", "end_time"],
		order_by="start_time asc",
		limit_page_length=0,
	)

	# ── Phân công GIAO với khoảng ────────────────────────────────────────────
	# Điều kiện giao khoảng, KHÔNG phải `date = ngay`: một bản ghi có thể trải nhiều ngày.
	# Không cần lọc trạng thái Lệnh sản xuất — PM-TASK-00045 đã dọn tại nguồn nên bảng luôn sạch.
	phan_cong = frappe.get_list(
		"Employee Allocation",
		filters={
			"employee_name": ["in", ma_nhan_su],
			"start_time": ["<", het_cuoi],
			"end_time": [">", moc_dau],
		},
		fields=["employee_name", "work_order", "start_time", "end_time"],
		order_by="start_time asc",
		limit_page_length=0,
	)

	# Thông tin Lệnh sản xuất cho tooltip (PM-TASK-00051 thêm Khách Hàng + Nhân Viên Bán Hàng).
	# Hai trường đó đã có sẵn trên Work Order từ PM-TASK-00050 nên chỉ cần đọc thêm, KHÔNG truy
	# ngược sang Đơn Bán Hàng.
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

	chi_so_ngay = {}
	for i, m in enumerate(cac_ngay):
		chi_so_ngay[m["ngay"]] = i

	ket_qua = []
	for e in nhan_su:
		ket_qua.append(
			_dung_dong(
				e,
				lich_theo_nguoi.get(e.name, []),
				pc_theo_nguoi.get(e.name, []),
				thong_tin_lenh,
				chi_so_ngay,
			)
		)

	khung["nhan_su"] = ket_qua
	return khung


def _dung_dong(nhan_vien, cac_ca, cac_pc, thong_tin_lenh, chi_so_ngay):
	"""Dựng nền ca + các đoạn bận/rảnh + tổng kết thời gian rảnh cho MỘT nhân sự."""
	nen_ca = []
	doan = []
	tong_phut = 0.0
	ban_phut = 0.0

	for ca in cac_ca:
		idx = chi_so_ngay.get(str(getdate(ca.date)))
		if idx is None:
			continue
		goc = idx * PHUT_MOI_NGAY

		def _vi_tri(dt, _goc=goc):
			"""Đổi mốc thời gian thật thành vị trí trên trục, cắt vào khung giờ của ngày đó."""
			phut = dt.hour * 60 + dt.minute + dt.second / 60.0
			return _goc + max(GIO_TU, min(GIO_DEN, phut)) - GIO_TU

		ca_tu = _vi_tri(ca.start_time)
		ca_den = _vi_tri(ca.end_time)
		if ca_den <= ca_tu:
			continue  # ca nằm hoàn toàn ngoài khung 08:00–24:00

		nen_ca.append({"tu_phut": ca_tu, "den_phut": ca_den})
		tong_phut += ca_den - ca_tu

		ban = []
		for pc in cac_pc:
			g = _giao(ca.start_time, ca.end_time, pc.start_time, pc.end_time)
			if g:
				ban.append((_vi_tri(g[0]), _vi_tri(g[1]), pc))
		ban.sort(key=lambda x: x[0])

		con_tro = ca_tu
		for tu, den, pc in ban:
			if tu > con_tro:
				doan.append(_doan_ranh(con_tro, tu, goc, ca))
			wo = thong_tin_lenh.get(pc.work_order) or {}
			# Hai phân công chồng nhau (dữ liệu hỏng) thì cắt về con_tro thay vì vẽ đè lên nhau —
			# nhìn ra ngay là có gì đó sai, thay vì im lặng chồng thanh.
			tu_that = max(tu, con_tro)
			if den - tu_that >= 0.5:
				doan.append(
					{
						"loai": "ban",
						"tu_phut": tu_that,
						"den_phut": den,
						"tu": _hhmm(tu_that - goc + GIO_TU),
						"den": _hhmm(den - goc + GIO_TU),
						"ngay": str(getdate(ca.date)),
						"work_order": pc.work_order,
						"mat_hang": wo.get("production_item"),
						"so_luong": wo.get("qty"),
						"trang_thai": wo.get("status"),
						"khach_hang": wo.get("custom_customer"),
						"nhan_vien_ban": wo.get("custom_sales_person"),
						"ca": ca.shift_type,
					}
				)
				ban_phut += den - tu_that
			con_tro = max(con_tro, den)

		if con_tro < ca_den:
			doan.append(_doan_ranh(con_tro, ca_den, goc, ca))

	doan = [d for d in doan if d]
	ranh_phut = max(0.0, tong_phut - ban_phut)

	return {
		"employee": nhan_vien.name,
		"ten": nhan_vien.employee_name or nhan_vien.name,
		"bac_tho": nhan_vien.bac_tho,
		"doi": nhan_vien.doi,
		"co_lich": bool(nen_ca),
		"nen_ca": nen_ca,
		"doan": doan,
		# PM-TASK-00053: tổng kết cho cột bên trái — rảnh / tổng (%)
		"tong_phut": round(tong_phut),
		"ranh_phut": round(ranh_phut),
		"ranh_phan_tram": round(ranh_phut / tong_phut * 100) if tong_phut else 0,
	}


def _doan_ranh(tu, den, goc, ca):
	if den - tu < 0.5:  # dưới nửa phút thì không vẽ nổi, bỏ cho đỡ rác
		return None
	return {
		"loai": "ranh",
		"tu_phut": tu,
		"den_phut": den,
		"tu": _hhmm(tu - goc + GIO_TU),
		"den": _hhmm(den - goc + GIO_TU),
		"ngay": str(getdate(ca.date)),
		"ca": ca.shift_type,
		"tang_ca": bool(ca.is_over_time),
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
