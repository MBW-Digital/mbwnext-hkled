// PM-TASK-00143 — Trưởng phòng chỉ chọn được Đội Sản Xuất thuộc phòng ban của lệnh.
//
// 🔒 Anh Thắng 03/09 14:57: "cho Đội Sản Xuất gắn phòng ban để trưởng phòng chỉ chọn được đội
// của phòng mình". Đây là phần lọc ở MÀN HÌNH cho tiện tay; chặn thật nằm ở server
// (work_order_phong_ban.validate_team_in_department) vì API và nhập hàng loạt đi vòng qua được.
//
// File riêng, không sửa controllers/js/work_order.js — file đó thuộc cửa sổ giữ Phần II–III.

frappe.ui.form.on("Work Order", {
	setup(frm) {
		frm.set_query("custom_work_team", function (doc) {
			// Lệnh chưa khai phòng ban thì KHÔNG lọc — hiện hết đội. Lọc theo một ô trống sẽ ra
			// danh sách rỗng và người dùng không hiểu vì sao; site hiện chưa dòng kế hoạch nào
			// khai phòng ban nên đây là trạng thái thường gặp, không phải ngoại lệ hiếm.
			if (!doc.custom_department) {
				return {};
			}
			// Đội chưa gắn phòng ban vẫn phải chọn được — dữ liệu cũ, cả 2 đội trên site đang
			// như vậy (đo 07/09). Cùng luật với ba ca cho qua ở validate phía server.
			//
			// 🔴 KHÔNG dùng `filters: [[..., "in", [phong, ""]]]` — bản đầu tôi viết thế và nó
			//    SAI: cột này ở bản ghi cũ là `NULL`, mà SQL thì `NULL` không khớp `IN` bất kể
			//    danh sách có gì. Đo 07/09: bộ lọc đó khớp 0/2 đội, tức ô này rỗng trắng ngay
			//    khi lệnh có Phòng Ban. Phải đi qua truy vấn riêng có `ifnull` ở server.
			return {
				query:
					"mbwnext_hkled.controllers.python_hook.work_order_phong_ban.doi_theo_phong_ban",
				filters: { phong_ban: doc.custom_department },
			};
		});
	},

	custom_department(frm) {
		// Đổi phòng ban mà giữ nguyên đội cũ thì lệnh mang một đội của phòng khác — server sẽ
		// chặn lúc Lưu. Xoá sẵn ở đây để người dùng thấy ngay, thay vì đụng lỗi sau khi bấm Lưu.
		if (!frm.doc.custom_work_team || !frm.doc.custom_department) {
			return;
		}
		frappe.db
			.get_value("Work Team", frm.doc.custom_work_team, "custom_department")
			.then((r) => {
				const phong_cua_doi = (r.message || {}).custom_department;
				if (phong_cua_doi && phong_cua_doi !== frm.doc.custom_department) {
					frm.set_value("custom_work_team", null);
					frappe.show_alert({
						message: __("Đã bỏ chọn đội cũ vì đội đó không thuộc phòng ban vừa chọn"),
						indicator: "orange",
					});
				}
			});
	},
});
