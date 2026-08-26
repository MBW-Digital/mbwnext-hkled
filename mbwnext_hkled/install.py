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

## THỨ TỰ CÀI APP — app lõi TRƯỚC, app khách SAU CÙNG

    1. erpnext
    2. hrms · print_designer                (độc lập, đâu cũng được)
    3. mbwnext_localization                 ⚠ PHẢI TRƯỚC MỌI APP MBWNEXT KHÁC
    4. mbwnext_advanced_selling
    5. mbwnext_advanced_buying · _stock · _accounting · _distribution_map
    6. super_admin
    7. mbwnext_hkled                        ⚠ APP KHÁCH, CUỐI CÙNG

Không phải quy ước cho đẹp — hai ràng buộc đo được, cả hai vấp thật ngày 25-26/08/2026:

**(a) `mbwnext_localization` phải đứng trước.** `install/after_install.py::del_masterdataCore()`
gọi `frappe.db.sql("DELETE FROM tab<doctype>")` — SQL thẳng, không kiểm liên kết — cho
`Item Group`, `UOM`, `UOM Conversion`, `Territory`, `Stock Entry Type`, `Province`, `Commune`,
rồi dựng lại bộ chuẩn MBWD. Cài nó SAU app khách là **xoá sạch phân nhóm của cả danh mục**:
đo trên `test.com`, Item Group tụt 50 → 8 và 61.835/61.836 mặt hàng trỏ vào nhóm không tồn
tại. (Mặt hàng và UOM thì còn — `tabItem.item_group` giữ nguyên chuỗi tên, dựng lại nhóm là
liên kết tự nối.) `mbwnext_advanced_selling` cũng có `del_masterdataCore` nhưng hẹp hơn
nhiều: chỉ xoá Customer Group.

**(b) `mbwnext_advanced_selling` phải đứng trước app khách.** Nó thêm Custom Field cho `Item`
(`setup/custom_fields.json`). Cài sau khi app khách đã nạp 62 nghìn mặt hàng thì các cột đó
rỗng toàn bộ. Ba app lõi còn lại không chạm `Item` nên đứng sau vô hại — nhưng đừng dựa vào
điều đó, nó đúng ở thời điểm đo chứ không phải luật.

⚠ **ĐỪNG lấy thứ tự từ `bench --site <site> list-apps`.** Nó in theo `idx` của bảng
`Installed Application`, phản ánh lịch sử cài của site đó chứ không phải thứ tự đúng.
Thứ tự lấy từ `hkled.com` ngày 25/08 có `mbwnext_localization` ở vị trí 9 (sau các app
advanced_*) và `mbwnext_hkled` ở vị trí 10 (trước `mbwnext_advanced_accounting`) — sai cả
hai ràng buộc trên. Chạy theo nó thì `bench install-app mbwnext_advanced_buying` chết ngay
ở `InvalidRemoteException` vì `required_apps` trỏ tới `mbwnext_localization` chưa cài.
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
