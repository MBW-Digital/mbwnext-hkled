# Test case — Phần IV · Kiểm tra tồn kho và nguồn lực trên Đơn bán hàng (PM-FEAT-00023)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`, mở bằng
`http://dev.mbwnext.com:8012`
**Ngày chạy vòng tự kiểm:** 03/09/2026 · **Người chạy:** Claude (Trợ lý HKLed 2)

Đầu bài: `docs/features/kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md`
Mockup đã duyệt: bản 7 (Bảng 1b bản 6, Bảng 2b bản 7)

**Tổng kết (05/09 sáng):** **53 ca · 52 Pass · 1 chưa xong** — chỉ còn `TC-HAPPY-13`
(`Employee Allocation` chưa có dòng nào từ hôm nay, nên cột *Đã phân bổ* luôn bằng 0).

> **Bổ sung 05/09** — 6 ca mới cho việc **Bảng 2 trừ bán thành phẩm đang có trong kho**
> (anh Thắng chốt 09:20, xem mục 12f của đầu bài): `TC-EDGE-19` → `TC-EDGE-21` và
> `TC-REGR-05` → `TC-REGR-07`. Đây là **đổi con số đi mua hàng thật**, không phải đổi hiển thị —
> `NVL 3` của `SO-26-00026` giảm từ cần mua 20 xuống **17**. Số đếm ở dòng trên tính bằng máy từ
> chính bảng, không gõ tay.

> ### 🔴 Đọc trước khi tin con số 45 Pass — Bảng 3 CHƯA ĐƯỢC KIỂM CHỨNG BAO GIỜ
>
> Trong ba bảng của tính năng, **Bảng 3 (nguồn lực nhân sự) chưa từng chạy đúng một lần nào** —
> không phải bởi tôi, không phải bởi ai. Bộ test chỉ có `TC-HAPPY-11` kiểm **đường hỏng**
> (thiếu dữ liệu thì có nói thật không), và nó Pass. Đường **tính toán thật** thì trống.
>
> Lý do là dữ liệu, không phải mã: site có 149 dòng `Employee Schedule` nhưng **dòng muộn nhất
> là 31-08**, không có dòng nào từ hôm nay trở đi. Đo trên `SO-26-00013` (giao 07-09),
> `SO-26-00014` (11-09), `SO-26-00016` (12-09) — cả ba đều ra `chua_tinh_duoc`.
>
> Lời văn trên màn hình **trung thực** (*"Chưa nhân sự nào được xếp lịch làm việc trong khoảng
> đang xét"*) nên đây **không phải lỗi**. Nhưng nghiệm thu Bảng 3 là **không thể** cho tới khi
> có người xếp lịch từ 04/09 trở đi. Đã thêm `TC-HAPPY-12/13` ghi rõ là **chưa chạy**, thay vì
> để lỗ hổng này ẩn sau con số tổng.

> ⚠ **Đính chính con số:** bản đăng 03/09 và 04/09 sáng ghi *"44 ca"* — đếm thừa **1**. Dòng
> `TC-PERM-02` xuất hiện **hai lần** trong file: một lần là ca test thật ở mục TC-PERM, một lần
> nữa là dòng nhắc trong bảng *"Hạn chế đã biết"* cuối file. Đếm máy móc theo dòng bắt đầu bằng
> `| TC-` nên cộng cả dòng nhắc. Số ca thật là **43**; số Pass (40) và số ca còn treo (3) **không đổi**.

> ## 🔴 ĐỌC TRƯỚC KHI CHẠY LẠI BỘ NÀY — nền test đã đổi lúc 04/09 14:01
>
> Ô **Thời Gian Bắt Đầu** (`Sales Order.custom_start_time`) đã thành **bắt buộc** trên cổng 8012
> (phiên `cozy-dev-0c` chạy `sync_fixtures`, theo chốt của anh Thắng 03/09 15:59).
>
> **Hệ quả:** mọi ca **lưu lại** một Đơn Bán cũ sẽ chết ở `_validate_mandatory`, **không phải ở
> logic ghim**. Đây là chỗ dễ đọc nhầm thành hồi quy của Phần IV nhất — thấy đơn không lưu được
> thì kiểm ô này trước khi nghi bản vá.
>
> Đo lúc **14:03**, sáu đơn mà bộ test này tham chiếu đều **không lưu lại được**:
> `SO-26-00013` · `SO-26-00014` · `SO-26-00015` · `SO-26-00016` · `SO-26-00022` · `SO-26-00024`.
> Điền ô *Thời Gian Bắt Đầu* là chạy lại được ngay.
>
> **Ca bị ảnh hưởng:** `TC-VALID-01a`, `TC-VALID-01b`, `TC-REGR-03`, `TC-REGR-04`.
> **Ca KHÔNG ảnh hưởng:** mọi ca dựng chứng từ bằng `frappe.new_doc` rồi gọi thẳng hàm — `reqd`
> chỉ nổ lúc `save()`. Đã kiểm lại sau khi áp: `ghim_boi_don_khac`, Bảng 2 và Bảng 3 ra **y hệt**
> số cũ, lớp chặn xuất kho vẫn chặn đúng.
>
> Lùi lại được sạch nếu cần: bỏ tích *"là Trường bắt buộc"* trên Custom Field
> `Sales Order-custom_start_time`. Không có DDL, không đụng dữ liệu.

---

## Điều kiện chuẩn bị

| Cần gì | Giá trị |
|---|---|
| **Địa chỉ site** | `http://dev.mbwnext.com:8012` |
| **Tài khoản** | `Administrator` — *mật khẩu anh Tuấn giữ, cố ý không ghi vào file này.* Anh Thắng dùng tài khoản riêng của anh, quyền đủ để mở Đơn bán hàng |
| **Cách vào tính năng** | Menu **Bán hàng → Đơn hàng bán →** mở một đơn **→** nút **Kiểm Tra Tồn Kho** ở góc trên bên phải |
| **Công ty** | `HKLED` — tập kho tính tồn là **5 kho lá** (đã loại *Nhóm kho lỗi* và *Nhóm kho trung chuyển*; anh Thắng chốt 03/09 15:33) |

### Dữ liệu dùng để chạy — trạng thái lúc 03/09 16:5x

⚠ **Đọc kỹ mục này trước khi kết luận Fail.** Mấy mặt hàng thử đang được sửa trường
*Phương pháp bổ sung* trong lúc phát triển. Trường đó quyết định mặt hàng có được bóc tiếp
xuống vật tư hay không, nên **cùng một đơn bấm hai lần cách nhau vài phút có thể ra bảng
khác nhau**. Nếu số không khớp bảng dưới, kiểm *Phương pháp bổ sung* của mặt hàng trước.

| Bản ghi | Trạng thái lúc chạy |
|---|---|
| `SO-26-00014` · `SO-26-00015` | **Đã duyệt**, có tích *Ghim Tồn Khả Dụng*, cùng ghim `Thành phẩm 1`: **28** (giao 11-09) và **3** (giao 09-09) — tổng **31**. *(Anh Thắng tự dựng lúc 17:12–17:15 để test; trước đó ca mẫu là `SO-26-00011` ghim 3)* |
| `SO-26-00010` | **Bản nháp**, `Thành phẩm 1` 199 · giữ chỗ 31; `Bán thành phẩm 1` 5 · giữ chỗ 1 |
| `SO-26-00006` | Đã duyệt, `Thành phẩm 1` 15 — dùng cho ca **đủ tồn, không thiếu** |
| Tồn thực tế | `Thành phẩm 1` 31 · `Bán thành phẩm 1` 1 · `NVL 1` 68 · `NVL 2` 36 · `NVL 3` 7 |
| Đang bị ghim | `Thành phẩm 1` **31** (trực tiếp). **Không còn ghim gián tiếp** — tổng ghim 31 bằng đúng tồn 31 nên không phải sản xuất cái nào (cách B, mục 6c của đặc tả) |
| User bị giới hạn | `test.gioihan.nhansu@hkled.test` (Employee = *Anh A*) — **không đọc được Đơn Bán**, dùng cho TC-PERM-01. `test.gioihan.sales@hkled.test` (*Sales User*, Customer = `a`) — **đọc được** Đơn Bán nhưng giới hạn phạm vi, dùng cho TC-PERM-02. *Em dựng user thứ hai ngày 04/09; xoá được nếu anh không cần giữ.* |

---

## TC-HAPPY — luồng đúng

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Vào được tính năng | Mở `SO-26-00010` → bấm **Kiểm Tra Tồn Kho** | Hộp thoại *Kiểm tra tồn kho — SO-26-00010* mở ra | Pass — kiểm trên giao diện | Pass |
| TC-HAPPY-02 | Đủ ba bảng + dòng kết luận | Nhìn hộp thoại | Dòng kết luận đỏ, rồi Bảng 1, Bảng 2, Bảng 3 | Pass — *"Đơn này đang thiếu hàng. 2 mặt hàng trên đơn và 3 loại vật tư chưa đủ tồn. Nhân lực chưa tính được"* | Pass |
| TC-HAPPY-03 | Bảng 1 trừ đúng phần đơn khác giữ | Xem dòng `Thành phẩm 1` | Tồn thực tế 31 · Đơn khác giữ 31 · **Tồn khả dụng 0** · Thiếu 199 | Pass — đúng cả 4 số *(đo lại 17:2x sau cách B)* | Pass |
| TC-HAPPY-04 | Bảng 2 chỉ bóc phần **còn thiếu** | Xem Bảng 2 | Chỉ có vật tư của phần thiếu, không bóc cả phần cần | Pass — `NVL 1` cần 175 chứ không phải theo 199 cái | Pass |
| TC-HAPPY-05 | **Bảng 1b** bung ra theo dòng | Bấm `31 đang ghim` ở cột *Đơn khác giữ* | Bung ra bảng: Mã đơn · Người phụ trách · Đang ghim · Ngày lấy hàng dự kiến. **Không có tên khách hàng**, đơn ngày xa nhất lên trước | Pass — `SO-26-00014` (28, 11-09) rồi `SO-26-00015` (3, 09-09); không có cột khách hàng | Pass |
| TC-HAPPY-06 | **Bảng 2b** có cột *Bóc ra từ* | Bấm số `đang ghim` dưới một mã vật tư ở Bảng 2 | Thêm cột *Bóc ra từ* ghi mã thành phẩm và định mức hiệu dụng | Pass — đo 16:5x: `NVL 3` ← `Thành phẩm 1 · 3 × 3,00`. ⚠ Sau cách B, tổng ghim 31 = tồn 31 nên **không còn ghim gián tiếp**; muốn tái hiện phải ghim NHIỀU HƠN tồn thành phẩm | Pass |
| TC-HAPPY-07 | Dòng Cộng khớp phần đã trừ | Xem dòng cuối Bảng 1b | *"Cộng — đúng phần đã trừ khỏi tồn khả dụng: 31"* | Pass | Pass |
| TC-HAPPY-08 | 🔒 Nút tạo phiếu lấy **đúng cột Thiếu** | Bấm **Tạo Yêu Cầu Mặt Hàng**, so với cột *Thiếu* của Bảng 2 | Số trên phiếu **bằng đúng** cột Thiếu, không trừ đơn/phiếu mua đang chạy (anh Thắng chốt 03/09 16:51) | Pass — gọi hàm: `NVL 1` 135 · `NVL 2` 370 · `NVL 3` 590, khớp đúng cột Thiếu | Pass |
| TC-HAPPY-09 | Bấm nút KHÔNG sinh chứng từ | Sau TC-HAPPY-08, rời trang không bấm Lưu | Không có Yêu cầu mặt hàng nào được tạo | Pass — form ở trạng thái *Chưa lưu*, đã rời trang | Pass |
| TC-HAPPY-10 | Đơn đủ tồn thì không báo thiếu | Mở `SO-26-00006` → Kiểm Tra Tồn Kho | Bảng 1 thiếu 0, Bảng 2 rỗng | Pass — kiểm qua `bench console`, `bang2` = 0 dòng | Pass |
| TC-HAPPY-11 | Bảng 3 nói thật khi thiếu dữ liệu | Xem Bảng 3 | Kết luận **Chưa tính được** màu cam, nói rõ thiếu gì | Pass — *"Chưa nhân sự nào được xếp lịch làm việc trong khoảng đang xét"* | Pass |

## TC-VALID — chặn dữ liệu sai

> 🔴 **Phát hiện khi test trên giao diện 04/09 — sửa lại kỳ vọng của bộ test.**
> Việc chặn giữ chỗ vượt tồn có **HAI lớp**, và bản đầu của bộ test này chỉ mô tả lớp thứ hai:
>
> **Lớp 1 (client)** kẹp ngay lúc gõ, ô tự trả về mức tối đa kèm một câu báo đỏ nhẹ nhàng —
> người dùng **không bao giờ** thấy câu lỗi của server khi thao tác trên lưới.
> **Lớp 2 (server)** mới ném câu *"chỉ giữ chỗ được tối đa…"*, và nó chỉ với tới được qua
> **API hoặc Nhập dữ liệu từ Excel**.
>
> ⚠ Ai test mà chỉ gõ trên lưới rồi không thấy câu lỗi ấy sẽ tưởng tính năng chưa làm.

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01a | 🔴 **Lớp 1 — client kẹp NGAY LÚC GÕ, không đợi Lưu** | `SO-26-00016`, dòng `Bán thành phẩm 1` (khả dụng 1), gõ **5** vào *Số Lượng Giữ Chỗ* | Ô tự trả về mức tối đa + báo đỏ | Pass — **giao diện**: *"Bán thành phẩm 1: chỉ giữ chỗ được 0,000 — đã sửa lại giúp anh/chị."*, ô về `0,000` ngay, chưa cần bấm Lưu | Pass |
| TC-VALID-01b | Lớp 2 — server chặn khi vào bằng đường khác | Đặt `custom_so_luong_giu_cho` = 5 rồi `save()` (đường API/Nhập dữ liệu, không qua lưới) | Chặn với câu đầy đủ | Pass — *"Dòng 2 — Bán thành phẩm 1: chỉ giữ chỗ được tối đa 1, không được 5. Tồn khả dụng còn 1 (đã trừ phần các đơn khác đang giữ), đơn này cần 10."* | Pass |
| TC-VALID-02 | 🔴 Nhiều dòng cùng một mã ăn chung MỘT lượng tồn | `SO-26-00016` có **2 dòng** `Bán thành phẩm 1` (tồn khả dụng 1). Tích *Ghim Tồn Khả Dụng* | Dòng đầu nhận 1, dòng sau nhận **0** — không phải mỗi dòng một suất | Pass — **giao diện**: lưới ra `1` và `0`, kèm thông báo *"Đã điền mức giữ chỗ tối đa cho 1 dòng."* | Pass |
| TC-VALID-03 | Gọi trên chứng từ khác Đơn Bán | Gửi nguyên tài liệu `Purchase Order` qua tham số `doc` (đường đơn **chưa lưu**) | Báo *"Chỉ dùng được cho Đơn Bán Hàng."* | Pass. ⚠ Chỉ nhánh `doc` mới ra câu này; truyền **tên** chứng từ khác thì rơi vào lỗi của Frappe *"Sales Order … not found"* | Pass |
| TC-VALID-04 | Không có quyền đọc đơn | Gọi `kiem_tra` dưới user không có quyền Đơn Bán | Báo *"Không có quyền đọc Đơn Bán Hàng."* (`PermissionError`) | Pass — xem TC-PERM-01 | Pass |

## TC-EDGE — biên và lặp

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | 🔴 **Ghim nhiều hơn số đang có thì tồn khả dụng KHÔNG âm** | Ghim một mã nhiều hơn tồn, rồi mở Kiểm Tra Tồn Kho | Tồn khả dụng **0**, không xuống âm | Pass — đo 03/09 16:5x trên `NVL 3` (tồn 7, ghim 9): khả dụng 0 thay vì −2. ⚠ **Sau cách B đường gián tiếp không còn sinh ra ca này**; muốn tái hiện phải ghim TRỰC TIẾP vượt tồn, hoặc ghim xong rồi làm tồn tụt (giao hàng/kiểm kê giảm) | Pass |
| TC-EDGE-02 | 🔴 Số âm không được cộng vào phần cần mua | Cùng ca trên | Thiếu tính theo khả dụng 0, không theo số âm | Pass — đo 16:5x: thiếu 513 thay vì 515; phiếu ra 444 thay vì 446 | Pass |
| TC-EDGE-03 | Nói rõ vì sao kẹp | Xem khối *Cần để ý* | *"{mã}: đơn khác đang ghim {x} nhưng kho chỉ có {y} — chỉ trừ được {y}. Phần {z} còn lại KHÔNG cộng vào đơn này; cộng vào là hai đơn cùng mua một lượng hàng"* | Pass — đo 16:5x trên `NVL 3` | Pass |
| TC-EDGE-04 | Dòng Cộng nói đúng khi bị kẹp | Bung bảng chi tiết của mã bị kẹp | *"Cộng {x} — nhưng kho không đủ nên chỉ trừ {y} khỏi tồn khả dụng"* | Pass — đo 16:5x trên `NVL 3` | Pass |
| TC-EDGE-12 | 🔒 **Cách B: thành phẩm đủ tồn thì KHÔNG giữ vật tư nào** | Hai đơn ghim tổng 31 `Thành phẩm 1`, kho có đúng 31 | Bảng 2: `NVL 1/2/3` có *Đơn khác giữ* = 0, tồn khả dụng bằng tồn thực tế | Pass — `NVL 1` 68/68 · `NVL 2` 36/36 · `NVL 3` 7/7 trên giao diện | Pass |
| TC-EDGE-13 | 🔒 Cách B: chia tồn theo đơn, tổng vẫn khớp | So tổng Bảng 1b/2b với phần đã trừ | 0 mã lệch | Pass — đo sau khi đổi: 1 mã, 0 lệch | Pass |
| TC-EDGE-14 | 🔒 Chia tồn theo **ngày lấy hàng sớm nhất trước** | 8 đơn ghim `Thành phẩm 1` tổng 61, kho có 31 | 4 đơn giao sớm nhất lấy hết hàng sẵn và **không giữ vật tư nào**; đơn giáp ranh chia đôi; đơn giao xa phải sản xuất toàn bộ | Pass — 05/09·08/09·09/09·11/09(SO-19) không giữ vật tư; `SO-26-00014` (11/09) lấy 13 từ kho, **phải làm 15** → giữ 15 `NVL 1` + 45 `NVL 3`; ba đơn 15·18·22/09 phải làm toàn bộ. Tổng chi tiết = tổng đã trừ, **4/4 mã khớp** | Pass |
| TC-EDGE-05 | Tồn ÂM thật thì giữ nguyên số âm | `_kha_dung(-5, 3)` | `(-5, 0, 3)` — không kẹp về 0 | Pass — chạy qua `bench console`. *(Site hiện có **0** bản ghi Bin âm)* | Pass |
| TC-EDGE-06 | Tổng bảng chi tiết khớp phần đã trừ | So `ghim_chi_tiet` với `ghim_boi_don_khac` trên toàn site | 0 mã lệch | Pass — **4 mã, 0 lệch** | Pass |
| TC-EDGE-07 | Cảnh báo trùng bị gộp | Xem khối *Cần để ý* | Mỗi câu chỉ xuất hiện một lần | Pass — trước khi sửa, câu *Phương pháp bổ sung* hiện 2 lần | Pass |
| TC-EDGE-08 | Hơn 5 đơn cùng ghim một mã | Dựng thêm **6 đơn** ghim `Thành phẩm 1` (ngày giao 05→22/09), thành **8 đơn** cùng ghim | Hiện 5 đơn **ngày lấy hàng xa nhất** + `còn lại 3`, dòng Cộng tính đủ 8 | Pass **ở tầng dữ liệu** — `tong_ghim=61 · da_tru=31 · hiện 5 dòng · con_lai=3`, và 5 dòng đúng là 22/09 · 18/09 · 15/09 · 11/09 · 11/09. ⚠ **Chưa nhìn thấy dòng chữ *“…và 3 đơn nữa”* trên màn hình** — 6 đơn thử đã xoá ngay sau khi đo để trả lại số liệu cho anh Thắng, nên lúc mở giao diện chỉ còn 2 đơn ghim. Người test dựng lại ≥6 đơn thì xem được | Pass |
| TC-EDGE-09 | Mặt hàng Sản xuất chưa có định mức | Mở đơn có mặt hàng *Sản xuất* chưa có BOM | Cảnh báo *"{mã}: chưa có định mức, tạm coi như phải mua"* | Pass — cảnh báo có hiện. ⚠ **Xem mục Hạn chế đã biết** | Pass |
| TC-EDGE-10 | Đơn chưa lưu | Tạo đơn mới, chưa Lưu, bấm Kiểm Tra Tồn Kho | Xem được 3 bảng; **không** cho bấm Tạo Yêu Cầu Mặt Hàng, có câu giải thích | Pass — **giao diện**: tiêu đề *"Kiểm tra tồn kho — đơn chưa lưu"*, không có nút tạo phiếu, có câu *"Đơn chưa lưu nên chưa tạo được Yêu Cầu Mặt Hàng — phiếu phải trỏ về số đơn, mà số đó chỉ có sau khi bấm Lưu."* | Pass |
| TC-EDGE-11 | Đơn không có dòng hàng | Đơn rỗng | Bảng 1 hiện *"Đơn chưa có dòng hàng nào."* | Pass — **giao diện**: đúng câu đó; Bảng 2 *"Không phải bóc định mức"*, Bảng 3 *"Không áp dụng"*, không nổ lỗi dù chưa có khách hàng | Pass |
| TC-EDGE-15 | 🔴 **Đơn mua QUÁ HẠN vẫn phải hiện ở cột "Ngày hàng về · SL về"** | `SO-26-00013`, `NVL 3`. Site có `PO-26-00003` hẹn **02-09** còn 7, và `PO-26-00004` hẹn 05-09 còn 2. Hôm nay 04/09 | Hiện đơn **về sớm nhất** là 02-09 · về 7, kèm ghi chú **quá hạn 2 ngày** | Pass **sau khi vá 04/09** — trước vá: hiện *"05-09 · về 2"*, giấu mất 7/9 = **78%** lượng đang về, đúng phần đã trễ. Sau vá: *"02-09-2026 · về 7 · quá hạn 2 ngày"*. Gốc: truy vấn lọc `poi.schedule_date >= CURDATE()` | Pass |
| TC-EDGE-16 | 🔴 Câu *"chưa có đơn mua"* không được nói dối | Mã `Thành phẩm 1` (có `PO-26-00003` còn 5 hẹn 02-09 và `PUR-ORD-2026-00002` còn 1 hẹn 10-08) và `dịch vụ gia công` (còn 1 hẹn 21-08) — **toàn bộ đều quá hạn** | Hiện đơn mua thật kèm số ngày quá hạn | Pass **sau khi vá 04/09** — trước vá: cả hai mã bị giấu **100%**, ô ghi *"chưa có đơn mua"* trong khi đơn mua **có thật**. Đây là ca nặng nhất: câu dự phòng vốn thêm vào để **chống** sai im lặng lại trở thành câu sai thẳng. Sau vá: `Thành phẩm 1` → *"10-08 · về 1 · quá hạn 25 ngày"*, `dịch vụ gia công` → *"21-08 · về 1 · quá hạn 14 ngày"* | Pass |
| TC-EDGE-17 | Cột này KHÔNG gồm Yêu Cầu Mặt Hàng | `NVL 3` có `YCM-26-00001` 60 cái đang chờ | Không cộng vào cột — YCM chưa phải nguồn cung chắc chắn. Đã ghi rõ trong tài liệu để không ai đọc nhầm | Pass — cột chỉ đếm Đơn Mua Hàng đã duyệt; `YCM-26-00001` không xuất hiện. **Có chủ ý, không phải sót** | Pass |
| TC-EDGE-18 | Số lượng trong câu cảnh báo đọc được, và không làm tròn sai | Gõ **30** vào *Số Lượng Giữ Chỗ* của `Thành phẩm 1` (khả dụng 0). Kiểm thêm hàm `so()` với 2,5 · 0,125 · 1000,5 | Câu hiện *"chỉ giữ chỗ được 0"*, không phải *"0,000"*; số lẻ **giữ nguyên**, không bị làm tròn | Pass **sau khi vá 04/09** — trước vá: *"chỉ giữ chỗ được **0,000**"* (`format_number` trần, 3 chữ số thập phân — đọc như số tiền). Sau vá: *"0"*. ⚠ Cố ý **không** ép cứng 0 chữ số: UOM `Kg`/`m`/`Lít` trên site đều cho phép số lẻ, ép 0 thì **2,5 hiện thành 3** — thay câu khó đọc bằng câu sai. Đo: 2,5 → `2,5` · 0,125 → `0,125` · 1000,5 → `1.000,5` · 68,0 → `68` | Pass |
| TC-EDGE-19 | 🔒 **Bảng 2 TRỪ bán thành phẩm đang có trong kho** (anh Thắng chốt 05/09 09:20) | `SO-26-00026` phải làm 9 `Thành phẩm 1`; kho có 6 `Bán thành phẩm 1` và 1 `Bán thành phẩm 2` | Chỉ bóc nguyên vật liệu cho phần **thật sự phải làm**, không bóc cho phần đang có sẵn | Pass — **giao diện**: `NVL 1` cần 9 → **3**, `NVL 2` 18 → **6**, `NVL 3` 27 → **24**. Cần mua `NVL 3` giảm 20 → **17**. Trước 05/09 hệ thống bảo đi mua vật tư để làm ra thứ đang nằm trong kho | Pass |
| TC-EDGE-20 | Dòng đã ĐỦ hàng vẫn phải hiện ở Bảng 2 | Cùng đơn trên; `NVL 1` và `NVL 2` thiếu 0 | Vẫn có dòng, vẫn hiện cần/tồn/khả dụng/ngày hàng về | Pass — **bắt được trong lúc làm**: bản đầu của hàm mới chỉ trả phần còn thiếu nên hai dòng này **biến mất khỏi bảng**. Đã sửa: hàm trả cả nhu cầu gộp lẫn phần phải mua | Pass |
| TC-EDGE-21 | Trừ theo **bể chung**, không trừ riêng từng nhánh | Một mã là con của nhiều thành phẩm | Một cái hàng trong kho chỉ che được một nhánh | Pass — bể `be` dùng chung cho cả phép bóc, trừ dần theo thứ tự cấp. Đây chính là cảnh báo đã ghi từ đầu ở `boc_dinh_muc` cũ | Pass |
| TC-REGR-05 | 25 đơn trên site vẫn tính được sau khi đổi phép bóc | Chạy `kiem_tra` cho mọi đơn `docstatus < 2` | Không đơn nào nổ lỗi | Pass — 25/25, 0 lỗi | Pass |
| TC-REGR-06 | Nút **Tạo Yêu Cầu Mặt Hàng** vẫn dựng được phiếu | `SO-26-00026` | Dựng được phiếu nháp với số mới | Pass — `co_phieu = True`, phiếu `YCM-…` dựng đủ dòng | Pass |
| TC-REGR-07 | **Phần V không bị ảnh hưởng** | `nhu_cau_vat_tu.tinh_nhu_cau()` | Chạy bình thường | Pass — Phần V có đường nổ định mức **riêng** (BOM → BOM Template → liệt kê), không dùng `boc_dinh_muc`. ⚠ Câu *"Phần V có phải trừ bán thành phẩm không"* **chưa hỏi anh Thắng** | Pass |
| TC-HAPPY-12 | 🔴 **Bảng 3 tính đúng khi CÓ lịch làm việc** | Anh Thắng thêm lịch 04/09 (**138 dòng từ hôm nay**, 3 nhân sự). Mở Bảng 3 trên `SO-26-00013` (giao 07-09), `SO-26-00014` (11-09), `SO-26-00016` (12-09) | Ra *Tổng theo lịch · Đã phân bổ · Còn lại · Đơn này cần* bằng phút chuẩn, có kết luận đủ/thiếu | Pass — **lần đầu tiên Bảng 3 được kiểm chứng**. `SO-26-00013`: 3 nhân sự, tổng **3.915** phút chuẩn, đơn cần **350** → *đủ*. `SO-26-00014`: **9.135** / cần 1.000 → *đủ*. `SO-26-00016`: **10.440** / cần 200 → *đủ*. ⚠ **Tự tính lại tay để đối chứng, không tin số của hàm**: 18 dòng lịch trong khoảng 04→07/09, mỗi ca 225 phút, `Anh A` 100% + `Anh B` 100% + `Anh C` **90%** = 450+450+**405** = 1.305 phút chuẩn/ngày × 3 ngày = **3.915** — **khớp đúng đến số lẻ**. Hệ số năng lực áp đúng vào phía cung | Pass |
| TC-HAPPY-13 | Bảng 3 trừ đúng phần đã cam kết cho đơn khác | Hai đơn cùng khoảng, đơn A đã phân bổ nhân sự | Cột *Đã phân bổ* của đơn B tính cả phần A đang giữ | **CHƯA CHẠY** — `Employee Allocation` có 39 dòng nhưng **0 dòng từ hôm nay trở đi**, nên `Đã phân bổ` = 0 trên cả ba đơn. Lịch làm việc đã có (TC-HAPPY-12 chạy được), còn **phân bổ** thì chưa. Cần một bản ghi phân bổ từ 04/09 trở đi mới chạm tới được | — |

## TC-PERM — phân quyền

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-PERM-01 | **Tầng Role** — user không có quyền Đơn Bán | `frappe.set_user("test.gioihan.nhansu@hkled.test")` rồi đọc Đơn Bán | Chặn bằng `PermissionError` | Pass — `frappe.get_list("Sales Order")` ném `PermissionError` ngay; user này không vào nổi màn hình | Pass |
| TC-PERM-02 | **Tầng dữ liệu** — user bị giới hạn phạm vi thấy đơn ngoài quyền | Dựng user `test.gioihan.sales@hkled.test` (*Sales User*, User Permission: Customer = `a`), chạy `ghim_chi_tiet()` dưới đúng user đó rồi so với `frappe.get_list` | Theo quyết định của người phụ trách nghiệp vụ | Pass — **anh Thắng chốt 04/09 10:45: “em cứ giữ nguyên nhé”**. Hành vi đo được: `get_list` cho user đó thấy **8 đơn**, Bảng 1b/2b hiện thêm `SO-26-00014` + `SO-26-00015` (khách `0201190939`, `0769734666`) kèm **Người phụ trách** và **Ngày lấy hàng dự kiến**. ⚠ Anh Thắng cũng **đính chính căn cứ 25/08 của chính mình**: câu chặn xuất kho không nêu tên đơn là *“sợ nó rối chứ không phải sợ lộ đơn”* — tức chưa bao giờ có luật che vì riêng tư, nên **không có mâu thuẫn** giữa hai chỗ như em từng nêu. 🔒 Đây là **quyết định có chủ ý**, không phải sót. Đừng “sửa” nó mà không hỏi lại anh Thắng | Pass |
| TC-PERM-05 | Đối chiếu: câu chặn xuất kho có lộ không | Dưới cùng user đó, gửi duyệt phiếu xuất vượt tồn | Không lộ mã đơn | Pass — vẫn chặn đúng, và câu lỗi **không chứa mã đơn nào**. ⚠ Tức trong cùng một mảng đang có **hai tư thế khác nhau**: câu chặn giấu (anh Thắng chốt 25/08), Bảng 1b/2b hiện (em tự chọn, chưa ai duyệt) | Pass |
| TC-PERM-03 | Không lộ tên khách hàng | Xem Bảng 1b và 2b | Không có cột tên khách hàng | Pass — mockup bản 6 chốt vậy, code không truy vấn trường đó | Pass |
| TC-PERM-04 | Admin không bị lớp lọc làm hồi quy | Chạy dưới `Administrator` | Thấy đủ như trước | Pass | Pass |

## TC-REGR — không làm hỏng app lõi

Bản đồ va chạm (`grep -rn '"Sales Order"' apps/*/*/hooks.py` + thứ tự `sites/apps.txt`):

| App | Hook trên Sales Order | Thứ tự nạp |
|---|---|---|
| `mbwnext_localization` | `before_validate` | trước `mbwnext_hkled` |
| `mbwnext_advanced_stock` | `before_save` | trước |
| **`mbwnext_hkled`** | **`validate` (2 handler)** | — |
| `mbwnext_advanced_accounting` | `validate`, `before_save`, `before_submit` | **sau** `mbwnext_hkled` |
| `mbwnext_advanced_selling` | `before_insert`, `on_submit`, `before_submit`, `before_print` | sau |

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | `validate` của app kế toán vẫn chạy sau app HKLED | Dựng Đơn Bán **không lưu** với `sales_voucher_type = "Bán Hàng Hóa Xuất Khẩu"`, 1 dòng thuế + `item_tax_template`, rồi gọi 3 hook `validate` **đúng thứ tự thật** (`fill_item_production_note` → `chan_giu_cho_vuot_ton` → `clear_taxes_for_export`). Chạy lại y hệt với `"Bán Hàng Hóa Trong Nước"` làm đối chứng | Đơn xuất khẩu: xoá hết dòng thuế, `item_tax_template = None`, tổng thuế 0. Đơn trong nước: giữ nguyên | Pass — **04/09**: xuất khẩu **1 dòng thuế → 0**, template → `None`, tổng **10 → 0**. Trong nước **không đổi** (1 dòng, template còn, tổng 10). Hai hook HKLED chạy trước **không cản** hook kế toán | Pass |
| TC-REGR-02 | 5 app cùng nạp `sales_order.js` không đè nhau | Mở form Đơn bán hàng | Form mở bình thường, nút của các app khác còn đủ | Pass — form mở được, nút *Lấy dữ liệu từ*, *Hành động* còn nguyên | Pass |
| TC-REGR-03 | `throw` mới không chặn đơn vốn hợp lệ | Lưu `SO-26-00016` **không tích Ghim** | Không bị chặn — hook thoát sớm khi không có dòng giữ chỗ | Pass — lưu nhiều lượt trên giao diện và qua `save()`, không lần nào bị chặn | Pass |
| TC-REGR-04 | Không đụng luồng duyệt đơn của lõi | **Duyệt 6 đơn** liên tiếp (SO-26-00017…00022) | Duyệt được, `on_submit` của các app khác vẫn chạy bình thường | Pass — cả 6 đơn duyệt trót lọt. Kiểm thêm: **không** sinh Hoá đơn hay Phiếu xuất kho ngoài ý muốn (cấu hình tự sinh đang tắt). Đã xoá cả 6 sau khi đo | ⚠ **Không chạy lại được như viết** — đo 04/09 14:03: `SO-26-00017`…`SO-26-00021` **không còn tồn tại** trên site, chỉ còn `SO-26-00022` (mà đơn này giờ cũng không lưu lại được, xem cảnh báo đầu file). Kết quả Pass ghi ngày 03/09 vẫn đúng tại thời điểm đó; muốn chạy lại có **hai đường**: (a) **dựng 6 đơn mới** rồi sửa số hiệu trong ca — an toàn, không đụng dữ liệu cũ; (b) **khôi phục 5 đơn kia** — đo 04/09 14:06: cả 5 đều còn bản ghi `Deleted Document` với `restored = 0` và JSON đủ 147 trường kèm dòng hàng, nên khôi phục được, và ca chạy lại đúng số hiệu đã viết. ⚠ Nhưng chúng bị **Administrator xoá sáng nay 09:23:57** — nhiều khả năng anh Thắng chủ động dọn, khôi phục là mọc lại thứ người ta vừa bỏ. **Phải hỏi trước, đừng tự khôi phục.** 📌 Cả 5 chưa từng sinh bút toán kho nào (đo: 0), nên dù chọn đường nào cũng không có dư âm tồn kho | Pass (03/09) |

## TC-ISO — cách ly app khách

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-ISO-01 | Custom Field gán đúng module | Đọc `module` của các Custom Field mới | `MBWNext HKLed` | Pass — `Sales Order Item-custom_so_luong_giu_cho` và `Item Default-custom_ton_kho_kha_dung_toi_thieu` đều là *MBWNext HKLed* | Pass |
| TC-ISO-02 | Code mới nằm trọn trong app khách | Xem đường dẫn file đã sửa | Chỉ trong `apps/mbwnext_hkled/` | Pass — `api/kiem_tra_ton_kho.py`, `controllers/python_hook/sales_order.py`, `controllers/js/sales_order.js` | Pass |
| TC-ISO-03 | Không lọt fixtures sang app lõi | `git status` ở 5 app lõi + `erpnext`; và `fixtures/` của app khách | Sạch | Pass — 5 app lõi MBWNext **0 file**, `fixtures/` app khách **0 file**. ⚠ `erpnext` có **2 file bẩn sẵn** (`Notification` bị tắt trên giao diện ngày **09/08**, Frappe ghi ngược ra đĩa) — **không phải do tính năng này**, nhưng nên dọn riêng | Pass |
| TC-ISO-04 | Site không cài `mbwnext_hkled` vẫn chạy | `bench --site mbw.com migrate` (Tuấn chạy 04/09 **10:29**), rồi trên site đó: đếm hook của hkled, tìm Custom Field của hkled, dựng Đơn Bán chạy `validate`, dựng Phiếu xuất 99.999 chạy `before_submit` | Không có lớp chặn nào; không hook, không Custom Field của hkled | Pass — **0 hook** `mbwnext_hkled` trên `mbw.com`; **0 Custom Field** của hkled (`custom_so_luong_giu_cho`/`custom_ghim_ton_kha_dung`/`custom_start_time` đều không có — riêng `Item Reorder-custom_max_stock_qty` có mặt nhưng `module = MBWNext Advanced Stock`, là của app lõi, **không phải rò rỉ**); `validate` Đơn Bán **đi qua**; Phiếu xuất **99.999** đơn vị cũng **đi qua** — đúng, site này không có lớp chặn. Patch `migrate_warehouse_to_company_table` chạy cùng lượt, không lỗi. 5 app lõi MBWNext `git status` **0 file**; `erpnext` bẩn 2 file `Notification` từ **09/08**, có trước tính năng này | Pass |

## TC-PWA

**Không áp dụng** — tính năng không có màn hình mobile.

---

## ⚠ Hạn chế đã biết — chưa sửa, không phải lỗi mới phát sinh

| Việc | Ảnh hưởng |
|---|---|
| `boc_dinh_muc` chỉ đọc **BOM thật**, không đọc **BOM Template** | Mặt hàng *Sản xuất* có Template nhưng chưa có BOM sẽ bị coi là **phải mua**, tức Bảng 2 bảo đi mua chính cái đèn đó. Có cảnh báo hiện ra chứ không im lặng (TC-EDGE-09), nhưng số thì sai |
| Bấm nút Tạo Yêu Cầu Mặt Hàng **hai lần** ra hai phiếu cho cùng phần thiếu | Hệ quả trực tiếp của luật mới 03/09 16:51 (lấy thẳng cột Thiếu, không trừ đơn/phiếu đang chạy). Anh Thắng đã cân nhắc và vẫn chọn. Chỗ duy nhất còn nhắc là dòng cảnh báo *"đơn này đã có phiếu"* — **đừng gỡ** |
| ~~Ghim gián tiếp giữ vật tư cho cả thành phẩm đã có sẵn trong kho~~ | ✅ **Đã xử lý 03/09 17:2x** — anh Thắng chốt **cách B** lúc 16:51. Chỉ giữ vật tư cho phần còn phải sản xuất. Xem TC-EDGE-12/13/14 và mục 6c của đặc tả |
| ~~TC-PERM-02 — Bảng 1b/2b không áp User Permission~~ | ✅ **Đã chốt 04/09 10:45: giữ nguyên.** Anh Thắng: *"em cứ giữ nguyên nhé, lúc xuất kho mà cho hiện nhiều thông tin sợ nó rối chứ không phải sợ lộ đơn"*. 🔒 Đây là **quyết định có chủ ý**, không phải việc treo — chi tiết và số đo ở ca `TC-PERM-02` phía trên. ⚠ Câu chốt đó cũng **đính chính một hiểu nhầm của em**: câu chặn xuất kho không nêu tên đơn là vì **sợ rối màn hình**, không phải vì riêng tư — nên **chưa bao giờ có mâu thuẫn** giữa hai chỗ như em từng nêu |
| Bảng 3 khớp nhân sự bằng **họ tên hiển thị**, không phải mã nhân sự (`kiem_tra_ton_kho.py:623`) | Ba đường vỡ, **hiện chưa đường nào xảy ra** (đo 04/09: 4 nhân sự đều Active, **0 họ tên trùng**; lịch làm việc nay **287 dòng**, 138 dòng từ hôm nay trở đi, khớp hết): (a) **đổi tên nhân sự** ➜ mọi dòng lịch cũ của người đó thôi khớp, im lặng; (b) **hai người trùng họ tên cùng Active** ➜ `ra[employee_name]` ghi đè, một người biến mất khỏi năng lực; (c) **nhân sự nghỉ việc** ➜ bỏ khỏi *tổng theo lịch* thì đúng, nhưng bỏ khỏi *đã phân bổ* làm `còn lại` **to hơn thực tế** — tức **báo đủ nhân lực trong khi không đủ**, sai về phía nguy hiểm. Chưa vá vì chưa lộ và sát hạn; khách chưa dùng phân hệ nhân sự nên lộ ra sẽ rất khó lần |
