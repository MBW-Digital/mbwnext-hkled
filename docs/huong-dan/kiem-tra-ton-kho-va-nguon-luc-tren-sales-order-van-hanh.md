# Hướng dẫn sử dụng: Kiểm tra tồn kho và nguồn lực trên Đơn hàng bán

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Nhân viên bán hàng, phụ trách kinh doanh
> **Cập nhật:** 2026-09-10
> **Mục đích:** Trước khi hứa ngày giao với khách, xem đơn này có làm được không —
> thiếu hàng gì, thiếu bao nhiêu, bao giờ có, và người có đủ không.

---

## Mục lục

1. [Tính năng này dùng để làm gì](#1-tính-năng-này-dùng-để-làm-gì)
2. [Chuẩn bị trước khi dùng](#2-chuẩn-bị-trước-khi-dùng)
3. [Các bước thực hiện](#3-các-bước-thực-hiện)
4. [Đọc ba bảng](#4-đọc-ba-bảng)
5. [Bung ra xem đơn nào đang giữ hàng](#5-bung-ra-xem-đơn-nào-đang-giữ-hàng)
6. [Tạo Yêu Cầu Mặt Hàng cho phần thiếu](#6-tạo-yêu-cầu-mặt-hàng-cho-phần-thiếu)
7. [Khối "Cần để ý"](#7-khối-cần-để-ý)
8. [Câu hỏi thường gặp](#8-câu-hỏi-thường-gặp)

---

## 1. Tính năng này dùng để làm gì

Khi nhân viên bán hàng đang lập một đơn, câu cần trả lời là: **đơn này có làm được
không, và bao giờ giao được?**

Màn hình này trả lời bằng ba bảng:

- **Bảng 1** — những mặt hàng **trên đơn** còn thiếu bao nhiêu.
- **Bảng 2** — bóc định mức phần còn thiếu ra thành **nguyên vật liệu cần mua**, kèm
  **ngày hàng về** nếu đã có đơn mua.
- **Bảng 3** — **người** có đủ không, tính bằng phút.

### 🔴 Đây là màn hình THAM KHẢO, không phải chứng từ

Câu này in ngay dưới chân bảng, và cần hiểu đúng ngay từ đầu:

> *Kết quả chỉ để tham khảo: không ghim vào đơn, không sinh chứng từ.*

Bấm **Kiểm Tra Tồn Kho** **không** giữ hàng, **không** đặt mua, **không** sửa gì trên
đơn. Nó chỉ đọc và tính. Muốn thật sự **giữ hàng** thì dùng ô *Ghim Tồn Khả Dụng*
(mục 2); muốn thật sự **đặt mua** thì bấm nút ở chân bảng (mục 6).

---

## 2. Chuẩn bị trước khi dùng

### Ô *Ghim Tồn Khả Dụng* — quyết định đơn của bạn có giữ chỗ hay không

Nằm trong mục **Items** của đơn, ngay trên lưới hàng hoá, kèm câu giải thích:

> *Tích ô này thì số lượng chưa giao của đơn được giữ chỗ, các đơn khác không dùng
> vào phần tồn đó nữa. Không tích thì hàng vẫn coi là rảnh để cấp cho đơn gấp hơn.*

- **Tích** — đơn của bạn chiếm chỗ, đơn người khác nhìn thấy tồn khả dụng giảm đi.
- **Không tích** — hàng vẫn để ngỏ, ai cần gấp hơn thì lấy trước.

Cột **Số Lượng Giữ Chỗ** trên lưới hàng hoá cho sửa từng dòng, nếu chỉ muốn giữ một
phần.

### Ba thứ nên khai đủ, nếu không kết quả sẽ mỏng

| Thiếu gì | Hậu quả trên màn hình |
|---|---|
| Mặt hàng chưa khai **Phương pháp bổ sung** | Hệ thống coi như **phải mua chính nó**, không bóc định mức xuống nguyên vật liệu |
| Mặt hàng Sản xuất/Gia công chưa có **định mức (BOM)** | Bảng 2 không bóc được, hiện cảnh báo *"chưa có định mức, tạm coi như phải mua"* |
| Chưa khai **Thời Gian Sản Xuất (Phút)** trên mặt hàng | Bảng 3 không cộng được phần việc đó — mặt hàng bị nêu tên trong khối *Cần để ý* |

---

## 3. Các bước thực hiện

### Bước 1 — Mở đơn hàng bán

Không cần lưu trước. Nút chạy được **cả khi đơn chưa lưu lần nào**.

### Bước 2 — Bấm **Kiểm Tra Tồn Kho**

Nút nằm ở **thanh trên cùng** của đơn, cạnh nút chính.

### Bước 3 — Đọc dòng kết luận ở đầu hộp thoại

Dòng đỏ trên cùng gộp cả ba bảng thành một câu, ví dụ:

> *Đơn này đang thiếu hàng. 2 mặt hàng trên đơn và 3 loại vật tư chưa đủ tồn. Nhân lực đủ.*

Đủ hàng thì dòng này nói đủ. **Đọc dòng này trước**, ba bảng bên dưới chỉ để tra chi tiết.

---

## 4. Đọc ba bảng

### Bảng 1 · Mặt hàng trên đơn

| Cột | Nghĩa |
|---|---|
| **Cần** | Số lượng trên đơn |
| **Tồn thực tế** | Hàng đang thật sự nằm trong kho |
| **Tồn khả dụng** | Phần còn **rảnh** — đã trừ phần các đơn khác giữ chỗ |
| **Đơn khác giữ** | Bấm được, bung ra xem đơn nào (mục 5) |
| **Thiếu** | Phần đơn này không đáp ứng được |

> ⚠️ **Tồn thực tế cao mà Tồn khả dụng bằng 0 là chuyện bình thường** — nghĩa là hàng
> có trong kho nhưng **đã có đơn khác giữ hết**. Đây là cột hay bị đọc nhầm nhất.

Chú thích dưới bảng ghi rõ: *cả hai cột tồn đều đã loại kho lỗi và kho trung chuyển* —
hàng nằm ở hai nhóm kho đó không được tính là bán được.

**Tồn khả dụng không bao giờ âm.** Nếu các đơn khác ghim nhiều hơn số đang có, hệ thống
vẫn hiển thị 0 chứ không hiện số âm.

### Bảng 2 · Cần mua sau khi bóc định mức

Chỉ bóc **phần còn thiếu** của Bảng 1, không bóc cả phần cần — nên số ở đây không phải
là toàn bộ nhu cầu vật tư của đơn.

| Cột | Nghĩa |
|---|---|
| **Thiếu** | Lượng vật tư còn phải lo |
| **Ngày hàng về · SL về** | Lấy từ đơn mua đã duyệt sớm nhất; kèm **số lượng** của chính đơn đó |

Hai câu cần đọc kỹ ở cột cuối:

- **"chưa có đơn mua"** — chưa ai đặt phần này.
- **"quá hạn N ngày"** (chữ đỏ) — đơn mua **đã trễ hẹn**, đừng lấy ngày đó mà hứa với khách.

> ⚠️ **SL về có thể nhỏ hơn phần Thiếu.** Thiếu 100 mà đơn về sớm nhất chỉ có 30 thì
> ngày đó không giải quyết hết. Luôn đọc **hai số cùng nhau**, đừng chỉ nhìn ngày.

### Bảng 3 · Nguồn lực nhân sự

Tính trong **khoảng từ hôm nay tới ngày giao của đơn**, trên những nhân sự có lịch làm việc.

| Cột | Nghĩa |
|---|---|
| **Tổng theo lịch** | Tổng phút làm việc trong khoảng đó |
| **Đã phân bổ** | Phần đã hứa cho việc khác |
| **Còn lại** | Phần còn rảnh |
| **Đơn này cần** | Thời gian sản xuất × số lượng, chỉ tính hàng Sản xuất/Gia công |
| **Kết luận** | *Đủ nhân lực* hoặc thiếu bao nhiêu phút |

Đơn vị là **phút chuẩn** — đã nhân hệ số *Năng Lực* của từng người, nên một phút của thợ
bậc cao không bằng một phút của thợ mới.

---

## 5. Bung ra xem đơn nào đang giữ hàng

Bấm vào chữ **"N đang ghim"** ở Bảng 1 (cột *Đơn khác giữ*) hoặc ngay dưới mã vật tư ở
Bảng 2.

| Cột | Nghĩa |
|---|---|
| **Mã đơn** | Đơn đang giữ |
| **Người phụ trách** | Nhân viên kinh doanh của đơn đó |
| **Đang ghim** | Số lượng họ giữ |
| **Bóc ra từ** | Nếu họ không bán chính mặt hàng này mà bán thứ **chứa** nó |
| **Ngày lấy hàng dự kiến** | Để biết đơn nào dễ thương lượng nhả hàng |

Ba điều cố ý:

1. **Không hiện tên khách hàng** — chỉ hiện người phụ trách, để bạn liên hệ nội bộ.
2. **Tối đa 5 đơn, ưu tiên ngày lấy hàng xa nhất** — đó là đơn dễ xin nhả hàng nhất.
   Còn nữa thì ghi *"…và N đơn nữa"*.
3. **Dòng Cộng nói đúng phần đã trừ**, không phải tổng ghim. Hai số này lệch nhau khi
   các đơn khác ghim nhiều hơn số đang có trong kho — lúc đó dòng Cộng ghi cả hai.

---

## 6. Tạo Yêu Cầu Mặt Hàng cho phần thiếu

Nút **Tạo Yêu Cầu Mặt Hàng** ở chân hộp thoại lấy thẳng cột *Thiếu* và **mở sẵn một
phiếu mới** cho bạn xem lại.

- Phiếu **chưa được lưu** — bạn kiểm rồi tự lưu và gửi duyệt.
- Phần **đã có người lo** (đã nằm trong đơn mua hoặc phiếu yêu cầu khác) được trừ ra,
  để không đặt trùng.

---

## 7. Khối "Cần để ý"

Khối vàng dưới Bảng 3 nêu tên **từng mặt hàng** có vấn đề về khai báo. Các câu hay gặp:

| Câu | Nên làm gì |
|---|---|
| *"chưa có định mức, tạm coi như phải mua"* | Khai BOM cho mặt hàng đó, hoặc xác nhận đúng là hàng mua |
| *"Phương pháp bổ sung đang là … nên coi như phải mua, nhưng mặt hàng này CÓ định mức"* | Kiểm lại *Phương pháp bổ sung* trên mặt hàng |
| *"định mức lặp vòng, dừng bóc tại đây"* | Xem ghi chú bên dưới |

> ⚠️ **Ghi chú 10/09/2026 — hai câu cuối có thể hiện SAI trong một tình huống bình thường.**
> Nếu trên cùng một đơn bạn bán **cả thành phẩm lẫn bán thành phẩm nằm bên trong nó**,
> màn hình sẽ báo *"định mức lặp vòng"* và khuyên kiểm lại *Phương pháp bổ sung* — trong
> khi định mức **không hề lặp vòng** và thiết lập **vẫn đúng**. Lúc đó Bảng 2 cũng liệt
> bán thành phẩm đó vào diện **phải mua** thay vì bóc tiếp xuống nguyên vật liệu.
>
> **Đang được kiểm tra và sửa.** Trong lúc chờ: gặp hai câu này thì kiểm xem đơn có rơi
> vào tình huống trên không trước khi đi sửa khai báo mặt hàng.

---

## 8. Câu hỏi thường gặp

**Bấm nút này có làm gì trên đơn không?**
Không. Không ghim, không sinh chứng từ, không sửa gì. Chỉ đọc và tính.

**Tồn thực tế 31 mà Tồn khả dụng 0 — kho báo sai à?**
Không sai. Hàng có trong kho nhưng đã bị các đơn khác giữ chỗ hết. Bấm *"N đang ghim"*
để xem đơn nào.

**Vì sao Bảng 2 không liệt kê hết vật tư của đơn?**
Bảng 2 chỉ bóc **phần còn thiếu** của Bảng 1. Phần nào tồn đã đủ thì không cần mua nên
không xuất hiện.

**Có ngày hàng về rồi, hứa với khách được chưa?**
Đọc thêm **SL về** và xem có chữ đỏ *"quá hạn"* không. Ngày về mà số lượng không đủ,
hoặc đơn mua đã trễ hẹn, thì chưa hứa được.

**Bảng 3 báo đủ nhân lực nhưng thực tế xưởng đang bận?**
Bảng 3 tính trên **lịch làm việc đã khai** và phần **đã phân bổ trong hệ thống**. Việc
nhận ngoài hệ thống thì nó không thấy.

**Đơn chưa lưu có bấm được không?**
Được.

**Muốn giữ hàng thật sự cho đơn này thì làm sao?**
Tích ô *Ghim Tồn Khả Dụng* trong mục Items, hoặc sửa cột *Số Lượng Giữ Chỗ* trên từng
dòng hàng hoá. Đó mới là thao tác giữ chỗ — màn hình kiểm tra không giữ.

---

> **Liên quan:** *Chặn xuất kho quá tồn khả dụng* (dùng chung cách tính tồn khả dụng) ·
> *Phân bổ hàng về vào phần đã ghim của Đơn hàng bán* · *Tính nhu cầu vật tư cần mua
> theo kỳ* (bóc định mức theo kỳ thay vì theo một đơn).
