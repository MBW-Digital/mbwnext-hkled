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

def classify_nguon(attrs):
	"""Phân loại nguồn thành 3 nhóm: "nho" / "to_hkled" / "to_khac".

	HAI TRỤC, lấy từ hai đặc tính khác nhau — đừng gộp:

	1. nhỏ hay to  -> đặc tính **"Kiểu nguồn"** trên chính biến thể. Site có sẵn đúng ba
	   giá trị bảng khách dùng: "Nguồn nhỏ" / "Nguồn to điện áp thấp" / "Nguồn to điện áp
	   cao", và có ở 55 mặt hàng cha.
	2. trong nhóm to: HKLED hay hãng khác -> đặc tính **"Nguồn"** (tên hãng), vì bảng khách
	   tách hai nhánh này theo đúng tên hãng.

	⚠ Bản cũ suy trục 1 từ danh sách tên hãng, và sai thật: "Năng lượng mặt trời" có
	Kiểu nguồn = "Nguồn to điện áp thấp" nhưng không nằm trong danh sách nào nên rơi vào
	"nho" — 512 biến thể mỗi template DP01S/DP03S tính sai Nguồn, Cầu đấu và Dây điện.
	Danh sách tên hãng cũng hỏng lặng mỗi lần khách thêm hãng mới.
	"""
	nhom_to_hkled = ("HKLED Dim 1 Cấp", "HKLED Dim 5 Cấp")
	nhom_to_khac = ("Done Dim 1 Cấp", "Philips Dim 1 Cấp", "Philips Dim 10 Cấp",
		"Meanwell Dim 1 Cấp", "Inventronics Dim 5 Cấp")
	nguon = attrs.get("Nguồn")
	kieu = (attrs.get("Kiểu nguồn") or "").strip()

	if kieu:
		if kieu == "Nguồn nhỏ":
			return "nho"
		# Còn lại là "Nguồn to điện áp thấp" / "Nguồn to điện áp cao" — bảng khách gộp
		# chung, chỉ tách tiếp theo tên hãng.
		# ⚠ Hãng không nằm trong danh sách nào (vd "Năng lượng mặt trời") rơi vào to_khac.
		# Bảng khách KHÔNG nói hãng đó thuộc nhánh nào — đã hỏi Thắng 22/08.
		return "to_hkled" if nguon in nhom_to_hkled else "to_khac"

	# Biến thể chưa khai "Kiểu nguồn": giữ nguyên cách suy cũ để không chặn giữa chừng.
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

def variant_matches(cond_attrs, variant_attrs):
	"""AND giữa các thuộc tính, OR trong values (spec §7.1)."""
	for cond in cond_attrs:
		if variant_attrs.get(cond.get("name")) not in (cond.get("values") or []):
			return False
	return True

def find_rule_item(bom_template, component_name, variant_attrs):
	"""Tra rule cho thành phần "Theo Rule" bằng cond_attrs (spec §8).

	Rule nằm ở bảng `bom_rules` của BOM Template, phân biệt theo `bom_component`
	(phương án B, spec §5 — phương án A không dựng được vì Frappe không hỗ trợ bảng con
	lồng 2 cấp).

	Trả về CẢ DÒNG rule chứ không chỉ mã NVL, vì rule tích "Không Sử Dụng" có ô NVL trống
	mà vẫn là một kết quả khớp hợp lệ — trả None thì người gọi không phân biệt được
	"khách khai không dùng" với "quên chưa đặt rule", hai thứ phải xử lý ngược nhau.
	Trả None chỉ khi thật sự không rule nào khớp.
	"""
	rules = frappe.get_all("BOM Rule",
		filters={"parent": bom_template, "parenttype": "BOM Template",
			"bom_component": component_name},
		fields=["item", "cond_attrs", "khong_su_dung"], order_by="idx")
	for r in rules:
		# Sandbox Server Script không có frappe.parse_json, chỉ có json.loads (safe_exec.py:187).
		cond = json.loads(r.cond_attrs) if r.cond_attrs else []
		if cond and variant_matches(cond, variant_attrs):
			return r
	return None

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
	"""Bảng khách gửi 22/08 (Google Sheet "công thức hoàn chỉnh", nhóm đèn pha P01-P03).

	Hai nhánh Ngang đều có bước ƯU TIÊN CHIA HẾT sau ngưỡng, và thứ tự ưu tiên của
	hai nhánh KHÁC NHAU — nguồn HKLED là 300/250/200, nguồn khác là 250/150/200.
	Đừng gộp lại cho gọn: đổi thứ tự là ra số khác (1200W: 250/150/200 -> 8, còn
	250/200/150 -> 6).
	"""
	if mount == "Dọc":
		if cat == "to_hkled":
			return 1
		return 1 if power <= 250 else 2
	else:  # Ngang
		if cat == "to_hkled":
			if power <= 100:
				return 1
			if power <= 600:
				return 2
			return resolve_modulo_priority(power, [300, 250, 200], 2)
		if power <= 100:
			return 1
		if power <= 500:
			return 2
		return resolve_modulo_priority(power, [250, 150, 200], 2)

def calc_nguon_qty_module_group(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	mount = attrs.get("Kiểu lắp")
	cat = classify_nguon(attrs)

	if cat == "nho":
		return 1 if power <= 50 else power / 50

	if rule_group == "P01_P03":
		return nguon_to_p01_p03(power, mount, cat)
	if rule_group == "D01_D05":
		# Không phân biệt Kiểu lắp, không có Ngang/Dọc.
		# Nguồn HKLED luôn 1 bất kể công suất (bảng khách 22/08) — bản cũ bỏ sót vế này.
		if cat == "to_hkled":
			return 1
		return 1 if power <= 250 else 2

	frappe.throw(f"Chưa cấu hình công thức Nguồn cho nhóm {rule_group}")

def calc_cau_dau_qty(attrs, rule_group):
	power = frappe.utils.flt(attrs.get("Công suất"))
	mount = attrs.get("Kiểu lắp")
	cat = classify_nguon(attrs)

	if rule_group == "P01_P03":
		if power <= 50:
			return 0
		if mount == "Dọc":
			return 1 if (cat == "to_hkled" or power <= 250) else 2
		else:  # Ngang
			# Cùng cấu trúc với Nguồn ở trên, chỉ khác ngưỡng đầu trả 0 thay vì 1.
			if cat == "to_hkled":
				if power <= 100:
					return 0
				if power <= 600:
					return 2
				return resolve_modulo_priority(power, [300, 250, 200], 2)
			if power <= 100:
				return 0
			if power <= 500:
				return 2
			# ⚠ Bảng khách KHÔNG có nhánh cho nguồn nhỏ ở Cầu đấu, chỉ liệt kê 2 nhóm
			# nguồn to. Nguồn nhỏ đang đi chung đường này (giữ nguyên hành vi cũ) —
			# trên site có biến thể nguồn nhỏ ở 600W/1200W. Đã hỏi Thắng 22/08.
			return resolve_modulo_priority(power, [250, 150, 200], 2)

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
		# Bảng khách 22/08: cả cây Dọc/Ngang bên dưới chỉ áp cho NGUỒN NHỎ (ô gộp
		# C37:C43); "Nguồn to điện áp thấp" và "Nguồn to điện áp cao" đều = 0 — đèn
		# dùng nguồn to thì dây đi kèm nguồn, không tính vào BOM đèn.
		# Bản cũ bỏ qua điều kiện này nên cấp thừa dây cho 98/160 tổ hợp.
		if classify_nguon(attrs) != "nho":
			return 0
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
	cat = classify_nguon(attrs)

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
	cat = classify_nguon(attrs)

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

# Ba thành phần dưới đây là SỐ CỐ ĐỊNH theo nhóm, không phải công thức — nhưng vẫn để
# ở đây chứ không để ô Số Lượng trên dòng thành phần. Lý do: file khách để TRỐNG ô SL,
# bộ nạp phải điền một giá trị dự phòng, và giá trị đó đi thẳng vào BOM mà không ai báo.
# Xốp góc đã sai như vậy suốt (dự phòng 1, đúng ra là 4). Khai ở đây thì sai lệch so với
# bảng khách lộ ra ngay, và mỗi nhóm khai một số riêng.
def calc_bo_vo_den_qty(attrs, rule_group):
	if rule_group in ("P01_P03", "D01_D05"):
		return 1
	frappe.throw(f"Chưa có số lượng Bộ vỏ đèn cho nhóm {rule_group}")

def calc_hop_carton_qty(attrs, rule_group):
	if rule_group in ("P01_P03", "D01_D05"):
		return 1
	frappe.throw(f"Chưa có số lượng Hộp carton cho nhóm {rule_group}")

def calc_xop_goc_qty(attrs, rule_group):
	# Đèn pha dùng "Xốp góc" 4 miếng; đèn đường dùng thành phần tên khác ("Xốp chèn", 2).
	if rule_group == "P01_P03":
		return 4
	frappe.throw(f"Chưa có số lượng Xốp góc cho nhóm {rule_group}")

def calc_xop_chen_qty(attrs, rule_group):
	if rule_group == "D01_D05":
		return 2
	frappe.throw(f"Chưa có số lượng Xốp chèn cho nhóm {rule_group}")

COMPONENT_MAP = {
	"Bộ vỏ đèn": calc_bo_vo_den_qty,
	"Hộp carton": calc_hop_carton_qty,
	"Xốp góc": calc_xop_goc_qty,
	"Xốp chèn": calc_xop_chen_qty,
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

# ------------------------------------------------------------------
# KHOÁ TRA CÔNG THỨC = MẶT HÀNG CHA (chốt của TungDA 07/08 trên PM-FEAT-00007)
#
# Trước đây khoá là field `rule_group` người dùng phải tự chọn trên BOM Template.
# Field đó đã bỏ; giờ script tự suy bộ công thức từ chính Mặt Hàng Cha (Item có
# biến thể) của BOM Template.
#
# Hai lớp tra, ưu tiên lớp 1:
#   1. FORMULA_GROUP_BY_TEMPLATE — khai đích danh từng mã. HKLED sửa TRỰC TIẾP ở đây
#      khi có mặt hàng mới hoặc mặt hàng không theo quy tắc prefix. Sửa Server Script
#      bấm Save là chạy ngay, không cần deploy app.
#   2. PREFIX_GROUPS — suy theo tiền tố mã, phủ các dòng sản phẩm đặt mã theo quy ước.
#
# Không suy được thì THROW nêu đích danh mã, tuyệt đối không đoán bộ công thức:
# đoán sai thì BOM ra sai số lượng mà không ai biết.
# ------------------------------------------------------------------

FORMULA_GROUP_BY_TEMPLATE = {
	# "DX01S": "XHB",   ← mẫu: bỏ comment và khai khi HKLED chốt công thức cho mã đó
}

PREFIX_GROUPS = (
	(("DP01", "DP02", "DP03"), "P01_P03"),
	(("DD11", "DD12", "DD13", "DD14", "DD15"), "D11_D15"),
	(("DD01", "DD02", "DD03", "DD04", "DD05"), "D01_D05"),
	(("DPTC", "DPTR", "DPXH", "DPTV", "DPVL", "DPKD"), "PTX"),
	(("DXHB",), "XHB"),
	(("DDQL",), "DQL"),
)

def resolve_formula_group(item_template):
	"""Suy bộ công thức từ Mặt Hàng Cha. None nếu chưa khai báo."""
	if item_template in FORMULA_GROUP_BY_TEMPLATE:
		return FORMULA_GROUP_BY_TEMPLATE[item_template]
	for prefixes, group in PREFIX_GROUPS:
		if item_template.startswith(prefixes):
			return group
	return None

item_code = frappe.form_dict.get("item_code")
component_name = frappe.form_dict.get("component_name")
item_template = frappe.form_dict.get("item_template")
bom_template_name = frappe.form_dict.get("bom_template")  # cần khi component = Nguồn

if not (item_code and component_name and item_template):
	frappe.throw("Thiếu tham số item_code / component_name / item_template")

rule_group = resolve_formula_group(item_template)
if not rule_group:
	frappe.throw(
		f"Mặt hàng cha {item_template} chưa có bộ công thức số lượng."
		f" Khai thêm vào FORMULA_GROUP_BY_TEMPLATE trong Server Script"
		f" hkled_resolve_bom_qty, hoặc xác nhận với HKLED công thức áp dụng cho mã này.")

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

component_type = frappe.db.get_value("BOM Component Table",
	{"parent": bom_template_name, "bom_component": component_name}, "component_type")

# "Theo Rule" -> NVL do rule quyết định. Áp dụng cho MỌI thành phần Theo Rule chứ không
# riêng "Nguồn" như bản cũ (spec §8). Số lượng vẫn do COMPONENT_MAP tính như thường.
if component_type == "Theo Rule":
	matched = find_rule_item(bom_template_name, component_name, attrs)
	if not matched:
		frappe.throw(
			f"Chưa thiết lập NVL cho thành phần {component_name} với biến thể {item_code}."
			f" Thêm rule phủ biến thể này trong BOM Template {bom_template_name}.")

	# Khách khai "Không sử dụng" cho tổ hợp này -> số lượng 0, và BỎ QUA khối tính bên dưới.
	# `resolve_components` đã có sẵn nhánh bỏ dòng khi qty <= 0 nên dòng tự rụng khỏi BOM.
	# Phải chặn TRƯỚC khối tính số lượng: chạy tiếp thì công thức của thành phần đó vẫn ra
	# số dương và dòng lại chui vào BOM.
	# Thân Server Script chạy ở CẤP MODULE, không phải trong hàm — không dùng `return` được
	# (SyntaxError), nên thoát sớm bằng cờ.
	khong_dung = 1 if matched.khong_su_dung else 0
	if not khong_dung:
		result["item"] = matched.item
else:
	khong_dung = 0

if khong_dung:
	qty = 0
	result["khong_su_dung"] = 1
elif component_name == "Nguồn":
	if rule_group in MODULE_GROUPS:
		qty = calc_nguon_qty_module_group(attrs, rule_group)
	elif rule_group in CHIP_GROUPS:
		qty = calc_nguon_qty_chip_group(attrs, rule_group)
	else:
		frappe.throw(
			f"Bộ công thức {rule_group} (suy từ mặt hàng cha {item_template})"
			f" chưa được xếp vào MODULE_GROUPS hay CHIP_GROUPS")
else:
	fn = COMPONENT_MAP.get(component_name)
	if fn:
		qty = fn(attrs, rule_group)
	elif component_type == "Theo Rule":
		# Thành phần Theo Rule chỉ đổi NVL theo biến thể, số lượng không theo công thức
		# (VD Bộ vỏ đèn). Lấy số lượng khai ngay trên dòng thành phần.
		qty = frappe.utils.flt(frappe.db.get_value("BOM Component Table",
			{"parent": bom_template_name, "bom_component": component_name}, "qty"))
		if qty <= 0:
			# Chưa khai Số Lượng thì tạm tính 1 để người dùng không bị chặn giữa chừng,
			# NHƯNG đánh dấu lại để báo lên giao diện. Không im lặng: số lượng đoán mà
			# không ai biết thì BOM sai âm thầm.
			qty = 1
			result["qty_defaulted"] = 1
	else:
		frappe.throw(f"Chưa có công thức cho thành phần: {component_name}")

result["qty"] = round_qty(qty)

# Trả kết quả qua frappe.flags — dùng được cho CẢ 2 đường gọi:
#   HTTP  /api/method/hkled_resolve_bom_qty  (handler trả flags khi flags khác {})
#   Python frappe.utils.safe_exec.run_script("hkled_resolve_bom_qty", ...)
# Không dùng frappe.response: biến này không luôn có trong sandbox (background job, console).
frappe.flags.result = result
'''
