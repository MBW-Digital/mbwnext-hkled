# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt
"""Dựng phần dữ liệu của app khi **cài lên site mới**.

⚠ VÌ SAO PHẢI CÓ FILE NÀY — đọc trước khi sửa `patches.txt`.

`frappe.installer.install_app()` gọi `set_all_patches_as_completed(app)` **trước**
khi chạy bất kỳ hook nào: mọi dòng trong `patches.txt` được ghi thẳng vào `Patch Log`
mà KHÔNG chạy. Đó là hành vi cố ý của Frappe — patch sinh ra để nâng cấp site đang
chạy, còn site mới thì phải tự dựng đủ trong lúc cài.

Hệ quả với app này: site mới cài xong `bench migrate` chạy 20 giây, báo thành công,
và **không có gì cả** — 0 mặt hàng, 0 Item Attribute, 0 BOM Template, không có Server
Script tính định mức, thiếu 2 dòng Custom DocPerm cho bên sản xuất. Hỏng hoàn toàn im
lặng. Đo trên site trắng `test.com` ngày 25/08/2026.

Cái sống sót được là fixtures (31 Custom Field + 19 Property Setter) — vì
`install_app` tự gọi `sync_fixtures`. Mọi thứ nằm trong patch thì không.

⚠ ĐỪNG SUY RỘNG SANG SITE ĐÃ CHẠY. `set_all_patches_as_completed` được gọi từ **đúng một
chỗ**: bên trong `install_app` (`installer.py:322`). `bench migrate` KHÔNG gọi nó. Nên trên
site đã cài app từ trước — `hkled.com`, và cổng thật — patch **thêm vào sau ngày cài vẫn
chạy bình thường** ở lần migrate kế tiếp. Đo 25/08/2026: `hkled.com` khai 24 patch, `Patch
Log` mới có 18, tức **7 patch sẽ chạy** ở lần `bench migrate` tới, trong đó có cả ba patch
nạp danh mục.

Tóm lại có hai ca ngược nhau, đừng lẫn:
  · site MỚI cài app  → patch bị đánh dấu xong, không chạy → file này lo phần đó
  · site ĐÃ CHẠY migrate → patch mới chạy thật, phải tính thời gian và tính rủi ro dữ liệu

DÙNG `after_sync`, KHÔNG DÙNG `after_install`:
`install_app` chạy `after_install` ở dòng 325 nhưng `sync_fixtures` mãi dòng 331.
Đặt ở `after_install` là các loader chạy lúc Custom Field của Item chưa tồn tại.
`after_sync` (dòng 336) chạy sau fixtures, và **chỉ chạy khi cài** — `bench migrate`
không đụng tới nó, nên không tốn 62.054 lần `db.exists` mỗi lần migrate.

LUẬT: thêm patch nào **tạo dữ liệu** (không phải sửa dữ liệu sẵn có) thì phải thêm
tên nó vào `CAC_BUOC` dưới đây, nếu không site mới sẽ thiếu đúng phần đó.
"""

import frappe

# Chỉ liệt kê patch DỰNG dữ liệu. Patch chuyển đổi dữ liệu cũ (rename_*, migrate_*,
# backfill_*, cleanup_*, adjust_*, drop_*) cố ý không có ở đây: site mới không có gì
# để chuyển đổi. Patch tạo Custom Field / Property Setter cũng không cần — fixtures lo.
CAC_BUOC = (
	# Server Script `hkled_resolve_bom_qty`: engine BOM không chạy nếu thiếu.
	"create_bom_qty_server_script",
	# 2 dòng Custom DocPerm cho Employee. Cố ý không khai vào fixtures — xem docstring
	# của chính patch đó để biết lý do (fixtures sẽ chụp cả quyền của app lõi).
	"grant_production_read_on_employee",
	# ⚠ THỨ TỰ DƯỚI ĐÂY GIỐNG HỆT `patches.txt` VÀ CÓ Ý NGHĨA — xem chú thích ở đó.
	"seed_item_attribute",
	"import_danh_muc_vat_tu",
	"add_item_replenishment_method",
	"import_danh_muc_vat_tu_dot_2",
	"import_thanh_pham",
	"import_bom_template",
)


def after_sync():
	for ten in CAC_BUOC:
		print(f"[mbwnext_hkled] dựng dữ liệu: {ten}")
		frappe.get_attr(f"mbwnext_hkled.patches.{ten}.execute")()
		frappe.db.commit()
