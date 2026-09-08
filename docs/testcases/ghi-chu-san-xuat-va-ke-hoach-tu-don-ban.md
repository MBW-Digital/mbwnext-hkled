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

## TC-THIEU — số lượng kế hoạch = phần CÒN THIẾU (PM-TASK-00188, 08/09/2026)

Anh Thắng 08/09 11:40: *"số lượng trên kế hoạch sản xuất đó chính là số lượng còn bị thiếu. Ví dụ
tồn khả dụng của A hiện tại là 6, đơn hàng bán 10 → ghim được 6 còn thiếu 4 → tạo kế hoạch sản
xuất số lượng 4"*.

Dữ liệu thật dùng để chạy: `SO-26-00026` — đặt **40**, giữ chỗ **31**, chưa có lệnh sản xuất,
chưa giao ➜ còn thiếu **9**. Mọi ca ghi dữ liệu đều chạy trong giao dịch rồi `frappe.db.rollback()`;
đã kiểm lại sau khi rollback: giữ chỗ về đúng 31, ô Ghim về đúng 1, số Kế hoạch sản xuất về đúng 14.

| Mã | Việc | Bước thực hiện | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|---|
| TC-THIEU-01 | Đúng ví dụ của anh Thắng | Đơn có tích **Ghim Tồn Khả Dụng**, đặt 40, giữ chỗ 31 → **Tạo > Kế Hoạch Sản Xuất** | Số lượng dự kiến = **9**, không phải 40 | Pass — `planned_qty = 9`, `pending_qty = 9` (**giao diện**, đọc từ form chưa lưu) | Pass |
| TC-THIEU-02 | 🔴 Bỏ tích Ghim thì **không** trừ | Cùng đơn, bỏ tích **Ghim Tồn Khả Dụng** → bấm nút | Giữ nguyên **40** — số giữ chỗ còn đó nhưng không có hiệu lực, trừ theo nó là sản xuất thiếu thật | Pass — `planned_qty = 40` (API server) | Pass |
| TC-THIEU-03 | Giữ chỗ đủ cả dòng | Đặt giữ chỗ = 40 trên đơn 40 → bấm nút | **Chặn**, nêu rõ mặt hàng đã đủ và cách xử lý; **không** tạo kế hoạch rỗng | Pass — *"đã giữ chỗ đủ hàng cho mọi dòng — không còn gì phải sản xuất"* (API server) | Pass |
| TC-THIEU-04 | Giữ chỗ **vượt** cả dòng | Đặt giữ chỗ = 50 trên đơn 40 | Vẫn chặn, **không** ra số âm | Pass — chặn, không có dòng nào âm (API server) | Pass |
| TC-THIEU-05 | Không giữ chỗ gì | Giữ chỗ = 0 | Giữ nguyên **40** | Pass (API server) | Pass |
| TC-THIEU-06 | Dòng đã đủ thì **biến mất**, số thứ tự đánh lại | Đơn 2 dòng khác mã: dòng 1 giữ đủ, dòng 2 giữ một nửa | Chỉ còn dòng 2, `idx` về **1** | Pass — còn `Bán thành phẩm 1` planned 0,5; idx = 1 (API server) | Pass |
| TC-THIEU-07 | 🔴 Hai dòng **cùng một mã**, giữ chỗ khác nhau | Đơn có 2 dòng cùng `Thành phẩm 1`: (8, giữ 1) và (10, giữ 9) | Trừ **theo từng dòng**: 7 và 1 | Pass — `[7, 1]`. Cách làm gộp theo mã hàng sẽ ra sai ở đúng ca này (API server) | Pass |
| TC-THIEU-08 | Đơn vị bán khác đơn vị kho | Dòng qty 8, giữ chỗ 1, `conversion_factor = 2` | `(8×2) − (1×2) = 14` | Pass — `planned_qty = 14`. Cổng 8012 hiện cả 35 dòng đều `cf = 1` nên ca này chưa gặp trong thực tế | Pass |
| TC-THIEU-09 | Đã có Lệnh sản xuất **và** giữ chỗ | Dòng qty 8, giữ chỗ 1, `work_order_qty = 1` | `8 − 1 − 1 = 6` | Pass — `planned_qty = 6` (API server) | Pass |

### TC-THIEU-1x — lỗ hổng nút *Lấy mặt hàng*, và câu cảnh báo bịt nó

Nút *Tạo > Kế Hoạch Sản Xuất* chỉ trừ **một lần lúc tạo**. Trong màn hình Kế hoạch còn nút *Lấy
mặt hàng* của ERPNext lõi, và nó tính lại bằng công thức của lõi — không biết gì về giữ chỗ.

**Đo thật trên cổng 8012 trước khi vá:** tạo kế hoạch ➜ `9`; bấm *Lấy mặt hàng* ➜ `40`, **không một
lời nào**. Đúng loại hỏng cả Phần IV sinh ra để chặn: con số sai trông y hệt con số đúng.

Cách chữa: **nói ra lúc lưu, không tự sửa số** — đặt nhiều hơn phần thiếu là chuyện hợp lệ (làm
dôi để tồn kho, gộp cho đủ mẻ). Cùng cách anh Thắng đã chọn cho phiếu Yêu Cầu Mặt Hàng.

| Mã | Việc | Bước thực hiện | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|---|
| TC-THIEU-10 | Lỗ hổng có thật | Tạo kế hoạch (ra 9) → bấm *Lấy mặt hàng* | Số quay về 40 — ghi nhận để chứng minh vì sao cần cảnh báo | Pass — `9 → 40` (**giao diện**) | Pass |
| TC-THIEU-11 | Lưu bản đã bị tính lại thì bị nhắc | Kế hoạch đang đặt 40 trên phần thiếu 9 → **Lưu** | Hộp thoại *Đặt nhiều hơn phần còn thiếu*, có bảng Đang đặt / Đã giữ chỗ / Còn thiếu | Pass — bảng hiện `40 · 31 · 9` (**giao diện**, `KSX-26-00003`; đã xoá phiếu thử sau khi chụp) | Pass |
| TC-THIEU-12 | Đặt **đúng** phần thiếu thì im | Kế hoạch đặt 9 → Lưu | Không cảnh báo | ⚠ Vòng đầu **Fail** — nổ cảnh báo cả ở ca đúng. Nguyên nhân: lấy `pending_qty` làm mốc, mà nút tạo kế hoạch đã hạ trường đó xuống cùng `planned_qty` ➜ **trừ hai lần**. Đã đổi sang tính lại từ đơn gốc; chạy lại Pass | Pass |
| TC-THIEU-13 | Đặt **ít hơn** phần thiếu thì im | Kế hoạch đặt 5 trên phần thiếu 9 | Không cảnh báo | Pass (API server) | Pass |
| TC-THIEU-14 | Hơn đúng 1 cái vẫn nhắc | Kế hoạch đặt 10 trên phần thiếu 9 | Có cảnh báo | Pass (API server) | Pass |
| TC-THIEU-15 | 🔴 Không được **tự tố cáo chính mình** | Kế hoạch 9 → duyệt → tạo Lệnh sản xuất cho cả 9 → mở kế hoạch, **Lưu lại** | Không cảnh báo. Lúc này `work_order_qty` của đơn đã lên 9 nên phần thiếu về 0, nếu không trừ phần lệnh do **chính kế hoạch này** đẻ ra thì nó sẽ tự báo mình sai | Pass — trừ `ordered_qty` của dòng kế hoạch; không cảnh báo (API server) | Pass |
| TC-THIEU-16 | Đơn không tích Ghim thì im | Đơn bỏ tích Ghim, kế hoạch đặt 40 | Không cảnh báo | Pass (API server) | Pass |

### Chỗ tài liệu suýt sai

Ảnh chụp màn hình lúc chạy TC-THIEU-11 cho thấy cột số lượng trên lưới **Sản phẩm lắp ráp** mang
nhãn **Số lượng dự kiến**, không phải *"Số Lượng Kế Hoạch"* như câu cảnh báo bản đầu của tôi viết.
Đã sửa lại theo đúng chữ hiện trên màn hình khách — cùng loại lỗi đã mắc ở HDSD PM-FEAT-00036
ngày 08/09 (ghi ô nằm "phần đầu đơn" trong khi nó nằm đầu mục Mặt Hàng).

### Hạn chế còn lại, đã biết và cố ý để lại

Bấm *Lấy mặt hàng* **vẫn** xoá phần trừ — cảnh báo chỉ **nói ra lúc lưu**, không tự đặt lại số.
Tự đặt lại sẽ đè lên những lần sửa tay có chủ ý, mà theo chốt 03/09 và 08/09 thì anh Thắng chọn
hướng *hệ thống nói, người quyết*. Muốn đổi thành tự đặt lại thì phải là một chốt mới.

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
