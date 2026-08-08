# Test case — 4 việc làm ngày 08/08/2026 (PM-TASK-00046, 00047, 00049, 00050)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Ngày chạy vòng tự kiểm:** 08/08/2026 · **Người chạy:** Claude (Trợ lý)

Bốn task này khách ghi vào mục *Vấn đề phát sinh* nhưng thực chất là **yêu cầu tính năng mới**, nên
không có mockup duyệt trước. Bộ test dưới đây viết sau khi code xong.

| Task | Nội dung |
|---|---|
| PM-TASK-00046 | Ghi Chú Sản Xuất chảy từ Đơn Bán Hàng → dòng hàng → Assembly Items → Lệnh sản xuất |
| PM-TASK-00047 | Nút *Kế Hoạch Sản Xuất* trong menu **Create** của Đơn Bán Hàng |
| PM-TASK-00049 | % thời gian rảnh của đội trong hộp thoại *Thêm Đội Sản Xuất* |
| PM-TASK-00050 | Khách Hàng + Nhân Viên Bán Hàng trên Lệnh sản xuất |

## Dữ liệu chuẩn bị

Đơn thử **SAL-ORD-2026-00011** để lại trên site: ghi chú đầu đơn *"Sơn màu đen mờ, đóng gói riêng
từng bộ"*, dòng thứ hai sửa tay thành *"Dòng này khách dặn riêng: dán tem tiếng Anh"*.
Kéo theo **MFG-PP-2026-00008** và hai lệnh **MFG-WO-2026-00030 / 00031**.

⚠ Site dùng chung — ai tạo thêm chứng từ khi test thì dọn sau.

---

## TC-HAPPY — luồng đúng

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Ghi chú đầu đơn chảy xuống dòng hàng | Nhập **Ghi Chú Sản Xuất** ở đầu đơn, thêm 2 dòng hàng, Lưu | Cả 2 dòng nhận đúng ghi chú đầu đơn | Pass — cả 2 dòng nhận "Ghi chú A" (**giao diện**) | Pass |
| TC-HAPPY-02 | Sửa tay từng dòng | Sửa ghi chú của riêng dòng 2 | Dòng 2 giữ nội dung riêng, dòng 1 không đổi | Pass (**giao diện**) | Pass |
| TC-HAPPY-03 | 🔴 Đổi ghi chú đầu đơn **không** xoá phần đã sửa tay | Đổi ghi chú đầu đơn sang giá trị khác | Dòng chưa ai đụng đổi theo; **dòng đã sửa tay giữ nguyên**, kèm thông báo cam *"Giữ nguyên Ghi Chú Sản Xuất đã sửa tay ở N dòng hàng"* | Pass — `["Ghi chú B","Ghi chú B","Riêng dòng 2"]` (**giao diện**) | Pass |
| TC-HAPPY-04 | Dòng thêm sau cũng có ghi chú | Bấm **Add Row** trên lưới Items | Dòng mới nhận ghi chú đầu đơn hiện tại | Pass — nhận "Ghi chú B" (**giao diện**) | Pass |
| TC-HAPPY-05 | Nút tạo Kế hoạch sản xuất | Mở đơn **đã Duyệt** → **Create** → *Kế Hoạch Sản Xuất* | Mở form kế hoạch mới, đã điền sẵn trước khi Lưu | Pass — mục *Kế Hoạch Sản Xuất* nằm đầu menu Create (**giao diện**) | Pass |
| TC-HAPPY-06 | Kế hoạch mang đủ thông tin | Xem form vừa mở | 1 dòng Đơn Bán Hàng + các dòng Assembly Items; Thời Gian Bắt Đầu, Thời Điểm Cần Hoàn Thành, Ghi Chú Sản Xuất đều có | Pass — 2 dòng Assembly, `11-08 08:00`, `20-08 16:30`, ghi chú đủ (**giao diện**) | Pass |
| TC-HAPPY-07 | Ghi chú ghép **theo từng dòng** | Xem bảng Assembly Items | Mỗi dòng mang ghi chú của **đúng dòng hàng tương ứng**, không áp chung một ghi chú | Pass — dòng qty 3 mang ghi chú riêng, dòng qty 2 mang ghi chú đầu đơn (API server) | Pass |
| TC-HAPPY-08 | Ghi chú tới Lệnh sản xuất | Duyệt kế hoạch → tạo Lệnh sản xuất | Mỗi lệnh nhận ghi chú của dòng Assembly Items sinh ra nó | Pass — WO-00030 (qty 3) "dán tem tiếng Anh", WO-00031 (qty 2) ghi chú đầu đơn (API server) | Pass |
| TC-HAPPY-09 | % thời gian rảnh của đội | Lệnh có đủ 2 mốc thời gian → **Thêm Đội Sản Xuất** → chọn đội | Dưới ô chọn đội hiện % rảnh của cả đội kèm số phút; bảng nhân sự có thêm cột **Rảnh (phút)** | Pass — MFG-WO-2026-00019 hiện **98%**, rảnh 1.566/1.603 phút; từng người 515/534, 525/534, 526/534 (**giao diện**) | Pass |
| TC-HAPPY-10 | Khách hàng + NV bán hàng trên lệnh | Mở lệnh có gắn Đơn Bán Hàng | Hai ô **Khách Hàng** và **Nhân Viên Bán Hàng** hiện đúng giá trị của đơn | Pass — sau khi sửa lỗi ở TC-VALID-03 (**giao diện**) | Pass |

## TC-VALID — kiểm tra dữ liệu và ràng buộc

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | Ghi chú điền cả khi tạo bằng máy | Tạo đơn bằng script/API có ghi chú đầu đơn, dòng hàng để trống | Dòng hàng vẫn được điền — không phụ thuộc thao tác trên giao diện | Pass (API server) | Pass |
| TC-VALID-02 | Đơn không có gì để sản xuất | Bấm **Create > Kế Hoạch Sản Xuất** trên đơn mà mặt hàng chưa có BOM đang hoạt động, hoặc đã tạo lệnh hết số lượng | Chặn lại kèm câu giải thích, **không** tạo ra kế hoạch rỗng | Pass — hiện câu nêu rõ 2 nguyên nhân cần kiểm (API server) | Pass |
| TC-VALID-03 | 🔴 Lệnh sản xuất phải luôn có Thời Gian Bắt Đầu | Đơn **không** khai Thời Gian Bắt Đầu → kế hoạch → tạo lệnh → mở lệnh sửa gì đó rồi **Lưu** | Lưu được bình thường | ⚠ Vòng đầu **Fail** — chi tiết ở `bac-tho-lich-san-xuat.md`, TC-EDGE-18/19/20. Đã sửa, chạy lại Pass | Pass |

## TC-EDGE — biên & ngoại lệ

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | Nút Create ẩn với đơn nháp | Mở đơn còn **Nháp** | Không có mục *Kế Hoạch Sản Xuất* trong menu Create | Pass — chỉ hiện khi `docstatus = 1`, vì hàm lấy dòng hàng của ERPNext lọc theo dòng đã duyệt (**giao diện**) | Pass |
| TC-EDGE-02 | Chưa đủ mốc thời gian thì không tính % | Lệnh **chưa** điền Thời Gian Bắt Đầu / Thời Điểm Cần Hoàn Thành → mở hộp thoại Thêm Đội | Hiện câu nhắc *"Điền Thời Gian Bắt Đầu và Thời Điểm Cần Hoàn Thành của lệnh để xem % thời gian rảnh của đội"*, không hiện % và không hiện cột Rảnh | Pass (API server) | Pass |
| TC-EDGE-03 | Khoảng thời gian ngược đầu | Thời Điểm Cần Hoàn Thành **sớm hơn** Thời Gian Bắt Đầu | Không tính, không vỡ | Pass — trả về rỗng (API server) | Pass |
| TC-EDGE-04 | 🔴 Phân công xuyên đêm chỉ tính phần trong ca | Khoảng 30/07 08:00–17:00, Anh B có phân công chạy từ 29/07 13:15 tới 30/07 08:28 | Chỉ **28 phút** thuộc ca sáng được tính là bận, không tính cả đêm | Pass — mỗi người 450 phút, bận ~79, rảnh 371, cả đội **83%** — khớp tính tay (API server) | Pass |
| TC-EDGE-05 | Đội bận kín | Khoảng 29/07 08:00–17:00 | **0%** | Pass (API server) | Pass |
| TC-EDGE-06 | Không trừ phần chính lệnh đang mở giữ chỗ | Lệnh đã có phân công cho đội đó, mở lại hộp thoại Thêm Đội | Phần thời gian do **chính lệnh này** chiếm không bị tính là bận | Pass — truyền `exclude_work_order` (API server) | Pass |
| TC-EDGE-07 | Lệnh không gắn Đơn Bán Hàng | Tạo lệnh tay, không chọn đơn | Khách Hàng và Nhân Viên Bán Hàng để trống, không báo lỗi | Pass (API server) | Pass |
| TC-EDGE-08 | Chỉ lấy theo ô `sales_person` | Gán người bán vào **Sales Person** của đơn → tạo/lưu lệnh | Lệnh lấy đúng người đó | Pass (API server) | Pass |
| TC-EDGE-09 | 🔴 Ô Sales Person **thứ hai** không được dùng | Để trống `sales_person`, chỉ điền `custom_sales_person` trên đơn → lưu lệnh | Ô Nhân Viên Bán Hàng trên lệnh **để trống** | Pass — HKLED chốt 08/08 chỉ dùng `sales_person`; đã bỏ nhánh dự phòng đọc ô kia (API server) | Pass |

## TC-PERM — phân quyền

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-PERM-01 | Hộp thoại Thêm Đội không lộ nhân sự ngoài quyền | Chạy dưới `test.gioihan.nhansu@hkled.test` (giới hạn Employee = `Anh A`) | Chỉ trả về `Anh A`; % rảnh chỉ tính trên người trong quyền | Pass — Administrator thấy 3 người, user giới hạn thấy 1 (API server) | Pass |

## TC-REGR — không làm hỏng cái đang chạy

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Luồng tạo lệnh từ kế hoạch vẫn chạy | Duyệt kế hoạch → tạo Lệnh sản xuất | Tạo được, thừa hưởng thời gian + đội như trước | Pass (API server) | Pass |
| TC-REGR-02 | Hộp thoại Thêm Đội vẫn thêm được nhân sự | Chọn đội → tick người → **Xác Nhận** | Dòng thêm vào có sẵn Bậc Thợ + Nguồn Lực như trước | Pass — phần thêm % không đụng nhánh này (**giao diện**) | Pass |
| TC-REGR-03 | Đơn bán không khai ghi chú vẫn lưu bình thường | Tạo đơn, để trống Ghi Chú Sản Xuất | Lưu bình thường, không điền gì vào dòng hàng | Pass (API server) | Pass |

## TC-ISO — cách ly app khách

| Mã | Mục tiêu | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|
| TC-ISO-01 | Không rò sang khách khác | 5 Custom Field mới đều thuộc module **MBWNext HKLed**, chỉ theo app này | Pass — đã kiểm trong `fixtures/custom_field.json` | Pass |
| TC-ISO-02 | Không sửa mã app lõi | Chỉ thêm hook và hàm mới trong `mbwnext_hkled`, không đụng `erpnext`/`frappe` | Pass | Pass |

---

## Kết luận

- Tổng: **27** — Pass: **27** — Fail: **0**
- **Một lỗi nặng phát hiện trong lúc test và đã sửa** (TC-VALID-03): lệnh sản xuất tạo từ Kế Hoạch
  Sản Xuất ra đời **thiếu Thời Gian Bắt Đầu** — trường bắt buộc — nên **không lưu lại được nữa**.
  ERPNext tạo hàng loạt bằng `flags.ignore_mandatory = True`. 5/34 lệnh trên site đang kẹt, gồm cả
  lệnh anh Thắng báo. Đã thêm hook chặn ở đầu vào + patch dọn dữ liệu cũ. Chi tiết ở
  `bac-tho-lich-san-xuat.md`, TC-EDGE-18/19/20.
- Ô **Nhân Viên Bán Hàng trống** mà anh Thắng báo chỉ là **triệu chứng** của lỗi trên, không phải
  lỗi riêng: lệnh không lưu được nên đoạn mã điền giá trị không bao giờ chạy, và Frappe ẩn hẳn
  trường chỉ-đọc đang rỗng nên ô biến mất khỏi màn hình.
- **Câu treo đã được trả lời (08/08, anh Thắng):** chỉ dùng ô **`sales_person`**. Đã bỏ nhánh dự
  phòng đọc `custom_sales_person`, thêm `TC-EDGE-09` chốt hành vi này.
  ⚠ Ô `custom_sales_person` **vẫn còn trên màn hình Đơn Bán Hàng** nhưng không được dùng. Nó thuộc
  app lõi `mbwnext_advanced_selling` (dùng chung mọi khách) nên app khách **không được tự gỡ** —
  muốn bỏ phải đề xuất bên lõi. Trong lúc chờ, người nhập liệu cần được dặn nhập đúng ô.
- **Đủ điều kiện nghiệm thu: CÓ** cho vòng tự kiểm. Chờ vòng test tay của anh Thắng.
