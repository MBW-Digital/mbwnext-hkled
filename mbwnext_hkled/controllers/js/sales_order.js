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

		// PM-FEAT-00023 — nút này KHÔNG chờ đơn duyệt, và cũng KHÔNG chờ đơn lưu. Sale cần biết
		// đủ hàng hay không TRƯỚC khi chốt đơn với khách; bắt lưu rồi mới cho xem là ngược thứ
		// tự công việc. Đơn chưa lưu thì `tham_so_don` gửi nguyên tài liệu sang máy chủ.
		frm.add_custom_button(__("Kiểm Tra Tồn Kho"), () => mo_kiem_tra(frm));

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
	     sạch thì không có đường lấy lại — bỏ tích chỉ là TẠM NGỪNG áp dụng.

	   ⚠ Bản đầu có thêm `|| frm.is_new()` ở đây và người dùng tích ô trên đơn mới thì KHÔNG có
	     gì xảy ra, cũng không có lời nào báo tại sao. Anh Thắng đụng ngay 03/09 10:32:
	     *"lúc mới tạo phiếu anh chọn sản phẩm xong tích ghim thì không thấy nó tính"*. Đã bỏ
	     chốt chặn đó — `kiem_tra` giờ nhận cả tài liệu chưa lưu. */
	custom_ghim_ton_kha_dung(frm) {
		if (!frm.doc.custom_ghim_ton_kha_dung) return;
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

	// PM-FEAT-00023: gõ quá tồn khả dụng thì kéo về mức tối đa ngay tại chỗ, đừng để người dùng
	// bấm Lưu rồi mới ăn thông báo lỗi từ server. Server vẫn chặn độc lập
	// (`python_hook/sales_order.py::chan_giu_cho_vuot_ton`) — đây chỉ là lớp cho êm tay.
	custom_so_luong_giu_cho(frm, cdt, cdn) {
		kep_giu_cho(frm, locals[cdt][cdn]);
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

// Đơn CHƯA LƯU LẦN NÀO thì `frm.doc.name` đang là `new-sales-order-…` — một cái tên không có
// trong cơ sở dữ liệu. Gửi tên đó sang là máy chủ ném lỗi và người dùng chỉ thấy ô số không
// nhúc nhích (anh Thắng báo 03/09 10:32). Lúc đó gửi nguyên tài liệu đi.
function tham_so_don(frm) {
	return frm.is_new() ? { doc: frm.doc } : { sales_order: frm.doc.name };
}

// Trần của một dòng = ít hơn giữa "đơn cần" và "kho còn", trừ tiếp phần các dòng KHÁC cùng mã
// trên chính đơn này đã giữ. Không trừ phần đó thì đơn 3 dòng cùng một mã sẽ giữ gấp ba.
function kep_giu_cho(frm, row) {
	// Đang trong lượt tự điền thì đừng chen vào: `dien_muc_toi_da` đã chia đúng phần rồi, kẹp
	// thêm ở đây chỉ làm bắn báo đỏ giữa một thao tác hoàn toàn bình thường.
	if (!row || !frm.doc.custom_ghim_ton_kha_dung || frm.__hkled_dang_dien) return;
	const moi = flt(row.custom_so_luong_giu_cho);
	if (moi <= 0) return;

	const ap_dung = (kha_dung) => {
		const cua_dong_khac = (frm.doc.items || [])
			.filter((r) => r.name !== row.name && r.item_code === row.item_code)
			.reduce((t, r) => t + flt(r.custom_so_luong_giu_cho), 0);
		const tran = Math.max(0, Math.min(flt(row.qty), flt(kha_dung) - cua_dong_khac));
		if (moi <= tran) return;

		frappe.model.set_value(row.doctype, row.name, "custom_so_luong_giu_cho", tran);
		frappe.show_alert({
			message: __("{0}: chỉ giữ chỗ được {1} — đã sửa lại giúp anh/chị.", [
				row.item_code,
				so(tran),
			]),
			indicator: "red",
		});
	};

	const cache = frm.__hkled_kha_dung;
	if (cache && row.item_code in cache) {
		ap_dung(cache[row.item_code]);
		return;
	}
	// Chưa có số trong tay thì hỏi server một lần rồi nhớ lại, đừng hỏi mỗi lần gõ phím.
	frappe.call({
		method: "mbwnext_hkled.api.kiem_tra_ton_kho.kiem_tra",
		args: tham_so_don(frm),
		callback(r) {
			if (!r.message) return;
			const kd = nho_kha_dung(frm, r.message);
			if (row.item_code in kd) ap_dung(kd[row.item_code]);
		},
	});
}

// Tồn khả dụng ở đây LUÔN là số đã trừ phần các đơn khác giữ (`kiem_tra` trả về vậy) và KHÔNG
// gồm phần chính đơn này đang giữ — nên dùng thẳng làm trần được, không phải cộng trừ gì thêm.
function nho_kha_dung(frm, du_lieu) {
	frm.__hkled_kha_dung = {};
	(du_lieu.bang1 || []).forEach((d) => (frm.__hkled_kha_dung[d.ma] = d.ton_kha_dung));
	return frm.__hkled_kha_dung;
}

function dien_muc_toi_da(frm) {
	frappe.call({
		method: "mbwnext_hkled.api.kiem_tra_ton_kho.kiem_tra",
		args: tham_so_don(frm),
		freeze: true,
		freeze_message: __("Đang tính mức giữ chỗ tối đa…"),
		callback(r) {
			if (!r.message) return;
			const kha_dung = nho_kha_dung(frm, r.message);

			// Chia theo thứ tự dòng và TRỪ DẦN. Nhiều dòng cùng một mã ăn chung một lượng tồn:
			// bản đầu tính từng dòng độc lập nên đơn 2 dòng × 5 cái trên tồn 1 được điền 1 + 1,
			// rồi lớp kẹp mới dọn về 0 + 1 kèm một dòng báo ĐỎ — người dùng chỉ tích một ô mà
			// tưởng mình vừa làm hỏng cái gì. Con số cuối vẫn đúng, nhưng đường đi thì sai.
			const con_lai = {};
			frm.__hkled_dang_dien = true;
			let da_dien = 0;
			(frm.doc.items || []).forEach((row) => {
				if (!(row.item_code in con_lai)) {
					con_lai[row.item_code] = flt(kha_dung[row.item_code] || 0);
				}
				// Tối đa = ít hơn giữa "đơn cần" và "phần kho còn lại sau các dòng trước".
				// Không cho vượt tồn — anh Thắng chốt 02/09 12:40; phần chênh hiện ở cột Thiếu
				// chứ không mất đi.
				const dat = Math.max(0, Math.min(flt(row.qty), con_lai[row.item_code]));
				con_lai[row.item_code] -= dat;
				if (flt(row.custom_so_luong_giu_cho) !== dat) {
					frappe.model.set_value(row.doctype, row.name, "custom_so_luong_giu_cho", dat);
					da_dien += 1;
				}
			});
			frm.__hkled_dang_dien = false;
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
		args: tham_so_don(frm),
		freeze: true,
		freeze_message: __("Đang kiểm tra tồn kho…"),
		callback(r) {
			if (!r.message) return;
			nho_kha_dung(frm, r.message);
			ve_popup(frm, r.message);
		},
	});
}

// Số lượng cho người đọc. `format_number` trần cho ra 3 chữ số thập phân — "0,000" đọc như
// số tiền, mà HKLED thì đếm cái đèn. Nhưng ép cứng 0 chữ số cũng sai: UOM Kg/m/Lít trên site
// đều cho phép số lẻ, ép 0 là 2,5 hiện thành 3 — thay một câu khó đọc bằng một câu SAI.
// Nên: nguyên thì bỏ hẳn phần thập phân, lẻ thì giữ nguyên phần lẻ, chỉ cắt số 0 thừa ở đuôi.
function so(v) {
	const n = flt(v);
	if (Number.isInteger(n)) return format_number(n, null, 0);
	return format_number(n, null, 3).replace(/0+$/, "").replace(/[.,]$/, "");
}

function o_thieu(v) {
	// Thiếu thì tô đỏ. Đủ thì để 0 mờ đi — không tô xanh, vì "đủ" là trạng thái bình thường,
	// tô màu cả hai phía làm mắt không bắt được dòng nào cần chú ý.
	return flt(v) > 0
		? `<b style="color:var(--red-500)">${so(v)}</b>`
		: `<span class="text-muted">0</span>`;
}

// Bảng 1b / Bảng 2b — bung ra xem ĐƠN NÀO đang giữ mã này.
//
// ⚠ Hai bảng này có trong mockup (1b bản 6, 2b bản 7) nhưng KHÔNG có trong bản đặc tả, nên
//   vòng code đầu bỏ sót cả hai. Anh Thắng hỏi lại 03/09 16:30. Ghi lại đây để lần sau ai đọc
//   file này cũng thấy: mockup đổi thì phải kéo sang đặc tả, code chỉ đọc đặc tả.
//
// ⚠ KHÔNG hiện tên khách hàng — anh Thắng chốt trong mockup bản 6. Chỉ người phụ trách.
function nut_chi_tiet(ct, id, nhan) {
	if (!ct || !ct.dong || !ct.dong.length) return nhan;
	return `<button type="button" class="btn btn-link btn-xs hkled-ct"
		data-mo="${id}" style="padding:0;text-decoration:underline">${nhan} <span class="hkled-mui">▸</span></button>`;
}

function hang_chi_tiet(ct, id, ma, la_gian_tiep) {
	if (!ct || !ct.dong || !ct.dong.length) return "";
	const co_boc = ct.dong.some((r) => r.tu_ma);
	const cot = co_boc ? 5 : 4;
	const rows = ct.dong
		.map((r) => {
			const boc = co_boc
				? `<td>${
						r.tu_ma
							? `${frappe.utils.escape_html(r.tu_ma)} <span class="text-muted">· ${so(r.tu_sl)} × ${format_number(flt(r.dinh_muc), null, 2)}</span>`
							: '<span class="text-muted">bán thẳng mã này</span>'
				  }</td>`
				: "";
			return `<tr>
				<td>${frappe.utils.escape_html(r.don)}</td>
				<td>${frappe.utils.escape_html(r.nguoi || "—")}</td>
				<td class="text-right">${so(r.giu)}</td>
				${boc}
				<td>${r.ngay ? frappe.datetime.str_to_user(r.ngay) : '<span class="text-muted">chưa có</span>'}</td>
			</tr>`;
		})
		.join("");

	// Dòng cộng phải nói đúng phần ĐÃ TRỪ, không phải tổng ghim. Hai số này lệch nhau khi đơn
	// khác ghim nhiều hơn số đang có trong kho — đúng ca anh Thắng bắt được 03/09 16:34.
	const lech = flt(ct.tong_ghim) - flt(ct.da_tru);
	const cong = lech > 0.001
		? `Cộng <b>${so(ct.tong_ghim)}</b> — nhưng kho không đủ nên chỉ trừ <b>${so(ct.da_tru)}</b> khỏi tồn khả dụng`
		: `Cộng — đúng phần đã trừ khỏi tồn khả dụng: <b>${so(ct.da_tru)}</b>`;

	const con_lai = ct.con_lai
		? `<p class="text-muted small" style="margin:4px 0 0">…và ${ct.con_lai} đơn nữa không hiện ở đây; dòng Cộng đã tính đủ tất cả.</p>`
		: "";

	return `<tr class="hkled-ct-hang" id="${id}" style="display:none">
		<td colspan="6" style="background:var(--fg-color, #fafafa)">
			<div style="padding:4px 2px 2px">
				<b>Bảng ${la_gian_tiep ? "2b" : "1b"} · Đơn đang ghim ${frappe.utils.escape_html(ma)}</b>
				<span class="text-muted small"> · tối đa 5 đơn có ngày lấy hàng xa nhất · không hiện tên khách hàng</span>
			</div>
			<table class="table table-bordered small" style="margin-bottom:4px">
				<thead><tr>
					<th>Mã đơn</th><th>Người phụ trách</th><th class="text-right">Đang ghim</th>
					${co_boc ? "<th>Bóc ra từ</th>" : ""}
					<th>Ngày lấy hàng dự kiến</th>
				</tr></thead>
				<tbody>${rows}</tbody>
				<tfoot><tr><td colspan="${cot}" class="text-muted small">${cong}</td></tr></tfoot>
			</table>
			${con_lai}
		</td>
	</tr>`;
}

function bang_1(dong) {
	const rows = dong
		.map((d, i) => {
			const id = `hkled-ct-b1-${i}`;
			const nhan = flt(d.dang_ghim) ? so(d.dang_ghim) + " đang ghim" : "—";
			return `<tr>
				<td>${frappe.utils.escape_html(d.ma)}</td>
				<td class="text-right">${so(d.can)}</td>
				<td class="text-right">${so(d.ton_thuc_te)}</td>
				<td class="text-right">${so(d.ton_kha_dung)}</td>
				<td class="text-right">${nut_chi_tiet(d.chi_tiet_ghim, id, nhan)}</td>
				<td class="text-right">${o_thieu(d.thieu)}</td>
			</tr>${hang_chi_tiet(d.chi_tiet_ghim, id, d.ma, false)}`;
		})
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
		.map((d, i) => {
			// Ô trống ở cột ngày đọc như "về ngay". Ghi thẳng chữ, đừng để trống — đúng chỗ
			// mục 8.2 của đầu bài đã dặn.
			// ⚠ Đơn mua QUÁ HẠN phải hiện rõ, không lẫn vào đơn đúng hẹn. Trước 04/09 truy vấn
			//   lọc `schedule_date >= CURDATE()` nên đơn trễ bị giấu sạch — có mã giấu 100% và
			//   ô này ghi "chưa có đơn mua" trong khi đơn mua có thật. Đơn trễ chính là đơn
			//   người lập kế hoạch phải đi giục, giấu nó là giấu đúng thứ cần hiện.
			const ngay = d.ngay_hang_ve
				? `${frappe.datetime.str_to_user(d.ngay_hang_ve)}<br><span class="text-muted small">về ${so(d.sl_ve)}</span>`
					+ (d.tre_ngay > 0
						? `<br><span class="text-danger small">quá hạn ${so(d.tre_ngay)} ngày</span>`
						: '')
				: '<span class="text-muted">chưa có đơn mua</span>';
			// Bảng 2 không có cột "Đơn khác giữ" nên nút bung nằm ngay dưới mã vật tư —
			// vẫn phải có, vì vật tư bị ghim GIÁN TIẾP là chỗ khó lần ra nhất.
			const id = `hkled-ct-b2-${i}`;
			const ct = d.chi_tiet_ghim;
			const nut = ct && ct.dong && ct.dong.length
				? `<br>${nut_chi_tiet(ct, id, so(ct.tong_ghim) + " đang ghim")}`
				: "";
			return `<tr>
				<td>${frappe.utils.escape_html(d.ma)}${nut}</td>
				<td class="text-right">${so(d.can)}</td>
				<td class="text-right">${so(d.ton_thuc_te)}</td>
				<td class="text-right">${so(d.ton_kha_dung)}</td>
				<td class="text-right">${o_thieu(d.thieu)}</td>
				<td>${ngay}</td>
			</tr>${hang_chi_tiet(ct, id, d.ma, true)}`;
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

// Bảng 3 — nguồn lực nhân sự.
//
// ⚠ Bảng này KHÔNG được phép nói "Đủ" khi chưa đo được. Đầu bài đã ghi rõ đây là rủi ro R2:
//   *"Bảng 3 sẽ ra gần 0 phút và luôn kết luận Đủ — sai mà không có gì báo."* Đo trên site
//   03/09 thì CẢ HAI VẾ đều rỗng (lịch làm việc chỉ tới 31/08; 59.743/59.746 mặt hàng chưa
//   khai Thời Gian Sản Xuất), nên 0 so 0 sẽ ra "đủ" ở mọi đơn. Máy chủ trả về trạng thái
//   `chua_tinh_duoc` riêng, và ở đây phải hiện nó ra bằng MÀU KHÁC + nói rõ thiếu cái gì.
const NHAN_KET_LUAN = {
	du: ["Đủ nhân lực", "green"],
	khong_du: ["KHÔNG đủ nhân lực", "red"],
	chua_tinh_duoc: ["Chưa tính được", "orange"],
	khong_ap_dung: ["Không áp dụng", "gray"],
};

function phut(v) {
	const n = flt(v);
	if (!n) return "0";
	// Phút trần rất khó hình dung ở mức hàng nghìn — kèm số giờ cho dễ đọc, không thay thế.
	return n >= 60 ? `${so(n)} <span class="text-muted">(≈ ${so(n / 60)} giờ)</span>` : so(n);
}

function bang_3(b3) {
	if (!b3) return "";
	const [nhan, mau] = NHAN_KET_LUAN[b3.ket_luan] || NHAN_KET_LUAN.chua_tinh_duoc;

	const ly_do = (b3.ly_do || []).length
		? `<div class="small text-muted" style="margin-top:6px">
				${b3.ly_do.map((x) => `• ${frappe.utils.escape_html(x)}`).join("<br>")}
			</div>`
		: "";

	const thieu = (b3.thieu_dinh_muc || []).length
		? `<div class="small" style="margin-top:6px">
				<b style="color:var(--orange-500)">Chưa khai Thời Gian Sản Xuất
				(${b3.thieu_dinh_muc.length} mặt hàng):</b>
				${b3.thieu_dinh_muc.slice(0, 12).map((m) => frappe.utils.escape_html(m)).join(" · ")}
				${b3.thieu_dinh_muc.length > 12 ? "…" : ""}
			</div>`
		: "";

	return `
		<h6 style="margin-top:16px">Bảng 3 · Nguồn lực nhân sự</h6>
		<p class="text-muted small" style="margin-bottom:6px">
			Tính từ <b>${b3.tu_ngay}</b> đến <b>${b3.den_ngay}</b> (ngày giao của đơn),
			trên ${b3.so_nhan_su_co_lich} nhân sự có lịch làm việc.
			Đơn vị là <b>phút chuẩn</b> — đã nhân Năng Lực của từng người.
		</p>
		<table class="table table-bordered table-sm small" style="margin-bottom:0">
			<thead><tr>
				<th>Tổng theo lịch</th><th>Đã phân bổ</th><th>Còn lại</th>
				<th>Đơn này cần</th><th>Kết luận</th>
			</tr></thead>
			<tbody><tr>
				<td>${phut(b3.tong_theo_lich)}</td>
				<td>${phut(b3.da_phan_bo)}</td>
				<td>${phut(b3.con_lai)}</td>
				<td>${phut(b3.don_can)}</td>
				<td><b style="color:var(--${mau}-500)">${nhan}</b></td>
			</tr></tbody>
		</table>
		${ly_do}${thieu}`;
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
	// Dòng kết luận gộp (mục 6 đầu bài): trạng thái vật tư CỘNG trạng thái nhân lực, một câu.
	// "Không áp dụng" thì im — đơn không có hàng sản xuất mà nói về nhân lực là gây nhiễu.
	const b3 = kq.bang3 || {};
	const cau_nhan_luc = {
		du: " Nhân lực đủ.",
		khong_du: " <b>Nhân lực KHÔNG đủ.</b>",
		chua_tinh_duoc: " <b>Nhân lực chưa tính được</b> — xem Bảng 3.",
	}[b3.ket_luan] || "";

	// Chỉ kể vế nào THẬT SỰ thiếu. Bản đầu luôn in cả hai vế nên ra câu "1 mặt hàng trên đơn và
	// 0 loại vật tư chưa đủ tồn" — đọc như thể số 0 cũng là một vấn đề.
	const ve = [];
	if (thieu_b1) ve.push(`${thieu_b1} mặt hàng trên đơn`);
	if (thieu_b2) ve.push(`${thieu_b2} loại vật tư`);
	const vat_tu = ve.length
		? `<b>Đơn này đang thiếu hàng.</b> ${ve.join(" và ")} chưa đủ tồn.`
		: "<b>Đơn này đủ hàng.</b>";
	// Nhân lực chưa đo được hoặc không đủ thì KHÔNG được để nền xanh: người đọc lướt chỉ nhìn màu.
	const nen = thieu_b1 || thieu_b2 || b3.ket_luan === "khong_du"
		? "alert-danger"
		: b3.ket_luan === "chua_tinh_duoc"
		? "alert-warning"
		: "alert-success";
	const ket_luan = `<div class="alert ${nen} small">${vat_tu}${cau_nhan_luc}</div>`;

	const d = new frappe.ui.Dialog({
		title: frm.is_new()
			? __("Kiểm tra tồn kho — đơn chưa lưu")
			: __("Kiểm tra tồn kho — {0}", [frm.doc.name]),
		size: "extra-large",
		fields: [{ fieldtype: "HTML", fieldname: "noi_dung" }],
		// Đơn chưa lưu thì KHÔNG cho tạo phiếu: phiếu phải trỏ ngược về số Đơn Bán, mà số đó
		// chưa tồn tại. Xem tồn thì vẫn xem được — đó mới là việc sale cần trước khi chốt đơn.
		primary_action_label: frm.is_new() ? undefined : __(NHAN_NUT_PHIEU),
		primary_action: frm.is_new()
			? undefined
			: () => {
					tao_phieu(frm, d);
			  },
	});
	d.fields_dict.noi_dung.$wrapper.html(
		ket_luan +
			bang_1(kq.bang1 || []) +
			bang_2(kq.bang2 || []) +
			bang_3(kq.bang3) +
			khoi_canh_bao(kq.canh_bao) +
			(frm.is_new()
				? `<p class="text-muted small" style="margin-top:8px">
						Đơn <b>chưa lưu</b> nên chưa tạo được Yêu Cầu Mặt Hàng — phiếu phải trỏ về số
						đơn, mà số đó chỉ có sau khi bấm Lưu. Phần xem tồn thì đã tính đủ.
					</p>`
				: "") +
			`<p class="text-muted small" style="margin-top:8px">
				Kết quả <b>chỉ để tham khảo</b>: không ghim vào đơn, không sinh chứng từ.
				Muốn đổi phần giữ chỗ thì sửa cột <b>Số Lượng Giữ Chỗ</b> ngay trên lưới hàng hoá.
				Tính trên ${kq.so_kho_tinh_ton} kho.</p>`
	);

	// Bung/gập Bảng 1b · 2b. Gắn ủy quyền trên wrapper thay vì từng nút: nội dung được dựng
	// bằng chuỗi HTML nên nút chưa tồn tại lúc gắn.
	d.fields_dict.noi_dung.$wrapper.on("click", ".hkled-ct", function () {
		const hang = document.getElementById($(this).data("mo"));
		if (!hang) return;
		const mo = hang.style.display === "none";
		hang.style.display = mo ? "" : "none";
		$(this).find(".hkled-mui").text(mo ? "▾" : "▸");
	});

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
			// 🔴 THÊM 05/09 — anh Thắng báo 15:04: *"anh thử lại ấn nút lần thứ 2 chưa thấy
			// cảnh báo gì"*. Anh ấy đúng nguyên văn: máy chủ VẪN trả `canh_bao`, nhưng nhánh
			// này **vứt đi**. `khoi_canh_bao()` chỉ dùng trong hộp thoại Kiểm Tra Tồn Kho.
			//
			// Cảnh báo nặng nhất ở đây là *"đơn này đã có phiếu yêu cầu mặt hàng rồi"* — bỏ
			// nó đi thì người dùng lập phiếu trùng mà không biết, tức mua trùng bằng tiền thật.
			//
			// Hiện SAU khi chuyển trang: hộp thoại nổi lên trên phiếu vừa dựng, người dùng đọc
			// rồi mới quyết định bấm Lưu. Dùng `msgprint` chứ không `show_alert` — alert tự tắt
			// sau vài giây, mà đây là thứ phải đọc.
			if (kq.canh_bao && kq.canh_bao.length) {
				frappe.msgprint({
					title: __("Đọc trước khi lưu phiếu"),
					message: khoi_canh_bao(kq.canh_bao),
					indicator: "orange",
				});
			}
		},
	});
}
