# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tạo Kế Hoạch Sản Xuất thẳng từ Đơn Bán Hàng (PM-TASK-00047).

ERPNext v15 KHÔNG có sẵn đường này: `Sales Order` không có mục Kế Hoạch Sản Xuất trong nút *Create*
(đã kiểm `erpnext/selling/doctype/sales_order/sales_order.js`). Cách làm sẵn có là mở Kế Hoạch Sản
Xuất rồi *Get Items From > Sales Order* rồi tự tìm lại đơn — đúng thứ khách muốn bỏ.

Dùng `get_mapped_doc` thay vì tự dựng doc rồi trả `as_dict()`: hàm này lo phần đặt tên tạm và cờ
`__islocal` để `frappe.model.open_mapped_doc` phía client mở được form chưa lưu, giống hệt mọi nút
Create khác của ERPNext — không phải tự chế cơ chế riêng.
"""

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

from mbwnext_hkled.controllers.python_hook.production_plan import combine_delivery_datetime


@frappe.whitelist()
def make_production_plan(source_name, target_doc=None):
	"""Đơn Bán Hàng → Kế Hoạch Sản Xuất, kéo sẵn dòng hàng và thông tin sản xuất."""

	def postprocess(source, target):
		target.company = source.company
		target.get_items_from = "Sales Order"

		# Bảng Đơn Bán Hàng của kế hoạch: điền luôn các trường sản xuất thay vì trông vào
		# `fetch_from`. Doc này CHƯA lưu nên vòng fetch của Frappe (chạy trong `_validate_links`
		# lúc insert) chưa xảy ra — người dùng sẽ thấy các ô trống ngay khi form vừa mở.
		# Cùng họ với bẫy đã ghi ở `python_hook/work_order.py`.
		target.append(
			"sales_orders",
			{
				"sales_order": source.name,
				"sales_order_date": source.transaction_date,
				"customer": source.customer,
				"grand_total": source.grand_total,
				"custom_start_time": source.get("custom_start_time"),
				"custom_required_completion_date_time": combine_delivery_datetime(
					source.get("delivery_date"), source.get("custom_time")
				),
				"custom_note": source.get("custom_note"),
			},
		)

		# Kéo dòng hàng của đơn vào bảng Assembly Items (`po_items`).
		target.get_items()

		if not target.get("po_items"):
			frappe.throw(
				_(
					"Đơn Bán Hàng {0} không có dòng hàng nào cần sản xuất. "
					"Kiểm tra lại: mặt hàng đã có Định Mức Nguyên Vật Liệu (BOM) đang hoạt động chưa, "
					"và số lượng đã được tạo Lệnh sản xuất hết chưa."
				).format(source.name)
			)

		_tru_phan_da_giu_cho(source, target)
		_fill_item_note(source, target)

	return get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Production Plan",
				"validation": {"docstatus": ["=", 1]},
			}
		},
		target_doc,
		postprocess,
	)


def _fill_item_note(source, target):
	"""Chép Ghi Chú Sản Xuất của từng dòng hàng sang đúng dòng Assembly Items (PM-TASK-00046).

	`get_so_items()` của ERPNext điền `sales_order_item` = tên dòng `Sales Order Item`, nên ghép
	được chính xác theo từng dòng chứ không phải áp chung ghi chú đầu đơn cho cả bảng.
	"""
	ghi_chu_theo_dong = {}
	for row in source.get("items") or []:
		if row.get("custom_note"):
			ghi_chu_theo_dong[row.name] = row.custom_note

	mac_dinh = source.get("custom_note")

	for row in target.get("po_items") or []:
		if row.get("custom_note"):
			continue
		row.custom_note = ghi_chu_theo_dong.get(row.get("sales_order_item")) or mac_dinh


def _tru_phan_da_giu_cho(source, target):
	"""Số lượng trên Kế Hoạch = phần CÒN THIẾU, không phải toàn bộ đơn (PM-TASK-00188).

	Anh Thắng 08/09 11:40: *"số lượng trên kế hoạch sản xuất đó chính là số lượng còn bị thiếu.
	Ví dụ tồn khả dụng của A hiện tại là 6, đơn hàng bán 10 → ghim được 6 còn thiếu 4 → tạo kế
	hoạch sản xuất số lượng 4"*.

	## Công thức, và vì sao không gọi lại `_phai_san_xuat`

	`ghim_vat_tu._phai_san_xuat()` tính đúng khái niệm này — `qty − delivered_qty − giữ chỗ` —
	nhưng **không dùng lại được ở đây**, vì hai chỗ hỏi hai câu khác nhau:

	- Hàm đó gộp theo **mã hàng** (đầu vào của phép bóc định mức), còn `po_items` là **từng dòng**
	  và phải ghép ngược về `sales_order_item`.
	- Hàm đó **không trừ `work_order_qty`**, vì phần đã có Lệnh sản xuất vẫn đang phải làm nên vẫn
	  cần vật tư. Ở đây thì ngược lại: phần đã có lệnh rồi mà lên kế hoạch lần nữa là **ra lệnh
	  sản xuất trùng**.

	Nên chỗ này trừ thêm lên trên con số ERPNext đã tính:

	    planned_qty(lõi) = (qty − max(work_order_qty, delivered_qty)) × conversion_factor
	    planned_qty(mới) = planned_qty(lõi) − giữ chỗ × conversion_factor

	## ⚠ Chỉ trừ khi ô *Ghim Tồn Khả Dụng* đang tích

	Bỏ tích thì con số giữ chỗ **vẫn nằm trong dòng hàng** nhưng không có hiệu lực — `loc_don_song`
	loại đơn khỏi mọi phép cộng, và `chan_giu_cho_vuot_ton` cũng ngừng kiểm nên số đó có thể đã
	vượt tồn từ lâu. Trừ theo một con số không ai bảo vệ là **sản xuất thiếu thật**: kế hoạch ra
	ít hơn nhu cầu, mà kho thì không thực sự giữ hàng cho đơn này.

	## ⚠ Nhân `conversion_factor`

	`custom_so_luong_giu_cho` nằm ngay dưới `qty` và bị `chan_giu_cho_vuot_ton` kẹp bằng
	`min(row.qty, …)`, tức nó đo bằng **đơn vị bán**. Còn `planned_qty` của lõi đã nhân
	`conversion_factor` để về **đơn vị kho**. Không nhân thì đơn bán theo Thùng mà kho tính theo
	Cái sẽ trừ hụt đúng bằng số lần quy đổi. Đo 08/09: cả 35 dòng trên cổng 8012 đều có
	`conversion_factor = 1`, nên hôm nay chưa ai thấy — đó là lý do phải viết đúng ngay bây giờ
	chứ không đợi lỗi.
	"""
	if not source.get("custom_ghim_ton_kha_dung"):
		return

	giu = giu_cho_quy_kho([row.name for row in source.get("items") or []])
	if not giu:
		return

	refs = target.get("prod_plan_references") or []

	con_lai = []
	da_du = []
	for pi in target.get("po_items") or []:
		tru = tru_theo_dong(pi, refs, giu)

		if tru:
			con = flt(pi.planned_qty) - tru
			pi.planned_qty = con if con > 0 else 0
			pi.pending_qty = pi.planned_qty

		if flt(pi.planned_qty) > 0:
			con_lai.append(pi)
		else:
			da_du.append(pi.item_code)

	if not con_lai:
		frappe.throw(
			_(
				"Đơn Bán Hàng {0} đã giữ chỗ đủ hàng cho mọi dòng — không còn gì phải sản xuất.<br><br>"
				"Mặt hàng đã đủ: <b>{1}</b>.<br><br>"
				"Muốn sản xuất thêm thì giảm <i>Số Lượng Giữ Chỗ</i> trên dòng hàng, "
				"hoặc bỏ tích <i>Ghim Tồn Khả Dụng</i> rồi bấm lại nút này."
			).format(source.name, ", ".join(dict.fromkeys(da_du)))
		)

	if len(con_lai) != len(target.get("po_items")):
		target.set("po_items", con_lai)
		for i, row in enumerate(target.po_items, start=1):
			row.idx = i


def chi_tiet_dong_don(ten_dong):
	"""{tên dòng Đơn Bán: số liệu cần để biết dòng đó CÒN THIẾU bao nhiêu} — quy về ĐƠN VỊ KHO.

	Nguồn duy nhất của phép quy đổi, dùng chung cho hai chỗ: lúc **tạo** kế hoạch
	(`_tru_phan_da_giu_cho`) và lúc **lưu** kế hoạch
	(`python_hook.production_plan.canh_bao_vuot_phan_thieu`). Viết một hàm để không đẻ ra công
	thức thứ hai — đúng bài học ở `ghim_vat_tu._phai_san_xuat`, nơi hai hàm tên na ná tính hai
	thứ khác nhau và đảo ngược kết quả.

	Bỏ dòng của đơn **không tích** *Ghim Tồn Khả Dụng*: số giữ chỗ vẫn nằm đó nhưng không có
	hiệu lực, `loc_don_song` đã loại đơn khỏi mọi phép cộng.

	⚠ `qty`, `work_order_qty`, `delivered_qty`, `custom_so_luong_giu_cho` đều đo bằng **đơn vị
	  bán**; `planned_qty` của kế hoạch đo bằng **đơn vị kho**. Nhân `conversion_factor` ngay ở
	  đây để phía trên không phải nhớ. Đo 08/09: cả 35 dòng trên cổng 8012 đều có
	  `conversion_factor = 1` — chưa ai thấy, nên phải viết đúng ngay chứ không đợi lỗi.
	"""
	ten_dong = [t for t in (ten_dong or []) if t]
	if not ten_dong:
		return {}

	rows = frappe.get_all(
		"Sales Order Item",
		filters={"name": ["in", ten_dong], "custom_so_luong_giu_cho": [">", 0]},
		fields=[
			"name",
			"parent",
			"qty",
			"work_order_qty",
			"delivered_qty",
			"custom_so_luong_giu_cho as giu",
			"conversion_factor as cf",
		],
	)
	if not rows:
		return {}

	co_ghim = set(
		frappe.get_all(
			"Sales Order",
			filters={"name": ["in", list({r.parent for r in rows})], "custom_ghim_ton_kha_dung": 1},
			pluck="name",
		)
	)

	ra = {}
	for r in rows:
		if r.parent not in co_ghim:
			continue
		cf = flt(r.cf) or 1
		ra[r.name] = {
			"qty": flt(r.qty) * cf,
			"wo": flt(r.work_order_qty) * cf,
			"dl": flt(r.delivered_qty) * cf,
			"giu": flt(r.giu) * cf,
		}
	return ra


def giu_cho_quy_kho(ten_dong):
	"""{tên dòng Đơn Bán: số đã giữ chỗ, quy về đơn vị kho}."""
	return {k: v["giu"] for k, v in chi_tiet_dong_don(ten_dong).items()}


def tru_theo_dong(po_item, refs, giu):
	"""Phần giữ chỗ ứng với MỘT dòng Assembly Items.

	Ô *Consolidate Sales Order Items* gộp nhiều dòng đơn vào một dòng kế hoạch theo `bom_no`, lúc
	đó phải cộng dồn qua `prod_plan_references`. Doc mới mặc định KHÔNG gộp (`combine_items = 0`)
	nên nhánh đó hầu như không chạy — giữ lại để không âm thầm sai nếu sau này ai bật mặc định.
	"""
	khoa = po_item.get("sales_order_item")
	if refs:
		return sum(flt(giu.get(r.get("sales_order_item"), 0)) for r in refs if r.get("item_reference") == khoa)
	return flt(giu.get(khoa, 0))
