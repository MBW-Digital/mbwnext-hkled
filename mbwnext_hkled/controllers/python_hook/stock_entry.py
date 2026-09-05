# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-7 — sinh serial thành phẩm khi Finish Lệnh sản xuất (mục IV.4, chốt C3 + C9 + C11).

Định dạng chốt với HKLED ngày 02/08: `<2 số cuối năm>-<số thứ tự đơn bán>-<STT 4 chữ số>`
→ đơn `SAL-ORD-2026-00001` sinh ra `26-00001-0001`, `26-00001-0002`, …

Vì sao rút gọn được: truy xuất của ERPNext KHÔNG đọc chuỗi serial — mỗi serial là một bản ghi
`Serial No` riêng, tự lưu liên kết tới lệnh sản xuất / chứng từ / khách hàng / kho / lô, và báo
cáo Sổ Serial truy ngược qua `Serial and Batch Entry`. Đơn bán ở HKLED chỉ dùng một naming
series `SAL-ORD-.YYYY.-` nên phần bỏ đi là cố định, serial vẫn duy nhất.

⚠ Lệnh KHÔNG có mã đơn bán thì lấy mã lệnh làm gốc, và phải thêm tiền tố `W`:
`MFG-WO-2026-00042` rút gọn trần sẽ ra `26-00042`, TRÙNG với đơn bán số 00042 cùng năm — mà
serial là khoá chính toàn hệ thống nên trùng là hỏng. `W26-00042-0001` tách hai nguồn ra.

STT đánh **liên tục theo đơn** (C9): tra số lớn nhất đã có của cùng prefix rồi nối tiếp, nên
nhiều lệnh cùng một đơn không sinh serial trùng nhau.
"""

import re

import frappe
from frappe import _
from frappe.utils import cint, flt

SERIAL_PADDING = 4
WORK_ORDER_PREFIX = "W"


def build_prefix(work_order):
	"""Gốc mã serial của một Lệnh sản xuất: theo đơn bán nếu có, không thì theo mã lệnh."""
	sales_order = work_order.get("sales_order")
	if sales_order:
		return shorten_document_name(sales_order)
	return WORK_ORDER_PREFIX + shorten_document_name(work_order.name)


def shorten_document_name(name):
	"""`SAL-ORD-2026-00001` → `26-00001`. Không khớp dạng chuẩn thì giữ nguyên cho an toàn."""
	match = re.search(r"(\d{4})-(\d+)$", name or "")
	if not match:
		return name
	year, seq = match.groups()
	return f"{year[-2:]}-{seq}"


def next_serial_index(prefix):
	"""STT lớn nhất đã dùng của prefix này, để lệnh sau nối tiếp lệnh trước (C9)."""
	rows = frappe.get_all(
		"Serial No",
		filters={"name": ["like", f"{prefix}-%"]},
		pluck="name",
	)
	largest = 0
	pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
	for name in rows:
		match = pattern.match(name)
		if match:
			largest = max(largest, cint(match.group(1)))
	return largest + 1


def generate_serials(prefix, qty):
	"""Danh sách serial mới, bỏ qua mã đã tồn tại phòng 2 người Finish cùng lúc."""
	serials = []
	index = next_serial_index(prefix)
	while len(serials) < qty:
		candidate = f"{prefix}-{str(index).zfill(SERIAL_PADDING)}"
		index += 1
		if frappe.db.exists("Serial No", candidate):
			continue
		serials.append(candidate)
	return serials


def set_serial_no_on_manufacture(doc, method=None):
	"""Điền sẵn serial cho dòng thành phẩm của phiếu Manufacture trước khi submit.

	Chỉ đụng mặt hàng bật `has_serial_no`, và chỉ dòng NHẬP kho thành phẩm (`t_warehouse`,
	không có `s_warehouse`) — nguyên vật liệu xuất ra không sinh serial mới.
	"""
	if doc.doctype != "Stock Entry":
		return
	if doc.purpose != "Manufacture" or not doc.get("work_order"):
		return

	work_order = frappe.db.get_value(
		"Work Order", doc.work_order, ["name", "sales_order"], as_dict=True
	)
	if not work_order:
		return

	prefix = build_prefix(work_order)

	for row in doc.get("items") or []:
		# Dòng thành phẩm = chỉ nhập kho, không xuất kho.
		if not row.t_warehouse or row.s_warehouse:
			continue
		if not frappe.get_cached_value("Item", row.item_code, "has_serial_no"):
			continue
		# Người dùng đã tự khai serial thì tôn trọng, không ghi đè.
		if row.get("serial_no") or row.get("serial_and_batch_bundle"):
			continue

		qty = cint(flt(row.qty))
		if qty <= 0:
			continue

		serials = generate_serials(prefix, qty)
		if not serials:
			continue

		# `use_serial_batch_fields = 1` là đường v15 hỗ trợ để tự cấp serial bằng text:
		# erpnext bỏ qua việc dựng lại Serial and Batch Bundle cho dòng có cờ này
		# (xem stock_entry.py, vòng lặp `if row.use_serial_batch_fields: continue`).
		row.use_serial_batch_fields = 1
		row.serial_no = "\n".join(serials)


def validate_serial_prefix_uniqueness(sales_order_name, work_order_name):
	"""Dùng cho test: khẳng định prefix từ đơn bán không bao giờ đụng prefix từ lệnh sản xuất."""
	so_prefix = shorten_document_name(sales_order_name)
	wo_prefix = WORK_ORDER_PREFIX + shorten_document_name(work_order_name)
	if so_prefix == wo_prefix:
		frappe.throw(_("Trùng gốc mã serial giữa đơn bán và lệnh sản xuất: {0}").format(so_prefix))
	return so_prefix, wo_prefix


def chuyen_ghim_khi_san_xuat_xong(doc, method=None):
	"""Chứng từ sản xuất được duyệt ➜ đơn được ghim thêm thành phẩm, vật tư tự nhả.

	PM-FEAT-00036 — luật ở `api/ghim_vat_tu.chuyen_ghim_sau_san_xuat`, đọc docstring bên đó
	trước khi sửa. Hàm này chỉ là chỗ cắm và chỗ **nuốt lỗi có kiểm soát**.

	🔴 **Cố ý KHÔNG cho lỗi ở đây làm hỏng việc duyệt chứng từ sản xuất.** Hàng đã làm ra thật
	  và đã nhập kho thật; chặn chứng từ lại vì một phép ghi sổ giữ chỗ là đổi một sai lệch nhỏ
	  lấy một sai lệch lớn — người thao tác sẽ không hiểu vì sao không duyệt được, và cái họ làm
	  tiếp thường là tắt tính năng đi.

	  Nhưng **không nuốt im lặng**: hiện thông báo ngay trên màn hình và ghi Error Log, vì phần
	  ghim lệch mà không ai biết đúng là loại lỗi cả Phần IV sinh ra để chặn.
	"""
	if doc.doctype != "Stock Entry" or doc.get("purpose") != "Manufacture":
		return
	if not doc.get("work_order") or flt(doc.get("fg_completed_qty")) <= 0:
		return

	from mbwnext_hkled.api.ghim_vat_tu import chuyen_ghim_sau_san_xuat

	nguoc = doc.docstatus == 2
	try:
		viec = chuyen_ghim_sau_san_xuat(doc.fg_completed_qty, doc.work_order, nguoc=nguoc)
	except Exception:
		frappe.log_error(
			title="Chuyển ghim sau sản xuất thất bại",
			message=f"{doc.name} · lệnh {doc.work_order}\n\n{frappe.get_traceback()}",
		)
		frappe.msgprint(
			_(
				"Chứng từ đã được ghi nhận, nhưng <b>phần giữ chỗ của Đơn Bán chưa cập nhật được</b>. "
				"Mở Đơn Bán liên quan và lưu lại một lần để hệ thống tính lại phần ghim."
			),
			title=_("Chưa chuyển được phần ghim"),
			indicator="orange",
		)
		return

	if viec:
		frappe.msgprint(
			_("Đã chuyển phần ghim sang thành phẩm:") + "<br>• " + "<br>• ".join(viec),
			alert=True,
			indicator="green",
		)
