# Quy trình cài `mbwnext_hkled` lên site thật

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Người triển khai (không phải người dùng cuối)
> **Cập nhật:** 2026-09-08
> **Mục đích:** Cài app lên `hkled.mbwnext.com` mà không xoá mất dữ liệu và không để lại một
> site "cài xong nhưng rỗng".

---

## 0. Đọc trước — hai cách hỏng của quy trình này

Cả hai đều **im lặng**: lệnh chạy xong, báo thành công, không có câu lỗi nào.

| Cách hỏng | Triệu chứng | Chặn ở bước |
|---|---|---|
| **Xoá mất dữ liệu đang có** | `Item Group` tụt còn 8, mọi mặt hàng trỏ vào nhóm không tồn tại | Bước 2 |
| **Cài xong mà rỗng** | 0 mặt hàng, 0 BOM Template, không có Server Script tính định mức | Bước 5 |

Cách hỏng thứ hai có nguyên nhân trong lõi Frappe: `install_app()` gọi
`set_all_patches_as_completed(app)` **trước** mọi hook — mọi dòng trong `patches.txt` bị ghi
thẳng vào `Patch Log` mà **không chạy**. App đã có `after_sync` để bù, nhưng chỉ đúng khi cài
theo thứ tự ở Bước 4.

---

## 1. Sao lưu — không bỏ qua

```bash
bench --site hkled.mbwnext.com backup --with-files
```

Ghi lại đường dẫn file backup trước khi sang bước sau. Mọi bước dưới đây đều có thể lùi bằng
chính file này; không có nó thì không có đường lùi.

---

## 2. ☢️ Kiểm chặn xoá dữ liệu — bước nguy hiểm nhất

**Chạy đúng một lệnh này trước khi gõ bất cứ lệnh `install-app` nào:**

```bash
bench --site hkled.mbwnext.com list-apps | grep localization
```

| Kết quả | Làm gì |
|---|---|
| **Có** `mbwnext_localization` | An toàn, đi tiếp Bước 3 |
| **Không có**, và site **chưa có dữ liệu** | An toàn, đi tiếp |
| **Không có**, và site **đã có dữ liệu** | 🔴 **DỪNG.** Hỏi người phụ trách trước |

### Vì sao

`hooks.py` khai `required_apps`, nên `bench install-app mbwnext_hkled` trên site thiếu
`mbwnext_localization` sẽ khiến Frappe **tự cài nó trước**. `after_install` của app đó chạy
`del_masterdataCore()` — `frappe.db.sql("DELETE FROM tab<doctype>")`, SQL thẳng, **không kiểm
liên kết, không hỏi** — cho:

```
Item Group · UOM · UOM Conversion · Territory · Stock Entry Type · Province · Commune
```

Site trắng thì đó đúng là việc cần làm. Site đã có dữ liệu thì mất sạch phân nhóm danh mục.

**Đã dính thật** trên `test.com` ngày 26/08/2026: `Item Group` 50 → 8, và 61.835/61.836 mặt
hàng trỏ vào nhóm không còn tồn tại. Mặt hàng thì còn — `tabItem.item_group` giữ nguyên chuỗi
tên, nên dựng lại bản ghi nhóm là liên kết tự nối.

⚠ **App này không tự chặn được.** Chỗ xoá nằm ở lượt gọi *trong* (`install_app` đệ quy sang
`mbwnext_localization`), mà hook sớm nhất của app khách chạy sau đó. Đã đo 26/08: chặn được
bằng một app **khác** đã nằm sẵn trên site khai `before_app_install` — hook bắn, throw, và
`Item Group` giữ nguyên 101. Nhưng đúng cảnh nguy hiểm nhất (site mới tinh chỉ có erpnext) thì
chưa app nào ôm hook đó. **Nên lệnh kiểm ở đầu mục này là lớp bảo vệ duy nhất đang thực sự tồn
tại.**

---

## 3. Kiểm nền tảng

```bash
bench --site hkled.mbwnext.com list-apps
```

Đối chiếu với bench thử nghiệm `cozy_dev`. Ba chỗ đã biết là **lệch**, ghi lại trước khi cài để
sau này không chẩn đoán nhầm:

| | `cozy_dev` (nơi test) | `hkled.mbwnext.com` (thật) |
|---|---|---|
| frappe / erpnext | 15.77.0 / 15.73.1 | 15.101.0 / 15.95.1 |
| Viết tắt công ty | `HKL` | `HKLED` |
| `auto_reserve_stock_for_sales_order_on_purchase` | 1 | 0 |

*(Số của site thật do phiên `HKLed 3` đo ngày 08/09/2026, chưa kiểm lại sau ngày đó.)*

**Hệ quả cần biết, không phải việc phải sửa:**

- **Viết tắt công ty** không ảnh hưởng code. Đã grep toàn bộ `.py`/`.js`: chỉ 3 chỗ chứa chuỗi
  `- HKL` và **cả 3 là chú thích cảnh báo đừng gõ cứng**. Bộ lọc kho khớp theo `warehouse_name`
  — trường này không mang hậu tố công ty. Chỉ **tài liệu** có ghi tên kho đầy đủ, và tài liệu
  thì không chạy.
- **Chênh phiên bản hơn 20 bản minor.** Bộ test hiện có chạy trên 15.77; "đạt ở cozy_dev" không
  còn là bằng chứng đủ cho site thật. Chạy lại ít nhất bộ TC-REGR sau khi cài.
- **`auto_reserve_stock_for_sales_order_on_purchase`** là cơ chế giữ chỗ của ERPNext lõi, chạy
  song song với cơ chế ghim riêng của HKLED. Spec Phần IV chốt 25/08 viết trong bối cảnh nó
  đang **bật**. Trên site thật nó đang **tắt** — cần chốt bật hay không **trước** khi nghiệm thu
  Phần IV, vì số ra sẽ khác.

---

## 4. Thứ tự cài app — bắt buộc, không phải quy ước cho đẹp

```
1. erpnext
2. hrms · print_designer                (độc lập, đâu cũng được)
3. mbwnext_localization                 ⚠ PHẢI TRƯỚC MỌI APP MBWNEXT KHÁC
4. mbwnext_advanced_selling
5. mbwnext_advanced_buying · _stock · _accounting · _distribution_map
6. super_admin
7. mbwnext_hkled                        ⚠ APP KHÁCH, CUỐI CÙNG
```

Hai ràng buộc đo được, cả hai vấp thật ngày 25–26/08/2026:

**(a) `mbwnext_localization` phải đứng trước** — lý do ở Bước 2. Nó còn tạo UOM `Cái`; thiếu
thì mọi lệnh tạo mặt hàng vỡ ở *"Could not find Default Unit of Measure: Cái"*.

**(b) `mbwnext_advanced_selling` phải đứng trước app khách** — nó thêm Custom Field cho `Item`.
Cài sau khi app khách đã nạp 62 nghìn mặt hàng thì các cột đó **rỗng toàn bộ**, và không có
cảnh báo nào.

Ba app lõi còn lại không chạm `Item` nên đứng sau vô hại — nhưng đừng dựa vào điều đó, cứ theo
đúng thứ tự trên.

```bash
bench --site hkled.mbwnext.com install-app mbwnext_hkled
```

---

## 5. Kiểm ngay sau khi cài — trước khi làm bất cứ việc gì khác

Đây là bước bắt cách hỏng thứ hai. **Bảy chỉ số phải khớp**, chạy trong `bench console`:

```python
import frappe
print("Item                :", frappe.db.count("Item"))
print("Item Attribute      :", frappe.db.count("Item Attribute"))
print("BOM Template        :", frappe.db.count("BOM Template"))
print("BOM Rule            :", frappe.db.count("BOM Rule"))
print("DocType cua app     :", len(frappe.get_all("DocType", filters={"module": "MBWNext HKLed"})))
print("Custom Field cua app:", frappe.db.count("Custom Field", {"module": "MBWNext HKLed"}))
print("Server Script       :", frappe.db.exists("Server Script", "hkled_resolve_bom_qty"))
print("Bang ghim ton tai   :", frappe.db.table_exists("HKLed Pinned Material"))
```

| Chỉ số | Phải ra | Ra sai nghĩa là |
|---|---|---|
| `Item` | **≈ 62.010** | `after_sync` không chạy — xem mục 0, cách hỏng thứ hai |
| `Item Attribute` | **90** | thiếu `seed_item_attribute` |
| `BOM Template` | **7** | patch nạp danh mục chạy **sau** `import_bom_template` |
| `BOM Rule` | **737** | như trên |
| `DocType cua app` | **13** | ra **12** là thiếu `HKLed Pinned Material` — xem mục 6 |
| `Custom Field cua app` | **40** | fixtures chưa đồng bộ |
| `Server Script` | có | engine BOM sẽ không chạy nếu thiếu |
| `Bang ghim ton tai` | **True** | như dòng `DocType` — xem mục 6 |

⚠ **Ba con số cố ý khác `cozy_dev`.** Cổng 8012 hiện đếm `Item` **62.061**, `BOM Template` **8**,
`BOM Rule` **738** — nhiều hơn vì có bản ghi tạo tay tích tụ từ tháng 8. Con số trong bảng trên là
số **bộ nạp dựng ra từ số 0**, đo ngày 26/08/2026. Site mới ra đúng bằng bảng là đạt.

⚠ **`BOM Template` ra 7 là ĐÚNG.** Trên `cozy_dev` con số là 8, nhưng cái thứ 8 tên
`thành phẩm 1` là bản ai đó tạo tay ngày 03/08 để thử giao diện, **không nằm trong
`spec.json`** nên sẽ không bao giờ được dựng lại. Đừng đi tìm nó.

### Nếu `Item` ra 0

Đó là cách hỏng thứ hai. Nguyên nhân gần như chắc chắn là **thứ tự cài app** (Bước 4) hoặc
`after_sync` không chạy. **Đừng chữa bằng `bench migrate`** — trên site vừa cài, mọi patch đã
bị đánh dấu xong nên migrate không dựng lại gì cả. Gọi thẳng:

```python
from mbwnext_hkled.install import after_sync
after_sync()
```

---

## 6. Bẫy đã biết: bảng Ghim Vật Tư

Nếu Bước 5 đếm ra **12** DocType thay vì 13, site sẽ **vỡ ngay lúc lưu Đơn Bán Hàng đầu tiên**:

```
ImportError: Module import failed for HKLed Pinned Material, the DocType you're trying to
open might be deleted.
Error: No module named 'frappe.core.doctype.hkled_pinned_material'
```

🔴 **Chữ `frappe.core` trong câu lỗi KHÔNG có nghĩa là lỗi nằm ở app lõi.** Đó là đường dẫn
Frappe suy ra khi không tìm thấy doctype ở đâu cả. Chi tiết và cách chữa: xem mục *"Dựng site
MỚI: câu lỗi chỉ sai chỗ"* trong
[phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve-cau-hinh.md](phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve-cau-hinh.md).

---

## 7. Dựng dữ liệu tổ chức — phần app không tự dựng được

App dựng **danh mục vật tư và BOM**. Nó **không** dựng phần tổ chức. Phải khai tay hoặc nạp
riêng:

| Cần khai | Vì sao |
|---|---|
| **Company** | mọi phép tính tồn đều lọc theo công ty |
| **Cây kho**, gồm hai nhóm tên **chính xác** `Nhóm kho lỗi` và `Nhóm kho trung chuyển` | hai tên này là **một phần của logic**, không phải nhãn — xem dưới |
| Khách hàng · Nhà cung cấp · Nhân sự · Đội Sản Xuất · Bậc Thợ | các tính năng sản xuất đọc từ đây |

🔴 **Tên hai nhóm kho là logic.** `api/kiem_tra_ton_kho.NHOM_KHO_LOAI` loại mọi kho nằm dưới hai
nhóm đó khỏi tồn khả dụng, khớp theo đúng chuỗi `warehouse_name`. Đặt tên lệch một chữ thì toàn
bộ phép tính tồn khả dụng, ghim và phân bổ ra **số khác — mà không có lỗi nào**, chỉ là số
khác. Đây là nguyên nhân số một của câu hỏi *"hàng về rồi sao không chia được"*.

⚠ Bản kho mặc định của `mbwnext_localization` sinh ra 15 kho **khác hẳn** (Kho Hà Nội / Đà Nẵng
/ HCM, **không** có tầng `Nhóm kho …`). Đừng tưởng nó giống cấu trúc đang chạy ở `cozy_dev`.

---

## 8. Nghiệm thu trước khi giao khách

```python
from mbwnext_hkled.api.ghim_vat_tu import kiem_bat_bien
print("SẠCH" if not kiem_bat_bien() else kiem_bat_bien())
```

Rồi kiểm bằng mắt: mở một Đơn Bán đã duyệt có tích **Ghim Tồn Khả Dụng** → bảng **Ghim Vật Tư**
phải có dòng; mở một Phiếu nhập mua đã duyệt → phải thấy nút **Phân Bổ**; phiếu còn nháp thì
**không** được có nút đó.

Và chạy lại bộ **TC-REGR** của các tính năng đã nghiệm thu — vì nền tảng lệch hơn 20 bản minor
so với nơi đã test (Bước 3).

---

## 9. Nếu phải lùi

```bash
bench --site hkled.mbwnext.com restore <đường dẫn backup ở Bước 1>
```

Gỡ app bằng `bench uninstall-app` **không** trả lại dữ liệu đã bị `del_masterdataCore()` xoá —
lệnh đó xoá bằng SQL thẳng, không có bản ghi nào để hoàn tác. Đường lùi duy nhất là bản sao lưu.
