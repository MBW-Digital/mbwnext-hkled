# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Nạp dữ liệu danh mục ban đầu cho Phần I — BOM Template theo biến thể.

- 6 Nhóm Công Thức (`BOM Rule Group`) — mục 2.1 tài liệu thiết kế.
- Danh mục `BOM Component` khớp CHÍNH XÁC tên khoá trong COMPONENT_MAP của Server Script
  `hkled_resolve_bom_qty`: sai một dấu là engine không tra được công thức.

Idempotent: chỉ tạo bản ghi còn thiếu, không sửa/ghi đè bản ghi người dùng đã có.
"""

import frappe

RULE_GROUPS = [
	("P01_P03", "Đèn LED pha P01/P02/P03 SMD+COB"),
	("D01_D05", "Đèn LED đường D01-D05"),
	("PTX", "Đèn LED pha PTC/PTR/PXH/PTV/PVL/PKD"),
	("XHB", "Đèn LED nhà xưởng highbay"),
	("DQL", "Đèn LED đường DQL"),
	("D11_D15", "Đèn LED đường D11-D15"),
]

# Thành phần có công thức số lượng (COMPONENT_MAP trong Server Script)
FORMULA_COMPONENTS = [
	"Module",
	"Ốc vít cố định module",
	"Cầu đấu",
	"Dây điện cấp nguồn",
	"Chip LED",
	"Ốc vít bắt chip",
	"Dây điện đấu chip - Đỏ",
	"Dây điện đấu chip - Đen",
	"Lens",
	"Gioăng chip",
	"Ốc vít bắt lens",
]

# Thành phần chọn NVL theo BOM Rule
RULE_COMPONENTS = ["Nguồn"]

# Thành phần nhập tay cố định (ví dụ trong tài liệu thiết kế, mục 2.3)
FIXED_COMPONENTS = ["Bộ vỏ đèn", "Hộp carton", "Xốp góc"]


def execute():
	# Từ 07/08 KHÔNG seed `BOM Rule Group` nữa: field `rule_group` trên BOM Template đã bỏ
	# (chốt của TungDA trên PM-FEAT-00007), khoá tra công thức là Mặt Hàng Cha và bảng suy
	# nhóm nằm trong Server Script `hkled_resolve_bom_qty`.
	# RULE_GROUPS giữ lại chỉ để tra cứu tên 6 bộ công thức khi đọc Server Script.
	# Site đã chạy patch này trước đó vẫn còn 6 bản ghi cũ — vô hại vì không còn ai tham chiếu.

	for name in FORMULA_COMPONENTS + RULE_COMPONENTS + FIXED_COMPONENTS:
		if frappe.db.exists("BOM Component", name):
			continue
		frappe.get_doc({"doctype": "BOM Component", "component_name": name}).insert(
			ignore_permissions=True
		)
