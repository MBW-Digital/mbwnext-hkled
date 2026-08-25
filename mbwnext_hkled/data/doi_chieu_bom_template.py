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
	from mbwnext_hkled.data.nhap_bom_template import _dac_tinh_bien_the, _doc_spec, dung_rules

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

		bao["sheet"][ten] = {
			"bom_template": bt,
			"so_rule_file": len(tu_file),
			"so_rule_site": len(tren_site),
			"lech": lech,
			"chi_co_site": chi_site,
			"chi_co_file": [{"thanh_phan": k[0], "cond_attrs": k[1]}
			                for k in tu_file if k not in tren_site],
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
	print(f"{'sheet':<14}{'file':>7}{'site':>7}{'LỆCH':>7}{'chỉ ở site':>12}{'chỉ ở file':>12}")
	for ten, s in bao["sheet"].items():
		tong_lech += len(s["lech"])
		tong_site += len(s["chi_co_site"])
		tong_file += len(s["chi_co_file"])
		print(f"{ten:<14}{s['so_rule_file']:>7}{s['so_rule_site']:>7}"
		      f"{len(s['lech']):>7}{len(s['chi_co_site']):>12}{len(s['chi_co_file']):>12}")

	for ten, s in bao["sheet"].items():
		for d in s["lech"]:
			print(f"  ⚠ {ten} · {d['thanh_phan']} · {d['dieu_kien']}: "
			      f"file={d['file']['item']!r} ≠ site={d['site']['item']!r} (sửa {d['modified']})")
		for d in s["chi_co_site"]:
			print(f"  ⚠ {ten} · {d['thanh_phan']} · {d['dieu_kien']}: "
			      f"chỉ có trên site, item={d['item']!r} (sửa {d['modified']})")

	for ten, loi in bao["loi"].items():
		print(f"  ⚠ BỎ QUA sheet {ten}: {loi}")
	for d in bao["ngoai_spec"]:
		print(f"  · ngoài spec: {d['bom_template']!r} (item {d['item_template']}, "
		      f"is_active={d['is_active']}, {d['so_rule']} rule) — bộ nạp không đụng tới")

	if tong_lech or tong_site:
		print(f"\n🔴 CÓ {tong_lech + tong_site} rule KHÁC với file. "
		      f"Chạy `import_bom_template` bây giờ là GHI ĐÈ MẤT. Hỏi trước khi migrate.")
	else:
		print("\n✅ Không rule nào lệch — chạy lại `import_bom_template` không mất gì.")
	return bao
