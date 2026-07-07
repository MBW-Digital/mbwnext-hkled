app_name = "mbwnext_hkled"
app_title = "MBWNext HKLed"
app_publisher = "MBWD"
app_description = "MBWNext HKLed"
app_email = "tuanbui@mbw.vn"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

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
	"BOM Template": "public/js/bom_template.js",
	"Production Plan": "public/js/production_plan.js",
	"Employee": "public/js/employee.js",
	"Work Order": "public/js/work_order.js",
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
	}
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
		"on_update": "mbwnext_hkled.controllers.python_hook.work_order.sync_employee_allocation_on_finish",
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

