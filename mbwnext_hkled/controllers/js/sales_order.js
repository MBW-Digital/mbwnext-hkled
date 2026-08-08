// Đơn Bán Hàng — PM-TASK-00046 (Ghi Chú Sản Xuất) và PM-TASK-00047 (nút tạo Kế hoạch sản xuất).

frappe.ui.form.on("Sales Order", {
	onload(frm) {
		// Ghi lại giá trị lúc mở form làm mốc so sánh. Thiếu bước này thì lần sửa ghi chú ĐẦU TIÊN
		// sau khi mở đơn cũ sẽ coi mọi dòng đang có nội dung là "đã sửa tay" và không cập nhật dòng nào.
		frm.__hkled_ghi_chu_cu = frm.doc.custom_note || "";
	},

	refresh(frm) {
		// Đặt lại mốc cả ở refresh: sau khi Lưu/Duyệt, Frappe dựng lại form nhưng không gọi onload.
		if (frm.__hkled_ghi_chu_cu === undefined) {
			frm.__hkled_ghi_chu_cu = frm.doc.custom_note || "";
		}

		// PM-TASK-00047 — chỉ hiện khi đơn ĐÃ DUYỆT: `Production Plan.get_so_items()` lọc
		// `Sales Order Item.docstatus == 1`, nên tạo từ đơn nháp sẽ ra kế hoạch rỗng.
		if (frm.doc.docstatus !== 1) return;

		frm.add_custom_button(
			__("Kế Hoạch Sản Xuất"),
			() =>
				frappe.model.open_mapped_doc({
					method: "mbwnext_hkled.api.production_plan.make_production_plan",
					frm: frm,
				}),
			__("Create")
		);
	},

	// PM-TASK-00046 — sửa ghi chú ở đầu đơn thì các dòng hàng nhận theo.
	custom_note(frm) {
		lan_toa_ghi_chu(frm);
	},
});

frappe.ui.form.on("Sales Order Item", {
	items_add(frm, cdt, cdn) {
		// Dòng thêm mới sau khi đã nhập ghi chú đầu đơn cũng phải nhận giá trị.
		const row = locals[cdt][cdn];
		if (!row.custom_note && frm.doc.custom_note) {
			frappe.model.set_value(cdt, cdn, "custom_note", frm.doc.custom_note);
		}
	},
});

// Chỉ ghi đè dòng đang TRỐNG hoặc đang giữ đúng giá trị cũ của đầu đơn. Dòng người dùng đã sửa tay
// thì để nguyên — khách yêu cầu rõ là sửa được từng dòng, mà đổi ghi chú đầu đơn rồi xoá sạch phần
// đã sửa thì hỏng đúng yêu cầu đó.
function lan_toa_ghi_chu(frm) {
	const moi = frm.doc.custom_note || "";
	const cu = frm.__hkled_ghi_chu_cu || "";
	frm.__hkled_ghi_chu_cu = moi;

	let da_doi = 0;
	(frm.doc.items || []).forEach((row) => {
		const hien_tai = row.custom_note || "";
		if (hien_tai === "" || hien_tai === cu) {
			frappe.model.set_value(row.doctype, row.name, "custom_note", moi);
			da_doi++;
		}
	});

	const giu_nguyen = (frm.doc.items || []).length - da_doi;
	if (giu_nguyen > 0) {
		frappe.show_alert({
			message: __("Giữ nguyên Ghi Chú Sản Xuất đã sửa tay ở {0} dòng hàng", [giu_nguyen]),
			indicator: "orange",
		});
	}
}
