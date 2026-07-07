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
