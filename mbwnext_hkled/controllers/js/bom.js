// Chọn Mặt Hàng trên BOM -> tra BOM Template của mặt hàng cha, điền sẵn bảng Nguyên Vật Liệu.
// Số lượng do Server Script hkled_resolve_bom_qty tính (yêu cầu của TungDA 07/08, PM-FEAT-00007).
//
// Mặt hàng không có BOM Template thì KHÔNG đụng gì tới form — giữ nguyên hành vi mặc định
// của ERPNext, tránh phá luồng làm BOM tay của các mặt hàng ngoài phạm vi HKLED.
//
// Cây BOM 3 tầng (đèn -> vỏ + module -> linh kiện) là mô hình khách gửi, không phải hiếm gặp
// (Thắng phát hiện 24/08, PM-FEAT-00007). Bảng Nguyên Vật Liệu chỉ điền PHẲNG — nếu một dòng tự
// nó là bán thành phẩm có BOM Template riêng nhưng CHƯA có BOM, ERPNext không tự tạo BOM cho nó
// (get_bom_material_detail chỉ nối bom_no vào BOM đã có sẵn). Nút "Tạo BOM tự động" bên dưới gọi
// lại đúng engine build_bom_tree đang chạy ở Kế hoạch sản xuất — một hành vi, hai lối vào, theo
// chốt của TungDA/Thắng 24/08. KHÔNG tự tạo BOM ngầm lúc chọn Mặt Hàng: app này từng vấp việc
// engine ghi đè is_default lên BOM đang được Work Order thật tham chiếu, phải cancel + khôi phục
// tay (xem CLAUDE.md mục "Bài học quan trọng") — tạo/duyệt văn bản thật luôn phải qua một cú bấm
// rõ ràng của người dùng.

const MISSING_BOM_BUTTON_LABEL = __("Tạo BOM tự động cho bán thành phẩm");

frappe.ui.form.on("BOM", {
	item(frm) {
		// frm.set_intro NỐI THÊM banner chứ không thay thế (Layout.show_message dùng appendTo,
		// chỉ chuỗi rỗng mới xoá). Không dọn tay thì đổi Mặt Hàng vài lần là chồng một cột banner.
		// Chỗ này an toàn: intro của ERPNext trên BOM chỉ đặt khi Mặt Hàng là hàng cha có biến
		// thể, mà trường hợp đó không bao giờ tra ra BOM Template nên hai bên không giẫm nhau.
		frm._hkled_banners = {};
		frm.set_intro("");
		frm.remove_custom_button(MISSING_BOM_BUTTON_LABEL);
		frm._hkled_missing_sub_assembly_boms = [];

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
		set_banner_section(
			frm,
			"qty_defaulted",
			__(
				"{0} chưa có công thức số lượng và cũng chưa khai Số Lượng trên BOM Template {1}, nên hệ thống tạm điền Số Lượng = <b>1</b>. Nếu thực tế khác, sửa cột Số Lượng của thành phần đó trong BOM Template rồi chọn lại Mặt Hàng.",
				[names, frappe.utils.escape_html(res.template)]
			)
		);
	} else {
		set_banner_section(frm, "qty_defaulted", null);
	}

	show_missing_sub_assembly_banner(frm, res.missing_sub_assembly_boms || []);
}

// frm.set_intro NỐI THÊM banner chứ không thay thế (Layout.show_message dùng appendTo, chỉ chuỗi
// rỗng mới xoá) — nên không thể gọi frm.set_intro trực tiếp ở hai chỗ độc lập (qty_defaulted và
// missing_sub_assembly_boms), vì cập nhật chỗ này sẽ đè/nhân đôi chỗ kia. Hai hàm dưới đây gộp tất
// cả banner đang có thành MỘT khối, xoá sạch rồi vẽ lại mỗi lần một mục đổi.
function set_banner_section(frm, key, html) {
	frm._hkled_banners = frm._hkled_banners || {};
	if (html) {
		frm._hkled_banners[key] = html;
	} else {
		delete frm._hkled_banners[key];
	}
	render_banners(frm);
}

function render_banners(frm) {
	const sections = Object.values(frm._hkled_banners || {});
	frm.set_intro(sections.join("<hr>"), "orange");
}

function show_missing_sub_assembly_banner(frm, missing) {
	frm._hkled_missing_sub_assembly_boms = missing;
	frm.remove_custom_button(MISSING_BOM_BUTTON_LABEL);

	if (!missing.length) {
		set_banner_section(frm, "missing_boms", null);
		return;
	}

	const names = missing.map((code) => `<b>${frappe.utils.escape_html(code)}</b>`).join(", ");
	set_banner_section(
		frm,
		"missing_boms",
		__(
			"{0} là bán thành phẩm có BOM Template riêng nhưng CHƯA có BOM nào — nguyên vật liệu của chính nó chưa được tính. Bấm nút <b>{1}</b> để tạo, hoặc tự tạo BOM tay cho từng mặt hàng rồi chọn lại Mặt Hàng.",
			[names, MISSING_BOM_BUTTON_LABEL]
		)
	);

	frm.add_custom_button(MISSING_BOM_BUTTON_LABEL, () => create_missing_sub_assembly_boms(frm));
}

async function create_missing_sub_assembly_boms(frm) {
	const missing = frm._hkled_missing_sub_assembly_boms || [];
	if (!missing.length) {
		return;
	}

	const ok = await new Promise((resolve) => {
		frappe.confirm(
			__(
				"Sẽ tạo và DUYỆT {0} BOM mới cho: {1}.<br><br>Đây là chứng từ thật (is_default), không phải bản nháp. Tiếp tục?",
				[missing.length, missing.map((c) => `<b>${frappe.utils.escape_html(c)}</b>`).join(", ")]
			),
			() => resolve(true),
			() => resolve(false)
		);
	});
	if (!ok) {
		return;
	}

	frappe.dom.freeze(__("Đang tạo BOM tự động..."));
	const created = [];
	const failed = [];
	try {
		// Tuần tự — cùng lý do phải tuần tự ở fill_raw_materials: mỗi lệnh sinh/đọc dữ liệu thật,
		// bắn song song thì không kiểm soát được thứ tự con/cha khi hai bán thành phẩm dùng chung
		// một linh kiện đang được tạo BOM lần đầu.
		for (const item_code of missing) {
			try {
				const r = await frappe.call({
					method: "mbwnext_hkled.api.bom.auto_create_bom",
					args: { item_code, company: frm.doc.company },
				});
				created.push({ item_code, ...(r.message || {}) });
			} catch (e) {
				failed.push(item_code);
			}
		}
	} finally {
		frappe.dom.unfreeze();
	}

	if (created.length) {
		frappe.show_alert(
			{
				message: __("Đã tạo BOM cho {0} bán thành phẩm.", [created.length]),
				indicator: "green",
			},
			7
		);
	}
	if (failed.length) {
		frappe.msgprint({
			title: __("Không tạo được BOM"),
			message: __("Không tạo được BOM cho: {0}. Xem Console để biết chi tiết lỗi.", [
				failed.map((c) => frappe.utils.escape_html(c)).join(", "),
			]),
			indicator: "red",
		});
	}

	// BOM con vừa có thì nối lại vào các dòng đang hiện trên bảng — không dựng lại từ đầu để khỏi
	// mất số lượng/đơn giá người dùng có thể đã sửa tay ở các dòng khác.
	const created_codes = new Set(created.map((c) => c.item_code));
	const rows = (frm.doc.items || []).filter((row) => created_codes.has(row.item_code));
	for (const row of rows) {
		await frm.script_manager.trigger("item_code", row.doctype, row.name);
	}
	frm.refresh_field("items");

	show_missing_sub_assembly_banner(
		frm,
		(frm._hkled_missing_sub_assembly_boms || []).filter((c) => !created_codes.has(c))
	);
}
