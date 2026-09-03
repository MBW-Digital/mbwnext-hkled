# Copyright (c) 2026, MBWD and contributors
# For license information, please see license.txt

"""Tồn Kho Khả Dụng Tối Thiểu — thêm vào bảng *Mặc định của mặt hàng* (PM-FEAT-00037).

Anh Thắng chốt 03/09/2026: mỗi mặt hàng cần một bảng ghi **Công ty · Kho mặc định · Tồn kho
khả dụng tối thiểu** — *"kho Nguyên vật liệu - A là kho chứa mặc định cho mặt hàng này nếu
thuộc các chứng từ của công ty A. Và tồn kho khả dụng tối thiểu của mặt hàng này ở công ty A
là 500"*.

## KHÔNG dựng bảng mới — lõi đã có sẵn đúng bảng đó

`Item.item_defaults` (bảng con `Item Default`) đã có **`company` + `default_warehouse`**, tức
2 trong 3 cột khách cần. Đo trên site 03/09: **62.055 dòng đã tồn tại**, mỗi mặt hàng một
dòng cho HKLED — chỉ là cột kho đang trống hết.

Nên việc phải làm rút xuống còn **đúng một cột**. Ba lý do không dựng bảng riêng:

1. Khai vào bảng lõi thì **các chức năng sẵn có của ERPNext cũng đọc theo** — mua hàng,
   chuyển kho, sản xuất đều đã biết `default_warehouse`. Bảng riêng thì chỉ app mình đọc.
2. Không đẻ ra **hai chỗ khai kho** để rồi lệch nhau mà không ai biết chỗ nào đúng.
3. Khách khai **một lần**, không phải khai hai bảng nội dung giống nhau.

## ⚠ Ba trường nghĩa gần nhau — đọc kỹ trước khi khai

| Ở đâu | Chi tiết tới đâu | Ai dùng |
|---|---|---|
| **`Item Default.custom_ton_kho_kha_dung_toi_thieu`** (trường này) | theo **công ty** | PM-FEAT-00037 và các tính năng gọi tới nó |
| `Item Reorder.warehouse_reorder_level` (*Mức đặt hàng lại*, lõi) | theo **từng kho** | cơ chế tự sinh Yêu cầu mặt hàng của lõi |
| `Item.custom_ton_kho_toi_thieu` (*Tồn kho tối thiểu*) | **một số cho cả mặt hàng** | PM-FEAT-00030 (Phần V) |

⚠ **Trường thứ ba đã bị chốt của anh Thắng 03/09 làm cho thừa.** Nó ra đời cho Phần V khi
chưa ai nói tới "theo công ty"; giờ cùng nghĩa với trường này nhưng thô hơn một bậc. Đo
03/09: **0 / 62.055 mặt hàng có giá trị**, nên gỡ đi không mất dữ liệu nào.

**Patch này KHÔNG tự gỡ nó.** Nó thuộc một commit của phiên làm việc khác và đang chờ Tuấn
quyết. Ghi ra đây để người gỡ có sẵn căn cứ, và để không ai tưởng hai trường là hai thứ khác
nhau rồi khai cả hai.

## Cố ý KHÔNG điền giá trị

Mức tồn tối thiểu là **quyết định của khách** cho từng mặt hàng. Đoán hộ một con số là đẻ ra
nhu cầu mua ảo trên 62.055 mặt hàng. Để trống = chưa khai.
"""

import frappe

DOCTYPE = "Item Default"
FIELDNAME = "custom_ton_kho_kha_dung_toi_thieu"
LABEL = "Tồn Kho Khả Dụng Tối Thiểu"
# Neo ngay sau Kho mặc định: hai cột này là một cặp, khách khai cùng lúc cho cùng công ty.
INSERT_AFTER = "default_warehouse"
MO_TA = (
	"Mức đệm hàng dùng được tối thiểu của mặt hàng này Ở CÔNG TY TRÊN CÙNG DÒNG. "
	"Khác với Mức đặt hàng lại (Reorder) của hệ thống — cái đó khai theo từng kho. "
	"Để trống nghĩa là chưa khai, không phải bằng 0."
)


def execute():
	if frappe.db.exists("Custom Field", {"dt": DOCTYPE, "fieldname": FIELDNAME}):
		# Giữ nguyên thuộc tính người dùng/fixtures đã chỉnh; patch chỉ lo lần tạo đầu.
		print(f"[mbwnext_hkled] {LABEL}: trường đã có, không tạo lại")
		return

	frappe.get_doc({
		"doctype": "Custom Field",
		"dt": DOCTYPE,
		"module": "MBWNext HKLed",  # để `export-fixtures` gom được
		"fieldname": FIELDNAME,
		"label": LABEL,
		"fieldtype": "Float",
		"insert_after": INSERT_AFTER,
		"description": MO_TA,
		"non_negative": 1,
		# Hiện thẳng trên lưới: bảng này người dùng khai bằng cách gõ vào từng dòng, bắt mở
		# từng dòng ra mới thấy ô thì khai 62.055 mặt hàng là không tưởng.
		#
		# ⚠ Lưới Frappe có TRẦN tổng độ rộng cột (`grid.js::setup_visible_columns`, tổng > 11
		#   thì các cột sau bị bỏ ÂM THẦM). Bảng này đang hiện 3 cột (Công ty, Kho mặc định,
		#   Bảng giá) và CHƯA có bố cục riêng của người dùng, nên còn chỗ. Đã kiểm bằng mắt
		#   trên cổng 8012 sau khi chạy — xem mục 5 của đầu bài.
		"in_list_view": 1,
		"columns": 2,
	}).insert(ignore_permissions=True)

	print(f"[mbwnext_hkled] Đã thêm {LABEL!r} vào bảng Mặc định của mặt hàng. "
	      "Giá trị để TRỐNG — khách phải tự khai.")
