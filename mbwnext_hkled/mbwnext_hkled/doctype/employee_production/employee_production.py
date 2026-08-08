# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class EmployeeProduction(Document):
	# Không đặt validate() ở đây: Frappe KHÔNG gọi validate() của child DocType.
	# Ràng buộc tổng sản lượng nằm ở controllers/python_hook/work_order.py.
	pass
