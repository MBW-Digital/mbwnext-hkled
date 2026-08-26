# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt
"""Đối chiếu `bom_template/spec.json` với BOM Rule đang có trên site. CHỈ ĐỌC.

## Chạy trước mỗi lần nâng cấp

	bench --site hkled.com execute mbwnext_hkled.data.doi_chieu_bom_template.chay

## Vì sao cần

`nhap_bom_template.nhap_mot_sheet()` **xoá sạch** `bom_rules` và `bom_component_table`
của template cũ rồi dựng lại từ file (chốt của Thắng 18/08: file là bản gốc, ghi đè bản
cũ). Đúng cho lần nạp đầu. Nhưng `import_bom_template` là **patch**, mà patch thì chạy lại
trên site đã có dữ liệu: đo 25/08/2026, `hkled.com` khai 24 patch mà `Patch Log` mới có 18
— `import_bom_template` nằm trong 7 patch **sẽ chạy** ở lần `bench migrate` tới.

Nghĩa là: rule nào khách tự sửa trên lưới sẽ bị ghi đè, **không có cảnh báo**. Ô Nguyên Vật
Liệu trên lưới sửa được, nên chuyện này không giả định — nó chỉ chưa xảy ra.

Hàm này trả lời đúng một câu: **khách đã sửa gì chưa.** Không sửa gì cả, chỉ báo.

## Đọc kết quả

- `lech` — rule có ở cả hai bên nhưng khác `item`/`khong_su_dung`. **Đây là dấu hiệu khách
  đã sửa tay**; ghi đè là mất. Cột `modified` cho biết sửa lúc nào.
- `chi_co_site` — rule có trên site mà file không sinh ra. Cũng là sửa tay (thêm dòng).
- `chi_co_file` — file sinh ra mà site chưa có. Bình thường nếu file vừa cập nhật.
- `ngoai_spec` — BOM Template trên site không có sheet tương ứng trong file. Bộ nạp
  **không đụng tới** chúng, nên không mất gì; liệt kê để biết chúng tồn tại.

⚠ Khoá đối chiếu là `(bom_component, cond_attrs)`. KHÔNG dùng `rule_id`: nó là số thứ tự
(`rule_1`, `rule_2`…) nên chỉ cần file đổi thứ tự dòng là lệch giả toàn bộ. Cũng không dùng
`cond_label` — `dung_rules()` không sinh trường đó, nó được tính lúc ghi.

Đo lần đầu 25/08/2026 trên `hkled.com`: **733/733 khớp tuyệt đối, 0 lệch** — tới thời điểm
đó khách chưa sửa rule nào. Ngoài spec có đúng 1 cái: `thành phẩm 1` (`DD11S050`), bản thử
tay từ 03/08, `is_active = 0`.

## MỐC GỐC ĐÃ CHỐT — đọc trước khi làm phần hợp nhất của hướng B

Thắng chốt 26/08/2026: **dữ liệu trên hệ thống là gốc** (hướng B). Nghĩa là bộ nạp không
được đè lên rule khách đã tự sửa. Nhưng file spec **vẫn đang đổi** (3 lần trong 7 ngày:
19/08, 22/08, 24/08), nên cũng không được ngừng đè hẳn — bản sửa file lần sau sẽ không vào
được.

Muốn phân biệt "khách sửa" với "file đổi" thì cần **ba bản**, không phải hai: bản trên site,
bản trong file mới, và **bản mà bộ nạp đã ghi lần trước** (bản gốc). Có bản gốc thì mọi ca
đều quyết được, kể cả ca cả hai cùng đổi:

	site == gốc, file != gốc                  -> chỉ file đổi      -> ĐÈ
	site != gốc, file == gốc                  -> chỉ khách sửa     -> GIỮ
	site != gốc, file != gốc, site != file     -> ĐỤNG NHAU        -> báo, đừng đoán
	site != gốc, file != gốc, site == file     -> trùng ý          -> không phải làm gì

⚠ **BẢN GỐC LÀ LẦN NẠP CUỐI, KHÔNG PHẢI `spec.json` HIỆN TẠI.** Chỗ này tôi kết luận sai
một lần (commit `a13ed32` ghi bản gốc là `f155666`) — sửa lại ngày 26/08/2026:

	BẢN GỐC của hkled.com = spec.json @ HEAD               ← đúng lại từ 26/08/2026

Trước 26/08 thì không phải vậy, và đây là lý do:

	spec.json @ 8f8795b (22/08)   ← lần bộ nạp chạy cuối, site phản ánh bản này
	spec.json @ f155666 (24/08)   ← lệch 4 dòng so với site, và LỆCH ĐÓ LÀ LỖI

4 dòng lệch (`Ốc dây điện` của `M30S050-A/B`, `M50S050-A/B`) hoá ra **không phải bản sửa
hợp lệ chưa nạp** — chúng là **lỗi đọc bảng khách**: chữ *"Theo rule"* trong bảng khách là
SỐ LƯỢNG theo rule, NVL vẫn cố định; bản trích 24/08 dịch thành `"Theo Rule"` của hệ thống
mình, nghĩa là NVL do rule quyết. Anh Thắng xác nhận 26/08. Đã sửa 4 dòng đó về `Cố Định`,
và sau khi sửa thì lệnh này ra **0 lệch cả hai bảng** — site và file nói cùng một thứ.

⚠ Bài học giữ lại: lệch giữa file và site có **ba** nguồn, không phải hai — file đổi chưa
nạp · khách sửa tay · **và file sai**. Ca thứ ba nhìn giống hệt ca thứ nhất. Phân biệt bằng
cách hỏi khách, không phải bằng dấu thời gian.

Bằng chứng: mọi `BOM Rule` và `BOM Component Table` trên site đều mang `modified`
`2026-08-22 10:49` — mốc nạp hàng loạt; sau đó không ai chạy lại bộ nạp, còn `spec.json` thì
đã có thêm commit `f155666` ngày 24/08.

Vì sao sai mà phần rule vẫn khớp: đã đo, **hai bản spec sinh ra `bom_rules` giống hệt nhau**
(733/733 với cả `8f8795b` lẫn `f155666`) — thay đổi 24/08 chỉ chạm `thanh_phan`. Nên với
`bom_rules` thì nhầm bản gốc vô hại. Với `bom_component_table` thì **không**: 4 dòng
`Ốc dây điện` của `M30S050-A/B` và `M50S050-A/B` đổi `kieu` từ `Cố Định` sang `Theo Rule`
trong commit 24/08.

Đây chính là kiểu hỏng âm thầm mà hướng B sinh ra để chặn, chỉ khác chiều: lấy `f155666` làm
bản gốc thì 4 dòng đó bị xếp nhầm là "khách sửa" → **GIỮ** → bản sửa 24/08 của đội mình
không bao giờ vào được site, và không có gì báo. Xếp đúng (`site == gốc`, `file != gốc`) thì
ra **ĐÈ**, đúng như mong muốn.

➜ **Cách xác định bản gốc**: là commit `spec.json` cuối cùng **trước** lần bộ nạp chạy gần
nhất. Lần nạp gần nhất đọc bằng `max(modified)` của `BOM Rule`. Đừng mặc định lấy HEAD.

➜ Chạy lệnh này trước khi làm phần hợp nhất. Còn ra `✅ 0 lệch` thì bản gốc còn suy ra được
từ git; ra `🔴` thì phải soi tiếp: lệch đó là **file đổi chưa nạp** hay **khách sửa thật** —
hai thứ nhìn giống nhau nếu chỉ so hai bản.

## Đọc kết quả ở lần chạy TỚI (26/08/2026 → tới khi hkled.com nạp lại)

Spec vừa đổi 4 dòng `Ốc dây điện` (`M30S050-A/B`, `M50S050-A/B`) từ `Cố Định` sang
`Theo Rule`, mà `hkled.com` thì **chưa nạp lại** — `import_bom_template` còn nằm trong nhóm
patch chờ `bench migrate`. Nên lệnh này **sẽ báo 4 lệch**, và đó là lệch HỢP LỆ.

Chạy lệnh này NGAY TRƯỚC khi nạp lại — đừng tin con số đo hôm trước, khách đang giai đoạn
test và có thể sửa bất cứ lúc nào. Đọc kết quả:

⚠ ĐẾM SỐ DÒNG VÀ ĐỌC TÊN LÀ KHÔNG ĐỦ. Nếu khách sửa tay **đúng một trong 4 dòng đang dự
kiến lệch**, kết quả vẫn ra "lệch = 4, đúng 4 dòng `Ốc dây điện`" — cái sửa nằm trùng lên
cái dự kiến, phép đếm mù đúng chỗ đó. Phải so **giá trị**, không chỉ so tên trường.

Lệch dự kiến có hình dạng chính xác như sau, cả 4 dòng giống hệt nhau:

	BOM Component Table — mỗi dòng `Ốc dây điện`, trường `khac` phải ĐÚNG BẰNG:
	    component_type : file 'Theo Rule'  ≠  site 'Số Lượng Theo Công Thức'
	    item           : file ''           ≠  site 'OPG-M12-RM'
	BOM Rule — "chỉ ở file" = 4, mỗi sheet module 1 (rule `Ốc dây điện` mới thêm)
	cột `sửa` của cả 4 dòng TRÙNG mốc nạp hàng loạt gần nhất
	                                            → ĐÚNG DỰ KIẾN, nạp tiếp

	`khac` có thêm trường khác (`qty`…), hoặc giá trị `site` khác hai giá trị trên,
	hoặc xuất hiện dòng ngoài 4 dòng đó, hoặc mốc `sửa` MUỘN HƠN lần nạp
	                                            → DỪNG, hỏi trước khi nạp

Vì sao so giá trị là kín: khách sửa NVL thì `item.site` khác `OPG-M12-RM`; sửa số lượng thì
`khac` mọc thêm `qty`. Việc nạp lại chỉ sinh đúng hai trường trên với đúng hai cặp giá trị
đó. Hai thứ không lẫn nhau được.

⚠ Điều kiện "mốc `sửa` muộn hơn lần nạp → DỪNG" áp cho **cả 4 dòng dự kiến lệch**, đừng miễn
cho chúng vì "đằng nào cũng lệch" — chúng chính là chỗ phép đếm không cứu được, nên mốc thời
gian là lớp bảo vệ còn lại duy nhất ở đó.

Sau khi nạp lại thành công thì cả hai bảng phải về 0 lệch, và đoạn này bỏ đi được.

## Cách kiểm chéo, KHÔNG dùng lệnh này

Lệnh này so **nội dung**. Muốn xác nhận độc lập thì đừng chạy lại chính nó — cùng một logic
thì ra cùng một kết quả, kể cả khi logic sai. Soi **dấu thời gian** là đường khác hẳn:

	select date_format(modified,'%Y-%m-%d %H:%i') moc, count(*)
	from `tabBOM Rule` group by 1 order by 2 desc;

Rule do bộ nạp ghi thì dồn vào **một mốc phút duy nhất** của lần nạp hàng loạt. Rule khách
sửa tay sẽ **lẻ ra mốc khác**, muộn hơn, và muộn hơn cả `modified` của `BOM Template` cha.
Đo 25/08/2026: cả 733 rule đúng một mốc `2026-08-22 10:49`, không cái nào muộn hơn template
cha — khớp kết quả so nội dung. (Cách này do phiên BOM `cozy-dev-a2` làm; ghi lại vì hai
phương pháp độc lập cùng ra một kết quả thì mới đáng tin.)

⚠ Dấu thời gian **không thay được** lệnh này, và ngược lại. Nó chỉ nói *có ai đụng vào
không*; lệnh này nói *đụng cái gì, giá trị cũ là gì*. Sửa rồi sửa lại đúng như cũ thì dấu
thời gian báo động giả; ngược lại thao tác ghi cả bảng cũng làm `modified` nhảy mà nội dung
không đổi. Dùng cả hai.
"""

import json

import frappe


# Chữ ký của MỘT lệch đã biết trước và vô hại — xem mục "Lệch dự kiến" trong docstring.
# Spec `5f25811` đổi `Ốc dây điện` sang `Theo Rule` và chuyển NVL sang rule; site nào chưa nạp
# lại thì lệch đúng hình dạng này.
#
# ⚠ TỰ HẾT HẠN, cố ý làm vậy: nạp xong thì `component_type` trên site thành `Theo Rule`, chữ ký
# không còn khớp, và 4 dòng đó lập tức được tính là lệch THẬT. Không ai phải nhớ đi xoá đoạn
# này. Ghi kỳ vọng bằng chữ trong tài liệu thì lần migrate sau người chạy vẫn chờ "4 lệch" và
# vẫy qua một lệch thật — phiên BOM chỉ ra đúng chỗ đó.
LECH_DU_KIEN = {
	"thanh_phan": "Ốc dây điện",
	"khac": {
		"component_type": {"file": "Theo Rule", "site": "Số Lượng Theo Công Thức"},
		"item": {"file": "", "site": "OPG-M12-RM"},
	},
}


def _la_lech_du_kien(d):
	return d.get("thanh_phan") == LECH_DU_KIEN["thanh_phan"] and d.get("khac") == LECH_DU_KIEN["khac"]


def _chuan_attrs(v):
	"""Chuẩn hoá cond_attrs về một chuỗi so sánh được: site lưu JSON, bộ dựng trả dict."""
	if v is None or v == "":
		return "{}"
	if isinstance(v, str):
		try:
			v = json.loads(v)
		except ValueError:
			return v
	if isinstance(v, dict):
		return json.dumps({str(k): str(x) for k, x in sorted(v.items())},
		                  ensure_ascii=False, sort_keys=True)
	return str(v)


def so_sanh():
	"""Trả về báo cáo dạng dict. Không in, không sửa gì."""
	from mbwnext_hkled.data.nhap_bom_template import (
		_dac_tinh_bien_the,
		_doc_spec,
		_so_luong,
		dung_rules,
	)

	spec = _doc_spec()
	bao = {"sheet": {}, "loi": dict(spec.get("loi") or {}), "ngoai_spec": []}
	da_soi = set()

	for ten, s in spec["sheets"].items():
		item_cha = s["item_cha"]
		bien_the = _dac_tinh_bien_the(item_cha)
		if not bien_the:
			bao["loi"][ten] = f"Mặt hàng cha {item_cha} chưa có biến thể nào"
			continue
		rules, _ghi_chu, _bo_qua = dung_rules(s, bien_the)
		tu_file = {}
		for r in rules:
			khoa = (str(r.get("bom_component") or ""), _chuan_attrs(r.get("cond_attrs")))
			tu_file[khoa] = (str(r.get("item") or ""), str(r.get("khong_su_dung") or 0))

		tren_site = {}
		bt = frappe.db.get_value("BOM Template", {"item_template": item_cha})
		if bt:
			da_soi.add(bt)
			for r in frappe.get_all(
				"BOM Rule",
				filters={"parent": bt, "parenttype": "BOM Template"},
				fields=["bom_component", "cond_attrs", "item", "khong_su_dung",
				        "cond_label", "modified"],
				limit_page_length=0,
			):
				khoa = (str(r.bom_component or ""), _chuan_attrs(r.cond_attrs))
				tren_site[khoa] = r

		lech, chi_site = [], []
		for khoa, r in tren_site.items():
			f = tu_file.get(khoa)
			hien = (str(r.item or ""), str(r.khong_su_dung or 0))
			if f is None:
				chi_site.append({"thanh_phan": khoa[0], "dieu_kien": r.cond_label,
				                 "item": hien[0], "modified": str(r.modified)})
			elif f != hien:
				lech.append({"thanh_phan": khoa[0], "dieu_kien": r.cond_label,
				             "file": {"item": f[0], "khong_su_dung": f[1]},
				             "site": {"item": hien[0], "khong_su_dung": hien[1]},
				             "modified": str(r.modified)})

		# BẢNG THỨ HAI — `bom_component_table`. `nhap_mot_sheet()` xoá cả hai bảng
		# (`doc.set(..., [])` hai dòng liền nhau), nên hợp nhất mà chỉ lo `bom_rules` là
		# hướng B **vẫn thủng ở đây**. Và đây mới là chỗ `qty` sống: `BOM Rule` không có
		# trường `qty` nào cả, số lượng thật đi vào BOM nằm ở bảng này.
		ct_file = {}
		for t in s["thanh_phan"]:
			sl, _ly_do = _so_luong(t["sl_tho"])
			kieu = t["kieu"]
			# lặp lại đúng phép nâng kiểu của bộ nạp, nếu không sẽ báo lệch giả
			if sl is None and kieu == "Cố Định":
				kieu = "Số Lượng Theo Công Thức"
			ct_file[t["thanh_phan"]] = {
				"component_type": kieu,
				"qty": float(sl if sl is not None else 0),
				"item": (t["nvl"] if t["kieu"] != "Theo Rule" else None) or "",
			}
		ct_site, ct_lech, ct_chi_site = {}, [], []
		if bt:
			for r in frappe.get_all(
				"BOM Component Table",
				filters={"parent": bt, "parenttype": "BOM Template"},
				fields=["bom_component", "component_type", "qty", "item", "modified"],
				limit_page_length=0,
			):
				ct_site[r.bom_component] = r
		for tp, r in ct_site.items():
			f = ct_file.get(tp)
			hien = {"component_type": r.component_type, "qty": float(r.qty or 0),
			        "item": r.item or ""}
			if f is None:
				ct_chi_site.append({"thanh_phan": tp, "site": hien,
				                    "modified": str(r.modified)})
			else:
				khac = {c: {"file": f[c], "site": hien[c]} for c in f if f[c] != hien[c]}
				if khac:
					ct_lech.append({"thanh_phan": tp, "khac": khac,
					                "modified": str(r.modified)})

		bao["sheet"][ten] = {
			"bom_template": bt,
			"so_rule_file": len(tu_file),
			"so_rule_site": len(tren_site),
			"lech": lech,
			"chi_co_site": chi_site,
			"chi_co_file": [{"thanh_phan": k[0], "cond_attrs": k[1]}
			                for k in tu_file if k not in tren_site],
			"ct_file": len(ct_file),
			"ct_site": len(ct_site),
			"ct_lech": ct_lech,
			"ct_chi_co_site": ct_chi_site,
			"ct_chi_co_file": [tp for tp in ct_file if tp not in ct_site],
		}

	for bt in frappe.get_all("BOM Template", fields=["name", "item_template", "is_active"]):
		if bt.name not in da_soi:
			bao["ngoai_spec"].append({
				"bom_template": bt.name, "item_template": bt.item_template,
				"is_active": bt.is_active,
				"so_rule": frappe.db.count("BOM Rule", {"parent": bt.name}),
			})
	return bao


def chay():
	"""Bản in ra màn hình, để gọi bằng `bench execute`."""
	bao = so_sanh()
	tong_lech = tong_site = tong_file = 0
	print("BOM Rule")
	print(f"{'  sheet':<14}{'file':>7}{'site':>7}{'LỆCH':>7}{'chỉ ở site':>12}{'chỉ ở file':>12}")
	for ten, s in bao["sheet"].items():
		tong_lech += len(s["lech"])
		tong_site += len(s["chi_co_site"])
		tong_file += len(s["chi_co_file"])
		print(f"  {ten:<12}{s['so_rule_file']:>7}{s['so_rule_site']:>7}"
		      f"{len(s['lech']):>7}{len(s['chi_co_site']):>12}{len(s['chi_co_file']):>12}")

	ct_lech = ct_site = ct_file = ct_du_kien = 0
	print("\nBOM Component Table")
	print(f"{'  sheet':<14}{'file':>7}{'site':>7}{'LỆCH':>7}{'chỉ ở site':>12}{'chỉ ở file':>12}")
	for ten, s in bao["sheet"].items():
		du_kien = [d for d in s["ct_lech"] if _la_lech_du_kien(d)]
		ct_du_kien += len(du_kien)
		ct_lech += len(s["ct_lech"]) - len(du_kien)
		ct_site += len(s["ct_chi_co_site"])
		ct_file += len(s["ct_chi_co_file"])
		print(f"  {ten:<12}{s['ct_file']:>7}{s['ct_site']:>7}"
		      f"{len(s['ct_lech']):>7}{len(s['ct_chi_co_site']):>12}{len(s['ct_chi_co_file']):>12}")
	print()

	for ten, s in bao["sheet"].items():
		for d in s["lech"]:
			print(f"  ⚠ Rule · {ten} · {d['thanh_phan']} · {d['dieu_kien']}: "
			      f"file={d['file']['item']!r} ≠ site={d['site']['item']!r} (sửa {d['modified']})")
		for d in s["chi_co_site"]:
			print(f"  ⚠ Rule · {ten} · {d['thanh_phan']} · {d['dieu_kien']}: "
			      f"chỉ có trên site, item={d['item']!r} (sửa {d['modified']})")
		for d in s["ct_lech"]:
			if _la_lech_du_kien(d):
				print(f"  · DỰ KIẾN · {ten} · {d['thanh_phan']}: site chưa nạp spec mới "
				      f"(sửa {d['modified']}) — nạp lại là hết")
				continue
			cts = ", ".join(f"{c}: file={v['file']!r} ≠ site={v['site']!r}"
			                for c, v in d["khac"].items())
			print(f"  ⚠ Thành phần · {ten} · {d['thanh_phan']}: {cts} (sửa {d['modified']})")
		for d in s["ct_chi_co_site"]:
			print(f"  ⚠ Thành phần · {ten} · {d['thanh_phan']}: chỉ có trên site "
			      f"(sửa {d['modified']})")

	for ten, loi in bao["loi"].items():
		print(f"  ⚠ BỎ QUA sheet {ten}: {loi}")
	for d in bao["ngoai_spec"]:
		print(f"  · ngoài spec: {d['bom_template']!r} (item {d['item_template']}, "
		      f"is_active={d['is_active']}, {d['so_rule']} rule) — bộ nạp không đụng tới")

	if ct_du_kien:
		print(f"\n· {ct_du_kien} dòng lệch DỰ KIẾN (site chưa nạp spec mới) — không tính là lệch.")
		print("  ⚠ Vẫn phải soi cột `sửa` của chúng: trùng mốc nạp hàng loạt thì yên tâm, muộn")
		print("    hơn thì có người đụng tay, DỪNG. Đây là 4 dòng phép đếm không cứu được.")
	tong = tong_lech + tong_site + ct_lech + ct_site
	if tong:
		print(f"\n🔴 CÓ {tong} dòng KHÁC với file ({tong_lech + tong_site} rule, "
		      f"{ct_lech + ct_site} thành phần).")
		print("   ⚠ KHÁC KHÔNG CÓ NGHĨA LÀ KHÁCH SỬA. Hai khả năng nhìn giống hệt nhau:")
		print("     · file đã đổi mà CHƯA nạp  -> nạp lại là đúng, không mất gì")
		print("     · khách sửa trên màn hình  -> nạp lại là MẤT")
		print("   Phân biệt bằng cột `sửa`: trùng mốc nạp hàng loạt gần nhất thì là file đổi;")
		print("   lẻ ra mốc muộn hơn thì là khách sửa. Xem mục MỐC GỐC trong docstring.")
	else:
		print("\n✅ Không dòng nào lệch — chạy lại `import_bom_template` không mất gì.")
	return bao
