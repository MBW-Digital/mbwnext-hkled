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
//   4. Tick chọn ĐƯỢC GIỮ khi đổi trang, đổi bộ lọc, đổi từ khoá tìm (anh Thắng chốt 09/09
//      14:55: "Câu 1: đúng em nhé"). Nghĩa là bấm Cập nhật sẽ ghi cho cả mã KHÔNG còn hiện trên
//      màn hình — nên bắt buộc có ba lớp che: ô "đang giữ N mã" xem/bỏ được, hộp thoại xác nhận
//      LIỆT KÊ TỪNG MÃ chứ không chỉ nói số lượng, và nút bỏ chọn tất cả luôn nhìn thấy.
//      ⚠ Trước 09/09 mã rời khỏi lưới bị bỏ tick tự động. Đừng khôi phục hành vi đó.
//
//   5. R&D và Lợi nhuận CHỈ ĐỂ XEM ở đây; sửa thì vào bản ghi Mặt hàng (anh Thắng chốt 09/09
//      14:55: "không sửa trên bảng em nhé, chỉ được sửa ở bản ghi mặt hàng"). Một con số chỉ có
//      một chỗ sửa thì không ai phải hỏi "sửa ở đâu thì thắng".
//
// ⚠ Vì sao phải phân trang và vì sao phải NÓI RA: site có hơn 61 nghìn mặt hàng. Dựng hết một
//   lượt là treo trình duyệt. Nhưng một bảng bị cắt trông y hệt một bảng đầy đủ — nên luôn hiện
//   "đang xem trang X trên Y, tổng M".

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
		this.trang = 1;
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
			change: () => this.tai(1),
		});
		this.f_cha = p.add_field({
			fieldname: "mat_hang_cha",
			label: __("Mặt hàng cha"),
			fieldtype: "Link",
			options: "Item",
			get_query: () => ({ filters: { has_variants: 1 } }),
			change: () => this.tai(1),
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
			change: () => this.tai(1),
		});
		// Ô chọn nguồn giá vốn — chỉ đổi CÁCH XEM, không ghi vào Cài đặt. Để người dùng so hai cách
		// trước khi quyết, mà không phải sửa cài đặt của cả hệ thống rồi trả lại.
		this.f_nguon = p.add_field({
			fieldname: "nguon",
			label: __("Giá vốn mặt hàng mua"),
			fieldtype: "Select",
			options: [
				{ value: "", label: __("Theo cài đặt") },
				{ value: "Đơn mua gần nhất", label: __("Đơn mua gần nhất") },
				{ value: "Giá vốn tồn kho trung bình", label: __("Giá vốn tồn kho trung bình") },
			],
			default: "",
			change: () => this.tai(1),
		});
		this.f_tim = p.add_field({
			fieldname: "tim",
			label: __("Tìm mã hoặc tên"),
			fieldtype: "Data",
			// Tìm cả mã lẫn tên, khớp ĐOẠN GIỮA — anh Thắng chốt 09/09 14:55.
			description: __("Gõ một đoạn bất kỳ, ví dụ 64LED"),
			change: () => this.tai(1),
		});
		this.f_so_dong = p.add_field({
			fieldname: "moi_trang",
			label: __("Số dòng mỗi trang"),
			fieldtype: "Select",
			options: ["50", "100", "200", "500"],
			default: "100",
			change: () => this.tai(1),
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
				<div class="bgny-trang"></div>
			</div>
		`).appendTo(p.main);
	}

	// ── Nạp ──────────────────────────────────────────────────────────────────

	tai(trang) {
		if (trang) this.trang = trang;
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
				tim: this.f_tim.get_value() || null,
				nguon: this.f_nguon.get_value() || null,
				trang: this.trang,
				moi_trang: this.f_so_dong.get_value() || 100,
			},
			callback: (r) => {
				if (!r.message) return;
				this.kq = r.message;
				this.dong = r.message.dong;
				this.trang = r.message.trang;
				// ⚠ KHÔNG cắt bớt `this.chon` ở đây. Tick phải sống qua trang và qua lần tìm khác
				//   — luật 4 ở đầu file. Chỗ che an toàn nằm ở ô "đang giữ N mã" và ở hộp thoại
				//   xác nhận liệt kê từng mã, KHÔNG phải ở chỗ này.
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
				<span class="bgny-chip ${
					k.nguon !== k.nguon_mac_dinh ? "bgny-chip-tam" : ""
				}">${__("Giá vốn mặt hàng mua")} <b>${frappe.utils.escape_html(k.nguon || "")}</b>${
					k.nguon !== k.nguon_mac_dinh ? ` — ${__("đang xem tạm")}` : ""
				}</span>
				<span class="bgny-chip ${lech ? "bgny-chip-lech" : ""}">${__("Đang lệch")} <b>${lech}</b></span>
				${
					this.chon.size
						? `<span class="bgny-chip bgny-chip-chon bgny-xem-chon" title="${__(
								"Bấm để xem và bỏ bớt"
						  )}">${__("Đang giữ")} <b>${this.chon.size}</b> ${__("mã đã tick")}</span>
						   <a class="bgny-bo-het" href="#">${__("Bỏ chọn tất cả")}</a>`
						: ""
				}
			</div>`;

		// ⚠ Tick giữ qua trang nghĩa là có thể đang giữ mã KHÔNG hiện trên màn hình. Phải nói ra,
		//   không được để người dùng tự đoán — xem luật 4 đầu file.
		const ngoai = [...this.chon].filter(
			(m) => !this.dong.some((d) => d.ma_hang === m)
		).length;
		if (ngoai) {
			tom += `<div class="bgny-canh">${__(
				"Trong <b>{0}</b> mã đang tick, có <b>{1}</b> mã <b>không nằm trên trang này</b>. Bấm Cập nhật là ghi cho cả chúng.",
				[this.chon.size, ngoai]
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
			this.gan_chung();
			this.ve_thanh_trang();
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
		// ⚠ Ô tick ở đầu bảng chỉ tác động lên TRANG ĐANG XEM, không phải toàn bộ 61 nghìn mã.
		$b.find(".bgny-all").on("change", (e) => {
			const v = e.currentTarget.checked;
			this.dong.forEach((d) => {
				if (d.gia_niem_yet === null) return;
				if (v) this.chon.add(d.ma_hang);
				else this.chon.delete(d.ma_hang);
			});
			this.ve();
		});
		this.gan_chung();
		this.ve_thanh_trang();
		this.dem();
	}

	// ── Danh sách đang giữ, và thanh chuyển trang ────────────────────────────

	gan_chung() {
		const $b = this.$than;
		$b.find(".bgny-bo-het").off("click").on("click", (e) => {
			e.preventDefault();
			this.chon.clear();
			this.ve();
		});
		$b.find(".bgny-xem-chon").off("click").on("click", () => this.xem_chon());
	}

	xem_chon() {
		if (!this.chon.size) return;
		const d = new frappe.ui.Dialog({
			title: __("{0} mã đang tick", [this.chon.size]),
			size: "large",
			primary_action_label: __("Xong"),
			primary_action: () => d.hide(),
		});
		const ve = () => {
			const ds = [...this.chon].sort();
			d.$body.html(
				ds.length
					? `<p class="text-muted">${__(
							"Đây là toàn bộ mã sẽ được ghi giá khi bấm Cập nhật, kể cả mã không nằm trên trang đang xem."
					  )}</p>
					   <div class="bgny-ds-chon">${ds
							.map(
								(m) =>
									`<div class="bgny-ds-dong"><span>${frappe.utils.escape_html(
										m
									)}</span><a href="#" data-bo="${frappe.utils.escape_html(
										m
									)}">${__("bỏ")}</a></div>`
							)
							.join("")}</div>`
					: `<p>${__("Không còn mã nào.")}</p>`
			);
			d.$body.find("[data-bo]").on("click", (e) => {
				e.preventDefault();
				this.chon.delete($(e.currentTarget).data("bo"));
				ve();
				this.ve();
			});
		};
		ve();
		d.show();
	}

	ve_thanh_trang() {
		const k = this.kq;
		const $t = this.$than.find(".bgny-trang");
		if (!k || k.so_trang <= 1) {
			$t.html(
				k && k.tong
					? `<div class="bgny-trang-tin">${__("Tổng <b>{0}</b> mặt hàng.", [
							format_number(k.tong, null, 0),
					  ])}</div>`
					: ""
			);
			return;
		}
		$t.html(`
			<div class="bgny-trang-tin">${__(
				"Đang xem trang <b>{0}</b> trên <b>{1}</b> — tổng <b>{2}</b> mặt hàng.",
				[k.trang, k.so_trang, format_number(k.tong, null, 0)]
			)}</div>
			<div class="bgny-trang-nut">
				<button class="btn btn-default btn-xs" data-di="1" ${k.trang <= 1 ? "disabled" : ""}>« ${__("Đầu")}</button>
				<button class="btn btn-default btn-xs" data-di="${k.trang - 1}" ${k.trang <= 1 ? "disabled" : ""}>‹ ${__("Trước")}</button>
				<input type="number" class="bgny-toi-trang" min="1" max="${k.so_trang}" value="${k.trang}">
				<button class="btn btn-default btn-xs" data-di="${k.trang + 1}" ${k.trang >= k.so_trang ? "disabled" : ""}>${__("Sau")} ›</button>
				<button class="btn btn-default btn-xs" data-di="${k.so_trang}" ${k.trang >= k.so_trang ? "disabled" : ""}>${__("Cuối")} »</button>
			</div>`);
		$t.find("[data-di]").on("click", (e) =>
			this.tai(parseInt($(e.currentTarget).data("di"), 10))
		);
		$t.find(".bgny-toi-trang").on("change", (e) => {
			const n = parseInt(e.currentTarget.value, 10);
			if (n >= 1 && n <= k.so_trang) this.tai(n);
		});
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
		// 🔴 Từ 09/09 tick sống qua trang, nên danh sách này có thể chứa mã KHÔNG hiện trên màn
		//    hình. Vì vậy hộp thoại phải LIỆT KÊ TỪNG MÃ — nói "12 mặt hàng" thì người dùng không
		//    có cách nào biết mình đang ghi cho cái gì.
		const ngoai = ds.filter((m) => !this.dong.some((d) => d.ma_hang === m));
		const ke = ds
			.map(
				(m) =>
					`<div class="bgny-ds-dong"><span>${frappe.utils.escape_html(m)}</span>${
						ngoai.includes(m)
							? `<i class="text-muted">${__("không trên trang này")}</i>`
							: ""
					}</div>`
			)
			.join("");
		// 🔴 Đang xem TẠM theo nguồn khác cài đặt mà bấm ghi thì con số đẩy sang sales là con số
		//    của cách đang xem — phải nói ra, vì mở lại màn hình nó sẽ hiện theo cài đặt và trông
		//    như hệ thống tự đổi giá.
		const tam =
			this.kq.nguon !== this.kq.nguon_mac_dinh
				? `<br><div class="bgny-canh bgny-canh-do">${__(
						"Bảng đang xem TẠM theo <b>{0}</b>, khác cài đặt chung (<b>{1}</b>). Giá đẩy sang sales sẽ là giá của cách đang xem.",
						[this.kq.nguon, this.kq.nguon_mac_dinh]
				  )}</div>`
				: "";
		frappe.confirm(
			tam +
			__(
				"Đẩy giá niêm yết mới của <b>{0}</b> mặt hàng sang bảng giá <b>{1}</b>?<br><br>Sau khi đẩy, sales lập đơn sẽ thấy giá mới ở cột <i>Đơn giá theo bảng giá</i>. Giá của những đơn đã lập <b>không</b> bị ảnh hưởng.",
				[ds.length, this.kq.bang_gia]
			) +
				(ngoai.length
					? `<br><div class="bgny-canh">${__(
							"Trong đó <b>{0}</b> mã <b>không nằm trên trang đang xem</b>.",
							[ngoai.length]
					  )}</div>`
					: "") +
				`<div class="bgny-ds-chon bgny-ds-xac-nhan">${ke}</div>`,
			() => {
				frappe.call({
					method: "mbwnext_hkled.api.gia_niem_yet.cap_nhat_gia",
					// Gửi kèm nguồn ĐANG XEM, không để server tự lấy mặc định — nếu không, con số
					// ghi sang sales sẽ khác con số người dùng vừa nhìn thấy.
					args: { ma_hang: ds, nguon: this.kq.nguon },
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
					encodeURIComponent(v.ty_le_chiet_khau || 0) +
					// Kèm nguồn ĐANG XEM: file xuất ra phải mang đúng con số trên màn hình.
					"&nguon=" +
					encodeURIComponent(this.kq.nguon || "");
				window.open(url, "_blank");
			},
		});
		d.show();
	}
};
