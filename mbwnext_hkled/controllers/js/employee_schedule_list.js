/* GAP-2 — nút "Tạo Nhanh" trên danh sách Lịch Làm Việc Nhân Sự.
   Phân ca cho cả đội trong một lần thay vì tạo từng bản ghi.
   Chốt C10 + C10b: theo khoảng "Từ Ngày – Đến Ngày" kèm tick chọn thứ trong tuần. */

// Thứ theo chuẩn JS: Chủ nhật = 0. Mặc định tick T2–T7, bỏ Chủ nhật.
const HKLED_WEEKDAYS = [
	{ dow: 1, label: "T2" },
	{ dow: 2, label: "T3" },
	{ dow: 3, label: "T4" },
	{ dow: 4, label: "T5" },
	{ dow: 5, label: "T6" },
	{ dow: 6, label: "T7" },
	{ dow: 0, label: "CN" },
];
const HKLED_DEFAULT_WEEKDAYS = [1, 2, 3, 4, 5, 6];
const HKLED_MAX_RANGE_DAYS = 62;

frappe.listview_settings["Employee Schedule"] = {
	onload(listview) {
		listview.page.add_inner_button(__("Tạo Nhanh"), () => show_quick_create(listview));
	},
};

function show_quick_create(listview) {
	const dialog = new frappe.ui.Dialog({
		title: __("Tạo Nhanh Lịch Làm Việc"),
		size: "large",
		fields: [
			{
				fieldtype: "Link",
				fieldname: "work_team",
				label: __("Đội Sản Xuất"),
				options: "Work Team",
				reqd: 1,
				get_query: () => ({ filters: { is_active: 1 } }),
				onchange() {
					load_members(dialog, this.get_value());
				},
			},
			{ fieldtype: "Column Break" },
			{
				fieldtype: "Date",
				fieldname: "from_date",
				label: __("Từ Ngày"),
				reqd: 1,
				default: frappe.datetime.get_today(),
				onchange: () => update_count(dialog),
			},
			{
				fieldtype: "Date",
				fieldname: "to_date",
				label: __("Đến Ngày"),
				reqd: 1,
				default: frappe.datetime.get_today(),
				onchange: () => update_count(dialog),
			},
			{ fieldtype: "Section Break" },
			{ fieldtype: "HTML", fieldname: "weekdays", label: __("Thứ Trong Tuần") },
			{ fieldtype: "Section Break" },
			{
				fieldtype: "Check",
				fieldname: "is_over_time",
				label: __("Là Tăng Ca"),
				onchange: () => toggle_over_time(dialog),
			},
			{
				fieldtype: "Link",
				fieldname: "shift_type",
				label: __("Ca Làm Việc"),
				options: "Shift Type",
			},
			{ fieldtype: "Column Break" },
			{
				fieldtype: "Time",
				fieldname: "start",
				label: __("Bắt Đầu"),
				default: "18:00:00",
				hidden: 1,
			},
			{
				fieldtype: "Time",
				fieldname: "end",
				label: __("Kết Thúc"),
				default: "21:00:00",
				hidden: 1,
			},
			{ fieldtype: "Section Break" },
			{ fieldtype: "HTML", fieldname: "members" },
			{ fieldtype: "HTML", fieldname: "summary" },
		],
		primary_action_label: __("Tạo Lịch Làm Việc"),
		primary_action: (values) => submit_quick_create(dialog, listview, values),
	});

	dialog.selected_weekdays = [...HKLED_DEFAULT_WEEKDAYS];
	dialog.members = [];
	render_weekdays(dialog);
	dialog.show();
	update_count(dialog);
}

function render_weekdays(dialog) {
	const wrapper = dialog.fields_dict.weekdays.$wrapper;
	const chips = HKLED_WEEKDAYS.map(
		(d) => `
		<label style="display:inline-flex;align-items:center;gap:6px;margin:0 8px 6px 0;
			border:1px solid var(--border-color);border-radius:6px;padding:5px 10px;cursor:pointer">
			<input type="checkbox" data-dow="${d.dow}"
				${dialog.selected_weekdays.includes(d.dow) ? "checked" : ""}> ${d.label}
		</label>`
	).join("");

	wrapper.html(
		`<div class="small text-muted" style="margin-bottom:6px">${__("Thứ Trong Tuần")}</div>
		 <div>${chips}</div>`
	);

	wrapper.find("input[type=checkbox]").on("change", function () {
		const dow = Number($(this).attr("data-dow"));
		if (this.checked) {
			if (!dialog.selected_weekdays.includes(dow)) dialog.selected_weekdays.push(dow);
		} else {
			dialog.selected_weekdays = dialog.selected_weekdays.filter((d) => d !== dow);
		}
		update_count(dialog);
	});
}

function toggle_over_time(dialog) {
	const on = dialog.get_value("is_over_time");
	dialog.set_df_property("shift_type", "hidden", on ? 1 : 0);
	dialog.set_df_property("shift_type", "reqd", on ? 0 : 1);
	dialog.set_df_property("start", "hidden", on ? 0 : 1);
	dialog.set_df_property("end", "hidden", on ? 0 : 1);
}

function load_members(dialog, work_team) {
	const wrapper = dialog.fields_dict.members.$wrapper;
	if (!work_team) {
		wrapper.empty();
		dialog.members = [];
		update_count(dialog);
		return;
	}

	frappe.call({
		method: "mbwnext_hkled.api.work_team.get_team_members",
		args: { work_team },
		callback(r) {
			// Chọn đội -> tự nạp nhân sự Công nhân đang Active, tick sẵn toàn bộ; bỏ tick ai nghỉ.
			dialog.members = ((r.message || {}).members || []).map((m) => ({ ...m, checked: true }));
			render_members(dialog);
			update_count(dialog);
		},
	});
}

function render_members(dialog) {
	const wrapper = dialog.fields_dict.members.$wrapper;
	if (!dialog.members.length) {
		wrapper.html(
			`<div class="text-muted small">${__(
				"Đội này chưa có nhân sự Công nhân nào đang làm việc."
			)}</div>`
		);
		return;
	}

	const body = dialog.members
		.map(
			(m, i) => `
			<tr>
				<td style="width:34px"><input type="checkbox" data-idx="${i}" ${m.checked ? "checked" : ""}></td>
				<td>${frappe.utils.escape_html(m.employee_name || m.employee)}</td>
				<td>${frappe.utils.escape_html(m.employee_level || "")}</td>
				<td class="text-right">${m.performance_factor || 0}</td>
			</tr>`
		)
		.join("");

	wrapper.html(`
		<table class="table table-bordered" style="margin:0">
			<thead><tr>
				<th></th><th>${__("Nhân sự")}</th><th>${__("Bậc thợ")}</th>
				<th class="text-right">${__("Nguồn lực (%)")}</th>
			</tr></thead>
			<tbody>${body}</tbody>
		</table>`);

	wrapper.find("input[type=checkbox]").on("change", function () {
		dialog.members[Number($(this).attr("data-idx"))].checked = this.checked;
	});
}

/* Đếm trước số bản ghi sẽ tạo: 1 tuần × 10 người đã là 70 bản ghi, người dùng cần thấy
   con số trước khi bấm chứ không phải sau khi lỡ chọn cả tháng. */
function count_matching_days(from_date, to_date, weekdays) {
	if (!from_date || !to_date || !weekdays.length) return { span: 0, matched: 0 };
	const a = frappe.datetime.str_to_obj(from_date);
	const b = frappe.datetime.str_to_obj(to_date);
	const span = Math.round((b - a) / 86400000) + 1;
	if (span <= 0) return { span, matched: 0 };

	let matched = 0;
	for (let i = 0; i < span; i++) {
		const d = new Date(a.getTime() + i * 86400000);
		if (weekdays.includes(d.getDay())) matched++;
	}
	return { span, matched };
}

function update_count(dialog) {
	const wrapper = dialog.fields_dict.summary.$wrapper;
	const picked = (dialog.members || []).filter((m) => m.checked).length;
	const { span, matched } = count_matching_days(
		dialog.get_value("from_date"),
		dialog.get_value("to_date"),
		dialog.selected_weekdays
	);

	let msg;
	let color = "var(--text-muted)";
	if (span <= 0) {
		msg = __("Đến Ngày phải từ Từ Ngày trở đi.");
		color = "var(--red-500)";
	} else if (span > HKLED_MAX_RANGE_DAYS) {
		msg = __("Khoảng {0} ngày, vượt quá {1} ngày cho phép.", [span, HKLED_MAX_RANGE_DAYS]);
		color = "var(--red-500)";
	} else if (!matched) {
		msg = __("Không ngày nào trong khoảng khớp thứ đã chọn.");
		color = "var(--red-500)";
	} else if (!picked) {
		msg = __("Chưa chọn nhân sự nào.");
		color = "var(--red-500)";
	} else {
		const skipped = span - matched;
		msg = __("Sẽ tạo {0} lịch làm việc ({1} ngày × {2} nhân sự{3}).", [
			matched * picked,
			matched,
			picked,
			skipped > 0 ? __(", bỏ qua {0} ngày không khớp thứ", [skipped]) : "",
		]);
	}

	wrapper.html(`<div style="font-weight:500;color:${color}">${msg}</div>`);
}

function submit_quick_create(dialog, listview, values) {
	const employees = (dialog.members || []).filter((m) => m.checked).map((m) => m.employee);

	frappe.call({
		method: "mbwnext_hkled.api.work_team.bulk_create_schedule",
		args: {
			work_team: values.work_team,
			from_date: values.from_date,
			to_date: values.to_date,
			weekdays: dialog.selected_weekdays,
			employees: employees,
			shift_type: values.shift_type,
			is_over_time: values.is_over_time ? 1 : 0,
			start: values.start,
			end: values.end,
		},
		freeze: true,
		freeze_message: __("Đang tạo lịch làm việc..."),
		callback(r) {
			const res = r.message;
			if (!res) return;

			// Bỏ qua dòng trùng thì phải nói RÕ bỏ dòng nào, không im lặng.
			let message = __("Đã tạo {0} lịch làm việc.", [res.created]);
			if (res.skipped && res.skipped.length) {
				const lines = res.skipped
					.slice(0, 10)
					.map((s) => `${frappe.utils.escape_html(s.employee)} — ${s.date}`)
					.join("<br>");
				const more =
					res.skipped.length > 10
						? `<br>${__("... và {0} dòng nữa", [res.skipped.length - 10])}`
						: "";
				message += `<br><br>${__("Bỏ qua {0} dòng do trùng lịch:", [
					res.skipped.length,
				])}<br>${lines}${more}`;
			}

			dialog.hide();
			frappe.msgprint({
				title: __("Kết Quả Tạo Nhanh"),
				message: message,
				indicator: res.created ? "green" : "orange",
			});
			listview.refresh();
		},
	});
}
