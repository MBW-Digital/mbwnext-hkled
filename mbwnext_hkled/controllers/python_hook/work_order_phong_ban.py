# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""PM-TASK-00143 — Lệnh Sản Xuất thừa hưởng Phòng Ban từ dòng Kế Hoạch Sản Xuất sinh ra nó.

🔒 **Anh Thắng chốt 07/09/2026 10:27:**

> *"mình sẽ dùng luôn Phòng ban của ERPNext lõi. Khách chốt lại là ở phần kế hoạch sản xuất
> mình chỉ cần ghi nhận phòng ban nào thực hiện sản xuất mặt hàng nào thôi, không cần gán đội
> sản xuất nữa. Khi tạo lệnh sản xuất thì các trưởng phòng ban sẽ tự vào lệnh sản xuất để phân
> đội em nhé. đối với thành phẩm chính mình sẽ gán phòng ban ở bảng Assembly Items em nhé"*

Vì sao file riêng chứ không viết thêm vào `python_hook/work_order.py`:
`work_order.py` là phần của cửa sổ Claude khác (Phần II–III, PM-FEAT-00008/00023). Bảng giành
việc `PHOI-HOP-CLAUDE.md` ghi rõ file đó do họ giữ. Tách file thì hai bên sửa song song không
đụng nhau, và nếu phải gỡ tính năng này thì chỉ cần bỏ một dòng trong `hooks.py`.

⚠ **KHÔNG đụng `ensure_start_time` của họ.** Hàm đó đang có lỗi `NameError: work_team` ở khối
273–286 (đo 07/09: chạy thật ra lỗi trên 2 ca) và việc sửa nó thuộc về họ, vì sửa xong sẽ bật
một tính năng chết — WO tự điền công nhân — kéo theo `Employee Allocation` và làm đổi số Bảng 3
của một tính năng đã nghiệm thu. Hook dưới đây chạy độc lập, không phụ thuộc hàm đó chạy hay nổ.
"""

import frappe

# "Bảng Assembly Items" theo cách anh Thắng gọi chính là `po_items` — nhãn trên màn hình của nó
# đúng là *Assembly Items*, và nó chứa THÀNH PHẨM CHÍNH. Bảng bán thành phẩm là
# `sub_assembly_items` nằm dưới mục *Sub Assembly Items*. Đã kiểm nhãn bằng meta, không đoán.
BANG_THANH_PHAM_CHINH = "Production Plan Item"
BANG_BAN_THANH_PHAM = "Production Plan Sub Assembly Item"


def _phong_ban_tu_ke_hoach(doc):
	"""Phòng ban của dòng kế hoạch đã sinh ra lệnh này; None nếu không tra được.

	Thứ tự tra giống `work_order._plan_row_for`: bán thành phẩm trước, rồi mới tới thành phẩm
	chính. Một lệnh chỉ sinh từ một trong hai, nhưng cứ theo đúng thứ tự đó cho khớp hành vi
	đã có, để hai đường không bao giờ nói khác nhau.

	⚠ `production_plan_sub_assembly_item` và `production_plan_item` đều là **Data chứa TÊN dòng**,
	không phải Link — nên tra bằng `db.get_value` theo tên. Đây là chỗ đã bẫy một lần ở
	`work_order.py` (xem chú thích PM-TASK-00046 trong hàm `inherit_from_production_plan`).
	"""
	if doc.get("production_plan_sub_assembly_item"):
		phong = frappe.db.get_value(
			BANG_BAN_THANH_PHAM, doc.production_plan_sub_assembly_item, "custom_department"
		)
		if phong:
			return phong

	if doc.get("production_plan_item"):
		phong = frappe.db.get_value(
			BANG_THANH_PHAM_CHINH, doc.production_plan_item, "custom_department"
		)
		if phong:
			return phong

	return None


def inherit_department(doc, method=None):
	"""`before_insert` — điền Phòng Ban cho lệnh mới nếu dòng kế hoạch có khai.

	Chỉ điền chỗ **còn trống**: người dùng nhập tay thì tôn trọng, cùng nguyên tắc với
	`inherit_from_production_plan` và `python_hook/sales_order.py`.

	Cố ý **không** báo lỗi khi không tra được phòng ban. Lệnh sản xuất vẫn phải tạo được như
	trước; ô trống là tín hiệu cho trưởng phòng biết chưa ai khai ở kế hoạch, chứ không phải
	lý do chặn sản xuất. Site hiện có 0/4 nhân sự và 0 dòng kế hoạch nào khai phòng ban — bắt
	buộc lúc này là chặn đứng cả nhà máy.
	"""
	if doc.doctype != "Work Order":
		return
	if doc.get("custom_department"):
		return

	phong = _phong_ban_tu_ke_hoach(doc)
	if phong:
		doc.custom_department = phong


def validate_team_in_department(doc, method=None):
	"""`validate` — Đội Sản Xuất chọn ở lệnh phải thuộc đúng Phòng Ban của lệnh.

	🔒 Anh Thắng thêm ý này ngày 03/09 14:57: *"cho Đội Sản Xuất gắn phòng ban để trưởng phòng
	chỉ chọn được đội của phòng mình"*. Màn hình đã lọc sẵn danh sách đội theo phòng, nhưng lọc
	ở màn hình chỉ là tiện tay — API và nhập liệu hàng loạt đi vòng qua được, nên chặn ở server.

	Ba trường hợp CỐ Ý cho qua, vì chặn là gây hại nhiều hơn lợi:
	  1. Lệnh chưa có phòng ban — chưa ai khai ở kế hoạch, không có gì để đối chiếu.
	  2. Đội chưa gắn phòng ban — dữ liệu cũ; 2 đội đang có trên site đều chưa gắn (đo 07/09).
	  3. Không chọn đội — phân đội là việc của trưởng phòng, làm sau, không phải điều kiện để
	     lệnh ra đời.
	Chỉ chặn khi **cả hai đều đã khai và khác nhau** — lúc đó mới thật sự là chọn nhầm.
	"""
	if doc.doctype != "Work Order":
		return
	if not doc.get("custom_work_team") or not doc.get("custom_department"):
		return

	phong_cua_doi = frappe.db.get_value("Work Team", doc.custom_work_team, "custom_department")
	if not phong_cua_doi:
		return

	if phong_cua_doi != doc.custom_department:
		frappe.throw(
			frappe._(
				"Đội <b>{0}</b> thuộc phòng <b>{1}</b>, không thuộc phòng <b>{2}</b> của lệnh này. "
				"Chọn đội của đúng phòng, hoặc sửa lại ô Phòng Ban."
			).format(doc.custom_work_team, phong_cua_doi, doc.custom_department),
			title=frappe._("Đội không thuộc phòng ban của lệnh"),
		)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def doi_theo_phong_ban(doctype, txt, searchfield, start, page_len, filters):
	"""Danh sách Đội Sản Xuất cho ô *Đội Sản Xuất* trên Lệnh sản xuất: đội của phòng này, **cộng**
	đội chưa khai phòng nào.

	🔴 **Vì sao phải là truy vấn riêng chứ không phải một dòng `filters` bình thường.**
	Bản đầu tôi viết ở JS là `["custom_department", "in", [phong, ""]]`. Nó dịch ra
	`custom_department IN ('Phòng kỹ thuật - HKL', '')`, và trong SQL **`NULL` không khớp `IN`
	bất kể trong danh sách có gì** — kể cả `NULL`. Mà cột này của các bản ghi cũ đúng là `NULL`
	chứ không phải chuỗi rỗng.

	Đo trên site 07/09 trước khi sửa: `Đội 1` và `Đội 2` đều `custom_department IS NULL`, và bộ
	lọc kia khớp **0 / 2** đội. Nghĩa là chỉ cần lệnh có Phòng Ban là ô Đội **rỗng trắng** —
	đúng thứ chú thích trong `work_order_phong_ban.js` viết ra để tránh. Dùng `ifnull(...)` thì
	khớp **2 / 2**.

	⚠ Đây là lần thứ ba cùng một cái bẫy trong ngày 07/09: nó cũng làm phép đếm "đơn trống Thời
	Gian Bắt Đầu" ra **0** trong khi thật ra là **9** (`filters={"custom_start_time": ["in",
	[None, ""]]}`). Hễ một cột có thể `NULL` mà đem so bằng `in` thì phải `ifnull` trước.
	"""
	phong = (filters or {}).get("phong_ban")
	dieu_kien = ["ifnull(wt.is_active, 0) = 1"]
	tham_so = {"txt": "%%%s%%" % (txt or ""), "start": start, "page_len": page_len}

	if phong:
		# Đội của đúng phòng này, HOẶC đội chưa khai phòng nào (dữ liệu cũ — không được giấu đi,
		# giấu là người dùng không chọn được gì mà không hiểu vì sao).
		dieu_kien.append("(wt.custom_department = %(phong)s or ifnull(wt.custom_department, '') = '')")
		tham_so["phong"] = phong

	return frappe.db.sql(
		"""select wt.name, wt.custom_department
		from `tabWork Team` wt
		where {dieu_kien} and (wt.name like %(txt)s or ifnull(wt.mo_ta, '') like %(txt)s)
		order by wt.name
		limit %(start)s, %(page_len)s""".format(dieu_kien=" and ".join(dieu_kien)),
		tham_so,
	)
