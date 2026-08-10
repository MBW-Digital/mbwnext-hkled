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
				fieldtype: "Link",
				options: "Item",
				fieldname: "item",
				label: __("Nguyên Vật Liệu áp dụng cho rule này"),
				reqd: 1,
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

			const new_rule = frm.add_child("bom_rules", {
				bom_component: row.bom_component,
				item: values.item,
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

function render_attributes(dialog, data, sel, frm) {
	const wrapper = dialog.fields_dict.attrs.$wrapper;

	const blocks = data.attributes
		.map(
			(a, ai) => `
			<div class="hkled-attr" style="border:1px solid var(--border-color);border-radius:6px;
					padding:8px 10px;margin-bottom:8px">
				<div style="font-weight:600;margin-bottom:6px">
					${frappe.utils.escape_html(a.name)}
					<span class="text-muted small" data-count="${ai}"></span>
				</div>
				<div>
					${a.values
						.map(
							(v, vi) => `
						<label style="display:inline-block;margin:0 10px 4px 0;font-weight:400">
							<input type="checkbox" data-attr="${ai}" data-val="${vi}">
							${frappe.utils.escape_html(v)}
						</label>`
						)
						.join("")}
				</div>
			</div>`
		)
		.join("");

	wrapper.html(`
		${blocks}
		<div class="text-muted small" data-matched style="margin-top:4px">
			${__("Chưa chọn thuộc tính nào — rule phải phủ ít nhất một thuộc tính.")}
		</div>`);

	wrapper.find("input[type=checkbox]").on("change", function () {
		const a = data.attributes[Number($(this).attr("data-attr"))];
		const value = a.values[Number($(this).attr("data-val"))];
		const list = sel[a.name];
		const at = list.indexOf(value);
		if (this.checked && at === -1) {
			list.push(value);
		} else if (!this.checked && at > -1) {
			list.splice(at, 1);
		}
		update_counts(wrapper, data, sel, frm);
	});
}

/* Gọi server đếm biến thể khớp thay vì đếm ở client: client không có bảng thuộc tính của
   hàng chục nghìn biến thể, tải về chỉ để đếm là quá nặng. */
function update_counts(wrapper, data, sel, frm) {
	data.attributes.forEach((a, ai) => {
		const n = sel[a.name].length;
		wrapper.find(`[data-count="${ai}"]`).text(n ? `(${n})` : "");
	});

	const cond_attrs = data.attributes
		.filter((a) => sel[a.name].length)
		.map((a) => ({ name: a.name, values: sel[a.name] }));

	const box = wrapper.find("[data-matched]");
	if (!cond_attrs.length) {
		box.text(__("Chưa chọn thuộc tính nào — rule phải phủ ít nhất một thuộc tính."));
		return;
	}

	frappe.call({
		method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.count_matched_variants",
		args: {
			item_template: frm.doc.item_template,
			cond_attrs: JSON.stringify(cond_attrs),
		},
		callback(r) {
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
