# Chạy lại TC-REGR trên nền erpnext 15.112

> **Vì sao chạy:** mọi kết quả TC-REGR đang có đều đo trên **erpnext 15.73**, mà bản đó
> **không còn tồn tại trên máy nào** — bench nay 15.112, cổng thật 15.95.
> **Nền chạy lại:** cổng 8012 (`cozy_dev` / `hkled.com`) — frappe **15.120.0** · erpnext
> **15.112.0**, đo bằng `bench version` lúc **09/09/2026 09:07**.
> **Cách chạy:** `bench --site hkled.com console`, **chỉ đọc**.

## 🔴 Giới hạn phải đọc trước khi trích kết quả

**Tôi chạy được 21 trong 60 ca TC-REGR, không phải 60/60.**

39 ca còn lại đòi **bấm nút trên giao diện** hoặc **duyệt/huỷ chứng từ thật**. Cổng 8012 là
**dữ liệu thật của khách**, nên tôi không submit, không cancel, không save bất kỳ chứng từ nào.
Ca nào không chạy được thì ghi thẳng là **chưa chạy** — không suy từ "code không đổi" ra "vẫn đạt".

Bù lại, 21 ca chạy được **là đúng nhóm nhạy cảm với nâng nền**: nạp hook, thứ tự hook giữa các
app, và các engine gọi thẳng vào API của erpnext. Đó là chỗ một bản nâng erpnext thật sự có thể
làm gãy. Nhóm không chạy được phần lớn là **khẳng định về dữ liệu của một lần nhập liệu cũ** —
chạy lại chúng trên nền mới gần như không nói lên điều gì về bản nâng.

## Kết quả

### Nhóm A — Nạp hook và thứ tự hook (nhạy nhất với nâng nền)

| File | TC | Đo được | KQ |
|---|---|---|---|
| chan-xuat-kho | TC-REGR-03 | **8/8** chứng từ có `chan_xuat_qua_ton_kha_dung` | ✅ Đạt |
| chan-xuat-kho | TC-REGR-04 | **1** định nghĩa `_kha_dung` duy nhất (`kiem_tra_ton_kho.py`) | ✅ Đạt |
| kiem-tra-ton-kho | TC-REGR-01 | 4 handler `Sales Order.validate`, thứ tự `hkled ×3 → advanced_accounting` — **app kế toán vẫn chạy sau** | ✅ Đạt |
| kiem-tra-ton-kho | TC-REGR-02 | **5** file `sales_order.js` cùng nạp, không đè nhau | ✅ Đạt |
| bac-tho-lich-san-xuat | TC-REGR-01 | `Stock Entry.before_submit`: 3 handler, `advanced_stock` **trước** `hkled ×2` | ✅ Đạt |
| bac-tho-lich-san-xuat | TC-REGR-05 | **5 app** cùng hook Sales Order: `advanced_accounting`, `advanced_selling`, `advanced_stock`, `localization`, `hkled` | ✅ Đạt |

### Nhóm B — Engine còn chạy trên nền mới

| File | TC | Đo được | KQ |
|---|---|---|---|
| kiem-tra-ton-kho | TC-REGR-05 | **31 đơn** `docstatus < 2` chạy `kiem_tra`, **0 lỗi** | ✅ Đạt |
| phan-bo-hang | TC-REGR-03 | `SO-26-00026`: đủ `bang1`/`bang2`/`bang3`, `canh_bao = 0` | ✅ Đạt |
| phan-bo-hang | TC-REGR-04 | `tinh_nhu_cau()` chạy, 3 dòng | ✅ Đạt |
| kiem-tra-ton-kho | TC-REGR-07 | Phần V không bị ảnh hưởng — cùng phép đo trên | ✅ Đạt |
| khai-kho-mac-dinh | TC-REGR-01 | `_kho_mac_dinh` trả đúng kho cho 3/3 mã thử | ✅ Đạt |
| khai-kho-mac-dinh | TC-REGR-02 | `nhu_cau_vat_tu.py` còn truy vấn `custom_ton_kho_kha_dung_toi_thieu` | ✅ Đạt |
| khai-kho-mac-dinh | TC-REGR-03 | 14 DocType riêng, không dựng bảng thay bảng lõi | ✅ Đạt |
| **xuat-bang-gia (mới)** | — | `bang_gia(chi_tinh_duoc=1)`: **tổng 4, trả về 4 dòng**, cả 4 tính ra giá — `Test Gia Công` 20.000→70.000 · `Test NVL 1` 1.000→5.000 · `Test NVL 2` 2.000→5.000 · `Test NVL 3` 3.000→10.000 | ✅ Đạt |

⚠ Ca cuối là ca **tôi thêm**, không có trong bộ cũ — PM-FEAT-00045 là thứ duy nhất **viết sau**
lần nâng erpnext, nên đáng đo nhất. Nó cũng xác nhận bản vá bộ lọc còn đứng: gọi
`bang_gia(gioi_han=50)` **không kèm** `chi_tinh_duoc` ra **0 mã tính được**, gọi
`chi_tinh_duoc=1` ra **4** — đúng như docstring đã cảnh báo, và đúng lý do bộ lọc phải nằm
**trong** truy vấn chứ không áp sau khi cắt.

### Nhóm C — Số liệu

| File | TC | Đo được | KQ |
|---|---|---|---|
| danh-muc-vat-tu | TC-REGR-01 | **62.061** Item (mốc cũ 59.063 mã *"cũ"*) | ✅ Đạt |
| ma-chung-tu | TC-REGR-03 | **9** tiền tố `-26-`, đôi một khác nhau | ✅ Đạt |
| phuong-phap-bo-sung | TC-REGR-01 | 62.061 Item, **0** mã khác `Purchase` | ✅ Đạt |
| danh-muc-lens | TC-REGR-02 | **449** mặt hàng cha, **0** cha mang *Phương pháp bổ sung* | ✅ Đạt |

## Ba chỗ lệch — không chỗ nào do bản nâng erpnext

**① `xuat-bang-gia` TC-REGR-03 — ghi "app 0 patch chờ", thực tế 1.** 🔴 Lệch thật.
Patch chờ là `mbwnext_hkled.patches.them_ty_le_gia_niem_yet` — **patch của chính PM-FEAT-00045**.
Nó chưa từng chạy qua `bench migrate`; hai Custom Field của nó có mặt trên site vì hồi làm tôi
gọi `execute()` **bằng tay**, mà gọi tay thì **không ghi vào `Patch Log`**. Hệ quả cần biết:
- Trên 8012 hiện trạng **đúng** — trường có, Single đã khai 3% / 30%.
- Nhưng dòng test case ghi *"0 patch chờ trước và sau"* **nay sai**, phải sửa.
- Và **PR B bắt buộc `bench migrate`** — chính patch này sẽ chạy lúc đó. Nó **an toàn khi chạy
  lại**: `create_custom_fields(update=True)`, phần khai mặc định có rào `if not …` nên không đè
  số của khách.

**② `danh-muc-vat-tu` TC-REGR-04 — ghi "Item Attribute vẫn 54", đo ra 90.** Không phải hồi quy:
bản ghi mới nhất tạo **24/08/2026**, và **0 bản ghi nào tạo sau 01/09**. Nghĩa là 36 attribute
kia đã có từ trước cả lần nâng erpnext lẫn lần chạy test này — con số 54 là **mốc của thời điểm
đo cũ**, không phải bất biến. Đây là lỗi *ghi một số đo tức thời như thể nó là hằng số*.

**③ `phan-bo-hang` TC-REGR-05 — hình dạng đúng, số đã đổi.** `ghim_boi_don_khac()` vẫn trả cả
thành phẩm lẫn vật tư, `canh_bao = 0`. Nhưng 3/6 con số khác bản ghi 08/09: `NVL 1` 8→**28**,
`NVL 2` 16→**36**, `Bán thành phẩm 1` 1→**6** (`Thành phẩm 1` 31, `NVL 3` 7, `BTP 2` 1 giữ nguyên).
Dữ liệu trên 8012 đã đổi từ hôm qua. ⚠ **Tôi KHÔNG kiểm lại "khớp sổ"** — làm vậy phải dựng lại
sổ ghim thủ công. Nên ca này ghi là **chạy được, chưa nghiệm thu phần khớp sổ**, không ghi Đạt.

## 39 ca chưa chạy

Nhóm phải bấm nút / duyệt chứng từ thật, **không chạy trên dữ liệu thật của khách**:

| File | TC chưa chạy |
|---|---|
| chan-xuat-kho | TC-REGR-01, 02 *(duyệt phiếu xuất)* |
| phan-bo-hang | TC-REGR-01, 02, 06, 07, 08 |
| bac-tho-lich-san-xuat | TC-REGR-02, 03, 04, 06 |
| ghi-chu-san-xuat | TC-REGR-01, 02, 03 |
| bieu-do-gantt | TC-REGR-01, 02 |
| bom-template | TC-REGR-01…05 |
| phan-v | TC-REGR-01, 02, 03 |
| kiem-tra-ton-kho | TC-REGR-03, 04, 06 |
| ma-chung-tu | TC-REGR-01, 02, 04 |
| danh-muc-lens | TC-REGR-01, 03 |
| danh-muc-vat-tu | TC-REGR-02, 03 |
| phuong-phap-bo-sung | TC-REGR-03, 04 |
| xuat-bang-gia | TC-REGR-01, 02 |

Hai ca tôi **đã thử mà phải bỏ vì đo sai câu hỏi**, ghi lại để người sau không lặp:
`phuong-phap-bo-sung` TC-REGR-02 và `bieu-do-gantt` TC-REGR-03 đều là *"fixtures **trước/sau**
tính năng đó có đổi không"*. Đếm tổng số custom field hôm nay (**40**) **không trả lời câu đó** —
nó trả lời *"app hiện có bao nhiêu field"*. Muốn đúng phải so hai commit ôm lấy tính năng.

## Kết luận cho quyết định deploy

**Không tìm thấy hồi quy nào do erpnext 15.112.** Toàn bộ nhóm nhạy cảm với nâng nền — nạp hook,
thứ tự hook giữa 5 app, engine gọi vào API lõi — đều đạt; 31/31 đơn chạy `kiem_tra` không lỗi.

Nhưng nói cho đúng phạm vi: đây là **21 ca chạy bằng lệnh, không phải 60 ca**, và **không ca nào
bấm nút thật**. Bài học `test-toan-ngay-tuong-lai` đã có giá của nó — 20/20 đạt bằng lệnh mà bấm
nút thật hỏng ngay dòng đầu. **Vòng test giao diện của anh Thắng vẫn là thứ không thay thế được.**
