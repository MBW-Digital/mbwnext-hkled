# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class OtherTaskTable(Document):
	# Frappe không gọi validate() của child DocType — ràng buộc nằm ở other_task.py.
	pass
