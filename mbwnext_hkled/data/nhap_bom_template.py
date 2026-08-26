# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Dựng BOM Template + BOM Rule từ đặc tả `data/bom_template/spec.json` (PM-TASK-00110).

Đặc tả do `data/doc_bom_sheet.py` sinh ra từ file Excel khách gửi. Module này chỉ lo phần
chuyển đặc tả -> bản ghi, và **kiểm khớp cho từng biến thể thật trước khi ghi**.

## Ba cách viết trong file khách, và cách dựng tương ứng

| Trong sheet | Dựng thành |
|---|---|
| `Mọi biến thể đều chọn` | 1 rule *Theo Rule*, điều kiện = một đặc tính chung, **tích đủ mọi giá trị** |
| `tất cả` ở ô đặc tính | bỏ hẳn đặc tính đó khỏi điều kiện |
| `Còn lại` | **liệt kê thẳng** các tổ hợp giá trị mà rule phía trên chưa chiếm |
| `Không sử dụng` ở ô Mã NVL | không tạo rule |

Chốt của Thắng 18/08 trên PM-TASK-00110. Riêng `Mọi biến thể đều chọn`: em đề xuất dùng
*Cố Định* cho gọn, Thắng chọn *Theo Rule* vì còn cần chạy công thức số lượng ở Server
Script. Đổi lại phải chấp nhận **chi phí bảo trì**: rule liệt kê sẵn mọi giá trị nên khách
thêm một giá trị đặc tính mới (màu sơn mới, mức công suất mới) thì rule không tự phủ —
phải mở BOM Template tích thêm.

## Vì sao `Còn lại` phải liệt kê chứ không bỏ trống điều kiện

Hai chỗ chặn, cùng chiều nhau:

1. `BOMTemplate.resolve_rules` **cấm hai rule cùng thành phần phủ chung một biến thể** —
   nên không dựng được kiểu "rule cụ thể ở trên, rule vét ở dưới".
2. `find_rule_item` trong Server Script lọc `if cond and variant_matches(...)`: rule để
   trống điều kiện **không bao giờ khớp**.

Và phải liệt kê theo **tổ hợp nhiều đặc tính cùng lúc**, không theo từng đặc tính riêng.
Ví dụ DP01S/Module: rule trên chiếm (50W, Dọc) và (100W, Ngang). Xét riêng từng đặc tính
thì *Công suất* còn lại {150,200,…} và *Kiểu lắp* còn lại {} — ra tập rỗng, sai. Xét theo
cặp thì còn 14 cặp, gom lại thành 2 rule (một cho Dọc, một cho Ngang).
"""

import json
import os

import frappe

CON_LAI = "Còn lại"
KHONG_DUNG = "Không sử dụng"
SPEC = os.path.join(os.path.dirname(__file__), "bom_template", "spec.json")

# Biến thể mà khách CỐ Ý chưa khai NVL. Khai tường minh ở đây thay vì hạ ngưỡng kiểm:
# thiếu dữ liệu ngoài danh sách này vẫn phải chặn không cho ghi.
#
# DP01S 1200W/1500W — chốt của Thắng 18/08 trên PM-TASK-00110: *"linh kiện bộ vỏ, hộp
# carton tạm thời chưa đặt sản xuất, chưa có BOM chính xác nên bỏ trống đã"*. Khách bổ
# sung sau thì xoá mục này đi, bộ nạp sẽ tự đòi lại.
CHUA_CO_DU_LIEU = {
	"DP01S": {"Công suất": ("1200", "1500")},
	# DP03S là dòng vỏ đen, cấu trúc sheet y hệt DP01S và thiếu đúng cùng 4 thành phần ở
	# cùng hai mức công suất — cùng lý do khách chưa đặt sản xuất.
	"DP03S": {"Công suất": ("1200", "1500")},
}


def _doc_spec():
	with open(SPEC, encoding="utf-8") as f:
		spec = json.load(f)
	_canh_bao_theo_rule_lai(spec)
	return spec


def _canh_bao_theo_rule_lai(spec):
	"""Bắt kiểu đọc nhầm bảng khách: *"Theo rule"* của khách là SỐ LƯỢNG theo rule, không phải NVL.

	⚠ Đã vấp thật 26/08/2026. Bảng khách ghi thành phần `Ốc dây điện` như sau:

	    Ốc dây điện | Theo rule | OPG-M12-RM | SL | Kiểu đấu: Cầu đấu SL 0 | Kiểu đấu: Dây điện SL 1

	Chữ *"Theo rule"* ở cột kiểu là **số lượng theo rule** — NVL thì cố định, luôn là
	`OPG-M12-RM`. Nhưng `"Theo Rule"` trong hệ thống mình nghĩa **ngược lại**: NVL do rule
	quyết, ô NVL để trống. Bản trích spec ngày 24/08 dịch thẳng chữ sang chữ nên 4 sheet
	module mất NVL, không rule nào khớp, và **cả 4 BOM Template bị bỏ** — mà trên site không
	ai thấy vì bản spec đó chưa từng được nạp.

	Chữ ký của lỗi rất gọn, nên bắt được bằng máy: `kieu == "Theo Rule"` mà **`nvl` khác
	rỗng**. Mọi thành phần "Theo Rule" thật đều có `nvl` rỗng — đã kiểm cả 44 mục trong spec,
	chỉ đúng 4 mục hỏng có NVL. In cảnh báo chứ KHÔNG tự sửa: dịch sai ý khách là chuyện phải
	hỏi khách, không phải đoán.
	"""
	for ten, sheet in (spec.get("sheets") or {}).items():
		for t in sheet.get("thanh_phan") or []:
			if t.get("kieu") == "Theo Rule" and (t.get("nvl") or "").strip():
				print(
					f"[mbwnext_hkled] ⚠ SPEC NGHI ĐỌC NHẦM — {ten} · {t['thanh_phan']}: "
					f"kiểu 'Theo Rule' mà vẫn có NVL {t['nvl']!r}. Trong bảng khách "
					f"'Theo rule' thường là SỐ LƯỢNG theo rule, NVL thì cố định — "
					f"nếu đúng vậy thì kiểu phải là 'Cố Định'. Hỏi lại trước khi nạp."
				)


def _dac_tinh_bien_the(item_cha):
	"""{mã biến thể: {đặc tính: giá trị}}."""
	variants = frappe.get_all("Item", filters={"variant_of": item_cha}, pluck="name")
	if not variants:
		return {}
	ra = {v: {} for v in variants}
	for row in frappe.get_all(
		"Item Variant Attribute",
		filters={"parent": ["in", variants]},
		fields=["parent", "attribute", "attribute_value"],
	):
		ra[row.parent][row.attribute] = row.attribute_value
	return ra


def _khop(cond, attrs):
	for c in cond:
		if attrs.get(c["name"]) not in c["values"]:
			return False
	return True


def _gia_tri(v):
	"""Ô điều kiện có thể là một giá trị hoặc nhiều giá trị viết gộp bằng chữ "và"."""
	return list(v) if isinstance(v, list) else [v]


def _dac_tinh_chung(bien_the):
	"""Đặc tính mà MỌI biến thể đều khai, kèm toàn bộ giá trị đang dùng."""
	gia_tri, chung = {}, None
	for attrs in bien_the.values():
		for k, v in attrs.items():
			gia_tri.setdefault(k, set()).add(v)
		chung = set(attrs) if chung is None else (chung & set(attrs))
	return gia_tri, sorted(chung or [], key=lambda x: (len(gia_tri[x]), x))


def _giai_con_lai(rule, da_co, bien_the, gia_tri):
	"""Rule có `Còn lại` -> danh sách cond đã liệt kê tường minh.

	`da_co`: các cond của rule ĐỨNG TRƯỚC cùng thành phần. Tổ hợp nào rule trước đã chiếm
	thì rule này phải loại ra, nếu không `resolve_rules` chặn vì phủ trùng.
	"""
	cl = [k for k, v in rule["cond"].items() if v == CON_LAI]
	co_dinh = {k: v for k, v in rule["cond"].items() if v != CON_LAI}

	# Tổ hợp giá trị của các đặc tính "Còn lại", lấy trên biến thể THẬT (không nhân bừa
	# tích Descartes: nhiều tổ hợp không tồn tại, VD 50W chỉ có Dọc).
	to_hop = set()
	for attrs in bien_the.values():
		if any(attrs.get(k) not in _gia_tri(v) for k, v in co_dinh.items()):
			continue
		if any(k not in attrs for k in cl):
			continue
		to_hop.add(tuple(attrs[k] for k in cl))

	# Bỏ tổ hợp đã bị rule trước chiếm (rule trước cùng phần cố định).
	for cond in da_co:
		theo_ten = {c["name"]: c["values"] for c in cond}
		if any(set(theo_ten.get(k, [])) != set(_gia_tri(v)) for k, v in co_dinh.items()):
			continue
		to_hop = {
			t for t in to_hop
			if not all(t[i] in theo_ten.get(k, []) for i, k in enumerate(cl))
		}
	if not to_hop:
		return []

	# Gom cho gọn: chọn MỘT đặc tính để OR nhiều giá trị vào cùng một rule, các đặc tính
	# còn lại giữ nguyên từng giá trị. Chọn trục cho ra ít rule nhất — 14 rule "mỗi mức công
	# suất một dòng" và 2 rule "Dọc / Ngang" cùng phủ một tập biến thể, nhưng bản 2 dòng dễ
	# đọc và dễ sửa hơn hẳn khi khách mở BOM Template ra xem.
	def _gom(truc):
		nhom = {}
		for t in to_hop:
			khoa = tuple(v for i, v in enumerate(t) if i != truc)
			nhom.setdefault(khoa, []).append(t[truc])
		return nhom

	truc = min(range(len(cl)), key=lambda i: (len(_gom(i)), i))
	con_lai_ten = [k for i, k in enumerate(cl) if i != truc]
	ra = []
	for khoa, gia_tri_truc in sorted(_gom(truc).items()):
		cond = [{"name": k, "values": _gia_tri(v)} for k, v in co_dinh.items()]
		cond += [{"name": k, "values": [khoa[i]]} for i, k in enumerate(con_lai_ten)]
		cond.append({"name": cl[truc], "values": sorted(gia_tri_truc)})
		ra.append(cond)
	return ra


def dung_rules(spec_sheet, bien_the):
	"""Đặc tả 1 sheet -> danh sách rule sẵn sàng ghi. Trả `(rules, ghi_chu)`."""
	gia_tri, chung = _dac_tinh_chung(bien_the)
	rules, ghi_chu, bo_qua = [], [], []
	da_co = {}  # thành phần -> các cond đã phát sinh, để giải "Còn lại"

	for r in spec_sheet["rules"]:
		tp = r["thanh_phan"]
		# `Không sử dụng` giờ thành RULE TƯỜNG MINH có tích ô, không còn bỏ trắng.
		# Bỏ trắng chính là chỗ sinh ra lỗ hổng phủ: engine không phân biệt được "khách khai
		# không dùng" với "quên chưa đặt rule" nên throw ở cả hai. Vẫn ghi vào `bo_qua` để
		# `kiem_khop` phân loại được cặp nào là cố ý.
		khong_dung = r["nvl"] == KHONG_DUNG
		if khong_dung:
			bo_qua.append({"tp": tp, "cond": r["cond"]})

		if r["moi_bien_the"]:
			if not chung:
				ghi_chu.append({"loai": "không có đặc tính chung nào", "tp": tp})
				continue
			dt = chung[0]
			conds = [[{"name": dt, "values": sorted(gia_tri[dt])}]]
		elif CON_LAI in r["cond"].values():
			conds = _giai_con_lai(r, da_co.get(tp, []), bien_the, gia_tri)
			if not conds:
				ghi_chu.append({"loai": "'Còn lại' không còn tổ hợp nào", "tp": tp, "nvl": r["nvl"]})
				continue
		else:
			cond = [{"name": k, "values": _gia_tri(v)} for k, v in r["cond"].items()]
			if not cond:
				ghi_chu.append({"loai": "rule rỗng điều kiện (không bao giờ khớp)", "tp": tp,
					"nvl": r["nvl"]})
				continue
			conds = [cond]

		for cond in conds:
			rules.append({
				"bom_component": tp,
				"item": None if khong_dung else r["nvl"],
				"khong_su_dung": 1 if khong_dung else 0,
				"cond_attrs": cond,
			})
			da_co.setdefault(tp, []).append(cond)
	return rules, ghi_chu, bo_qua


def kiem_khop(ten_sheet, spec_sheet, rules, bien_the, bo_qua):
	"""Mô phỏng khớp cho TỪNG biến thể × TỪNG thành phần Theo Rule.

	Chạy TRƯỚC khi ghi. Engine `find_rule_item` throw khi không rule nào khớp, nên một cặp
	không khớp = một BOM không tạo được.

	Xếp cặp không khớp vào ba nhóm, chỉ nhóm cuối mới chặn việc ghi:

	- `co_y` — trùng một tổ hợp khách ghi "Không sử dụng". ⚠ Từ 21/08 nhóm này PHẢI BẰNG 0:
	  các tổ hợp đó giờ có rule tường minh tích "Không Sử Dụng" nên vẫn khớp, chỉ là khớp ra
	  một rule bảo bỏ dòng. Còn cặp nào rơi vào đây nghĩa là rule chưa sinh đủ.
	- `chua_co_du_lieu` — nằm trong `CHUA_CO_DU_LIEU`, khách chưa khai và đã xác nhận.
	- `hong` — còn lại. Thiếu ngoài dự kiến, chặn ghi.
	"""
	theo_rule = [t["thanh_phan"] for t in spec_sheet["thanh_phan"] if t["kieu"] == "Theo Rule"]
	mien = CHUA_CO_DU_LIEU.get(ten_sheet) or {}
	hong, co_y, chua = [], [], []
	for ma, attrs in bien_the.items():
		trong_mien = mien and all(attrs.get(k) in v for k, v in mien.items())
		for tp in theo_rule:
			if any(r["bom_component"] == tp and _khop(r["cond_attrs"], attrs) for r in rules):
				continue
			cap = {"bien_the": ma, "thanh_phan": tp}
			if any(b["tp"] == tp and all(attrs.get(k) in _gia_tri(v) for k, v in b["cond"].items()
					if v != CON_LAI) for b in bo_qua):
				co_y.append(cap)
			elif trong_mien:
				chua.append(cap)
			else:
				hong.append(cap)
	return hong, co_y, chua


def _bao_dam_component(ten):
	if frappe.db.exists("BOM Component", ten):
		return False
	frappe.get_doc({"doctype": "BOM Component", "component_name": ten}).insert(
		ignore_permissions=True
	)
	return True


# Vài dòng còn nguyên nhãn cột thay vì số — coi như khách chưa khai số lượng.
NHAN_CHUA_KHAI = ("", "Ghi chú", "SL")


def _so_luong(sl_tho):
	"""Ô SL trong sheet -> `(số lượng, lý do cần báo)`.

	Ba trường hợp: số thuần dùng luôn; ô còn nguyên nhãn cột = chưa khai; còn lại là câu mô
	tả số lượng đổi theo đặc tính — mô hình hiện tại chưa đỡ được, phải báo chứ không nuốt.
	"""
	if (sl_tho or "").strip() in NHAN_CHUA_KHAI:
		return None, "chưa khai số lượng"
	try:
		return int(float(sl_tho)), None
	except (TypeError, ValueError):
		return None, "số lượng đổi theo đặc tính"


def nhap_mot_sheet(ten_sheet, spec_sheet, chi_kiem=False):
	item_cha = spec_sheet["item_cha"]
	bien_the = _dac_tinh_bien_the(item_cha)
	if not bien_the:
		return {"sheet": ten_sheet, "loi": f"Mặt hàng cha {item_cha} chưa có biến thể nào"}

	rules, ghi_chu, bo_qua = dung_rules(spec_sheet, bien_the)
	hong, co_y, chua = kiem_khop(ten_sheet, spec_sheet, rules, bien_the, bo_qua)
	bao = {
		"sheet": ten_sheet, "item_cha": item_cha, "so_bien_the": len(bien_the),
		"so_rule": len(rules), "so_cap_hong": len(hong), "cap_hong": hong[:10],
		"so_cap_co_y": len(co_y), "so_cap_chua_co_du_lieu": len(chua),
		"ghi_chu": ghi_chu, "sl_thieu": [],
	}
	if hong or chi_kiem:
		bao["da_ghi"] = False
		return bao

	ten_tp = set()
	for t in spec_sheet["thanh_phan"]:
		ten_tp.add(t["thanh_phan"])
	for r in rules:
		ten_tp.add(r["bom_component"])
	bao["component_moi"] = sorted(t for t in sorted(ten_tp) if _bao_dam_component(t))

	code = f"BOM Template {ten_sheet}"
	cu = frappe.db.get_value("BOM Template", {"item_template": item_cha})
	doc = frappe.get_doc("BOM Template", cu) if cu else frappe.new_doc("BOM Template")
	doc.bom_template_code = doc.bom_template_code or code
	doc.item_template = item_cha
	doc.is_active = 1
	doc.set("bom_component_table", [])
	doc.set("bom_rules", [])

	for t in spec_sheet["thanh_phan"]:
		sl, ly_do = _so_luong(t["sl_tho"])
		kieu = t["kieu"]
		if sl is None:
			bao["sl_thieu"].append({
				"tp": t["thanh_phan"], "ly_do": ly_do, "ghi_trong_sheet": t["sl_tho"],
			})
			# Khách khai "Cố Định" nhưng số lượng lại ĐỔI theo đặc tính (vd Ốc dây điện:
			# "Kiểu đấu: Cầu đấu SL 0 | Kiểu đấu: Dây điện SL 1") — hai thứ mâu thuẫn.
			# "Cố Định" lấy thẳng ô Số Lượng, mà ô đó không điền được số nào đúng cho cả
			# hai trường hợp; để nguyên là dòng bị bỏ khỏi BOM một cách âm thầm.
			# Nâng lên "Số Lượng Theo Công Thức" để Server Script tính, NVL vẫn lấy từ ô
			# khách khai. Ghi lại để người đọc báo cáo biết bộ nạp đã đổi kiểu.
			if kieu == "Cố Định":
				kieu = "Số Lượng Theo Công Thức"
				bao.setdefault("doi_kieu", []).append({
					"tp": t["thanh_phan"], "tu": "Cố Định", "sang": kieu,
					"vi": ly_do,
				})
		doc.append("bom_component_table", {
			"bom_component": t["thanh_phan"],
			"component_type": kieu,
			# Khách để trống ô SL thì ghi 0, KHÔNG ghi 1. Ghi 1 thì engine coi như số lượng
			# hợp lệ, dùng thẳng vào BOM và cảnh báo "chưa khai số lượng" không bao giờ bắn
			# (nó chỉ bắn khi qty <= 0). Xốp góc đã lọt lưới đúng kiểu đó: dự phòng 1 trong
			# khi bảng khách ghi 4, suốt từ lúc nạp không có gì báo.
			"qty": sl if sl is not None else 0,
			"item": t["nvl"] if t["kieu"] != "Theo Rule" else None,
		})
	for r in rules:
		doc.append("bom_rules", {
			"bom_component": r["bom_component"],
			"item": r["item"],
			"khong_su_dung": r.get("khong_su_dung", 0),
			"cond_attrs": json.dumps(r["cond_attrs"], ensure_ascii=False),
		})

	doc.save(ignore_permissions=True)
	bao["da_ghi"] = True
	bao["ten"] = doc.name
	return bao


DIEM_LUU_SHEET = "nhap_bom_template_sheet"


def nhap_tat_ca(chi_kiem=False):
	spec = _doc_spec()
	bao = {"bo_qua_sheet": spec.get("loi", {}), "sheets": []}
	for ten, s in spec["sheets"].items():
		# Một sheet hỏng KHÔNG được giết cả lượt nạp.
		#
		# ⚠ Vì sao cần: `BOM Template` là Link tới Item, nên NVL nào chưa có trên site là
		# `LinkValidationError` ném thẳng ra ngoài. Trên site đã chạy thì không bao giờ xảy ra
		# — mọi mặt hàng đã có sẵn. Trên SITE MỚI thì có: đo ngày 25/08/2026 trên `test.com`,
		# sheet DP01S tra tới 8 mã module bị bỏ vì thiếu Nhóm sản phẩm, cộng `W-3x0.75-BK` và
		# `XOP-GOC-110x110x120mm` vốn chỉ được tạo tay trên `hkled.com` chứ không nằm trong
		# file CSV nào. Lỗi này bay ra sau 2 giờ 22 phút nạp danh mục và bỏ lại site cài dở.
		#
		# Bỏ qua sheet hỏng rồi báo tên NVL còn thiếu thì lượt cài chạy hết, và người đọc log
		# biết chính xác phải bổ sung cái gì. KHÔNG tự tạo mặt hàng thiếu — xem
		# "THÀ BỎ QUA CÒN HƠN ĐOÁN" trong `nhap_item.py`.
		frappe.db.savepoint(DIEM_LUU_SHEET)
		try:
			bao["sheets"].append(nhap_mot_sheet(ten, s, chi_kiem=chi_kiem))
		except frappe.exceptions.LinkValidationError as e:
			frappe.db.rollback(save_point=DIEM_LUU_SHEET)
			frappe.local.message_log = []
			bao["sheets"].append({"sheet": ten, "loi": f"thiếu mặt hàng được tra tới — {e}"})
	return bao
