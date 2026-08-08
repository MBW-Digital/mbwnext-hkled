# Test case — Bậc Thợ & Lịch Sản Xuất (Phần II/III/IV, GAP-1…GAP-8)

| | |
|---|---|
| App | `mbwnext_hkled` |
| DocType liên quan | Work Team, Employee Schedule, Employee Allocation, Employee Production, Other Task, Work Order, Production Plan, Sales Order, Stock Entry |
| Đầu bài + spec | `apps/mbwnext_hkled/docs/features/bac-tho-lich-san-xuat.md` |
| Mockup | `apps/mbwnext_hkled/docs/mockups/bac-tho-lich-san-xuat.html` |
| PM Feature | `PM-FEAT-00008` (dự án `PM-PRJ-00003`) |
| Người viết / Ngày | Trợ lý Claude / 2026-08-03 |

## Điều kiện chuẩn bị

**Môi trường:** develop, bench `/home/mbw/mbw-dev/cozy_dev`, site `hkled.com`

**Địa chỉ vào:**

| Test từ đâu | Địa chỉ |
|---|---|
| **Ngay trên máy chạy bench** | `http://localhost:8012/app` |
| **Máy khác trong mạng** | `http://dev.mbwnext.com:8012/app` |

Bench có `default_site = hkled.com` + `serve_default_site = true` nên mọi hostname vào
cổng 8012 đều ra site `hkled.com` — không cần cấu hình gì thêm ở phía site.

⚠ **Đừng gõ thẳng `hkled.com`** — tên miền đó phân giải ra IP thật ngoài internet
(`183.129.217.194`), không phải máy dev.

**Tài khoản:** `Administrator` / `<mật khẩu — người giao test điền>`
Không có mật khẩu thì lấy link đăng nhập một lần trên máy chạy bench:
`bench browse hkled.com --user Administrator` — lấy phần `sid=` rồi ghép thành
`http://localhost:8012/app?sid=...` (hoặc `dev.mbwnext.com` nếu test từ máy khác).

⚠ `sid` phải gắn vào **`/app`**, không phải route con — vào thẳng
`/app/work-team?sid=...` sẽ bị đá về màn hình đăng nhập.

**Dữ liệu sẵn có trên site (đã kiểm 2026-08-03):**

| Bản ghi | Ghi chú |
|---|---|
| Nhân sự `Anh A`, `Anh B`, `Anh C` | đều Active, Loại = *Công nhân*, có Bậc Thợ |
| Bậc Thợ `Bậc 7` (100%, 1.080đ/phút), `Bậc 6` (90%, 920đ/phút) | dùng để đối chiếu lương và năng lực |
| Ca `Ca Sáng` 08:00–11:45, `Ca Chiều` 13:15–17:00 | |
| Item `Thành phẩm 1` | có serial + batch, `Thời Gian Sản Xuất` = **10 phút**, BOM mặc định `BOM-Thành phẩm 1-001` |
| `NVL 1` / `NVL 2` / `NVL 3` | tồn 99 / 98 / 97 ở `Kho nguyên vật liệu - HKL`, có lô `t1` / `t2` / `t3` |
| Khách hàng `a`, Công ty `HKLED` | |
| 11 Lịch làm việc (29–30/07/2026) | dữ liệu gốc, **đừng xoá** |

**Dữ liệu tự tạo khi test:** đặt tiền tố `HKLED-TEST` cho Đội Sản Xuất và Công Việc Khác.
Chứng từ (Đơn bán / Kế hoạch / Lệnh sản xuất / Phiếu kho) sinh theo số tự động — ghi lại mã để huỷ và xoá sau.

**⚠ Chặn trước khi test luồng sản xuất — vấn đề DỮ LIỆU, không phải lỗi code:**
`Thành phẩm 1` bật **cả** *Có Serial* lẫn *Có Lô*, mà site chưa có lô nào cho nó → phiếu
Manufacture báo `Batch No is mandatory for Item Thành phẩm 1` và **không submit được**.
Muốn chạy TC-HAPPY-06/07 phải tắt tạm *Có Lô* trên `Thành phẩm 1` rồi bật lại sau.
Đây đúng là vấn đề 36.890 item bật cả batch đã nêu trong spec, chờ HKLED dọn.

**Cách vào từng tính năng (đường bấm thật):**

| Tính năng | Đường vào |
|---|---|
| GAP-1 Đội Sản Xuất | Thanh tìm kiếm → gõ `Work Team` → *Add Work Team* |
| GAP-1 Bậc Thợ bắt buộc | Nhân Sự (Employee) → mở 1 nhân sự → tab thông tin, trường *Bậc Thợ* |
| GAP-2 Tạo nhanh lịch | `Employee Schedule` → danh sách → nút **Tạo Nhanh** trên thanh công cụ |
| GAP-3 Bắt đầu sản xuất | Lệnh sản xuất đang *In Process* → nút **Bắt Đầu Sản Xuất** |
| GAP-4 Trường mới | Đơn Bán Hàng → mục *Thông Tin Sản Xuất*; Kế Hoạch Sản Xuất → bảng *Sales Orders* |
| GAP-5 Thừa hưởng | Kế Hoạch Sản Xuất → nút *Create* → *Work Order* |
| GAP-6 Thêm đội vào lệnh | Lệnh sản xuất → nút **Thêm Đội Sản Xuất** |
| GAP-7 Sản lượng + serial | Lệnh sản xuất → mục *Sản Lượng Nhân Viên*; serial xem ở `Serial No` |
| GAP-8 Công Việc Khác | Thanh tìm kiếm → gõ `Other Task` → *Add Other Task* |

---

## Bảng test case

Cột **KQ thực tế** là kết quả vòng một do Claude tự chạy trên site dev ngày 03/08/2026.
Người test lại tay mới là người chốt Pass/Fail để nghiệm thu.

### TC-HAPPY — luồng đúng

| Mã | Mục tiêu | Bước thực hiện | Dữ liệu vào | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|---|
| TC-HAPPY-01 | Tạo Đội Sản Xuất | 1. Vào `Work Team` → Add<br>2. Nhập Tên Đội<br>3. Lưu | Tên: `HKLED-TEST Doi Lap Rap` | Lưu được, mã bản ghi chính là tên đội, *Đang Hoạt Động* mặc định bật | Pass — lưu được, tên bản ghi = `HKLED-TEST Doi Lap Rap` (kiểm qua giao diện) | Pass |
| TC-HAPPY-02 | Tạo nhanh lịch theo đội + khoảng ngày + thứ | 1. `Employee Schedule` → **Tạo Nhanh**<br>2. Chọn đội<br>3. Từ 01/04/2027 đến 10/04/2027<br>4. Giữ tick T2–T7, bỏ CN<br>5. Chọn Ca Sáng<br>6. Bấm *Tạo Lịch Làm Việc* | 3 nhân sự của đội | Dòng đếm ghi *"Sẽ tạo 27 lịch làm việc (9 ngày × 3 nhân sự, bỏ qua 1 ngày không khớp thứ)"*. Tạo đúng 27 bản ghi, **không có ngày 04/04 (Chủ nhật)** | Pass — 27 bản ghi, danh sách không có 04/04, giờ lấy đúng Ca Sáng 08:00 (bấm trên giao diện) | Pass |
| TC-HAPPY-03 | Trường mới trên Đơn Bán Hàng | 1. Tạo Đơn Bán Hàng<br>2. Điền *Thời Gian Bắt Đầu*, *Giờ Cần Hoàn Thành*, *Ghi Chú Sản Xuất*<br>3. Lưu + Duyệt | KH `a`, `Thành phẩm 1` × 20, giao 14/08/2026, giờ 17:00 | Lưu được, 3 trường giữ nguyên giá trị | Pass — `SAL-ORD-2026-00002` (chạy qua API server) | Pass |
| TC-HAPPY-04 | Thời Điểm Cần Hoàn Thành ghép 2 trường | 1. Tạo Kế Hoạch Sản Xuất từ đơn trên<br>2. Gán *Đội Sản Xuất* cho dòng đơn<br>3. Lưu + Duyệt | Kế hoạch 20 cái | Dòng đơn có *Thời Điểm Cần Hoàn Thành* = **14-08-2026 17:00:00** (= Ngày Giao + Giờ Cần Hoàn Thành), *Ghi Chú* và *Thời Gian Bắt Đầu* lấy từ đơn | Pass — `14-08-2026 17:00:00`, ghi chú + giờ bắt đầu đúng (API server) | Pass |
| TC-HAPPY-05 | WO thừa hưởng thời gian + nhân sự đội | 1. Từ Kế Hoạch → *Create* → *Work Order* | | WO có *Thời Gian Bắt Đầu* = 03-08-2026 08:00, *Thời Điểm Cần Hoàn Thành* = 14-08-2026 17:00, và bảng Nhân Công Tham Gia **tự có đủ 3 người** của đội | Pass — `MFG-WO-2026-00008`, đủ Anh A/B/C (API server) | Pass |
| TC-HAPPY-06 | Nút Bắt Đầu Sản Xuất + tính lại lịch | 1. Duyệt WO, chuyển NVL để lệnh sang *In Process*<br>2. Bấm **Bắt Đầu Sản Xuất** → *Yes* | 20 cái × 10 phút, 3 người (100+100+90%) | Hộp xác nhận hiện. Sau khi đồng ý: *Thời Gian Bắt Đầu* = giờ hiện tại, *Tổng Thời Gian Dự Kiến* = **69 phút**, kết thúc **09:08:57** (bắt đầu 08:00 do ca sáng gần nhất). Cờ *Đã Bắt Đầu Sản Xuất* bật, **nút tự ẩn** | Pass — đúng 69 phút, 09:08:57, nút ẩn sau khi ấn (bấm trên giao diện) | Pass |
| TC-HAPPY-07 | Chia sản lượng + sinh serial khi Finish | 1. Làm phiếu Manufacture cho đủ 20 cái<br>2. Mở lại WO xem *Sản Lượng Nhân Viên*<br>3. Vào `Serial No` lọc theo `26-%` | | Trạng thái *Completed*. Sản lượng chia **Anh A 8 / Anh B 6 / Anh C 6** (phần dư dồn dòng đầu). Sinh **20 serial** `26-00002-0001` … `26-00002-0020` | Pass — đúng 8/6/6, 20 serial liên tục (API server; phải tắt tạm *Có Lô* của `Thành phẩm 1`) | Pass |
| TC-HAPPY-08 | Thêm cả đội vào lệnh đang có sẵn người | 1. Mở 1 WO đã có `Anh C` trong bảng<br>2. Bấm **Thêm Đội Sản Xuất** → chọn đội → *Xác Nhận* | | `Anh C` hiện mờ, ghi *"đã có trong bảng"*, **không tick được**. Chỉ Anh A + Anh B được thêm, bảng không có dòng trùng | Pass — bảng thành `[Anh C, Anh A, Anh B]` (bấm trên giao diện) | Pass |
| TC-HAPPY-09 | Công Việc Khác chia đều + tính lương | 1. Tạo `Other Task`<br>2. Tổng Thời Gian = 90<br>3. Thêm 3 dòng Anh A/B/C, để trống thời gian<br>4. Lưu | 90 phút | Tự chia **30/30/30**. Lương: Anh A 32.400, Anh B 32.400, Anh C 27.600. **Tổng Lương = 92.400** | Pass — đúng từng con số (bấm trên giao diện) | Pass |
| TC-HAPPY-10 | Đồng bộ Phân Công khi Finish | Sau TC-HAPPY-07, mở `Employee Allocation` của WO đó | | *Kết Thúc* co từ giờ dự kiến về **giờ hoàn thành thật** của lệnh | Pass — co từ 09:08:57 → 00:16:23 (đúng `actual_end_date`) | Pass |

### TC-VALID — kiểm tra dữ liệu (mỗi `frappe.throw` một dòng)

| Mã | Mục tiêu | Bước thực hiện | Dữ liệu vào | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|---|
| TC-VALID-01 | Bậc Thợ bắt buộc với Công nhân (C1) | Mở 1 nhân sự, Loại = *Công nhân*, xoá *Bậc Thợ*, Lưu | | Chặn lưu: **Nhân sự {0} là Công nhân nên bắt buộc phải có Bậc Thợ** | ⚠ Vòng đầu **Fail** — lưu được. `mandatory_depends_on` của Frappe **chỉ chạy phía client**, script/API lọt hết. Đã thêm hook server `Employee.validate`, chạy lại **Pass** (API server) | Pass |
| TC-VALID-02 | Không chọn nhân sự | Tạo Nhanh → bỏ tick hết nhân sự → Tạo | | Chặn: **Chưa chọn nhân sự nào** | Pass — chặn đúng nguyên văn (API server) | Pass |
| TC-VALID-03 | Không chọn thứ nào | Tạo Nhanh → bỏ tick cả 7 thứ → Tạo | | Chặn: **Chưa chọn thứ nào trong tuần** | Pass — dòng đếm đỏ *"Không ngày nào trong khoảng khớp thứ đã chọn."* (giao diện) | Pass |
| TC-VALID-04 | Đến Ngày trước Từ Ngày | Từ 10/08 → Đến 01/08 | | Chặn: **Đến Ngày phải từ Từ Ngày trở đi** | Pass — dòng đếm đỏ đúng câu (giao diện, mockup) | Pass |
| TC-VALID-05 | Khoảng quá dài | Từ 01/08 → Đến 31/12 | 153 ngày | Chặn: **Khoảng 153 ngày, vượt quá 62 ngày cho phép** | Pass — báo đúng số ngày (giao diện) | Pass |
| TC-VALID-06 | Tăng ca thiếu giờ | Tick *Là Tăng Ca*, để trống Bắt Đầu/Kết Thúc | | Chặn: **Tăng ca phải nhập Bắt Đầu và Kết Thúc** | Pass — chặn đúng nguyên văn (API server) | Pass |
| TC-VALID-07 | Không chọn ca | Không tick tăng ca, để trống *Ca Làm Việc* | | Chặn: **Vui lòng chọn Ca Làm Việc** | Pass — chặn đúng nguyên văn (API server) | Pass |
| TC-VALID-08 | Không ngày nào khớp thứ | Từ 02/08 đến 02/08 (Chủ nhật), chỉ tick T2–T7 | | Chặn: **Không ngày nào trong khoảng khớp thứ đã chọn** | Pass — gặp đúng khi mở dialog vào Chủ nhật (giao diện) | Pass |
| TC-VALID-09 | Bắt đầu sản xuất khi lệnh chưa duyệt | Mở WO nháp | | Nút **Bắt Đầu Sản Xuất** không hiện | Pass — nút ẩn (giao diện) | Pass |
| TC-VALID-10 | Bắt đầu sản xuất khi lệnh chưa *In Process* | Mở WO đã duyệt, trạng thái *Not Started* | | Nút không hiện; gọi thẳng API báo **Chỉ ấn được khi Lệnh sản xuất đang ở trạng thái In Process (hiện tại: Not Started)** | Pass — nút ẩn (giao diện) **và** gọi thẳng API bị chặn đúng nguyên văn (API server) | Pass |
| TC-VALID-11 | Ấn Bắt Đầu Sản Xuất lần hai | Dựng WO *In Process*, gọi API lần 1 rồi gọi lại lần 2 | | Lần 1 chạy được; lần 2 báo **Lệnh sản xuất này đã được bắt đầu rồi, không ấn lại được** | Pass — lần 1 OK (2 cái → 7 phút), lần 2 chặn đúng nguyên văn (API server); nút cũng đã ẩn trên giao diện | Pass |
| TC-VALID-12 | Tổng Công Việc Khác lệch | Sau TC-HAPPY-09, sửa dòng Anh A thành 50 (tổng 110 ≠ 90), Lưu | | Chặn: **Tổng thời gian các dòng (110.0 phút) phải bằng Tổng Thời Gian (90.0 phút). Đang vượt 20.0 phút.** | Pass — chặn đúng nguyên văn (API server) | Pass |
| TC-VALID-13 | Đổi Tổng Thời Gian mà không sửa dòng | Đổi Tổng Thời Gian thành 200, Lưu | | Chặn: **… Đang thiếu 110.0 phút.** | Pass (API server) | Pass |
| TC-VALID-14 | Tổng Sản Lượng Nhân Viên lệch | Sau khi Finish, sửa 1 dòng sản lượng cho tổng ≠ số đã sản xuất, Lưu | | Chặn: **Tổng Sản Lượng Nhân Viên (x cái) phải bằng Số Lượng Đã Sản Xuất (y cái). Đang vượt/thiếu z cái.** | Pass — `Tổng Sản Lượng Nhân Viên (24 cái) phải bằng Số Lượng Đã Sản Xuất (20 cái). Đang vượt 4 cái.` (API server) | Pass |

### TC-EDGE — biên & lặp (mỗi nhánh thoát sớm một dòng)

| Mã | Mục tiêu | Bước thực hiện | Dữ liệu vào | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|---|
| TC-EDGE-01 | Tạo nhanh lần hai lên cùng khoảng | Chạy lại y hệt TC-HAPPY-02 | | Báo **"Đã tạo 0 lịch làm việc. Bỏ qua 27 dòng do trùng lịch:"** kèm danh sách 10 dòng đầu và *"… và 17 dòng nữa"*. **Không** được hiện hàng chục thông báo lỗi đỏ | Pass — đúng dạng tóm tắt (giao diện). ⚠ Vòng đầu **Fail**: hiện 27 dòng lỗi đỏ; đã sửa (cắt `message_log`) rồi chạy lại mới Pass | Pass |
| TC-EDGE-02 | Đội không có nhân sự nào | Tạo đội mới, không gán ai, mở Tạo Nhanh chọn đội đó | | Bảng nhân sự hiện *"Đội này chưa có nhân sự Công nhân nào đang làm việc."* | Pass — API trả `{members: []}`, giao diện hiện đúng câu (API server) | Pass |
| TC-EDGE-03 | Chia sản lượng khi bảng đã có dữ liệu | Bảng đã có sản lượng, gọi lại nhánh chia khi Finish | | **Không** chia đè — giữ nguyên phần đã sửa tay | Pass — trước và sau đều `[Anh B, 2]`, không đè (API server) | Pass |
| TC-EDGE-04 | Chưa Completed thì chưa chia sản lượng | Làm 15/20 cái rồi mở WO | | Bảng *Sản Lượng Nhân Viên* vẫn rỗng | Pass — rỗng khi mới làm 15/20 (API server) | Pass |
| TC-EDGE-05 | Serial khi lệnh KHÔNG có mã đơn bán | Finish một WO tạo tay (không từ đơn bán) | | Serial dạng **`W26-00001-0001`** — có chữ `W` để không đụng số với đơn bán cùng năm | Pass — ra `W26-00001-0001` (API server) | Pass |
| TC-EDGE-06 | Serial đánh liên tục theo đơn | Finish lệnh thứ hai cùng đơn `SAL-ORD-2026-00003` | | STT **nối tiếp** lệnh trước, không đánh lại từ 0001 | Pass — lệnh 1 ra `26-00003-0001/0002`, lệnh 2 ra `26-00003-0003/0004` (API server) | Pass |
| TC-EDGE-07 | Mặt hàng không bật serial | Finish lệnh của item không có *Có Serial* | | Không sinh serial, phiếu vẫn submit bình thường | Pass — dòng `NVL 1` không được gán serial (API server) | Pass |
| TC-EDGE-08 | Người dùng đã tự khai serial | Nhập tay serial vào dòng thành phẩm rồi submit | | Giữ nguyên serial người dùng nhập, **không ghi đè** | Pass — gọi hook 2 lần không đổi giá trị (API server) | Pass |
| TC-EDGE-09 | Huỷ (cancel) phiếu Manufacture | Cancel phiếu đã submit | | Cancel được, tồn kho hoàn lại đúng | Pass — cancel 4 phiếu, tồn NVL 1 về đúng 99 (API server) | Pass |
| TC-EDGE-10 | Đơn bán mã không đúng dạng chuẩn | Lệnh gắn đơn có mã lạ (không kết thúc bằng `năm-số`) | | Giữ nguyên mã làm gốc, không vỡ | Pass — `ABC-XYZ` giữ nguyên (API server) | Pass |
| TC-EDGE-11 | Công Việc Khác thêm dòng mới | Thêm 1 dòng vào bảng đã cân, đổi Tổng Thời Gian | | Dòng mới được chia phần còn thiếu, lưu được | Pass — thêm dòng thứ 4, tổng 120 → 30/30/30/30 (API server) | Pass |
| TC-EDGE-12 | **Lỗi anh Thắng báo 03/08** — WO tạo từ Kế Hoạch phải có sẵn Bậc Thợ + Nguồn Lực | 1. Kế Hoạch có chọn Đội Sản Xuất<br>2. *Create* → *Work Order*<br>3. Mở WO, xem bảng Nhân Công Tham Gia **ngay, chưa bấm Lưu** | Đội 3 người: Bậc 7/100, Bậc 7/100, Bậc 6/90 | Mỗi dòng có **Bậc Thợ** và **Nguồn Lực (%)** đúng theo hồ sơ nhân sự; bấm *Tính Lại Lịch* ra kết quả, không báo thiếu Nguồn Lực | ⚠ Vòng đầu **Fail**: `employee_level = None`, `performance_factor_ = 0` → không tính được lịch. Nguyên nhân: `_validate_links()` (nơi áp `fetch_from`) chạy **trước** `before_insert`, nên dòng hook thêm vào không qua vòng fetch. Đã tự điền 2 trường trong hook; chạy lại ra `Bậc 7/100, Bậc 7/100, Bậc 6/90` (API server) | Pass |
| TC-EDGE-13 | Cùng lỗi ở nút **Thêm Đội Sản Xuất** | Mở WO nháp → **Thêm Đội Sản Xuất** → chọn đội → *Xác Nhận*, xem bảng ngay | | Mỗi dòng thêm vào có sẵn Bậc Thợ + Nguồn Lực | ⚠ Vòng đầu **Fail**: cả 3 dòng `bac=undefined, nguonluc=undefined`, chờ 4 giây vẫn không đổi (không phải bất đồng bộ). Đã điền thẳng từ dữ liệu dialog; chạy lại ra `Bậc 7/100, Bậc 7/100, Bậc 6/90` (**bấm trên giao diện**) | Pass |
| TC-EDGE-14 | **PM-TASK-00045** — huỷ lệnh thì dọn Phân Công | 1. Tạo WO, gán đội, *Tính Lại Lịch* → sinh Phân Công<br>2. Bấm **Cancel** → *Yes*<br>3. Mở danh sách Phân Công lọc theo lệnh đó | WO `MFG-WO-2026-00029`, 3 người, 3 bản ghi Phân Công | Còn **0** Phân Công; cột *Bản Ghi Phân Công* trên bảng Nhân Công Tham Gia cũng trống. Không báo *LinkExistsError* | Pass — trạng thái về *Cancelled*, danh sách hiện *"No Employee Allocation found"*, link treo 0 (**bấm trên giao diện**) | Pass |
| TC-EDGE-15 | **PM-TASK-00045** — xoá hẳn lệnh cũng dọn Phân Công | Huỷ lệnh → menu **…** → **Delete** → *Yes* | `MFG-WO-2026-00030` | Xoá được, còn **0** Phân Công. Đây là ca dễ vỡ nhất: dòng con của lệnh vẫn còn trong CSDL lúc hook chạy, không xoá link trước là dính `LinkExistsError` | Pass — xoá xong về form trống, `alloc_30 = 0` (**bấm trên giao diện**) | Pass |
| TC-EDGE-16 | **PM-TASK-00045** — **Nhân bản** lệnh không mang theo link Phân Công | Mở lệnh **đang hoạt động** có Phân Công → menu **…** → **Duplicate** → đọc `cur_frm.doc` | 3 dòng, trước khi nhân bản đều có `allocation_record` | Cả 3 dòng *Bản Ghi Phân Công* **trống**, nhưng Bậc Thợ và Nguồn Lực vẫn giữ | Pass — trước: `rl9lne7583 / rl9t365vuq / rl9h2i9j73`; sau nhân bản: cả 3 TRỐNG, Bậc 7/100, Bậc 7/100, Bậc 6/90 vẫn còn (**bấm trên giao diện**) | Pass |
| TC-EDGE-18 | 🔴 **Lỗi Thắng báo 08/08** — lệnh tạo từ Kế Hoạch không được thiếu Thời Gian Bắt Đầu | 1. Đơn bán **không** khai *Thời Gian Bắt Đầu*<br>2. Tạo Kế Hoạch Sản Xuất từ đơn, Duyệt<br>3. Từ kế hoạch tạo Lệnh sản xuất<br>4. Mở lệnh, sửa gì đó rồi bấm **Lưu** | | Lệnh phải có sẵn Thời Gian Bắt Đầu và **lưu được**. Không được báo *"Value missing for Work Order: Thời Gian Bắt Đầu"* | ⚠ Vòng đầu **Fail**: ERPNext tạo lệnh hàng loạt bằng `flags.ignore_mandatory = True` nên ghi được lệnh với ô bắt buộc bỏ trống → sau đó **mọi lần Lưu đều lỗi**, người dùng không sửa được gì, kể cả điền tay chính ô đang thiếu. 5/34 lệnh trên site đang kẹt như vậy. Đã thêm hook `ensure_start_time` ở `before_insert` + patch dọn dữ liệu cũ; chạy lại lưu được (API server) | Pass |
| TC-EDGE-19 | Hệ quả — Nhân Viên Bán Hàng không hiện trên lệnh | Như TC-EDGE-18, sau đó xem ô *Nhân Viên Bán Hàng* | Đơn có *Sales Person* = `Thắng` | Ô hiện đúng `Thắng` | ⚠ Vòng đầu **Fail**: đây chính là triệu chứng anh Thắng báo. Gốc là TC-EDGE-18 — lệnh không lưu nổi nên hook `set_sales_info` (chạy ở `validate`) không bao giờ ghi được. Thêm nữa Frappe **ẩn hẳn** trường chỉ-đọc đang rỗng nên ô biến mất khỏi form, nhìn như chưa làm tính năng. Đã chuyển `set_sales_info` sang chạy cả ở `before_insert`; chạy lại ra `Thắng` (API server) | Pass |
| TC-EDGE-20 | Tạo lệnh tay, không gắn đơn bán | Tạo Lệnh sản xuất không chọn Đơn Bán Hàng, để trống Thời Gian Bắt Đầu | | Tự lấy theo *Planned Start Date*, lưu lại được, Khách Hàng và Nhân Viên Bán Hàng để trống | Pass — lấy đúng `2026-08-14 07:30`, sửa rồi lưu lại OK (API server) | Pass |
| TC-EDGE-17 | **PM-TASK-00045** — **Sửa đổi** lệnh đã huỷ không mang theo link | Huỷ một lệnh → **Amend** → đọc `cur_frm.doc` | | Cột *Bản Ghi Phân Công* **trống** | ⚠ `no_copy` **không đủ**: `create_new.js` cố ý bỏ qua `no_copy` khi Sửa đổi (`is_no_copy = !from_amend && df.no_copy`) — đúng đường đã sinh ra dữ liệu bẩn `MFG-WO-2026-00022-1`. Đã thêm hook `before_insert` dọn link (đo API: 3 link trước insert → 0 sau). **Trên giao diện thì ca này không còn tái hiện được**: muốn Sửa đổi phải huỷ trước, mà huỷ đã dọn link rồi — nên bản Amend nhận được đã trống sẵn. Hook `before_insert` giờ là lớp phòng thủ thứ hai, không phải lớp duy nhất | Pass |

### TC-PERM — phân quyền

| Mã | Mục tiêu | Bước thực hiện | Dữ liệu vào | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|---|
| TC-PERM-01 | Tầng Role — không có quyền sửa Lệnh sản xuất | Đăng nhập user chỉ có role `Stock User` (đọc, không ghi Work Order), gọi *Tính Lại Lịch* | | Chặn: **User … does not have doctype access via role permission for document Work Order** | Pass — `PermissionError`, đúng câu (API server, chạy dưới `zz-test-readonly`) | Pass |
| TC-PERM-02 | Tầng Role — tạo lịch hàng loạt | Cùng user trên, gọi *Tạo Nhanh* | | Chặn: **User … does not have doctype access via role permission for document Employee Schedule** | Pass — `PermissionError`, đúng câu (API server) | Pass |
| TC-PERM-03 | **Tầng dữ liệu** — user bị User Permission giới hạn, không đụng bộ lọc | User có đủ role (System Manager + HR Manager + Manufacturing Manager) nhưng bị User Permission chỉ cho thấy nhân sự `Anh A`; mở dialog chọn đội | | Chỉ thấy `Anh A`; **khớp đúng** kết quả `frappe.get_list("Employee")` chạy dưới chính user đó | ⚠ Vòng đầu **Fail — RÒ RỈ**: `frappe.get_list` trả `[Anh A]` nhưng tính năng trả `[Anh A, Anh B, Anh C]`. Nguyên nhân: dùng `frappe.get_all` (không áp User Permission). Đã đổi sang `frappe.get_list`, chạy lại **Pass**, khớp `[Anh A]` (API server) | Pass |
| TC-PERM-04 | **Tầng dữ liệu** — tự gửi nhân sự NGOÀI phạm vi | Cùng user trên, gọi thẳng API tạo lịch với `Anh B` | | Chặn: **Bạn không có quyền tạo lịch cho nhân sự: Anh B** | Pass — `PermissionError`, đúng câu (API server) | Pass |
| TC-PERM-05 | **Tầng dữ liệu** — trộn có quyền + ngoài quyền | Gọi API với `["Anh A", "Anh C"]` | | Chặn (không được âm thầm bỏ `Anh C` rồi chạy tiếp): **Bạn không có quyền tạo lịch cho nhân sự: Anh C** | Pass — chặn cả lô, đúng câu (API server) | Pass |
| TC-PERM-06 | **Tầng dữ liệu** — đúng phạm vi thì vẫn chạy | Gọi API với đúng `Anh A` | | Tạo được lịch bình thường, không bị chặn nhầm | Pass — tạo 2 bản ghi, `skipped` rỗng (API server) | Pass |
| TC-PERM-07 | Không hồi quy với user không bị giới hạn | Chạy lại dưới `Administrator` | | Vẫn thấy đủ 3 nhân sự của đội | Pass — `[Anh A, Anh B, Anh C]` (API server) | Pass |
| TC-PERM-08 | Vai trò sản xuất dùng được tính năng theo Đội | Đăng nhập user chỉ có role `Manufacturing Manager`, mở dialog chọn đội và tạo lịch | | Xem được nhân sự của đội và tạo được lịch làm việc | Pass — thấy `[Anh A, Anh B, Anh C]`, tạo lịch OK (API server) | Pass |
| TC-PERM-09 | `Manufacturing User` cũng xếp được ca | Như trên với role `Manufacturing User` | | Tạo được lịch; dòng trùng thì bỏ qua đúng cơ chế | Pass — bỏ qua đúng dòng đã có (API server) | Pass |
| TC-PERM-10 | Sản xuất **không** sửa được hồ sơ Nhân sự | Kiểm quyền ghi `Employee` dưới 2 role sản xuất | | Chỉ đọc — `write` phải là **False** | Pass — cả 2 role đều `read=True, write=False` (API server) | Pass |
| TC-PERM-11 | **Không hồi quy phân hệ Nhân sự** — quyền HR còn nguyên sau khi cấp quyền cho sản xuất | Kiểm `Custom DocPerm` của `Employee` sau khi chạy patch | | Vẫn đủ `Employee`, `Employee Self Service`, `HR Manager` (r/w/c/d), `HR User` (r/w/c/d) — **không** bị thay thế | Pass — đủ 6 dòng, HR Manager và HR User vẫn full quyền; `HR Manager` vẫn ghi được Employee (API server) | Pass |

### TC-REGR — regression app lõi

| Mã | Mục tiêu | Bước thực hiện | Dữ liệu vào | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|---|
| TC-REGR-01 | `Stock Entry.before_submit` dùng chung với `mbwnext_advanced_stock` | Đặt *Max Stock Qty* = 1 trên Item Reorder của `Thành phẩm 1` / `Kho thành phẩm - HKL` (tồn đang 7), rồi Finish thêm 2 cái | | Ràng buộc của `mbwnext_advanced_stock` **vẫn chặn**: **Maximum stock level exceeded (Max Stock Qty on Item Reorder)** | Pass — chặn đúng, hook hkled không chạy vì bị dừng trước. Đã trả `Max Stock Qty` về 0 (API server) | Pass |
| TC-REGR-02 | Phiếu kho không liên quan sản xuất | Submit phiếu Material Receipt / Material Transfer thường | | Không sinh serial, không lỗi — hook hkled tự thoát vì `purpose != Manufacture` | Pass — 2 phiếu Material Transfer submit bình thường (API server) | Pass |
| TC-REGR-03 | Lệnh sản xuất không từ Kế Hoạch | Tạo WO tay, không chọn Kế Hoạch Sản Xuất | | Không bị hook GAP-5 đụng vào; lưu bình thường, bảng nhân công để trống | Pass — hook tự thoát khi không có `production_plan` (API server) | Pass |
| TC-REGR-04 | Luồng Lệnh sản xuất cũ vẫn nguyên | Mở WO cũ (`MFG-WO-2026-00001`), bấm *Tính Lại Lịch* | | Chạy như trước, không lỗi | Pass — nút hiện và WO mở bình thường (giao diện) | Pass |
| TC-REGR-05 | Đơn Bán Hàng dùng chung với 5 app lõi | Tạo + duyệt đơn bán bình thường | | 5 app kia (`advanced_selling`, `advanced_accounting`, `advanced_stock`, `localization`, `sinhthaihcm`) vẫn chạy; hkled **chỉ thêm trường**, không doc_events trên Sales Order | Pass — tạo và duyệt `SAL-ORD-2026-00002` không lỗi (API server) | Pass |
| TC-REGR-06 | Nhân sự dùng chung với `hrms` | Sửa + lưu một nhân sự | | `hrms` và các app khác vẫn chạy; chỉ thêm ràng buộc Bậc Thợ cho *Công nhân* | Pass — lưu `Anh B` bình thường, không lỗi từ `hrms`/`advanced_selling`/`econtract_service` (API server) | Pass |

### TC-ISO — cách ly app khách

| Mã | Mục tiêu | Bước thực hiện | Dữ liệu vào | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|---|
| TC-ISO-01 | Site không cài hkled không bị ảnh hưởng | Backup rồi `bench --site mbw.com migrate`, sau đó kiểm DocType + Custom Field | | Migrate sạch; site đó **không** có DocType hay Custom Field nào của hkled | Pass — migrate rc=0, 0 dòng lỗi. Sau migrate: `mbwnext_hkled` không cài, không có `Work Team`/`Other Task`, 0 Custom Field module `MBWNext HKLed`. Đã backup trước (372 MB) (API server) | Pass |
| TC-ISO-02 | Custom Field gán đúng module | Kiểm 25 Custom Field của tính năng | | Tất cả có `module = MBWNext HKLed` | Pass — 0 field thiếu module (API server) | Pass |
| TC-ISO-03 | Fixtures không lọt sang app lõi | `git status` ở `apps/mbwnext_advanced_*`, `apps/erpnext` | | Sạch, không file nào bị sửa | Pass — 4 app lõi MBWNext sạch. `erpnext` có 1 file `notification_for_new_fiscal_year.json` nhưng là **artifact có sẵn** (`modified` 2025-08-14, do ai đó tắt notification qua UI rồi migrate ghi ngược), không liên quan hkled | Pass |
| TC-ISO-04 | Chuỗi dịch nằm đúng app | Kiểm `locale/vi.po` của `mbwnext_hkled` | | Tên 4 DocType mới dịch trong app hkled, **không** đẩy sang `mbwnext_localization` | Pass — `_()` trả về Đội Sản Xuất / Công Việc Khác / Sản Lượng Nhân Viên / Bảng Công Việc Khác (API server) | Pass |

**TC-PWA:** Không áp dụng — tính năng không có màn hình mobile.

---

## Kết luận

- Tổng: **58** — Pass: **58** — Fail: **0** — Chưa chạy: **0**
- Ba lỗi phát hiện và **đã sửa** ngay trong vòng test, đều đã chạy lại Pass:
  1. **Tạo nhanh lần hai hiện 27 thông báo lỗi đỏ** thay vì một dòng tóm tắt.
     `frappe.throw` ghi vào `message_log` **trước khi** raise, nuốt exception không xoá được nên
     message vẫn theo response về trình duyệt. → cắt `message_log` về đúng độ sâu trước mỗi insert.
     *Chỉ test trên giao diện mới lộ ra.*
  2. **Ràng buộc C1 (Công nhân phải có Bậc Thợ) không chặn phía server.**
     `mandatory_depends_on` của Frappe **chỉ chạy phía client** (`form/save.js`, `layout.js` —
     không có một dòng Python nào kiểm), nên lưu bằng script/API/Data Import vẫn lọt.
     → thêm hook server `Employee.validate`.
  3. **RÒ RỈ DỮ LIỆU — nghiêm trọng nhất.** Dưới user bị User Permission giới hạn chỉ được thấy
     nhân sự `Anh A`, dialog chọn đội vẫn trả về **cả `Anh B` và `Anh C`**. Nguyên nhân:
     `frappe.get_all` **không** áp User Permission (chỉ `frappe.get_list` mới áp), và
     `frappe.has_permission(...)` không cứu được vì nó chỉ trả lời "có được xem loại dữ liệu này
     không", không trả lời "được xem những bản ghi nào".
     → đổi sang `frappe.get_list`, và thêm `_assert_employees_permitted()` soi lại danh sách nhân
     sự do client gửi lên (chặn cả ca **trộn** có quyền + ngoài quyền, không âm thầm bỏ bớt).
     Chỉ phát hiện được khi **đổi user rồi chạy lại** — chạy bằng `Administrator` thì mọi thứ đều
     trông đúng.
- **Phân quyền đã bổ sung (03/08)** để tính năng dùng được ngoài quyền quản trị:
  `Employee Schedule`, `Employee Allocation`, `Employee Level` cấp thêm cho `Manufacturing Manager`
  và `Manufacturing User` (sửa trong DocType JSON của app); `Employee` cấp thêm quyền **chỉ đọc**
  cho 2 vai trò đó qua patch `grant_production_read_on_employee`.
  ⚠ Với `Employee` **bắt buộc** dùng `frappe.permissions.add_permission()` chứ không tự `insert`
  `Custom DocPerm`: hễ một DocType có bản ghi Custom DocPerm nào thì Frappe **thay thế sạch**
  DocPerm chuẩn — tự tạo 2 dòng là xoá luôn quyền của HR Manager / HR User. Đã kiểm chứng ở
  TC-PERM-11: sau patch vẫn đủ 6 dòng, HR giữ nguyên full quyền.
- **Lỗi anh Thắng báo 03/08 — đã sửa** (TC-EDGE-12, TC-EDGE-13): WO tạo từ Kế Hoạch Sản Xuất có
  Đội, nhưng bảng Nhân Công Tham Gia **không tự điền Bậc Thợ / Nguồn Lực** → không tính được lịch.
  Nguyên nhân: trong `Document.insert()`, `self._validate_links()` — nơi Frappe áp `fetch_from`
  (qua `get_invalid_links()`) — chạy **TRƯỚC** `run_method("before_insert")`. Dòng nào hook thêm ở
  `before_insert` thì đã lỡ vòng fetch, nên 2 trường đó rỗng.
  → Tự điền `employee_level` + `performance_factor_` trong hook, không trông vào `fetch_from`.
  Kiểm thêm mới thấy **nút "Thêm Đội Sản Xuất" cũng dính cùng gốc** (dòng thêm bằng `add_child`
  không kích hoạt fetch phía client) — đã sửa nốt và test trên giao diện thật.
- Vấn đề **dữ liệu** chặn luồng sản xuất, không phải lỗi code: `Thành phẩm 1` bật cả *Có Serial*
  lẫn *Có Lô* mà chưa có lô → Manufacture báo `Batch No is mandatory` và không submit được.
  Phải tắt tạm *Có Lô* mới chạy được. Chờ HKLED dọn (nằm trong 36.890 item bật cả batch ở spec).
- **Đủ điều kiện nghiệm thu: CÓ** cho vòng test tự động. Còn chờ **vòng test tay của người test**
  để chốt Pass/Fail cuối và tick gate `testcase_passed`.

## Dọn dẹp sau khi test

Vòng test ngày 03/08 đã dọn sạch: huỷ + xoá 4 phiếu kho, 1 Lệnh sản xuất, 1 Kế hoạch,
1 Đơn bán, 20 serial, các Phân Công, đội test, lịch test và Công Việc Khác test.
Tồn `NVL 1` về đúng 99, `Thành phẩm 1` bật lại *Có Lô*, Lịch làm việc về đúng 11 bản ghi gốc.

**Người test lại nhớ làm tương tự** — đây là site dùng chung.
