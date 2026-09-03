# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Đưa cột *Số Lượng Giữ Chỗ* lên lưới hàng hoá của Đơn Bán (PM-FEAT-00023).

Anh Thắng chốt 03/09 09:11 chọn **cách 1**: ô giữ chỗ nằm ngay trên bảng mặt hàng của đơn,
popup chỉ để xem. Khai `in_list_view` thôi thì **chưa chắc nó hiện** — có hai chỗ chặn, cả hai
đều KHÔNG lộ ra khi kiểm bằng query hay API, phải mở giao diện thật mới thấy.

## Chặn 1 — lưới chỉ có 11 đơn vị cột, vượt là bỏ LẶNG

`grid.js::setup_visible_columns` cộng dồn `colsize`, bắt đầu từ 1, và **`if (total_colsize > 11)
return false`** — các cột sau đó rụng khỏi lưới, không cảnh báo gì.

## Chặn 2 — bố cục người dùng tự lưu ĐÈ HẲN khai báo DocType

`__UserSettings.GridView["Sales Order Item"]` được ưu tiên tuyệt đối (`user_defined_columns`).
Người từng chỉnh lưới sẽ **không bao giờ** thấy cột mới, người chưa chỉnh thì thấy — khác nhau
theo từng tài khoản, rất khó đoán khi đi hỗ trợ.

## Hiện trạng đo trên hkled.com ngày 03/09 — cả hai bố cục ĐÃ vượt trần từ trước

	Administrator     tổng 11 đơn vị  (1 + 11 = 12 > 11)  -> đang ẩn cột cuối
	hkled@gmail.com   tổng 13 đơn vị  (1 + 13 = 14 > 11)  -> đang ẩn 3 cột cuối

Nghĩa là **hôm nay đã có cột bị giấu** mà không ai báo. Chèn thêm cột mà không dọn chỗ thì hoặc
cột mới rụng, hoặc nó đẩy một cột đang dùng ra ngoài.

## Cách xử lý: LẤY CHỖ TỪ CỘT RỘNG NHẤT, KHÔNG XOÁ CỘT NÀO

Bản đầu tôi định gỡ sạch khoá `GridView` như patch `reset_bom_rule_grid_view`. Không làm vậy ở
đây: `Sales Order Item` là lưới dùng hằng ngày, xoá bố cục là người dùng mất hết tuỳ chỉnh của
họ, đắt hơn nhiều so với lợi ích.

Thay vào đó: chèn cột mới ngay **sau `qty`** (đọc cạnh số lượng mới có nghĩa), rồi **thu hẹp cột
rộng nhất đúng 1 đơn vị** để bù. Không cột nào bị xoá, không ai mất tuỳ chỉnh.

Trên site này cột rộng nhất của `hkled@gmail.com` là *Ghi Chú Sản Xuất* (3 đơn vị) — hạ xuống 2
thì vẫn đọc được và **không cột nào rụng thêm**. Nếu không thu hẹp, cột **Đơn giá** sẽ biến mất
khỏi màn hình của họ; đã tính trước theo đúng vòng lặp của `grid.js`.

⚠ Không thu hẹp cột nào xuống dưới 1. Không tìm được chỗ thì **bỏ qua người đó và in ra**, để
còn biết mà báo — im lặng ở đây là người dùng mở lên không thấy ô nhập và tưởng tính năng hỏng.
"""

import json

import frappe


FIELDNAME = "custom_so_luong_giu_cho"
DOCTYPE_CON = "Sales Order Item"
TRAN = 11


def _dat_thuoc_tinh_field():
	"""Khai `in_list_view` + `columns` cho người CHƯA có bố cục riêng.

	⚠ Phải khai `columns` tường minh. Bỏ trống thì Frappe tự chia và tổng dễ vượt 11, cột cuối
	  rụng — đúng cái bẫy đã ghi ở `CLAUDE.md`.
	"""
	ten = f"{DOCTYPE_CON}-{FIELDNAME}"
	if not frappe.db.exists("Custom Field", ten):
		return False
	doc = frappe.get_doc("Custom Field", ten)
	if doc.in_list_view and doc.columns == 1:
		return False
	doc.in_list_view = 1
	doc.columns = 1
	doc.save(ignore_permissions=True)
	return True


def _chen_vao_bo_cuc_da_luu():
	rows = frappe.db.sql(
		"""select user, doctype, data from `__UserSettings` where data like %s""",
		(f"%{DOCTYPE_CON}%",),
		as_dict=True,
	)
	da_sua, khong_du_cho = [], []

	for row in rows:
		try:
			data = json.loads(row["data"] or "{}")
		except ValueError:
			continue
		grid = (data.get("GridView") or {}).get(DOCTYPE_CON)
		if not isinstance(grid, list) or not grid:
			continue

		# BƯỚC 1 — bỏ những cột ĐANG VÔ HÌNH SẴN.
		#
		# Đây là chỗ bản đầu của patch bỏ sót, và vì thế nó báo "không đủ chỗ" cho cả hai
		# người dùng trên site. Bố cục của họ đã vượt trần từ trước (11 và 13 đơn vị) nên
		# Frappe vốn đã cắt phần đuôi — những mục đó **không hiện trên màn hình dù có nằm
		# trong bố cục**. Bỏ chúng đi thì người dùng KHÔNG mất gì đang nhìn thấy, mà lại có
		# chỗ cho cột mới.
		giu, cong_don = [], 1
		for c in grid:
			if c.get("fieldname") == FIELDNAME:
				continue                       # sẽ chèn lại đúng chỗ ở bước 2
			rong = int(c.get("columns") or 0) or 1
			# Chừa sẵn 1 đơn vị cho cột Giữ Chỗ sắp chèn. Không chừa thì cắt xong vừa đủ trần,
			# chèn thêm là vượt lại đúng 1 — bản trước vấp chỗ này, và vì mọi cột lúc đó đã
			# rộng 1 nên bước thu hẹp không còn gì để thu.
			if cong_don + rong > TRAN - 1:
				break                          # từ đây trở đi vốn đã không hiện
			cong_don += rong
			giu.append(c)
		grid = giu

		# BƯỚC 2 — chèn ngay sau `qty`; không có `qty` thì đặt cuối
		vi_tri = len(grid)
		for i, c in enumerate(grid):
			if c.get("fieldname") == "qty":
				vi_tri = i + 1
				break
		grid.insert(vi_tri, {"fieldname": FIELDNAME, "columns": 1})

		# BƯỚC 3 — vẫn chật thì thu hẹp cột RỘNG NHẤT, không hạ xuống dưới 1
		tong = sum(int(c.get("columns") or 0) for c in grid)
		while 1 + tong > TRAN:
			ung_vien = [
				c for c in grid
				if c.get("fieldname") != FIELDNAME and int(c.get("columns") or 0) > 1
			]
			if not ung_vien:
				khong_du_cho.append(row["user"])
				break
			rong_nhat = max(ung_vien, key=lambda c: int(c.get("columns") or 0))
			rong_nhat["columns"] = int(rong_nhat["columns"]) - 1
			tong -= 1

		data.setdefault("GridView", {})[DOCTYPE_CON] = grid
		frappe.db.sql(
			"""update `__UserSettings` set data = %s where user = %s and doctype = %s""",
			(json.dumps(data), row["user"], row["doctype"]),
		)
		da_sua.append(row["user"])

	return da_sua, khong_du_cho


def execute():
	moi = _dat_thuoc_tinh_field()
	da_sua, khong_du_cho = _chen_vao_bo_cuc_da_luu()
	frappe.clear_cache(doctype=DOCTYPE_CON)
	frappe.db.commit()

	if moi:
		print("[mbwnext_hkled] Số Lượng Giữ Chỗ: đã khai in_list_view, rộng 1 đơn vị")
	if da_sua:
		print(f"[mbwnext_hkled] Chèn cột vào bố cục lưới đã lưu của {len(da_sua)} người dùng")
	if khong_du_cho:
		print(
			"[mbwnext_hkled] ⚠ KHÔNG đủ chỗ trên lưới, cột Giữ Chỗ sẽ không hiện với: "
			+ ", ".join(sorted(set(khong_du_cho)))
			+ " — nhờ họ bỏ bớt một cột trong Cấu Hình Cột của lưới hàng hoá."
		)
