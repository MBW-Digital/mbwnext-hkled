# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Chặn xuất kho quá tồn khả dụng — PM-FEAT-00034 (Phần IV.1).

Đầu bài: `docs/features/chan-xuat-kho-qua-ton-kha-dung.md`. Anh Thắng chốt **đường B** ngày
25/08 (cơ chế giữ chỗ của lõi ERPNext không dùng được: nó tính theo MỘT kho, và chỉ giữ được
mặt hàng nằm trên Đơn Bán chứ không giữ được NVL bóc từ định mức).

## Một hàm, tám cửa

Mọi chứng từ rút tồn đều đi qua `stock_ledger.make_sl_entries`, nhưng hook được vào đó thì
đụng lõi. Nên chặn ở `before_submit` của **từng** chứng từ, dùng **chung một hàm** — đầu bài §4
ràng buộc rõ: *"Không hook 3-4 doctype rời"* và *"dùng lại đúng hàm tính tồn khả dụng của Phần
IV, không viết công thức thứ hai"*.

Đếm được **8 chứng từ** có thể làm giảm tồn (§1.1). Bản đầu của đầu bài định hook 3 cái ➜ thủng
6 cái, và kiểu thủng đó **chỉ lộ ra sau khi kho đã xuất lọt**.

⚠ **Chứng từ nào chưa có bộ đọc thì THROW, không im lặng.** Thà chặn nhầm một chứng từ hiếm còn
hơn để nó đi qua mà không ai kiểm — đúng tinh thần "thiếu một cái là thủng".

## Miễn trừ đơn của chính nó

Cơ chế lõi tự miễn trừ chứng từ sinh ra từ chính đơn đang giữ chỗ; đường B **phải tự làm lấy**.
Không có bước này thì đơn ghim 3 cái sẽ **tự chặn chính phiếu xuất của mình** — tính năng biến
thành cái khoá cửa từ bên trong.

## Yêu Cầu Mặt Hàng KHÔNG nằm ở đây

Nó không sinh Stock Ledger Entry, không lấy hàng đi đâu. Chặn ở đó là chặn một *dự định* ➜ chỉ
**cảnh báo** (§4 của đầu bài; bản đầu xếp nhầm nó ngang Phiếu xuất kho).
"""

import frappe
from frappe import _
from frappe.utils import flt

from mbwnext_hkled.api.kiem_tra_ton_kho import _kho_hop_le, _ton_thuc_te, ghim_boi_don_khac


# ══════════ Bộ đọc: chứng từ này rút những gì ra khỏi kho? ══════════
#
# Mỗi hàm trả về {mã hàng: số lượng RÚT RA} — chỉ phần thật sự đi ra, quy về đơn vị tồn kho.
# Dòng nhập vào (trả hàng, nhận về) không tính; kho ngoài tập kho hợp lệ cũng không tính, vì
# tồn ở đó vốn đã không nằm trong "tồn khả dụng" nên rút đi cũng không ăn vào phần ai đang giữ.


def _cong(ra, ma, sl):
	if ma and flt(sl) > 0:
		ra[ma] = ra.get(ma, 0) + flt(sl)


def _xuat_theo_warehouse(doc, kho_ok, dao_chieu=False):
	"""Khuôn chung cho chứng từ có `items` mang sẵn `warehouse` + `stock_qty`.

	`dao_chieu=True` dùng cho chứng từ MUA: bình thường nó nhập kho, chỉ bản **trả hàng** mới
	rút tồn ra.
	"""
	la_tra_hang = bool(doc.get("is_return"))
	if dao_chieu != la_tra_hang:
		return {}
	ra = {}
	for d in doc.get("items") or []:
		if d.get("warehouse") in kho_ok:
			_cong(ra, d.get("item_code"), abs(flt(d.get("stock_qty") or d.get("qty"))))
	return ra


def _xuat_delivery_note(doc, kho_ok):
	return _xuat_theo_warehouse(doc, kho_ok)


def _xuat_sales_invoice(doc, kho_ok):
	# Không tích "Cập nhật tồn kho" thì hoá đơn không đụng kho — hàng đi bằng Phiếu xuất kho.
	if not doc.get("update_stock"):
		return {}
	return _xuat_theo_warehouse(doc, kho_ok)


def _xuat_purchase_receipt(doc, kho_ok):
	return _xuat_theo_warehouse(doc, kho_ok, dao_chieu=True)


def _xuat_purchase_invoice(doc, kho_ok):
	if not doc.get("update_stock"):
		return {}
	return _xuat_theo_warehouse(doc, kho_ok, dao_chieu=True)


def _xuat_stock_entry(doc, kho_ok):
	"""Phiếu xuất/chuyển kho: rút ở **kho nguồn**.

	⚠ Chuyển kho nội bộ giữa hai kho HỢP LỆ là **rút ở đây, nhập ở kia** — tổng tồn khả dụng
	  không đổi. Nên trừ lại phần nhập vào kho hợp lệ, nếu không mọi phiếu chuyển kho đều bị
	  chặn oan.
	"""
	ra = {}
	for d in doc.get("items") or []:
		sl = flt(d.get("transfer_qty") or d.get("qty"))
		if d.get("s_warehouse") in kho_ok:
			_cong(ra, d.get("item_code"), sl)
		if d.get("t_warehouse") in kho_ok:
			ma = d.get("item_code")
			if ma:
				ra[ma] = ra.get(ma, 0) - sl
	return {m: sl for m, sl in ra.items() if sl > 0}


def _xuat_stock_reconciliation(doc, kho_ok):
	"""Kiểm kê: chỉ dòng ĐIỀU CHỈNH GIẢM mới là rút tồn."""
	ra = {}
	for d in doc.get("items") or []:
		if d.get("warehouse") not in kho_ok:
			continue
		giam = flt(d.get("current_qty")) - flt(d.get("qty"))
		_cong(ra, d.get("item_code"), giam)
	return ra


def _xuat_subcontracting_receipt(doc, kho_ok):
	"""Nhận hàng gia công: tiêu hao NVL đã đưa cho nhà cung cấp.

	Bảng con không có cột kho — kho tiêu hao nằm ở đầu phiếu (`supplier_warehouse`).
	"""
	kho = doc.get("supplier_warehouse")
	if kho not in kho_ok:
		return {}
	ra = {}
	for d in doc.get("supplied_items") or []:
		_cong(ra, d.get("rm_item_code"), d.get("consumed_qty"))
	return ra


def _xuat_asset_capitalization(doc, kho_ok):
	"""Tiêu hao vật tư để hình thành tài sản."""
	ra = {}
	for d in doc.get("stock_items") or []:
		if d.get("warehouse") in kho_ok:
			_cong(ra, d.get("item_code"), d.get("stock_qty"))
	return ra


BO_DOC = {
	"Delivery Note": _xuat_delivery_note,
	"Sales Invoice": _xuat_sales_invoice,
	"Purchase Receipt": _xuat_purchase_receipt,
	"Purchase Invoice": _xuat_purchase_invoice,
	"Stock Entry": _xuat_stock_entry,
	"Stock Reconciliation": _xuat_stock_reconciliation,
	"Subcontracting Receipt": _xuat_subcontracting_receipt,
	"Asset Capitalization": _xuat_asset_capitalization,
}


# ══════════ Miễn trừ ══════════


def _don_duoc_mien(doc):
	"""Những Đơn Bán mà chứng từ này đang thực hiện — phần ghim của chúng không được tính là
	"người khác giữ", nếu không đơn tự chặn phiếu xuất của chính mình."""
	don = set()
	for d in doc.get("items") or []:
		for truong in ("against_sales_order", "sales_order"):
			if d.get(truong):
				don.add(d.get(truong))
	return don


# ══════════ Hàm chặn ══════════


def chan_xuat_qua_ton_kha_dung(doc, method=None):
	"""Gọi từ `before_submit` của cả 8 chứng từ rút tồn."""
	bo_doc = BO_DOC.get(doc.doctype)
	if bo_doc is None:
		# Được khai trong hooks mà không có bộ đọc = lỗi lập trình, không phải ca nghiệp vụ.
		frappe.throw(
			_("Chưa có bộ đọc tồn cho chứng từ {0} — báo đội kỹ thuật, đừng bỏ qua.").format(doc.doctype)
		)

	kho_ok = set(_kho_hop_le(doc.get("company")))
	if not kho_ok:
		return

	xuat = bo_doc(doc, kho_ok)
	if not xuat:
		return

	ghim, _cb = ghim_boi_don_khac(tru_don=_don_duoc_mien(doc) or None)
	ton = _ton_thuc_te(set(xuat), list(kho_ok))

	loi = []
	for ma, sl in sorted(xuat.items()):
		kha_dung = flt(ton.get(ma, 0)) - flt(ghim.get(ma, 0))
		if sl > kha_dung:
			loi.append((ma, sl, kha_dung))

	if not loi:
		return

	# ⚠ Câu chặn KHÔNG nêu tên đơn đang giữ — anh Thắng chốt 25/08 15:47: *"em chỉ cần báo là
	#   tồn đang không đủ thôi nhé"*. Nêu tên đơn là để lộ đơn của khách này sang mắt người
	#   thao tác đơn khác.
	dong = "<br>".join(
		_("• {0}: xuất {1}, tồn khả dụng còn {2}").format(
			ma,
			frappe.format_value(sl, {"fieldtype": "Float"}),
			frappe.format_value(max(0.0, kd), {"fieldtype": "Float"}),
		)
		for ma, sl, kd in loi
	)
	frappe.throw(
		_("Không xuất được: tồn khả dụng không đủ.<br><br>{0}<br><br>"
		  "Phần chênh đang được các Đơn Bán khác giữ chỗ.").format(dong),
		title=_("Xuất quá tồn khả dụng"),
	)


def canh_bao_yeu_cau_mat_hang(doc, method=None):
	"""Yêu Cầu Mặt Hàng: **cảnh báo, không chặn**.

	Nó không sinh Stock Ledger Entry — chặn ở đây là chặn một *dự định*. Người dùng hoàn toàn
	có thể lập yêu cầu cho phần chưa có hàng; đó chính là việc của phiếu này.
	"""
	if doc.get("material_request_type") != "Material Issue":
		return

	kho_ok = set(_kho_hop_le(doc.get("company")))
	if not kho_ok:
		return

	xin = {}
	for d in doc.get("items") or []:
		if d.get("warehouse") in kho_ok:
			_cong(xin, d.get("item_code"), d.get("stock_qty") or d.get("qty"))
	if not xin:
		return

	ghim, _cb = ghim_boi_don_khac()
	ton = _ton_thuc_te(set(xin), list(kho_ok))

	vuot = [
		ma for ma, sl in sorted(xin.items())
		if sl > flt(ton.get(ma, 0)) - flt(ghim.get(ma, 0))
	]
	if vuot:
		frappe.msgprint(
			_("{0} mặt hàng đang xin nhiều hơn tồn khả dụng: {1}.<br>"
			  "Vẫn lập được phiếu, nhưng lúc xuất kho thật sẽ bị chặn nếu tồn chưa về kịp.").format(
				len(vuot), ", ".join(vuot[:8]) + ("…" if len(vuot) > 8 else "")
			),
			title=_("Tồn khả dụng không đủ"),
			indicator="orange",
		)
