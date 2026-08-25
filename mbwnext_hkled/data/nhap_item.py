# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Bộ nạp danh mục vật tư HKLED từ file CSV (PM-TASK-00061).

Nguồn: Google Sheet đính trong PM-TASK-00061 — 11 sheet, mỗi sheet một loại vật tư, chép nguyên xi
thành `mbwnext_hkled/data/danh_muc/*.csv`. Mọi sheet dùng chung khuôn:

    Mã sản phẩm | Tên sản phẩm | Nhóm sản phẩm | Mã biến thể | Tên biến thể | [Mô tả] | <các đặc tính…>

Mọi cột ngoài 6 cột trên đều được coi là **đặc tính biến thể** (Item Attribute). Danh sách đặc tính
của từng mặt hàng cha suy ra từ chính dữ liệu: cột nào có giá trị ở ít nhất một biến thể thì cột đó
là đặc tính của cha ấy.

## Nguyên tắc: THÀ BỎ QUA CÒN HƠN ĐOÁN

Bảng nguồn có lỗi thật (trùng mã, thiếu ô, mã ghép hụt). Bộ nạp này **không tự chế mã, không tự
điền ô trống, không tự chọn giữa hai dòng mâu thuẫn**. Dòng nào không xử lý được thì bỏ qua và ghi
vào báo cáo để hỏi khách. Đoán một cái mã sai rồi để nó chạy vào chứng từ thật thì gỡ rất đắt.

Ba nhóm bị bỏ qua, xem `bao_cao["bo_qua"]`:

1. **Trùng mã biến thể, nội dung khác nhau** — cùng một mã gán cho hai sản phẩm khác nhau.
   Ví dụ thật: `CM30S050-6P3-5C` có hai dòng, một dòng 64 LED một dòng 50 LED — mã không mã hoá số
   LED nên hai sản phẩm đâm nhau. Không có cách nào chọn hộ khách.
2. **Mã biến thể để trống**.
3. **Mã ghép hụt** — ví dụ `-BN` ở sheet Vỏ đèn: công thức trong bảng tính mất phần đầu, còn mỗi
   hậu tố, 3 dòng khác công suất dùng chung một "mã".

Trùng mã mà **nội dung giống hệt** thì không phải lỗi — chỉ là dòng lặp, giữ dòng đầu.

## Những chỗ đã vấp

**`standard_rate` là trường BẮT BUỘC của Item trên bench này**, nằm thẳng trong
`erpnext/stock/doctype/item/item.json` (không phải Property Setter nên grep mãi không ra). Ràng buộc
chỉ chặn khi trường **để trống** — `0` vẫn qua, vì `_get_missing_mandatory_fields()` so bằng
`cstr(value).strip()`. Nên đặt `standard_rate = 0`, **không** dùng `ignore_mandatory`: làm vậy là đẻ
ra bản ghi mở lên không lưu lại được, đúng bẫy đã gặp với `custom_start_time` trên Lệnh sản xuất.

**Biến thể KHÔNG bắt buộc có đủ đặc tính của mặt hàng cha.** Bản đầu của file này bỏ qua 5 mặt hàng
cha vì tin ngược lại. Thử nghiệm trên chính site (mặt hàng cha 3 đặc tính, biến thể khai 2) cho thấy
tạo được bình thường; khai đủ dòng nhưng để trống giá trị thì ERPNext **tự bỏ dòng đó**, cũng không
báo lỗi. Thứ nó thật sự chặn là hai biến thể **đụng cùng một tổ hợp giá trị** — `ItemVariantExistsError`.
Đừng suy ra ràng buộc từ trực giác, chạy thử là biết.

**Cây Nhóm Sản Phẩm của site này phẳng hoàn toàn** — 60 nhóm đều `parent_item_group = NULL` và không
có gốc `All Item Groups`. Nhóm mới cũng tạo phẳng cho khớp.

**Hai cột đặc tính trong bảng trùng nghĩa với đặc tính đã có trên site, chỉ khác tên** — xem
`DOI_TEN_DAC_TINH`. Đối chiếu giá trị thấy trùng khít nên ánh xạ chứ không tạo đặc tính mới.
"""

import csv
import os
import re

import frappe

# Cột không phải đặc tính biến thể.
COT_CO_DINH = {
	"Mã sản phẩm",
	"Tên sản phẩm",
	"Nhóm sản phẩm",
	"Mã biến thể",
	"Biến thể",
	"Tên biến thể",
	"Mô tả",
	# Đây là TRƯỜNG của Item, không phải đặc tính biến thể — đổ vào Custom Field
	# `custom_replenishment_method` ở `cap_nhat_phuong_phap()`, không tạo Item Attribute.
	# ⚠ Thiếu dòng này là bộ nạp coi nó như một đặc tính rồi dừng ở
	# "Chưa có Item Attribute 'Phương pháp bổ sung' trên site" — vỡ luôn `bench migrate`
	# trên site cài mới. Đã vấp khi nạp sheet Lens (PM-TASK-00108).
	"Phương pháp bổ sung",
	# PM-TASK-00126: 16 file danh mục đợt 2 dùng thêm mấy tên cột này.
	# ⚠ "Đơn vị tính" là TRƯỜNG `stock_uom` của Item, KHÔNG phải đặc tính biến thể. Thiếu dòng này
	# là bộ nạp dừng ở "Chưa có Item Attribute 'Đơn vị tính' trên site" — đã vấp thật khi nạp đợt 2.
	"Đơn vị tính",
	# Hai cột dưới là cách file (SLP) và sheet "(M) Module (1)" gọi mã/tên biến thể — xem
	# `_khoa_bien_the` và `_khoa_ten_bien_the`.
	"Mã đặc tính",
	"Tên đặc tính",
}

COT_DON_VI = "Đơn vị tính"

# Cột trong bảng -> Item Attribute đã có trên site.
# Không tạo đặc tính mới: đã đối chiếu giá trị và thấy trùng khít 100%.
#   Dimming              = {Không, Dim 1 Cấp, Dim 5 Cấp, Dim 10 Cấp} = Khả năng điều chỉnh công suất
#   Tương thích chip LED = {5C, 40C, 5C / 7C / 8C}                   = Phù hợp với chip LED
DOI_TEN_DAC_TINH = {
	"Dimming": "Khả năng điều chỉnh công suất",
	"Tương thích chip LED": "Phù hợp với chip LED",
}

# Chuẩn hoá giá trị viết khác kiểu về đúng giá trị site đang dùng.
# `Công suất` trên site là SỐ TRẦN (`1`, `2`, `5`, `30`…), phần "W" nằm ở `abbr`. Riêng sheet LED
# ghi `1W/2W/5W`; 10 sheet còn lại đều số trần. Không chuẩn hoá là site có cả `1` lẫn `1W` cho cùng
# một công suất, lọc báo cáo sẽ sót.
# ⚠ Chỉ đưa vào đây thứ CHẮC CHẮN là cùng một giá trị. `Loại LED` có `3030` (PCB không kén hãng)
# khác hẳn `Lumileds 3030` — đó là giá trị mới thật, không phải viết khác kiểu.
CHUAN_HOA_GIA_TRI = {}

# Đặc tính mà giá trị trong bảng có kèm đơn vị, còn trên site lưu SỐ TRẦN (đơn vị nằm ở `abbr`).
# ⚠ Bản cũ chỉ liệt kê tay {"1W": "1", "2W": "2", "5W": "5"} vì 12 file đợt 1 hầu hết ghi số trần.
# 16 file đợt 2 (PM-TASK-00126) ghi **toàn bộ** kèm "W" — nạp thẳng là site có cả `200` (59.959 item
# cũ) lẫn `200W` (589 item mới) cho cùng một công suất, lọc báo cáo theo công suất sẽ **sót một
# nửa mà không báo gì**. Đúng cái đã ghi trong CLAUDE.md. Cắt hậu tố cho mọi giá trị dạng số + đơn vị.
CAT_DON_VI = {"Công suất": "W"}


def gia_tri_so_tran(dac_tinh_bang, gia_tri):
	"""Cắt hậu tố đơn vị nếu phần còn lại là số. `200W` -> `200`; `Điện áp cao` giữ nguyên."""
	hau_to = CAT_DON_VI.get(dac_tinh_bang)
	if not hau_to or not gia_tri:
		return gia_tri
	v = gia_tri.strip()
	if v.upper().endswith(hau_to.upper()):
		than = v[: -len(hau_to)].strip()
		if re.fullmatch(r"[\d.]+", than):
			return than
	return v

# Nhãn bị bỏ lại trơ trọi khi đặc tính tương ứng để trống — chỉ gặp ở sheet Ốc/vít/bulong,
# nơi tên được ghép theo khuôn "<tên hàng>, Ren <x>, Đầu <y>, Khe <z>, <chất liệu>".
NHAN_TRONG = ("Ren", "Đầu", "Khe")

DON_VI = "Cái"

# PM-TASK-00067: cột khách thêm vào cả 11 sheet, đổ vào Custom Field cùng nghĩa trên Item.
COT_PHUONG_PHAP = "Phương pháp bổ sung"
TRUONG_PHUONG_PHAP = "custom_replenishment_method"

# Nguồn của *Phương pháp bổ sung* nằm ở HAI chỗ:
#   data/danh_muc/     — vật tư, linh kiện (bảng của PM-TASK-00061, khách thêm cột vào đó)
#   data/thanh_pham/   — đèn thành phẩm (4 file "Nhóm I…IV" trong thư mục Drive của PM-TASK-00067)
# File thành phẩm chỉ giữ 3 cột cần dùng, không chép cả bảng: bản gốc là 4 Google Sheet nặng
# ~10 MB, mà 30+ cột còn lại thuộc việc nhập danh mục đèn — không phải việc của task này.
THU_MUC_NGUON = ("danh_muc", "thanh_pham")


def thu_muc_du_lieu(ten="danh_muc"):
	return os.path.join(os.path.dirname(__file__), ten)


def don_ten(ten):
	"""Bỏ mảnh chỉ có nhãn mà không có giá trị. `Ren mịn` giữ nguyên, `Đầu ,` thì bỏ."""
	giu = []
	for manh in ten.split(","):
		if manh.strip() in NHAN_TRONG:
			continue
		giu.append(manh.strip())
	return ", ".join(giu)


# Ô có giá trị đúng bằng tên một cột — dấu hiệu dòng tiêu đề bị lặp lại giữa bảng.
DONG_TIEU_DE_LAP = {"Mã sản phẩm", "Tên sản phẩm", "Nhóm sản phẩm", "Mã biến thể", "Tên biến thể",
                    "Biến thể", "Mô tả", "Phương pháp bổ sung", "Đơn vị tính"}


def _doc_csv(duong_dan):
	"""Đọc CSV, bỏ dòng trống mã và **dòng tiêu đề lặp giữa bảng**.

	⚠ Khách gộp nhiều bảng con vào một sheet nên tiêu đề xuất hiện lại ở giữa — file (TSE) có 6 dòng
	như vậy, file (SLP) có 1. Không lọc thì bộ nạp tạo ra mặt hàng tên "Mã sản phẩm", và nó **không
	báo lỗi gì**: mã hợp lệ, tên hợp lệ, nhóm hợp lệ. Đây không phải đoán ý khách — ô mã trùng khít
	tên một cột thì chắc chắn là tiêu đề, không phải mã hàng.
	"""
	with open(duong_dan, encoding="utf-8") as f:
		tat_ca = list(csv.DictReader(f))
	dong = []
	for r in tat_ca:
		ma_cha = (r.get("Mã sản phẩm") or "").strip()
		if not ma_cha or ma_cha in DONG_TIEU_DE_LAP:
			continue
		dong.append(r)
	return dong


# Khách gọi cột mã biến thể bằng ba tên khác nhau tuỳ file. "Mã đặc tính" xuất hiện ở file (SLP)
# và sheet "(M) Module (1)" — cùng nghĩa, không phải cột đặc tính. Đã đối chiếu dữ liệu: giá trị là
# mã biến thể của mặt hàng cha ở cùng dòng, không phải tên đặc tính.
KHOA_BIEN_THE = ("Mã biến thể", "Biến thể", "Mã đặc tính")
KHOA_TEN_BIEN_THE = ("Tên biến thể", "Tên đặc tính")


def _khoa_bien_the(dong):
	for k in KHOA_BIEN_THE:
		if k in dong[0]:
			return k
	return KHOA_BIEN_THE[0]


def _khoa_ten_bien_the(dong):
	for k in KHOA_TEN_BIEN_THE:
		if k in dong[0]:
			return k
	return KHOA_TEN_BIEN_THE[0]


def _cot_dac_tinh(dong):
	ra = []
	for c in dong[0].keys():
		if c and c not in COT_CO_DINH:
			ra.append(c)
	return ra


def _dau_van(r, cot):
	"""Chữ ký nội dung một dòng, để phân biệt 'lặp y hệt' với 'trùng mã khác nội dung'."""
	cap = []
	for c in cot:
		cap.append((c, (r.get(c) or "").strip()))
	return tuple(sorted(cap))


def gia_tri_chuan(dac_tinh_bang, gia_tri):
	"""Giá trị đã chuẩn hoá theo tên cột TRONG BẢNG (trước khi đổi sang tên đặc tính trên site)."""
	gia_tri = CHUAN_HOA_GIA_TRI.get(dac_tinh_bang, {}).get(gia_tri, gia_tri)
	return gia_tri_so_tran(dac_tinh_bang, gia_tri)


def ten_mat_hang_cha(ten_cha, ten_cac_bien_the):
	"""Tên mặt hàng cha, đã tránh trùng y hệt tên một biến thể của chính nó.

	Bảng nguồn để cột *Tên sản phẩm* của cha chép nguyên tên biến thể đầu tiên, kèm cả công suất —
	25 mặt hàng cha ở sheet Vỏ đèn dính, ví dụ `VDD11` và `VDD11S050` cùng tên
	*"Vỏ đèn đường D11 Chip LED SMD Công suất 50W"*. Trên danh sách Item hiện hai dòng chữ y hệt,
	chỉ phân biệt bằng mã và nhãn Template.

	Mặt hàng cha bao trùm mọi công suất nên bỏ đuôi *"Công suất …W"* là đủ. Chốt của Thắng 11/08:
	chỉ sửa chỗ này, còn tên dài thì giữ nguyên.

	⚠ Chỉ đụng vào khi **thật sự trùng**. Mặt hàng cha nào tên đã khác biến thể thì để nguyên xi,
	kể cả khi tên nó cũng có đuôi công suất.
	"""
	if ten_cha not in ten_cac_bien_the:
		return ten_cha
	rut = re.sub(r"\s*C[ôo]ng su[ấa]t\s*[\d.,]+\s*W\s*$", "", ten_cha).strip(" -,")
	return rut or ten_cha


def _tao_nhom(ten):
	if not ten or frappe.db.exists("Item Group", ten):
		return False
	doc = frappe.new_doc("Item Group")
	doc.item_group_name = ten
	doc.is_group = 0
	doc.insert(ignore_permissions=True)
	return True


def _bao_dam_gia_tri(dac_tinh, gia_tri):
	"""Thêm giá trị còn thiếu vào Item Attribute. Đặc tính chưa tồn tại thì báo lỗi, KHÔNG tự tạo —
	đặt thêm một Item Attribute là quyết định về mô hình dữ liệu, phải do người quyết."""
	if not frappe.db.exists("Item Attribute", dac_tinh):
		frappe.throw(f"Chưa có Item Attribute {dac_tinh!r} trên site")
	doc = frappe.get_doc("Item Attribute", dac_tinh)
	dang_co = set()
	for v in doc.item_attribute_values:
		dang_co.add(v.attribute_value)
	them = []
	for v in gia_tri:
		if v not in dang_co:
			them.append(v)
	if not them:
		return []

	# ERPNext bắt `abbr` duy nhất trong một Item Attribute (item_attribute.py::validate_duplication).
	# Đã vấp: thêm giá trị `1W` vào `Công suất` thì đụng abbr của giá trị `1` đang có.
	abbr_da_co = set()
	for v in doc.item_attribute_values:
		abbr_da_co.add((v.abbr or "").lower())
	for v in them:
		abbr = v
		i = 2
		while abbr.lower() in abbr_da_co:
			abbr = f"{v}-{i}"
			i += 1
		abbr_da_co.add(abbr.lower())
		doc.append("item_attribute_values", {"attribute_value": v, "abbr": abbr})
	doc.save(ignore_permissions=True)
	return them


def sua_ten_neu_lech(ma, ten_dung):
	"""Đổi tên item đã tồn tại nếu đang khác tên mong muốn. Trả về True nếu có sửa.

	Cần vì bộ nạp vốn chỉ-thêm-mới: 25 mặt hàng cha đã nằm trên site với tên cũ từ vòng nạp trước,
	không sửa ở đây thì chúng ở lại vĩnh viễn với tên trùng biến thể.
	"""
	hien = frappe.db.get_value("Item", ma, "item_name")
	if hien is None or hien == ten_dung:
		return False
	doc = frappe.get_doc("Item", ma)
	doc.item_name = ten_dung
	doc.save(ignore_permissions=True)
	return True


def _tao_item(ma, ten, nhom, mo_ta=None, cha=None, dac_tinh=None, la_cha=False, don_vi=None):
	if frappe.db.exists("Item", ma):
		return False
	doc = frappe.new_doc("Item")
	doc.item_code = ma
	doc.item_name = ten
	doc.item_group = nhom
	# Đơn vị lấy từ file nếu có và site đã khai; không có thì dùng mặc định "Cái".
	# Không tự tạo UOM mới — đó là danh mục dùng chung, tạo bừa là đẻ ra "Cái"/"cái"/"CÁI".
	doc.stock_uom = don_vi if (don_vi and frappe.db.exists("UOM", don_vi)) else DON_VI
	doc.is_stock_item = 1
	doc.standard_rate = 0
	if mo_ta:
		doc.description = mo_ta
	if la_cha:
		doc.has_variants = 1
		doc.variant_based_on = "Item Attribute"
		for a in dac_tinh or []:
			doc.append("attributes", {"attribute": a})
	elif cha:
		doc.variant_of = cha
		doc.variant_based_on = "Item Attribute"
		for a, v in (dac_tinh or []):
			doc.append("attributes", {"attribute": a, "attribute_value": v})
	doc.insert(ignore_permissions=True)
	return True


def nhap_mot_file(duong_dan, don_ten_bien_the=False):
	"""Nạp một sheet. Trả về báo cáo chi tiết, không throw vì một dòng hỏng."""
	bc = {
		"file": os.path.basename(duong_dan),
		"nhom_moi": [],
		"gia_tri_dac_tinh_moi": {},
		"cha_moi": 0,
		"bien_the_moi": 0,
		"hang_don_le": 0,
		"lap_y_het": 0,
		"bo_qua": {"trung_ma_khac_noi_dung": [], "cha_lech_dac_tinh": [], "thieu_ma": 0,
		           "dung_to_hop_dac_tinh": []},
	}
	dong = _doc_csv(duong_dan)
	if not dong:
		return bc
	kbt = _khoa_bien_the(dong)
	ktbt = _khoa_ten_bien_the(dong)
	cot_dt = _cot_dac_tinh(dong)

	# 0. Hàng KHÔNG CÓ BIẾN THỂ: dòng có mã sản phẩm nhưng ô mã biến thể để trống.
	#
	# ⚠ 12 file đợt 1 (PM-TASK-00061) luôn có mã biến thể nên trường hợp này chưa từng xảy ra, và
	# bản cũ xếp chúng vào `bo_qua["thieu_ma"]` rồi bỏ luôn — 16 file đợt 2 (PM-TASK-00126) có 85
	# dòng như vậy, tức 85 mặt hàng biến mất mà báo cáo chỉ ghi "thiếu mã", rất dễ đọc lướt qua.
	#
	# Đây KHÔNG phải đoán ý khách: dòng có đủ mã sản phẩm + tên + nhóm, chỉ trống ô biến thể, thì
	# đúng nghĩa là mặt hàng không có biến thể. Đã kiểm: không mã cha nào vừa có dòng biến thể vừa
	# có dòng trống, nên không có chuyện nhầm dòng thừa thành mặt hàng riêng.
	con_lai = []
	co_bien_the = {(r.get("Mã sản phẩm") or "").strip() for r in dong if (r.get(kbt) or "").strip()}
	for r in dong:
		cha_r = (r.get("Mã sản phẩm") or "").strip()
		if (r.get(kbt) or "").strip():
			con_lai.append(r)
			continue
		if cha_r in co_bien_the:
			# mã cha này đã có dòng biến thể ở chỗ khác — dòng trống là dòng thừa, bỏ đúng như cũ
			bc["bo_qua"]["thieu_ma"] += 1
			continue
		nhom_r = (r.get("Nhóm sản phẩm") or "").strip()
		if _tao_nhom(nhom_r):
			bc["nhom_moi"].append(nhom_r)
		if _tao_item(cha_r, (r.get("Tên sản phẩm") or "").strip(), nhom_r,
		             (r.get("Mô tả") or "").strip() or None,
		             don_vi=(r.get(COT_DON_VI) or "").strip() or None):
			bc["hang_don_le"] += 1
	dong = con_lai
	if not dong:
		return bc

	# 1. gom theo mặt hàng cha, loại dòng hỏng
	theo_ma = {}
	for r in dong:
		m = (r.get(kbt) or "").strip()
		if not m:
			bc["bo_qua"]["thieu_ma"] += 1
			continue
		theo_ma.setdefault(m, []).append(r)

	ma_xau = set()
	for m, rs in theo_ma.items():
		if len(rs) == 1:
			continue
		chu_ky = set()
		for r in rs:
			chu_ky.add(_dau_van(r, list(rs[0].keys())))
		if len(chu_ky) == 1:
			bc["lap_y_het"] += len(rs) - 1
		else:
			ma_xau.add(m)
			bc["bo_qua"]["trung_ma_khac_noi_dung"].append(m)

	theo_cha = {}
	for r in dong:
		m = (r.get(kbt) or "").strip()
		if not m or m in ma_xau:
			continue
		cha = (r.get("Mã sản phẩm") or "").strip()
		theo_cha.setdefault(cha, {})
		if m not in theo_cha[cha]:  # lặp y hệt -> giữ dòng đầu
			theo_cha[cha][m] = r

	# 2. nạp từng mặt hàng cha
	for cha, cac_bt in theo_cha.items():
		rs = list(cac_bt.values())
		nhom = (rs[0].get("Nhóm sản phẩm") or "").strip()

		# Đặc tính của mặt hàng cha = HỢP của mọi đặc tính mà biến thể của nó có giá trị.
		# ⚠ Bản đầu ở đây bỏ qua cả mặt hàng cha khi các biến thể không dùng cùng một bộ đặc tính,
		# vì tưởng ERPNext bắt biến thể phải có đủ mọi đặc tính khai trên cha. **Sai** — Thắng phản
		# biện và thử nghiệm cho thấy: khai 2/3 đặc tính vẫn tạo được, ô để trống thì ERPNext tự bỏ
		# dòng đó chứ không báo lỗi. Thứ ERPNext thật sự chặn là hai biến thể **đụng cùng một tổ hợp
		# giá trị** (ItemVariantExistsError) — xử lý ở đoạn dưới.
		dt_dung = []
		for a in cot_dt:
			for r in rs:
				if (r.get(a) or "").strip():
					dt_dung.append(a)
					break

		if _tao_nhom(nhom):
			bc["nhom_moi"].append(nhom)

		for a in dt_dung:
			gt = set()
			for r in rs:
				v = (r.get(a) or "").strip()
				if v:
					gt.add(gia_tri_chuan(a, v))
			them = _bao_dam_gia_tri(DOI_TEN_DAC_TINH.get(a, a), gt)
			if them:
				bc["gia_tri_dac_tinh_moi"].setdefault(DOI_TEN_DAC_TINH.get(a, a), []).extend(them)

		# hàng đơn lẻ: một dòng duy nhất, mã biến thể trùng mã cha, hoặc không có đặc tính nào
		don_le = (len(rs) == 1 and (rs[0].get(kbt) or "").strip() == cha) or not dt_dung
		if don_le:
			for r in rs:
				ma = (r.get(kbt) or "").strip()
				ten = (r.get(ktbt) or r.get("Tên sản phẩm") or "").strip()
				if don_ten_bien_the:
					ten = don_ten(ten)
				if _tao_item(ma, ten, nhom, (r.get("Mô tả") or "").strip() or None,
				             don_vi=(r.get(COT_DON_VI) or "").strip() or None):
					bc["hang_don_le"] += 1
			continue

		# Hai mã khác nhau mà bộ giá trị đặc tính giống hệt thì ERPNext chặn
		# (ItemVariantExistsError). Nghĩa là bảng thiếu một cột đặc tính để phân biệt chúng —
		# ví dụ `PQU-VDP0X-D-…` và `PQU-VDP0X-N-…` khác nhau ở ký tự D/N mà không cột nào tả.
		# Bỏ qua đúng những mã đụng nhau, phần còn lại của mặt hàng cha vẫn nạp bình thường.
		theo_to_hop = {}
		for r in rs:
			khoa = []
			for a in dt_dung:
				v = (r.get(a) or "").strip()
				if v:
					khoa.append((a, gia_tri_chuan(a, v)))
			theo_to_hop.setdefault(tuple(khoa), []).append((r.get(kbt) or "").strip())
		ma_dung = set()
		for ma_list in theo_to_hop.values():
			nhieu = sorted(set(ma_list))
			if len(nhieu) > 1:
				for m in nhieu:
					ma_dung.add(m)
				bc["bo_qua"]["dung_to_hop_dac_tinh"].extend(nhieu)
		giu = []
		for r in rs:
			if (r.get(kbt) or "").strip() not in ma_dung:
				giu.append(r)
		if not giu:
			continue
		rs = giu

		dt_site = []
		for a in dt_dung:
			dt_site.append(DOI_TEN_DAC_TINH.get(a, a))

		ten_bt = []
		for r in rs:
			t = (r.get(ktbt) or "").strip()
			if don_ten_bien_the:
				t = don_ten(t)
			ten_bt.append(t)
		ten_cha = ten_mat_hang_cha((rs[0].get("Tên sản phẩm") or "").strip(), ten_bt)

		if _tao_item(cha, ten_cha, nhom, dac_tinh=dt_site, la_cha=True,
		             don_vi=(rs[0].get(COT_DON_VI) or "").strip() or None):
			bc["cha_moi"] += 1
		elif sua_ten_neu_lech(cha, ten_cha):
			bc["cha_doi_ten"] = bc.get("cha_doi_ten", 0) + 1

		for r in rs:
			ma = (r.get(kbt) or "").strip()
			ten = (r.get(ktbt) or "").strip()
			if don_ten_bien_the:
				ten = don_ten(ten)
			cap = []
			for a in dt_dung:
				v = (r.get(a) or "").strip()
				if v:
					cap.append((DOI_TEN_DAC_TINH.get(a, a), gia_tri_chuan(a, v)))
			if _tao_item(ma, ten, nhom, (r.get("Mô tả") or "").strip() or None, cha=cha, dac_tinh=cap,
			             don_vi=(r.get(COT_DON_VI) or "").strip() or None):
				bc["bien_the_moi"] += 1

	return bc


def cap_nhat_phuong_phap():
	"""Điền *Phương pháp bổ sung* cho mặt hàng theo file nguồn (PM-TASK-00067).

	⚠ **Chỉ đặt cho mặt hàng thường và biến thể, KHÔNG đặt cho mặt hàng cha.** Chốt của Thắng
	12/08: *"Các mặt hàng cha thì không cần phương pháp bổ sung, vì cùng 1 mặt hàng cha có biến thể
	là sản xuất, có biến thể là mua hàng"*. Bản đầu của hàm này có điền cho cha khi mọi biến thể
	khai giống nhau — sai, và hàm cũng **xoá lại** giá trị đã lỡ đặt trên cha.

	Dùng `db_set` chứ không `doc.save()`: chỉ gắn một nhãn phân loại, không cần chạy lại toàn bộ
	validate của Item — mặt hàng cũ trên site có thể vướng ràng buộc khác và hỏng giữa chừng.
	"""
	bc = {"da_dat": 0, "khong_doi": 0, "khong_co_tren_site": 0, "da_xoa_o_cha": 0, "theo_file": {}}
	for ten_thu_muc in THU_MUC_NGUON:
		thu_muc = thu_muc_du_lieu(ten_thu_muc)
		if not os.path.isdir(thu_muc):
			continue
		for f in sorted(os.listdir(thu_muc)):
			if not f.endswith(".csv"):
				continue
			dong = _doc_csv(os.path.join(thu_muc, f))
			if not dong or COT_PHUONG_PHAP not in dong[0]:
				continue
			kbt = _khoa_bien_the(dong)
			dem = 0
			for r in dong:
				gia_tri = (r.get(COT_PHUONG_PHAP) or "").strip()
				# Hàng không có biến thể: mã nằm ở cột "Mã sản phẩm". Bản cũ chỉ đọc cột mã biến
				# thể nên 85 mặt hàng loại này bị bỏ trắng Phương pháp bổ sung (PM-TASK-00126).
				ma = (r.get(kbt) or "").strip() or (r.get("Mã sản phẩm") or "").strip()
				if not ma or not gia_tri:
					continue
				hien = frappe.db.get_value("Item", ma, ["has_variants", TRUONG_PHUONG_PHAP])
				if hien is None:
					bc["khong_co_tren_site"] += 1
					continue
				co_bien_the, dang_co = hien
				if co_bien_the:  # mặt hàng cha — bỏ qua, xử lý ở vòng dưới
					continue
				if dang_co == gia_tri:
					bc["khong_doi"] += 1
					continue
				frappe.db.set_value("Item", ma, TRUONG_PHUONG_PHAP, gia_tri, update_modified=False)
				bc["da_dat"] += 1
				dem += 1
			bc["theo_file"][f] = dem

	# Dọn giá trị đã lỡ đặt trên mặt hàng cha.
	for ma in frappe.db.sql_list(
		f"select name from tabItem where has_variants = 1 and ifnull({TRUONG_PHUONG_PHAP}, '') != ''"
	):
		frappe.db.set_value("Item", ma, TRUONG_PHUONG_PHAP, None, update_modified=False)
		bc["da_xoa_o_cha"] += 1

	frappe.db.commit()
	return bc


def nhap_tat_ca():
	"""Nạp toàn bộ file trong `data/danh_muc/`, trả về danh sách báo cáo theo từng file."""
	thu_muc = thu_muc_du_lieu()
	ket_qua = []
	ten_file = sorted(os.listdir(thu_muc))
	for f in ten_file:
		if not f.endswith(".csv"):
			continue
		# chỉ sheet ốc/vít/bulong dựng tên theo khuôn có nhãn cụt; 10 sheet còn lại tên sạch
		don = "oc-vit-bulong" in f
		ket_qua.append(nhap_mot_file(os.path.join(thu_muc, f), don_ten_bien_the=don))
	return ket_qua
