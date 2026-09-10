# Hướng dẫn sử dụng: Tính nhu cầu vật tư cần mua theo kỳ

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Nhân viên mua hàng, phụ trách kế hoạch sản xuất
> **Cập nhật:** 2026-09-10
> **Mục đích:** Nhìn trước vài tuần tới cần mua vật tư gì, mua bao nhiêu, và lập đơn
> mua thẳng từ đó.

---

## Mục lục

1. [Tính năng này dùng để làm gì](#1-tính-năng-này-dùng-để-làm-gì)
2. [Ai dùng được, và cần khai gì trước](#2-ai-dùng-được-và-cần-khai-gì-trước)
3. [Tab *Tính toán* — chọn kỳ và bấm](#3-tab-tính-toán--chọn-kỳ-và-bấm)
4. [Đọc bảng kết quả](#4-đọc-bảng-kết-quả)
5. [Tab *Lập kế hoạch* — chốt số và tạo đơn mua](#5-tab-lập-kế-hoạch--chốt-số-và-tạo-đơn-mua)
6. [Mười hai câu cảnh báo](#6-mười-hai-câu-cảnh-báo)
7. [Khi màn hình chặn lại](#7-khi-màn-hình-chặn-lại)
8. [Câu hỏi thường gặp](#8-câu-hỏi-thường-gặp)

---

## 1. Tính năng này dùng để làm gì

Màn hình *Kiểm tra tồn kho* trên Đơn hàng bán trả lời cho **một đơn**. Màn hình này trả
lời cho **một khoảng thời gian**: chia khoảng đó thành các kỳ, và với mỗi kỳ cho biết
**cần mua vật tư gì, bao nhiêu**.

Từ đó lập thẳng **Đơn Mua Hàng** cho phần thiếu, gộp nhiều mặt hàng vào một đơn theo
nhà cung cấp.

### Đường vào

**Trang chủ HKLed → Tính Nhu Cầu Vật Tư** (có ở cả phần đầu trang lẫn thẻ *Sản Xuất*).

---

## 2. Ai dùng được, và cần khai gì trước

### Xem được ≠ lập được đơn

| Việc | Ai làm được |
|---|---|
| **Mở màn hình, bấm Tính toán** | Cả người lập kế hoạch sản xuất |
| **Lập Đơn Mua Hàng** | Chỉ người có quyền tạo Đơn Mua Hàng — *Quản lý mua hàng*, *Nhân viên mua hàng* |

Đây là chốt của anh Thắng ngày 09/09: *"người mua hàng được lập em nhé, vì chức năng này
phục vụ cho phòng mua hàng"*.

Người không có quyền vẫn xem được bảng — màn hình **nói rõ ngay từ khi vẽ lưới**, không
để bạn tích dòng, gõ số lượng, chọn nhà cung cấp xong mới bị chặn ở bước cuối.

### Ba thứ nên khai, không khai thì kết quả mỏng

| Thiếu gì | Hậu quả |
|---|---|
| **Thời Gian Bắt Đầu** trên đơn bán | Đơn đó **không xếp được vào kỳ nào** — xem câu cảnh báo số 2 và 3, đây là chỗ hay gặp nhất |
| **Tồn Kho Khả Dụng Tối Thiểu** của mặt hàng | Không có phần đệm tồn an toàn, chỉ tính đúng phần thiếu so với nhu cầu |
| **Bảng giá mua** | Đơn mua lập ra có dòng **đơn giá 0 đồng** |

---

## 3. Tab *Tính toán* — chọn kỳ và bấm

| Ô | Ý nghĩa |
|---|---|
| **Kiểu tính** | **1 — Theo đơn hàng**: lấy nhu cầu từ đơn bán đã duyệt. **2 — Theo lịch sử**: ước lượng từ một khoảng quá khứ |
| **Loại kỳ** | *Ngày* · *Tuần* · *Tháng* |
| **Số kỳ** | Từ 1 đến **52** |
| **Bắt đầu từ ngày** | Mặc định là **hôm nay** |

Bấm **Tính toán** ở góc phải.

> Kết quả nhiều thì màn hình chạy nền và hiện *"Đang xếp hàng đợi — N%"*. Cứ để yên,
> bảng sẽ tự hiện.

> ⚠️ **Kết quả chỉ giữ 30 phút.** Để lâu rồi mới sang tab *Lập kế hoạch* thì màn hình
> báo *"Kết quả đã hết hạn — bấm Tính toán lại"*. Không mất gì, chỉ cần bấm lại.

---

## 4. Đọc bảng kết quả

Ba thẻ trên cùng: **Vật tư cần mua** (bao nhiêu mã) · **Tổng còn phải mua** (tổng số
lượng) · **Kỳ tính** (khoảng ngày).

Bảng bên dưới: mỗi mặt hàng một dòng, mỗi kỳ **hai cột** *Nhu cầu* và *Cần mua*, cột
**Cần mua** ngoài cùng bên phải là tổng.

> **Cột Cần mua có thể hiện hai số**, ví dụ `16 (6)`:
> — số **trước ngoặc** là lượng phải mua **nếu chưa đặt gì**;
> — số **trong ngoặc** là phần **còn phải mua thêm** sau khi trừ hàng đang trên đường về.
>
> Đặt hàng thì nhìn số trong ngoặc; đánh giá tổng nhu cầu thì nhìn số ngoài.

**Bảng trống** không có nghĩa là hỏng — nếu trong khoảng đã chọn không có đơn bán nào
(Kiểu 1) hoặc không có lịch sử (Kiểu 2) thì màn hình ghi rõ *"Không có nhu cầu nào trong
khoảng đã chọn"*.

---

## 5. Tab *Lập kế hoạch* — chốt số và tạo đơn mua

### Bước 1 — Chọn dòng

Tích từng dòng, hoặc tích ô ở **đầu bảng** để chọn hết. Dòng dưới bảng cho biết đang
chọn mấy dòng và tổng bao nhiêu.

### Bước 2 — Sửa *Số lượng đặt* nếu cần

Cột này **sửa được** — mua tròn thùng, mua theo lô tối thiểu, hoặc **cho về 0 để bỏ dòng**
(về 0 thì dòng tự bỏ tích).

Cột **Ngày cần hàng** chỉ đọc, là **ngày đầu của kỳ bị thiếu**.

> 🔴 **Nhãn đỏ "đã trễ"** nghĩa là ngày cần hàng đã ở quá khứ — phần hàng đó **đang trễ
> so với kế hoạch**. Đơn mua lập ra sẽ ghi **ngày hôm nay** (hệ thống không cho ghi ngày
> yêu cầu sớm hơn ngày lập đơn), và màn hình **nói rõ ngày gốc là bao nhiêu**. Đây không
> phải dữ liệu sai — đừng bỏ qua nó.

### Bước 3 — Bấm *Lập đơn hàng*, rồi mới chọn nhà cung cấp

Hộp thoại hiện **gợi ý từ lịch sử mua** theo ba tiêu chí — *Giá tốt nhất* · *Giao nhanh
nhất* · *Chất lượng tốt nhất*. Bấm thẳng vào tên để điền vào ô nhà cung cấp.

> **Mỗi gợi ý luôn ghi kèm mẫu số** — ví dụ *"rẻ nhất ở 1/2 mặt hàng, so giữa **1 nhà cung
> cấp** từng bán"*. Đọc mẫu số trước khi tin: "rẻ nhất" mà chỉ so giữa một nhà cung cấp thì
> chưa so với ai cả. Chưa đủ dữ liệu thì tiêu chí đó ghi thẳng là **chưa đủ dữ liệu**.
>
> *"Giao nhanh nhất: trung bình **0.0 ngày**"* nghĩa là những lần trước **đặt và nhận trong
> cùng một ngày** — không phải lỗi, không phải "chưa đo được".

Một lần bấm ra **một đơn mua, nhiều dòng hàng**, cho **một** nhà cung cấp. Cần hai nhà
cung cấp thì làm hai lượt.

### Bước 4 — Đọc hộp báo kết quả

Tiêu đề ghi **"Đã tạo đơn mua nháp"** kèm mã đơn bấm được.

> 🔴 **Đơn ra ở dạng NHÁP, và điều đó là cố ý.** Anh Thắng chốt 09/09: *"đơn tạo ra ở dạng
> nháp em nhé, vì sau này họ cài luồng duyệt trên đơn nữa"*. Người mua phải mở đơn ra kiểm
> rồi tự duyệt.
>
> **Hệ quả phải nhớ:** phép tính chỉ trừ đơn **đã duyệt**. Lập đơn xong mà chưa đi duyệt
> thì bấm *Tính toán* lại vẫn thấy **số thiếu y nguyên** — không phải lỗi. Màn hình che ba
> lớp: cảnh báo phần đang nằm trong đơn nháp · dòng đã lập đơn bị **khoá lại kèm số đơn** ·
> hộp báo kết quả nói thẳng. Nhưng **vẫn phải nhớ vào duyệt đơn**.

---

## 6. Mười hai câu cảnh báo

Khối vàng *"N điều cần biết về kết quả này"* gập/mở được. Dưới đây là **toàn bộ 12 câu**
màn hình có thể hiện — liệt kê từ mã nguồn, không phải từ một lần chạy, nên có câu bạn
sẽ không bao giờ gặp.

### Nhóm A — về dữ liệu đầu vào

| Câu | Nghĩa · nên làm gì |
|---|---|
| *"N đơn bán đã duyệt bị bỏ qua vì trống Thời Gian Bắt Đầu — không xếp được vào kỳ nào"* | Điền *Thời Gian Bắt Đầu* cho các đơn được nêu tên |
| *"N đơn ĐANG GHIM nhưng trống Thời Gian Bắt Đầu…"* | 🔴 **Câu quan trọng nhất nhóm này.** Phần hàng các đơn đó giữ **vẫn bị trừ** khỏi tồn khả dụng, nhưng nhu cầu của chúng **không được tính vào kỳ nào** — nên bảng **báo thiếu mà không thấy đơn tương ứng**. Điền *Thời Gian Bắt Đầu* là hết |
| *"Khoảng tham chiếu … không có đơn bán nào — không tính được nhu cầu Kiểu 2"* | Chọn khoảng tham chiếu khác, hoặc dùng Kiểu 1 |
| *"Chưa mặt hàng nào … được khai Tồn Kho Khả Dụng Tối Thiểu cho công ty X"* | Kết quả **không có phần đệm tồn an toàn**, chỉ đúng phần thiếu so với nhu cầu |

### Nhóm B — về định mức

| Câu | Nghĩa · nên làm gì |
|---|---|
| *"…: định mức lặp vòng, dừng nổ tại đây"* | Định mức khai vòng. Sửa định mức của mã được nêu |
| *"Chưa có mặt hàng **dịch vụ gia công** nên không lập được dòng đơn mua gia công cho: …"* | Khai mặt hàng dịch vụ gia công trong danh mục |

### Nhóm C — về phần "đã có người lo" (hay bị hiểu nhầm nhất)

| Câu | Nghĩa · nên làm gì |
|---|---|
| *"Đang có phiếu Yêu Cầu Mặt Hàng ĐÃ DUYỆT mà chưa thành đơn mua: …"* | Số cần mua bên dưới **CHƯA trừ** phần đó. Kiểm trước khi đặt thêm, kẻo mua trùng |
| *"Đang có Đơn Mua Hàng CÒN NHÁP chứa: …"* | Đơn nháp **chưa được trừ**. Duyệt đơn thì lần tính sau mới trừ |
| *"N mặt hàng đang bị ghim NHIỀU HƠN số có trong kho; phần vượt đã bỏ qua…"* | Không phải lỗi — bỏ phần vượt để **không sinh nhu cầu mua ảo** |

> ⚠️ **Ba câu nhóm C đều nói cùng một điều: con số trong bảng CHƯA trừ phần đó.** Rất dễ
> đọc ngược thành "đã tính hộ rồi" rồi bớt số đi — bớt là mua thiếu, hoặc đặt trùng.

### Nhóm D — chỉ hiện khi bấm *Tạo đơn mua*

| Câu | Nghĩa · nên làm gì |
|---|---|
| *"N dòng có Ngày cần hàng đã ở quá khứ nên đơn ghi ngày hôm nay (…) — phần hàng này ĐÃ TRỄ"* | Xem mục 5, bước 2 |
| *"N dòng chưa có đơn giá (bảng giá mua chưa khai): … Điền giá trước khi duyệt."* | **Điền giá trước khi duyệt đơn**, đừng duyệt đơn 0 đồng |
| *"Đơn đang ở trạng thái NHÁP. Số cần mua ở tab Tính toán chỉ giảm sau khi đơn được DUYỆT."* | Câu này **luôn hiện**. Nhớ vào duyệt đơn |

---

## 7. Khi màn hình chặn lại

Khác với cảnh báo, những câu dưới đây **dừng thao tác**:

| Câu | Cách xử lý |
|---|---|
| *"Kết quả đã hết hạn hoặc chưa tính xong — bấm Tính toán lại"* | Bấm *Tính toán* lại (kết quả giữ 30 phút) |
| *"Bạn không có quyền tạo Đơn Mua Hàng…"* | Chuyển danh sách cho bộ phận mua hàng — xem mục 2 |
| *"Tối đa 52 kỳ, đang chọn N"* · *"Số kỳ phải từ 1 trở lên"* | Giảm số kỳ |
| *"Đến Ngày phải từ Từ Ngày trở đi"* · *"Kiểu 2 phải nhập Từ Ngày và Đến Ngày"* | Sửa khoảng ngày |
| *"Chưa xác định được Công ty…"* | Mức tồn tối thiểu lưu **theo từng công ty** — chọn công ty |
| *"Chưa chọn nhà cung cấp"* · *"Nhà cung cấp X đang bị khoá"* | Chọn nhà cung cấp khác |
| *"Không lập được đơn mua"* kèm danh sách dòng | Mỗi dòng nêu rõ lý do: không có mặt hàng · mặt hàng **đang bị khoá** · mặt hàng **không được khai là hàng mua**. Sửa trong danh mục mặt hàng rồi bấm lại |

---

## 8. Câu hỏi thường gặp

**Lập đơn xong, bấm Tính toán lại mà số thiếu không giảm — hỏng à?**
Không. Phép tính chỉ trừ đơn **đã duyệt**, mà đơn lập ra cố ý để **nháp**. Vào duyệt đơn
rồi tính lại thì số mới giảm.

**Bảng trống, không có dòng nào.**
Trong khoảng đã chọn không có đơn bán (Kiểu 1) hoặc không có lịch sử (Kiểu 2). Thử nới
khoảng ngày hoặc đổi kiểu tính.

**Bảng báo thiếu nhưng tôi không tìm ra đơn nào cần lượng đó.**
Xem câu cảnh báo *"N đơn ĐANG GHIM nhưng trống Thời Gian Bắt Đầu"* ở mục 6 — đây đúng là
triệu chứng của nó.

**Sao có mặt hàng cột Cần mua ghi hai số?**
Số ngoài ngoặc là chưa trừ hàng đang về, số trong ngoặc là đã trừ. Đặt hàng thì nhìn số
trong ngoặc.

**Tôi mở được màn hình nhưng bấm Tạo đơn mua thì bị chặn.**
Đúng thiết kế: xem được không có nghĩa là lập được đơn. Xem mục 2.

**Gợi ý nhà cung cấp có đáng tin không?**
Đọc **mẫu số** ghi kèm mỗi dòng. Sổ mua còn mỏng thì gợi ý chỉ so giữa một vài nhà cung
cấp — lúc đó nó là gợi ý, không phải kết luận.

**Muốn hai nhà cung cấp trong một lần thì làm sao?**
Không được — một lần bấm ra một đơn cho một nhà cung cấp. Chọn nhóm dòng thứ nhất, lập
đơn, rồi chọn nhóm còn lại và lập đơn thứ hai.

**Đơn mua lập ra có tự gửi cho nhà cung cấp không?**
Không. Đơn ở dạng **nháp**, chưa có hiệu lực gì cho tới khi người mua duyệt.

---

> **Liên quan:** *Kiểm tra tồn kho và nguồn lực trên Đơn hàng bán* (cùng cách tính tồn
> khả dụng, nhưng cho **một đơn** thay vì **một khoảng kỳ**) · *Khai kho mặc định và tồn
> tối thiểu theo công ty* (khai *Tồn Kho Khả Dụng Tối Thiểu* dùng ở mục 2).
