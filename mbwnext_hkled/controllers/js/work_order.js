frappe.ui.form.on("Work Order", {
	refresh(frm) {
		if (frm.doc.custom_start_time && (frm.doc.custom_work_order_employee || []).length) {
			frm.add_custom_button(__("Tính Lại Lịch"), () => recalculate_schedule(frm));
		}
	},
});

function recalculate_schedule(frm) {
	frappe.call({
		method: "mbwnext_hkled.api.work_order_schedule.recalculate_schedule",
		args: { work_order: frm.doc.name },
		freeze: true,
		freeze_message: __("Đang tính toán lịch sản xuất..."),
		callback: function (r) {
			if (!r.message) {
				return;
			}
			frappe.show_alert(
				{
					message: __("Thời gian kết thúc dự kiến: {0} ({1} phút)", [
						frappe.datetime.str_to_user(r.message.end_time),
						r.message.estimated_completion_time_minutes,
					]),
					indicator: "green",
				},
				7
			);
			frm.reload_doc();
		},
	});
}
