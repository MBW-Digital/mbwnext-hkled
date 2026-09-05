// Phiếu Nhập Mua — nút Phân Bổ (PM-FEAT-00036, Phần IV.2).
//
// Đầu bài anh Thắng 31/08: hàng về thì người dùng bấm một nút, hệ thống chia phần tồn khả dụng
// vào phần ghim của những Đơn Bán chưa ghim đủ, ưu tiên đơn cần gấp trước.

frappe.ui.form.on("Purchase Receipt", {
	refresh(frm) {
		// ⚠ Chỉ hiện trên phiếu ĐÃ DUYỆT. Hàng chỉ thực sự vào kho khi phiếu được duyệt; bấm
		//   trên bản nháp là chia hàng chưa có. Máy chủ cũng chặn lần nữa — nút này ẩn đi để
		//   người dùng không phải gặp câu lỗi mới hiểu.
		if (frm.doc.docstatus !== 1) return;

		frm.add_custom_button(__("Phân Bổ"), () => phan_bo(frm));
	},
});

function phan_bo(frm) {
	frappe.call({
		method: "mbwnext_hkled.api.ghim_vat_tu.phan_bo",
		args: { purchase_receipt: frm.doc.name },
		freeze: true,
		freeze_message: __("Đang chia hàng cho các đơn…"),
		callback: (r) => {
			if (!r.message) return;
			hien_ket_qua(r.message);
			frm.reload_doc();
		},
	});
}

function so(n) {
	// Cùng luật với `_so()` bên Python và `so()` bên sales_order.js: nguyên thì bỏ phần thập
	// phân, lẻ thì giữ, cắt số 0 thừa ở đuôi. Sửa một bên thì sửa cả ba.
	n = flt(n);
	return Number.isInteger(n)
		? format_number(n, null, 0)
		: format_number(n, null, 3).replace(/0+$/, "").replace(/[.,]$/, "");
}

function hien_ket_qua(kq) {
	const phan = [];

	if (kq.dong && kq.dong.length) {
		const hang = kq.dong
			.map(
				(d) =>
					`<tr><td>${frappe.utils.escape_html(d.ma)}</td>
					 <td>${frappe.utils.escape_html(d.don)}</td>
					 <td class="text-right"><b>${so(d.them)}</b></td>
					 <td>${frappe.utils.escape_html(d.loai)}</td></tr>`
			)
			.join("");
		phan.push(`
			<p><b>${__("Đã chia")}:</b></p>
			<table class="table table-bordered table-sm">
				<thead><tr>
					<th>${__("Mặt hàng")}</th><th>${__("Đơn bán")}</th>
					<th class="text-right">${__("Ghim thêm")}</th><th>${__("Loại")}</th>
				</tr></thead>
				<tbody>${hang}</tbody>
			</table>`);
	} else {
		phan.push(
			`<p>${__(
				"Không chia được gì thêm — hoặc các đơn đã ghim đủ, hoặc hàng vừa về đã có chủ."
			)}</p>`
		);
	}

	// ⚠ Ba khối dưới đây là phần QUAN TRỌNG NHẤT của hộp thoại, không phải phần phụ. Không nói
	//   ra thì người dùng thấy "không chia được gì" mà không biết vì sao — đúng loại im lặng mà
	//   cả Phần IV sinh ra để chặn.
	if (kq.kho_ngoai_tap && kq.kho_ngoai_tap.length) {
		const d = kq.kho_ngoai_tap
			.map(
				(x) =>
					`<li><b>${frappe.utils.escape_html(x.ma)}</b> → ${frappe.utils.escape_html(x.kho)}</li>`
			)
			.join("");
		phan.push(`
			<div class="alert alert-warning">
				<b>${__("Có mặt hàng nhập vào kho không được tính tồn")}</b> —
				${__("hàng về thật nhưng hệ thống chưa coi là tồn khả dụng nên không chia được:")}
				<ul>${d}</ul>
			</div>`);
	}

	if (kq.bo_qua_chua_ghim && kq.bo_qua_chua_ghim.length) {
		const d = kq.bo_qua_chua_ghim
			.map(
				(x) =>
					`<li>${frappe.utils.escape_html(x.don)} — ${frappe.utils.escape_html(
						x.ma
					)}: ${__("còn thiếu")} <b>${so(x.con_thieu)}</b></li>`
			)
			.join("");
		phan.push(`
			<div class="alert alert-info">
				<b>${__("Đơn đang thiếu mã này nhưng CHƯA bật Ghim Tồn Khả Dụng")}</b> —
				${__("không được chia. Bật Ghim trên đơn rồi bấm lại nếu muốn chia cho các đơn này:")}
				<ul>${d}</ul>
			</div>`);
	}

	if (kq.canh_bao && kq.canh_bao.length) {
		const d = kq.canh_bao.map((x) => `<li>${frappe.utils.escape_html(x)}</li>`).join("");
		phan.push(
			`<div class="alert alert-danger"><b>${__(
				"Phần giữ chỗ đang có chỗ không khớp"
			)}</b><ul>${d}</ul></div>`
		);
	}

	frappe.msgprint({
		title: __("Phân bổ hàng về"),
		indicator: kq.canh_bao && kq.canh_bao.length ? "red" : "green",
		message: phan.join(""),
		wide: true,
	});
}
