/* GAP-8 — Công Việc Khác: hiện tổng thời gian và lương ngay khi gõ, không đợi lưu mới biết lệch. */
frappe.ui.form.on("Other Task", {
	total_time: refresh_summary,
	employees_add: refresh_summary,
	employees_remove: refresh_summary,
	refresh: refresh_summary,
});

frappe.ui.form.on("Other Task Table", {
	time: refresh_summary,
	employee: refresh_summary,
});

function refresh_summary(frm) {
	const rows = frm.doc.employees || [];
	const total = rows.reduce((s, r) => s + flt(r.time), 0);
	const goal = flt(frm.doc.total_time);
	const diff = total - goal;

	if (!rows.length) {
		frm.dashboard.clear_headline();
		return;
	}

	if (Math.abs(diff) < 0.001) {
		frm.dashboard.set_headline(
			__("Tổng khớp — lưu được. ({0} phút)", [format_number(total, null, 2)]),
			"green"
		);
	} else {
		frm.dashboard.set_headline(
			__("Tổng thời gian các dòng ({0} phút) phải bằng Tổng Thời Gian ({1} phút). Đang {2} {3} phút.", [
				format_number(total, null, 2),
				format_number(goal, null, 2),
				diff > 0 ? __("vượt") : __("thiếu"),
				format_number(Math.abs(diff), null, 2),
			]),
			"red"
		);
	}
}
