// Chọn Mặt Hàng trên BOM -> tra BOM Template của mặt hàng cha, điền sẵn bảng Nguyên Vật Liệu.
// Số lượng do Server Script hkled_resolve_bom_qty tính (yêu cầu của TungDA 07/08, PM-FEAT-00007).
//
// Mặt hàng không có BOM Template thì KHÔNG đụng gì tới form — giữ nguyên hành vi mặc định
// của ERPNext, tránh phá luồng làm BOM tay của các mặt hàng ngoài phạm vi HKLED.

frappe.ui.form.on("BOM", {
	item(frm) {
		// frm.set_intro NỐI THÊM banner chứ không thay thế (Layout.show_message dùng appendTo,
		// chỉ chuỗi rỗng mới xoá). Không dọn tay thì đổi Mặt Hàng vài lần là chồng một cột banner.
		// Chỗ này an toàn: intro của ERPNext trên BOM chỉ đặt khi Mặt Hàng là hàng cha có biến
		// thể, mà trường hợp đó không bao giờ tra ra BOM Template nên hai bên không giẫm nhau.
		frm.set_intro("");

		if (!frm.doc.item) {
			return;
		}

		frappe.call({
			method: "mbwnext_hkled.api.bom.get_template_raw_materials",
			args: { item_code: frm.doc.item },
			freeze: true,
			freeze_message: __("Đang tra BOM Template..."),
			callback(r) {
				const res = r.message || {};
				if (!res.template) {
					return; // không có template -> để ERPNext xử lý như thường
				}

				if (res.error) {
					frappe.msgprint({
						title: __("Chưa điền được Nguyên Vật Liệu"),
						message: __("BOM Template {0} có nhưng chưa tính được: {1}", [
							res.template,
							res.error,
						]),
						indicator: "orange",
					});
					return;
				}

				if (!(res.items || []).length) {
					return;
				}

				const existing = (frm.doc.items || []).filter((row) => row.item_code);
				if (!existing.length) {
					fill_raw_materials(frm, res);
					return;
				}

				// Đã có dòng nhập tay thì hỏi trước — ghi đè im lặng là mất công người dùng.
				frappe.confirm(
					__(
						"Mặt hàng này có BOM Template <b>{0}</b> với {1} nguyên vật liệu.<br><br>Thay toàn bộ {2} dòng đang có trong bảng Nguyên Vật Liệu?",
						[res.template, res.items.length, existing.length]
					),
					() => fill_raw_materials(frm, res)
				);
			},
		});
	},
});

async function fill_raw_materials(frm, res) {
	frm.clear_table("items");

	// PHẢI gọi TUẦN TỰ, không được bắn song song trong forEach.
	//
	// Trigger item_code của ERPNext gọi frappe.call({doc: doc, ...}) — dạng run_doc_method, tức
	// gửi nguyên cả tài liệu BOM lên server. Đường về mới là chỗ hỏng:
	//   1. handler.py `run_doc_method` trả lại chính bản chụp client vừa gửi (frappe.response.docs).
	//   2. request.js chạy `frappe.model.sync` TRƯỚC callback → `update_in_locals` ghi đè bảng con
	//      rồi `clear_keys` XOÁ những trường không có trong bản chụp.
	//   3. Callback mới `$.extend(d, r.message)` — chỉ cho đúng dòng của nó.
	// Bắn song song thì phản hồi thứ N xoá sạch dòng 1…N-1, chỉ dòng về cuối cùng còn dữ liệu.
	// Mất cả 12 trường chứ không riêng uom: item_name, description, stock_uom, uom,
	// conversion_factor, bom_no, rate, base_rate, stock_qty, image... — nghĩa là BOM ra giá 0 và
	// bán thành phẩm mất liên kết BOM con. Thắng báo 23/08 (PM-FEAT-00007) vì thấy cột UOM trống.
	//
	// Gọi tuần tự thì bản chụp gửi lên đã chứa dữ liệu các dòng trước nên vòng sync không xoá gì.
	// `script_manager.trigger` trả về `frappe.after_server_call()` (resolve khi ajax_count về 0),
	// await được vì `$(document).ajaxSend` tăng biến đếm ngay lúc $.ajax chạy.
	frappe.dom.freeze(__("Đang lấy thông tin nguyên vật liệu..."));
	try {
		for (const comp of res.items) {
			const row = frm.add_child("items", {
				item_code: comp.item_code,
				qty: comp.qty,
			});
			// Trigger item_code của ERPNext tự lấy tên, đơn vị tính, đơn giá, kho và bom_no
			// của bán thành phẩm — mình chỉ điền mã và số lượng.
			await frm.script_manager.trigger("item_code", row.doctype, row.name);
		}
	} finally {
		frappe.dom.unfreeze();
	}

	frm.refresh_field("items");
	frappe.show_alert(
		{
			message: __("Đã điền {0} nguyên vật liệu từ BOM Template {1}", [
				res.items.length,
				res.template,
			]),
			indicator: "green",
		},
		7
	);

	// Thành phần Theo Rule chưa khai Số Lượng thì hệ thống tạm tính 1. Phải nói ra,
	// không để người dùng tưởng con số đó là do công thức tính.
	//
	// Dùng banner cố định chứ KHÔNG dùng frappe.msgprint: lúc này chuỗi trigger item_code của
	// ERPNext vẫn đang chạy và nó dọn hộp thoại msgprint dùng chung, làm thân hộp thoại rỗng.
	// Banner cũng hợp lý hơn — cảnh báo nằm lại trên form trong suốt lúc người dùng nhập.
	if ((res.qty_defaulted || []).length) {
		const names = res.qty_defaulted
			.map((c) => `<b>${frappe.utils.escape_html(c)}</b>`)
			.join(", ");
		frm.set_intro(
			__(
				"{0} chưa có công thức số lượng và cũng chưa khai Số Lượng trên BOM Template {1}, nên hệ thống tạm điền Số Lượng = <b>1</b>. Nếu thực tế khác, sửa cột Số Lượng của thành phần đó trong BOM Template rồi chọn lại Mặt Hàng.",
				[names, frappe.utils.escape_html(res.template)]
			),
			"orange"
		);
	}
}
