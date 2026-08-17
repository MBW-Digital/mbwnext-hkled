# Hướng dẫn cấu hình: Bậc Thợ & Lịch Sản Xuất

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Quản trị hệ thống, tư vấn triển khai — làm **một lần** lúc go-live
> **Cập nhật:** 2026-08-11
> **Mục đích:** Khai xong các danh mục nền để bộ phận sản xuất dùng được tính năng Bậc Thợ &
> Lịch Sản Xuất. Người dùng hằng ngày đọc file
> [bac-tho-lich-san-xuat-van-hanh.md](bac-tho-lich-san-xuat-van-hanh.md).

---

## Mục lục

1. [Cần khai những gì](#1-cần-khai-những-gì)
2. [Bước 1 — Bậc Thợ](#2-bước-1--bậc-thợ)
3. [Bước 2 — Ca làm việc](#3-bước-2--ca-làm-việc)
4. [Bước 3 — Thời Gian Sản Xuất của mặt hàng](#4-bước-3--thời-gian-sản-xuất-của-mặt-hàng)
5. [Bước 4 — Đội Sản Xuất](#5-bước-4--đội-sản-xuất)
6. [Bước 5 — Hồ sơ nhân sự](#6-bước-5--hồ-sơ-nhân-sự)
7. [Phân quyền](#7-phân-quyền)
8. [Kiểm tra đã cấu hình đủ chưa](#8-kiểm-tra-đã-cấu-hình-đủ-chưa)
9. [Thông báo lỗi thường gặp](#9-thông-báo-lỗi-thường-gặp)

---

## 1. Cần khai những gì

Năm danh mục dưới đây phải khai **theo đúng thứ tự**, vì cái sau tham chiếu cái trước.

| Thứ tự | Danh mục | Vì sao cần |
|---|---|---|
| 1 | **Bậc Thợ** (*Employee Level*) | quyết định năng lực và tiền lương từng người |
| 2 | **Shift Type** (ca làm việc) | khung giờ để hệ thống xếp lịch |
| 3 | **Thời Gian Sản Xuất (Phút)** trên mặt hàng | không có thì không tính được thời gian hoàn thành |
| 4 | **Đội Sản Xuất** (*Work Team*) | để tạo lịch hàng loạt và gán cả đội vào lệnh |
| 5 | Hồ sơ **nhân sự** | nối 3 thứ trên vào từng người |

Thiếu bất kỳ mục nào, người dùng vẫn mở được màn hình nhưng sẽ vấp lỗi lúc tính lịch. Mục 9
liệt kê đúng câu lỗi tương ứng với từng thứ còn thiếu.

---

## 2. Bước 1 — Bậc Thợ

Bậc Thợ là bảng năng lực và đơn giá nhân công. Mỗi bậc khai một lần, dùng cho mọi nhân sự.

1. Thanh tìm kiếm → gõ `Employee Level` → **Add Employee Level**
2. Điền:

   | Trường | Ý nghĩa | Ví dụ |
   |---|---|---|
   | **Bậc Thợ** | tên bậc, cũng là mã bản ghi | `Bậc 7` |
   | **Lương Mỗi Phút** | đơn giá nhân công tính theo phút | `1.080` |
   | **Nguồn Lực (%)** | năng suất so với chuẩn 100% | `100` |
   | **Tỉ Lệ Đóng Quỹ Đội (%)** | phần trích quỹ đội | theo quy định công ty |

3. **Save**

> ⚠️ **Nguồn Lực (%)** là con số ảnh hưởng trực tiếp tới thời gian hoàn thành lệnh sản xuất.
> Ba người 100% + 100% + 90% cho năng lực 2,9 lần một người chuẩn. Khai sai chỗ này thì mọi lịch
> sản xuất đều lệch, mà không có cảnh báo nào.

**Lương Mỗi Phút** dùng để tính tiền công trong Công Việc Khác. Đây là số nhạy cảm — cân nhắc
trước khi cấp quyền xem `Employee Level` cho người ngoài bộ phận nhân sự.

---

## 3. Bước 2 — Ca làm việc

Hệ thống chỉ xếp việc vào **trong khung giờ ca**. Ngoài ca thì coi như người đó không làm việc.

1. Thanh tìm kiếm → gõ `Shift Type` → **Add Shift Type**
2. Khai tên ca, **Start Time**, **End Time**
3. **Save**

HKLED đang dùng hai ca:

| Ca | Giờ |
|---|---|
| Ca Sáng | 08:00 – 11:45 |
| Ca Chiều | 13:15 – 17:00 |

Việc **tăng ca** không khai ở đây — người dùng nhập trực tiếp giờ bắt đầu/kết thúc trên từng
Lịch Làm Việc.

---

## 4. Bước 3 — Thời Gian Sản Xuất của mặt hàng

Trên mỗi **thành phẩm** cần sản xuất:

1. Mở **Item** → tìm mặt hàng
2. Điền **Thời Gian Sản Xuất (Phút)** — số phút làm ra **một** sản phẩm ở năng lực chuẩn 100%
3. **Save**

Đây là con số nhân với số lượng để ra tổng khối lượng công việc. Ví dụ 20 cái × 10 phút = 200
phút công chuẩn; chia cho năng lực đội 2,9 ra **69 phút** thực tế.

Mặt hàng chưa khai thì lúc bấm **Tính Lại Lịch** sẽ bị chặn (xem mục 9).

---

## 5. Bước 4 — Đội Sản Xuất

1. Thanh tìm kiếm → gõ `Work Team` → **Add Work Team**
2. Điền **Tên Đội Sản Xuất** — tên này chính là mã bản ghi, đặt xong nên hạn chế đổi
3. **Đang Hoạt Động** để bật (mặc định đã bật)
4. **Save**

> ⚠️ Đội tắt **Đang Hoạt Động** sẽ **không hiện** trong ô chọn đội ở hộp thoại Tạo Nhanh và nút
> Thêm Đội Sản Xuất. Dùng cách này để ngừng một đội cũ thay vì xoá — xoá đội đang được tham chiếu
> sẽ bị hệ thống chặn.

Đội **không** ràng buộc gì về sau: người dùng thêm cả đội vào lệnh sản xuất rồi vẫn xoá/sửa từng
dòng tự do, và nhân sự chuyển đội sau đó không làm đổi các lệnh đã tạo.

---

## 6. Bước 5 — Hồ sơ nhân sự

Với **từng công nhân**, mở **Employee** và khai:

| Trường | Giá trị | Bắt buộc |
|---|---|---|
| **Loại Nhân Sự** | `Công nhân` | có |
| **Bậc Thợ** | chọn từ danh mục bước 1 | **bắt buộc khi Loại Nhân Sự = Công nhân** |
| **Đội Sản Xuất** | chọn từ bước 4 | cần, nếu muốn dùng Tạo Nhanh và Thêm Đội |
| **Status** | `Active` | có |

**Nguồn Lực (%)** tự lấy theo Bậc Thợ, không nhập tay.

> ⚠️ Ràng buộc Bậc Thợ được kiểm **ở cả giao diện và máy chủ**. Nhập liệu hàng loạt bằng import
> hay API mà bỏ trống Bậc Thợ vẫn bị chặn — đúng như ý đồ, vì thiếu Bậc Thợ là không tính được
> lịch lẫn lương.

Chỉ nhân sự **Active**, **Loại Nhân Sự = Công nhân** và có Đội mới xuất hiện trong danh sách
Tạo Nhanh. Người khai thiếu một trong ba điều kiện sẽ lặng lẽ không có trong danh sách — đây là
nguyên nhân phổ biến nhất khi người dùng báo "đội của tôi không thấy ai".

---

## 7. Phân quyền

Quyền mặc định đã cài sẵn theo vai trò, thường không cần chỉnh:

| Đối tượng | `System Manager` | `Manufacturing Manager` | `Manufacturing User` | `HR Manager` |
|---|---|---|---|---|
| Đội Sản Xuất | toàn quyền | tạo/sửa/xem | chỉ xem | — |
| Lịch Làm Việc | toàn quyền | toàn quyền | tạo/sửa/xem | — |
| Bậc Thợ | toàn quyền | chỉ xem | chỉ xem | tạo/sửa/xem |
| Công Việc Khác | toàn quyền | toàn quyền | tạo/sửa/xem | — |
| Phân Công Nhân Sự | toàn quyền | toàn quyền | chỉ xem | — |

Bậc Thợ giao cho `HR Manager` giữ vì trong đó có đơn giá lương.

**Nếu công ty có phân quyền theo phạm vi nhân sự** (User Permission trên Employee): chức năng
Tạo Nhanh **tôn trọng đúng phạm vi đó** — người dùng chỉ thấy và chỉ tạo được lịch cho nhân sự
mình được phép. Chọn nhầm người ngoài phạm vi thì bị chặn cả lô kèm tên người vi phạm, chứ hệ
thống **không** âm thầm bỏ bớt.

---

## 8. Kiểm tra đã cấu hình đủ chưa

Làm thử một vòng, hết khoảng 5 phút:

1. Mở `Employee Schedule` → bấm **Tạo Nhanh** → chọn đội vừa khai.
   → Danh sách phải hiện **đủ** công nhân của đội, kèm Bậc thợ và Nguồn lực (%) khác 0.
2. Chọn một khoảng ngày ngắn → dòng chữ dưới danh sách phải báo đúng số lịch sắp tạo.
3. Tạo thử một Lệnh Sản Xuất cho mặt hàng đã khai Thời Gian Sản Xuất, thêm đội vào, bấm
   **Tính Lại Lịch** → phải ra được **Tổng Thời Gian Dự Kiến (Phút)** và giờ kết thúc.

Ba bước trên chạy trơn nghĩa là cấu hình đã đủ.

---

## 9. Thông báo lỗi thường gặp

Bảng này dành cho lỗi **do cấu hình thiếu**. Lỗi thao tác hằng ngày xem trong file vận hành.

| Thông báo | Nguyên nhân | Cách xử lý |
|---|---|---|
| *Nhân sự **X** là Công nhân nên bắt buộc phải có Bậc Thợ* | Hồ sơ nhân sự để Loại Nhân Sự = Công nhân nhưng bỏ trống Bậc Thợ | Mở **Employee** của người đó, chọn **Bậc Thợ**, lưu lại |
| *Mặt hàng **X** chưa thiết lập Thời Gian Sản Xuất (Phút)* | Thành phẩm chưa khai số phút sản xuất một cái | Mở **Item** đó, điền **Thời Gian Sản Xuất (Phút)**, lưu lại |
| *Row #N: Nhân sự **X** chưa có Nguồn Lực (%) hợp lệ* | Nhân sự chưa có Bậc Thợ, hoặc Bậc Thợ để Nguồn Lực (%) = 0 | Kiểm **Bậc Thợ** của người đó; mở danh mục **Employee Level** kiểm **Nguồn Lực (%)** khác 0 |
| *Row #N: Không tìm thấy khoảng thời gian làm việc hợp lệ nào cho nhân sự **X*** | Người đó chưa có Lịch Làm Việc nào từ thời điểm bắt đầu trở đi | Dùng **Tạo Nhanh** tạo lịch cho khoảng ngày tương ứng |
| *Không đủ Lịch làm việc của nhân sự để hoàn thành khối lượng công việc. Vui lòng bổ sung thêm nhân sự hoặc Lịch làm việc.* | Tổng giờ có lịch ít hơn khối lượng cần làm | Tạo thêm lịch cho những ngày tiếp theo, hoặc thêm người vào lệnh |
| *Không tìm thấy Ca Làm Việc **X*** | Ca bị xoá hoặc đổi tên sau khi đã dùng | Khai lại **Shift Type** đúng tên, hoặc chọn ca khác |
| *Bạn không có quyền tạo lịch cho nhân sự: **X*** | Người dùng bị giới hạn phạm vi nhân sự, trong lô có người ngoài phạm vi | Bỏ chọn những người đó, hoặc cấp thêm quyền cho tài khoản |

---

## Liên quan

- [Hướng dẫn vận hành](bac-tho-lich-san-xuat-van-hanh.md) — thao tác hằng ngày
- [Biểu đồ tình hình làm việc của nhân sự](bieu-do-gantt-lich-lam-viec-van-hanh.md) — màn hình xem lịch đã xếp
- Đầu bài và thiết kế: `apps/mbwnext_hkled/docs/features/bac-tho-lich-san-xuat.md`
