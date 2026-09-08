// Bảng giá niêm yết — PM-FEAT-00045.
//
// Đầu bài:  docs/features/xuat-bang-gia-niem-yet.md
// Mockup:   docs/mockups/xuat-bang-gia-niem-yet.html  (bản vẽ bấm được, anh Thắng đã duyệt 08/09)
//
// BA LUẬT CỦA MÀN HÌNH NÀY, đừng gỡ cái nào:
//
//   1. Cột "Giá niêm yết" luôn TÍNH LẠI theo dữ liệu hiện tại; cột "Đang áp dụng" là con số sales
//      đang nhìn thấy. Hai cột lệch nhau nghĩa là có thay đổi CHƯA được đẩy sang.
//
//   2. KHÔNG bao giờ tự đẩy giá sang phần bán hàng. Chốt trong `notes` của PM Feature: "không
//      được tự ý cập nhật" — vì đổi giá niêm yết làm lệch hoa hồng của những đơn đã phát sinh.
//      Chỉ nút "Cập nhật giá niêm yết" mới ghi, và chỉ cho những dòng người dùng đã tick.
//
//   3. Mặt hàng KHÔNG tính được giá thì hiện kèm chữ "không tính được" (anh Thắng chốt 16:39),
//      và KHÔNG tick chọn được — để không ai lỡ đẩy một ô trống sang cho sales.
//
// ⚠ Vì sao có giới hạn số dòng và vì sao phải NÓI RA: site có hơn 61 nghìn mặt hàng. Dựng hết một
//   lượt là treo trình duyệt. Nhưng một bảng bị cắt trông y hệt một bảng đầy đủ — nên luôn hiện
//   "đang xem N trên tổng M".

frappe.pages["bang-gia-niem-yet"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Bảng giá niêm yết"),
		single_column: true,
	});
	new mbwnext_hkled.BangGiaNiemYet(page);
};

frappe.provide("mbwnext_hkled");

mbwnext_hkled.BangGiaNiemYet = class BangGiaNiemYet {
	constructor(page) {
		this.page = page;
		this.dong = [];
		this.chon = new Set();
		this.dung_khung();
		this.tai();
	}

	// ── Khung ────────────────────────────────────────────────────────────────

	dung_khung() {
		const p = this.page;

		this.f_nhom = p.add_field({
			fieldname: "nhom_hang",
			label: __("Nhóm mặt hàng"),
			fieldtype: "Link",
			options: "Item Group",
			change: () => this.tai(),
		});
		this.f_cha = p.add_field({
			fieldname: "mat_hang_cha",
			label: __("Mặt hàng cha"),
			fieldtype: "Link",
			options: "Item",
			get_query: () => ({ filters: { has_variants: 1 } }),
			change: () => this.tai(),
		});
		this.f_loc = p.add_field({
			fieldname: "loc",
			label: __("Hiện"),
			fieldtype: "Select",
			options: [
				{ value: "tat_ca", label: __("Tất cả mặt hàng") },
				{ value: "tinh_duoc", label: __("Chỉ dòng tính được giá") },
				{ value: "lech", label: __("Chỉ dòng đang lệch") },
			],
			default: "tat_ca",
			change: () => this.tai(),
		});
		this.f_so_dong = p.add_field({
			fieldname: "gioi_han",
			label: __("Số dòng tối đa"),
			fieldtype: "Select",
			options: ["100", "200", "500", "1000"],
			default: "200",
			change: () => this.tai(),
		});

		p.set_primary_action(__("Cập nhật giá niêm yết"), () => this.cap_nhat());
		p.set_secondary_action(__("Xuất Excel"), () => this.xuat());

		p.add_menu_item(__("Cài đặt tỷ lệ"), () =>
			frappe.set_route("Form", "HKLed Pricing Setting")
		);

		this.$than = $(`
			<div class="bgny">
				<div class="bgny-tom"></div>
				<div class="bgny-bang"></div>
			</div>
		`).appendTo(p.main);
	}

	// ── Nạp ──────────────────────────────────────────────────────────────────

	tai() {
		const loc = this.f_loc.get_value() || "tat_ca";
		this.$than.find(".bgny-bang").html(
			`<div class="bgny-trong">${__("Đang tính…")}</div>`
		);

		frappe.call({
			method: "mbwnext_hkled.api.gia_niem_yet.bang_gia",
			args: {
				nhom_hang: this.f_nhom.get_value() || null,
				mat_hang_cha: this.f_cha.get_value() || null,
				chi_tinh_duoc: loc === "tinh_duoc" ? 1 : 0,
				chi_lech: loc === "lech" ? 1 : 0,
				gioi_han: this.f_so_dong.get_value() || 200,
			},
			callback: (r) => {
				if (!r.message) return;
				this.kq = r.message;
				this.dong = r.message.dong;
				// Bỏ khỏi danh sách chọn những mã không còn trong lưới, nếu không thì bấm Cập nhật
				// sẽ ghi cho cả mặt hàng người dùng không còn nhìn thấy.
				const co = new Set(this.dong.map((d) => d.ma_hang));
				this.chon = new Set([...this.chon].filter((m) => co.has(m)));
				this.ve();
			},
		});
	}

	// ── Vẽ ───────────────────────────────────────────────────────────────────

	so(n) {
		return n === null || n === undefined ? "—" : format_number(n, null, 0);
	}

	ve() {
		const k = this.kq;
		const tinh_duoc = this.dong.filter((d) => d.gia_niem_yet !== null).length;
		const lech = this.dong.filter((d) => d.lech).length;

		let tom = `
			<div class="bgny-chip-hang">
				<span class="bgny-chip">${__("Hao phí")} <b>${k.hao_phi}%</b></span>
				<span class="bgny-chip">${__("Tỷ lệ tính giá niêm yết")} <b>${k.ty_le_niem_yet}%</b></span>
				<span class="bgny-chip">${__("Ghi vào bảng giá")} <b>${frappe.utils.escape_html(k.bang_gia)}</b></span>
				<span class="bgny-chip ${lech ? "bgny-chip-lech" : ""}">${__("Đang lệch")} <b>${lech}</b></span>
			</div>`;

		// ⚠ Bảng bị cắt phải NÓI RA. Xem docstring đầu file.
		if (k.bi_cat) {
			tom += `<div class="bgny-canh">${__(
				"Đang xem <b>{0}</b> trên tổng <b>{1}</b> mặt hàng. Lọc theo nhóm hoặc mặt hàng cha để xem đúng phần cần, hoặc tăng số dòng tối đa.",
				[this.dong.length, format_number(k.tong, null, 0)]
			)}</div>`;
		}
		if (tinh_duoc === 0 && this.dong.length) {
			tom += `<div class="bgny-canh bgny-canh-do">${__(
				"Không mặt hàng nào trong danh sách này tính được giá niêm yết. Nguyên nhân nằm ở cột <b>Giá vốn</b> — mặt hàng mua thì cần một đơn mua đã duyệt, mặt hàng sản xuất thì cần định mức mặc định có giá thành."
			)}</div>`;
		}
		this.$than.find(".bgny-tom").html(tom);

		if (!this.dong.length) {
			this.$than.find(".bgny-bang").html(
				`<div class="bgny-trong">${__("Không có mặt hàng nào khớp bộ lọc.")}</div>`
			);
			this.dem();
			return;
		}

		const h = [];
		h.push(`<div class="bgny-cuon"><table class="bgny-tb"><thead><tr>
			<th class="bgny-tick"><input type="checkbox" class="bgny-all"></th>
			<th>${__("Mã mặt hàng")}</th>
			<th>${__("Tên mặt hàng")}</th>
			<th class="num">${__("Giá vốn")}</th>
			<th class="num">${__("R&D")}</th>
			<th class="num">${__("Lợi nhuận")}</th>
			<th class="num">${__("Cộng")}</th>
			<th class="num">${__("Giá niêm yết")}</th>
			<th class="num">${__("Đang áp dụng")}</th>
		</tr></thead><tbody>`);

		this.dong.forEach((d) => {
			const duoc = d.gia_niem_yet !== null;
			h.push(`<tr class="${duoc ? "" : "bgny-mo"}" data-ma="${frappe.utils.escape_html(d.ma_hang)}">
				<td class="bgny-tick">${
					duoc
						? `<input type="checkbox" class="bgny-mot" ${this.chon.has(d.ma_hang) ? "checked" : ""}>`
						: `<span class="text-muted" title="${__("Chưa tính được giá nên không chọn được")}">–</span>`
				}</td>
				<td><a href="/app/item/${encodeURIComponent(d.ma_hang)}" target="_blank">${frappe.utils.escape_html(d.ma_hang)}</a></td>
				<td class="bgny-ten">${frappe.utils.escape_html(d.ten_hang || "")}</td>
				<td class="num">${
					duoc
						? this.so(d.cost)
						: `<span class="bgny-khong" title="${frappe.utils.escape_html(d.ly_do || "")}">${__("chưa có")}</span>`
				}</td>
				<td class="num text-muted">${d.rnd}%</td>
				<td class="num text-muted">${d.loi_nhuan}%</td>
				<td class="num">${this.so(d.cong)}</td>
				<td class="num"><b>${duoc ? this.so(d.gia_niem_yet) : `<span class="bgny-khong">${__("không tính được")}</span>`}</b></td>
				<td class="num ${d.lech ? "bgny-lech" : "text-muted"}">${this.so(d.dang_ap_dung)}${d.lech ? " ▲" : ""}</td>
			</tr>`);
		});
		h.push("</tbody></table></div>");
		this.$than.find(".bgny-bang").html(h.join(""));

		const $b = this.$than;
		$b.find(".bgny-mot").on("change", (e) => {
			const ma = $(e.currentTarget).closest("tr").data("ma");
			if (e.currentTarget.checked) this.chon.add(ma);
			else this.chon.delete(ma);
			this.dem();
		});
		$b.find(".bgny-all").on("change", (e) => {
			const v = e.currentTarget.checked;
			this.dong.forEach((d) => {
				if (d.gia_niem_yet === null) return;
				if (v) this.chon.add(d.ma_hang);
				else this.chon.delete(d.ma_hang);
			});
			this.ve();
		});
		this.dem();
	}

	dem() {
		const n = this.chon.size;
		const co = this.dong.filter((d) => d.gia_niem_yet !== null);
		this.$than
			.find(".bgny-all")
			.prop("checked", co.length > 0 && co.every((d) => this.chon.has(d.ma_hang)));
		this.page.set_primary_action(
			n ? __("Cập nhật giá niêm yết ({0})", [n]) : __("Cập nhật giá niêm yết"),
			() => this.cap_nhat()
		);
		this.page.set_secondary_action(
			n ? __("Xuất Excel ({0})", [n]) : __("Xuất Excel"),
			() => this.xuat()
		);
	}

	// ── Hai nút ──────────────────────────────────────────────────────────────

	danh_sach() {
		if (!this.chon.size) {
			frappe.msgprint({
				title: __("Chưa chọn mặt hàng"),
				message: __("Tick chọn ít nhất một dòng trong bảng rồi bấm lại."),
				indicator: "orange",
			});
			return null;
		}
		return [...this.chon];
	}

	cap_nhat() {
		const ds = this.danh_sach();
		if (!ds) return;

		// 🔴 Hỏi lại trước khi ghi. Nút này đổi con số SALES NHÌN THẤY lúc lập đơn — không phải
		//    thao tác hoàn tác được bằng Ctrl+Z. Nêu rõ số lượng và tên bảng giá trong câu hỏi.
		frappe.confirm(
			__(
				"Đẩy giá niêm yết mới của <b>{0}</b> mặt hàng sang bảng giá <b>{1}</b>?<br><br>Sau khi đẩy, sales lập đơn sẽ thấy giá mới ở cột <i>Đơn giá theo bảng giá</i>. Giá của những đơn đã lập <b>không</b> bị ảnh hưởng.",
				[ds.length, this.kq.bang_gia]
			),
			() => {
				frappe.call({
					method: "mbwnext_hkled.api.gia_niem_yet.cap_nhat_gia",
					args: { ma_hang: ds },
					freeze: true,
					freeze_message: __("Đang cập nhật giá niêm yết…"),
					callback: (r) => {
						if (!r.message) return;
						const { da_doi, bo_qua } = r.message;
						let msg = __("Đã cập nhật <b>{0}</b> mặt hàng.", [da_doi.length]);
						if (!da_doi.length) {
							msg = __("Không có gì phải đổi — các mặt hàng đã chọn đang đúng giá.");
						}
						if (bo_qua.length) {
							msg +=
								"<br><br>" +
								__("<b>{0}</b> mặt hàng bị bỏ qua vì chưa tính được giá:", [bo_qua.length]) +
								"<ul>" +
								bo_qua
									.slice(0, 10)
									.map(
										(b) =>
											`<li>${frappe.utils.escape_html(b.ma_hang)} — ${frappe.utils.escape_html(b.ly_do)}</li>`
									)
									.join("") +
								"</ul>";
						}
						frappe.msgprint({
							title: __("Cập nhật giá niêm yết"),
							message: msg,
							indicator: da_doi.length ? "green" : "orange",
						});
						this.tai();
					},
				});
			}
		);
	}

	xuat() {
		const ds = this.danh_sach();
		if (!ds) return;

		// Hỏi tỷ lệ chiết khấu ngay lúc xuất: khách điền sẵn vào file thì đỡ một bước, mà vẫn sửa
		// được trong Excel vì cột Giá bán là CÔNG THỨC trỏ về ô đó, không phải số chết.
		const d = new frappe.ui.Dialog({
			title: __("Xuất bảng giá niêm yết"),
			fields: [
				{
					fieldname: "ghi_chu",
					fieldtype: "HTML",
					options: `<p class="text-muted">${__(
						"File gồm 3 cột: <b>Mã mặt hàng</b>, <b>Giá niêm yết</b>, <b>Giá bán</b>. Cột Giá bán mang <b>công thức sống</b> — sửa ô tỷ lệ chiết khấu trong file là cả cột tự tính lại."
					)}</p>`,
				},
				{
					fieldname: "ty_le_chiet_khau",
					label: __("Tỷ lệ chiết khấu (%)"),
					fieldtype: "Percent",
					default: 68,
					description: __("Điền sẵn vào file. Người nhận vẫn sửa được trong Excel."),
				},
			],
			primary_action_label: __("Xuất file"),
			primary_action: (v) => {
				d.hide();
				const url =
					"/api/method/mbwnext_hkled.api.gia_niem_yet.xuat_excel" +
					"?ma_hang=" +
					encodeURIComponent(JSON.stringify(ds)) +
					"&ty_le_chiet_khau=" +
					encodeURIComponent(v.ty_le_chiet_khau || 0);
				window.open(url, "_blank");
			},
		});
		d.show();
	}
};
