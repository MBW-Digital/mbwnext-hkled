// Tính nhu cầu vật tư cần mua theo kỳ — PM-FEAT-00030, bước 3 (tab Tính toán).
//
// Đầu bài: docs/features/phan-v-tinh-toan-nhu-cau-vat-tu-can-mua-theo-ky.md
//
// HAI tab, và ranh giới giữa chúng là ranh giới GHI DỮ LIỆU:
//   • tab Tính toán    — chỉ đọc, không tạo BOM, không tạo đơn mua, không ghi một bản ghi nào;
//   • tab Lập kế hoạch — chỗ DUY NHẤT của cả Phần V ghi dữ liệu thật, và chỉ khi người dùng bấm
//     Lập đơn hàng rồi xác nhận nhà cung cấp trong hộp thoại.
//
// Kết quả chỉ đúng tại thời điểm bấm Tính toán, không chốt cứng — nên lưới Lập kế hoạch luôn dựng
// lại từ lần tính gần nhất, không giữ trạng thái qua các lần bấm.
//
// ⚠ Vì sao chạy NỀN chứ không gọi thẳng: chi phí tỉ lệ với số BIẾN THỂ khác nhau — đo 03/09 trên
// cổng 8012 là ~0,15 s mỗi biến thể, tức 300 biến thể ≈ 44 giây. Vượt timeout gateway, mà kể cả
// không vượt thì để màn hình đứng im 44 giây cũng là hỏng. Nên: đẩy vào hàng đợi, nghe realtime,
// xong thì lấy kết quả về.

frappe.pages["tinh-nhu-cau-vat-tu"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Tính nhu cầu vật tư cần mua theo kỳ"),
		single_column: true,
	});
	new mbwnext_hkled.TinhNhuCauVatTu(page);
};

frappe.provide("mbwnext_hkled");

mbwnext_hkled.TinhNhuCauVatTu = class TinhNhuCauVatTu {
	constructor(page) {
		this.page = page;
		this.kieu = "1";
		this.ma_phien = null;
		this.dung_khung();
		this.nghe_realtime();
	}

	// ── Khung ────────────────────────────────────────────────────────────────

	dung_khung() {
		this.$nd = $(`
			<div class="hkled-nc">
				<div class="hkled-nc-tab">
					<button type="button" class="t" data-tab="tinh">${__("Tính toán")}</button>
					<button type="button" class="t" data-tab="ke">${__("Lập kế hoạch")}</button>
				</div>

				<div class="hkled-nc-loc">
					<div class="hkled-nc-o"><label>${__("Kiểu tính")}</label><div class="o-kieu"></div></div>
					<div class="hkled-nc-o k1"><label>${__("Loại kỳ")}</label><div class="o-loai-ky"></div></div>
					<div class="hkled-nc-o k1"><label>${__("Số kỳ")}</label><div class="o-so-ky"></div></div>
					<div class="hkled-nc-o"><label>${__("Từ ngày")}</label><div class="o-tu"></div></div>
					<div class="hkled-nc-o k2"><label>${__("Đến ngày")}</label><div class="o-den"></div></div>
					<div class="hkled-nc-o k2">
						<label>${__("Lùi lại")}
							<span class="hkled-nc-phu">(${__("tháng — lấy lượng bán kỳ tham chiếu")})</span>
						</label>
						<div class="o-lui"></div>
					</div>
				</div>

				<div class="hkled-nc-tiendo" hidden>
					<div class="thanh"><div class="day"></div></div>
					<div class="chu"></div>
				</div>

				<div class="pane pane-tinh">
					<div class="hkled-nc-tomtat" hidden></div>
					<div class="hkled-nc-canhbao" hidden></div>
					<div class="hkled-nc-khung"><div class="hkled-nc-bang"></div></div>
					<div class="hkled-nc-phu-luc"></div>
				</div>

				<div class="pane pane-ke" hidden>
					<div class="hkled-nc-ke"></div>
				</div>
			</div>
		`).appendTo(this.page.main);

		this.$nd
			.find(".hkled-nc-tab .t")
			.on("click", (e) => this.doi_tab($(e.currentTarget).data("tab")));

		this.o_kieu = this.o({
			sel: ".o-kieu",
			df: {
				fieldtype: "Select",
				options: [
					{ value: "1", label: __("1 — Theo đơn hàng") },
					{ value: "2", label: __("2 — Theo kết quả bán trước đó") },
				],
				default: "1",
				change: () => {
					this.kieu = this.o_kieu.get_value() || "1";
					this.doi_kieu();
				},
			},
		});
		// Kiểu 1 chia nhiều kỳ; Kiểu 2 là MỘT khoảng duy nhất (anh Thắng chốt 19/08 12:52) — nên
		// hai bộ ô lọc khác hẳn nhau, hiện cả hai cùng lúc là mời người dùng điền nhầm.
		this.o_loai_ky = this.o({
			sel: ".o-loai-ky",
			df: { fieldtype: "Select", options: ["Ngày", "Tuần", "Tháng"], default: "Tuần" },
		});
		this.o_so_ky = this.o({ sel: ".o-so-ky", df: { fieldtype: "Int", default: 4 } });
		this.o_tu = this.o({
			sel: ".o-tu",
			df: { fieldtype: "Date", default: frappe.datetime.get_today() },
		});
		this.o_den = this.o({
			sel: ".o-den",
			df: { fieldtype: "Date", default: frappe.datetime.add_months(frappe.datetime.get_today(), 1) },
		});
		this.o_lui = this.o({ sel: ".o-lui", df: { fieldtype: "Int", default: 12 } });

		this.page.set_primary_action(__("Tính toán"), () => this.tinh(), "play");
		this.doi_kieu();
		this.doi_tab("tinh");
	}

	// Số lượng vật tư gần như luôn là số nguyên. `format_number` mặc định 3 chữ số thập phân nên
	// 36 hiện thành "36,000" — đúng giá trị nhưng đọc rất dễ nhầm thành ba mươi sáu nghìn khi lướt
	// mắt qua một bảng đầy số. Nguyên thì bỏ hẳn phần thập phân; lẻ thì giữ tối đa 3 chữ số và
	// cắt số 0 thừa ở đuôi.
	so(x) {
		const v = flt(x);
		if (Number.isInteger(v)) return format_number(v, null, 0);
		return format_number(v, null, 3).replace(/[.,]?0+$/, "");
	}

	o({ sel, df }) {
		const ctrl = frappe.ui.form.make_control({
			parent: this.$nd.find(sel),
			df: Object.assign({ fieldname: sel.replace(/\W/g, "_") }, df),
			render_input: true,
		});
		ctrl.set_value(df.default);
		return ctrl;
	}

	doi_kieu() {
		this.$nd.find(".k1").toggle(this.kieu === "1");
		this.$nd.find(".k2").toggle(this.kieu === "2");
		this.$nd
			.find(".o-tu")
			.closest(".hkled-nc-o")
			.find("label")
			.contents()
			.first()
			.replaceWith(this.kieu === "1" ? __("Bắt đầu từ ngày") : __("Từ ngày"));
	}

	// Tab Lập kế hoạch KHOÁ cho tới khi có kết quả. Cho bấm vào một lưới rỗng thì người dùng
	// đọc thành "không phải mua gì" — trong khi thật ra là chưa bấm Tính toán lần nào.
	doi_tab(ten) {
		if (ten === "ke" && !this.kq) {
			frappe.show_alert({
				message: __("Bấm Tính toán trước — lưới lập kế hoạch dựng từ kết quả lần tính gần nhất"),
				indicator: "orange",
			});
			return;
		}
		this.tab = ten;
		this.$nd.find(".hkled-nc-tab .t").each((i, el) => {
			$(el).toggleClass("dang", $(el).data("tab") === ten);
		});
		this.$nd.find(".pane-tinh").attr("hidden", ten !== "tinh" ? true : null);
		this.$nd.find(".pane-ke").attr("hidden", ten !== "ke" ? true : null);
		// Bộ lọc thuộc về tab Tính toán. Để nó nằm trên lưới lập kế hoạch là mời người dùng đổi kỳ
		// rồi tưởng lưới bên dưới đã đổi theo — nó không đổi cho tới khi bấm Tính toán lại.
		this.$nd.find(".hkled-nc-loc").toggle(ten === "tinh");
		if (this.page.btn_primary) this.page.btn_primary.toggle(ten === "tinh");
	}

	// ── Chạy ─────────────────────────────────────────────────────────────────

	tham_so() {
		if (this.kieu === "1") {
			return {
				kieu: "1",
				loai_ky: this.o_loai_ky.get_value(),
				so_ky: this.o_so_ky.get_value(),
				tu_ngay: this.o_tu.get_value(),
			};
		}
		return {
			kieu: "2",
			tu_ngay: this.o_tu.get_value(),
			den_ngay: this.o_den.get_value(),
			lui_thang: this.o_lui.get_value(),
		};
	}

	// Hai đường nhận kết quả, cố ý dư một đường.
	//
	// ⚠ Realtime là đường NHANH, không phải đường CHẮC. Đo 03/09 trên chính bench này: socketio
	// chạy ở cổng 9006 còn site vào qua 8012 nên trình duyệt báo "Error connecting to socket.io:
	// timeout". Bản đầu của trang chỉ nghe realtime, và hậu quả là job chạy xong, kết quả nằm sẵn
	// trong cache, mà màn hình treo vĩnh viễn ở 3% — không lỗi, không thông báo, chỉ đứng im.
	// Nên luôn có thêm vòng hỏi; realtime chỉ làm nó nhanh hơn.
	nghe_realtime() {
		// Lọc theo `ma_phien`: người dùng bấm Tính toán lần hai khi lần một chưa xong thì kết quả
		// cũ về sau sẽ ghi đè lên bảng mới. Bỏ qua mọi phiên không phải phiên đang chờ.
		frappe.realtime.on("hkled_nhu_cau_tien_do", (d) => {
			if (d.ma_phien !== this.ma_phien) return;
			this.tien_do(d.phan_tram, d.mo_ta);
		});
		frappe.realtime.on("hkled_nhu_cau_xong", (d) => {
			if (d.ma_phien !== this.ma_phien) return;
			this.lay_ve(d.ma_phien);
		});
	}

	tinh() {
		this.$nd.find(".hkled-nc-bang").empty();
		this.$nd.find(".hkled-nc-phu-luc").empty();
		this.$nd.find(".hkled-nc-tomtat, .hkled-nc-canhbao").attr("hidden", true);
		this.tien_do(3, __("Đang xếp hàng đợi"));
		this.dung_hoi_vong();
		frappe
			.xcall("mbwnext_hkled.api.nhu_cau_vat_tu.tinh_nen", this.tham_so())
			.then((r) => {
				this.ma_phien = r.ma_phien;
				this.hoi_vong();
			})
			.catch(() => this.tien_do(null));
	}

	hoi_vong() {
		const cua_phien = this.ma_phien;
		this.bo_dem = setInterval(() => {
			// Đổi phiên giữa chừng thì vòng cũ tự tắt, khỏi ghi đè bảng của phiên mới.
			if (this.ma_phien !== cua_phien) return this.dung_hoi_vong();
			frappe
				.xcall("mbwnext_hkled.api.nhu_cau_vat_tu.trang_thai", { ma_phien: cua_phien })
				.then((t) => {
					if (this.ma_phien !== cua_phien) return;
					if (t.xong) return this.lay_ve(cua_phien);
					if (t.phan_tram) this.tien_do(t.phan_tram, t.mo_ta);
				})
				.catch(() => this.dung_hoi_vong());
		}, 1500);
	}

	dung_hoi_vong() {
		if (this.bo_dem) clearInterval(this.bo_dem);
		this.bo_dem = null;
	}

	lay_ve(ma_phien) {
		// Realtime và vòng hỏi có thể cùng gọi; chốt cửa để không lấy kết quả hai lần rồi vẽ đôi.
		if (this.dang_lay === ma_phien) return;
		this.dang_lay = ma_phien;
		this.dung_hoi_vong();
		frappe
			.xcall("mbwnext_hkled.api.nhu_cau_vat_tu.lay_ket_qua", { ma_phien: ma_phien })
			.then((kq) => this.ve(kq))
			.finally(() => {
				this.tien_do(null);
				this.dang_lay = null;
			});
	}

	tien_do(phan_tram, mo_ta) {
		const $t = this.$nd.find(".hkled-nc-tiendo");
		if (phan_tram === null) {
			$t.attr("hidden", true);
			return;
		}
		$t.removeAttr("hidden");
		$t.find(".day").css("width", phan_tram + "%");
		$t.find(".chu").text(`${mo_ta || ""} — ${phan_tram}%`);
	}

	// ── Vẽ ───────────────────────────────────────────────────────────────────

	ve(kq) {
		if (kq.loi) {
			this.kq = null;
			this.doi_tab("tinh");
			this.$nd
				.find(".hkled-nc-canhbao")
				.removeAttr("hidden")
				.html(`<div class="d nang">${frappe.utils.escape_html(kq.loi)}</div>`);
			return;
		}

		this.kq = kq;
		this.ve_tomtat(kq);
		this.ve_canhbao(kq.canh_bao || []);
		this.ve_bang(kq);
		this.ve_phu_luc(kq);
		this.ve_ke_hoach(kq);
	}

	ve_tomtat(kq) {
		const ky = kq.cac_ky || [];
		const dong = kq.dong || [];
		const tong = dong.reduce((a, d) => a + d.con_phai_mua, 0);
		const khoang = ky.length ? `${ky[0].tu} → ${ky[ky.length - 1].den}` : "";

		// Ba con số người dùng cần đọc TRƯỚC khi soi bảng. Trước đây chúng nằm trong một dòng chữ
		// mảnh chạy ngang, tức là thứ quan trọng nhất lại là thứ khó thấy nhất.
		const o = (nhan, gia_tri, phu) => `
			<div class="hkled-nc-the">
				<div class="nhan">${nhan}</div>
				<div class="gt">${gia_tri}</div>
				${phu ? `<div class="phu">${phu}</div>` : ""}
			</div>`;

		// Cả ba thẻ phải cùng một thứ bậc: NHÃN nhỏ ở trên, SỐ lớn ở giữa, chú thích nhỏ ở dưới.
		// Thẻ thứ ba từng lấy "4 kỳ" làm nhãn và khoảng ngày làm giá trị — ngược thứ bậc so với hai
		// thẻ kia, mà khoảng ngày lại dài nên phải thu nhỏ chữ, thành ra thẻ nào cũng lệch nhịp.
		const don_vi = { Ngày: __("ngày"), Tuần: __("tuần"), Tháng: __("tháng") };
		let h = o(
			__("Vật tư cần mua"),
			dong.length,
			kq.kieu === "1" ? __("Theo đơn hàng") : __("Theo lượng bán trước")
		);
		h += o(__("Tổng còn phải mua"), this.so(tong), "");
		h += o(
			__("Kỳ tính"),
			kq.kieu === "1"
				? `${ky.length} <span class="dv">${don_vi[this.o_loai_ky.get_value()] || ""}</span>`
				: __("Một khoảng"),
			khoang + (kq.khoang_tham_chieu ? ` · ${__("đối chiếu {0} → {1}", kq.khoang_tham_chieu)}` : "")
		);
		this.$nd.find(".hkled-nc-tomtat").removeAttr("hidden").html(h);
	}

	ve_canhbao(ds) {
		if (!ds.length) return;
		// Gom vào MỘT khối có đầu đề đếm số, thay vì ba dải vàng xếp chồng chiếm nhiều đất hơn cả
		// bảng dữ liệu. Cảnh báo vẫn phải đọc được — nên mở sẵn, chỉ là không còn hét.
		const $k = this.$nd.find(".hkled-nc-canhbao").removeAttr("hidden").empty();
		const $dau = $(`
			<button class="hkled-nc-cb-dau" type="button">
				<span class="dau-cham">!</span>
				<span>${__("{0} điều cần biết về kết quả này", [ds.length])}</span>
				<span class="mui">▾</span>
			</button>`).appendTo($k);
		const $than = $('<div class="hkled-nc-cb-than"></div>').appendTo($k);
		ds.forEach((c) => $than.append(`<div class="d">${c}</div>`));
		$dau.on("click", () => {
			$k.toggleClass("gap");
			$dau.find(".mui").text($k.hasClass("gap") ? "▸" : "▾");
		});
	}

	ve_bang(kq) {
		const dong = kq.dong || [];
		const $b = this.$nd.find(".hkled-nc-bang").empty();
		if (!dong.length) {
			// HAI trạng thái rỗng, nghĩa ngược nhau — đừng gộp một câu.
			//   • `co_nhu_cau === false`: kỳ này chẳng ai đặt gì, hệ thống CHƯA TÍNH gì cả;
			//   • ngược lại: có nhu cầu, tính xong, đủ hàng thật.
			// Trước 05/09 cả hai đều hiện "Không có vật tư nào thiếu" — ở ca đầu là NÓI SAI, người
			// lập kế hoạch đọc thành "tồn đủ". Cùng họ với "chưa có đơn mua" của Phần IV.
			$b.html(
				`<div class="hkled-nc-trong">${
					kq.co_nhu_cau === false
						? __(
								// 🔒 Chốt anh Thắng 08/09: đơn tính vào KỲ NÓ KHỞI CÔNG. Hệ quả trực
								// tiếp — đơn khởi công trước khoảng đang xem thì không hiện ở đây, dù
								// nó vẫn đang thiếu hàng thật. Nói luôn cách gỡ, vì trạng thái này là
								// mặc định trên site (mọi đơn đã duyệt đều khởi công trước hôm nay),
								// không phải ngoại lệ hiếm.
								"Kỳ đã chọn không có đơn hàng nào — chưa tính được gì.<br>Đơn được xếp theo <b>Thời Gian Bắt Đầu</b>, nên đơn khởi công <b>trước</b> khoảng này không hiện ở đây dù vẫn đang thiếu hàng. Thử <b>kéo ngày bắt đầu về trước</b>, hoặc kiểm lại ô Thời Gian Bắt Đầu trên đơn bán."
						  )
						: __("Mọi vật tư đều đủ trong khoảng đã chọn — không phải mua gì thêm")
				}</div>`
			);
			return;
		}

		const ky = kq.cac_ky;
		// Mỗi kỳ chiếm hai cột — Nhu cầu và Cần mua. Bảng rộng thì cuộn NGANG trong khung riêng,
		// không để cả trang trôi ngang.
		let dau = `<tr>
			<th rowspan="2">${__("Mã")}</th><th rowspan="2">${__("Tên")}</th><th rowspan="2">${__("ĐVT")}</th>
			<th rowspan="2" class="s">${__("Tồn khả dụng")}</th>
			<th rowspan="2" class="s">${__("Tối thiểu")}</th>`;
		ky.forEach(
			(k, i) =>
				(dau += `<th colspan="2" class="ky${i % 2 ? " le" : ""}">${__("Kỳ")} ${k.chi_so}<br><span>${k.tu}</span></th>`)
		);
		dau += `<th rowspan="2" class="s tong">${__("Cần mua")}</th></tr><tr>`;
		ky.forEach(
			(k, i) =>
				(dau += `<th class="s${i % 2 ? " le" : ""}">${__("Nhu cầu")}</th><th class="s${i % 2 ? " le" : ""}">${__("Cần mua")}</th>`)
		);
		dau += "</tr>";

		let than = "";
		dong.forEach((d) => {
			than += `<tr><td class="ma">${frappe.utils.escape_html(d.ma)}</td>`;
			than += `<td>${frappe.utils.escape_html(d.ten || "")}</td><td>${frappe.utils.escape_html(d.don_vi || "")}</td>`;
			than += `<td class="s${d.ton_kha_dung < 0 ? " am" : ""}">${this.so(d.ton_kha_dung)}</td>`;
			// "Chưa khai" khác hẳn "khai là 0": cùng hiện số 0 nhưng nghĩa ngược nhau. Đang 0/62.055
			// mặt hàng có khai, nên chỗ này phải nói rõ chứ không được để người đọc tự suy.
			than += d.da_khai_toi_thieu
				? `<td class="s">${this.so(d.ton_toi_thieu)}</td>`
				: `<td class="s chua-khai" title="${__("Chưa khai Tồn Kho Khả Dụng Tối Thiểu cho công ty này")}">${__("chưa khai")}</td>`;
			// Ô trống để hẳn dấu gạch mờ chứ không bỏ trắng: bảng nhiều kỳ mà toàn ô trắng thì
			// không phân biệt được "kỳ này không cần gì" với "cột bị lệch".
			d.ky.forEach((k, i) => {
				const le = i % 2 ? " le" : "";
				than += `<td class="s mo${le}">${k.nhu_cau ? this.so(k.nhu_cau) : '<span class="trong">–</span>'}</td>`;
				than += `<td class="s${le}${k.can_mua ? " can" : ""}">${
					k.can_mua ? this.so(k.can_mua) : '<span class="trong">–</span>'
				}</td>`;
			});
			// Mục 8 của đầu bài: "120 (70)". Trước ngoặc là phần phải mua nếu chưa đặt gì; trong
			// ngoặc là phần CÒN phải mua sau khi trừ hàng đang về. Bằng nhau thì bỏ ngoặc cho đỡ rối.
			const co_po = d.con_phai_mua !== d.tong_can_mua;
			than += `<td class="s tong">${this.so(d.tong_can_mua)}`;
			than += co_po ? ` <span class="con">(${this.so(d.con_phai_mua)})</span>` : "";
			than += "</td></tr>";
		});

		$b.html(`<table class="hkled-nc-t"><thead>${dau}</thead><tbody>${than}</tbody></table>`);
		if (dong.some((d) => d.con_phai_mua !== d.tong_can_mua)) {
			$b.append(
				`<div class="hkled-nc-chugiai">${__(
					"Cột Cần mua: số trước ngoặc là lượng phải mua nếu chưa đặt gì; số trong ngoặc là phần còn phải mua thêm sau khi trừ hàng đang về."
				)}</div>`
			);
		}
	}

	// ── Tab Lập kế hoạch (bước 4) ────────────────────────────────────────────
	//
	// 🔒 Anh Thắng chốt 08/09 08:49: tích mặt hàng ➜ bấm Lập đơn hàng ➜ **rồi mới** chọn nhà cung
	// cấp; một đơn mua nhiều dòng hàng. Bản mockup trước để cột Nhà cung cấp ngay trong lưới —
	// sai luồng, đã bỏ. Đừng đưa lại vào đây.

	ve_ke_hoach(kq) {
		const ds = kq.lap_ke_hoach || [];
		const $k = this.$nd.find(".hkled-nc-ke").empty();
		// Lưới dựng lại từ đầu mỗi lần tính, nên trạng thái tích/sửa số cũng phải mới hoàn toàn.
		// Giữ lại số cũ trên bộ dữ liệu mới là để người dùng đặt mua theo một con số đã hết hạn.
		this.dong_ke = ds.map((d) => Object.assign({ chon: false, dat: flt(d.so_luong_dat) }, d));
		this.da_lap = {};

		if (!ds.length) {
			$k.html(
				`<div class="hkled-nc-trong">${
					kq.co_nhu_cau === false
						? __("Kỳ đã chọn không có đơn hàng nào — chưa có gì để lập kế hoạch mua.")
						: __("Mọi vật tư đều đủ trong khoảng đã chọn — không phải lập đơn mua nào.")
				}</div>`
			);
			return;
		}

		let dau = `<tr>
			<th class="o-tich"><input type="checkbox" class="tich-tat-ca"></th>
			<th>${__("Mã")}</th><th>${__("Tên")}</th><th>${__("ĐVT")}</th>
			<th class="s">${__("Tồn khả dụng")}</th><th class="s">${__("Tối thiểu")}</th>
			<th class="s">${__("Thiếu hụt")}</th>
			<th class="s">${__("Số lượng đặt")}</th>
			<th class="s">${__("Ngày cần hàng")}</th>
		</tr>`;

		let than = "";
		this.dong_ke.forEach((d, i) => {
			than += `<tr data-i="${i}">`;
			than += `<td class="o-tich"><input type="checkbox" class="tich"></td>`;
			than += `<td class="ma">${frappe.utils.escape_html(d.ma)}</td>`;
			than += `<td>${frappe.utils.escape_html(d.ten || "")}</td>`;
			than += `<td>${frappe.utils.escape_html(d.don_vi || "")}</td>`;
			than += `<td class="s${d.ton_kha_dung < 0 ? " am" : ""}">${this.so(d.ton_kha_dung)}</td>`;
			than += d.da_khai_toi_thieu
				? `<td class="s">${this.so(d.ton_toi_thieu)}</td>`
				: `<td class="s chua-khai" title="${__("Chưa khai Tồn Kho Khả Dụng Tối Thiểu cho công ty này")}">${__("chưa khai")}</td>`;
			than += `<td class="s">${this.so(d.thieu_hut)}</td>`;
			// Ô SỬA ĐƯỢC — mặc định bằng thiếu hụt. Người dùng sửa để mua tròn thùng, mua theo lô
			// tối thiểu, hoặc cho về 0 để bỏ dòng. Lúc lập đơn dùng số này, không dùng thiếu hụt.
			than += `<td class="s"><input type="number" class="o-dat" min="0" step="any" value="${flt(d.so_luong_dat)}"></td>`;
			// Chỉ đọc — chốt của anh 08/09. Đây là ngày ĐẦU của kỳ bị thiếu, không phải đầu khoảng
			// đang xem; hai vật tư thiếu ở hai kỳ khác nhau thì ra hai ngày khác nhau.
			//
			// ⚠ Ngày này RẤT HAY nằm ở quá khứ — kỳ bị thiếu là kỳ đã trôi qua. Phải nói ra tại
			// đây chứ không đợi tới lúc bấm: ERPNext không nhận ngày trước ngày lập đơn, nên đơn
			// sẽ ghi ngày hôm nay, và người mua cần biết phần hàng này đã trễ.
			const tre = this.qua_han(d.ngay_can_hang);
			than += `<td class="s ngay${tre ? " qua-han" : ""}"${
				tre ? ` title="${__("Đã quá hạn — đơn sẽ ghi ngày hôm nay")}"` : ""
			}>${frappe.datetime.str_to_user(d.ngay_can_hang) || "—"}${
				tre ? ` <span class="nhan-tre">${__("đã trễ")}</span>` : ""
			}</td>`;
			than += "</tr>";

			// Hai chỗ hở đã biết, đặt NGAY DƯỚI dòng hàng chứ không gom vào một khối riêng: gom lại
			// thì người bấm không nối được con số cảnh báo với dòng mình đang định mua.
			const nhac = [];
			if (flt(d.ycm_dang_cho) > 0) {
				nhac.push(
					__("còn {0} đang chờ trong Yêu Cầu Mặt Hàng đã duyệt chưa thành đơn mua", [
						this.so(d.ycm_dang_cho),
					])
				);
			}
			if (flt(d.po_nhap) > 0) {
				nhac.push(__("còn {0} nằm trong đơn mua CÒN NHÁP", [this.so(d.po_nhap)]));
			}
			if (nhac.length) {
				than += `<tr class="nhac" data-nhac="${i}"><td></td><td colspan="8">⚠ ${
					frappe.utils.escape_html(d.ma)
				} — ${nhac.join(" · ")}. ${__("Số bên trên CHƯA trừ phần đó.")}</td></tr>`;
			}
		});

		$k.html(`
			<div class="hkled-nc-khung"><table class="hkled-nc-t ke">
				<thead>${dau}</thead><tbody>${than}</tbody>
			</table></div>
			<div class="hkled-nc-chan">
				<div class="dem"></div>
				<button class="btn btn-primary btn-sm nut-lap">${__("Lập đơn hàng")}</button>
			</div>
		`);

		$k.find(".tich-tat-ca").on("change", (e) => {
			const bat = e.currentTarget.checked;
			// Dòng đã lập đơn trong phiên này thì không tích lại — xem chú thích ở `tao_don`.
			this.dong_ke.forEach((d, i) => (d.chon = bat && !this.da_lap[i] && flt(d.dat) > 0));
			$k.find("tbody tr[data-i]").each((i, tr) => {
				$(tr).find(".tich").prop("checked", this.dong_ke[$(tr).data("i")].chon);
			});
			this.dem_chon();
		});
		$k.find(".tich").on("change", (e) => {
			const $tr = $(e.currentTarget).closest("tr");
			this.dong_ke[$tr.data("i")].chon = e.currentTarget.checked;
			this.dem_chon();
		});
		$k.find(".o-dat").on("input", (e) => {
			const $tr = $(e.currentTarget).closest("tr");
			const d = this.dong_ke[$tr.data("i")];
			d.dat = flt(e.currentTarget.value);
			// Cho về 0 là bỏ dòng — bỏ tích luôn, thay vì để một dòng tích sẵn với số 0 đi vào hộp
			// thoại rồi bị chặn ở server. Chặn được thì tốt, nhưng bắt người dùng bấm hai lần mới
			// biết mình sai thì không.
			if (flt(d.dat) <= 0 && d.chon) {
				d.chon = false;
				$tr.find(".tich").prop("checked", false);
			}
			this.dem_chon();
		});
		$k.find(".nut-lap").on("click", () => this.hop_thoai_lap_don());

		// Nói ra NGAY khi vẽ lưới, không đợi tới lúc bấm.
		//
		// ⚠ Vai trò Quản lý sản xuất mở được màn hình này nhưng mặc định không tạo được Đơn Mua
		// Hàng. Hồi trang còn chỉ đọc thì chênh lệch đó vô hại; từ khi có nút lập đơn, để nguyên
		// là bắt người ta tích dòng, gõ số lượng, chọn nhà cung cấp rồi mới bị chặn ở bước cuối.
		if (kq.duoc_lap_don === false) {
			$k.find(".hkled-nc-chan").append(
				`<div class="khong-quyen">${__(
					"Bạn xem được bảng này nhưng không lập được đơn mua — việc đó cần quyền của bộ phận mua hàng."
				)}</div>`
			);
		}
		this.dem_chon();
	}

	// Một chỗ duy nhất trả lời "ngày này đã trôi qua chưa" — lưới và hộp thoại phải cùng câu trả
	// lời, nếu không thì lưới bảo trễ mà hộp thoại bảo không, và không ai biết cái nào đúng.
	qua_han(ngay) {
		return !!ngay && ngay < frappe.datetime.get_today();
	}

	dem_chon() {
		const chon = (this.dong_ke || []).filter((d) => d.chon && flt(d.dat) > 0);
		const $k = this.$nd.find(".hkled-nc-ke");
		const tong = chon.reduce((a, d) => a + flt(d.dat), 0);
		$k.find(".dem").html(
			chon.length
				? __("{0} dòng đã chọn · tổng {1}", [chon.length, this.so(tong)])
				: `<span class="mo">${__("Chưa chọn dòng nào")}</span>`
		);
		// Không có quyền thì khoá hẳn, bất kể đã tích bao nhiêu dòng.
		const co_quyen = !this.kq || this.kq.duoc_lap_don !== false;
		$k.find(".nut-lap").prop("disabled", !chon.length || !co_quyen);
		return chon;
	}

	// ── Hộp thoại: giờ mới hỏi nhà cung cấp ──────────────────────────────────

	hop_thoai_lap_don() {
		const chon = this.dem_chon();
		if (!chon.length) return;

		let bang = `<table class="hkled-nc-t nho"><thead><tr>
			<th>${__("Mã")}</th><th class="s">${__("Số lượng đặt")}</th><th class="s">${__("Ngày cần hàng")}</th>
		</tr></thead><tbody>`;
		chon.forEach((d) => {
			bang += `<tr><td class="ma">${frappe.utils.escape_html(d.ma)}</td>`;
			bang += `<td class="s">${this.so(d.dat)}</td>`;
			bang += `<td class="s${this.qua_han(d.ngay_can_hang) ? " qua-han" : ""}">${
				frappe.datetime.str_to_user(d.ngay_can_hang) || "—"
			}${this.qua_han(d.ngay_can_hang) ? ` <span class="nhan-tre">${__("đã trễ")}</span>` : ""}</td></tr>`;
		});
		bang += "</tbody></table>";

		// 🔴 Chốt (B) của anh Thắng 08/09 09:12 — Phần V KHÔNG trừ Yêu Cầu Mặt Hàng đang chờ, nên
		// màn hình phải nói ra, kèm SỐ ĐO của đúng rổ hàng đang định mua. Đặt ngay trong hộp thoại
		// vì đây là giây cuối cùng trước khi tiền đi ra.
		const cho = chon.filter((d) => flt(d.ycm_dang_cho) > 0 || flt(d.po_nhap) > 0);
		const tre = chon.filter((d) => this.qua_han(d.ngay_can_hang));
		let canh = "";
		if (tre.length) {
			canh += `<div class="hkled-nc-cb-hop">⚠ ${__(
				"{0} dòng có Ngày cần hàng đã ở quá khứ. Đơn mua sẽ ghi ngày hôm nay — phần hàng này đã TRỄ so với kế hoạch.",
				[tre.length]
			)}</div>`;
		}
		if (cho.length) {
			canh = `<div class="hkled-nc-cb-hop">${cho
				.map((d) => {
					const v = [];
					if (flt(d.ycm_dang_cho) > 0)
						v.push(__("{0} chờ trong Yêu Cầu Mặt Hàng", [this.so(d.ycm_dang_cho)]));
					if (flt(d.po_nhap) > 0)
						v.push(__("{0} trong đơn mua còn nháp", [this.so(d.po_nhap)]));
					return `<div>⚠ ${frappe.utils.escape_html(d.ma)} — ${v.join(" · ")}</div>`;
				})
				.join("")}<div class="ghi">${__(
				"Số lượng đặt bên dưới CHƯA trừ những phần đó. Kiểm lại trước khi tạo đơn, kẻo mua trùng."
			)}</div></div>`;
		}

		const hop = new frappe.ui.Dialog({
			title: __("Lập đơn mua hàng"),
			fields: [
				{
					fieldname: "nha_cung_cap",
					label: __("Nhà cung cấp"),
					fieldtype: "Link",
					options: "Supplier",
					reqd: 1,
				},
				{ fieldname: "goi_y", fieldtype: "HTML" },
				{ fieldname: "ds", fieldtype: "HTML", options: canh + bang },
			],
			primary_action_label: __("Tạo đơn mua"),
			primary_action: (v) => this.tao_don(hop, v.nha_cung_cap, chon),
		});
		hop.show();

		// Gợi ý nhà cung cấp (mục 5) — nạp sau khi hộp thoại đã hiện, để việc chọn tay không phải
		// chờ một truy vấn thống kê. Gợi ý hỏng thì hộp thoại vẫn dùng được.
		const $gy = hop.fields_dict.goi_y.$wrapper.html(
			`<div class="hkled-nc-goiy dang-cho">${__("Đang xem lịch sử mua…")}</div>`
		);
		frappe
			.xcall("mbwnext_hkled.api.nhu_cau_vat_tu.goi_y_nha_cung_cap", {
				ma_hang: chon.map((d) => d.ma),
			})
			.then((ds) => this.ve_goi_y($gy, ds, hop))
			.catch(() => $gy.html(`<div class="hkled-nc-goiy">${__("Chưa xem được lịch sử mua")}</div>`));
	}

	// Ba tiêu chí có thể trỏ về ba nhà cung cấp khác nhau — hiện cả ba, KHÔNG tự ép chọn và không
	// chấm điểm tổng hợp. Người mua biết mình đang ưu tiên giá hay tiến độ; máy thì không.
	ve_goi_y($gy, ds, hop) {
		if (!(ds || []).length) return $gy.empty();
		let h = `<div class="hkled-nc-goiy"><div class="dau">${__("Gợi ý từ lịch sử mua")}</div>
			<table class="hkled-nc-t nho"><thead><tr>
			<th>${__("Tiêu chí")}</th><th>${__("Nhà cung cấp")}</th><th>${__("Căn cứ")}</th>
			</tr></thead><tbody>`;
		ds.forEach((t) => {
			h += `<tr class="${t.du_lieu ? "" : "chua"}"><td>${frappe.utils.escape_html(t.tieu_chi)}</td>`;
			h += t.du_lieu
				? `<td><a class="chon-ncc" data-ncc="${frappe.utils.escape_html(
						t.nha_cung_cap
				  )}" href="#">${frappe.utils.escape_html(t.nha_cung_cap)}</a></td>`
				: `<td class="mo">${__("chưa đủ dữ liệu")}</td>`;
			h += `<td class="ghi">${frappe.utils.escape_html(t.can_cu || "")}</td></tr>`;
		});
		$gy.html(h + "</tbody></table></div>");
		$gy.find(".chon-ncc").on("click", (e) => {
			e.preventDefault();
			hop.set_value("nha_cung_cap", $(e.currentTarget).data("ncc"));
		});
	}

	tao_don(hop, ncc, chon) {
		hop.disable_primary_action();
		frappe
			.xcall("mbwnext_hkled.api.nhu_cau_vat_tu.tao_don_mua", {
				nha_cung_cap: ncc,
				dong: chon.map((d) => ({
					ma: d.ma,
					so_luong: flt(d.dat),
					ngay_can_hang: d.ngay_can_hang,
				})),
				company: this.kq && this.kq.company,
			})
			.then((r) => {
				hop.hide();
				// Đánh dấu ngay trên lưới các dòng vừa đi vào đơn, và BỎ TÍCH chúng.
				//
				// ⚠ Đây không phải chuyện thẩm mỹ. Đơn tạo ra ở trạng thái NHÁP, mà phép tính chỉ
				// trừ đơn ĐÃ DUYỆT — nên bấm Tính toán lại thì số thiếu vẫn y nguyên. Không đánh
				// dấu ở đây thì người dùng nhìn lưới không đổi và lập tiếp một đơn nữa cho cùng
				// phần hàng, bằng tiền thật.
				chon.forEach((d) => {
					const i = this.dong_ke.indexOf(d);
					if (i < 0) return;
					d.chon = false;
					this.da_lap[i] = r.name;
					const $tr = this.$nd.find(`.hkled-nc-ke tbody tr[data-i="${i}"]`);
					$tr.addClass("da-lap").find(".tich").prop("checked", false).prop("disabled", true);
					$tr.find(".o-dat").prop("disabled", true);
					$tr.find("td.ma").append(
						` <span class="da-lap-nhan">${__("đã vào")} ${frappe.utils.escape_html(r.name)}</span>`
					);
				});
				this.dem_chon();

				const ghi = (r.canh_bao || [])
					.map((c) => `<div>${frappe.utils.escape_html(c)}</div>`)
					.join("");
				frappe.msgprint({
					title: __("Đã tạo đơn mua nháp"),
					indicator: "orange",
					message: `<div><a href="/app/purchase-order/${encodeURIComponent(
						r.name
					)}" target="_blank"><b>${frappe.utils.escape_html(r.name)}</b></a></div>
						<div class="hkled-nc-cb-hop">${ghi}</div>`,
				});
			})
			.finally(() => hop.enable_primary_action());
	}

	ve_phu_luc(kq) {
		const $p = this.$nd.find(".hkled-nc-phu-luc").empty();

		// Mặt hàng Gia công sinh THÊM một dòng đơn mua dịch vụ, Finished Good = chính nó
		// (anh Thắng chốt 24/08). Nguyên vật liệu của nó đã nằm trong bảng chính, nên khối này
		// chỉ liệt kê phần dịch vụ — gộp vào bảng trên là đếm hai lần.
		if ((kq.gia_cong || []).length) {
			let h = `<h5>${__("Dòng đơn mua gia công")}</h5><table class="hkled-nc-t nho"><thead><tr>
				<th>${__("Mặt hàng dịch vụ")}</th><th>${__("Thành phẩm")}</th><th class="s">${__("Số lượng")}</th>
			</tr></thead><tbody>`;
			kq.gia_cong.forEach((g) => {
				h += `<tr><td>${frappe.utils.escape_html(g.ma_dich_vu)}</td>`;
				h += `<td class="ma">${frappe.utils.escape_html(g.finished_good)}</td>`;
				h += `<td class="s">${this.so(g.so_luong)}</td></tr>`;
			});
			$p.append(h + "</tbody></table>");
		}

		// Nhánh thứ ba của mục 4.2: không có BOM lẫn BOM Template thì LIỆT KÊ cho người dùng kiểm,
		// tuyệt đối không lặng lẽ coi như phải mua chính nó — với hàng sản xuất thì đó là sai hẳn.
		if ((kq.chua_no_duoc || []).length) {
			let h = `<h5 class="canh">${__("Chưa nổ được định mức — cần người kiểm")}</h5>
				<div class="hkled-nc-phu">${__(
					"Những mặt hàng này là hàng sản xuất/gia công nhưng chưa có BOM lẫn BOM Template, nên KHÔNG được tính vào nhu cầu bên trên."
				)}</div>
				<table class="hkled-nc-t nho"><thead><tr>
				<th>${__("Mã")}</th><th class="s">${__("Số lượng")}</th><th>${__("Lý do")}</th>
				</tr></thead><tbody>`;
			kq.chua_no_duoc.forEach((c) => {
				h += `<tr><td class="ma">${frappe.utils.escape_html(c.ma)}</td>`;
				h += `<td class="s">${this.so(c.so_luong)}</td>`;
				h += `<td>${frappe.utils.escape_html(c.ly_do)}</td></tr>`;
			});
			$p.append(h + "</tbody></table>");
		}
	}
};
