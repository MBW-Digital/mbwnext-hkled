/* Bậc Thợ bắt buộc với Công nhân (C1, chốt 31/07).
   Ràng buộc thật nằm ở `mandatory_depends_on` của custom_employee_level — patch
   `add_work_team_fields` đặt. Phần dưới chỉ để báo sớm ngay lúc người dùng đổi Loại nhân sự,
   thay vì đợi tới lúc bấm Lưu mới biết. */
frappe.ui.form.on("Employee", {
	custom_employee_type: warn_missing_employee_level,
	custom_employee_level: warn_missing_employee_level,
});

function warn_missing_employee_level(frm) {
	if (frm.doc.custom_employee_type === "Công nhân" && !frm.doc.custom_employee_level) {
		frappe.show_alert(
			{
				message: __("Nhân sự Công nhân bắt buộc phải có Bậc Thợ — chưa chọn thì không lưu được."),
				indicator: "red",
			},
			5
		);
	}
}
