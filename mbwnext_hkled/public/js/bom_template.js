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
		method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.get_template_attributes",
		args: { item_template: frm.doc.item_template },
		freeze: true,
		callback: function (r) {
			const attributes = r.message || [];
			if (!attributes.length) {
				frappe.msgprint(__("Mặt hàng cha chưa khai báo Đặc Tính nào"));
				return;
			}
			show_condition_dialog(frm, row, attributes);
		},
	});
});

function show_condition_dialog(frm, row, attributes) {
	const dialog = new frappe.ui.Dialog({
		title: __("Chọn Điều Kiện"),
		fields: attributes.map((a) => ({
			fieldtype: "MultiCheck",
			fieldname: frappe.scrub(a.attribute),
			label: a.attribute,
			options: a.values.map((v) => ({ label: v, value: v })),
			columns: 2,
		})),
		primary_action_label: __("Tiếp Theo"),
		primary_action(values) {
			const selected = attributes
				.map((a) => ({
					attribute: a.attribute,
					values: values[frappe.scrub(a.attribute)] || [],
				}))
				.filter((a) => a.values.length);

			if (!selected.length) {
				frappe.msgprint(__("Vui lòng chọn ít nhất 1 giá trị đặc tính"));
				return;
			}

			const combos = cartesian_product(selected);
			dialog.hide();
			show_material_dialog(frm, row, combos);
		},
	});
	dialog.show();
}

function cartesian_product(selected) {
	let combos = [{}];
	selected.forEach((attr) => {
		const next = [];
		combos.forEach((combo) => {
			attr.values.forEach((val) => {
				next.push(Object.assign({}, combo, { [attr.attribute]: val }));
			});
		});
		combos = next;
	});
	return combos;
}

function show_material_dialog(frm, row, combos) {
	const dialog = new frappe.ui.Dialog({
		title: __("Chọn Nguyên Vật Liệu"),
		fields: [
			{
				fieldtype: "Link",
				fieldname: "item",
				label: __("Nguyên Vật Liệu"),
				options: "Item",
				reqd: 1,
				get_query: () => ({ filters: { has_variants: 0 } }),
			},
			{
				fieldtype: "Int",
				fieldname: "qty",
				label: __("Số Lượng"),
				reqd: 1,
			},
		],
		primary_action_label: __("Xác Nhận"),
		primary_action(values) {
			frappe.call({
				method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.get_matching_variants",
				args: {
					item_template: frm.doc.item_template,
					combos: combos,
				},
				freeze: true,
				callback: function (r) {
					const items = r.message || [];
					if (!items.length) {
						frappe.msgprint(__("Không tìm thấy mặt hàng biến thể nào khớp điều kiện đã chọn"));
						return;
					}
					fill_bom_rule(frm, row, items, values.item, values.qty);
					dialog.hide();
				},
			});
		},
	});
	dialog.show();
}

function fill_bom_rule(frm, row, items, material, qty) {
	let added = 0;
	let updated = 0;

	items.forEach((item_code) => {
		const existing = (frm.doc.bom_rule || []).find(
			(r) => r.item_to_manufacture === item_code && r.bom_component === row.bom_component
		);
		if (existing) {
			existing.item = material;
			existing.qty = qty;
			updated++;
		} else {
			const new_row = frm.add_child("bom_rule");
			new_row.item_to_manufacture = item_code;
			new_row.bom_component = row.bom_component;
			new_row.item = material;
			new_row.qty = qty;
			added++;
		}
	});

	frm.refresh_field("bom_rule");
	frappe.show_alert({
		message: __("Đã thêm {0} dòng, cập nhật {1} dòng trong Công Thức BOM", [added, updated]),
		indicator: "green",
	});
}
