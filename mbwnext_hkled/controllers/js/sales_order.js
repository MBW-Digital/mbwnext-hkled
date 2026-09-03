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

		// PM-FEAT-00023 — nút này KHÔNG chờ đơn duyệt. Sale cần biết đủ hàng hay không TRƯỚC
		// khi duyệt; bắt duyệt rồi mới cho xem là ngược thứ tự công việc. Chỉ cần đơn đã lưu,
		// vì API đọc dòng hàng từ cơ sở dữ liệu chứ không từ form.
		if (!frm.is_new()) {
			frm.add_custom_button(__("Kiểm Tra Tồn Kho"), () => mo_kiem_tra(frm));
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

	/* PM-FEAT-00023 — tích ô Ghim thì điền sẵn mức TỐI ĐA giữ được cho mọi dòng.
	   Anh Thắng chốt 02/09: "tích ghim thì hệ thống tự tính ra số lượng tối đa có thể ghim
	   và nhập vào ô số lượng ghim, người dùng có thể sửa tay".

	   ⚠ BỎ tích thì KHÔNG xoá số đã nhập (luật 2). Sale sửa tay 20 dòng rồi lỡ bỏ tích mà mất
	     sạch thì không có đường lấy lại — bỏ tích chỉ là TẠM NGỪNG áp dụng. */
	custom_ghim_ton_kha_dung(frm) {
		if (!frm.doc.custom_ghim_ton_kha_dung || frm.is_new()) return;
		dien_muc_toi_da(frm);
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

/* ══════════ PM-FEAT-00023 — Kiểm tra tồn kho và nguồn lực ══════════
   Đầu bài: docs/features/kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md
   Mockup khách duyệt 03/09: docs/mockups/ cùng tên.

   ⚠ Popup CHỈ ĐỂ XEM — không ghim vào đơn, không sinh chứng từ, không đụng Stock Ledger
     (chốt 19/08). Ô Giữ Chỗ sửa trên LƯỚI HÀNG HOÁ của đơn, không sửa trong popup
     (anh Thắng chốt cách 1, 03/09 09:11). Nút Tạo Yêu Cầu Mặt Hàng chỉ mở form mới
     điền sẵn, người dùng vẫn phải tự bấm Lưu.                                          */

const NHAN_NUT_PHIEU = "Tạo Yêu Cầu Mặt Hàng";

function dien_muc_toi_da(frm) {
	frappe.call({
		method: "mbwnext_hkled.api.kiem_tra_ton_kho.kiem_tra",
		args: { sales_order: frm.doc.name },
		freeze: true,
		freeze_message: __("Đang tính mức giữ chỗ tối đa…"),
		callback(r) {
			if (!r.message) return;
			const kha_dung = {};
			(r.message.bang1 || []).forEach((d) => (kha_dung[d.ma] = d.ton_kha_dung));
			let da_dien = 0;
			(frm.doc.items || []).forEach((row) => {
				// Tối đa = ít hơn giữa "đơn cần" và "kho còn". Không cho vượt tồn — anh Thắng
				// chốt 02/09 12:40; phần chênh hiện ở cột Thiếu chứ không mất đi.
				const tran = Math.min(flt(row.qty), flt(kha_dung[row.item_code] || 0));
				const dat = Math.max(0, tran);
				if (flt(row.custom_so_luong_giu_cho) !== dat) {
					frappe.model.set_value(row.doctype, row.name, "custom_so_luong_giu_cho", dat);
					da_dien += 1;
				}
			});
			frappe.show_alert({
				message: da_dien
					? __("Đã điền mức giữ chỗ tối đa cho {0} dòng. Sửa lại được ngay trên lưới.", [da_dien])
					: __("Không dòng nào đổi — mức giữ chỗ đang khớp tồn khả dụng."),
				indicator: "green",
			});
		},
	});
}

function mo_kiem_tra(frm) {
	frappe.call({
		method: "mbwnext_hkled.api.kiem_tra_ton_kho.kiem_tra",
		args: { sales_order: frm.doc.name },
		freeze: true,
		freeze_message: __("Đang kiểm tra tồn kho…"),
		callback(r) {
			if (r.message) ve_popup(frm, r.message);
		},
	});
}

function so(v) {
	return format_number(flt(v), null, 0);
}

function o_thieu(v) {
	// Thiếu thì tô đỏ. Đủ thì để 0 mờ đi — không tô xanh, vì "đủ" là trạng thái bình thường,
	// tô màu cả hai phía làm mắt không bắt được dòng nào cần chú ý.
	return flt(v) > 0
		? `<b style="color:var(--red-500)">${so(v)}</b>`
		: `<span class="text-muted">0</span>`;
}

function bang_1(dong) {
	const rows = dong
		.map(
			(d) => `<tr>
				<td>${frappe.utils.escape_html(d.ma)}</td>
				<td class="text-right">${so(d.can)}</td>
				<td class="text-right">${so(d.ton_thuc_te)}</td>
				<td class="text-right">${so(d.ton_kha_dung)}</td>
				<td class="text-right">${flt(d.dang_ghim) ? so(d.dang_ghim) + " đang ghim" : "—"}</td>
				<td class="text-right">${o_thieu(d.thieu)}</td>
			</tr>`
		)
		.join("");
	return `<h5>Bảng 1 · Mặt hàng trên đơn</h5>
		<p class="text-muted small">Cả hai cột tồn đều đã loại kho lỗi và kho trung chuyển.</p>
		<table class="table table-bordered small">
			<thead><tr>
				<th>Mặt hàng</th><th class="text-right">Cần</th><th class="text-right">Tồn thực tế</th>
				<th class="text-right">Tồn khả dụng</th><th class="text-right">Đơn khác giữ</th>
				<th class="text-right">Thiếu</th>
			</tr></thead>
			<tbody>${rows || '<tr><td colspan="6" class="text-muted">Đơn chưa có dòng hàng nào.</td></tr>'}</tbody>
		</table>`;
}

function bang_2(dong) {
	if (!dong.length) {
		return `<h5>Bảng 2 · Cần mua sau khi bóc định mức</h5>
			<p class="text-muted">Không phải bóc định mức — mọi mặt hàng trên đơn đều đủ tồn.</p>`;
	}
	const rows = dong
		.map((d) => {
			// Ô trống ở cột ngày đọc như "về ngay". Ghi thẳng chữ, đừng để trống — đúng chỗ
			// mục 8.2 của đầu bài đã dặn.
			const ngay = d.ngay_hang_ve
				? `${frappe.datetime.str_to_user(d.ngay_hang_ve)}<br><span class="text-muted small">về ${so(d.sl_ve)}</span>`
				: '<span class="text-muted">chưa có đơn mua</span>';
			return `<tr>
				<td>${frappe.utils.escape_html(d.ma)}</td>
				<td class="text-right">${so(d.can)}</td>
				<td class="text-right">${so(d.ton_thuc_te)}</td>
				<td class="text-right">${so(d.ton_kha_dung)}</td>
				<td class="text-right">${o_thieu(d.thieu)}</td>
				<td>${ngay}</td>
			</tr>`;
		})
		.join("");
	return `<h5>Bảng 2 · Cần mua sau khi bóc định mức</h5>
		<p class="text-muted small">Chỉ bóc phần <b>còn thiếu</b> của Bảng 1, không bóc cả phần cần.</p>
		<table class="table table-bordered small">
			<thead><tr>
				<th>Nguyên vật liệu</th><th class="text-right">Cần</th><th class="text-right">Tồn thực tế</th>
				<th class="text-right">Tồn khả dụng</th><th class="text-right">Thiếu</th>
				<th>Ngày hàng về · SL về</th>
			</tr></thead>
			<tbody>${rows}</tbody>
		</table>`;
}

function khoi_canh_bao(canh_bao) {
	if (!canh_bao || !canh_bao.length) return "";
	const li = canh_bao.map((c) => `<div>• ${frappe.utils.escape_html(c)}</div>`).join("");
	return `<div class="alert alert-warning small" style="margin-top:12px">
		<b>Cần để ý</b>${li}</div>`;
}

function ve_popup(frm, kq) {
	const thieu_b1 = (kq.bang1 || []).filter((d) => flt(d.thieu) > 0).length;
	const thieu_b2 = (kq.bang2 || []).filter((d) => flt(d.thieu) > 0).length;
	const ket_luan = thieu_b1 || thieu_b2
		? `<div class="alert alert-danger small"><b>Đơn này đang thiếu hàng.</b>
			${thieu_b1} mặt hàng trên đơn và ${thieu_b2} loại vật tư chưa đủ tồn.</div>`
		: `<div class="alert alert-success small"><b>Đơn này đủ hàng.</b></div>`;

	const d = new frappe.ui.Dialog({
		title: __("Kiểm tra tồn kho — {0}", [frm.doc.name]),
		size: "extra-large",
		fields: [{ fieldtype: "HTML", fieldname: "noi_dung" }],
		primary_action_label: __(NHAN_NUT_PHIEU),
		primary_action() {
			tao_phieu(frm, d);
		},
	});
	d.fields_dict.noi_dung.$wrapper.html(
		ket_luan +
			bang_1(kq.bang1 || []) +
			bang_2(kq.bang2 || []) +
			khoi_canh_bao(kq.canh_bao) +
			`<p class="text-muted small" style="margin-top:8px">
				Kết quả <b>chỉ để tham khảo</b>: không ghim vào đơn, không sinh chứng từ.
				Muốn đổi phần giữ chỗ thì sửa cột <b>Số Lượng Giữ Chỗ</b> ngay trên lưới hàng hoá.
				Tính trên ${kq.so_kho_tinh_ton} kho.</p>`
	);
	d.show();
}

function tao_phieu(frm, dialog) {
	frappe.call({
		method: "mbwnext_hkled.api.kiem_tra_ton_kho.tao_yeu_cau_mua_hang",
		args: { sales_order: frm.doc.name },
		freeze: true,
		freeze_message: __("Đang dựng phiếu…"),
		callback(r) {
			const kq = r.message;
			if (!kq) return;
			if (!kq.co_phieu) {
				frappe.msgprint({
					title: __(NHAN_NUT_PHIEU),
					message: frappe.utils.escape_html(kq.thong_bao),
					indicator: "blue",
				});
				return;
			}
			// Mở form MỚI điền sẵn, KHÔNG lưu hộ. Người dùng phải nhìn thấy nội dung rồi tự
			// bấm Lưu — chứng từ thật không được sinh ra bởi một cú bấm ở màn hình khác.
			dialog && dialog.hide();
			const doc = frappe.model.sync(kq.phieu)[0];
			frappe.set_route("Form", doc.doctype, doc.name);
			if (kq.ngay_bi_kep) {
				frappe.show_alert({
					message: __("Ngày giao của đơn đã qua nên Ngày Cần lấy theo hôm nay."),
					indicator: "orange",
				});
			}
		},
	});
}
