# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Trường *Phương pháp bổ sung* trên Mặt hàng, và điền cho toàn bộ danh mục (PM-TASK-00067).

Yêu cầu của HKLED: thêm một trường Select ba giá trị *Sản xuất / Gia công / Mua hàng*, rồi cập
nhật cho các sản phẩm. Sau này dùng cho chức năng dự báo tồn kho.

Nguồn dữ liệu nằm ở **hai chỗ**, cả hai đều do khách bổ sung cột *"Phương pháp bổ sung"*:

- `data/danh_muc/*.csv` — vật tư, linh kiện (11 sheet của PM-TASK-00061)
- `data/thanh_pham/*.csv` — đèn thành phẩm (4 file *Nhóm I…IV* trong thư mục Drive của task này)

Phần điền giá trị ở `data/nhap_item.py::cap_nhat_phuong_phap()`.

⚠ **Mặt hàng cha không mang giá trị này** — chốt của Thắng 12/08: cùng một mặt hàng cha có biến thể
là *Sản xuất*, có biến thể là *Mua hàng*, nên đặt ở cha là sai.

## Vì sao không dùng trường lõi sẵn có

ERPNext đã có `default_material_request_type` (*Purchase / Material Transfer / Material Issue /
Manufacture / Customer Provided*) nghĩa gần trùng. **Cố ý không dùng lại**, hai lý do:

1. Nó **không có** giá trị tương ứng *"Gia công"* — ERPNext mô tả gia công bằng cờ
   `is_sub_contracted_item` + BOM, không phải một lựa chọn trong danh sách này.
2. Trường lõi đang là `Purchase` cho cả 60.784 mặt hàng (giá trị mặc định, chưa ai đụng), và nó
   điều khiển hành vi thật của Yêu cầu mặt hàng. Ghi đè hàng loạt lên đó là đổi hành vi nghiệp vụ
   chứ không chỉ gắn nhãn phân loại.

Đã nêu với HKLED để họ biết có hai trường nghĩa gần nhau (xem bình luận PM-TASK-00067).

⚠ Patch này phải chạy **sau** `import_danh_muc_vat_tu`: trên site mới, mặt hàng được tạo trước rồi
mới tới đây điền giá trị.
"""

import frappe

from mbwnext_hkled.data.nhap_item import cap_nhat_phuong_phap

FIELDNAME = "custom_replenishment_method"
LABEL = "Phương pháp bổ sung"
# Dòng trống đầu tiên để người dùng bỏ trống được — mặt hàng ngoài phạm vi bảng khách gửi
# chưa có giá trị nào, ép một giá trị mặc định là đoán hộ khách.
OPTIONS = "\nSản xuất\nGia công\nMua hàng"


def _tao_truong():
	if frappe.db.exists("Custom Field", {"dt": "Item", "fieldname": FIELDNAME}):
		return False
	frappe.get_doc(
		{
			"doctype": "Custom Field",
			"dt": "Item",
			"module": "MBWNext HKLed",
			"fieldname": FIELDNAME,
			"label": LABEL,
			"fieldtype": "Select",
			"options": OPTIONS,
			# Ngay dưới Nhóm Mặt Hàng: đây là thông tin phân loại, người dùng cần thấy ngay
			# ở tab Chi tiết chứ không phải lặn vào tab Sản xuất.
			"insert_after": "custom_item_line",
			"in_standard_filter": 1,
			"translatable": 0,
		}
	).insert(ignore_permissions=True)
	return True


def execute():
	moi = _tao_truong()
	frappe.clear_cache(doctype="Item")

	bao_cao = cap_nhat_phuong_phap()

	frappe.db.commit()
	print(
		f"[mbwnext_hkled] Phương pháp bổ sung: {'tạo trường mới' if moi else 'trường đã có'}; "
		f"điền {bao_cao['da_dat']} mặt hàng, giữ nguyên {bao_cao['khong_doi']}, "
		f"bỏ qua {bao_cao['khong_co_tren_site']} mã không có trên site, "
		f"xoá giá trị ở {bao_cao['da_xoa_o_cha']} mặt hàng cha."
	)
