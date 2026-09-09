# Xuất bảng giá niêm yết

> **Khách hàng:** HKLED
> **App:** `mbwnext_hkled` (tầng 4 — chỉ khách này dùng)
> **PM Project:** `PM-PRJ-00003` · **PM Feature:** `PM-FEAT-00045`
> **Trạng thái:** Analysis — **chưa đủ đầu bài để code**, xem mục 6
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

🔴 **Hai nguồn nói hai việc khác nhau** — xem mục 6, câu hỏi 1.

---

## 2. Hiểu của tôi — tính năng này dùng để làm gì

HKLED gửi báo giá cho đại lý bằng một file Excel dựng tay. File có hai cột giá: **niêm yết**
(giá gốc, chung cho mọi khách) và **giá bán** (= niêm yết × tỷ lệ chiết khấu, khác nhau theo
từng đối tượng khách).

Khách **không cần hệ thống tính cột giá bán** — họ tự điền tỷ lệ chiết khấu vào file rồi Excel
tự nhân ra. Thứ họ cần hệ thống làm là **xuất ra bảng giá niêm yết luôn khớp dữ liệu hiện tại**,
để khỏi phải dò tay mỗi lần nhà máy đổi giá.

**Ví dụ tình huống:** kinh doanh cần gửi báo giá cho một đại lý mới. Hôm nay họ mở file Excel cũ,
không chắc giá đã cũ chưa, phải hỏi lại nhà máy. Sau khi có tính năng: bấm xuất, được bảng giá
niêm yết đúng tại thời điểm xuất, điền tỷ lệ chiết khấu của đại lý đó rồi gửi đi.

---

## 3. 5W — trả lời được tới đâu

| | Trả lời | Nguồn |
|---|---|---|
| **WHAT** | Xuất bảng giá **niêm yết** theo đúng bố cục file khách đang dùng. **Không** xuất cột giá bán, không tính chiết khấu | Khách nói thẳng 11:22 |
| **WHEN** | Bấm nút, người dùng chủ động. Không phải theo lịch, không phải lúc lưu chứng từ | Suy ra từ *"chỉ cần xuất ra"* — ⚠ **chưa hỏi** |
| **WHO** | Kinh doanh (người gửi báo giá cho đại lý) | ⚠ **chưa hỏi** — mới suy từ ngữ cảnh |
| **WHERE** | File xuất ra (Excel?) — bố cục theo ảnh 1 | ⚠ **chưa hỏi** định dạng |
| **ERROR** | Mặt hàng chưa có giá niêm yết thì xử lý thế nào? | ⚠ **chưa hỏi** |

Ba dòng ⚠ là lý do tính năng **chưa được tick `intake_ready`**.

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

**Hệ quả:** dù bố cục file có chốt xong hôm nay thì cũng **chưa xuất được gì có nghĩa**, vì chưa
biết con số niêm yết lấy ở đâu ra. Đây là câu hỏi 1 ở mục 6, và nó chặn toàn bộ phần còn lại.

### Cột nào lấy được, cột nào chưa

| Cột trong file khách | Lấy từ đâu | Được chưa |
|---|---|---|
| MÃ THUỘC TÍNH (SKU) | `Item.name` của biến thể | ✔ có sẵn |
| MÔ TẢ SẢN PHẨM | `Item.description` / mặt hàng cha | ✔ có sẵn, cần chốt lấy trường nào |
| CẤU HÌNH SẢN XUẤT | tổ hợp đặc tính biến thể (Chip LED, Driver…) | ✔ dựng được từ `Item Variant Attribute` |
| HÌNH ẢNH | `Item.image` | ⚠ chưa đo có bao nhiêu mặt hàng có ảnh |
| BẢO HÀNH | `Item.warranty_period` | ⚠ đơn vị lệch (ngày vs "03 năm") |
| KHO | ? — file ghi `SLL` | ❌ **chưa biết `SLL` nghĩa là gì** |
| **NIÊM YẾT** | ? | ❌ **chưa có nguồn** |
| GIÁ BÁN | — | ✔ **không cần**, khách tự tính |

---

## 5. Tầng và app — chốt tầng 4

`mbwnext_hkled`. Lý do: bố cục bảng giá này là **mẫu riêng của HKLED** (logo HKLED, cột *Cấu hình
sản xuất* bám theo bộ đặc tính riêng, chữ *Chipled 3030*). Khách khác không dùng lại được.

Phần **nguồn giá** thì có thể khác: nếu chốt là dùng `Price List` của ERPNext thì đó là cơ chế
tầng 1 sẵn có, không phải viết mới. Chỉ phần **xuất file** mới là tầng 4.

⚠ Chưa tra va chạm hook vì chưa biết sẽ hook vào DocType nào — làm ở Giai đoạn 3, sau khi có
câu trả lời cho mục 6.

---

## 6. 🔴 Năm câu phải hỏi trước khi code

**Câu 1 — Giá niêm yết LẤY Ở ĐÂU, hay HỆ THỐNG TÍNH RA?**
Hai nguồn đang nói hai việc: chat với khách nói *"chỉ cần xuất ra"* (tức giá đã có sẵn ở đâu đó),
còn sheet hiện trạng nói *"thiết kế bảng giá dựa theo các chỉ số như hao hụt, RND"* (tức hệ thống
phải **tính ra** giá). Đây là hai tính năng có khối lượng khác nhau rất xa. Câu này chặn mọi thứ
còn lại.

**Câu 2 — Nếu là "đã có sẵn" thì ai nhập và nhập vào đâu?**
Hiện toàn site chỉ có 20 dòng Item Price cho 62.061 mặt hàng, và không có bảng giá nào tên *niêm
yết*. Dựng một `Price List` mới tên *Giá niêm yết* rồi khách tự nhập, hay nhập vào ô
*Standard Selling Rate* trên từng mặt hàng?

**Câu 3 — `SLL` ở cột KHO nghĩa là gì?**
Xuất hiện ở mọi dòng trong ảnh. Nếu là *"số lượng lớn"* thì nó là thuộc tính bán hàng chứ không
phải kho, và không lấy từ dữ liệu kho được.

**Câu 4 — Xuất ra định dạng nào, và ai bấm?**
Excel để khách điền tiếp tỷ lệ chiết khấu, hay PDF để gửi thẳng? Ảnh cho thấy khách còn **sửa
tiếp trong file** (điền chiết khấu), nên nghiêng về Excel — nhưng cần xác nhận. Và ai được bấm:
chỉ kinh doanh, hay cả người khác?

**Câu 5 — Cột đơn giá sửa được trên Đơn bán hàng có thuộc tính năng này không?**
Khách nêu ở đoạn cuối, kèm chữ *"đang có phương án"* — tức **chưa chốt**. Nếu có thì đây là việc
riêng, chạm tới cách tính hoa hồng, phải tách thành tính năng khác chứ không gộp vào bảng giá.

---

## 7. Việc chưa làm, và vì sao

- **Chưa dựng mockup.** Luật dự án: mockup vẽ trước khi code, nhưng sau khi có đầu bài. Vẽ bây giờ
  là vẽ theo phỏng đoán về nguồn giá.
- **Chưa tick `intake_ready`.** Ba trong năm câu 5W còn để ⚠, và đây là quyết định của người, không
  phải của tôi.
- **Chưa đo số mặt hàng có ảnh / có `warranty_period`.** Sẽ đo khi biết bố cục cột được chốt —
  đo bây giờ có thể đo nhầm cột.
