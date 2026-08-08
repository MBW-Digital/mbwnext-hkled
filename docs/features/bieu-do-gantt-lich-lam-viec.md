# Biểu Đồ Gantt quản lý Lịch làm việc

**Khách hàng:** HKLED
**Người cung cấp thông tin:** anh Thắng (`thangdo@mbw.vn`) — người tạo PM Feature
**Người trực tiếp thao tác đã trao đổi:** ❌ CHƯA — xem mục "Còn thiếu để đủ điều kiện sang DEV"
**Ngày tiếp nhận:** 07/08/2026
**PM Project:** `PM-PRJ-00003` · **PM Feature:** `PM-FEAT-00009` (trạng thái *Analysis*)
**Tài liệu khách:** `PM-DOC-00086` "Biểu đồ tình hình làm việc của nhân sự" (kèm ảnh `Untitled.png`)

## Đầu bài gốc (nguyên văn)

> Dựa vào các bản ghi **Employee Allocation** và **Employee Schedule**
>
> Hãy thiết kế cho anh biểu đồ này để người dùng có thể dễ dàng theo dõi lịch làm việc của nhân sự,
> thời gian làm việc trong work order nào, thời gian rảnh,...

Kèm 1 ảnh mockup (`PM-DOC-00086`): tiêu đề **"Tình hình làm việc của nhân sự (Timeline)"**, một ô
*Chọn ngày xem* (23/06/2026), trục ngang 08:00→22:00, mỗi nhân sự một dòng có ghi bậc thợ bên dưới
tên. Thanh **đỏ** = `WO-001 (08h00 - 11h45)`, `WO-001 (13h15 - 16h32)`; thanh **xanh lá** = rảnh
(`Ca sáng (Rảnh)`, `Ca chiều (Rảnh)`, `Tăng ca: Rảnh (18:00 - 21:00)`); vùng **xám** = ngoài ca.
Đáng chú ý: sau thanh đỏ 13h15–16h32 có một mẩu xanh ngắn nối tới 17:00 — tức **phần còn lại của ca
sau khi xong việc vẫn tính là rảnh**.

---

## Hiện trạng đã đối chiếu (code + dữ liệu site `hkled.com`, kiểm 07/08/2026)

### Dữ liệu thật đang có

| DocType | Số bản ghi | Ghi chú |
|---|---|---|
| Employee | 3 | cả 3 đều `custom_employee_type = "Công nhân"`, Active, đủ Bậc Thợ |
| Employee Level | 5 | |
| Shift Type | 2 | Ca Sáng 08:00–11:45, Ca Chiều 13:15–17:00 |
| Employee Schedule | 53 | trải 29/07 → 12/08/2026 |
| Employee Allocation | 21 | thuộc 8 Work Order |
| Work Order | 14 | |
| Work Team | 1 | |
| Other Task | 0 | chưa ai dùng |

Quy mô rất nhỏ → **không có ràng buộc hiệu năng**. Một ngày nhiều nhất vài chục bản ghi; kể cả khi
HKLED chạy thật với ~40 nhân sự thì một ngày cũng chỉ cỡ 40 lịch + vài trăm phân công.

### Cấu trúc 2 DocType nguồn

```
Employee Schedule (không phải child table)     → KHẢ DỤNG
  employee_name (Link Employee), date, shift_type, is_over_time
  start / end (Time)  ·  start_time / end_time (Datetime, read-only, tự tính)

Employee Allocation (không phải child table)   → BẬN
  employee_name (Link Employee), work_order (Link Work Order)
  start_time / end_time (Datetime)
```

⚠ Field tên là `employee_name` nhưng **là Link tới Employee** (chứa mã nhân sự, không phải tên) —
đặt tên nhầm từ trước, giữ nguyên. Muốn hiện tên phải join `Employee.employee_name`.

---

## 4 phát hiện quyết định cách làm

### ❶ `Employee Allocation` là MỘT khoảng liên tục, KHÔNG phải các đoạn làm việc thật

`api/work_order_schedule.py::sync_employee_allocation()` ghi đúng **một** bản ghi cho mỗi cặp
(nhân sự, Work Order), với `start_time`/`end_time` là hai đầu mút của cả quá trình tham gia. Khoảng
này **bao trùm cả giờ nghỉ trưa và ban đêm**.

Bằng chứng trong dữ liệu thật — `MFG-WO-2026-00004`:

```
start_time = 2026-07-29 08:00:00
end_time   = 2026-07-30 08:28:00     ← một bản ghi, dài hơn 24 giờ
```

Vẽ thẳng bản ghi này lên timeline sẽ tô đỏ 11:45–13:15 (nghỉ trưa) và 17:00–08:00 (ban đêm) —
sai hoàn toàn so với mockup.

➜ **Toàn bộ phần "logic" của tính năng nằm ở đây, không nằm ở phần vẽ:**

```
Đoạn BẬN  = Employee Allocation  ∩  Employee Schedule   (giao từng đoạn)
Đoạn RẢNH = Employee Schedule    −  Employee Allocation (hiệu)
Vùng XÁM  = ngoài mọi Employee Schedule của ngày đó
```

Đây cũng chính là cách mockup vẽ mẩu xanh 16h32→17:00: phần ca chiều còn lại sau khi trừ đoạn bận.

### ❷ KHÔNG dùng Gantt view có sẵn của Frappe — có lỗi phá dữ liệu

Frappe v15.77 có sẵn chế độ xem Gantt, chỉ cần khai calendar settings là bật được. **Không nên**:

| Vấn đề | Chi tiết |
|---|---|
| Độ phân giải | `frappe-gantt` 0.6.0, mức nhỏ nhất là *Quarter Day* = 6 giờ/cột. Ca 3h45 gần như dính liền nhau |
| Bố cục | mỗi **bản ghi** một dòng, không gom theo nhân sự như mockup (3 nhân sự × 4 WO = 12 dòng) |
| Không vẽ được "rảnh" | rảnh không phải bản ghi nào cả — nó là phép trừ, Gantt view chỉ vẽ được cái gì có trong list |
| 🔴 **Phá dữ liệu** | kéo/co thanh → `on_date_change` gọi `frappe.db.set_value(...)` với `date_format = "YYYY-MM-DD"` ⇒ **cắt cụt Datetime thành 00:00:00**, đồng thời bỏ qua `recalculate_schedule` nên Work Order lệch hẳn khỏi Allocation |

Nguồn: `apps/frappe/frappe/public/js/frappe/views/gantt/gantt_view.js:110-116`.

Hiện `Employee Allocation` **chưa** có calendar settings nên nút Gantt chưa hiện — không có rủi ro
ngay lúc này, nhưng cũng có nghĩa "bật cho nhanh" là con đường sai.

➜ Dựng **màn hình riêng**, tự vẽ. Không cần thư viện ngoài (xem Giai đoạn 3).

### ❸ Allocation của Work Order đã Huỷ / còn Nháp vẫn nằm nguyên trong bảng

Không có `on_cancel`/`on_trash` nào xoá `Employee Allocation` (grep toàn app: không có). Dữ liệu thật
đang chứng minh điều đó:

| Work Order | status | docstatus | số allocation |
|---|---|---|---|
| MFG-WO-2026-00003 | **Cancelled** | 2 | 3 |
| MFG-WO-2026-00004 | **Draft** | 0 | 3 |
| MFG-WO-2026-00015 | **Draft** | 0 | 3 |
| MFG-WO-2026-00017 | **Draft** | 0 | 3 |

➜ Biểu đồ nếu đọc thẳng bảng Allocation sẽ **báo bận giả** cho 12/21 bản ghi hiện có.

⚠ **Đây không chỉ là chuyện hiển thị — chính engine tính lịch cũng đang dính.**
`find_conflicting_allocation_at()` và `get_next_conflicting_allocation()`
(`api/work_order_schedule.py:35-62`) lọc theo `employee_name` + thời gian, **không lọc trạng thái
Work Order**. Nghĩa là một WO đã huỷ vẫn đang chiếm chỗ của nhân sự và đẩy lùi lịch các WO sau.
Tính năng này chỉ làm lộ ra lỗi có sẵn đó. Phải chốt cách xử lý (câu **C6**) rồi sửa **một lần cho
cả hai chỗ**, không vá riêng cho biểu đồ.

### ❹ `Other Task` không đặt được lên trục giờ

`Other Task` (GAP-8, Phần IV) chỉ có `date` + `Other Task Table.time` (Float, **số phút**) — **không
có giờ bắt đầu/kết thúc**. Vậy nếu một người mất 120 phút làm việc khác trong ngày, biểu đồ vẫn báo
họ **rảnh** cả ca. Đây là câu hỏi nghiệp vụ thật, không phải chi tiết kỹ thuật → câu **C7**.

---

## Giai đoạn 1 — 5W

| | |
|---|---|
| **WHAT** | Một màn hình xem (chỉ đọc) trả lời trong một cái nhìn: ngày hôm đó ai đang làm Work Order nào, từ mấy giờ tới mấy giờ, còn trống khoảng nào. Không tạo/sửa dữ liệu nào. |
| **WHEN** | Người dùng chủ động mở và chọn ngày. Không có trigger tự động, không job nền. |
| **WHO** | Quản lý sản xuất (`Manufacturing Manager`) và tổ trưởng (`Manufacturing User`) — đúng 2 vai trò đã được cấp quyền đọc `Employee Schedule`/`Employee Allocation`/`Employee` ở PM-FEAT-00008. ⚠ Phải áp User Permission: người bị giới hạn chỉ thấy nhân sự của mình thì biểu đồ **không** được lộ người khác (đúng lỗi rò rỉ đã vấp ở TC-PERM của PM-FEAT-00008). |
| **WHERE** | Desk, màn hình riêng. Chỉ máy tính, không làm mobile/PWA lần này (chốt **C8**). |
| **ERROR** | Không có ca "sai dữ liệu" nào cần chặn — đây là màn hình đọc. Ngày không có lịch → hiện thông báo trống, không báo lỗi đỏ. |

**Business requirement (1 câu):**
> Cho phép quản lý sản xuất chọn một ngày và nhìn thấy, theo từng nhân sự, các đoạn thời gian đang
> bận vì Work Order nào và các đoạn còn rảnh trong ca — suy ra bằng cách giao/trừ `Employee Allocation`
> với `Employee Schedule`, không sửa bất kỳ dữ liệu nào.

---

## Giai đoạn 2A — Tầng

| | |
|---|---|
| **Tầng** | **4 — app khách `mbwnext_hkled`** |
| **Lý do** | Câu 4 trong bảng Giai đoạn 2A: không phải quy định pháp luật VN (câu 1); chưa có khách thứ hai nào yêu cầu (câu 2); không phải module bật/tắt dùng lại (câu 3). `Employee Schedule` / `Employee Allocation` / `Work Team` / engine tính lịch **đều là tài sản riêng của `mbwnext_hkled`** — không app lõi nào biết tới chúng, nên đưa xuống lõi cũng vô nghĩa. |
| **Luật vàng** | Phân vân → chọn tầng cao hơn. Ở đây không phân vân: dữ liệu nguồn chỉ tồn tại ở tầng 4. |

### Va chạm

| Khía cạnh | Kết quả |
|---|---|
| DocType/event sẽ hook | Bản thân biểu đồ **không hook gì** (chỉ đọc). Nhưng quyết định **C6** kéo theo 2 hook mới: `Work Order.on_cancel` và `Work Order.on_trash` để dọn `Employee Allocation` |
| App khác đang hook cùng chỗ | `Work Order` hiện đã có 4 hook của chính app này (`update_status`, `before_insert`, `validate`, `before_update_after_submit`) — **chưa** có `on_cancel`/`on_trash`, nên không chồng lên nhau. Không app nào khác hook `Employee Schedule`/`Employee Allocation` (grep `apps/*/*/hooks.py`) |
| Ghi cùng trường/tài liệu? | Hook mới chỉ **xoá** `Employee Allocation` và xoá link `allocation_record` trên dòng con — không app nào khác đụng 2 chỗ đó |
| Override xuyên tầng? | Không |

Rủi ro va chạm thấp. Riêng phần C6 đụng vào code Phần III đã bàn giao → phải chạy lại test hồi quy
lịch sản xuất, xem mục "Phần việc kèm theo (C6)".

---

## Giai đoạn 2B — Định tuyến app

Tầng 4 nên đích đã rõ: `mbwnext_hkled`. Không chồng lên app lõi nào (`advanced_stock`,
`advanced_selling`, `pos_next` đều không liên quan). Không đụng 4 hàm override
`pos_next ↔ advanced_selling`.

---

## Giai đoạn 3 — Cơ chế kỹ thuật

### Chọn dạng màn hình

| Phương án | Đánh giá |
|---|---|
| Bật Gantt view sẵn có | ❌ đã loại ở phát hiện ❷ |
| Query Report | ❌ báo cáo dạng bảng, không vẽ được thanh thời gian |
| **Desk Page riêng** (`page/`) | ✅ **chọn** — toàn quyền bố cục, có sẵn khung Desk (quyền, breadcrumb, thanh tiêu đề), URL `/app/<ten-page>` |
| Trang `www/` (web) | ❌ chỉ cần khi làm cho mobile/khách ngoài — chưa có yêu cầu, xem C8 |

### Vẽ bằng gì

**Không dùng thư viện ngoài.** Mỗi thanh là một `<div>` định vị theo phần trăm:

```
left  = (phút_bắt_đầu − phút_đầu_trục) / tổng_số_phút_trục × 100%
width = độ_dài_phút / tổng_số_phút_trục × 100%
```

Lý do: mockup chỉ cần thanh ngang phẳng, không cần phụ thuộc/kéo thả/thu phóng. Thêm thư viện chỉ
tốn dung lượng ổ đĩa server (đã là ràng buộc đã biết của nền tảng) mà không được gì.

### Backend

| Khía cạnh | Giá trị |
|---|---|
| Cơ chế | 1 hàm **whitelisted** trong `api/employee_timeline.py` + 1 **Desk Page** |
| Chữ ký | `get_timeline(date, work_team=None)` |
| Truy vấn | **`frappe.get_list`** cho cả `Employee`, `Employee Schedule`, `Employee Allocation` — **tuyệt đối không `frappe.get_all`** |
| Custom Field | Không thêm field nào |
| Fixtures | Không đổi |
| Version | v15 |

⚠ **`frappe.get_all` không áp User Permission** — đây đúng là lỗi rò rỉ dữ liệu nghiêm trọng nhất đã
vấp ở PM-FEAT-00008 (dialog chọn đội trả về cả nhân sự ngoài quyền). Tính năng này đọc đúng loại dữ
liệu đó nên phải dùng `get_list` ngay từ dòng code đầu tiên, và test case phải có ca **đổi user rồi
chạy lại** — chạy bằng `Administrator` thì mọi thứ đều trông đúng.

### Thuật toán (chạy server-side, trả JSON đã tính sẵn)

```
1. Nhân sự = get_list(Employee, status="Active",
                      custom_employee_type="Công nhân")        ← chốt C2 (11:21) — chữ thường
             nếu người dùng có chọn đội  → lọc custom_work_team IN (<các đội đã tích>)
             không chọn đội nào          → không lọc thêm, hiện hết công nhân
2. Với mỗi nhân sự:
   a. lich[]  = get_list(Employee Schedule, employee_name=e, date=<ngày>)
                → [(start_time, end_time, shift_type, is_over_time)]
                không có lịch → dòng vẫn hiện, toàn xám (chốt C2)
   b. phancong[] = get_list(Employee Allocation, employee_name=e,
                            start_time < cuối_ngày, end_time > đầu_ngày)   ← giao với NGÀY, vì
                            một allocation có thể trải nhiều ngày (phát hiện ❶)
   c. ban[]   = với mỗi (ca, pc): giao 2 khoảng → đoạn bận thật
   d. ranh[]  = mỗi ca trừ đi các đoạn bận (gộp đoạn liền kề)
3. Trục giờ = CỐ ĐỊNH 08:00 → 24:00 (chốt C3)
```

Bước 2b **không cần lọc trạng thái Work Order**: theo chốt C6, phân công của lệnh đã huỷ/đã xoá sẽ
bị dọn ngay tại nguồn, nên bảng `Employee Allocation` luôn sạch. Lọc thêm ở đây là vá triệu chứng và
che mất lỗi ở engine.

Bước `2c`/`2d` là phép giao/trừ khoảng kinh điển, ~40 dòng Python, không có gì phức tạp.

---

## Technical Specification — mbwnext_hkled

### Summary
Một Desk Page chỉ-đọc vẽ timeline theo ngày: mỗi nhân sự một dòng, đoạn đỏ = đang làm Work Order,
đoạn xanh = rảnh trong ca, xám = ngoài ca.

### Layer & Collision
| Aspect | Value |
|---|---|
| Tầng thực thi | **4 — app khách** |
| Lý do chọn tầng | Câu 4 bảng 2A; dữ liệu nguồn chỉ tồn tại trong `mbwnext_hkled` |
| DocType/event sẽ hook | không hook |
| App khác đang hook cùng chỗ | không |
| Hai bên ghi cùng trường? | không ghi gì |
| Override xuyên tầng? | không |

### Implementation
| Aspect | Value |
|---|---|
| File mới | `mbwnext_hkled/api/employee_timeline.py` · `mbwnext_hkled/page/<slug>/` (js + json + css) |
| File sửa (C6) | `controllers/python_hook/work_order.py` + `hooks.py` |
| DocType(s) đọc | Employee, Employee Level, Employee Schedule, Employee Allocation, Work Order, Work Team |
| Trigger | người dùng mở trang / đổi ngày / đổi bộ lọc đội (đa chọn) |
| Mechanism | Whitelisted method + Desk Page (JS thuần, không thư viện ngoài) + 2 doc_events cho C6 |
| Trục thời gian | cố định 08:00 → 24:00 |
| Fixture convention | không phát sinh Custom Field |
| Version | v15 |

### Data Flow
1. Người dùng mở trang, chọn ngày (mặc định hôm nay), chọn Đội (tuỳ chọn).
2. JS gọi `mbwnext_hkled.api.employee_timeline.get_timeline`.
3. Server dựng danh sách nhân sự → lấy lịch + phân công của ngày → giao/trừ khoảng → trả JSON
   `{truc_gio, nhan_su: [{ten, bac_tho, doan: [{loai, tu, den, nhan, work_order}]}]}`.
4. JS vẽ mỗi đoạn thành một `<div>` định vị theo phần trăm; bấm đoạn đỏ → mở Work Order.

### Cross-app impact
Không. Không phụ thuộc `mbwnext_localization` ngoài phần nền chung, không đụng `pos_next`.

### Error Handling
| Tình huống | Xử lý |
|---|---|
| Ngày không có Employee Schedule nào | vẫn hiện đủ danh sách nhân sự, tất cả các dòng toàn xám. **Không** báo lỗi đỏ |
| Nhân sự có lịch nhưng không có phân công | vẽ nguyên ca màu xanh (rảnh) — đúng nghiệp vụ, không phải lỗi |
| Nhân sự không có lịch ngày đó | **vẫn hiện dòng**, toàn xám (chốt C2, 11:23 — khác đề xuất ban đầu là ẩn) |
| Nhân sự không phải Công nhân | **không hiện** (chốt C2, 11:21) |
| Chọn đội không có ai | hiện danh sách rỗng kèm dòng chữ giải thích, không báo lỗi |
| Người dùng bị User Permission giới hạn | chỉ trả về nhân sự trong quyền, **không** báo lỗi, **không** âm thầm trả hết |

### Required Skills
- [ ] `erpnext-syntax-whitelisted` — chữ ký hàm API, kiểu trả về
- [ ] `erpnext-impl-whitelisted` — mẫu kiểm quyền trong API
- [ ] `erpnext-permissions` — `get_list` vs `get_all`, User Permission
- [ ] `erpnext-mbwnext-customer-app` — bắt buộc **dựng mockup HTML và chốt trước khi viết logic**
- [ ] `erpnext-errors-api` — thông báo lỗi phía API

### Validation Criteria
1. Dựng đúng ví dụ trong ảnh mockup của khách rồi so từng mốc: 08:00–11:45 đỏ, 11:45–13:15 xám,
   13:15–16:32 đỏ, 16:32–17:00 xanh.
2. Ca kiểm chứng ❶: WO trải 2 ngày (như `MFG-WO-2026-00004`: 29/07 08:00 → 30/07 08:28) — xem ngày
   29/07 và 30/07 phải ra 2 mảnh khác nhau, **không** mảnh nào đè lên giờ nghỉ trưa/ban đêm.
3. Ca kiểm chứng ❸/C6: huỷ một Work Order → các `Employee Allocation` của nó **biến mất khỏi bảng**
   (không phải "còn nhưng bị ẩn"); xoá hẳn Work Order cũng vậy. Sau đó `Tính Lại Lịch` một WO khác
   của cùng nhân sự phải cho ra thời điểm bắt đầu **sớm hơn** trước khi dọn — chứng minh chỗ bị
   chiếm đã được trả lại.
4. Ca kiểm chứng quyền: đăng nhập bằng user bị User Permission giới hạn 1 nhân sự → chỉ thấy đúng
   1 dòng. Chạy bằng `Administrator` **không** tính là đã test.
5. Đối chiếu chéo: tổng số phút đỏ của một nhân sự trong một WO phải khớp phần `Nhân Công Tham Gia`
   trên chính Work Order đó.

---

## ĐÃ CHỐT — Thắng trả lời 08/08/2026 09:44 (bình luận trên PM-FEAT-00009)

| # | Câu hỏi | **Chốt** | So với đề xuất |
|---|---|---|---|
| **C1** | Một ngày hay cả tuần? | **Một ngày** | ✅ giống |
| **C2** | Hiện những ai? | **Chỉ nhân sự có Loại Nhân Sự = "Công nhân"** (chốt bổ sung 08/08 11:21 sau khi xem mockup). Người **không có lịch** ngày đó **vẫn hiện**, dòng toàn xám (11:23). Bộ lọc Đội Sản Xuất ở trên, **cho chọn nhiều đội**; tích đội nào thì chỉ hiện thành viên các đội đó; **không tích gì = hiện tất cả công nhân** | ❗ chốt **hai lần**: ban đầu "hiện hết mọi người", sau khi mockup cho thấy dòng Kế toán thì thu lại còn Công nhân |
| **C3** | Trục giờ | **Cố định 08:00 – 24:00** | ❗ **khác** — đề xuất cũ là co giãn; ảnh mockup là 08:00–22:00 |
| **C4** | Nghỉ trưa để xám? | **Đúng** | ✅ giống |
| **C5** | Phân biệt kế hoạch/thực tế? | **Không.** Phần đỏ là thời gian người đó tham gia lệnh sản xuất, lấy theo `Employee Allocation` | ✅ giống |
| **C6** | Phân công của WO huỷ/nháp | **Huỷ lệnh sản xuất thì xoá luôn phân công tương ứng; xoá lệnh sản xuất cũng xoá phân công tương ứng** | ✅ giống, và mở rộng thêm ca **xoá** |
| **C7** | Hiện Công Việc Khác? | **Không** — "công việc khác họ tự quản lý ngoài" | ✅ giống |
| **C8** | Thiết bị | **Máy tính** | ✅ giống |

Hai điểm tự quyết không bị phản đối, coi như chốt: bấm thanh đỏ mở Work Order; **không** kéo thả sửa
lịch trên biểu đồ.

### Điểm C2 — đã chốt lại sau khi xem mockup

Câu trả lời đầu (08/08 09:44) là *"hiện hết tất cả mọi người"*. Mockup cố ý dựng thêm dòng
**Lê Thị F — Kế toán** để cho thấy hệ quả trên dữ liệu thật (HKLED có cả Bán hàng và Kế toán, họ
sẽ chiếm nhiều dòng xám trên một biểu đồ dành cho sản xuất). Nhìn thấy dòng đó, anh Thắng chốt lại:

> *"Giới hạn giúp anh là biểu đồ này chỉ hiện những nhân sự có Loại Nhân Sự là Công Nhân thôi nhé"*
> — 08/08 11:21
>
> *"người không có lịch hôm đó vẫn hiện nhé"* — 08/08 11:23

➜ Điều kiện cuối cùng: `status = "Active"` **và** `custom_employee_type = "Công nhân"`; không lọc
theo việc có lịch hay không.

⚠ So chuỗi phải đúng **`"Công nhân"`** — options thật trên site là *Công nhân / Bán hàng / Kế toán*
(chữ thường), không phải *"Công Nhân"* như tài liệu nghiệp vụ viết. `employee.js` đang so đúng chuỗi
này, code mới phải theo.

Đây chính là lý do mockup phải dựng trước khi viết logic: một câu trả lời bằng lời ("hiện hết") và
cùng câu đó khi nhìn thấy trên màn hình lại ra hai kết quả khác nhau.

### Điểm C6 chưa được trả lời hết: lệnh sản xuất còn **Nháp**

Thắng chốt ca **Huỷ** và ca **Xoá**, không nói về WO còn Nháp (hiện đang có 9 bản ghi phân công
thuộc 3 WO nháp). Hiểu hợp lý: WO nháp là **kế hoạch sắp tới**, vẫn nên giữ chỗ của nhân sự, nên
không dọn. Ghi lại đây làm giả định đang áp dụng; nếu sai thì sửa rất nhẹ (thêm điều kiện lọc).

## Phần việc kèm theo (C6) — ✅ ĐÃ LÀM XONG 08/08/2026 (`PM-TASK-00045`)

Đây **không phải phần của biểu đồ**, mà là lỗi có sẵn được lộ ra. Tách thành `PM-TASK-00045` để
không lẫn vào khối lượng của tính năng này. Đã làm:

1. `doc_events["Work Order"]["on_cancel"]` + `["on_trash"]` → `cleanup_employee_allocation()` xoá
   `Employee Allocation` của lệnh đó.
2. ⚠ **Xoá link trước, xoá bản ghi sau.** `Work Order Employee.allocation_record` là Link tới
   `Employee Allocation`, nên `frappe.delete_doc` sẽ ném `LinkExistsError`
   (`frappe/model/delete_doc.py:130` gọi `check_if_doc_is_linked`). Đã xoá trắng
   `allocation_record` bằng `frappe.db.set_value` rồi mới xoá. **Không** dùng `force=True` để né —
   nó tắt luôn mọi kiểm tra liên kết khác.
3. Không sửa `find_conflicting_allocation_at` / `get_next_conflicting_allocation` — dọn tại nguồn
   nên bảng luôn sạch, chỉ phải đúng ở một chỗ thay vì nhớ thêm điều kiện lọc ở mọi chỗ đọc.
4. Patch `cleanup_cancelled_work_order_allocations` dọn dữ liệu tồn: **7 bản ghi mồ côi** của 3
   lệnh đã huỷ (`MFG-WO-2026-00003`, `-00022`, `-00026`) — nhiều hơn con số 3 ước lượng ban đầu vì
   site phát sinh thêm sau đó.

### Phát hiện thêm khi làm: link Phân Công bị mang sang lệnh mới

Trong 7 bản ghi mồ côi có **14 dòng** *Nhân Công Tham Gia* trỏ tới, và đáng chú ý là chúng thuộc cả
những lệnh **Sửa đổi** đang hoạt động (`MFG-WO-2026-00022-1`, `-2`, `MFG-WO-2026-00026-1`) — tức là
lệnh mới mang link trỏ vào Phân Công của lệnh gốc đã huỷ.

Hậu quả nếu để nguyên: `sync_employee_allocation()` thấy `allocation_record` đã có thì **cập nhật**
bản ghi đó thay vì tạo mới, nên lịch của lệnh mới bị ghi vào bản ghi vẫn mang `work_order` của lệnh
cũ — rồi chính nó lại bị tính là xung đột với lệnh mới.

Đã chặn ở **cả hai đường**, vì chúng khác nhau:

| Đường | Cách chặn |
|---|---|
| **Nhân bản** | `no_copy = 1` trên `Work Order Employee.allocation_record` |
| **Sửa đổi** (Amend) | `no_copy` **không có tác dụng** — `create_new.js` cố ý bỏ qua nó khi Amend (`is_no_copy = !from_amend && df.no_copy`). Phải thêm hook `before_insert` → `clear_copied_allocation_record()` |

Test: `TC-EDGE-14…17` trong `docs/testcases/bac-tho-lich-san-xuat.md`, cả 4 Pass trên bench dev.

## Trạng thái điều kiện sang DEV

- [x] Có tài liệu khách hàng (ảnh mockup `PM-DOC-00086`)
- [x] Đã hỏi ≥2 câu về ngoại lệ (C6, C7) — **đã có trả lời**
- [x] Biết quy mô dữ liệu (nhỏ) và thiết bị sử dụng (máy tính, C8)
- [x] Đã chốt "không làm gì" lần này: không xem theo tuần, không hiện Công Việc Khác, không kéo thả
      sửa lịch, không làm mobile
- [ ] **Chưa hỏi người trực tiếp thao tác** — anh Thắng là người yêu cầu, chưa hỏi quản đốc/tổ trưởng
      là người sẽ mở màn hình này hằng ngày. Mockup sẽ đóng vai trò này (xem dưới)
- [ ] Chưa rõ **ai nghiệm thu** tính năng này

➜ Bước tiếp theo: dựng **mockup HTML** `docs/mockups/bieu-do-gantt-lich-lam-viec.html` với dữ liệu
thật của một ngày cụ thể, đưa anh Thắng + người dùng thật duyệt. Chốt mockup rồi mới viết logic —
đúng bài học PM-FEAT-00007. Gate `intake_ready` tick khi có xác nhận trong hội thoại.
