frappe.ui.form.on("BOM Template", {
	item_template(frm) {
		// Gợi ý Nhóm Công Thức theo prefix mã Item Template — người dùng vẫn sửa được.
		if (!frm.doc.item_template || frm.doc.rule_group) return;

		frappe.call({
			method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.suggest_rule_group",
			args: { item_template: frm.doc.item_template },
			callback(r) {
				if (r.message) frm.set_value("rule_group", r.message);
			},
		});
	},
});

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
		method: "mbwnext_hkled.mbwnext_hkled.doctype.bom_template.bom_template.get_rule_condition_values",
		args: { item_template: frm.doc.item_template },
		freeze: true,
		callback: function (r) {
			const data = r.message || {};
			const values = data.values || [];
			if (!values.length) {
				frappe.msgprint(
					__("Không tìm thấy giá trị đặc tính {0} nào cho mặt hàng cha này", [
						data.attribute || "",
					])
				);
				return;
			}
			show_rule_dialog(frm, row, data.attribute, values);
		},
	});
});

/* Mỗi giá trị đặc tính điều kiện (Nguồn) = 1 dòng BOM Rule, KHÔNG sinh ma trận biến thể.
   Số lượng không hỏi ở đây: do Server Script hkled_resolve_bom_qty tính lúc tạo BOM. */
function show_rule_dialog(frm, row, attribute, values) {
	const existing = {};
	(frm.doc.bom_rule || []).forEach((r) => {
		if (r.bom_component === row.bom_component) existing[r.condition_value] = r.item;
	});

	const fields = [
		{
			fieldtype: "HTML",
			fieldname: "intro",
			options: `<div class="text-muted small" style="margin-bottom:8px">
				${__("Thành Phần BOM")}: <b>${frappe.utils.escape_html(row.bom_component)}</b> ·
				${__("Mặt Hàng Cha")}: <b>${frappe.utils.escape_html(frm.doc.item_template)}</b><br>
				${__("Chọn Nguyên Vật Liệu cho từng giá trị {0}. Bỏ trống = không tạo dòng.", [
					`<b>${frappe.utils.escape_html(attribute)}</b>`,
				])}<br>
				${__("Số lượng do công thức tự tính khi Tạo BOM, không nhập ở đây.")}
			</div>`,
		},
	];

	values.forEach((value, idx) => {
		fields.push({
			fieldtype: "Link",
			options: "Item",
			fieldname: `item_${idx}`,
			label: value,
			default: existing[value] || "",
			get_query: () => ({ filters: { has_variants: 0 } }),
		});
	});

	const dialog = new frappe.ui.Dialog({
		title: __("Tạo Rule — Chọn NVL theo {0}", [attribute]),
		size: "small",
		fields: fields,
		primary_action_label: __("Xác Nhận"),
		primary_action(form_values) {
			let added = 0;
			let updated = 0;

			values.forEach((value, idx) => {
				const item = form_values[`item_${idx}`];
				if (!item) return;

				const found = (frm.doc.bom_rule || []).find(
					(r) => r.bom_component === row.bom_component && r.condition_value === value
				);
				if (found) {
					if (found.item !== item) {
						found.item = item;
						updated++;
					}
				} else {
					const new_row = frm.add_child("bom_rule");
					new_row.bom_component = row.bom_component;
					new_row.condition_value = value;
					new_row.item = item;
					added++;
				}
			});

			if (!added && !updated) {
				frappe.msgprint(__("Chưa chọn Nguyên Vật Liệu nào"));
				return;
			}

			frm.refresh_field("bom_rule");
			dialog.hide();
			frappe.show_alert({
				message: __("Đã thêm {0} dòng, cập nhật {1} dòng trong Công Thức BOM", [added, updated]),
				indicator: "green",
			});
		},
	});
	dialog.show();
}
