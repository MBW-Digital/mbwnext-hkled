# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Phiếu nhập mua — thu hồi phần đã phân bổ khi huỷ phiếu (PM-FEAT-00036, Phần IV.2).

Luật ở `api/ghim_vat_tu.thu_hoi_phan_bo`, đọc docstring bên đó trước khi sửa. File này là chỗ
cắm và chỗ nuốt lỗi có kiểm soát.

## Ca này đã xảy ra thật trên cổng 8012

05/09/2026, anh Thắng tự chạy thử trước khi hỏi: 09:08 tạo `PNK-26-00004` 10 `NVL 3` rồi bấm
*Phân Bổ* ➜ 10 cái vào `SO-26-00028`; 09:09 **huỷ phiếu** ➜ tồn tụt về 7 nhưng phần ghim vẫn 17.
Kết quả: `NVL 3` còn 7 cái thật mà mọi đơn đều thấy tồn khả dụng **0** — hàng bị giam, không có
thông báo nào. Phép kiểm bất biến bắt được, và đó là lý do file này tồn tại.
"""

import frappe
from frappe import _


def thu_hoi_ghim_khi_huy(doc, method=None):
	"""Treo ở `on_cancel` của Phiếu nhập mua."""
	if doc.doctype != "Purchase Receipt":
		return

	from mbwnext_hkled.api.ghim_vat_tu import thu_hoi_phan_bo

	try:
		viec = thu_hoi_phan_bo(doc.name)
	except Exception:
		frappe.log_error(
			title="Thu hồi phần đã phân bổ thất bại",
			message=f"{doc.name}\n\n{frappe.get_traceback()}",
		)
		# ⚠ KHÔNG chặn việc huỷ phiếu: hàng đã ra khỏi kho rồi, chặn lại là giữ một chứng từ sai
		#   trong sổ. Nhưng cũng không im lặng — phần ghim lệch mà không ai biết thì hàng bị giam.
		frappe.msgprint(
			_(
				"Phiếu đã huỷ, nhưng <b>chưa thu hồi được phần giữ chỗ đã chia từ phiếu này</b>. "
				"Mở các Đơn Bán liên quan và lưu lại một lần để hệ thống tính lại."
			),
			title=_("Chưa thu hồi được phần ghim"),
			indicator="orange",
		)
		return

	if viec:
		frappe.msgprint(
			_("Đã thu hồi phần giữ chỗ đã chia từ phiếu này:") + "<br>• " + "<br>• ".join(viec),
			title=_("Thu hồi phần đã phân bổ"),
			indicator="orange",
		)
