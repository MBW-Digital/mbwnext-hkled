// Tính nhu cầu vật tư cần mua theo kỳ — PM-FEAT-00030, bước 3 (tab Tính toán).
//
// Đầu bài: docs/features/phan-v-tinh-toan-nhu-cau-vat-tu-can-mua-theo-ky.md
//
// Trang CHỈ ĐỌC. Không tạo BOM, không tạo đơn mua — tab Lập kế hoạch (bước 4) mới làm việc đó,
// và phải qua một cú bấm rõ ràng. Kết quả chỉ đúng tại thời điểm bấm Tính toán, không chốt cứng.
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

				<div class="hkled-nc-tomtat" hidden></div>
				<div class="hkled-nc-canhbao" hidden></div>
				<div class="hkled-nc-khung"><div class="hkled-nc-bang"></div></div>
				<div class="hkled-nc-phu-luc"></div>
			</div>
		`).appendTo(this.page.main);

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
			this.$nd
				.find(".hkled-nc-canhbao")
				.removeAttr("hidden")
				.html(`<div class="d nang">${frappe.utils.escape_html(kq.loi)}</div>`);
			return;
		}

		this.ve_tomtat(kq);
		this.ve_canhbao(kq.canh_bao || []);
		this.ve_bang(kq);
		this.ve_phu_luc(kq);
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
						? __("Kỳ đã chọn không có đơn hàng nào — chưa tính được gì. Chọn khoảng khác hoặc kiểm lại ô Thời Gian Bắt Đầu trên đơn bán.")
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
