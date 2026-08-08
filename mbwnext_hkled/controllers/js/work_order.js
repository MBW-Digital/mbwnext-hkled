frappe.ui.form.on("Work Order", {
	refresh(frm) {
		if (frm.doc.custom_start_time && (frm.doc.custom_work_order_employee || []).length) {
			frm.add_custom_button(__("Tính Lại Lịch"), () => recalculate_schedule(frm));
		}

		// GAP-3 (C8): chỉ hiện khi lệnh đã duyệt, đang In Process, và chưa từng ấn.
		if (
			frm.doc.docstatus === 1 &&
			frm.doc.status === "In Process" &&
			!frm.doc.custom_production_started
		) {
			frm.add_custom_button(__("Bắt Đầu Sản Xuất"), () => start_production(frm)).addClass(
				"btn-primary"
			);
		}

		// GAP-6: thêm cả đội vào bảng Nhân Công Tham Gia.
		if (frm.doc.docstatus < 2) {
			frm.add_custom_button(__("Thêm Đội Sản Xuất"), () => show_work_team_dialog(frm));
		}
	},
});

function recalculate_schedule(frm) {
	frappe.call({
		method: "mbwnext_hkled.api.work_order_schedule.recalculate_schedule",
		args: { work_order: frm.doc.name },
		freeze: true,
		freeze_message: __("Đang tính toán lịch sản xuất..."),
		callback: function (r) {
			if (!r.message) {
				return;
			}
			frappe.show_alert(
				{
					message: __("Thời gian kết thúc dự kiến: {0} ({1} phút)", [
						frappe.datetime.str_to_user(r.message.end_time),
						r.message.estimated_completion_time_minutes,
					]),
					indicator: "green",
				},
				7
			);
			frm.reload_doc();
		},
	});
}

/* Ấn một lần là ghi giờ thực tế rồi tính lại lịch — hỏi lại cho chắc vì không hoàn tác được. */
function start_production(frm) {
	frappe.confirm(
		__(
			"Ghi Thời Gian Bắt Đầu = giờ hiện tại và tính lại lịch?<br><br>Chỉ ấn được <b>một lần</b>, không hoàn tác được."
		),
		() => {
			frappe.call({
				method: "mbwnext_hkled.api.work_order_actions.start_production",
				args: { work_order: frm.doc.name },
				freeze: true,
				freeze_message: __("Đang bắt đầu sản xuất..."),
				callback: function (r) {
					if (!r.message) {
						return;
					}
					frappe.msgprint({
						title: __("Đã Bắt Đầu Sản Xuất"),
						message: __("Thời Gian Bắt Đầu: {0}<br>Kết thúc dự kiến: {1} ({2} phút)", [
							frappe.datetime.str_to_user(r.message.actual_start),
							frappe.datetime.str_to_user(r.message.end_time),
							r.message.estimated_completion_time_minutes,
						]),
						indicator: "green",
					});
					frm.reload_doc();
				},
			});
		}
	);
}

/* GAP-6 — chọn đội rồi tick nhân sự. Chỉ để thêm nhanh chứ KHÔNG ràng buộc (chốt C6):
   sau khi thêm vẫn xoá/sửa từng dòng tự do, nhân sự đổi đội về sau không làm đổi bảng này. */
function show_work_team_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __("Thêm Đội Sản Xuất"),
		fields: [
			{
				fieldtype: "Link",
				fieldname: "work_team",
				label: __("Đội Sản Xuất"),
				options: "Work Team",
				reqd: 1,
				get_query: () => ({ filters: { is_active: 1 } }),
				onchange() {
					load_team_members(dialog, frm, this.get_value());
				},
			},
			{ fieldtype: "HTML", fieldname: "members" },
		],
		primary_action_label: __("Xác Nhận"),
		primary_action() {
			const picked = (dialog.selected_members || []).filter(
				(m) => m.checked && !m.already_added
			);
			if (!picked.length) {
				frappe.msgprint(__("Chưa chọn nhân sự nào"));
				return;
			}

			// Điền luôn Bậc Thợ + Nguồn Lực, KHÔNG trông vào fetch_from của Link:
			// dòng thêm bằng add_child không kích hoạt vòng fetch, nên hai trường đó sẽ
			// rỗng và "Tính Lại Lịch" báo "chưa có Nguồn Lực (%) hợp lệ".
			// Cùng gốc với lỗi anh Thắng báo ở luồng tạo WO từ Kế Hoạch Sản Xuất (03/08).
			// API get_team_members đã trả sẵn 2 giá trị này nên không cần gọi thêm.
			picked.forEach((m) => {
				const row = frm.add_child("custom_work_order_employee", {
					employee: m.employee,
					employee_level: m.employee_level,
					performance_factor_: m.performance_factor,
				});
				frm.script_manager.trigger("employee", row.doctype, row.name);
			});

			frm.refresh_field("custom_work_order_employee");
			dialog.hide();
			frappe.show_alert(
				{ message: __("Đã thêm {0} nhân sự", [picked.length]), indicator: "green" },
				5
			);
		},
	});
	dialog.show();
}

function load_team_members(dialog, frm, work_team) {
	const wrapper = dialog.fields_dict.members.$wrapper;
	if (!work_team) {
		wrapper.empty();
		dialog.selected_members = [];
		return;
	}

	// PM-TASK-00049: gửi kèm khoảng thời gian của lệnh để API tính luôn thời gian rảnh.
	// `exclude_work_order` là chính lệnh đang mở — không trừ phần lệnh này đang giữ chỗ thì
	// đội luôn trông như đã kín, trong khi người dùng đang cân nhắc thêm đội VÀO lệnh này.
	frappe.call({
		method: "mbwnext_hkled.api.work_team.get_team_members",
		args: {
			work_team: work_team,
			exclude: (frm.doc.custom_work_order_employee || [])
				.map((r) => r.employee)
				.filter(Boolean),
			start: frm.doc.custom_start_time || null,
			end: frm.doc.custom_required_completion_date__time || null,
			exclude_work_order: frm.doc.name,
		},
		callback(r) {
			const msg = r.message || {};
			const rows = msg.members || [];
			dialog.selected_members = rows.map((m) => ({ ...m, checked: !m.already_added }));
			dialog.free_time = msg.free_time || null;
			render_members(wrapper, dialog, frm);
		},
	});
}

function render_members(wrapper, dialog, frm) {
	const rows = dialog.selected_members || [];
	if (!rows.length) {
		wrapper.html(
			`<div class="text-muted small">${__(
				"Đội này chưa có nhân sự Công nhân nào đang làm việc."
			)}</div>`
		);
		return;
	}

	// PM-TASK-00049 — ô % thời gian rảnh của cả đội, đặt ngay dưới ô chọn đội đúng như ảnh mô tả.
	const ft = dialog.free_time;
	let khoi_pct = "";
	if (ft) {
		const mau = ft.free_percent >= 50 ? "green" : ft.free_percent >= 20 ? "orange" : "red";
		khoi_pct = `
			<div class="mb-3">
				<div style="font-size:22px;font-weight:700;line-height:1.2" class="text-${mau}">
					${ft.free_percent}%
				</div>
				<div class="text-muted small">
					${__("thời gian rảnh của cả đội")} —
					${__("rảnh {0} phút / tổng {1} phút", [
						format_number(ft.free_minutes, null, 0),
						format_number(ft.total_minutes, null, 0),
					])}
				</div>
			</div>`;
	} else {
		// Không có khoảng thời gian thì nói thẳng vì sao, đừng để ô trống cho người dùng đoán.
		khoi_pct = `<div class="mb-3 text-muted small">${__(
			"Điền Thời Gian Bắt Đầu và Thời Điểm Cần Hoàn Thành của lệnh để xem % thời gian rảnh của đội."
		)}</div>`;
	}

	const co_so_lieu = !!ft;
	const body = rows
		.map(
			(m, i) => `
			<tr class="${m.already_added ? "text-muted" : ""}">
				<td style="width:34px">
					<input type="checkbox" data-idx="${i}"
						${m.checked ? "checked" : ""} ${m.already_added ? "disabled" : ""}>
				</td>
				<td>${frappe.utils.escape_html(m.employee_name || m.employee)}</td>
				<td>${frappe.utils.escape_html(m.employee_level || "")}</td>
				<td class="text-right">${m.performance_factor || 0}</td>
				${
					co_so_lieu
						? `<td class="text-right">${format_number(m.free_minutes || 0, null, 0)}
							<span class="text-muted small">/ ${format_number(m.total_minutes || 0, null, 0)}</span></td>`
						: ""
				}
				<td class="small">${m.already_added ? __("đã có trong bảng") : ""}</td>
			</tr>`
		)
		.join("");

	wrapper.html(`
		${khoi_pct}
		<table class="table table-bordered" style="margin:0">
			<thead><tr>
				<th></th><th>${__("Nhân sự")}</th><th>${__("Bậc thợ")}</th>
				<th class="text-right">${__("Nguồn lực (%)")}</th>
				${co_so_lieu ? `<th class="text-right">${__("Rảnh (phút)")}</th>` : ""}
				<th></th>
			</tr></thead>
			<tbody>${body}</tbody>
		</table>`);

	wrapper.find("input[type=checkbox]").on("change", function () {
		const idx = Number($(this).attr("data-idx"));
		dialog.selected_members[idx].checked = this.checked;
	});
}
