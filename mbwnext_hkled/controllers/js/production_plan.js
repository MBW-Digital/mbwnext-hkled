frappe.ui.form.on("Production Plan Item", "custom_create_bom", function (frm, cdt, cdn) {
	const row = locals[cdt][cdn];

	if (!row.item_code) {
		frappe.msgprint(__("Vui lòng chọn Mặt Hàng trước"));
		return;
	}

	frappe.call({
		method: "mbwnext_hkled.api.bom.auto_create_bom",
		args: {
			item_code: row.item_code,
			company: frm.doc.company,
		},
		freeze: true,
		freeze_message: __("Đang xử lý BOM tự động..."),
		callback: function (r) {
			if (!r.message) {
				return;
			}
			const res = r.message;

			frappe.msgprint({
				title: res.status === "valid" ? __("BOM Hiện Tại Hợp Lệ") : __("Đã Tạo BOM Mới"),
				message: res.message,
				indicator: res.status === "valid" ? "blue" : "green",
			});

			frappe.model.set_value(cdt, cdn, "bom_no", res.bom);
		},
	});
});

/* GAP-4 — hiện Thời Điểm Cần Hoàn Thành ngay khi chọn Đơn Bán Hàng.
   Giá trị thật vẫn do server tính lại lúc lưu (doc_events Production Plan.validate), phần này
   chỉ để người dùng thấy trước khi lưu chứ không phải nguồn dữ liệu. */
frappe.ui.form.on("Production Plan Sales Order", {
	sales_order(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (!row.sales_order) return;

		frappe.db
			.get_value("Sales Order", row.sales_order, ["delivery_date", "custom_time"])
			.then((r) => {
				const so = (r && r.message) || {};
				if (!so.delivery_date) return;

				// custom_time trống thì lấy 00:00 — khớp DEFAULT_TIME bên production_plan.py
				const time_part = so.custom_time || "00:00:00";
				frappe.model.set_value(
					cdt,
					cdn,
					"custom_required_completion_date_time",
					`${so.delivery_date} ${time_part}`
				);
			});
	},
});
