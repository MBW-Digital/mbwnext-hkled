app_name = "mbwnext_hkled"
app_title = "MBWNext HKLed"
app_publisher = "MBWD"
app_description = "MBWNext HKLed"
app_email = "tuanbui@mbw.vn"
app_license = "mit"

# Apps
# ------------------

# ☢️ ĐỌC DÒNG NÀY TRƯỚC KHI GÕ `bench install-app mbwnext_hkled`.
#
# Khai `required_apps` biến lệnh cài app này thành một lệnh CÓ THỂ XOÁ DỮ LIỆU. Trên site
# THIẾU `mbwnext_localization`, Frappe tự cài nó trước, và `after_install` của nó chạy
# `del_masterdataCore()` = `frappe.db.sql("DELETE FROM tab<doctype>")` — SQL thẳng, không
# kiểm liên kết, không hỏi — cho `Item Group`, `UOM`, `UOM Conversion`, `Territory`,
# `Stock Entry Type`, `Province`, `Commune`.
#
# Site trắng: đó đúng là việc cần làm. Site ĐANG CÓ DỮ LIỆU: mất sạch phân nhóm danh mục.
# Đã dính thật trên `test.com` ngày 26/08/2026 — Item Group 50 → 8, và 61.835/61.836 mặt
# hàng trỏ vào nhóm không còn tồn tại. (Mặt hàng thì còn: `tabItem.item_group` giữ nguyên
# chuỗi tên, dựng lại bản ghi nhóm là liên kết tự nối.)
#
# ➜ TRƯỚC KHI CÀI LÊN SITE THẬT: `bench --site <site> list-apps | grep localization`.
#   Đã có thì an toàn. Chưa có mà site đã có dữ liệu thì DỪNG, hỏi trước.
#
# ⚠ KHÔNG CHẶN ĐƯỢC TỪ APP NÀY — nhưng KHÔNG PHẢI "không đâu chặn được".
# Ghi rõ để người đọc sau khỏi tìm nhầm chỗ, hoặc ngừng tìm quá sớm.
#
# Chỗ xoá dữ liệu nằm ở LƯỢT GỌI TRONG: `install_app("mbwnext_hkled")` đệ quy sang
# `install_app("mbwnext_localization")` tại dòng 287. Phải đọc thứ tự của lượt TRONG đó:
#
#     310  before_app_install       ← điểm chặn DUY NHẤT chạy trước lúc xoá
#     325  after_install của localization -> del_masterdataCore() -> DELETE FROM
#
# `before_install` (305) và `before_app_install` (310) của lượt trong đều thuộc về
# localization / các app đã cài, không phải app này. Còn ở lượt NGOÀI thì hook sớm nhất của
# `mbwnext_hkled` là 305 — mãi sau 287, tức sau khi đã xoá xong. Nên từ app này: không kịp.
#
# ⚠ `before_app_install` CHẶN ĐƯỢC THẬT — ĐÃ ĐO, KHÔNG PHẢI SUY. Nhưng KHÔNG khai được từ
# chính app này. `frappe.get_hooks("before_app_install")` gom hook từ `get_installed_apps()`
# (`frappe/__init__.py::_load_app_hooks` — không truyền `app_name` thì lấy danh sách app ĐÃ
# CÀI). Lúc lượt trong chạy ở dòng 287, `mbwnext_hkled` chưa qua `add_to_installed_apps()`
# (mãi dòng 318 của lượt ngoài), nên hook của chính nó không bao giờ bắn. Phải là **một app
# khác đã nằm sẵn trên site** đứng ra khai.
#
# Đo ngày 26/08/2026 trên `test.com`: dựng một app rỗng khai
# `before_app_install`, cài nó trước, gỡ localization, rồi `bench install-app mbwnext_hkled`.
# Kết quả: hook BẮN với `app='mbwnext_localization'`, throw, `RC=1`, và
# **Item Group giữ nguyên 101 (không tụt về 8), Item 61.836, UOM 37** — chặn đúng trước
# `del_masterdataCore()`, không mất dòng nào.
#
# ➜ Nghĩa là nếu không sửa được app lõi thì vẫn còn đường: cho một app lõi ĐANG CÓ SẴN trên
# mọi site khách ôm hook này. Điểm yếu: đúng cảnh nguy hiểm nhất — site mới tinh chỉ có
# erpnext — thì chưa app nào ôm.
#
# ➜ Rào đúng chỗ nhất vẫn là chính `del_masterdataCore()` bên `mbwnext_localization`: nó là
# nơi duy nhất biết chắc site có dữ liệu hay không, ngay trước khi xoá. App lõi, phải xin
# phép mới sửa. Chừng nào chưa sửa được ở đó thì dòng cảnh báo phía trên là lớp bảo vệ duy
# nhất đang thực sự tồn tại — đừng xoá nó đi cho gọn.

# ── Vì sao đúng hai app này, không hơn không kém ──
#
# Trước 26/08/2026 chỗ này để trống và thứ tự cài chỉ nằm trong docstring `install.py` — tức
# người ta chỉ đọc SAU KHI đã cài sai. Khai ở đây thì Frappe tự cài đúng thứ tự, không ai gõ
# sai được nữa.
#
# · `mbwnext_localization`    — lý do ở khối trên: nó xoá `Item Group`/`UOM`. Cài SAU app này
#   là xoá mất phân nhóm của danh mục vừa nạp.
# · `mbwnext_advanced_selling` — thêm Custom Field cho `Item` (`setup/custom_fields.json`).
#   Cài sau khi `after_sync` đã nạp 62.054 mặt hàng thì các cột đó rỗng toàn bộ.
#
# Bốn app lõi còn lại (buying, stock, accounting, distribution_map) KHÔNG chạm `Item` và
# không xoá gì, nên cố ý không khai — khai thừa chỉ làm lệnh cài dài ra và khó gỡ khi lỗi.
#
# ⚠ PHẢI CÓ TIỀN TỐ TỔ CHỨC, và phần sau dấu `/` PHẢI LÀ TÊN APP (gạch dưới), không phải tên
# repo GitHub (`mbwnext-localization`, gạch ngang). Chuỗi không có `/` thì `parse_app_name()`
# đi hỏi GitHub rồi 404 → `InvalidRemoteException`; ghi đúng tên repo thì hỏng ở "App not in
# apps.txt". Đây không phải đường clone — `mbwnext_advanced_buying/hooks.py` đã hỏng vì đúng
# lý do này.
#
# 📌 Tác dụng phụ có lợi, Frappe tự có: khai dòng này thì `bench uninstall-app` TỪ CHỐI gỡ hai
# app trên chừng nào `mbwnext_hkled` còn cài ("... is a dependency of ...", installer.py:383).
required_apps = [
	"MBW-Digital/mbwnext_localization",
	"MBW-Digital/mbwnext_advanced_selling",
]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "mbwnext_hkled",
# 		"logo": "/assets/mbwnext_hkled/logo.png",
# 		"title": "MBWNext HKLed",
# 		"route": "/mbwnext_hkled",
# 		"has_permission": "mbwnext_hkled.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mbwnext_hkled/css/mbwnext_hkled.css"
# app_include_js = "/assets/mbwnext_hkled/js/mbwnext_hkled.js"

# include js, css files in header of web template
# web_include_css = "/assets/mbwnext_hkled/css/mbwnext_hkled.css"
# web_include_js = "/assets/mbwnext_hkled/js/mbwnext_hkled.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mbwnext_hkled/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"BOM": "controllers/js/bom.js",
	"BOM Template": "controllers/js/bom_template.js",
	"Production Plan": "controllers/js/production_plan.js",
	"Sales Order": "controllers/js/sales_order.js",
	"Employee": "controllers/js/employee.js",
	"Work Order": "controllers/js/work_order.js",
	"Other Task": "controllers/js/other_task.js",
}

# GAP-2: nút "Tạo Nhanh" nằm trên DANH SÁCH Lịch Làm Việc, không phải trên form.
doctype_list_js = {
	"Employee Schedule": "controllers/js/employee_schedule_list.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mbwnext_hkled/public/icons.svg"

# Fixtures
# --------

fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [["module", "=", "MBWNext HKLed"]],
	},
	# PM-TASK-00054: mã chứng từ riêng của HKLED (SO-26-…, LSX-26-… ) nằm ở Property Setter.
	# Đưa vào fixtures để cài lại site mới là có ngay, không phải nhớ chạy patch bằng tay.
	# ⚠ Hệ quả: thêm series mới bằng giao diện sẽ bị ghi đè ở lần `bench migrate` kế tiếp —
	# muốn thêm thì sửa `patches/set_document_naming_series.py` rồi export-fixtures lại.
	{
		"doctype": "Property Setter",
		"filters": [["module", "=", "MBWNext HKLed"]],
	},
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mbwnext_hkled.utils.jinja_methods",
# 	"filters": "mbwnext_hkled.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mbwnext_hkled.install.before_install"
# after_install = "mbwnext_hkled.install.after_install"

# ⚠ `after_sync`, KHÔNG PHẢI `after_install`: hook này chạy sau khi fixtures đã vào
# (`installer.py` gọi `sync_fixtures` giữa hai hook), và chỉ chạy lúc CÀI app.
# Nó dựng toàn bộ phần dữ liệu mà `patches.txt` không dựng được trên site mới —
# lý do đầy đủ nằm trong docstring của `mbwnext_hkled/install.py`, đọc trước khi sửa.
after_sync = ["mbwnext_hkled.install.after_sync"]

# Uninstallation
# ------------

# before_uninstall = "mbwnext_hkled.uninstall.before_uninstall"
# after_uninstall = "mbwnext_hkled.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mbwnext_hkled.utils.before_app_install"
# after_app_install = "mbwnext_hkled.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mbwnext_hkled.utils.before_app_uninstall"
# after_app_uninstall = "mbwnext_hkled.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mbwnext_hkled.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Work Order": {
		# KHÔNG dùng "on_update": Work Order không có method đó, và status chuyển sang
		# "Completed" bằng db_set trong WorkOrder.update_status() nên không hook nào chạy.
		# "update_status" được Stock Entry gọi qua run_method() -> doc_events có compose.
		# Xem giải thích đầy đủ trong controllers/python_hook/work_order.py.
		"update_status": [
			"mbwnext_hkled.controllers.python_hook.work_order.sync_employee_allocation_on_finish",
			"mbwnext_hkled.controllers.python_hook.work_order.split_employee_production_on_finish",
		],
		# GAP-5: thừa hưởng thời gian + đội từ Kế Hoạch Sản Xuất khi WO được tạo.
		# PM-TASK-00045: lệnh tạo bằng Sửa đổi/Nhân bản không được mang link Phân Công của lệnh cũ
		# (no_copy KHÔNG chặn được đường Sửa đổi — xem clear_copied_allocation_record).
		# ensure_start_time phải chạy SAU inherit_from_production_plan: hàm kia lấy giờ từ Kế Hoạch,
		# hàm này chỉ lấp chỗ trống còn lại. Đảo thứ tự là luôn lấy giá trị dự phòng.
		"before_insert": [
			"mbwnext_hkled.controllers.python_hook.work_order.clear_copied_allocation_record",
			"mbwnext_hkled.controllers.python_hook.work_order.inherit_from_production_plan",
			"mbwnext_hkled.controllers.python_hook.work_order.set_sales_info",
			"mbwnext_hkled.controllers.python_hook.work_order.ensure_start_time",
		],
		# GAP-7 (C12): tổng Sản Lượng Nhân Viên phải khớp Số Lượng Đã Sản Xuất.
		# Phải khai CẢ HAI: document đã submit thì Frappe không gọi `validate` nữa,
		# mà C12 lại cho sửa tay sau khi Finish.
		# PM-TASK-00050: Khách Hàng + Nhân Viên Bán Hàng lấy từ Đơn Bán Hàng của lệnh.
		"validate": [
			"mbwnext_hkled.controllers.python_hook.work_order.validate_employee_production",
			"mbwnext_hkled.controllers.python_hook.work_order.set_sales_info",
		],
		"before_update_after_submit": (
			"mbwnext_hkled.controllers.python_hook.work_order.validate_employee_production"
		),
		# PM-TASK-00045 (C6): huỷ/xoá lệnh thì dọn Phân Công, nếu không nhân sự bị giữ chỗ
		# vĩnh viễn và engine tính lịch trả về thời điểm bắt đầu muộn hơn thực tế.
		"on_cancel": "mbwnext_hkled.controllers.python_hook.work_order.cleanup_employee_allocation",
		"on_trash": "mbwnext_hkled.controllers.python_hook.work_order.cleanup_employee_allocation",
	},
	"Production Plan": {
		# GAP-4: Thời Điểm Cần Hoàn Thành phải ghép delivery_date + custom_time nên không fetch_from được.
		# PM-TASK-00046: Ghi Chú Sản Xuất cho từng dòng bảng Assembly Items.
		"validate": [
			"mbwnext_hkled.controllers.python_hook.production_plan.set_required_completion_time",
			"mbwnext_hkled.controllers.python_hook.production_plan.set_item_production_note",
		],
	},
	"Sales Order": {
		# PM-TASK-00046: Ghi Chú Sản Xuất của đơn chảy xuống dòng hàng còn trống. Phải có ở server
		# vì client script không chạy khi tạo đơn bằng API / Data Import.
		# PM-FEAT-00023: Số Lượng Giữ Chỗ không được vượt tồn khả dụng. Cùng lý do trên, và nặng
		# hơn: con số này bị TRỪ khỏi tồn khả dụng của mọi đơn khác, sai một dòng là sai cả site.
		"validate": [
			"mbwnext_hkled.controllers.python_hook.sales_order.fill_item_production_note",
			"mbwnext_hkled.controllers.python_hook.sales_order.chan_giu_cho_vuot_ton",
			# PM-FEAT-00036: sổ cam kết vật tư. Phải đứng SAU `chan_giu_cho_vuot_ton` — nó cấp
			# phát dựa trên số ghim thành phẩm, cấp phát trước khi số đó được kiểm là cấp theo
			# con số có thể bị chặn ngay sau đó.
			"mbwnext_hkled.controllers.python_hook.sales_order.dong_bo_ghim_vat_tu",
		],
		# 🔴 PM-FEAT-00036: từ 04/09 hai ô ghim mở khoá sau khi duyệt (anh Thắng chốt 15:59).
		# Frappe **không chạy `validate`** trên đường update-after-submit, nên không treo lại ở
		# đây thì lớp chặn giữ-chỗ-vượt-tồn thủng đúng ngay lúc vừa mở khoá.
		"before_update_after_submit": [
			"mbwnext_hkled.controllers.python_hook.sales_order.chan_giu_cho_vuot_ton",
			"mbwnext_hkled.controllers.python_hook.sales_order.dong_bo_ghim_vat_tu",
		],
	},
	"Stock Entry": {
		# GAP-7: sinh serial theo mã đơn bán khi Finish, thay cho series mặc định.
		# PM-FEAT-00034: chặn xuất quá tồn khả dụng — xem khối 8 chứng từ ngay dưới.
		"before_submit": [
			"mbwnext_hkled.controllers.python_hook.stock_entry.set_serial_no_on_manufacture",
			"mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
		],
	},
	# ══ PM-FEAT-00034 · Chặn xuất kho quá tồn khả dụng ══
	#
	# ĐỦ 8 CHỨNG TỪ có thể làm giảm tồn (đầu bài §1.1). Bản đầu của đầu bài định hook 3 cái ➜
	# thủng 6, và kiểu thủng đó chỉ lộ ra SAU KHI kho đã xuất lọt. Thêm chứng từ mới vào lõi
	# thì phải thêm vào đây; `chan_xuat_kho` THROW nếu bị gọi cho chứng từ chưa có bộ đọc, cố ý
	# ồn ào thay vì lặng lẽ cho qua.
	#
	# `Stock Entry` đã khai ở khối trên vì nó còn hook khác — đừng khai lại thành hai chỗ.
	"Delivery Note": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	"Sales Invoice": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	"Purchase Receipt": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	"Purchase Invoice": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	"Stock Reconciliation": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	"Subcontracting Receipt": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	"Asset Capitalization": {
		"before_submit": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.chan_xuat_qua_ton_kha_dung",
	},
	# Yêu Cầu Mặt Hàng KHÔNG sinh Stock Ledger Entry ➜ chỉ CẢNH BÁO, không chặn (đầu bài §4).
	"Material Request": {
		"validate": "mbwnext_hkled.controllers.python_hook.chan_xuat_kho.canh_bao_yeu_cau_mat_hang",
	},
	"Employee": {
		# C1: `mandatory_depends_on` của Frappe CHỈ chạy phía client — lưu bằng script/API
		# vẫn lọt. Phải chặn thêm ở server. Xem controllers/python_hook/employee.py.
		"validate": "mbwnext_hkled.controllers.python_hook.employee.validate_employee_level",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mbwnext_hkled.tasks.all"
# 	],
# 	"daily": [
# 		"mbwnext_hkled.tasks.daily"
# 	],
# 	"hourly": [
# 		"mbwnext_hkled.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mbwnext_hkled.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mbwnext_hkled.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "mbwnext_hkled.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mbwnext_hkled.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mbwnext_hkled.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mbwnext_hkled.utils.before_request"]
# after_request = ["mbwnext_hkled.utils.after_request"]

# Job Events
# ----------
# before_job = ["mbwnext_hkled.utils.before_job"]
# after_job = ["mbwnext_hkled.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mbwnext_hkled.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

