# Xuất bảng giá niêm yết

> **Khách hàng:** HKLED
> **App:** `mbwnext_hkled` (tầng 4 — chỉ khách này dùng)
> **PM Project:** `PM-PRJ-00003` · **PM Feature:** `PM-FEAT-00045`
> **Trạng thái:** Analysis — đặc tả đã rõ, **chặn ở dữ liệu đầu vào**, xem mục 4b
> **Ngày lập:** 2026-09-08

⚠ Tên trên PM đang là *"Phần IV.3 - Tạo bảng giá niêm yết"*. Đề nghị đổi thành **Xuất bảng giá
niêm yết**: bỏ số Phần (thông tin quản lý dự án, không thuộc tên tính năng), và động từ *xuất*
đúng với chữ khách dùng — *"chỉ cần xuất ra giá niêm yết là được"*.

---

## 1. Nguồn — nguyên văn, chưa diễn giải

Anh Thắng đăng lên `PM-FEAT-00045` lúc **08/09/2026 14:11**, gồm **hai ảnh chụp chat với khách,
không kèm chữ nào**. Ảnh lưu tại `anh/bang-gia-niem-yet-chat-khach-01.png` và `...-02.png`.

**Đây là bản gốc duy nhất.** Mọi thứ từ mục 2 trở xuống là *cách tôi hiểu*, không phải lời khách.

### 1.1 Ảnh 1 — file bảng giá khách đang dùng

Khách (`Kd Hkled 0768734666`) gửi ảnh chụp một file Excel đang dùng thật:

> **BẢNG BÁO GIÁ ĐÈN LED PHA MODULE LED 3030**
> *(Bảng giá có giá trị đến khi nhà máy HKLED cập nhật giá mới)*
> Header: **CHIẾT KHẤU (ĐÃ VAT: 8%): 68%**

Các cột trong file:

| TT | HÌNH ẢNH | MÔ TẢ SẢN PHẨM | CẤU HÌNH SẢN XUẤT | MÃ THUỘC TÍNH (SKU) | LED 3030 NIÊM YẾT | LED 3030 GIÁ BÁN | BẢO HÀNH | KHO |
|---|---|---|---|---|---|---|---|---|

Dòng nhóm: *ĐÈN LED PHA P01 SMD 50W (Khung xám) / (Khung đen) - Chipled 3030*.

Vài dòng dữ liệu thật đọc được trên ảnh:

| Cấu hình sản xuất | SKU | Niêm yết | Giá bán | Bảo hành | Kho |
|---|---|---|---|---|---|
| Chip Bridgelux + Driver HKLED nhỏ | `DP01S050-B3HN-B` | 880.000 | 282.000 | 03 năm | SLL |
| Chip Lumileds + Driver HKLED nhỏ | `DP01S050-L3HN-B` | 935.000 | 299.000 | 03 năm | SLL |
| Chip Lumileds + Driver HKLED DIM 1 CẤP | `DP01S050-L3HT-B` | 1.133.000 | *(che)* | 03 năm | SLL |
| Chip Lumileds + Driver HKLED DIM 5 CẤP | `DP01S050-L3HD-B` | 1.342.000 | 429.000 | 03 năm | SLL |
| Chip Bridgelux + Driver DONE nhỏ | `DP01S050-B3DN-B` | 902.000 | 289.000 | 02 năm | SLL |
| Chip Lumileds + Driver DONE nhỏ | `DP01S050-L3DN-B` | 957.000 | 306.000 | 02 năm | SLL |
| Chip Lumileds + Driver DONE DIM 1 CẤP | `DP01S050-L3DT-B` | 1.243.000 | 398.000 | 03 năm | SLL |
| Chip Lumileds + Driver PHILIPS DIM 1 CẤP | `DP01S050-P3PT-B` | 1.980.000 | 634.000 | 03 năm | SLL |
| Chip Lumileds + Driver PHILIPS DIM 10 CẤP | `DP01S050-P3PD-B` | 2.233.000 | 715.000 | 03 năm | SLL |
| Chip Lumileds + Driver INVENTRONIC 5 CẤP | `DP01S050-P3ID-B` | 1.793.000 | 574.000 | 03 năm | SLL |

Kèm khối mô tả sản phẩm bên trái:

> - TÊN SP: ĐÈN LED PHA 50W
> - Mã sản phẩm: `DP01S050-B`
> - Sử dụng: MODULE 50W (64LED) NHÔM ĐÚC SMD 3030
> - Kích thước SP: 85\*305\*120mm
> - Kích thước hộp: 240\*360\*185mm
> - Số lượng SP/thùng: 2

**Câu khách viết dưới ảnh (11:22):**

> *"cột giá bán trên file sẽ thay đổi theo tỷ lệ chiết khấu*
> *nên chỉ cần xuất ra giá niêm yết là được"*

### 1.2 Ảnh 2 — phần chat tiếp theo

> **Thắng (11:22):** *"vậy là mình xuất ra giá niêm yết, còn chỗ chiết khấu kia anh tự điền đúng ko ạ"*
>
> **Khách:** *"đúng rồi, tùy đối tượng khách hàng thì bên mình sẽ tự điều chỉnh và gửi bảng giá với
> mức chiết khấu khác nhau"*
>
> **Thắng:** *"vậy là con số ở bảng giá niêm yết thì nó luôn đúng realtime, nhưng mình có cập nhật
> về giá niêm yết…"* (câu bị cắt trong ảnh)
>
> **Khách (11:29):** *"đúng rồi, với những mặt hàng được chọn thì mới cập nhật lại*
> *tuy nhiên với các đơn hàng đã phát sinh nếu thay đổi thì sẽ ảnh hưởng tới phần tính hoa hồng
> trên các đơn cũ trước có 1 buổi họp đang có phương án là trên đơn hàng bán sẽ có thêm 1 cột đơn
> giá nữa trên đơn hàng bán mà kinh doanh có thể sửa được ấy, nếu theo phương án đó và hoa hồng
> tính theo trường đơn giá có thể sửa thì nếu giá niêm yết có cập nhật lại cũng sẽ không bị ảnh
> hưởng"*

### 1.3 Một nguồn khác, nói khác

Sheet *Tổng Hợp Hiện Trạng HKLED Giai Đoạn I*, dòng 14, mô tả cùng hạng mục này là:

> *"Thiết kế bảng giá dựa theo các chỉ số như hao hụt, RND,…(phát sinh mới)"*

➜ Ban đầu tôi tưởng hai nguồn **mâu thuẫn**. Không phải: chúng nói về **hai bước** của cùng
một việc — tính giá (mục 6.3), rồi xuất bảng (mục 6.4). Xem mục 6.

---

## 2. Hiểu của tôi — tính năng này dùng để làm gì

HKLED gửi báo giá cho đại lý bằng một file Excel dựng tay. File có hai cột giá: **niêm yết**
(giá gốc, chung cho mọi khách) và **giá bán** (= niêm yết × tỷ lệ chiết khấu, khác nhau theo
từng đối tượng khách).

Khách **không cần hệ thống tính cột giá bán** — họ tự điền tỷ lệ chiết khấu vào file rồi Excel
tự nhân ra. Thứ hệ thống phải làm là **tự tính giá niêm yết** từ giá vốn và bốn tỷ lệ (mục 6.3),
rồi **xuất ra bảng** luôn khớp dữ liệu hiện tại — để khỏi phải dò tay mỗi lần nhà máy đổi giá.

**Ví dụ tình huống:** kinh doanh cần gửi báo giá cho một đại lý mới. Hôm nay họ mở file Excel cũ,
không chắc giá đã cũ chưa, phải hỏi lại nhà máy. Sau khi có tính năng: bấm xuất, được bảng giá
niêm yết đúng tại thời điểm xuất, điền tỷ lệ chiết khấu của đại lý đó rồi gửi đi.

---

## 3. 5W — trả lời được tới đâu

| | Trả lời | Nguồn |
|---|---|---|
| **WHAT** | Màn hình **tự tính** giá niêm yết từ giá vốn + 4 tỷ lệ; xem trên bảng, xuất Excel, và cập nhật sang phần bán hàng khi có người bấm | `notes` của PM Feature |
| **WHEN** | Bảng tính lại theo dữ liệu hiện tại. Xuất và cập nhật thì **người dùng bấm nút** — cố ý không tự động | `notes`: *"không được tự ý cập nhật"* |
| **WHO** | Kinh doanh (gửi báo giá cho đại lý) | ⚠ **vẫn chưa hỏi** — mới suy từ ngữ cảnh |
| **WHERE** | Màn hình riêng của app, **không** dùng Price List của ERPNext | Anh Thắng 15:36 |
| **ERROR** | Mặt hàng không tính được giá (thiếu cost) thì hiện gì? | ⚠ **chưa hỏi** — và với dữ liệu hiện tại đây là **đa số**, xem mục 4b |

---

## 4. Đo hiện trạng trên hệ thống — 08/09/2026, cổng 8012

🔴 **Chỗ chặn lớn nhất: dữ liệu giá gần như không tồn tại.**

| Bảng giá | Bán | Mua | Số Item Price |
|---|---|---|---|
| `Standard Selling` | ✔ | | **11** |
| `Standard Buying` | | ✔ | **9** |

**Tổng 20 dòng giá cho 62.061 mặt hàng.** Và **không có** bảng giá nào tên *niêm yết*.

Rà Custom Field toàn site: **không có** trường nào cho *hao hụt*, *RND*, *giá niêm yết*,
*chiết khấu*. Trường sẵn có dùng được:

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `Item.standard_rate` | Currency | *Standard Selling Rate* — ứng viên cho giá niêm yết |
| `Item.valuation_rate` | Currency | giá vốn |
| `Item.last_purchase_rate` | Float | giá mua gần nhất |
| `Item.warranty_period` | Data | số ngày bảo hành — cột **BẢO HÀNH** của file lấy từ đây được, nhưng file ghi *"03 năm"* chứ không ghi số ngày |

**Hệ quả:** không có bảng giá nào dùng lại được, nên giá niêm yết phải **tính ra** chứ không
phải đọc lên — đúng như đặc tả ở mục 6.3. Còn cost để tính thì cũng gần như chưa có: xem mục 4b.

### Cột nào lấy được, cột nào chưa

| Cột trong file khách | Lấy từ đâu | Được chưa |
|---|---|---|
| MÃ THUỘC TÍNH (SKU) | `Item.name` của biến thể | ✔ có sẵn |
| MÔ TẢ SẢN PHẨM | `Item.description` / mặt hàng cha | ✔ có sẵn, cần chốt lấy trường nào |
| CẤU HÌNH SẢN XUẤT | tổ hợp đặc tính biến thể (Chip LED, Driver…) | ✔ dựng được từ `Item Variant Attribute` |
| HÌNH ẢNH | `Item.image` | ⚠ chưa đo có bao nhiêu mặt hàng có ảnh |
| BẢO HÀNH | `Item.warranty_period` | ⚠ đơn vị lệch (ngày vs "03 năm") |
| KHO | ? — file ghi `SLL` | ❌ **chưa biết `SLL` nghĩa là gì** |
| **NIÊM YẾT** | tính theo công thức mục 6.3 | ⚠ công thức rõ, **thiếu cost đầu vào** — mục 4b |
| GIÁ BÁN | — | ✔ **không cần**, khách tự tính |

---

## 5. Tầng và app — chốt tầng 4

`mbwnext_hkled`. Lý do **mạnh hơn tôi tưởng lúc đầu**: ban đầu tôi xếp tầng 4 chỉ vì *bố cục file
là mẫu riêng của HKLED*. Sau khi anh Thắng nói rõ 15:36 (*"đang tạo ra 1 chức năng mới, không phải
dùng chức năng bảng giá có sẵn"*), lý do thành ra: **cả cơ chế tính giá là riêng** — bốn tỷ lệ ở
hai cấp, công thức chia theo tỷ lệ niêm yết, và luật không-tự-động-cập-nhật. Không có phần nào
dùng lại `Price List` của ERPNext.

⚠ Chưa tra va chạm hook vì chưa biết sẽ hook vào DocType nào — làm ở Giai đoạn 3, sau khi có
câu trả lời cho mục 6.

---

## 6. Đặc tả — anh Thắng bổ sung 08/09 15:36 và trường `notes` của PM Feature

Câu hỏi 1 của tôi (*"xuất ra"* hay *"tính ra"*) đặt sai vế: **không phải chọn một, mà là cả hai
nối tiếp nhau**. Hệ thống **tính** giá niêm yết, rồi mới **xuất** bảng cho đại lý. Hai nguồn ở
mục 1.3 nói về hai bước khác nhau của cùng một việc, không mâu thuẫn.

> *"Bản chất ở đây là mình đang tạo ra 1 chức năng mới em nhé, không phải là dùng chức năng bảng
> giá có sẵn của phần mềm"* — 15:36

Nghĩa là **không** dùng `Price List` / `Item Price` của ERPNext làm màn hình. Mockup khách gửi:
[Google Sheet *Tính giá*](https://docs.google.com/spreadsheets/d/1s-Dv0D2ASYD5Farv_7VHP4WbxQiZPxgQuN62IBOCgM0/edit).

### 6.1 Hai phần

**Phần 1 — nơi khai tỷ lệ.** Bốn tỷ lệ, ở **hai cấp khác nhau**:

| Tỷ lệ | Khai ở đâu |
|---|---|
| Tỷ lệ **hao phí** | chung toàn hệ thống |
| Tỷ lệ **tính giá niêm yết** | chung toàn hệ thống |
| Tỷ lệ chi phí **R&D** | **trên từng mặt hàng** |
| Tỷ lệ **lợi nhuận** | **trên từng mặt hàng** |

**Phần 2 — bảng giá niêm yết**, hiển thị giá đã tính của mọi mặt hàng.

### 6.2 Cost lấy ở đâu — theo Phương pháp bổ sung

> *"nếu item mua hàng thì cost sẽ dựa trên giá của đơn mua gần nhất của item này, nếu item sản
> xuất hoặc gia công thì cost sẽ dựa trên cost của BOM mặc định"*

Đây là câu trả lời cho *"giá trị tồn kho"* ở mockup: **không phải giá vốn tồn kho**, mà là giá đơn
mua gần nhất hoặc cost của BOM. App đã có sẵn trường `Phương pháp bổ sung` (PM-TASK-00067) để rẽ
nhánh.

### 6.3 Công thức — nguyên văn của anh Thắng

```
giá niêm yết = Làm tròn đến 5000 của
               [ (cost × (100 + tỷ lệ hao phí + R&D + lợi nhuận) / 100) / tỷ lệ tính giá niêm yết × 100 ]
```

Ví dụ của anh: cost 50.000 · hao phí 3 · niêm yết 30 · R&D 5 · lợi nhuận 10
➜ `(50.000 × 118/100) / 30 × 100 = 196.667` ➜ **195.000**.
Và *"ví dụ mà tính ra 197800 thì sẽ làm tròn lên 200000"*.

✔ **Đã đối chiếu độc lập với số trong mockup, khớp tuyệt đối:**

| | Dòng 1 | Dòng 2 |
|---|---|---|
| Giá thành (cost) | 739.300 | 749.300 |
| × 1,18 (3+5+10) | **872.374** | **884.174** |
| ÷ 30 × 100 | 2.907.913 | 2.947.247 |
| Làm tròn 5.000 | **2.910.000** | **2.945.000** |

Cả hai khớp con số in trong file. Và quy tắc làm tròn là **tới bội 5.000 gần nhất** — không phải
làm tròn lên: 2.947.247 ra 2.945.000 chứ không phải 2.950.000. Ví dụ *"197800 → 200000"* của anh
Thắng cũng là gần nhất, không phải lên.

⚠ **Ba tỷ lệ cộng vào tử số, còn tỷ lệ niêm yết thì CHIA.** Giá vốn + lãi chỉ chiếm 30% giá niêm
yết. Điều này khớp với file báo giá ở mục 1.1: chiết khấu 68% ⇒ giá bán = 32% niêm yết
(282.000/880.000 = 32,05%). **Hai file khách gửi độc lập nhau mà ăn khớp** — dấu hiệu đọc đúng.

### 6.4 Ba tính năng

1. **Xem** — bảng hiển thị giá niêm yết, luôn cập nhật theo dữ liệu hiện tại.
2. **Xuất Excel** — tick chọn dòng ➜ bấm xuất ➜ file có giá niêm yết, và **một ô tỷ lệ chiết khấu
   để người dùng tự điền, Excel tự tính ra giá bán**. Tức file phải mang **công thức sống**, không
   phải số chết.
3. **Cập nhật giá niêm yết cho từng mặt hàng** — 🔴 **KHÔNG tự động**:

   > *"Giá niêm yết ở bảng này sẽ không được phép tự động cập nhật sang phần bán hàng… người dùng
   > tích chọn item đó trên bảng rồi ấn nút cập nhật giá niêm yết thì nó mới cập nhật qua cho
   > sales nhìn thấy, không được tự ý cập nhật"*

   Đây chính là cách giải quyết mối lo về hoa hồng ở mục 1.2: đổi tỷ lệ thì bảng đổi, nhưng giá
   sales nhìn thấy chỉ đổi khi có người bấm.

### 6.5 Phạm vi đợt 1 — anh Thắng thu hẹp

> *"tạm thời phần xuất file em chưa cần phải xuất được như bản của họ chụp ảnh, mà chỉ cần xuất
> được cho anh 2 trường chính là mã mặt hàng và giá niêm yết trước đã"*

Đợt 1: **2 cột**. Hình ảnh, mô tả, cấu hình sản xuất, bảo hành, kho — để sau.

---

## 4b. 🔴 CHẶN — công thức chạy được, nhưng gần như không có dữ liệu để chạy

Đo trên cổng 8012 ngày 08/09/2026, 16:1x.

**Phương pháp bổ sung** đã khai gần đủ:

| | Số mặt hàng |
|---|---|
| Sản xuất | 59.747 |
| Mua hàng | 1.828 |
| Gia công | 2 |
| *(chưa khai)* | 484 |

Nhưng **cả hai nhánh lấy cost đều rỗng**:

| Nhánh | Cần gì | Thực tế có |
|---|---|---|
| **Mua hàng** (1.828 mã) | giá đơn mua gần nhất | **3 mã** có `last_purchase_rate` > 0; chỉ **5 mã** từng xuất hiện trên đơn mua đã duyệt |
| **Sản xuất / Gia công** (59.749 mã) | cost của BOM mặc định | **12 BOM** mặc định đang hoạt động, trong đó **1 BOM** có `total_cost` > 0 |

➜ **Tính được giá niêm yết cho khoảng 4 trên 62.061 mặt hàng.**

Đây **không phải lỗi thiết kế và cũng không phải việc code sửa được** — nó là dữ liệu nghiệp vụ
khách phải nạp. Nhưng phải nói ra trước khi dựng màn hình, vì dựng xong mà bảng trống 99,99% thì
trông y hệt tính năng hỏng.

⚠ Lưu ý riêng nhánh sản xuất: app **cố ý không tự tạo BOM** (chốt 25/08 — *"Ghim không nên tạo
BOM, chỉ đọc thành phần từ template"*). Có 7 BOM Template và 737 rule, nhưng BOM **thật** trên
site chỉ 13. Muốn 59.747 mặt hàng có cost thì phải sinh BOM thật cho chúng — đó là một khối lượng
riêng, không nằm trong tính năng này.

---

## 7. Còn phải hỏi — năm câu

**Câu 1 🔴 — Ai nạp dữ liệu giá đầu vào, và bao giờ?**
Xem mục 4b. Nếu chưa có thì đợt 1 nên làm gì: dựng màn hình để sẵn (chấp nhận bảng gần như trống),
hay chờ dữ liệu?

**Câu 2 — "Cập nhật sang cho sales nhìn thấy" là ghi vào đâu?**
Ô *Standard Selling Rate* trên mặt hàng, hay một `Item Price` trong một bảng giá cụ thể? Câu này
quyết định chỗ sales đọc giá, nên phải chốt trước khi code.

**Câu 3 — Hai tỷ lệ cấp hệ thống đặt ở đâu?**
`MBWNext System Setting` là của app lõi dùng chung nhiều khách — thêm trường vào đó phải xin phép.
Đề nghị dựng một màn hình cài đặt riêng của HKLED. Anh duyệt hướng nào?

**Câu 4 — Đợt 1 gồm mấy trong ba tính năng ở mục 6.4?**
Anh nói *"chỉ cần xuất 2 trường trước"* — em hiểu là **cả ba** tính năng đều làm, chỉ **file xuất**
là rút gọn còn 2 cột. Đúng không, hay đợt 1 chỉ làm mỗi phần xuất?

**Câu 5 — File Excel xuất ra có cần công thức sống không?**
Mục 6.4 nói người dùng điền tỷ lệ chiết khấu thì Excel *tự tính* ra giá bán. Vậy file phải chứa
công thức, không phải số chết. Xác nhận giúp em, vì hai cách làm khác nhau.

---

## 8. Việc chưa làm, và vì sao

- **Chưa dựng mockup.** Khách đã gửi mockup dạng Google Sheet — em sẽ dựng bản HTML theo đúng bố
  cục đó sau khi có đáp án Câu 2 và Câu 3, vì hai câu đó đổi phần *cài đặt* của màn hình.
- **Chưa tick `intake_ready`.** Đặc tả đã rõ, nhưng Câu 1 và Câu 2 còn treo, và đây là quyết định
  của người.
