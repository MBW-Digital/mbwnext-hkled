# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tạo sẵn 80 Item Attribute mà bộ nạp danh mục cần (PM-TASK-00126).

**Vấn đề patch này chữa.** `nhap_item._bao_dam_gia_tri()` cố tình `frappe.throw` khi Item
Attribute chưa tồn tại, thay vì tự tạo — thêm một đặc tính là quyết định về mô hình dữ
liệu, không để bộ nạp đoán từ tên cột (một cột gõ sai chính tả sẽ lặng lẽ đẻ ra đặc tính
mới). Guard đó đúng, nhưng chưa ai tạo 77 đặc tính đó bằng patch hay fixture: chúng lên
site `hkled.com` bằng thao tác tay/Data Import từ trước.

Hệ quả trên site cài mới: `import_danh_muc_vat_tu` dừng ngay ở đặc tính đầu tiên và
**vỡ luôn `bench migrate`**. Nghĩa là chuỗi patch nạp danh mục chưa từng chạy được từ số 0,
kể cả trước khi có `import_thanh_pham`.

Danh sách dưới đây là **bản chốt**, dựng từ đúng các cột đặc tính của 30 file
`data/danh_muc/` + 4 file `data/thanh_pham/`, đối chiếu với 77 Item Attribute đang chạy
thật trên `hkled.com` ngày 25/08. Giữ nguyên guard: cột đặc tính mới xuất hiện về sau vẫn
throw, người quyết rồi mới thêm tên vào đây.

Chỉ tạo cái vỏ (đặc tính rỗng, không numeric). Giá trị do bộ nạp điền từ CSV — CSV vẫn là
nguồn duy nhất của giá trị, patch này không nhân đôi nguồn.
"""

import frappe

from mbwnext_hkled.data.nhap_item import (
	COT_CO_DINH,
	DOI_TEN_DAC_TINH,
	DON_VI,
	THU_MUC_NGUON,
	thu_muc_du_lieu,
)

DAC_TINH = (
	"Bề mặt cột",
	"Chip LED",
	"Chiều cao cột",
	"Chóa",
	"Chất liệu",
	"Chỉ số hoàn màu",
	"Công suất",
	"Dung lượng pin",
	"Dài",
	"Dày",
	"Dòng xả cực đại",
	"Dòng điện",
	"Gia công",
	"Góc chiếu",
	"Hiệu suất phát quang",
	"Hình dạng",
	"Hình dạng đầu",
	"Khả năng điều chỉnh công suất",
	"Kiểu khe vặn",
	"Kiểu lắp",
	"Kiểu nguồn",
	"Kiểu ren",
	"Kiểu đấu",
	"Kiểu đấu nối",
	"Kích cỡ",
	"Kích thước",
	"Kích thước LED",
	"Kích thước cần đèn liền",
	"Kích thước khung móng",
	"Kích thước pin",
	"Kích thước ren",
	"Loại LED",
	"Loại cột",
	"Loại pin",
	"Loại tản nhiệt",
	"Model",
	"Màu sơn",
	"Màu ánh sáng",
	# Ba đặc tính Màu dây / Số lõi / Tiết diện do sheet (W) Dây điện mang vào, 26/08/2026.
	# Thiếu chúng thì `_bao_dam_gia_tri` throw và cả lượt nạp danh mục dừng giữa chừng.
	# Chúng KHÔNG xếp liền nhau — mỗi cái nằm đúng vị trí bảng chữ cái của nó.
	"Màu dây",
	"Mạch",
	"Nguồn",
	"Phân loại",
	"Phân loại chao",
	"Phân loại chóa",
	"Phân loại cần đèn",
	"Phân loại gioăng",
	"Phân loại gông/nẹp",
	"Phân loại hộp nguồn",
	"Phân loại kính",
	"Phân loại lens",
	"Phân loại nắp",
	"Phân loại quai",
	"Phân loại tai",
	"Phân loại viền",
	"Phân loại vỏ",
	"Phù hợp với chip LED",
	"Quang thông",
	"Rộng",
	"Số lõi (Số cực)",
	"Số lõi",
	"Số lượng LED",
	"Số mắt LED",
	"Thương hiệu",
	"Tính năng",
	"Tiết diện",
	"Tăng cứng khung móng",
	"Version",
	"Vật liệu",
	"Xuất xứ",
	"Điện áp",
	"Điện áp bảo vệ",
	"Điện áp ra",
	"Điện áp vào",
	"Đường kính cột",
	"Đấu nối",
	"Đầu vào",
	"Đế cột",
	"Độ dài",
	"Độ dày",
	"Độ dày thân cột",
)


def _dac_tinh_trong_file():
	"""Tên đặc tính suy ra từ tiêu đề cột của mọi file nguồn — để đối chiếu với DAC_TINH."""
	import csv
	import os

	can = set()
	for ten_thu_muc in THU_MUC_NGUON:
		thu_muc = thu_muc_du_lieu(ten_thu_muc)
		if not os.path.isdir(thu_muc):
			continue
		for f in sorted(os.listdir(thu_muc)):
			if not f.endswith(".csv"):
				continue
			with open(os.path.join(thu_muc, f), encoding="utf-8") as fh:
				cot = next(csv.reader(fh), [])
			for c in cot:
				c = (c or "").strip()
				if c and c not in COT_CO_DINH:
					can.add(DOI_TEN_DAC_TINH.get(c, c))
	return can


def _kiem_tien_de():
	"""Chặn sớm nếu app lõi chưa cài xong — đây là patch đầu của chuỗi nạp danh mục.

	`_tao_item()` đặt `stock_uom = "Cái"` cho mọi mặt hàng, mà UOM đó do
	`mbwnext_localization` tạo trong `after_install`, không phải hàng có sẵn của ERPNext.
	Cài `mbwnext_hkled` lên site chưa có `mbwnext_localization` thì 62.000 mặt hàng vỡ ở
	`LinkValidationError: Could not find Default Unit of Measure: Cái` — đọc traceback đó
	rất khó suy ra nguyên nhân là thiếu app. Báo thẳng ở đây.
	"""
	if not frappe.db.exists("UOM", DON_VI):
		frappe.throw(
			f"Chưa có UOM {DON_VI!r} trên site. Cài `mbwnext_localization` TRƯỚC "
			f"`mbwnext_hkled` (UOM do `after_install` của app đó tạo), rồi chạy lại `bench migrate`."
		)


def execute():
	_kiem_tien_de()

	da_tao = []
	for ten in DAC_TINH:
		if frappe.db.exists("Item Attribute", ten):
			continue
		doc = frappe.new_doc("Item Attribute")
		doc.attribute_name = ten
		doc.numeric_values = 0
		doc.insert(ignore_permissions=True)
		da_tao.append(ten)
	frappe.db.commit()

	print(f"[mbwnext_hkled] Item Attribute: tạo mới {len(da_tao)}, đã có sẵn {len(DAC_TINH) - len(da_tao)}.")

	# Cột đặc tính có trong file nhưng chưa nằm trong DAC_TINH: bộ nạp sẽ throw ở đó và làm
	# vỡ `bench migrate`. Báo ngay tại đây để thấy nguyên nhân, thay vì đọc traceback ở patch sau.
	thieu = sorted(_dac_tinh_trong_file() - set(DAC_TINH))
	if thieu:
		print(
			f"[mbwnext_hkled] ⚠ {len(thieu)} cột đặc tính trong file nguồn CHƯA khai trong "
			f"DAC_TINH của patch này — patch nạp danh mục sẽ dừng ở đó: {', '.join(thieu)}"
		)
