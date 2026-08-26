// Không còn ô "Nhóm Công Thức" để điền: khoá tra công thức chính là Mặt Hàng Cha,
// Server Script hkled_resolve_bom_qty tự suy (chốt của TungDA 07/08).
//
// Hộp thoại "Chọn Điều Kiện" dựng theo bom_template_mockup: tick nhiều thuộc tính,
// mỗi thuộc tính tick nhiều giá trị (AND giữa thuộc tính, OR trong giá trị), kèm ô
// Nguyên Vật Liệu áp dụng. Số biến thể khớp hiện ngay khi đang tick.

frappe.ui.form.on("BOM Component Table", "create_rule", function (frm, cdt, cdn) {
	const row = locals[cdt][cdn];

	if (!frm.doc.item_template) {
		frappe.msgprint(__("Vui lòng chọn Mặt Hàng Cha trước"));
		return;
	}
	if (!row.bom_component) {
		frappe.msgprint(__("Vui lòng chọn Thành Phần BOM trước"));
		return;
	}

	frappe.call({
		method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.get_condition_attributes",
		args: { item_template: frm.doc.item_template },
		freeze: true,
		callback: function (r) {
			const data = r.message || {};
			if (!(data.attributes || []).length) {
				frappe.msgprint(
					__("Mặt hàng cha {0} chưa có biến thể nào để đặt điều kiện", [
						frm.doc.item_template,
					])
				);
				return;
			}
			show_rule_dialog(frm, row, data);
		},
	});
});

function show_rule_dialog(frm, row, data) {
	// sel[tên thuộc tính] = [giá trị đã tick]
	const sel = {};
	data.attributes.forEach((a) => (sel[a.name] = []));

	const dialog = new frappe.ui.Dialog({
		title: __("Chọn Điều Kiện — {0}", [row.bom_component]),
		size: "large",
		fields: [
			{
				fieldtype: "Check",
				fieldname: "khong_su_dung",
				label: __("Không sử dụng thành phần này"),
				description: __(
					"Tích khi biến thể khớp điều kiện bên dưới KHÔNG dùng thành phần này —" +
						" lúc tạo BOM dòng đó bị bỏ hẳn, không cần chọn Nguyên Vật Liệu."
				),
			},
			{
				fieldtype: "Link",
				options: "Item",
				fieldname: "item",
				label: __("Nguyên Vật Liệu áp dụng cho rule này"),
				depends_on: "eval:!doc.khong_su_dung",
				mandatory_depends_on: "eval:!doc.khong_su_dung",
				get_query: () => ({ filters: { has_variants: 0 } }),
			},
			{ fieldtype: "Section Break", label: __("Thuộc Tính Điều Kiện") },
			{ fieldtype: "HTML", fieldname: "attrs" },
		],
		primary_action_label: __("Xác Nhận"),
		primary_action(values) {
			const cond_attrs = data.attributes
				.filter((a) => sel[a.name].length)
				.map((a) => ({ name: a.name, values: sel[a.name].slice() }));

			if (!cond_attrs.length) {
				frappe.msgprint(__("Vui lòng chọn ít nhất một thuộc tính"));
				return;
			}

			// Chặn trùng ngay trên giao diện cho người dùng biết sớm. Server vẫn kiểm lại
			// khi lưu (BOMTemplate.resolve_rules) — đây chỉ là lớp cảnh báo sớm.
			const clash = find_overlap(frm, row.bom_component, cond_attrs);
			if (clash) {
				frappe.msgprint(
					__("Điều kiện này trùng với rule #{0} ({1}) của cùng thành phần", [
						clash.idx,
						clash.cond_label || "",
					])
				);
				return;
			}

			// Tích ô thì PHẢI bỏ trống NVL — server chặn trường hợp vừa tích vừa có NVL
			// (BOMTemplate.validate_rule_items). Người dùng chọn NVL rồi mới tích ô thì giá
			// trị cũ vẫn nằm trong dialog, không dọn ở đây là lưu xong mới báo lỗi.
			const new_rule = frm.add_child("bom_rules", {
				bom_component: row.bom_component,
				item: values.khong_su_dung ? null : values.item,
				khong_su_dung: values.khong_su_dung ? 1 : 0,
				cond_attrs: JSON.stringify(cond_attrs),
				cond_label: describe_cond(cond_attrs),
			});

			frm.refresh_field("bom_rules");
			dialog.hide();
			frappe.show_alert(
				{ message: __("Đã thêm rule cho {0}", [row.bom_component]), indicator: "green" },
				5
			);
		},
	});

	render_attributes(dialog, data, sel, frm);
	dialog.show();
}

function describe_cond(cond_attrs) {
	return cond_attrs.map((c) => `${c.name}: ${c.values.join(", ")}`).join(" · ");
}

/* Trùng khi 2 rule cùng thành phần cùng phủ ít nhất 1 biến thể. Không so chuỗi điều kiện:
   hai điều kiện viết khác nhau vẫn có thể phủ chung biến thể. */
function find_overlap(frm, bom_component, cond_attrs) {
	const covers = (a, b) =>
		// b có giao với a trên MỌI thuộc tính chung -> 2 điều kiện giao nhau
		a.every((ca) => {
			const cb = b.find((x) => x.name === ca.name);
			return !cb || cb.values.some((v) => ca.values.indexOf(v) > -1);
		});

	const same = (frm.doc.bom_rules || []).filter((r) => r.bom_component === bom_component);
	for (const existing of same) {
		let cond;
		try {
			cond = JSON.parse(existing.cond_attrs || "[]");
		} catch (e) {
			continue;
		}
		if (!cond.length) continue;
		if (covers(cond_attrs, cond) && covers(cond, cond_attrs)) {
			return existing;
		}
	}
	return null;
}

function render_attributes(dialog, data, sel, frm, on_change) {
	const wrapper = dialog.fields_dict.attrs.$wrapper;

	const blocks = data.attributes
		.map(
			(a, ai) => `
			<div class="hkled-attr" data-attr-block="${ai}"
					style="border:1px solid var(--border-color);border-radius:6px;
					padding:8px 10px;margin-bottom:8px">
				<div style="font-weight:600;margin-bottom:6px">
					${frappe.utils.escape_html(a.name)}
					<span class="text-muted small" data-count="${ai}"></span>
					<label style="font-weight:400;margin-left:10px;font-size:var(--text-sm)"
							class="text-muted">
						<input type="checkbox" data-all="${ai}"> ${__("Chọn tất cả")}
					</label>
				</div>
				<div>
					${a.values
						.map((v, vi) => {
							// PM-TASK-00105: giá trị chưa có biến thể nào dùng vẫn cho chọn (để
							// đặt rule trước cho hàng sắp có), nhưng làm mờ + chú thích để người
							// dùng không tick nhầm mà tưởng đang phủ hàng thật.
							const co_hang = (a.used_values || []).indexOf(v) > -1;
							return `
						<label style="display:inline-block;margin:0 10px 4px 0;font-weight:400"
								class="${co_hang ? "" : "text-muted"}"
								${co_hang ? "" : `title="${__("Chưa có biến thể nào dùng giá trị này")}"`}>
							<input type="checkbox" data-attr="${ai}" data-val="${vi}">
							${frappe.utils.escape_html(v)}${co_hang ? "" : " °"}
						</label>`;
						})
						.join("")}
				</div>
			</div>`
		)
		.join("");

	const co_gia_tri_chua_dung = data.attributes.some(
		(a) => a.values.length > (a.used_values || []).length
	);

	wrapper.html(`
		${blocks}
		${
			co_gia_tri_chua_dung
				? `<div class="text-muted small" style="margin-bottom:4px">${__(
						"Giá trị có dấu ° là chưa có biến thể nào dùng tới — vẫn đặt rule trước được."
				  )}</div>`
				: ""
		}
		<div class="text-muted small" data-matched style="margin-top:4px">
			${
				on_change
					? ""
					: __("Chưa chọn thuộc tính nào — rule phải phủ ít nhất một thuộc tính.")
			}
		</div>`);

	wrapper.find("input[data-attr]").on("change", function () {
		const a = data.attributes[Number($(this).attr("data-attr"))];
		const value = a.values[Number($(this).attr("data-val"))];
		const list = sel[a.name];
		const at = list.indexOf(value);
		if (this.checked && at === -1) {
			list.push(value);
		} else if (!this.checked && at > -1) {
			list.splice(at, 1);
		}
		bao_da_doi_tick(wrapper, data, sel, frm, on_change);
	});

	// PM-TASK-00102 — chọn tất cả giá trị của một đặc tính chỉ bằng một ô tick.
	// Đặc tính Công suất có 13 giá trị, tick tay từng cái vừa lâu vừa dễ sót.
	wrapper.find("input[data-all]").on("change", function () {
		const ai = Number($(this).attr("data-all"));
		const a = data.attributes[ai];
		// Gán mảng mới thay vì sửa tại chỗ cho gọn; sel[a.name] không được tham chiếu ở đâu khác.
		sel[a.name] = this.checked ? a.values.slice() : [];
		wrapper.find(`input[data-attr="${ai}"]`).prop("checked", this.checked);
		bao_da_doi_tick(wrapper, data, sel, frm, on_change);
	});
}

/* Hai chế độ dùng chung bảng tick: "Tạo Rule" cần đếm biến thể khớp (gọi server),
   "Tìm Rule" chỉ lọc trong bảng rule đã tải sẵn (không gọi server). Phần cập nhật
   ô đếm và ô "Chọn tất cả" thì cả hai đều cần. */
function bao_da_doi_tick(wrapper, data, sel, frm, on_change) {
	cap_nhat_o_tick(wrapper, data, sel);
	if (on_change) {
		on_change();
	} else {
		dem_bien_the_khop(wrapper, data, sel, frm);
	}
}

function cap_nhat_o_tick(wrapper, data, sel) {
	data.attributes.forEach((a, ai) => {
		const n = sel[a.name].length;
		wrapper.find(`[data-count="${ai}"]`).text(n ? `(${n})` : "");

		// Đồng bộ ngược ô "Chọn tất cả": tick tay đủ hết thì nó phải tự bật, bỏ một cái thì
		// tự tắt. Trạng thái lỡ cỡ để dạng gạch ngang cho người dùng biết đang chọn một phần.
		const o_tat_ca = wrapper.find(`input[data-all="${ai}"]`);
		o_tat_ca.prop("checked", n > 0 && n === a.values.length);
		o_tat_ca.prop("indeterminate", n > 0 && n < a.values.length);
	});
}

function lay_tich_dang_chon(data, sel) {
	return data.attributes
		.filter((a) => sel[a.name].length)
		.map((a) => ({ name: a.name, values: sel[a.name] }));
}

/* Gọi server đếm biến thể khớp thay vì đếm ở client: client không có bảng thuộc tính của
   hàng chục nghìn biến thể, tải về chỉ để đếm là quá nặng. */
function dem_bien_the_khop(wrapper, data, sel, frm) {
	const cond_attrs = lay_tich_dang_chon(data, sel);

	const box = wrapper.find("[data-matched]");
	if (!cond_attrs.length) {
		box.text(__("Chưa chọn thuộc tính nào — rule phải phủ ít nhất một thuộc tính."));
		return;
	}

	// Mỗi lần tick là một lượt gọi server mất khoảng 1 giây (phải quét toàn bộ biến thể của
	// mặt hàng cha — 5.120 biến thể với DP01S). Tick nhanh vài ô là các lượt gọi chồng nhau và
	// lượt về SAU CÙNG chưa chắc là lượt MỚI NHẤT -> hiện số sai. Đánh số lượt và chỉ nhận
	// kết quả của lượt mới nhất.
	const luot = (dem_bien_the_khop._luot = (dem_bien_the_khop._luot || 0) + 1);
	box.text(__("Đang đếm..."));

	frappe.call({
		method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.count_matched_variants",
		args: {
			item_template: frm.doc.item_template,
			cond_attrs: JSON.stringify(cond_attrs),
		},
		callback(r) {
			if (luot !== dem_bien_the_khop._luot) {
				return; // đã có lượt mới hơn, bỏ kết quả cũ
			}
			const res = r.message || {};
			const sample = (res.sample || []).join(", ");
			box.html(
				res.matched
					? __("Khớp <b>{0}</b>/{1} biến thể{2}", [
							res.matched,
							data.total_variants,
							sample ? ` — ${__("ví dụ")}: ${frappe.utils.escape_html(sample)}` : "",
					  ])
					: __("Không biến thể nào khớp điều kiện này")
			);
		},
	});
}

/* ------------------------------------------------------------------------- *
 * TÌM RULE — Thắng chốt 26/08 09:47 (PM-FEAT-00007)
 *
 * Vì sao cần: bảng Công Thức BOM của một template lớn có tới vài trăm dòng
 * (DP01S: 316 rule — riêng thành phần Module đã 128 dòng). Muốn sửa Nguyên Vật
 * Liệu của đúng một rule thì phải cuộn tay dò từng dòng, không làm nổi. Trước
 * khi có nút này, đường duy nhất người dùng chạm được tới điều kiện là bấm
 * "Tạo Rule" tạo lại — tức là đẻ thêm rule trùng chứ không phải sửa.
 *
 * Cách lọc: LỌC ĐÚNG, không đoán "dòng giống nhất". Một rule chỉ hiện ra khi
 * điều kiện của nó THẬT SỰ phủ được tổ hợp vừa tích. "Giống nhất" nguy ở chỗ
 * khi không có dòng nào đúng nó vẫn tự tin đưa ra một dòng gần đúng, người dùng
 * sửa nhầm dòng đó mà không biết — sai âm thầm.
 *
 * Bảo đảm: tích ĐỦ mọi thuộc tính thì kết quả LUÔN nhiều nhất một rule, vì
 * BOMTemplate.resolve_rules đã cấm hai rule cùng thành phần cùng phủ một biến
 * thể. Tích thiếu thì ra nhiều dòng — lúc đó có dòng nhắc còn thiếu thuộc tính
 * nào, để người dùng tự thu hẹp chứ không phải đoán.
 * ------------------------------------------------------------------------- */

const NHAN_NUT_TIM_RULE = "Tìm Rule";

frappe.ui.form.on("BOM Template", {
	refresh(frm) {
		const grid = frm.fields_dict.bom_rules && frm.fields_dict.bom_rules.grid;
		if (!grid) {
			return;
		}
		grid.add_custom_button(__(NHAN_NUT_TIM_RULE), () => mo_tim_rule(frm), "top");
	},
});

function mo_tim_rule(frm) {
	if (!frm.doc.item_template) {
		frappe.msgprint(__("Vui lòng chọn Mặt Hàng Cha trước"));
		return;
	}
	if (!(frm.doc.bom_rules || []).length) {
		frappe.msgprint(__("Bảng Công Thức BOM chưa có rule nào để tìm"));
		return;
	}

	frappe.call({
		method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.get_condition_attributes",
		args: { item_template: frm.doc.item_template },
		freeze: true,
		freeze_message: __("Đang lấy danh sách thuộc tính..."),
		callback(r) {
			const data = r.message || {};
			if (!(data.attributes || []).length) {
				frappe.msgprint(
					__("Mặt hàng cha {0} chưa có biến thể nào để đặt điều kiện", [
						frm.doc.item_template,
					])
				);
				return;
			}
			hien_hop_tim_rule(frm, data);
		},
	});
}

function hien_hop_tim_rule(frm, data) {
	// Chỉ liệt kê thành phần THỰC SỰ có rule. Đưa vào cả thành phần không có rule nào
	// thì người dùng chọn xong nhận kết quả rỗng và không biết là do chọn nhầm chỗ hay
	// do tích sai điều kiện.
	const so_rule = {};
	(frm.doc.bom_rules || []).forEach((r) => {
		if (r.bom_component) {
			so_rule[r.bom_component] = (so_rule[r.bom_component] || 0) + 1;
		}
	});
	const thanh_phan = Object.keys(so_rule).sort();
	if (!thanh_phan.length) {
		frappe.msgprint(__("Không rule nào trong bảng có Thành Phần BOM để tìm theo"));
		return;
	}

	const sel = {};
	data.attributes.forEach((a) => (sel[a.name] = []));

	const dialog = new frappe.ui.Dialog({
		title: __("Tìm Rule"),
		size: "large",
		fields: [
			{
				fieldtype: "Select",
				fieldname: "bom_component",
				label: __("Thành Phần BOM"),
				reqd: 1,
				options: thanh_phan.map((c) => ({
					// frappe.ui.form.add_options nhét label bằng .html() nên phải escape
					label: `${frappe.utils.escape_html(c)} — ${so_rule[c]} rule`,
					value: c,
				})),
				default: thanh_phan[0],
				onchange: () => ve_ket_qua(frm, dialog, data, sel),
			},
			{ fieldtype: "Section Break", label: __("Thuộc Tính Điều Kiện") },
			{ fieldtype: "HTML", fieldname: "attrs" },
			{ fieldtype: "Section Break", label: __("Kết Quả") },
			{ fieldtype: "HTML", fieldname: "ket_qua" },
		],
	});

	render_attributes(dialog, data, sel, frm, () => ve_ket_qua(frm, dialog, data, sel));
	dialog.show();
	// add_options tự chọn option đầu tiên, nhưng đặt lại cho chắc: ve_ket_qua đọc
	// bằng get_value, rỗng là ra màn hình trống ngay lúc vừa mở.
	dialog.set_value("bom_component", thanh_phan[0]);
	ve_ket_qua(frm, dialog, data, sel);
}

/* Rule hiện ra khi điều kiện của nó CÓ THỂ phủ tổ hợp vừa tích: với mọi thuộc tính
   người dùng đã tích mà rule cũng ràng buộc, hai bên phải giao nhau. Thuộc tính rule
   không nhắc tới nghĩa là rule không quan tâm -> không loại. Đây đúng là phép so mà
   BOMTemplate.variant_matches dùng lúc tạo BOM, nên cái tìm được cũng chính là cái
   sẽ chạy. */
function rule_phu_tich(cond, tich) {
	return tich.every((t) => {
		const c = cond.find((x) => x.name === t.name);
		return !c || c.values.some((v) => t.values.indexOf(v) > -1);
	});
}

function loc_rule(frm, bom_component, tich) {
	const khop = [];
	const kho_doc = [];

	(frm.doc.bom_rules || []).forEach((r) => {
		if (r.bom_component !== bom_component) {
			return;
		}
		let cond = null;
		try {
			cond = JSON.parse(r.cond_attrs || "[]");
		} catch (e) {
			cond = null;
		}
		// Rule không đọc được điều kiện thì KHÔNG lọc lẫn vào kết quả, nhưng cũng không
		// giấu đi — giấu một dòng hỏng là để người dùng tưởng thành phần này không có
		// rule nào, rồi tạo thêm một rule chồng lên.
		if (!cond || !cond.length) {
			kho_doc.push(r);
			return;
		}
		if (rule_phu_tich(cond, tich)) {
			khop.push({ row: r, cond: cond });
		}
	});

	return { khop: khop, kho_doc: kho_doc };
}

function ve_ket_qua(frm, dialog, data, sel) {
	const box = dialog.fields_dict.ket_qua.$wrapper;
	const comp = dialog.get_value("bom_component");
	if (!comp) {
		box.html(`<div class="text-muted small">${__("Chọn Thành Phần BOM để bắt đầu")}</div>`);
		return;
	}

	an_thuoc_tinh_khong_lien_quan(dialog, data, comp, frm);

	const tich = lay_tich_dang_chon(data, sel);
	const kq = loc_rule(frm, comp, tich);

	// Thuộc tính mà các rule tìm được có ràng buộc nhưng người dùng CHƯA tích — chính
	// là thứ đang làm kết quả ra nhiều dòng. Nêu tên ra để họ biết tích thêm cái gì.
	const da_tich = tich.map((t) => t.name);
	const con_thieu = [];
	kq.khop.forEach((k) =>
		k.cond.forEach((c) => {
			if (da_tich.indexOf(c.name) === -1 && con_thieu.indexOf(c.name) === -1) {
				con_thieu.push(c.name);
			}
		})
	);

	const dong = kq.khop
		.map((k) => {
			const r = k.row;
			const nvl = r.khong_su_dung
				? `<span class="text-muted">${__("Không sử dụng thành phần này")}</span>`
				: r.item
				? `<b>${frappe.utils.escape_html(r.item)}</b>`
				: `<span class="text-danger">${__("chưa đặt Nguyên Vật Liệu")}</span>`;
			return `
			<div class="hkled-kq-rule" data-docname="${frappe.utils.escape_html(r.name)}"
					style="border:1px solid var(--border-color);border-radius:6px;padding:6px 10px;
							margin-bottom:6px;cursor:pointer">
				<div><b>#${r.idx}</b> — ${nvl}</div>
				<div class="text-muted small">
					${frappe.utils.escape_html(r.cond_label || "")}
					· ${__("phủ {0} biến thể", [r.matched_count || 0])}
				</div>
			</div>`;
		})
		.join("");

	let dau_de;
	if (!kq.khop.length) {
		dau_de = `<div class="text-muted" style="margin-bottom:6px">${__(
			"Không rule nào của thành phần này phủ tổ hợp vừa tích."
		)}</div>`;
	} else {
		dau_de = `<div class="text-muted small" style="margin-bottom:6px">${__(
			"Tìm được <b>{0}</b> rule — bấm vào một dòng để nhảy tới đúng dòng đó trong bảng.",
			[kq.khop.length]
		)}</div>`;
	}

	const nhac_thieu =
		kq.khop.length > 1 && con_thieu.length
			? `<div class="text-muted small" style="margin-top:4px">${__(
					"Còn ra nhiều dòng vì chưa tích: <b>{0}</b>. Tích đủ thì chỉ còn đúng một rule.",
					[frappe.utils.escape_html(con_thieu.join(", "))]
			  )}</div>`
			: "";

	const canh_bao_hong = kq.kho_doc.length
		? `<div class="text-danger small" style="margin-top:8px">${__(
				"⚠ {0} rule của thành phần này có ô Điều Kiện trống hoặc không đọc được, nên không lọc theo được: {1}",
				[
					kq.kho_doc.length,
					kq.kho_doc.map((r) => `#${r.idx}`).join(", "),
				]
		  )}</div>`
		: "";

	box.html(`${dau_de}${dong}${nhac_thieu}${canh_bao_hong}`);

	box.find(".hkled-kq-rule").on("click", function () {
		nhay_toi_dong(frm, dialog, $(this).attr("data-docname"));
	});
}

/* Bảng Công Thức BOM chia trang 50 dòng một, nên dòng cần tới thường KHÔNG nằm trong
   trang đang hiện — grid_rows_by_docname lúc đó không có nó. Phải sang đúng trang
   trước rồi mới mở dòng ra được. */
function nhay_toi_dong(frm, dialog, docname) {
	const grid = frm.fields_dict.bom_rules.grid;
	const ds = grid.data || frm.doc.bom_rules || [];
	const vi_tri = ds.findIndex((d) => d.name === docname);
	if (vi_tri === -1) {
		frappe.msgprint(__("Không thấy dòng này trong bảng — có thể bảng vừa được lọc lại."));
		return;
	}

	const phan_trang = grid.grid_pagination;
	if (phan_trang) {
		const trang = Math.floor(vi_tri / phan_trang.page_length) + 1;
		if (phan_trang.page_index !== trang) {
			phan_trang.go_to_page(trang);
		}
	}

	dialog.hide();

	const dong = grid.grid_rows_by_docname[docname];
	if (!dong) {
		frappe.msgprint(__("Không mở được dòng #{0} — thử cuộn tìm tay giúp em.", [vi_tri + 1]));
		return;
	}
	dong.toggle_view(true);
	frappe.utils.scroll_to(dong.wrapper || dong.row, true, 40, null, null, true);
}

/* Bảng tick liệt kê MỌI thuộc tính của mặt hàng cha, nhưng mỗi thành phần chỉ bị ràng buộc
   bởi vài cái — Bộ vỏ đèn chỉ dùng 2 trong 7. Bày đủ 7 khối là bắt người dùng tự đoán khối
   nào có tác dụng, đúng cái việc mà nút này sinh ra để bỏ đi. Ẩn khối không liên quan, nhưng
   NÊU TÊN ra chứ không giấu im.

   Tick còn sót ở khối bị ẩn không làm sai kết quả: rule không nhắc tới thuộc tính đó thì
   rule_phu_tich không loại nó. Nên chỉ ẩn, không xoá tick — đổi thành phần qua lại vẫn giữ
   nguyên cái người dùng đã tick. */
function an_thuoc_tinh_khong_lien_quan(dialog, data, comp, frm) {
	const dang_dung = {};
	(frm.doc.bom_rules || []).forEach((r) => {
		if (r.bom_component !== comp) {
			return;
		}
		let cond = null;
		try {
			cond = JSON.parse(r.cond_attrs || "[]");
		} catch (e) {
			return;
		}
		(cond || []).forEach((c) => (dang_dung[c.name] = 1));
	});

	const wrapper = dialog.fields_dict.attrs.$wrapper;
	const an_bot = [];
	data.attributes.forEach((a, ai) => {
		const co_dung = !!dang_dung[a.name];
		wrapper.find(`[data-attr-block="${ai}"]`).toggle(co_dung);
		if (!co_dung) {
			an_bot.push(a.name);
		}
	});

	let ghi_chu = wrapper.find("[data-an-bot]");
	if (!ghi_chu.length) {
		ghi_chu = $(
			'<div class="text-muted small" data-an-bot style="margin-bottom:8px"></div>'
		).prependTo(wrapper);
	}
	ghi_chu.html(
		an_bot.length
			? __("Đang ẩn {0} thuộc tính mà không rule nào của <b>{1}</b> dùng tới: {2}", [
					an_bot.length,
					frappe.utils.escape_html(comp),
					frappe.utils.escape_html(an_bot.join(", ")),
			  ])
			: ""
	);
}
