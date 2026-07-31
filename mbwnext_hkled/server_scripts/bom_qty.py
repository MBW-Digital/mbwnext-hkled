# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Nguồn của Server Script `hkled_resolve_bom_qty` (mục 3 tài liệu thiết kế BOM Template HKLED).

QUAN TRỌNG — vì sao công thức nằm ở Server Script chứ không phải code app:
công thức số lượng NVL là quyết định nghiệp vụ thay đổi thường xuyên, HKLED cần sửa được
**ngay lập tức, không build/deploy lại app**. Sửa Server Script bấm Save là chạy ngay.

File này chỉ là **bản gốc để cài lần đầu** (qua patch `create_bom_qty_server_script`) và để
review/diff trong git. Sau khi cài, **nguồn chạy thật là document Server Script trên site** —
patch cố tình KHÔNG ghi đè script đã tồn tại, để không xoá mất chỉnh sửa của người dùng.

Giới hạn sandbox phải tuân thủ khi sửa: không `import`, không tên hàm bắt đầu bằng `_`,
chỉ dùng `frappe.utils.*` / `frappe.get_all` / `frappe.db.*` / `frappe.throw`.
"""

SCRIPT_NAME = "hkled_resolve_bom_qty"

SCRIPT = '''
# ==================================================================
# HELPER FUNCTIONS
# ==================================================================

def classify_nguon(nguon):
	"""Phân loại giá trị đặc tính "Nguồn" thành 3 nhóm dùng chung nhiều công thức."""
	nhom_to_hkled = ("HKLED Dim 1 Cấp", "HKLED Dim 5 Cấp")
	nhom_to_khac = ("Done Dim 1 Cấp", "Philips Dim 1 Cấp", "Philips Dim 10 Cấp",
		"Meanwell Dim 1 Cấp", "Inventronics Dim 5 Cấp")
	if nguon in nhom_to_hkled:
		return "to_hkled"
	if nguon in nhom_to_khac:
		return "to_khac"
	return "nho"

def resolve_modulo_priority(power, divisors, fallback):
	"""Ưu tiên chia hết từ trên xuống. VD [300,250,200]:
	power=600 chia hết cả 300 và 200 -> ưu tiên 300 -> 600/300=2"""
	for d in divisors:
		if power % d == 0:
			return power / d
	return fallback

def round_qty(value):
	return frappe.utils.ceil(value)  # TODO: xác nhận quy tắc làm tròn với HKLED

def get_variant_attrs(variant_code):
	rows = frappe.get_all("Item Variant Attribute",
		filters={"parent": variant_code},
		fields=["attribute", "attribute_value"])
	result = {}
	for r in rows:
		result[r.attribute] = r.attribute_value
	return result

# ==================================================================
# NHÓM 1 & 2: MODULE-BASED (Đèn pha P01-P03, Đèn đường D01-D05)
# ==================================================================

def calc_module_qty(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	return 1 if power <= 50 else power / 50

def calc_oc_vit_module_qty(attrs, rule_group):
	return calc_module_qty(attrs, rule_group) * 2

def nguon_to_p01_p03(power, mount, cat):
	if mount == "Dọc":
		if cat == "to_hkled":
			return 1
		return 1 if power <= 250 else 2
	else:  # Ngang
		if cat == "to_hkled":
			return 1 if power <= 100 else 2
		if power <= 100:
			return 1
		if power <= 500:
			return 2
		return resolve_modulo_priority(power, [250, 200, 150], 2)

def calc_nguon_qty_module_group(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	mount = attrs.get("Kiểu lắp")
	cat = classify_nguon(attrs.get("Nguồn"))

	if cat == "nho":
		return 1 if power <= 50 else power / 50

	if rule_group == "P01_P03":
		return nguon_to_p01_p03(power, mount, cat)
	if rule_group == "D01_D05":
		# Không phân biệt Kiểu lắp, không có Ngang/Dọc
		return 1 if power <= 250 else 2

	frappe.throw(f"Chưa cấu hình công thức Nguồn cho nhóm {rule_group}")

def calc_cau_dau_qty(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	mount = attrs.get("Kiểu lắp")
	cat = classify_nguon(attrs.get("Nguồn"))

	if rule_group == "P01_P03":
		if power <= 50:
			return 0
		if mount == "Dọc":
			return 1 if (cat == "to_hkled" or power <= 250) else 2
		else:  # Ngang
			if cat == "to_hkled":
				return 0 if power <= 100 else 2
			if power <= 100:
				return 0
			if power <= 500:
				return 2
			return resolve_modulo_priority(power, [250, 200, 150], 2)

	if rule_group == "D01_D05":
		if power <= 50:
			return 0
		return 1 if (cat == "to_hkled" or power <= 250) else 2

	frappe.throw(f"Chưa cấu hình công thức Cầu đấu cho nhóm {rule_group}")

def calc_day_dien_cap_nguon_qty(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	mount = attrs.get("Kiểu lắp")

	flat_table = {"D01_D05": 70, "PTX": 50, "XHB": 50, "DQL": 70, "D11_D15": 70}
	if rule_group in flat_table:
		return flat_table[rule_group]

	if rule_group == "P01_P03":
		if mount == "Dọc":
			if power <= 50:
				return 0
			return 50 if power <= 250 else 100
		else:  # Ngang
			if power <= 100:
				return 0
			if power <= 500:
				return 100
			if power <= 600:
				return 100  # KHOẢNG TRỐNG DỮ LIỆU 500-600, chờ HKLED xác nhận
			if power <= 1000:
				return 200
			return 300

	frappe.throw(f"Chưa cấu hình công thức Dây điện cấp nguồn cho nhóm {rule_group}")

# ==================================================================
# NHÓM 3, 4, 5: CHIP LED-BASED, chia sẻ chung công thức Nguồn/Chip
# (Đèn pha PTX, Highbay XHB, Đèn đường DQL)
# ==================================================================

def calc_chip_led_qty(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	if rule_group == "D11_D15":
		return power / 50  # nhóm này không có ngưỡng, luôn chia
	return 1 if power < 100 else power / 50

def calc_oc_vit_bat_chip_qty(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	if rule_group == "D11_D15":
		return (power / 50) * 8
	return 4 if power < 100 else (power / 50) * 4

def nguon_to_ptx_xhb_dql(power, cat):
	"""Công thức Nguồn to dùng chung cho PTX / XHB / DQL"""
	if cat == "to_hkled":
		return resolve_modulo_priority(power, [300, 250, 200], 1)
	return resolve_modulo_priority(power, [250, 200, 150], 1)

def calc_nguon_qty_chip_group(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	cat = classify_nguon(attrs.get("Nguồn"))

	if rule_group == "D11_D15":
		if cat == "nho":
			return power / 50
		if cat == "to_hkled":
			return 1  # Nguồn HKLED Dim 1/5 Cấp: luôn = 1, không có ngưỡng công suất
		return 1 if power <= 250 else 2  # Done/Philips/Meanwell/Inventronics

	# PTX / XHB / DQL dùng chung
	if cat == "nho":
		return 1 if power < 100 else power / 50
	return nguon_to_ptx_xhb_dql(power, cat)

def calc_day_dien_dau_chip_qty(attrs, rule_group):
	"""Dùng chung cho cả Đỏ và Đen — 2 màu công thức giống hệt nhau"""
	power = frappe.utils.flt(attrs.get("Công suất"))
	cat = classify_nguon(attrs.get("Nguồn"))

	if rule_group == "PTX":
		if cat == "nho":
			return 0
		return (power / 50) * 20 if power < 200 else (power / 50) * 25

	if rule_group == "XHB":
		return (power / 50) * 30

	if rule_group == "DQL":
		return 0 if power < 100 else (power / 50) * 20

	if rule_group == "D11_D15":
		# BẢNG TRA RỜI RẠC, không phải công thức liên tục
		lookup = {50: 0, 100: 50, 150: 90, 200: 140, 250: 200, 300: 270}
		if power in lookup:
			return lookup[power]
		frappe.throw(
			f"Công suất {power} chưa có trong bảng tra Dây điện đấu chip nhóm D11_D15")

	frappe.throw(f"Chưa cấu hình công thức Dây điện đấu chip cho nhóm {rule_group}")

# ==================================================================
# NHÓM 6: D11-D15 — có thêm Lens, Gioăng chip, Ốc vít bắt lens
# ==================================================================

def calc_lens_qty(attrs, rule_group):
	return frappe.utils.flt(attrs.get("Công suất")) / 50

def calc_gioang_chip_qty(attrs, rule_group):
	return frappe.utils.flt(attrs.get("Công suất")) / 50

def calc_oc_vit_bat_lens_qty(attrs, rule_group):
	return (frappe.utils.flt(attrs.get("Công suất")) / 50) * 16

# ==================================================================
# DISPATCH TABLE + ENTRY POINT
# ==================================================================

COMPONENT_MAP = {
	"Module": calc_module_qty,
	"Ốc vít cố định module": calc_oc_vit_module_qty,
	"Cầu đấu": calc_cau_dau_qty,
	"Dây điện cấp nguồn": calc_day_dien_cap_nguon_qty,
	"Chip LED": calc_chip_led_qty,
	"Ốc vít bắt chip": calc_oc_vit_bat_chip_qty,
	"Dây điện đấu chip - Đỏ": calc_day_dien_dau_chip_qty,
	"Dây điện đấu chip - Đen": calc_day_dien_dau_chip_qty,
	"Lens": calc_lens_qty,
	"Gioăng chip": calc_gioang_chip_qty,
	"Ốc vít bắt lens": calc_oc_vit_bat_lens_qty,
}

MODULE_GROUPS = ("P01_P03", "D01_D05")
CHIP_GROUPS = ("PTX", "XHB", "DQL", "D11_D15")

item_code = frappe.form_dict.get("item_code")
component_name = frappe.form_dict.get("component_name")
rule_group = frappe.form_dict.get("rule_group")
bom_template_name = frappe.form_dict.get("bom_template")  # cần khi component = Nguồn

if not (item_code and component_name and rule_group):
	frappe.throw("Thiếu tham số item_code / component_name / rule_group")

attrs = get_variant_attrs(item_code)

# Chặn tính sai âm thầm: thiếu đặc tính Công suất thì mọi công thức đều ra số vô nghĩa.
if not attrs.get("Công suất"):
	frappe.throw(
		f"Mặt hàng {item_code} chưa khai báo đặc tính Công suất"
		f" — không thể tính số lượng {component_name}")

power_value = frappe.utils.flt(attrs.get("Công suất"))

# Nhóm P01_P03 phân biệt Dọc/Ngang từ mốc trên 50W. Thiếu Kiểu lắp ở mức này là lỗi dữ liệu.
if rule_group == "P01_P03" and power_value > 50 and not attrs.get("Kiểu lắp"):
	frappe.throw(
		f"Mặt hàng {item_code} ({power_value}W) chưa khai báo đặc tính Kiểu lắp"
		f" — nhóm P01_P03 cần Dọc/Ngang")

result = {}

if component_name == "Nguồn":
	nguon = attrs.get("Nguồn")
	rule_row = frappe.get_all("BOM Rule",
		filters={"parent": bom_template_name, "bom_component": "Nguồn",
			"condition_value": nguon},
		fields=["item"], limit=1)
	if not rule_row:
		frappe.throw(f"Chưa thiết lập NVL cho Nguồn: {nguon}")
	result["item"] = rule_row[0].item

	if rule_group in MODULE_GROUPS:
		qty = calc_nguon_qty_module_group(attrs, rule_group)
	elif rule_group in CHIP_GROUPS:
		qty = calc_nguon_qty_chip_group(attrs, rule_group)
	else:
		frappe.throw(f"rule_group không hợp lệ: {rule_group}")
else:
	fn = COMPONENT_MAP.get(component_name)
	if not fn:
		frappe.throw(f"Chưa có công thức cho thành phần: {component_name}")
	qty = fn(attrs, rule_group)

result["qty"] = round_qty(qty)

# Trả kết quả qua frappe.flags — dùng được cho CẢ 2 đường gọi:
#   HTTP  /api/method/hkled_resolve_bom_qty  (handler trả flags khi flags khác {})
#   Python frappe.utils.safe_exec.run_script("hkled_resolve_bom_qty", ...)
# Không dùng frappe.response: biến này không luôn có trong sandbox (background job, console).
frappe.flags.result = result
'''
