# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""GAP-3 — nút "Bắt Đầu Sản Xuất" trên Lệnh sản xuất (mục III.5, chốt C2 + C8).

Vì sao là nút riêng chứ không hook vào trạng thái In Process:
`WorkOrder.get_status()` của erpnext hard-code `material_transferred_for_manufacturing > 0`
→ "In Process", nên lệnh tự chuyển ngay khi NHẬN nguyên vật liệu, không phải lúc thật sự bắt
đầu làm. Sửa chỗ đó là vá app lõi tầng 1, ảnh hưởng mọi khách → không làm.

Chốt C8: nút chỉ hiện khi lệnh đang In Process và CHƯA từng ấn; ấn một lần là xong.
"""

import frappe
from frappe import _
from frappe.utils import now_datetime

from mbwnext_hkled.api.work_order_schedule import recalculate_schedule


@frappe.whitelist()
def start_production(work_order):
	"""Ghi Thời Gian Bắt Đầu = giờ thực tế rồi tính lại lịch cho các dòng chưa khoá."""
	wo = frappe.get_doc("Work Order", work_order)
	wo.check_permission("write")

	if wo.docstatus != 1:
		frappe.throw(_("Chỉ bắt đầu sản xuất được khi Lệnh sản xuất đã được duyệt"))
	if wo.status != "In Process":
		frappe.throw(
			_("Chỉ ấn được khi Lệnh sản xuất đang ở trạng thái In Process (hiện tại: {0})").format(
				frappe.bold(wo.status)
			)
		)
	if wo.get("custom_production_started"):
		frappe.throw(_("Lệnh sản xuất này đã được bắt đầu rồi, không ấn lại được"))

	planned_start = wo.custom_start_time
	actual_start = now_datetime()

	wo.db_set("custom_start_time", actual_start)
	wo.db_set("custom_production_started", 1)

	# Ghi lại mốc dự kiến vs thực tế để sau còn đối chiếu — db_set không ghi Version log.
	wo.add_comment(
		"Comment",
		_("Bắt Đầu Sản Xuất: giờ dự kiến {0} → giờ thực tế {1}").format(planned_start, actual_start),
	)

	result = recalculate_schedule(wo.name)
	return {
		"planned_start": planned_start,
		"actual_start": actual_start,
		"end_time": result.get("end_time"),
		"estimated_completion_time_minutes": result.get("estimated_completion_time_minutes"),
	}
