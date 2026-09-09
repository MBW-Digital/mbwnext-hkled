# Xuất bảng giá niêm yết

> **Khách hàng:** HKLED
> **App:** `mbwnext_hkled` (tầng 4 — chỉ khách này dùng)
> **PM Project:** `PM-PRJ-00003` · **PM Feature:** `PM-FEAT-00045`
> **Trạng thái:** **Đặc tả đã chốt đủ 08/09 16:39 — sẵn sàng code.** Dữ liệu đầu vào còn thiếu
> nhưng anh Thắng đã quyết cứ dựng màn hình trước, xem mục 4b.
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

## 7. Năm câu đã hỏi — anh Thắng trả lời đủ

| Câu | Trả lời | Lúc |
|---|---|---|
| **1** Ai nạp dữ liệu giá đầu vào, bao giờ? | *"Em cứ dựng màn hình để sẵn nhé, rồi anh sẽ test trên dữ liệu đã có thôi, hoặc anh tự tạo dữ liệu để test"* — **dựng trước, không chờ dữ liệu** | 16:21 |
| **2** "Cập nhật cho sales" ghi vào đâu? | Ghi vào `Item Price`, bảng giá **`Standard Selling`** | 16:21 + 16:39 |
| **3** Hai tỷ lệ cấp hệ thống đặt ở đâu? | *"nên tạo 1 màn hình cài đặt riêng cho HKLED"* — **không** đụng màn hình cài đặt của app lõi | 16:21 |
| **4** Đợt 1 gồm mấy tính năng? | **Cả ba**; chỉ riêng **file xuất** rút gọn còn 3 cột (mã · giá niêm yết · giá bán để trống) | 16:21 |
| **5** File Excel có công thức sống không? | *"em thêm 1 trường tỷ lệ chiết khấu trên file… file xuất sẽ có công thức sống"* — **có** | 16:21 |

### Ba chỗ hỏi thêm ở mockup — cũng đã chốt

> **1. Làm tròn** — *"Làm tròn gần nhất em nhé"* ➜ bội **5.000 gần nhất**, không phải làm tròn lên.
> Đúng cách tôi suy từ số trong file khách.
>
> **2. Bảng giá** — *"ghi vào bảng giá Standard Selling em nhé"* ➜ đúng đề xuất của tôi. Khớp luồng
> đang chạy: cả 40 đơn bán trên cổng 8012 đều dùng bảng giá này.
>
> **3. Dòng không tính được** — *"Em có hiện kèm chữ không tính được nhé"* ➜ **hiện, không ẩn**.
> Đúng đề xuất của tôi.
>
> **4. Cột *Đang áp dụng*** (tôi tự thêm) — *"ok em theo cột Đang áp dụng đó nhé"* ➜ **được duyệt**.

*(Tất cả ở bình luận `rnor4mk16o`, 08/09/2026 16:39.)*

---

## 8. Chốt kỹ thuật rút ra từ các câu trả lời

**Cost — rẽ nhánh theo `Phương pháp bổ sung`:**

| Phương pháp bổ sung | Nguồn cost |
|---|---|
| `Mua hàng` | giá của **đơn mua gần nhất** của mặt hàng đó |
| `Sản xuất` · `Gia công` | **giá thành của BOM mặc định** |

**Bốn tỷ lệ, hai cấp:**

| Tỷ lệ | Khai ở | Ghi vào |
|---|---|---|
| Hao phí | toàn hệ thống | màn hình *Cài Đặt Giá Niêm Yết* (Single riêng của HKLED) |
| Tính giá niêm yết | toàn hệ thống | như trên |
| Chi phí R&D | **từng mặt hàng** | Custom Field trên `Item` |
| Lợi nhuận | **từng mặt hàng** | Custom Field trên `Item` |

⚠ **Không thêm trường vào `MBWNext System Setting`** — đó là màn hình của app lõi dùng chung nhiều
khách, sửa phải xin phép. Anh Thắng đã chốt dựng màn hình riêng.

**Công thức:**

```
Cộng          = cost × (100 + hao phí + R&D + lợi nhuận) / 100
Giá niêm yết  = làm_tròn_5000_gần_nhất( Cộng / tỷ lệ tính giá niêm yết × 100 )
```

**Nút *Cập nhật giá niêm yết*:** ghi `Item Price` của bảng giá `Standard Selling` cho **đúng những
mặt hàng người dùng tick**. Không tự động — chốt trong `notes`: *"không được tự ý cập nhật"*.

Kiểm trên cổng 8012 (08/09): `Sales Order Item.price_list_rate` là trường **chỉ đọc**, chảy từ
`Item Price`; `rate` thì sales sửa được. Cơ chế sẵn có, không phải viết thêm.

**Xuất Excel:** 3 cột — mã mặt hàng · giá niêm yết · **giá bán (rỗng, mang công thức)** — cộng một
ô *tỷ lệ chiết khấu*. Công thức trong file: `giá bán = giá niêm yết × (1 − tỷ lệ chiết khấu)`.

---

## 9. Việc còn lại

- **Mockup bản 3** đã dựng, bấm được, mọi chỗ đều đã chốt:
  `docs/mockups/xuat-bang-gia-niem-yet.html`.
- **Chưa tick `intake_ready`** — đủ điều kiện rồi, nhưng đó là quyết định của người, không phải
  của tôi. ⚠ Lưu ý: tải file mockup vào thư mục `03-mockup` trên PM sẽ **tự tích cổng này** và đẩy
  Analysis ➜ Dev, và code app PM ghi rõ *"chỉ tích một lần, không tự bỏ tích lại"*.
- **Chưa viết test case** — thuộc giai đoạn sau, sau khi code xong.

---

## Đợt 2 — chốt 09/09/2026

Anh Thắng nêu yêu cầu lúc **14:41**, trả lời ba câu chốt lúc **14:55**.

**Nguyên văn yêu cầu:**

> *"Em bổ sung thêm cho anh phần chuyển trang nhé, và ô tìm kiếm mã mặt hàng nữa, ví dụ anh tìm
> kiếm mã A, tích chọn rồi tìm kiếm mã B tích chọn"*

**Nguyên văn ba câu trả lời:**

> *"Câu 1: đúng em nhé — Câu 2: a) tìm theo cả 2 — b) có em nhé — R&D và Lợi nhuận không sửa trên
> bảng em nhé, chỉ được sửa ở bản ghi mặt hàng"*

### Điều quan trọng nhất không nằm trong chữ "chuyển trang"

Ví dụ của anh Thắng — *tìm A tick, tìm B tick* — **không phải yêu cầu thêm giao diện, mà là đổi
cách chạy**. Bản đợt 1 cố ý **bỏ tick của mã rời khỏi lưới** (`bang_gia_niem_yet.js`, cũ):

```js
const co = new Set(this.dong.map((d) => d.ma_hang));
this.chon = new Set([...this.chon].filter((m) => co.has(m)));
```

Lý do khi đó: để không ai ghi giá cho mặt hàng mình không nhìn thấy. Bỏ đoạn này đi thì
**bấm *Cập nhật* sẽ ghi `Item Price` cho cả mã không còn hiện trên màn hình** — với 61.612 mặt
hàng, sau vài lượt tìm rất dễ quên mình đang giữ gì.

Nên đã hỏi lại trước khi làm, và anh Thắng xác nhận *"đúng em nhé"* kèm chấp nhận **ba lớp che**:

1. Ô **"đang giữ N mã đã tick"** — bấm vào mở danh sách đầy đủ, bỏ được từng mã.
2. Dòng cảnh báo khi có mã **không nằm trên trang đang xem**, nêu rõ bao nhiêu mã.
3. Hộp thoại xác nhận **liệt kê từng mã**, đánh dấu mã ngoài trang — không chỉ nói số lượng.

Thêm nút **Bỏ chọn tất cả** luôn nhìn thấy khi đang giữ tick.

### Ba quyết định còn lại

| Chỗ | Chốt | Ghi chú kỹ thuật |
|---|---|---|
| Ô tìm kiếm tìm theo gì | **Cả mã lẫn tên** | `it.name like %x% or it.item_name like %x%` |
| Khớp kiểu nào | **Chứa** (gõ đoạn giữa ra được) | mã khách dạng `M30S050-…-8C-64LED-DD-…`; gõ `64LED` ra 66 mã |
| R&D / Lợi nhuận sửa ở đâu | **Chỉ ở bản ghi Mặt hàng** | bảng giá để **chỉ đọc**; bản vẽ 3 cho sửa tại chỗ, bản 4 đã bỏ |

### 🔴 Luật kỹ thuật của phân trang

Câu **đếm** và câu **lấy dữ liệu** dùng chung hàm `_dieu_kien()`. Viết WHERE hai lần là màn hình
báo *"trang 7/12"* rồi mở trang 7 ra rỗng — và **rỗng trông y hệt "hết dữ liệu"**.

Nhánh có bộ lọc *tính được / đang lệch* vẫn **lấy hết rồi mới cắt trang trong Python**, đúng lý do
đã ghi ở `ma_co_nguon_cost()`: `ma_co_nguon_cost()` chỉ là điều kiện **cần**, cắt trước khi
`cost_cua()` loại là cắt nhầm — lỗi đã mắc ngày 08/09.
