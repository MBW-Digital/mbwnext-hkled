# Test case — Biểu đồ tình hình làm việc của nhân sự (PM-FEAT-00009)

**App:** `mbwnext_hkled` (tầng 4) · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Màn hình:** `/app/bieu-do-lich-lam-viec` — *Tình hình làm việc của nhân sự*
**Ngày chạy vòng tự kiểm:** 08/08/2026 · **Người chạy:** Claude (Trợ lý)

## Điều kiện chuẩn bị

Bộ dữ liệu thật đang có sẵn trên site, **không cần dựng thêm**:

| Ngày | Có gì | Dùng để kiểm |
|---|---|---|
| **29/07/2026** | Anh A: WO-00004 cả ngày · Anh B: chỉ ca chiều · Anh C: WO-00001 rồi WO-00004 | luồng chính, cắt nghỉ trưa, thiếu ca, 2 lệnh nối nhau |
| **31/07/2026** | không ai có lịch | ngày rỗng |
| **08/08/2026** | có lịch, không có phân công | toàn bộ rảnh |

Nhân sự: `Anh A` (Bậc 7, Đội 1), `Anh B` (Bậc 7, Đội 1), `Anh C` (Bậc 6, Đội 1). Đội 2 chưa có ai.
Ca Sáng 08:00–11:45, Ca Chiều 13:15–17:00.

⚠ Đây là **site dùng chung** — ai chạy test có tạo dữ liệu thì dọn sạch sau khi xong.

---

## TC-HAPPY — luồng đúng

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Mở được màn hình | Vào `/app/bieu-do-lich-lam-viec` | Hiện tiêu đề *Tình hình làm việc của nhân sự*, ô chọn ngày mặc định **hôm nay**, bộ lọc đội, chú giải 4 màu | Pass (**giao diện**) | Pass |
| TC-HAPPY-02 | Vẽ đúng ngày có việc | Đổi ngày sang **29-07-2026** | 3 dòng nhân sự, mỗi dòng ghi *Bậc thợ · Đội* dưới tên | Pass — Anh A/B/C, Bậc 7·Đội 1, Bậc 7·Đội 1, Bậc 6·Đội 1 (**giao diện**) | Pass |
| TC-HAPPY-03 | **Cắt nghỉ trưa** — ca quan trọng nhất | Xem dòng **Anh A** ngày 29/07 | **Hai** thanh đỏ `08:00–11:45` và `13:15–17:00`, **ở giữa là khoảng xám**. Trong CSDL đây chỉ là MỘT bản ghi phân công liền mạch 08:00→17:00 | Pass — đúng 2 thanh, giữa xám (**giao diện**) | Pass |
| TC-HAPPY-04 | Hai lệnh nối nhau trong một ca | Xem dòng **Anh C** ngày 29/07 | `08:00–10:00` WO-00001, `10:00–11:45` WO-00004, `13:15–17:00` WO-00004 | Pass — đúng 3 thanh, đúng mã lệnh (**giao diện**) | Pass |
| TC-HAPPY-05 | Rảnh khi có ca mà chưa có việc | Xem ngày **08-08-2026** | Cả 3 người: 2 thanh **xanh** *Rảnh (08:00 – 11:45)* và *Rảnh (13:15 – 17:00)* | Pass (**giao diện**) | Pass |
| TC-HAPPY-06 | Chi tiết khi rê chuột | Rê lên một thanh đỏ | Hiện tên nhân sự, mã lệnh, mặt hàng × số lượng, trạng thái lệnh, khoảng giờ và tên ca | Pass — vd. *Anh A · MFG-WO-2026-00004 / Thành phẩm 1 × 100 / Draft / 08:00 – 11:45 · Ca Sáng* (**giao diện**) | Pass |
| TC-HAPPY-07 | Bấm thanh đỏ mở Lệnh sản xuất | Bấm thanh của Anh A | Chuyển sang form `MFG-WO-2026-00004` | Pass (**giao diện**) | Pass |
| TC-HAPPY-08 | Lọc theo đội | Tích **Đội 1** | Vẫn đủ 3 người (cả 3 thuộc Đội 1) | Pass (**giao diện**) | Pass |
| TC-HAPPY-09 | Bỏ hết tích = hiện tất cả | Bỏ tích Đội 1 | Quay lại hiện đủ 3 người | Pass (**giao diện**) | Pass |
| TC-HAPPY-11 | **PM-TASK-00051** — tooltip có Khách hàng và NV bán hàng | Rê lên thanh đỏ của lệnh **có gắn Đơn Bán Hàng** | Thêm 2 dòng *Khách hàng: …* và *NV bán hàng: …*, nằm giữa dòng mặt hàng và dòng trạng thái | Pass | Pass |
| TC-HAPPY-12 | **PM-TASK-00053** — chọn khoảng nhiều ngày | Đặt **Từ ngày** 29/07, **Đến ngày** 31/07 | Trục chia thành 3 dải ngày có nhãn `29/07 · 30/07 · 31/07`, mỗi dải vẫn là khung 08:00–24:00 | Pass — trục 0–2880 phút, đoạn của 30/07 nằm đúng dải thứ hai (**giao diện**) | Pass |
| TC-HAPPY-13 | **PM-TASK-00053** — cột rảnh/tổng (%) | Xem cột **Rảnh** bên trái mỗi dòng | Hiện `%` kèm `rảnh / tổng phút` theo đúng khoảng đang lọc | Pass — 3 ngày: Anh A `41% · 371/900`, Anh B `55% · 371/675` (**giao diện**) | Pass |
| TC-HAPPY-14 | **PM-TASK-00053** — biểu đồ co vừa màn hình | Chọn khoảng 8 ngày rồi 31 ngày | **Không** có thanh cuộn ngang | Pass — `scrollWidth = clientWidth` ở cả 8 và 31 ngày (**giao diện**) | Pass |

## TC-VALID — kiểm tra dữ liệu

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | Không có tham số ngày | Gọi `get_timeline()` không truyền `date` | Lấy **hôm nay**, không báo lỗi | Pass (API) | Pass |
| TC-VALID-02 | Trục giờ cố định | Đọc `truc_tu` / `truc_den` | **480 / 1440** phút = 08:00–24:00, không đổi theo dữ liệu | Pass (API) | Pass |
| TC-VALID-03 | **PM-TASK-00053** — khoảng quá dài | Gọi API với khoảng 365 ngày | Chặn kèm câu nêu rõ giới hạn | Pass — *"Khoảng ngày tối đa là 31 ngày. Đang chọn 365 ngày."* (API server) | Pass |

## TC-EDGE — biên & ngoại lệ

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | **Người không có lịch vẫn hiện** (chốt C2, 11:23) | Xem ngày **31-07-2026** | Vẫn đủ **3 dòng**, phần thời gian xám toàn bộ, có chữ *"Không có lịch làm việc trong ngày này"* | Pass — 3 người, `co_lich = false`, 0 đoạn (API + **giao diện**) | Pass |
| TC-EDGE-02 | Nhân sự thiếu một ca | Xem dòng **Anh B** ngày 29/07 | Buổi sáng **xám** (không có ca), chỉ có thanh chiều. Xám ≠ rảnh | Pass (**giao diện**) | Pass |
| TC-EDGE-03 | Đội không có ai | Tích **Đội 2** | Hiện *"Không có nhân sự nào thuộc đội đã chọn."*, không báo lỗi đỏ | Pass (**giao diện**) | Pass |
| TC-EDGE-04 | Phân công trải nhiều ngày | Xem 29/07 dòng Anh B (phân công thật chạy tới 08:28 hôm sau) | Chỉ vẽ phần thuộc ngày đang xem, **không** tràn sang cột đêm | Pass (**giao diện**) | Pass |
| TC-EDGE-05 | Nhãn trên thanh hẹp | Xem thanh `10:00–11:45` của Anh C | Nhãn rút gọn còn `WO-00004` thay vì bị cắt cụt giữa chừng; chi tiết đầy đủ vẫn có khi rê chuột | Pass (**giao diện**) | Pass |
| TC-EDGE-06 | Số lượng trong tooltip | Rê lên thanh của lệnh có qty = 100 | Hiện **`× 100`** | ⚠ Vòng đầu **Fail**: hiện `× 100,000` do site để 3 chữ số thập phân, dễ đọc nhầm thành một trăm nghìn. Đã bỏ phần thập phân khi là số nguyên; chạy lại ra `× 100` (**giao diện**) | Pass |
| TC-EDGE-07 | **PM-TASK-00051** — lệnh không gắn Đơn Bán Hàng | Rê lên thanh đỏ của lệnh tạo tay | **Bỏ hẳn** 2 dòng đó, không hiện nhãn với giá trị rỗng | Pass — API trả `null`, tooltip chỉ còn 4 dòng như cũ | Pass |
| TC-EDGE-08 | **PM-TASK-00053** — khoảng càng dài, nhãn giờ càng thưa | Lần lượt 1 · 3 · 7 · 8 ngày | 1 ngày: nhãn mỗi giờ · 2–3 ngày: mỗi 2 giờ · 4–7 ngày: mỗi 4 giờ · trên 7 ngày: **chỉ còn nhãn ngày** | Pass (**giao diện**) | Pass |
| TC-EDGE-09 | **PM-TASK-00053** — chọn Từ ngày muộn hơn Đến ngày | Đặt Từ ngày = 31/07 khi Đến ngày = 29/07 | Kéo đầu kia theo cho bằng, **không** báo lỗi | Pass — người dùng gần như luôn muốn dời cả khoảng chứ không phải nhập sai (**giao diện**) | Pass |

## TC-PERM — phân quyền

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-PERM-01 | Vai trò được vào trang | Kiểm `Has Role` của Page | Đúng 3 vai trò: `System Manager`, `Manufacturing Manager`, `Manufacturing User` | Pass (API) | Pass |
| TC-PERM-02 | 🔴 **Rò rỉ nhân sự ngoài quyền** | Chạy `get_timeline` và `get_team_members` dưới user `test.gioihan.nhansu@hkled.test` (vai trò `Manufacturing User`, User Permission giới hạn Employee = `Anh A`) | Chỉ hiện đúng nhân sự trong quyền, **không** lộ người khác | **Pass** — Administrator thấy `Anh A/B/C`, user bị giới hạn chỉ thấy `Anh A` ở **cả hai** chỗ: biểu đồ và hộp thoại Thêm Đội Sản Xuất. % thời gian rảnh cũng chỉ tính trên nhân sự trong quyền (450 phút / 83%) (API server) | Pass |
| TC-PERM-03 | Chỉ được xem một phần Lệnh sản xuất | Chạy `get_timeline` dưới user `test.gioihan.lenh@hkled.test` (User Permission giới hạn Work Order = `MFG-WO-2026-00004`) | *(dự đoán ban đầu)* vẫn thấy thanh đỏ và mã lệnh, chỉ ẩn mặt hàng/số lượng | ⚠ **Thực tế KHÁC dự đoán — xem mục "Điểm cần quyết" bên dưới.** Thanh đỏ của lệnh ngoài quyền **biến mất hoàn toàn**, khoảng đó chuyển thành **rảnh**. Nguyên nhân: User Permission đặt `apply_to_all_doctypes = 1` nên lọc luôn `Employee Allocation` (bảng này có trường Link tới Work Order), không chỉ lọc bảng Work Order | ⚠ |

⚠ **Chạy bằng `Administrator` không tính là đã test phân quyền.** Đây đúng loại lỗi đã xảy ra ở
PM-FEAT-00008: dialog chọn đội trả về cả nhân sự ngoài quyền, chỉ lộ ra khi đổi user rồi chạy lại.

Hai tài khoản dựng riêng để chạy 2 ca trên (08/08/2026), **cố ý không đặt mật khẩu** — chỉ dùng qua
`frappe.set_user()`, không đăng nhập được bằng trình duyệt:

| Tài khoản | Vai trò | User Permission |
|---|---|---|
| `test.gioihan.nhansu@hkled.test` | Manufacturing User | Employee = `Anh A` |
| `test.gioihan.lenh@hkled.test` | Manufacturing User | Work Order = `MFG-WO-2026-00004` |

Muốn test bằng trình duyệt thì người test tự đặt mật khẩu cho 2 tài khoản này.

### ⚠ Điểm cần quyết — phát hiện từ TC-PERM-03

Người dùng bị giới hạn chỉ xem được một số Lệnh sản xuất thì **không thấy thanh đỏ** của các lệnh
ngoài quyền, và khoảng thời gian đó hiện thành **rảnh** — tức là biểu đồ báo người đó đang rảnh
trong khi thực tế họ đang bận.

Đo được: Anh C ngày 29/07 dưới Administrator có 3 đoạn bận (WO-00001 rồi WO-00004); dưới user bị
giới hạn chỉ còn 2 đoạn của WO-00004, đoạn 08:00–10:00 biến mất.

Đây là **hành vi đúng theo cơ chế phân quyền của Frappe**, không phải lỗi code, và **không** ảnh
hưởng phần tính lịch (engine dùng `frappe.get_all`, không bị lọc — nên máy vẫn không xếp trùng).
Rủi ro nằm ở **người đọc**: quản lý bị giới hạn quyền có thể nhìn nhầm là nhân sự đang rảnh rồi
giao thêm việc.

Hai hướng, cần HKLED chọn:

1. **Giữ nguyên** — ai không được xem lệnh thì không thấy gì về lệnh đó. An toàn về dữ liệu nhất.
2. **Vẫn vẽ thanh bận nhưng ẩn chi tiết** — hiện đúng "người này đang bận" mà không nói bận lệnh
   nào, mặt hàng gì. Muốn vậy phải đọc `Employee Allocation` bằng `frappe.get_all` (bỏ qua User
   Permission) rồi tự che phần thông tin lệnh. Lộ ra mức "đang bận", giấu phần còn lại.

Chưa chốt thì để nguyên phương án 1 (mặc định hiện tại).

## TC-REGR — không làm hỏng cái đang chạy

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Không đụng dữ liệu | Mở biểu đồ, đổi ngày, đổi bộ lọc nhiều lần | **Không** bản ghi nào bị tạo/sửa/xoá — màn hình chỉ đọc | Pass — tổng Employee Allocation trước và sau đều **33** (API) | Pass |
| TC-REGR-02 | Nút Tính Lại Lịch vẫn chạy | Mở một Lệnh sản xuất, bấm *Tính Lại Lịch* | Chạy như trước, không lỗi | Pass (**giao diện**, khi kiểm PM-TASK-00045) | Pass |
| TC-REGR-03 | Không thêm Custom Field nào | So `fixtures/custom_field.json` trước/sau | Không thay đổi | Pass — tính năng không phát sinh Custom Field | Pass |

## TC-ISO — cách ly app khách

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-ISO-01 | Không rò sang site khách khác | Kiểm trang chỉ tồn tại khi cài `mbwnext_hkled` | Page thuộc module **MBWNext HKLed**; site không cài app này thì không có trang | Pass — `module = "MBWNext HKLed"`, `standard = Yes` (API) | Pass |
| TC-ISO-02 | Không hook vào app lõi | `grep` `hooks.py` | Tính năng **không** thêm `doc_events`/`override` nào — chỉ 1 hàm whitelisted + 1 Desk Page | Pass | Pass |

---

## Kết luận

- Tổng: **31** — Pass: **30** — Fail: **0** — Cần quyết định: **1** (TC-PERM-03)
- **Cập nhật 08/08 (vòng 2):** đã dựng 2 tài khoản bị giới hạn quyền và chạy nốt 2 ca còn treo.
  `TC-PERM-02` **Pass** — không rò rỉ nhân sự ngoài quyền, cả ở biểu đồ lẫn hộp thoại Thêm Đội Sản
  Xuất. `TC-PERM-03` ra hành vi khác dự đoán ban đầu, không phải lỗi code nhưng cần HKLED chọn
  hướng — xem mục *"Điểm cần quyết"* ở phần TC-PERM.
- Hai lỗi phát hiện và **đã sửa** ngay trong vòng test, đã chạy lại Pass:
  1. **Trang dựng xong khung nhưng lưới trống trơn.** `frappe.freeze` **không tồn tại** trong
     Frappe v15 — hàm đúng là `frappe.dom.freeze()`. Gọi sai làm hàm tải dữ liệu chết ngay dòng
     đầu, mà màn hình **không báo gì cả**: vẫn đủ tiêu đề, ô chọn ngày, bộ lọc, chú giải màu.
     Nhìn ảnh chụp rất dễ kết luận nhầm là "không có dữ liệu". *Chỉ mở console mới thấy.*
  2. **Số lượng trong tooltip đọc dễ nhầm.** qty = 100 hiện thành `× 100,000` (site để 3 chữ số
     thập phân, dấu phẩy là dấu thập phân). Đúng cấu hình nhưng người Việt đọc rất dễ hiểu thành
     một trăm nghìn. Đã bỏ phần thập phân khi là số nguyên.
- **Đối chiếu với mockup khách đã duyệt**: ngày 29/07 trên màn hình thật khớp **từng mốc** với
  mockup — kể cả chỗ khó nhất là thanh đỏ của Anh A bị ngắt ở 11:45–13:15.
- **Đủ điều kiện nghiệm thu: CHƯA HOÀN TOÀN.** Còn **TC-PERM-02 và TC-PERM-03** chưa chạy được vì
  site chưa có user bị giới hạn quyền. Người test cần tạo một user như vậy (hoặc dùng
  `hkled@gmail.com` nếu đã gán User Permission) rồi chạy lại 2 ca đó — đây là loại lỗi từng xảy ra
  thật ở PM-FEAT-00008 nên **không được bỏ qua**.

## Dọn dẹp sau khi test

Vòng 08/08 không tạo dữ liệu mới cho tính năng này (chỉ đọc). Hai Lệnh sản xuất dựng để kiểm
PM-TASK-00045 đã xoá; tổng Employee Allocation về đúng **33** như trước khi test.
