# Hướng dẫn sử dụng: Chặn xuất kho quá tồn khả dụng

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Thủ kho, nhân viên bán hàng, kế toán kho
> **Cập nhật:** 2026-09-04
> **Mục đích:** Hiểu vì sao một phiếu xuất bị chặn, và làm gì để xuất được.

---

## Mục lục

1. [Tính năng này dùng để làm gì](#1-tính-năng-này-dùng-để-làm-gì)
2. [Chuẩn bị trước khi dùng](#2-chuẩn-bị-trước-khi-dùng)
3. [Các bước thực hiện](#3-các-bước-thực-hiện)
4. [Kiểm tra kết quả](#4-kiểm-tra-kết-quả)
5. [Thông báo lỗi thường gặp](#5-thông-báo-lỗi-thường-gặp)
6. [Câu hỏi thường gặp](#6-câu-hỏi-thường-gặp)

---

## 1. Tính năng này dùng để làm gì

Khi một Đơn hàng bán đã **giữ chỗ** hàng cho khách của mình, số hàng đó không còn
là hàng tự do nữa — dù nó vẫn nằm trong kho.

Tính năng này **ngăn không cho xuất phần hàng người khác đang giữ**. Bạn vẫn xuất
được phần còn tự do; chỉ khi số muốn xuất vượt quá phần đó thì hệ thống mới chặn.

**Ví dụ tình huống:** Kho còn 31 chiếc *Thành phẩm 1*. Nhưng ba đơn hàng bán đã
giữ chỗ trọn 31 chiếc để giao tuần sau. Bạn lập phiếu xuất 5 chiếc cho một khách
mới — hệ thống chặn, vì 5 chiếc đó đã có chủ. Nếu không chặn, tuần sau ba đơn kia
mới phát hiện thiếu hàng, lúc đó đã hứa ngày giao với khách rồi.

---

## 2. Chuẩn bị trước khi dùng

- **Quyền cần có:** không cần quyền đặc biệt. Đây là **luật nghiệp vụ**, không phải
  phân quyền — kể cả Quản trị hệ thống cũng bị chặn như mọi người.
- **Không phải bật gì cả.** Tính năng chạy tự động trên mọi phiếu xuất.
- **Dữ liệu liên quan:** phần giữ chỗ đến từ ô *Ghim tồn khả dụng* trên Đơn hàng bán
  (xem tài liệu *Kiểm tra tồn kho và nguồn lực trên Đơn bán hàng*).
- Cấu hình kho: xem [chan-xuat-kho-qua-ton-kha-dung-cau-hinh.md](chan-xuat-kho-qua-ton-kha-dung-cau-hinh.md)

---

## 3. Các bước thực hiện

Bạn **không thao tác gì thêm** — cứ lập phiếu như bình thường. Tính năng chỉ lên
tiếng khi có vấn đề. Phần dưới mô tả điều sẽ xảy ra.

### Bước 1 — Lập phiếu xuất như thường lệ

1. Vào **Tồn kho > Phiếu xuất kho hàng bán** (hoặc bất kỳ chứng từ nào ở mục 6.2)
2. Bấm **Thêm mới**
3. Điền **Khách hàng**, chọn **Mã hàng**, **Số lượng**, **Kho**

### Bước 2 — Lưu phiếu

Bấm **Lưu** (hoặc `Ctrl+S`). Lưu thì **không bao giờ bị chặn** — bạn cứ soạn thoải mái.

> ⚠️ Ô *Giờ hạch toán* tự cập nhật mỗi lần mở phiếu, nên phiếu hay ở trạng thái
> *Chưa lưu* và nút chính là **Lưu** chứ không phải **Gửi**. Bấm **Lưu** một lượt
> nữa thì nút **Gửi** mới hiện ra. Đây là cách ERPNext hoạt động, không phải lỗi.

### Bước 3 — Gửi duyệt

Bấm **Gửi**, rồi **Đồng ý** ở hộp xác nhận.

- Hàng còn đủ → phiếu chuyển sang **ĐÃ DUYỆT**, kho trừ bình thường.
- Hàng đã có người giữ → hiện hộp đỏ **Xuất quá tồn khả dụng**, phiếu **vẫn ở bản nháp**,
  kho **không bị trừ**. Xem mục 5.

---

## 4. Kiểm tra kết quả

Phiếu đi qua được thì trạng thái ở đầu màn hình đổi thành **ĐÃ DUYỆT** và có
thông báo xanh *"Delivery Note has been submitted successfully"*.

Muốn biết trước một mặt hàng còn xuất được bao nhiêu, **đừng đoán**: mở Đơn hàng
bán bất kỳ, bấm **Kiểm Tra Tồn Kho**, xem cột **Tồn khả dụng** ở Bảng 1. Đó chính
là con số tính năng này dùng để chặn.

---

## 5. Thông báo lỗi thường gặp

| Thông báo | Nguyên nhân | Cách xử lý |
|---|---|---|
| **Xuất quá tồn khả dụng**<br>*"Không xuất được: tồn khả dụng không đủ.*<br>*• `<mã hàng>`: xuất `<số>`, tồn khả dụng còn `<số>`*<br>*Phần chênh đang được các Đơn Bán khác giữ chỗ."* | Số bạn muốn xuất lớn hơn phần hàng còn tự do. Phần chênh đang bị các Đơn hàng bán khác **ghim** | Ba đường: **(a)** giảm số lượng trên phiếu xuống đúng mức *tồn khả dụng còn* mà câu lỗi ghi; **(b)** đợi hàng mua về; **(c)** liên hệ người phụ trách đơn đang giữ để họ **bỏ ghim** phần bạn cần |
| **Tồn khả dụng không đủ** *(màu cam, trên Yêu cầu mặt hàng)*<br>*"`<N>` mặt hàng đang xin nhiều hơn tồn khả dụng: `<danh sách>`.*<br>*Vẫn lập được phiếu, nhưng lúc xuất kho thật sẽ bị chặn nếu tồn chưa về kịp."* | Bạn lập Yêu cầu mặt hàng loại *Xuất vật tư* cho phần chưa có hàng | **Không phải lỗi** — đây chỉ là nhắc trước. Phiếu vẫn lập được. Nhưng hãy lo nguồn hàng trước ngày xuất, nếu không lúc xuất thật sẽ bị chặn |
| *"Chưa có bộ đọc tồn cho chứng từ `<tên>` — báo đội kỹ thuật, đừng bỏ qua."* | Lỗi lập trình, không phải do bạn nhập sai | **Báo đội kỹ thuật.** Đừng tìm cách lách — thà chặn nhầm một chứng từ hiếm còn hơn để hàng xuất lọt mà không ai kiểm |

> **Câu lỗi cố ý không nêu tên đơn đang giữ.** Anh Thắng chốt ngày 25/08: *"chỉ cần
> báo là tồn đang không đủ thôi"* — vì màn hình xuất kho mà hiện quá nhiều thông tin
> thì rối. Muốn biết **ai** đang giữ, mở Đơn hàng bán → **Kiểm Tra Tồn Kho** → bấm
> vào con số ở cột *Đơn khác giữ* để bung Bảng 1b.

---

## 6. Câu hỏi thường gặp

**Hỏi:** Tôi là Quản trị hệ thống, sao vẫn bị chặn?
**Đáp:** Đúng như thiết kế. Đây là **luật nghiệp vụ**, không phải phân quyền — hàng
đã có chủ thì ai cũng không lấy được. Đã kiểm chứng: chặn y hệt nhau ở mọi vai trò.

**Hỏi:** Những chứng từ nào bị kiểm?
**Đáp:** Tám chứng từ có thể làm giảm tồn:
Phiếu xuất kho hàng bán · Hóa đơn bán hàng *(khi có tích Cập nhật tồn kho)* ·
Phiếu Nhập Kho Hàng Mua *(bản trả hàng)* · Hóa Đơn Mua Hàng *(bản trả hàng)* ·
Chứng từ kho nội bộ · Đối soát tồn kho *(dòng điều chỉnh giảm)* ·
Subcontracting Receipt · Hạch toán tài sản.

**Hỏi:** Chuyển kho nội bộ có bị chặn không?
**Đáp:** Không, nếu chuyển giữa hai kho đều nằm trong tập kho hợp lệ — lấy ra ở đây,
nhập vào ở kia, tổng không đổi. Chỉ bị tính là *rút hàng* khi chuyển sang kho ngoài
tập đó, ví dụ **Kho Sản xuất**.

**Hỏi:** Đơn của tôi đang ghim, tôi xuất hàng cho chính đơn đó có bị chặn không?
**Đáp:** Không. Hệ thống nhận ra phiếu đang thực hiện đơn nào và **miễn trừ** phần
đơn đó tự giữ. Áp dụng cho cả phiếu xuất vật tư đi sản xuất theo **Lệnh sản xuất**
của đơn ấy.

**Hỏi:** Tại sao Yêu cầu mặt hàng chỉ cảnh báo mà không chặn?
**Đáp:** Vì nó chưa lấy hàng đi đâu cả — nó là một *dự định*. Bạn hoàn toàn có quyền
xin cho phần chưa có hàng; đó chính là việc của phiếu này.

**Hỏi:** Sau khi bị chặn, phiếu của tôi có mất không?
**Đáp:** Không. Phiếu vẫn nguyên ở **bản nháp**, kho không bị trừ dòng nào. Sửa số
lượng rồi **Lưu** và **Gửi** lại.
