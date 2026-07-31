frappe.ui.form.on("Employee", {
	custom_employee_type: check_employee_level_hint,
	custom_employee_level: check_employee_level_hint,
});

function check_employee_level_hint(frm) {
	if (frm.doc.custom_employee_type === "Công nhân" && !frm.doc.custom_employee_level) {
		frappe.show_alert(
			{
				message: __("Nhân sự Công nhân nên được gán Bậc Thợ để tính giờ công chuẩn."),
				indicator: "orange",
			},
			5
		);
	}
}
