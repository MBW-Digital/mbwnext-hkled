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
7. [Hẹn lại ngày giao](#7-hẹn-lại-ngày-giao)
8. [Khối "Cần để ý"](#8-khối-cần-để-ý)
9. [Câu hỏi thường gặp](#9-câu-hỏi-thường-gặp)

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

### Bốn câu chỉ hiện khi bấm nút này

Khác với khối *Cần để ý* ở mục 8 — bốn câu dưới đây **chỉ xuất hiện lúc bấm nút**, không có
trên màn hình kiểm tra.

| Câu | Nghĩa | Nên làm gì |
|---|---|---|
| *"…: có ở cả Bảng 1 và Bảng 2 nên số cần mua là **tổng hai dòng Thiếu**…"* | Mặt hàng vừa bán thẳng trên đơn, vừa là vật tư của mặt hàng khác | Kiểm lại số trước khi gửi. Phần tồn đang có **đã được trừ ở cả hai bảng**, nên cộng thẳng có thể xin dôi ra |
| *"N mã không có trong danh mục hoặc thiếu đơn vị tính, **đã bỏ khỏi phiếu**: …"* | Những mã đó **không** vào phiếu | Khai lại mặt hàng cho đủ đơn vị tính rồi bấm lại, nếu thật sự cần mua |
| *"…đã xin rồi: … Kiểm lại trước khi gửi để khỏi mua trùng"* | **Chính đơn này** đã từng sinh phiếu yêu cầu | Mở phiếu cũ ra xem trước; bấm nữa là ra thêm phiếu cho cùng phần thiếu |
| *"**Toàn nhà máy** đang có phiếu yêu cầu ĐÃ DUYỆT mà chưa thành đơn mua: …"* | Xem ghi chú đỏ bên dưới | Phần đó sắp về thì **giục mua** thay vì xin thêm |

> 🔴 **Câu cuối dễ hiểu nhầm nhất — đọc kỹ.** Nó nói về **toàn nhà máy**, không phải đơn đang
> mở, và **số đó KHÔNG được trừ vào phiếu đang tạo**. Rất dễ tưởng phần đó đã được tính hộ rồi
> nên bớt đi — bớt là thiếu hàng thật. Câu trên màn hình có ghi rõ vế này, đừng đọc lướt qua nó.

---

## 7. Hẹn lại ngày giao

Nút **Hẹn lại ngày giao** ở chân hộp thoại trả lời câu **"bao giờ giao được?"** — khác với nút
bên cạnh vốn trả lời **"đặt mua phần thiếu"**.

Ngày gợi ý ghép **hai vế nối tiếp nhau**, không phải lấy cái muộn hơn trong hai cái:

1. **Chờ vật tư** — lấy **ngày hàng về muộn nhất** trong số vật tư còn thiếu (Bảng 2).
2. **Rồi mới làm** — từ ngày đó mới xếp khối lượng sản xuất vào lịch làm việc.

Thợ rảnh cả tháng cũng không sản xuất được trước khi hàng về, nên hai vế phải nối tiếp. Ghép
kiểu khác sẽ ra ngày **sớm hơn thực tế** — tức hứa sớm rồi trễ hẹn.

> ⚠️ **Ngày này chỉ để tham khảo.** Bấm nút **không** sửa *Ngày Giao Hàng* trên đơn. Muốn đổi
> thì tự sửa ô đó.

### Bốn kiểu trả lời — hai trong bốn cố ý KHÔNG có ngày

| Kiểu | Khi nào | Nên làm gì |
|---|---|---|
| **Có ngày** (nền xanh) | Đủ dữ liệu | Dùng được. Câu bên dưới ghi rõ **cách ra ngày đó**: hàng về ngày nào, cộng bao nhiêu phút, trên mấy người |
| **Có ngày, nền vàng** | Có mặt hàng chưa khai *Thời Gian Sản Xuất* | **Ngày thật sẽ MUỘN HƠN** — mới cộng được phần công của những mặt hàng đã khai. Màn hình nêu tên mặt hàng còn thiếu |
| **Không có ngày** — *"chưa có đơn mua nào đang mở"* | Vật tư thiếu mà chưa ai đặt mua | Đặt mua trước (nút *Tạo Yêu Cầu Mặt Hàng* ngay cạnh), rồi bấm lại |
| **Không có ngày** — *"lịch làm việc hiện có không đủ"* | Dữ liệu đủ nhưng lịch không kham nổi khối lượng | Xếp thêm ca hoặc thêm người, rồi bấm lại |

> 🔴 **Không ra ngày KHÔNG phải là nút hỏng.** Chưa ai đặt mua thì không có căn cứ nào để đoán
> ngày hàng về — máy có đưa ra một ngày thì cũng là bịa. **Một ô trống có giải thích thì bạn còn
> đi hỏi bộ phận mua; một ngày sai thì bạn hứa thẳng với khách rồi trễ hẹn.**

### Hai kiểu "không có ngày" khác nhau ở việc bạn phải làm

Đọc kỹ câu giải thích, đừng chỉ nhìn màu nền:

- *"chưa có đơn mua nào đang mở"* ➜ đi **giục mua hàng**.
- *"lịch làm việc hiện có không đủ"* ➜ đi **xếp thêm ca hoặc thêm người**.

Hai việc khác hẳn nhau, làm nhầm thì mất thời gian mà đơn vẫn kẹt.

### ⚠️ Lịch làm việc phải được khai tới đủ xa

Nút chỉ xếp việc trong phạm vi **lịch làm việc đã khai**. Hết lịch thì nó trả lời *"chưa có nhân
sự nào được xếp lịch làm việc"* — không phải lỗi, mà là **chưa có dữ liệu để tính**.

> **Đo ngày 10/09/2026:** lịch làm việc trên hệ thống mới khai **tới 30/09**. Nghĩa là từ
> **01/10**, đơn nào có hàng về sau ngày đó sẽ không ra ngày cho tới khi có người khai thêm lịch.
> Nên khai lịch trước, đừng đợi tới lúc bấm không ra.

---

## 8. Khối "Cần để ý"

Khối vàng dưới Bảng 3 nêu tên **từng mặt hàng** có vấn đề về khai báo. Các câu hay gặp:

| Câu | Nghĩa | Nên làm gì |
|---|---|---|
| *"chưa có định mức, tạm coi như phải mua"* | Mặt hàng khai là Sản xuất/Gia công nhưng chưa có BOM | Khai định mức cho nó, hoặc sửa *Phương pháp bổ sung* thành Mua hàng |
| *"Phương pháp bổ sung đang là … nên coi như phải mua, nhưng mặt hàng này CÓ định mức"* | Khai báo mâu thuẫn: có định mức nhưng không khai là hàng sản xuất | Sửa *Phương pháp bổ sung* trên mặt hàng. **Không sửa thì hệ thống đi mua chính nó thay vì mua nguyên vật liệu** |
| *"định mức lặp vòng (mặt hàng này nằm trong định mức của chính nó), dừng bóc tại đây"* | Định mức bị khai vòng — A cần B, B lại cần A | Sửa định mức. Câu này **nêu đủ tên mọi mặt hàng trong vòng** để biết sửa ở đâu |
| *"định mức lồng quá N cấp, dừng bóc"* | Cây định mức quá sâu | Kiểm lại dữ liệu định mức của những mã được nêu tên |

Hai câu nữa **không nói về khai báo định mức mà nói về con số**, ít gặp hơn nhưng quan trọng hơn:

| Câu | Nghĩa | Nên làm gì |
|---|---|---|
| *"…: bảng chi tiết cộng ra X nhưng phần đang trừ là Y — báo đội kỹ thuật, **đừng dựa vào bảng bung ra** của mã này"* | Bảng bung ra (mục 5) và con số đang trừ **không khớp nhau** | **Đừng dùng bảng bung ra của mã đó** để đi thương lượng nhả hàng, và báo kỹ thuật. Con số *Tồn khả dụng* ở bảng chính vẫn dùng được |
| *"…: đơn khác đang ghim A nhưng kho chỉ có B — chỉ trừ được B. Phần C còn lại **KHÔNG cộng vào đơn này**"* | Các đơn khác giữ nhiều hơn số thật có trong kho | Không phải lỗi. Đây là lý do *Tồn khả dụng* hiện **0** chứ không hiện số âm, và vì sao dòng **Cộng** ở bảng bung ra có thể lớn hơn phần đã trừ |

---

## 9. Câu hỏi thường gặp

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
Được — cả *Kiểm Tra Tồn Kho* lẫn *Hẹn lại ngày giao*. Riêng *Tạo Yêu Cầu Mặt Hàng* thì phải lưu
đơn trước, vì phiếu phải trỏ về số đơn.

**Bấm Hẹn lại ngày giao mà không ra ngày nào — hỏng à?**
Không. Đọc câu giải thích: hoặc **chưa ai đặt mua** phần vật tư còn thiếu, hoặc **lịch làm việc
không đủ**. Cả hai đều là "chưa đủ căn cứ để hẹn", chứ không phải tính sai. Xem mục 7.

**Ngày gợi ý có tự điền vào Ngày Giao Hàng không?**
Không. Nó chỉ hiện ra để bạn cân nhắc; muốn đổi thì tự sửa ô *Ngày Giao Hàng*.

**Màn hình báo "toàn nhà máy đang có phiếu yêu cầu đã duyệt…" — vậy tôi bớt số đi à?**
**Không.** Câu đó nói về **cả nhà máy**, và số đó **chưa được trừ** vào phiếu bạn đang tạo. Bớt
đi là xin thiếu. Nó chỉ để bạn cân nhắc **giục mua** phần đang chờ thay vì xin thêm.

**Muốn giữ hàng thật sự cho đơn này thì làm sao?**
Tích ô *Ghim Tồn Khả Dụng* trong mục Items, hoặc sửa cột *Số Lượng Giữ Chỗ* trên từng
dòng hàng hoá. Đó mới là thao tác giữ chỗ — màn hình kiểm tra không giữ.

---

> **Liên quan:** *Chặn xuất kho quá tồn khả dụng* (dùng chung cách tính tồn khả dụng) ·
> *Phân bổ hàng về vào phần đã ghim của Đơn hàng bán* · *Tính nhu cầu vật tư cần mua
> theo kỳ* (bóc định mức theo kỳ thay vì theo một đơn).
