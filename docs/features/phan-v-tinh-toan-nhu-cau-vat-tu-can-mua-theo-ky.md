# Tính nhu cầu vật tư cần mua theo kỳ — PM-FEAT-00030

> Trạng thái: **spec, chưa code.** Viết 03/09/2026 sau khi Thắng chốt nốt hai câu cuối (02/09 11:14).
> Nguồn: `PM-DOC-00310` *TÀI LIỆU NGHIỆP VỤ PHẦN V.docx* (bản Thắng phân tích) + 9 ảnh lời khách
> ở `01-tai-lieu-khach-hang` (`PM-DOC-00312`…`00320`) + 15 bình luận chốt trên PM-FEAT-00030.
> Mọi con số hiện trạng trong file này **đo trên cổng 8012 ngày 03/09/2026**, không lấy theo trí nhớ.

⚠ **Về cái tên.** Tài liệu khách gọi là "Phần V", nhưng số Phần đang chỉ hai thứ khác nhau: Phần V
của tài liệu Giai đoạn 1 là *Biểu đồ tình hình làm việc* (đã xong 08/08). Thắng chốt 19/08: Phần IV
cũ đổi cách hiểu thành "Phần III.01", Phần IV thật là *Kiểm tra tồn kho trên Đơn bán hàng*. Tên
thư mục giữ theo PM để tra chéo được; tên nghiệp vụ nên dùng **"Tính nhu cầu vật tư cần mua theo kỳ"**.

---

## 1. Người dùng làm được gì

Hai tab:

| Tab | Việc |
|---|---|
| **Tính toán** | Chọn kiểu tính + tham số kỳ → ra bảng thiếu hụt theo từng kỳ cho từng vật tư |
| **Lập kế hoạch** | Gộp tổng các kỳ thành một dòng/vật tư → sửa số lượng đặt → tạo đơn mua |

Kết quả **chỉ mang tính tham khảo tại thời điểm bấm Tính toán**, không chốt cứng.

---

## 2. Hai kiểu tính — khác nhau đúng một chỗ

Kiểu tính chỉ là cái vòi cấp con số *Nhu cầu*. Phần trừ tồn, phạm vi kho và tạo đơn mua thì dùng chung.

| | **Kiểu 1 — Theo đơn hàng** | **Kiểu 2 — Theo kết quả bán trước đó** |
|---|---|---|
| Cấu trúc thời gian | Nhiều kỳ (`loại kỳ` × `số kỳ`) | **Một khoảng duy nhất** (từ–đến) |
| Nguồn nhu cầu | Đơn bán có *Thời Gian Bắt Đầu* rơi vào kỳ | Lượng bán thật của khoảng cùng kỳ tháng trước / năm trước |
| Kéo tồn qua kỳ | **Bắt buộc** khi ≥ 2 kỳ | Không có |
| Gộp ở Lập kế hoạch | Cộng tổng các kỳ | Một con số/vật tư |

⚠ **Kiểu 2 KHÔNG chia kỳ** — Thắng chốt 19/08 12:52. Khoảng tham chiếu luôn cùng độ dài với khoảng
đích (chỉ lùi thời gian) nên **lấy thẳng tổng lượng bán**, không quy bình quân/ngày.

---

## 3. Công thức

### 3.1. Một kỳ

```
Thiếu hụt = Tồn tối thiểu − (Tồn khả dụng + PO chưa về − Nhu cầu)
```

Âm là đang dư → kỳ đó không mua, phần dư chuyển sang kỳ sau.

### 3.2. 🔴 Kéo tồn qua kỳ — chỗ dễ sai nhất, chỉ áp cho Kiểu 1

Từ 2 kỳ trở lên **không được** tính mỗi kỳ độc lập từ cùng một tồn ban đầu. Nhu cầu kỳ trước đã ăn
vào tồn:

```
Tồn cuối kỳ N  =  Tồn đầu kỳ N+1

Khả dụng     = Tồn đầu kỳ + PO về trong kỳ − Nhu cầu trong kỳ
Cần mua      = max(0, Tồn tối thiểu − Khả dụng)
Tồn cuối kỳ  = Khả dụng + Cần mua
```

Ví dụ kiểm chứng của tài liệu (min 50, tồn 60, không PO, nhu cầu 30/tuần):

| | Tồn đầu kỳ | Nhu cầu | Khả dụng | Cần mua | Tồn cuối kỳ |
|---|---|---|---|---|---|
| Tuần 1 | 60 | 30 | 30 | **20** | 50 |
| Tuần 2 | 50 | 30 | 20 | **30** | 50 |
| | | | | **Tổng 50** | |

Tính mỗi kỳ độc lập ra **40** — mua thiếu 10, tuần 2 tụt dưới mức tối thiểu mà không ai biết.

⚠ **PO chưa về phải xếp đúng kỳ theo ngày dự kiến nhận**, không dồn hết vào kỳ 1.

### 3.3. 🔴 Chống trừ trùng giữa hai vế

Cơ chế Ghim trừ phần giữ chỗ của đơn bán khỏi tồn khả dụng. Nhưng ở Kiểu 1, nhu cầu tương lai
**cũng lấy từ đơn bán**. Một đơn vừa bị trừ ở vế Tồn vừa được cộng ở vế Nhu cầu là trừ hai lần.

> **Mỗi đơn bán chỉ được tính đúng MỘT vế.**

| | Tồn khả dụng trừ gì |
|---|---|
| **Kiểu 1** | Chỉ trừ phần giữ chỗ của đơn đã ghim có *Thời Gian Bắt Đầu* **NGOÀI** các kỳ đang tính. Đơn ghim **trong** kỳ đã nằm ở vế Nhu cầu → không trừ. |
| **Kiểu 2** | Trừ **toàn bộ** phần giữ chỗ của mọi đơn đã ghim (nhu cầu là lịch sử bán, không trùng đơn hiện tại). |

Ví dụ: tồn 100 · đơn #1 ghim 20 (bắt đầu 15/8, trong kỳ) · đơn #2 ghim 30 (bắt đầu 05/8, ngoài kỳ).
→ Nhu cầu tuần 1 = 20 · Tồn khả dụng = 100 − 30 = **70** · Khả dụng = 70 − 20 = 50.
Trừ cả đơn #1 vào tồn thì ra 30 — sai.

---

## 4. Nguồn nhu cầu theo Phương pháp bổ sung

| Phương pháp | Sinh ra gì |
|---|---|
| **Mua hàng** | Nhu cầu chính là số lượng mặt hàng đó |
| **Sản xuất** | Nổ định mức → nhu cầu nguyên vật liệu và bán thành phẩm |
| **Gia công** | **Hai loại dòng cùng lúc** — xem 4.1 |

### 4.1. Gia công sinh hai loại dòng — Thắng chốt 24/08 01:10

Mặt hàng `A` gia công thiếu 10 thì sinh:

- **1 dòng** đơn mua gia công: mặt hàng = `dịch vụ gia công`, **Finished Good = A**, SL 10
- **n dòng** nguyên vật liệu từ định mức của `A` — vì ERPNext bắt công ty cấp NVL cho nhà cung cấp
  gia công (phần *Supplied Items*)

Khách nói nguyên văn: *"dạng này nó giống cả dạng sản xuất lẫn dạng mua hàng"*. Nên **Gia công không
phải nhánh con của Sản xuất**, nó là nhánh thứ ba.

### 4.2. 🔴 Thứ tự nổ định mức — Thắng chốt 02/09 11:14

```
có BOM  →  dùng BOM
chưa có BOM nhưng có BOM Template  →  nổ theo BOM Template
không có cả hai  →  liệt kê ra cho người dùng kiểm
```

Nhánh giữa là điểm khác biệt của HKLED so với tài liệu gốc: khách **không nuôi BOM sẵn**, BOM được
sinh theo đơn từ BOM Template (Phần I). Dùng lại `api/bom.py::resolve_components(item_code,
template_name)` — hàm **chỉ đọc**, không tạo BOM, đã có sẵn.

⚠ Không gọi `auto_create_bom` ở đây. Tính nhu cầu là việc **chỉ đọc**; tạo BOM thật phải qua một cú
bấm rõ ràng của người dùng (luật đã ghi trong `CLAUDE.md`).

### 4.3. Phạm vi — Thắng chốt 24/08 01:10

> Chỉ tính cho mặt hàng **đã xuất hiện trong chứng từ**. Mặt hàng sản xuất/gia công chưa từng nằm
> trong phiếu bán hay phiếu sản xuất nào thì **không cần dự báo**.

Đây là chốt gỡ được vướng mắc nêu 20/08: toàn site có 62.055 mặt hàng nhưng BOM Template mới phủ
khoảng 17% biến thể. Khoanh theo chứng từ thì con số 62 nghìn không còn là rào cản.

### 4.4. Tránh đếm trùng nhu cầu

Một đơn bán đã sinh Lệnh sản xuất thì **đừng vừa cộng nhu cầu từ đơn (qua nổ định mức) vừa cộng từ
Lệnh sản xuất**. Chọn **một nguồn duy nhất**.

---

## 5. Tồn khả dụng — cùng một cơ sở cho mọi con số

Đây là **tồn khả dụng riêng của HKLED**, không phải tồn khả dụng mặc định của hệ thống. Hai điều kiện:

1. **Loại trừ kho**: lấy tồn mọi kho, trừ kho con của `Nhóm kho lỗi` và `Nhóm kho trung chuyển`.
2. **Cơ chế Ghim**: chỉ đơn bán được tích *Ghim Tồn Khả Dụng* mới giữ chỗ tồn. Đơn chưa ghim không giữ.

`Tồn tối thiểu` và `Tồn hiện tại` phải **cùng đo trên tồn khả dụng** thì so sánh mới cùng chuẩn.
`PO chưa về` vẫn cộng đủ vì hàng đặt về sẽ nhập kho dùng được.

---

## 6. 🔴 Hiện trạng 11 mục checklist — đo ngày 03/09/2026

Tài liệu gốc có checklist "chốt trước khi code". Đây là kết quả đo thật, **không phải đánh dấu suông**:

| # | Mục | Hiện trạng đo được |
|---|---|---|
| 1 | Trường *Tồn kho tối thiểu* trên Mặt hàng | ❌ **CHƯA CÓ**. Phải tạo Custom Field mới. ERPNext chỉ có `Item Reorder` — theo **từng kho**, không dùng được vì tài liệu cần **một con số duy nhất/mặt hàng** |
| 2 | Hai nhóm kho loại trừ | ✅ `Nhóm kho lỗi - HKL` và `Nhóm kho trung chuyển - HKL` **đã có**, đúng tên tài liệu |
| 3 | Cây kho đã xếp đúng chưa | ⚠ Lỗi: `Kho hàng lỗi cần sửa chữa`, `Kho hàng lỗi/trả`. Trung chuyển: `Kho đang sản xuất`, `Kho trung chuyển`. **Nhưng `Kho ký gửi` và `Kho khuyến mãi/hàng mẫu` đang treo thẳng dưới `Kho Tổng`** → sẽ được tính vào tồn khả dụng. Xem câu hỏi Q1 |
| 4 | Chuẩn tồn hiện tại | Lấy `Bin.actual_qty`, loại kho lá của 2 nhóm trên |
| 5 | Ô *Ghim Tồn Khả Dụng* trên đơn bán | ✅ `custom_ghim_ton_kha_dung` (Check) **đã có** — HkLed2 vừa thêm cho Phần IV. Hiện **0 đơn** đã tích |
| 6 | Cách lấy *PO chưa về* + ngày nhận | `Purchase Order Item`: SL chưa nhận + ngày dự kiến nhận, dùng để xếp kỳ |
| 7 | Nguồn nhu cầu Kiểu 1 duy nhất | Chốt: đơn bán nổ định mức. **Không** cộng thêm từ Lệnh sản xuất |
| 8 | Đơn bán dùng trường nào để xếp kỳ | ✅ `custom_start_time` *Thời Gian Bắt Đầu* (Datetime) **đã có**. ⚠ **Nhưng 9/16 đơn đã duyệt đang để TRỐNG ô này** — xem 6.1 |
| 9 | Kiểu 2: nguồn lượng bán | Đơn bán, bỏ nháp/huỷ. ⚠ Site có **0 Phiếu giao hàng và 0 Hoá đơn bán** — xem 6.2 |
| 10 | Gợi ý nhà cung cấp: 3 nguồn dữ liệu | ⚠ Gần như trắng — xem 6.3 |
| 11 | Tab Lập kế hoạch gộp tổng các kỳ | Chốt: gộp tổng, **một dòng/vật tư** |

### 6.1. 🔴 9/16 đơn bán đã duyệt không có *Thời Gian Bắt Đầu*

Kiểu 1 xếp đơn vào kỳ **theo chính ô này**. Đơn để trống sẽ **không rơi vào kỳ nào** — bị bỏ lặng
lẽ khỏi mọi con số nhu cầu, không có gì báo.

➜ Bắt buộc: mặt hàng của đơn để trống ô này phải hiện thành **một dòng cảnh báo có nêu đích danh
số đơn**, không được im lặng bỏ qua. Cân nhắc đề nghị Thắng đặt ô này thành bắt buộc trên đơn bán.

### 6.2. Kiểu 2 nặng hơn Kiểu 1 về dữ liệu

Kiểu 2 tính theo lượng bán kỳ trước, mà site đang có **0 Phiếu giao hàng · 0 Hoá đơn bán · 21 đơn
bán (16 đã duyệt)**, và toàn bộ là dữ liệu đội mình dựng để thử — khách chưa phát sinh giao dịch
thật nào. Kiểu 1 còn có đơn để bấu víu, Kiểu 2 thì không.

Thắng chốt 02/09: **nghiệm thu chạy trên dữ liệu tự dựng**, quy mô thật là **hơn 2.000 đơn/năm,
mỗi đơn 1–2 dòng sản phẩm** (≈ 170 đơn/tháng, 250–350 dòng mỗi kỳ). Bộ dữ liệu thử phải dựng
sát quy mô đó, đừng thử trên bảng 5 dòng rồi tưởng chạy tốt.

### 6.3. Gợi ý nhà cung cấp — hai trong ba tiêu chí chưa có dữ liệu

| Tiêu chí | Nguồn | Đo được |
|---|---|---|
| Giá tốt nhất | Đơn giá gần nhất theo NCC | 6 đơn mua · 10 Item Price · 2 nhà cung cấp — **chạy được, ít** |
| Tiến độ nhanh nhất | Khoảng cách ngày đặt → ngày nhận | **1/6 đơn mua có phiếu nhập** — gần như không tính được |
| Chất lượng tốt nhất | Tỉ lệ đạt theo NCC | **0 bản ghi** ở cả `Quality Inspection`, `Goods Receipt` và `KCS Quantity` |

⚠ Tài liệu ghi nguồn chất lượng là `Quality Inspection`, nhưng nền MBWNext dùng **luồng KCS của
`mbwnext_advanced_buying`** (`Goods Receipt` → `KCS Quantity`). Cả hai đều rỗng. Chốt nguồn nào thì
cũng phải xử lý gọn khi thiếu dữ liệu: ghi **"chưa đủ dữ liệu"**, **không đoán**, không ép chọn.

---

## 7. Tab Lập kế hoạch

- Gộp tổng *Cần mua* của tất cả các kỳ → **một dòng/vật tư**.
- Cột **Số lượng đặt** sửa được, mặc định = số thiếu hụt. Cột *Thiếu hụt* để chỉ đọc bên cạnh.
  Người dùng sửa để mua theo lô tối thiểu, mua tròn thùng, hoặc cho về 0 để bỏ dòng.
- Bấm *Lập đơn hàng* → dùng **Số lượng đặt do người dùng chốt**, không dùng số thiếu hụt gốc.
- Rê chuột vào dòng → popover gợi ý 3 nhà cung cấp theo 3 tiêu chí. Ba tiêu chí có thể trỏ về **3
  nhà cung cấp khác nhau** — hiện cả 3, không tự động ép chọn.

⚠ **Không cần chia đơn mua theo kỳ.** Gộp tổng là đúng — với điều kiện từng kỳ đã tính bằng kéo tồn
qua kỳ. Nếu mỗi kỳ tính độc lập thì con số từng kỳ đã sai, gộp lại càng sai.

### 7.1. Vòng lặp — đơn mua vừa tạo thành *PO chưa về* của lần sau

Lần chạy tiếp theo **phải** cộng số lượng đó vào phần đang về. Không cộng thì báo thiếu lần nữa và
người dùng đặt mua trùng. Phần trở thành *PO chưa về* là **số lượng thật trên đơn mua đã tạo**, không
phải số thiếu hụt gợi ý ban đầu.

---

## 8. Cách hiển thị nhiều kỳ — ảnh 09, chat khách 13/08

Tồn tối thiểu 50, đầu kỳ 60, tuần 1 cần 30, tuần 3 cần 100 → cần đặt 120, nhưng đã mua 50 dự kiến
về tuần 2 → hiển thị **"120 (70)"**. Số trong ngoặc là **phần còn phải mua thêm**.

Chi tiết này **không có trong bản .docx**, chỉ có trong ảnh chat — và nó quyết định cách trình bày
cả bảng.

---

## 9. Việc còn chặn

| | Chặn gì | Ai gỡ |
|---|---|---|
| 🔜 | **Cơ chế Ghim của Phần IV chưa xong.** Phần V dùng lại định nghĩa tồn khả dụng + phần giữ chỗ. Ô `custom_ghim_ton_kha_dung` đã có nhưng logic giữ chỗ đang được HkLed2 viết trong `api/kiem_tra_ton_kho.py`. Mọi chỗ đánh 🔜 trong file này phải chốt lại sau khi Phần IV xong | HkLed2 · PM-FEAT-00023 |
| ❌ | **Trường Tồn kho tối thiểu chưa tồn tại.** Không có nó thì không tính được dòng nào | Cần patch tạo Custom Field |
| ❓ | Câu hỏi Q1–Q3 bên dưới | Thắng |

### Câu hỏi cần Thắng chốt

- **Q1.** `Kho ký gửi` và `Kho khuyến mãi/hàng mẫu` đang treo thẳng dưới `Kho Tổng`, tức **được tính
  vào tồn khả dụng**. Hàng ký gửi có phải hàng dùng được không? Nếu không thì chuyển vào `Nhóm kho
  trung chuyển` — anh đã chốt 25/08 là "kho nào không tính vào pool thì chuyển vào 2 nhóm đó".
- **Q2.** Ô *Thời Gian Bắt Đầu* trên đơn bán có nên đặt thành **bắt buộc** không? Hiện 9/16 đơn đã
  duyệt để trống, mà Kiểu 1 xếp kỳ theo đúng ô đó.
- **Q3.** Tiêu chí **chất lượng** trong gợi ý nhà cung cấp lấy từ `Quality Inspection` hay từ luồng
  KCS của `mbwnext_advanced_buying`? Cả hai đang 0 bản ghi, nên chọn nguồn nào cũng phải chấp nhận
  hiện "chưa đủ dữ liệu" trong thời gian đầu.

---

## 10. Thứ tự làm

1. Patch tạo Custom Field *Tồn kho tối thiểu* trên Mặt hàng.
2. Engine tính (`api/nhu_cau_vat_tu.py`) — **chỉ đọc**: gom nhu cầu → nổ định mức theo thứ tự 4.2 →
   trừ tồn theo 3.1 + kéo tồn theo 3.2 → áp ranh giới chống trừ trùng 3.3.
3. Màn hình tab Tính toán.
4. Tab Lập kế hoạch + tạo đơn mua.
5. Gợi ý nhà cung cấp (mục 9.2 tài liệu) — **làm cuối**, vì hai trong ba tiêu chí chưa có dữ liệu.

⚠ Bước 2 viết được **ngay bây giờ** cho phần không phụ thuộc Ghim: gom nhu cầu, nổ định mức, kéo tồn
qua kỳ, gộp ở Lập kế hoạch. Chỉ mục 3.3 (chống trừ trùng) phải chờ Phần IV chốt phần giữ chỗ.
