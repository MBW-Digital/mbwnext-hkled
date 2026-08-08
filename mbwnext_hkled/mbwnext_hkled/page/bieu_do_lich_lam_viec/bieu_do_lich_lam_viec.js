// Biểu đồ tình hình làm việc của nhân sự — PM-FEAT-00009.
//
// Trang CHỈ ĐỌC: không sửa dữ liệu, không kéo thả. Mọi thay đổi lịch phải đi qua nút
// "Tính Lại Lịch" trên Lệnh sản xuất — kéo thả trực tiếp sẽ làm Lệnh sản xuất lệch khỏi
// Phân Công. Đây cũng là lý do KHÔNG dùng chế độ xem Gantt sẵn có của Frappe: hàm
// `on_date_change` của nó ghi bằng `frappe.db.set_value` với định dạng "YYYY-MM-DD", tức là
// CẮT CỤT phần giờ của Datetime (frappe/public/js/frappe/views/gantt/gantt_view.js).

frappe.pages["bieu-do-lich-lam-viec"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Tình hình làm việc của nhân sự"),
		single_column: true,
	});
	new mbwnext_hkled.BieuDoLichLamViec(page);
};

frappe.provide("mbwnext_hkled");

mbwnext_hkled.BieuDoLichLamViec = class BieuDoLichLamViec {
	constructor(page) {
		this.page = page;
		this.ngay = frappe.datetime.get_today();
		this.doi_chon = [];
		this.dung_bo_loc();
		this.tai_doi().then(() => this.tai());
	}

	dung_bo_loc() {
		this.$noi_dung = $(`
			<div class="hkled-tl">
				<div class="hkled-tl-thanh">
					<div class="hkled-tl-o">
						<label>${__("Chọn ngày xem")}</label>
						<div class="hkled-tl-ngay"></div>
					</div>
					<div class="hkled-tl-o">
						<label>${__("Lọc theo Đội Sản Xuất")}
							<span class="text-muted" style="text-transform:none;letter-spacing:0;font-weight:400">
								(${__("chọn nhiều · không chọn = hiện tất cả")})
							</span>
						</label>
						<div class="hkled-tl-doi"></div>
					</div>
				</div>
				<div class="hkled-tl-khung"><div class="hkled-tl-luoi"></div></div>
				<div class="hkled-tl-chugiai">
					<span><i class="hkled-tl-o-mau" style="background:#c62828"></i> ${__("Đang làm Lệnh sản xuất")}</span>
					<span><i class="hkled-tl-o-mau" style="background:#2e7d32"></i> ${__("Rảnh (trong ca, chưa có việc)")}</span>
					<span><i class="hkled-tl-o-mau" style="background:#1565c0"></i> ${__("Rảnh trong ca tăng ca")}</span>
					<span><i class="hkled-tl-o-mau" style="background:#e9e9ec;border:1px solid #d8d8de"></i> ${__(
						"Ngoài ca làm việc / nghỉ trưa"
					)}</span>
				</div>
			</div>
		`).appendTo(this.page.main);

		this.o_ngay = frappe.ui.form.make_control({
			parent: this.$noi_dung.find(".hkled-tl-ngay"),
			df: {
				fieldtype: "Date",
				fieldname: "ngay",
				default: this.ngay,
				change: () => {
					const v = this.o_ngay.get_value();
					if (v && v !== this.ngay) {
						this.ngay = v;
						this.tai();
					}
				},
			},
			render_input: true,
		});
		this.o_ngay.set_value(this.ngay);

		this.page.set_secondary_action(__("Tải lại"), () => this.tai(), "refresh");
	}

	tai_doi() {
		return frappe
			.xcall("mbwnext_hkled.api.employee_timeline.get_work_teams")
			.then((doi) => {
				const $o = this.$noi_dung.find(".hkled-tl-doi");
				if (!doi || !doi.length) {
					$o.append(`<span class="text-muted">${__("Chưa khai báo Đội Sản Xuất nào")}</span>`);
					return;
				}
				doi.forEach((d) => {
					$(`<label><input type="checkbox" value="${frappe.utils.escape_html(d.name)}"> ${
						frappe.utils.escape_html(d.name)
					}</label>`).appendTo($o);
				});
				$o.on("change", "input", () => {
					this.doi_chon = $o
						.find("input:checked")
						.map((_i, el) => el.value)
						.get();
					this.tai();
				});
			});
	}

	tai() {
		// `frappe.dom.freeze/unfreeze`, KHÔNG phải `frappe.freeze` — hàm đó không tồn tại trong v15
		// và gọi nhầm thì trang dựng xong khung nhưng lưới trống trơn, không báo gì trên màn hình.
		frappe.dom.freeze();
		frappe
			.xcall("mbwnext_hkled.api.employee_timeline.get_timeline", {
				date: this.ngay,
				work_teams: JSON.stringify(this.doi_chon),
			})
			.then((r) => this.ve(r))
			.finally(() => frappe.dom.unfreeze());
	}

	// Vị trí theo phần trăm của trục: dùng % chứ không dùng px để biểu đồ tự co theo bề rộng
	// màn hình mà không phải tính lại khi đổi kích thước cửa sổ.
	pct(phut) {
		return ((phut - this.truc_tu) / (this.truc_den - this.truc_tu)) * 100;
	}

	vach_gio($dai, co_nhan) {
		for (let h = Math.ceil(this.truc_tu / 60); h <= this.truc_den / 60; h++) {
			const trai = this.pct(h * 60);
			$(`<div class="hkled-tl-vach" style="left:${trai}%"></div>`).appendTo($dai);
			if (co_nhan) {
				const nhan = `${String(h === 24 ? 24 : h).padStart(2, "0")}:00`;
				$(`<div class="hkled-tl-gio" style="left:${trai}%">${nhan}</div>`).appendTo($dai);
			}
		}
	}

	ve(dl) {
		this.truc_tu = dl.truc_tu;
		this.truc_den = dl.truc_den;

		const $luoi = this.$noi_dung.find(".hkled-tl-luoi").empty();

		const $dau = $(`<div class="hkled-tl-dong dau">
			<div class="hkled-tl-ten"><div class="nm">${__("Nhân sự")}</div></div>
			<div class="hkled-tl-dai"></div></div>`).appendTo($luoi);
		this.vach_gio($dau.find(".hkled-tl-dai"), true);

		if (!dl.nhan_su.length) {
			$(`<div class="hkled-tl-dong"><div style="padding:16px" class="text-muted">${__(
				"Không có nhân sự nào thuộc đội đã chọn."
			)}</div></div>`).appendTo($luoi);
			return;
		}

		dl.nhan_su.forEach((ns) => {
			const $dong = $('<div class="hkled-tl-dong"></div>').appendTo($luoi);
			const phu = [ns.bac_tho, ns.doi].filter(Boolean).join(" · ") || __("Chưa gán bậc thợ / đội");
			$(`<div class="hkled-tl-ten">
				<div class="nm">${frappe.utils.escape_html(ns.ten)}</div>
				<div class="mt">${frappe.utils.escape_html(phu)}</div>
			</div>`).appendTo($dong);

			const $dai = $('<div class="hkled-tl-dai"></div>').appendTo($dong);

			// Nền ca trước, vạch giờ sau — không thì vạch bị nền phủ mất.
			ns.nen_ca.forEach((ca) => {
				$(
					`<div class="hkled-tl-nenca" style="left:${this.pct(ca.tu_phut)}%;width:${
						this.pct(ca.den_phut) - this.pct(ca.tu_phut)
					}%"></div>`
				).appendTo($dai);
			});
			this.vach_gio($dai, false);

			if (!ns.co_lich) {
				$(`<div class="hkled-tl-trong">${__("Không có lịch làm việc trong ngày này")}</div>`).appendTo(
					$dai
				);
			}

			ns.doan.forEach((d) => this.ve_doan($dai, ns, d));
		});
	}

	ve_doan($dai, ns, d) {
		const rong = this.pct(d.den_phut) - this.pct(d.tu_phut);
		const la_ban = d.loai === "ban";
		const ma_ngan = la_ban ? (d.work_order || "").replace(/^MFG-WO-\d{4}-/, "WO-") : "";

		// Nhãn rút gọn dần theo bề rộng: thanh hẹp mà nhồi nhãn dài thì bị cắt cụt giữa chừng,
		// đọc còn khó hơn là không ghi. Chi tiết đầy đủ luôn có ở tooltip.
		let nhan;
		if (la_ban) {
			nhan = rong >= 20 ? `${ma_ngan} (${d.tu} – ${d.den})` : rong >= 11 ? `${ma_ngan} · ${d.tu}` : ma_ngan;
		} else if (d.tang_ca) {
			nhan = rong >= 16 ? `${__("Tăng ca: Rảnh")} (${d.tu} – ${d.den})` : __("Tăng ca: Rảnh");
		} else {
			nhan = rong >= 14 ? `${__("Rảnh")} (${d.tu} – ${d.den})` : __("Rảnh");
		}

		const lop = ["hkled-tl-doan", d.loai];
		if (d.tang_ca) lop.push("tangca");
		if (rong < 4) lop.push("hep");

		const $d = $(
			`<div class="${lop.join(" ")}" style="left:${this.pct(d.tu_phut)}%;width:${rong}%"></div>`
		)
			.text(nhan)
			.appendTo($dai);

		if (la_ban) {
			// Số lượng: bỏ phần thập phân khi là số nguyên. Để `format_number` tự quyết thì qty = 100
			// hiện thành "100,000" (site đang để 3 chữ số thập phân, dấu phẩy là dấu thập phân) —
			// đúng cấu hình nhưng người đọc rất dễ hiểu thành một trăm nghìn.
			const sl =
				d.so_luong == null
					? null
					: format_number(d.so_luong, null, Number.isInteger(d.so_luong) ? 0 : 2);
			// PM-TASK-00051: thêm Khách Hàng và Nhân Viên Bán Hàng.
			// Lệnh tạo tay (không gắn Đơn Bán Hàng) thì hai trường này trống — bỏ hẳn dòng thay vì
			// hiện nhãn với giá trị rỗng, để tooltip không dài ra vì mấy dòng không có nội dung.
			//
			// ⚠ Nhãn viết ĐÚNG như nhãn trường trên Lệnh sản xuất: "Khách Hàng", "Nhân Viên Bán Hàng".
			// Chuỗi "Khách hàng" (chữ h thường) có bản dịch sang tiếng Anh do một app MBWNext khác
			// ship, mà site này chạy `lang = en`, nên `__()` trả về "Customer" và tooltip thành nửa
			// Anh nửa Việt. Viết tiếng Việt trong mã nguồn thì phải nhớ `__()` vẫn tra bảng dịch.
			const chi_tiet = [
				`${ns.ten} · ${d.work_order}`,
				d.mat_hang ? `${d.mat_hang} × ${sl}` : null,
				d.khach_hang ? `${__("Khách Hàng")}: ${d.khach_hang}` : null,
				d.nhan_vien_ban ? `${__("Nhân Viên Bán Hàng")}: ${d.nhan_vien_ban}` : null,
				d.trang_thai ? __(d.trang_thai) : null,
				`${d.tu} – ${d.den}${d.ca ? " · " + d.ca : ""}`,
			]
				.filter(Boolean)
				.join("\n");
			$d.attr("title", chi_tiet);
			$d.on("click", () => frappe.set_route("Form", "Work Order", d.work_order));
		} else {
			$d.attr("title", `${ns.ten} · ${__("Rảnh")} ${d.tu} – ${d.den}${d.ca ? " · " + d.ca : ""}`);
		}
	}
};
