# Bậc Thợ & Lịch Sản Xuất — hoàn thiện theo tài liệu Giai đoạn 1 (Phần II + III + IV)

> **PM-FEAT-00008 · Phần II–III · Tính lịch sản xuất theo bậc thợ**
> Tên trên PM khác tên file này — nối hai bên bằng MÃ, không bằng tên. Xem `CLAUDE.md`.

**Khách hàng:** HKLED (công ty sản xuất đèn LED)
**PM Project:** PM-PRJ-00003
**Nguồn yêu cầu:** PM-DOC-00044 — "Bản sao của TÀI LIỆU NGHIỆP VỤ NÂNG CẤP GIAI ĐOẠN 1 HKLED.docx"
**Ngày phân tích:** 2026-07-31
**Site dev:** hkled.com (bench `mbwnext_project`, dữ liệu restore backup khách 31/07)

## Đầu bài gốc (tóm tắt trung thành theo tài liệu — bản đầy đủ đính kèm trên PM)

- **PHẦN II — Bậc thợ và giờ công chuẩn**: field Thời Gian Sản Xuất (Phút) trên Item;
  DocType Bậc Thợ (lương/phút, nguồn lực %, tỉ lệ đóng quỹ đội); trên Employee: Bậc Thợ
  (*bắt buộc khi Vai trò = Công Nhân*), Vai Trò Nhân Sự, Nguồn Lực % (fetch).
  Giờ công chuẩn = số lượng SP thực tế × thời gian SX 1 SP.
- **PHẦN III — Lịch sản xuất thông minh**: DocType **Đội Sản Xuất (Work Team)** *(mới)*;
  Employee thêm field Đội Sản Xuất; Employee Schedule (phân ca, tăng ca 17h01–23h59,
  chống trùng, **nút "Tạo nhanh" theo Đội** ngoài list view); Employee Allocation (chống
  đè lịch); Work Order Employee (child table, khoá bắt đầu/kết thúc); Work Order tự tính
  thời gian kết thúc dự kiến theo năng lực nhân công (ví dụ chuẩn 100 SP × 10 phút,
  3 nhân sự → 478 phút, kết thúc 8h28 hôm sau); **khi ấn Start WO thì start_time lấy theo
  thời gian thực tế và tự tính lại**; khi Finish cập nhật lại Employee Allocation.
- **PHẦN IV — Một số bổ sung thêm** *(toàn bộ là yêu cầu mới)*:
  1. `Production Plan Sub Assembly Item` + field Đội Sản Xuất → WO tạo ra tự thêm nhân sự đội.
  2. `Sales Order` + Ghi chú (text) + Thời Gian Bắt Đầu (datetime).
  3. `Production Plan Sales Order` + Ghi chú/Thời Gian Bắt Đầu (fetch từ SO), Thời Điểm Cần
     Hoàn Thành (fetch Delivery Date), Đội Sản Xuất.
  4. Tạo WO từ Kế Hoạch SX: item chính thừa hưởng Thời Gian Bắt Đầu + Thời Điểm Cần Hoàn Thành
     từ Production Plan Sales Order, tự thêm nhân sự Đội; nút **"Thêm Đội Sản Xuất"** trên bảng
     Work Order Employee (popup chọn đội → tick nhân sự); bảng **Sản Lượng Nhân Viên (Employee
     Production)** — khi Finish chia đều số lượng (phần nguyên cho tất cả, phần dư cộng dòng đầu:
     10 cái / A,B,C → A 4, B 3, C 3); **Serial sản phẩm tự sinh = mã WO + STT**.
  5. DocType **Công Việc Khác (Other Task)**: tổng thời gian (phút) chia đều cho nhân sự trong
     bảng con; Lương nhân công = lương mỗi phút của bậc thợ × thời gian.

## Bối cảnh & phạm vi

- Phần II + lõi Phần III **đã được code và kiểm chứng từ trước** trong `mbwnext_hkled`
  (engine `api/work_order_schedule.py` khớp 100% ví dụ 478 phút của tài liệu).
- Việc lần này = **phần chênh lệch** giữa tài liệu và code hiện có (bảng GAP dưới).
- ✅ Làm lần này: GAP-1 … GAP-8 (sau khi chốt câu hỏi mục "Cần chốt").
- ❌ Không làm lần này: tính lương/bảng lương từ giờ công chuẩn (tài liệu II chỉ nói "phục vụ
  tính lương **sau này**"); báo cáo năng lực đội; sửa gì thuộc Phần I (đã bàn giao ở PM-FEAT-00007).

## Hiện trạng đã đối chiếu (code + dữ liệu site restore 31/07)

### Đã có và khớp tài liệu — không làm lại

| Hạng mục tài liệu | Hiện trạng |
|---|---|
| II.1 Item: Thời Gian Sản Xuất (Phút) | ✅ `custom_time_to_manufacture` (Int, tab Manufacturing). Site có 3 item đã điền |
| II.2 DocType Bậc Thợ | ✅ `Employee Level` đủ 4 field. Site có 5 bản ghi thật (Bậc 3–7, nguồn lực 60–100%) |
| II.3 Employee: Bậc Thợ / Vai Trò / Nguồn Lực | ✅ `custom_employee_level` / `custom_employee_type` / `custom_performance_factor_` (fetch). Site: 3 nhân sự Active, đều Công nhân + đủ Bậc Thợ |
| III.2 Employee Schedule | ✅ đủ field + ràng buộc tăng ca 17h01/23h59 + chống trùng (Employee+Start, Employee+End). Site có 11 bản ghi |
| III.3 Employee Allocation | ✅ validate chống đè lịch (overlap thật sự, chặt hơn mô tả). Site có 6 bản ghi |
| III.4 Work Order Employee | ✅ đủ field kể cả lock_start/lock_end (allow on submit), allocation_record |
| III.5 WO: 5 field + engine tính lịch | ✅ `custom_start_time/end_time/estimated_completion_time_minutes/required_completion_date__time/work_order_employee` + nút "Tính Lại Lịch". Engine sweep-line khớp 100% ví dụ 478 phút / 8h28 |
| III.5 Finish WO → update Allocation | ✅ `doc_events on_update` khi status = Completed |
| Shift Type | ✅ Ca Sáng 8h00–11h45, Ca Chiều 13h15–17h00 — trùng khớp ví dụ tài liệu |

### GAP — tài liệu yêu cầu nhưng CHƯA có trong code

| # | Hạng mục | Nguồn | Mức độ |
|---|---|---|---|
| GAP-1 | DocType **Work Team** + field Đội Sản Xuất trên Employee | III.1 | Nhỏ — nền cho GAP-2/5/6 |
| GAP-2 | Nút **"Tạo nhanh"** Employee Schedule theo Đội (popup, tạo hàng loạt) | III.2 | Vừa — có UI popup |
| GAP-3 | **Ấn Start WO** → `custom_start_time` = thời gian thực, dòng không khoá tính lại toàn bộ | III.5 | Vừa — hook trạng thái |
| GAP-4 | `Sales Order` + Ghi chú + Thời Gian Bắt Đầu; `Production Plan Sales Order` + 4 field fetch | IV.2, IV.3 | Nhỏ — chỉ Custom Field |
| GAP-5 | `PP Sub Assembly Item` + Đội SX; tạo WO từ PP → thừa hưởng thời gian + tự thêm nhân sự đội | IV.1, IV.4 | Lớn — đụng luồng tạo WO của core |
| GAP-6 | Nút **"Thêm Đội Sản Xuất"** trên bảng Work Order Employee (popup chọn đội → tick nhân sự) | IV.4 | Vừa |
| GAP-7 | Bảng **Employee Production** trên WO + chia sản lượng khi Finish + **Serial = mã WO + STT** | IV.4 | Lớn — serial đụng cơ chế core |
| GAP-8 | DocType **Other Task** + bảng con (chia đều thời gian, tính lương nhân công) | IV.5, IV.6 | Nhỏ — độc lập |

### Lệch nhỏ giữa tài liệu và hiện trạng (đã có quyết định trước, giữ nguyên)

1. Tên field thực tế có tiền tố `custom_` và `custom_employee_type` (tài liệu ghi `employee_role`),
   options thực tế **"Công nhân/Bán hàng/Kế toán"** (tài liệu viết hoa "Công Nhân/Bán Hàng/Kế Toán")
   — field do khách tự tạo trước, đã quyết giữ nguyên. Mọi code mới phải so sánh đúng chuỗi
   **"Công nhân"** (như `employee.js` đang làm).
2. **3 Custom Field còn label tiếng Anh, chưa khớp tài liệu** (phát hiện khi khai lên PM 31/07):
   `custom_employee_level` = "Employee Level" (tài liệu: **Bậc Thợ**), `custom_performance_factor_`
   = "Performance Factor (%)" (tài liệu: **Nguồn Lực (%)**), `custom_work_order_employee`
   = "Work Order Employee" (tài liệu: **Nhân Công Tham Gia**). Đây là label do khách tự tạo trước.
   Đổi label KHÔNG ảnh hưởng dữ liệu (chỉ là nhãn hiển thị) — xem câu hỏi C7.
3. Tài liệu II.3: Bậc Thợ **bắt buộc** khi Vai trò = Công Nhân. Hiện chỉ cảnh báo mềm (quyết định cũ
   vì dữ liệu bench cũ có 33/38 nhân sự thiếu). **Dữ liệu restore mới chỉ có 3 nhân sự, đều đủ Bậc Thợ**
   → có thể bật ràng buộc cứng đúng tài liệu. Xem câu hỏi C1.

---

## Technical Specification — mbwnext_hkled

### Summary
Bổ sung 8 hạng mục còn thiếu của Phần II/III/IV: Đội Sản Xuất và các luồng gắn đội vào lịch
làm việc + lệnh sản xuất, hành vi Start WO, sản lượng nhân viên + serial khi Finish, và Công Việc Khác.

### Layer & Collision

| Aspect | Value |
|---|---|
| Tầng thực thi | 4 — app khách `mbwnext_hkled` (quy trình sản xuất riêng HKLED, câu 4 bảng 2A) |
| DocType/event sẽ hook | Work Order (`on_update` — đã hook sẵn, thêm nhánh; `before_save`), Sales Order/Production Plan (chỉ Custom Field + client script), Stock Entry (serial, nếu chốt làm) |
| App khác hook cùng chỗ | Sales Order bị 5 app lõi hook (`advanced_selling/accounting/stock/localization/integration_dms`) nhưng HKLed **chỉ thêm field mới, không doc_events trên SO** → ghi rời nhau, vô hại. Work Order/Production Plan: chỉ mình `mbwnext_hkled` |
| Ghi cùng trường/tài liệu? | Không — toàn bộ field mới đều `custom_*` riêng HKLed |
| Override xuyên tầng? | Không dự kiến. Duy nhất GAP-5 cần điểm nối khi core tạo WO từ Production Plan — ưu tiên `doc_events` trên Work Order (`before_insert`/`after_insert`) đọc ngược Production Plan, KHÔNG override `make_work_order` của erpnext |

### Implementation theo từng GAP

**GAP-1 — Work Team** (DocType trong app, module MBWNext HKLed)
- `Work Team`: `work_team_name` (Data, reqd, unique, autoname field).
- Custom Field `Employee.custom_work_team` (Link Work Team) — 1 nhân sự thuộc 1 đội.
- Trước khi tạo: `frappe.db.exists("DocType", "Work Team")` + query Custom Field (bài học thangdo).
  Đã kiểm 31/07: chưa tồn tại — an toàn.
- Kèm theo **C1**: đổi `custom_employee_level` thành bắt buộc khi `custom_employee_type == "Công nhân"`
  (`mandatory_depends_on`), và sửa `employee.js` từ cảnh báo mềm sang chặn. Dữ liệu hiện tại 3/3
  nhân sự đều đã có Bậc Thợ nên bật được ngay, không cần dọn dữ liệu trước.

**GAP-2 — Tạo nhanh Employee Schedule** (`listview_settings` / nút trên List View + dialog)
- Popup: chọn Đội SX → server trả nhân sự đội (Công nhân, Active) → bảng tick chọn
  + **`Từ Ngày` / `Đến Ngày`** *(chốt theo C10)*, Ca **hoặc** Tăng Ca (điền sẵn 18h00–21h00,
  cho sửa trong khung 17h01–23h59).
- Sinh tích Descartes `(mỗi ngày trong khoảng) × (mỗi nhân sự được tick)`. Hiện số bản ghi sẽ tạo
  ngay trên dialog trước khi bấm Xác Nhận — khoảng 1 tuần × 10 người đã là 70 bản ghi, người dùng
  cần thấy con số trước khi lỡ tay chọn cả tháng.
- **Bộ chọn thứ trong tuần** *(chốt theo C10b)*: 7 ô tick T2…CN, **mặc định tick T2–T7**, bỏ CN.
  Chỉ ngày trong khoảng **khớp thứ đã tick** mới sinh bản ghi. Số tạo ra =
  `(số ngày khớp thứ) × (số nhân sự được tick)`; dialog ghi rõ *"bỏ qua N ngày không khớp thứ"*.
- Chặn khi: `Đến Ngày` < `Từ Ngày`; **bỏ tick hết các thứ**; khoảng quá dài (> 62 ngày, tính theo
  tổng số ngày của khoảng chứ không phải số ngày khớp thứ — tránh cho người dùng quét cả năm rồi
  lách giới hạn bằng cách chỉ tick 1 thứ).
- Xác nhận → API whitelisted tạo hàng loạt qua `frappe.get_doc(...).insert()` **từng bản ghi**
  (để validate chống trùng của Employee Schedule chạy đủ); bản ghi trùng thì bỏ qua + báo lại
  danh sách bỏ qua, không fail cả lô. Với khoảng ngày thì việc "bỏ qua dòng trùng" càng quan
  trọng: phân ca tuần sau chồng lên vài ngày đã tạo rồi là chuyện thường.

**GAP-3 — Nút "Bắt Đầu Sản Xuất" riêng** *(viết lại theo C2)*
- ❌ **Không** hook vào status "In Process": `WorkOrder.get_status()` của erpnext (tầng 1) hard-code
  `material_transferred_for_manufacturing > 0 → "In Process"`, nên WO tự chuyển ngay khi nhận NVL,
  không phải lúc thật sự bắt đầu làm. Sửa chỗ này = vá app lõi tầng 1 → không làm.
- ✅ Thêm nút **"Bắt Đầu Sản Xuất"** trên `Work Order` *(chốt theo C8)* → API whitelisted:
  set `custom_start_time = now()`, rồi `recalculate_schedule` (dòng có `lock_start` giữ nguyên).
- **Điều kiện hiện nút**: `docstatus == 1` **và** `status == "In Process"` **và** chưa từng ấn.
- ⚠ **Cần thêm 1 Custom Field làm cờ**: `Work Order.custom_production_started`
  (Check, read_only, **allow_on_submit=1**, label *Đã Bắt Đầu Sản Xuất*). Lý do: `custom_start_time`
  là field **Mandatory** nên luôn có giá trị ngay từ lúc tạo WO (giờ dự kiến), không thể dùng
  "trống/không trống" để biết đã ấn nút chưa. Ấn nút → set cờ = 1 → nút tự ẩn, đảm bảo đúng
  yêu cầu "chỉ ấn 1 lần".
- Ghi log rõ trong comment/version của WO: giờ dự kiến ban đầu vs giờ bắt đầu thực tế, để sau
  còn đối chiếu được.

**GAP-4 — Custom Field SO / PP Sales Order** (fixtures module MBWNext HKLed)
- `Sales Order`: `custom_note` (Text), `custom_start_time` (Datetime),
  **`custom_time` (Time)** — giờ cần hoàn thành, ghép với `delivery_date` *(thêm theo C4)*.
- `Production Plan Sales Order`: `custom_note` (fetch `sales_order.custom_note`),
  `custom_start_time` (fetch `sales_order.custom_start_time`),
  `custom_required_completion_date_time` (Datetime — **KHÔNG dùng `fetch_from`**),
  `custom_work_team` (Link Work Team).
- ⚠ `custom_required_completion_date_time` = `delivery_date` **+** `custom_time` → là phép ghép
  2 field nên `fetch_from` không làm được. Tính trong code: client script khi chọn SO trên
  Production Plan, và tính lại phía server lúc tạo WO (GAP-5) để không phụ thuộc UI.
  `custom_time` trống → lấy 00:00 của `delivery_date` (giữ hành vi cũ, không tự đoán 17:00).

**GAP-5 — Tạo WO từ Production Plan thừa hưởng + gắn đội**
- `PP Sub Assembly Item.custom_work_team` (Link).
- `doc_events Work Order.before_insert` (hoặc `after_insert` + save): nếu WO có `production_plan`:
  - Item chính (khớp `production_plan_item`) → tra dòng Production Plan Sales Order tương ứng
    → set `custom_start_time`, `custom_required_completion_date__time`, đội = `custom_work_team`.
  - Item bán thành phẩm (khớp PP Sub Assembly Item) → đội theo dòng đó.
  - Có đội → append toàn bộ nhân sự Công nhân Active của đội vào `custom_work_order_employee`.
- KHÔNG override `erpnext...production_plan.make_work_order` — hook `before_insert` áp dụng được
  cho cả tạo tay lẫn tạo hàng loạt, không phụ thuộc chữ ký hàm core.

**GAP-6 — Nút "Thêm Đội Sản Xuất"** (`work_order.js`)
- Button trên section Nhân Công: dialog chọn Work Team → server trả nhân sự đội → MultiCheck
  → append dòng chưa có vào `custom_work_order_employee` (không trùng nhân sự — engine đã có
  `validate_no_duplicate_employee`).

**GAP-7 — Employee Production + Serial khi Finish**
- Child table `Employee Production`: `employee` (Link), `qty` (Int) — **không có cột Ghi chú**
  *(chốt theo C13: khách đồng ý bỏ)*; field `Work Order.custom_employee_production`
  (Table, allow_on_submit).
- ⚠ **allow_on_submit phải đặt trên CẢ field con `employee` và `qty`**, không chỉ trên field bảng
  ở Work Order. Frappe kiểm `allow_on_submit` của **từng field trong child DocType**
  (`validate_update_after_submit` → `d._validate_update_after_submit()` cho mọi dòng đã có trong DB).
  Đặt thiếu thì C12 (sửa tay sau Finish) báo *"Not allowed to change … after submission"*.
  Đây đúng là lỗi đã mắc ở bảng `Work Order Employee` — xem mục "Lỗi đã sửa" cuối tài liệu.
- Nhánh Finish trong hook (status → Completed, cùng chỗ sync allocation):
  chia `produced_qty` phần nguyên cho mọi dòng Work Order Employee, phần dư cộng dòng đầu
  (10/3 → 4,3,3), ghi vào bảng. Chỉ chia khi bảng **đang trống** — đã chia rồi mà chia đè thì
  xoá mất phần người dùng sửa tay ở C12.
- **Cho sửa tay sau khi Finish** *(chốt theo C12)*: `validate` chặn lưu nếu
  `sum(rows.qty) != wo.produced_qty`, thông báo rõ đang lệch bao nhiêu cái.
  ✅ **Đã xác nhận 02/08**: khách nói *"tổng các dòng bằng tổng sản lượng sản xuất được của lệnh
  sản xuất đó"* → mốc so đúng là **`produced_qty`** (số thực làm được), không phải `qty` (số đặt làm).
- Serial *(viết lại theo C3)*: **chỉ item bật `has_serial_no`** mới sinh. Công thức:
  `<mã SO> + STT`, nếu WO không có mã SO thì `<mã WO> + STT`.
- ✅ **Không cần thêm field lưu mã SO**: `Work Order.sales_order` là field **sẵn có của erpnext**
  và **tự điền** khi tạo WO từ Production Plan — `get_production_items()` truyền
  `Production Plan Item.sales_order` (cũng là field sẵn có, được điền khi kéo SO vào Kế hoạch SX).
  Chỉ cần đọc `wo.sales_order or wo.name`.
- Cơ chế: `doc_events Stock Entry.before_submit` — entry `purpose = Manufacture` thuộc WO và item
  bật Has Serial No → tự sinh danh sách serial theo công thức thay cho series mặc định.
- **STT đánh liên tục theo SO** *(chốt theo C9)*: prefix = `wo.sales_order or wo.name`; tìm STT
  lớn nhất trong các `Serial No` đã có prefix đó rồi **tiếp nối**, không đánh lại từ 001. Nhờ vậy
  nhiều WO cùng 1 SO không sinh serial trùng.
- **Định dạng chốt theo C11 (02/08): `<2 số cuối năm>-<số thứ tự SO>-<STT 4 chữ số>`**
  → `SAL-ORD-2026-00001` sinh ra `26-00001-0001`, `26-00001-0002`, … (13 ký tự).
  An toàn vì SO trên site chỉ có **một** naming series `SAL-ORD-.YYYY.-`, nên phần bỏ đi là cố định.
- ⚠ **Trường hợp WO không có mã SO cần ký hiệu riêng** — phát sinh từ chính việc rút gọn:
  nếu rút gọn `MFG-WO-2026-00042` y hệt thì ra `26-00042`, **trùng** với SO số 00042 cùng năm, mà
  serial là khoá chính toàn hệ thống. Dùng tiền tố **`W`**: `W26-00042-0001`.
  Đã nêu trong mockup để HKLED xác nhận ký hiệu; đổi chữ khác thì sửa 1 hằng số.
- Viết test khẳng định: 2 SO khác nhau không bao giờ ra cùng prefix, và prefix từ SO không bao giờ
  đụng prefix từ WO.
- Chống trùng khi 2 người Finish cùng lúc: sinh xong kiểm tra `frappe.db.exists("Serial No", ...)`,
  nếu đã tồn tại thì nhảy tiếp — không dựa hoàn toàn vào lần đếm ban đầu.

**GAP-8 — Other Task** (độc lập, làm cuối)
- `Other Task`: `total_time` (Float, phút) + bảng con `Other Task Table`:
  `employee` (Link), `employee_level` (fetch), `time` (Float), `labor_wage` (Currency,
  = `employee_level.earnings_per_minute × time`).
- Chia đều chỉ là **giá trị gợi ý ban đầu** (khi đổi `total_time` hoặc thêm/bớt dòng);
  người dùng **sửa tay được** từng dòng.
- `validate` *(theo C5)*: **chặn lưu nếu `sum(rows.time) != total_time`** — thông báo rõ đang lệch
  bao nhiêu phút. `labor_wage` tính lại theo `employee_level.earnings_per_minute × time` mỗi lần lưu.

### Data Flow (luồng chính sau khi đủ 8 GAP)

1. SO nhập Ghi chú + Thời Gian Bắt Đầu → kéo vào Production Plan (PP Sales Order fetch) →
   người lập kế hoạch chọn Đội SX cho item chính (PPSO) và từng bán thành phẩm (PP Sub Assembly).
2. Create Work Order → WO nhận start_time/required_completion + nhân sự đội tự vào bảng Nhân Công.
3. Người điều phối bấm "Tính Lại Lịch" (hoặc sửa đội bằng nút Thêm Đội Sản Xuất) → engine tính
   end_time dự kiến, tạo Employee Allocation.
4. Ấn Start → start_time thực tế, tự tính lại. Finish → sync Allocation + chia Sản Lượng Nhân Viên
   (+ serial nếu chốt làm).
5. Việc ngoài sản xuất → Other Task, chia thời gian + lương nhân công theo bậc thợ.

### Error Handling
- Tạo nhanh lịch: bản ghi trùng → bỏ qua từng dòng + tổng kết, không chặn cả lô.
- Start WO: nhân sự không còn lịch/đè lịch → thông báo lỗi của engine hiện có (throw, chặn).
- Thêm đội vào WO: nhân sự thiếu Bậc Thợ → chặn kèm tên người (engine cần performance_factor).
- Chia sản lượng: WO không có dòng nhân công → bỏ qua, không lỗi.

### Required Skills
- [ ] erpnext-syntax-hooks / erpnext-impl-hooks — doc_events Work Order/Stock Entry
- [ ] erpnext-syntax-clientscripts — 2 dialog (Tạo nhanh, Thêm Đội Sản Xuất)
      ⚠ File JS đặt ở `controllers/js/<doctype>.js` (quy ước chung MBWNext — 4 file cũ đã được
      di dời khỏi public/js ngày 31/07, hooks.py trỏ theo đường dẫn mới)
- [ ] erpnext-mbwnext-customer-app — mockup trước logic (2 dialog + bảng Employee Production)
- [ ] erpnext-mbwnext-testcase — bộ test, nối tiếp bộ Phần III cũ (18 ca A–E)

### Validation Criteria
- Ví dụ chuẩn tài liệu (478 phút / 8h28) vẫn đúng sau khi thêm GAP-3 (regression).
- Tạo WO từ PP có đội → bảng nhân công đúng thành viên; không đội → WO như cũ (regression core).
- Finish WO 10 SP / 3 nhân sự → 4/3/3 đúng thứ tự dòng.
- TC-Isolation: site khách khác không thấy Work Team/Other Task/field mới.

---

## ĐÃ CHỐT — Thắng trả lời 31/07/2026 16:03 (comment trên PM-FEAT-00008)

| # | Câu trả lời của Thắng | Ảnh hưởng tới spec |
|---|---|---|
| C1 | **Bật** ràng buộc Công nhân phải có Bậc Thợ | `custom_employee_level` đặt `mandatory_depends_on: eval:doc.custom_employee_type=="Công nhân"`; đổi cảnh báo mềm ở `employee.js` thành chặn |
| C2 | Hiện WO tự sang *In Process* **ngay khi nhận NVL**; khách muốn chỉ khi ấn Start mới chuyển. Không sửa được logic gốc thì **làm nút Start riêng**, ấn vào đó mới tính thời gian bắt đầu | ✅ **Đã kiểm chứng: KHÔNG sửa được logic gốc** — `WorkOrder.get_status()` của erpnext (tầng 1) hard-code `if material_transferred_for_manufacturing > 0 → "In Process"`. → Đi theo phương án 2: **nút riêng** ở app khách. Xem GAP-3 viết lại |
| C3 | Chỉ item **bật serial** mới sinh serial khi Finish. Công thức đổi: SO → Production Plan lưu mã SO → WO lưu mã SO → serial = **mã SO + STT**; WO không có mã SO thì **mã WO + STT** | ✅ **Tin tốt: không cần thêm field nào.** `Work Order.sales_order` là field **có sẵn của erpnext** và **tự điền** khi tạo WO từ Production Plan (`get_production_items()` truyền `po_items.sales_order`, mà `Production Plan Item.sales_order` cũng là field sẵn có). Chỉ cần đọc `wo.sales_order`, fallback `wo.name`. Xem GAP-7 viết lại |
| C4 | **Thêm 1 trường Time ở SO**; Thời Điểm Cần Hoàn Thành = **Time + Delivery Date** của SO | `Sales Order.custom_time` (Time). Vì phải **ghép 2 field** nên KHÔNG dùng được `fetch_from` — phải tính trong code khi tạo WO / khi lập Production Plan. Xem GAP-4 + GAP-5 |
| C5 | Other Task **sửa tay được**, nhưng **chỉ lưu được nếu tổng thời gian các dòng = tổng thời gian chung** | Đổi từ "tự chia đè" thành: chia đều làm **giá trị gợi ý ban đầu**, `validate` chặn khi `sum(rows.time) != total_time`. Xem GAP-8 |
| C6 | Đúng — nút Thêm Đội Sản Xuất ở WO **chỉ để chọn thành viên nhanh, không ràng buộc** | Giữ nguyên thiết kế snapshot; không đồng bộ lại khi nhân sự đổi đội |

### C7–C9 — Thắng trả lời 31/07/2026 16:32

| # | Câu trả lời | Ảnh hưởng tới spec |
|---|---|---|
| C7 | **Đổi label sang tiếng Việt** | Đổi 3 label: `custom_employee_level` → **Bậc Thợ**, `custom_performance_factor_` → **Nguồn Lực (%)**, `custom_work_order_employee` → **Nhân Công Tham Gia**. Chỉ sửa nhãn, không đổi fieldname → không đụng dữ liệu. Nhớ cập nhật `locale/vi.po` cho khớp |
| C8 | Tên nút **"Bắt Đầu Sản Xuất"**, **chỉ cho ấn 1 lần**, khi WO ở trạng thái **In Process** | Xem GAP-3 viết lại. ⚠ Để chặn ấn lần 2 phải có **cờ đánh dấu** — `custom_start_time` là field Mandatory nên luôn có giá trị sẵn từ lúc tạo, không dùng được làm mốc "đã ấn chưa" |
| C9 | **Đánh STT liên tục theo SO** | Serial của WO thứ 2 cùng SO tiếp nối WO thứ 1 (không đánh lại từ 001). Xem GAP-7 viết lại |

### C10–C13 — khách duyệt mockup, trả lời 01/08/2026

4 câu hỏi cuối mockup (mục F, `docs/mockups/bac-tho-lich-san-xuat.html`). Thắng chuyển ý kiến
vào `PM-DOC-00074` sáng 01/08, khách trả lời cùng ngày.

| # | Câu hỏi mockup | Khách trả lời | Ảnh hưởng tới spec |
|---|---|---|---|
| C10 | Tạo nhanh lịch — một ngày hay một khoảng ngày? | **Một khoảng "từ ngày – đến ngày"**, **kèm tick chọn thứ trong tuần** (chốt nốt 02/08) | GAP-2 viết lại: cặp `Từ Ngày` / `Đến Ngày` + bộ chọn thứ; chỉ ngày khớp thứ mới sinh bản ghi |
| C11 | Độ dài mã serial — rút gọn phần mã đơn hay để nguyên? | Hỏi ngược về truy xuất → đã trả lời; khách **chọn phương án ngắn nhất `26-00001-0001`** (02/08) | ✅ Truy xuất KHÔNG phụ thuộc độ dài mã (xem mục dưới). GAP-7: prefix = 2 số cuối của năm + số thứ tự SO |
| C12 | Sản lượng nhân viên có cho sửa tay sau Finish? | **Có cho sửa tay**; tổng các dòng = **tổng sản lượng sản xuất được** (xác nhận 02/08) | GAP-7 viết lại: cho sửa sau khi WO đã submit + `validate` chặn khi `sum(qty) != produced_qty` |
| C13 | Cột "Ghi chú" ở bảng Sản Lượng Nhân Viên — giữ hay bỏ? | **Bỏ được** | GAP-7: bỏ cột Ghi chú khỏi `Employee Production`; bỏ luôn khỏi mockup màn C |

#### C10b — tick chọn thứ trong tuần (chốt 02/08)

Thắng chuyển lời khách: *"khách muốn tích chọn được thứ trong tuần, ví dụ anh chọn từ ngày 1/8-10/8,
nhưng chỉ chọn thứ 2 đến thứ 7, thì ngày chủ nhật nó sẽ không tạo bản ghi lịch làm việc"*.

➜ GAP-2 phải có **bộ chọn thứ** (T2…CN), mặc định tick T2–T7. Số bản ghi tạo ra =
`(số ngày trong khoảng KHỚP thứ đã tick) × (số nhân sự được tick)`. Dialog hiện rõ đã bỏ qua bao
nhiêu ngày vì không khớp thứ — người phân ca không phải tự nhẩm.

⚠ Đây là **hạng mục phát sinh ngoài 8 GAP ban đầu**, không có trong tài liệu nghiệp vụ gốc.

#### Truy xuất serial khi rút gọn mã — trả lời C11 (đã kiểm chứng trên code + site)

**Rút gọn không làm mất khả năng truy xuất.** ERPNext không hề phân tích chuỗi serial để tìm chứng từ:

- `Serial No` có `autoname: field:serial_no` → **chuỗi serial chính là khoá chính** của bản ghi.
  Gõ serial vào ô tìm kiếm là ra thẳng bản ghi đó, bất kể chuỗi dài hay ngắn.
- Bản ghi `Serial No` lưu sẵn `work_order`, `purchase_document_no`, `customer`, `warehouse`,
  `batch_no`, `status` — liên kết bằng **field**, không phải bằng cách đọc mã.
- Báo cáo **Serial No Ledger** (`erpnext/stock/report/serial_no_ledger`) truy ngược qua
  `Serial and Batch Entry.serial_no` → Stock Ledger Entry → trả về **Voucher Type + Voucher No**
  (Dynamic Link, bấm mở thẳng chứng từ) cho **mọi** lần nhập/xuất/chuyển kho của serial đó.

Ràng buộc DUY NHẤT phải giữ: **serial vẫn phải duy nhất toàn hệ thống** (vì nó là khoá chính).
Nếu rút gọn tới mức 2 đơn khác nhau sinh ra cùng một mã thì hỏng 2 chỗ: lỗi trùng khoá lúc tạo, và
logic C9 (tìm STT lớn nhất theo prefix rồi nối tiếp) sẽ nối nhầm STT của đơn này sang đơn kia.

Kiểm tra trên site `hkled.com` ngày 01/08: Sales Order chỉ có **đúng một** naming series
`SAL-ORD-.YYYY.-`, không có Property Setter nào đổi khác. Nghĩa là `SAL-ORD-` là tiền tố **cố định
của mọi đơn**, bỏ đi không mất một chút thông tin phân biệt nào:

| Phương án | Ví dụ | Độ dài | Duy nhất? |
|---|---|---|---|
| Giữ nguyên (C9 đề xuất ban đầu) | `SAL-ORD-2026-00001-0001` | 23 | ✅ |
| Bỏ tiền tố cố định `SAL-ORD-` | `2026-00001-0001` | 15 | ✅ |
| **Bỏ tiền tố + rút năm 2 số — ✅ HKLED ĐÃ CHỌN 02/08** | **`26-00001-0001`** | **13** | ✅ |

Thêm một thuận lợi: site hiện có **0 bản ghi Serial No** (chưa từng sinh serial nào), nên đổi định
dạng bây giờ **không phải chuyển đổi dữ liệu cũ**. Đổi sau khi đã chạy thật thì tốn kém hơn nhiều.

⚠ Điều kiện kèm theo: nếu sau này HKLED thêm naming series thứ hai cho Sales Order (theo chi nhánh,
theo loại đơn…) thì phần bị bỏ có thể lại mang thông tin phân biệt — lúc đó phải rà lại.

### Vấn đề dữ liệu serial — ĐÃ XỬ LÝ (không phải việc của mình)

Thắng 31/07 16:32: *"khách đã xác nhận sẽ tắt các item không dùng đi, đợi khách chỉnh sửa hoàn chỉnh
anh sẽ up lại dữ liệu cho khách"*.

➜ Không cần làm gì với dữ liệu. Logic GAP-7 **không phụ thuộc** item nào bật serial (chỉ đọc cờ
`has_serial_no` lúc chạy) nên code được ngay. **Nhưng khi Thắng up dữ liệu mới thì phải audit lại**
đúng như lần restore 31/07 (đếm lại item bật serial theo nhóm, chạy lại bộ test) — dữ liệu mới có
thể lại lệch mô tả.

### ⚠ Vấn đề dữ liệu phát sinh từ C3 — cần rà lại với HKLED

Thắng nói *"chỉ 1 số item thành phẩm mới quản lý theo serial"*, nhưng số liệu thật (31/07) lệch:

| Nhóm | Số item bật `has_serial_no` |
|---|---|
| Biến thể đèn thành phẩm 6 nhóm | **34.175 / 34.176** — khớp ý Thắng ✅ |
| **KHÔNG phải thành phẩm nhưng vẫn bật serial** | **2.710** ⚠️ |
| Tổng bật serial | 36.885 / 37.053 item (chỉ 168 item ốc-vít-bulong là tắt) |

2.710 item không phải thành phẩm gồm: `(V) Vỏ đèn` 331, `Chip LED đèn đường` 217, `Chip LED đèn
nhà xưởng` 188, `(PTN) Tản nhiệt` 177, `Chip LED Module` 78, `PCB` 64, `(N) Nguồn` 44,
`Linh phụ kiện gia công cơ khí` 44… — đều là **NVL/bán thành phẩm**. Bật serial ở đây nghĩa là
mọi phiếu nhập/xuất/chuyển kho của chúng cũng bắt khai serial từng chiếc.

Ngoài ra 725 item nhóm `Đèn LED phòng nổ UFO NU1` + 365 item nhóm `Đèn LED nhà xưởng UFO X01`
**là đèn thành phẩm thật** nhưng thuộc 10 template chưa có nhóm công thức (`DNU1*`, `DX01*` —
xem PM-FEAT-00007 mục 4.5), nên chưa tạo được BOM.

➜ Đề nghị HKLED rà lại và **tắt serial cho nhóm NVL/bán thành phẩm**, giữ serial chỉ ở thành phẩm
bán ra. Nếu giữ nguyên thì vận hành kho sẽ nặng lên rất nhiều — và cơ chế sinh serial tự động ở
GAP-7 cũng phải mở rộng cho cả NVL (hiện chỉ thiết kế cho thành phẩm khi Finish WO).

## Cần chốt trước khi DEV (C1–C6 — ĐÃ TRẢ LỜI, xem mục trên)

| # | Câu hỏi | Phương án đề xuất |
|---|---|---|
| C1 | Bật ràng buộc **cứng** "Công nhân phải có Bậc Thợ" đúng tài liệu II.3? Dữ liệu mới chỉ còn 3 nhân sự đều đủ | Bật cứng (mandatory_depends_on), giữ cảnh báo mềm thành lỗi chặn |
| C2 | "Ấn Start" hiểu là nút **Start** chuẩn của ERPNext (status → In Process)? Hay cần nút riêng? | Dùng status → In Process |
| C3 | **Serial = mã WO + STT**: kiểm 31/07 — **36.885/37.053 item ĐÃ bật Has Serial No** (36.890 bật cả Batch) nhưng `serial_no_series` **trống toàn bộ** và 0 bản ghi Serial No (chưa từng giao dịch). Không có cơ chế tự sinh thì Finish WO sẽ bắt gõ tay serial từng chiếc → yêu cầu này là **bắt buộc để luồng chạy được**, không phải tuỳ chọn | Làm theo tài liệu (sinh `mã WO + STT` lúc Manufacture). ⚠ Cảnh báo kèm: bật serial+batch trên ~37k item nghĩa là MỌI giao dịch kho (nhập, xuất bán, chuyển kho) từ nay đều phải có serial/batch — cần HKLED xác nhận đây là chủ đích, vì vận hành sẽ nặng hơn đáng kể |
| C4 | Thời Điểm Cần Hoàn Thành fetch từ **Delivery Date** (Date, không giờ) → mặc định 00:00 ngày đó — lấy 00:00 hay cuối ngày 17h? | Lấy 17:00 (giờ hết ca chiều) — cần khách xác nhận |
| C5 | Other Task: sau khi chia đều, người dùng sửa tay 1 dòng thì có chia lại các dòng khác không? | Chỉ chia đều khi đổi `total_time` hoặc thêm/bớt dòng; sửa tay giữ nguyên |
| C6 | Nhân sự đổi đội giữa chừng: WO đang chạy giữ danh sách cũ hay đồng bộ theo đội mới? | Giữ danh sách tại thời điểm tạo (bảng WO Employee là snapshot) |
| C7 | Đổi 3 label còn tiếng Anh sang đúng chữ tài liệu (Bậc Thợ / Nguồn Lực (%) / Nhân Công Tham Gia)? | Nên đổi — chỉ là nhãn hiển thị, không đụng dữ liệu, và giúp khớp HDSD sẽ viết ở Giai đoạn 4 |

## Thứ tự làm đề xuất

1. GAP-1 (Work Team — nền) → GAP-4 (chỉ field) → GAP-2, GAP-6 (2 dialog, chung mockup)
2. GAP-5 (luồng PP→WO) → GAP-3 (Start) — cần test regression engine
3. GAP-7 (chia sản lượng ngay; serial **chờ C3**) → GAP-8 (Other Task, độc lập)

Mỗi bước con: mockup duyệt trước khi viết logic (bài học PM-FEAT-00007).

---

## Khai báo trên app PM (31/07/2026)

Tab **Doctype** (9 bản ghi) và **Trường tùy chỉnh** (11 bản ghi) của dự án `PM-PRJ-00003` đã được
khai đầy đủ, mỗi dòng ghi rõ mục đích, field chính, và cột "Khác" đánh dấu cái nào MỚI 31/07 vs
đã có trước, kèm cảnh báo về các tên field/label lệch tài liệu.

DocType/Custom Field **thuộc kế hoạch GAP-1…GAP-8 chưa được khai** vì chưa tồn tại thật —
sẽ khai ngay khi tạo, để 2 tab đó luôn phản ánh đúng hiện trạng site, không lẫn dự kiến:

- DocType dự kiến: `Work Team`, `Other Task`, `Other Task Table`, `Employee Production`
- Custom Field dự kiến: `Employee.custom_work_team`; `Sales Order.custom_note` +
  `custom_start_time` + **`custom_time`** (C4); `Production Plan Sales Order` (4 field);
  `Production Plan Sub Assembly Item.custom_work_team`; `Work Order.custom_employee_production`
  + **`custom_production_started`** (cờ chặn ấn nút 2 lần, C8)
- Sửa 3 label sẵn có sang tiếng Việt (C7) — không phải field mới, nhưng phải cập nhật lại mô tả
  trong tab *Trường tùy chỉnh* trên PM sau khi đổi

---

## Lỗi đã sửa trong code Phần III sẵn có (01/08/2026)

Hai lỗi nằm ở phần lõi Phần III **đã có từ trước** (không thuộc GAP-1…GAP-8), phát hiện khi rà lại
code app trước lúc vào DEV. Cả hai đều chặn đúng những thứ sắp code, nên phải sửa trước.

**1. `Tính Lại Lịch` không chạy được trên Work Order đã Submit**

`recalculate_schedule` kết thúc bằng `wo.save()`. Với `docstatus = 1`, Frappe chạy
`validate_update_after_submit`, duyệt **từng dòng con** và kiểm `allow_on_submit` của **field trong
child DocType** — không phải của field bảng ở cha. Cả 9 field của `Work Order Employee` đều đang
`allow_on_submit = 0`, trong khi patch `adjust_work_order_schedule_fields` chỉ set cho field bảng
`Work Order-custom_work_order_employee` ở cha. Kết quả: mọi lần tính lại trên WO đã submit đều báo
*"Not allowed to change … after submission"*.

→ Đã set `allow_on_submit = 1` cho cả 9 field của `Work Order Employee`.

⚠ **Liên quan trực tiếp tới GAP-3 và GAP-7**: nút "Bắt Đầu Sản Xuất" (C8) ấn khi WO ở *In Process*
— tức đã submit — rồi gọi `recalculate_schedule`; và bảng Sản Lượng Nhân Viên (C12) cũng sửa tay
sau khi Finish. Cả hai đều đâm vào đúng lỗi này nếu không sửa trước. Xem lại cảnh báo ở GAP-7.

**2. Hook đồng bộ Employee Allocation khi Finish là code chết**

Đăng ký ở `doc_events["Work Order"]["on_update"]`, nhưng: Work Order **không có** method
`on_update`, và status sang `Completed` được set bằng `db_set` trong `WorkOrder.update_status()`
— `db_set` không chạy hook nào. Ngoài ra WO lúc đó đã submit nên Frappe chỉ gọi
`on_update_after_submit`. Tức hook chưa từng chạy lần nào, Employee Allocation không bao giờ được
co về giờ kết thúc thật → nhân sự bị giữ chỗ theo lịch dự kiến, đẩy lùi lịch của các WO sau.

→ Đổi sang hook `update_status`, là chỗ `Stock Entry.update_work_order()` gọi bằng
`pro_doc.run_method("update_status")` — `run_method` có compose `doc_events`, và hook chạy **sau**
method gốc nên `doc.status` đã là `Completed`.

⚠ Bẫy kèm theo: trong cùng luồng đó `set_actual_dates()` chạy **sau** `update_status()`, nên
`doc.actual_end_date` lúc hook chạy vẫn là giá trị cũ. Phải tự tính thời điểm hoàn thành từ
operations / Stock Entry thay vì đọc thẳng field đó.

Cả hai lỗi **chưa được ghi nhận trên app PM** (dự án đang 0 PM Task) — cần bổ sung.
