# Test case — Phần IV.1 · Chặn xuất kho quá tồn khả dụng (PM-FEAT-00034)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`, mở bằng
`http://dev.mbwnext.com:8012`
**Ngày chạy vòng tự kiểm:** 03/09/2026 · **Người chạy:** Claude (Trợ lý HKLed 2)

Đầu bài: `docs/features/chan-xuat-kho-qua-ton-kha-dung.md` · Mockup bản 2 (anh Thắng duyệt 03/09)
Code: `controllers/python_hook/chan_xuat_kho.py`, cắm vào `before_submit` của **8 chứng từ**.

> ### ⚠ Cách Claude tự chạy vòng một — đọc trước khi tin cột KQ thực tế
>
> Submit một Phiếu xuất kho thật là **đổi tồn kho thật** trên site anh Thắng đang test, nên em
> **không** làm. Thay vào đó em dựng chứng từ **trong bộ nhớ, không lưu**, rồi gọi thẳng hàm
> `chan_xuat_qua_ton_kha_dung(doc)` — đúng hàm mà `before_submit` gọi.
>
> Cách này kiểm được **toàn bộ phần quyết định chặn hay không chặn**, và đó là phần dễ sai nhất.
>
> **✅ Bổ sung 04/09 — vòng hai đã chạy THẬT trên giao diện.** Tuấn yêu cầu test qua giao diện,
> nên hai ca quan trọng nhất (`TC-HAPPY-10` chặn đúng · `TC-REGR-01` không chặn oan) nay đã được
> bấm **Gửi** thật trên hai Phiếu xuất kho hàng bán, và đã dọn lại: phiếu duyệt được thì **huỷ**
> để tồn về nguyên (68 → 63 → 68), phiếu bị chặn thì **xoá** bản nháp.
>
> ⚠ **Bẫy gặp khi bấm tay, người test sẽ gặp lại:** ô *Giờ hạch toán* tự cập nhật mỗi lần mở
> phiếu, nên form luôn ở trạng thái *Chưa lưu* và nút chính là **Lưu** chứ không phải **Gửi**.
> Phải bấm Lưu (hoặc `Ctrl+S`) một lượt rồi mới bấm Gửi được. Đây là hành vi của ERPNext lõi,
> không phải lỗi tính năng — nhưng không biết trước thì tưởng nút Gửi hỏng.
>
> **✅ Bổ sung 04/09 (chiều) — phiên `cozy-dev-0c` đóng thêm hai ca.** `TC-REGR-02` (luật tồn kho
> tối đa của app lõi) và `TC-PERM-01` (chặn không phụ thuộc vai trò) chạy bằng đúng kỹ thuật dựng
> chứng từ không lưu ở trên — **0 bút toán kho**, tồn không đổi. Bảng hiện là **41 ca · 41 Pass · 0 chưa chạy** — bộ test này đã **chạy hết**.
> `TC-EDGE-05` (huỷ rồi sửa) và `TC-ISO-03` (`bench --site mbw.com migrate`) đóng nốt chiều 04/09 sau khi Tuấn cấp phép.
> Đọc kèm ô cảnh báo dưới bảng TC-REGR về `custom_max_stock_qty = 0`.

---

## Điều kiện chuẩn bị

| Cần gì | Giá trị |
|---|---|
| **Địa chỉ site** | `http://dev.mbwnext.com:8012` |
| **Tài khoản** | tài khoản của anh Thắng trên cổng 8012 (mật khẩu không ghi vào file) |
| **Cách vào tính năng** | Không có màn hình riêng. Tính năng chạy lúc **Gửi duyệt** một trong 8 chứng từ kho |
| **Công ty** | `HKLED` |

**5 kho hợp lệ** (đã loại *Nhóm kho lỗi* và *Nhóm kho trung chuyển*, đo 03/09):
`Kho bán thành phẩm - HKL` · `Kho nguyên vật liệu - HKL` · `Kho thành phẩm - HKL` ·
`Kho khuyến mãi/hàng mẫu - HKL` · `Kho ký gửi - HKL`.
Hai kho cuối **có** trong pool — anh Thắng chốt 25/08.

**Dữ liệu dùng để chạy (03/09 ~17:1x):** `SO-26-00011` đã duyệt, có tích *Ghim Tồn Khả Dụng*,
giữ chỗ 3 `Thành phẩm 1`. Ghim lan xuống định mức nên **`NVL 3` đang bị giữ 9 trong khi kho chỉ
có 7** → tồn khả dụng **0**. Mọi ca dưới đây dùng `NVL 3`, xuất 5.

⚠ *Phương pháp bổ sung* của mấy mặt hàng thử đang được sửa trong lúc phát triển; đổi trường đó là
đổi đường bóc định mức, nên con số ghim có thể khác lúc anh chạy. Kiểm lại bằng nút **Kiểm Tra
Tồn Kho** trên `SO-26-00010` trước khi kết luận Fail.

---

## TC-HAPPY — chặn đúng chỗ cần chặn

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Phiếu xuất kho vượt tồn khả dụng bị chặn | Phiếu xuất kho hàng bán, `NVL 3` 5 cái, kho nguyên vật liệu → Gửi duyệt | Chặn, tiêu đề **Xuất quá tồn khả dụng**, nội dung: *"Không xuất được: tồn khả dụng không đủ."* · *"• NVL 3: xuất 5, tồn khả dụng còn 0"* · *"Phần chênh đang được các Đơn Bán khác giữ chỗ."* | Pass — chặn, câu lỗi khớp nguyên văn *(gọi hàm trên chứng từ chưa lưu)* | Pass |
| TC-HAPPY-02 | Câu chặn **không nêu tên đơn** đang giữ | Đọc câu lỗi ở TC-HAPPY-01 và TC-HAPPY-10 | Không xuất hiện mã đơn nào | Pass — kiểm cả hai đường: gọi hàm, và **hộp lỗi thật trên giao diện**. Chỉ có mã hàng và hai con số, không mã đơn, không tên khách | Pass |
| TC-HAPPY-03 | Dùng thống nhất chữ *Tồn khả dụng* | Đọc câu lỗi | Không dùng chữ khác như "tồn rảnh", "có thể xuất" | Pass | Pass |
| TC-HAPPY-04 | Hoá đơn bán có cập nhật kho cũng bị chặn | Hoá đơn bán hàng, tích *Cập nhật tồn kho*, `NVL 3` 5 | Chặn | Pass | Pass |
| TC-HAPPY-05 | Chứng từ kho nội bộ xuất một chiều bị chặn | Chứng từ kho nội bộ, kho nguồn hợp lệ, **không** có kho đích | Chặn | Pass | Pass |
| TC-HAPPY-06 | Trả hàng mua bị chặn | Phiếu Nhập Kho Hàng Mua bản **trả hàng** | Chặn — trả hàng là hàng đi ra | Pass | Pass |
| TC-HAPPY-07 | Kiểm kê điều chỉnh giảm bị chặn | Đối soát tồn kho, `NVL 3` từ 7 xuống 2 | Chặn | Pass | Pass |
| TC-HAPPY-08 | Nhận hàng gia công bị chặn | Subcontracting Receipt, kho nhà cung cấp là kho hợp lệ, tiêu hao `NVL 3` 5 | Chặn | Pass | Pass |
| TC-HAPPY-09 | Hạch toán tài sản bị chặn | Asset Capitalization, tiêu hao `NVL 3` 5 | Chặn | Pass | Pass |
| TC-HAPPY-10 | 🔴 Câu lỗi hiện đúng trên giao diện | `PXK-26-00003`: xuất 5 `Thành phẩm 1` (khả dụng 0) → bấm **Gửi** | Hộp lỗi đỏ, đọc hiểu được, chứng từ **không** được duyệt | Pass — **giao diện 04/09**: hộp đỏ tiêu đề **“Xuất quá tồn khả dụng”**, nội dung *“Không xuất được: tồn khả dụng không đủ.”* · *“• Thành phẩm 1: xuất 5, tồn khả dụng còn 0”* · *“Phần chênh đang được các Đơn Bán khác giữ chỗ.”* Chứng từ giữ nguyên **Bản nháp** | Pass |

## TC-VALID — chặn nhầm thì tệ hơn chặn sót

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | 🔴 **Chuyển kho nội bộ KHÔNG bị chặn** | Chứng từ kho nội bộ, `NVL 3` 5 cái, `Kho nguyên vật liệu` → `Kho bán thành phẩm` (cả hai đều hợp lệ) | **Đi qua** — tổng tồn khả dụng không đổi | Pass — không chặn | Pass |
| TC-VALID-02 | 🔴 **Đơn đang ghim được miễn trừ** | Phiếu xuất kho có `against_sales_order = SO-26-00011` | **Đi qua** — đơn không tự chặn phiếu xuất của chính mình | Pass — không chặn | Pass |
| TC-VALID-03 | Miễn trừ **chỉ** cho đúng đơn đó | Phiếu xuất kho có `against_sales_order = SO-26-00006` (đơn khác) | **Chặn** — không được miễn lây | Pass — chặn | Pass |
| TC-VALID-04 | Hoá đơn không cập nhật kho thì bỏ qua | Hoá đơn bán hàng, **bỏ tích** *Cập nhật tồn kho* | Đi qua — hàng đi bằng phiếu xuất kho, không đụng kho ở đây | Pass | Pass |
| TC-VALID-05 | Nhập mua bình thường không bị chặn | Phiếu Nhập Kho Hàng Mua, `is_return = 0` | Đi qua — đây là hàng đi vào | Pass | Pass |
| TC-VALID-06 | Kiểm kê điều chỉnh **tăng** không bị chặn | Đối soát tồn kho, `NVL 3` từ 7 lên 9 | Đi qua | Pass | Pass |
| TC-VALID-07 | Gia công ở kho ngoài pool không bị chặn | Subcontracting Receipt, kho nhà cung cấp = `Kho lỗi - HKL` | Đi qua — tồn ở kho đó vốn không nằm trong tồn khả dụng | Pass | Pass |
| TC-VALID-08 | Yêu cầu mặt hàng **chỉ cảnh báo** | Yêu cầu mặt hàng loại *Material Issue*, `NVL 3` 5 | **Không chặn**, hiện cảnh báo cam *"1 mặt hàng đang xin nhiều hơn tồn khả dụng: NVL 3. Vẫn lập được phiếu, nhưng lúc xuất kho thật sẽ bị chặn nếu tồn chưa về kịp."* | Pass — không chặn, cảnh báo đúng câu | Pass |
| TC-VALID-09 | Yêu cầu mặt hàng loại khác thì im | Yêu cầu mặt hàng loại *Purchase* | Không cảnh báo gì | Pass | Pass |

## TC-EDGE — biên và lặp

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | Chứng từ khai trong hooks mà thiếu bộ đọc | Gọi hàm chặn với một `Quotation` | Báo *"Chưa có bộ đọc tồn cho chứng từ Quotation — báo đội kỹ thuật, đừng bỏ qua."* | Pass — chặn, đúng câu. Đây là lưới an toàn: thà chặn nhầm còn hơn để lọt | Pass |
| TC-EDGE-02 | Công ty không có kho hợp lệ nào | Phiếu xuất kho của một công ty không có kho nào | Đi qua, không nổ lỗi | Pass — `_kho_hop_le` trả `[]`, hàm chặn thoát sớm, không ném lỗi | Pass |
| TC-EDGE-03 | Chứng từ không rút gì khỏi kho hợp lệ | Phiếu xuất kho chỉ có dòng ở kho ngoài pool | Đi qua | Pass — cùng đường thoát với TC-VALID-07 | Pass |
| TC-EDGE-04 | Ghim vượt tồn thì báo "còn 0", không báo số âm | Đọc câu lỗi TC-HAPPY-01 (`NVL 3` tồn 7, ghim 9) | *"tồn khả dụng còn 0"* | Pass | Pass |
| TC-EDGE-05 | 🔴 **Huỷ rồi sửa lại chứng từ** | `PXK-26-00002` (`NVL 1` × 5, tồn 68): Lưu → **Gửi** → **Huỷ** → **Sửa đổi** → đổi lên **100** → Gửi → đổi về **5** → Gửi → Huỷ. Toàn bộ bấm tay trên giao diện cổng 8012 | Luật chặn chạy lại trên bản sửa đổi; tồn **không bị trừ hai lần** | Pass — **giao diện 04/09, Tuấn cho phép ghi dữ liệu thật**. Duyệt: 68 → **63**. Huỷ: → **68**. Sửa đổi ra `PXK-26-00002-1` (*Sửa đổi từ PXK-26-00002*). Gửi với 100 → **CHẶN**: *“Xuất quá tồn khả dụng — NVL 1: xuất 100, tồn khả dụng còn 68”* ⟵ luật chạy lại đúng trên bản sửa đổi, **và số hiện đúng nguyên** (không còn `,000`, xác nhận bản vá `_so()` ăn trên giao diện). Hạ về 5 → duyệt được, 68 → **63**. **Không nhân đôi**: 3 bút toán `NVL 1`, hai dòng của `PXK-26-00002` đều `is_cancelled=1`, tổng ảnh hưởng đúng **−5**. Huỷ nốt → tồn **68**. ⚠ **Vết để lại vĩnh viễn**: `PXK-26-00002` và `PXK-26-00002-1`, cả hai `docstatus=2` (đã huỷ) — do test sinh ra, không phải chứng từ nghiệp vụ | Pass |
| TC-EDGE-06 | 🔴 Nhiều dòng cùng một mã trên một chứng từ | `NVL 1` khả dụng 68. **Ca A**: 3 dòng × 30 = 90. **Ca B (đối chứng)**: 3 dòng × 20 = 60 | Cộng dồn theo mã rồi mới so: ca A chặn, ca B đi qua | Pass — ca A: *"NVL 1: xuất **90**, tồn khả dụng còn 68"* (báo theo tổng, không theo dòng lẻ); ca B đi qua. Nếu xét từng dòng riêng thì ca A đã lọt vì 30 < 68 | Pass |
| TC-EDGE-15 | 🔴 **Đơn ghim KHÔNG được tự chặn phiếu xuất vật tư đi sản xuất của mình** | Chứng từ kho nội bộ `Material Transfer for Manufacture`, đầu phiếu gắn **Lệnh sản xuất** của chính đơn đã ghim, xuất `Bán thành phẩm 1` (khả dụng 0 vì chính đơn đó ghim) | Đi qua — miễn trừ phải nối được `Stock Entry.work_order` ➜ `Work Order.sales_order` | Pass **sau khi vá 04/09** — trước vá: **CHẶN** (`_don_duoc_mien` trả tập rỗng cho *mọi* Chứng từ kho nội bộ vì bảng con không có cột nào trỏ về Đơn Bán). Sau vá: **LỌT**. Đối chứng cùng lượt: cùng phiếu đó gắn Lệnh sản xuất của **đơn khác** → vẫn **CHẶN**, không gắn gì → vẫn **CHẶN** | Pass |
| TC-EDGE-16 | Yêu Cầu Mặt Hàng của chính đơn đã ghim không bị cảnh báo oan | Yêu Cầu Mặt Hàng loại *Material Issue*, dòng có `sales_order` = đơn đã ghim, xin đúng phần mình đã giữ | Không nói gì — phần đó là của chính đơn này | Pass **sau khi vá 04/09** — trước vá: **1 cảnh báo** (`canh_bao_yeu_cau_mat_hang` gọi `ghim_boi_don_khac()` **không truyền `tru_don`**, dù `Material Request Item` có sẵn cột `sales_order`). Sau vá: **0 cảnh báo** | Pass |
| TC-EDGE-17 | Số lượng trong câu chặn đọc được | Dựng phiếu xuất 5 `Bán thành phẩm 1` khi khả dụng 0, đọc nguyên văn câu chặn | *"xuất 5, tồn khả dụng còn 0"* — không có đuôi `,000` | Pass **sau khi vá 04/09** — trước vá 4 chỗ dùng `frappe.format_value(..., Float)` cho ra 3 chữ số thập phân. Nay cả 6 chỗ (2 ở đây + 4 ở hook Đơn Bán) dùng chung hàm `_so()` của `kiem_tra_ton_kho.py`, khớp đúng hàm `so()` bên JS | Pass |
| TC-EDGE-18 | 🔴 **Miễn trừ đi được HAI chặng: Lệnh sản xuất ➜ Kế hoạch sản xuất ➜ Đơn Bán** | `MFG-WO-2026-00020` và `00021` (ô *Đơn Bán* **trống**, nhưng kế hoạch `MFG-PP-2026-00006` có `SAL-ORD-2026-00007-1`); `MFG-WO-2026-00018` qua `MFG-PP-2026-00005`. Dựng Chứng từ kho nội bộ gắn từng lệnh, gọi `_don_duoc_mien` | Tra ra đúng Đơn Bán qua kế hoạch | Pass **sau khi vá 04/09 16:39** — trước vá cả ba trả **tập rỗng**, tức bị chặn oan khi lấy chính vật tư đơn của mình đã ghim. Sau vá: `00020`/`00021` → `{SAL-ORD-2026-00007-1}`, `00018` → `{SAL-ORD-2026-00006}`. Anh Thắng mô tả quy trình 04/09 16:35: hàng làm cho đơn thì tạo **Kế hoạch sản xuất từ Đơn Bán** rồi mới tạo Lệnh sản xuất — nên chặng này là đường chính, không phải ngoại lệ | Pass |
| TC-EDGE-19 | Sản xuất để tồn kho **KHÔNG** được miễn trừ | `MFG-WO-2026-00006`, `00001`, `00002` — không có cả `sales_order` lẫn `production_plan` | Trả tập rỗng; chứng từ vẫn bị kiểm như mọi chứng từ khác | Pass — cả ba trả **tập rỗng**. Đúng thiết kế: lệnh để tồn kho không phục vụ đơn nào nên **không được phép** lấy hàng đơn khác đang giữ. Đo 04/09: **17/33** lệnh thuộc loại này | Pass |

## TC-PERM — phân quyền

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-PERM-01 | Lớp chặn không bị bỏ qua theo vai trò | Dưới `test.gioihan.sales@hkled.test` (`Sales User` + `Desk User`, **không** System Manager): xuất 531 `Thành phẩm 1` khi tồn khả dụng 0. Lặp lại y hệt dưới `Administrator` | Vẫn bị chặn — đây là luật nghiệp vụ, không phải quyền | Pass — **04/09, phiên `cozy-dev-0c` chạy**: cả hai vai trò đều bị chặn như nhau, cùng câu *“Không xuất được: tồn khả dụng không đủ… Phần chênh đang được các Đơn Bán khác giữ chỗ.”* Câu lỗi **không nêu mã đơn nào** (khớp TC-PERM-02) | Pass |
| TC-PERM-02 | Câu lỗi không lộ dữ liệu đơn khác | Đọc câu lỗi | Không có mã đơn, không có tên khách hàng, không có tên người phụ trách | Pass — xem TC-HAPPY-02 | Pass |
| TC-PERM-03 | Người bị giới hạn phạm vi vẫn bị chặn đúng | Dưới `test.gioihan.sales@hkled.test` (Customer = `a`), gọi hàm chặn trên phiếu xuất 5 `Thành phẩm 1` | Vẫn chặn — phần ghim tính trên **toàn bộ** đơn, không theo phạm vi người xem | Pass — vẫn chặn, và **câu lỗi không chứa mã đơn nào** (đã kiểm bằng máy, không đọc bằng mắt) | Pass |

## TC-REGR — regression app lõi

Bản đồ va chạm ở `before_submit` (thứ tự nạp theo `sites/apps.txt`):

| Chứng từ | App khác cùng `before_submit` | Chạy trước hay sau `mbwnext_hkled` |
|---|---|---|
| Chứng từ kho nội bộ · Phiếu Nhập Kho Hàng Mua · Đối soát tồn kho | `mbwnext_advanced_stock.utils.stock_validation` | **trước** |
| Phiếu xuất kho hàng bán · Hoá đơn bán hàng | `mbwnext_advanced_selling` | **sau** |
| Hoá đơn bán hàng | `mbwnext_advanced_accounting` (validate/on_submit) | sau |

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | 🔴 **Chứng từ vốn hợp lệ vẫn duyệt được** | `PXK-26-00002`: xuất 5 `NVL 1` (không đơn nào ghim) → bấm **Gửi** | Đi qua như trước khi có tính năng | Pass — **giao diện 04/09**: *“Delivery Note has been submitted successfully”*, chứng từ sang **ĐÃ DUYỆT**. Tồn `NVL 1` 68 → 63, huỷ phiếu xong về lại **68** | Pass |
| TC-REGR-02 | Kiểm tra tồn của `mbwnext_advanced_stock` vẫn chạy | Đặt tạm `custom_max_stock_qty = 35` cho `Thành phẩm 1` / `Kho thành phẩm`. Nhập **10** (27+10 = 37 > 35) rồi nhập **2** (29 ≤ 35). Trả lại 0 sau khi chạy | Ca 10 báo lỗi tồn kho tối đa của app lõi; ca 2 đi qua; hook HKLED không chặn nhầm phiếu **nhập** | Pass — **04/09, phiên `cozy-dev-0c` chạy**: ca 10 nổ đúng *“Maximum stock level exceeded”*, ca 2 đi qua, phiếu nhập không bị hook HKLED đụng vào. Đã trả `custom_max_stock_qty` về 0, tồn không đổi, **0 bút toán kho**. ⚠ Xem chú ý bên dưới bảng | Pass |
| TC-REGR-03 | Hook nạp đủ trên cả 8 chứng từ | `frappe.get_hooks("doc_events")` | 8 chứng từ có `chan_xuat_qua_ton_kha_dung` | Pass — đếm được đúng 8 | Pass |
| TC-REGR-04 | Không viết công thức tồn khả dụng thứ hai | Đọc code | Dùng chung `_kha_dung` với Phần IV | Pass — 03/09 gom **6 bản chép** trong tính năng về một hàm; bản thứ 7 ở Phần V do phiên kia sửa (`6550816`) | Pass |

> ⚠ **`TC-REGR-02` Pass không có nghĩa là luật tồn kho tối đa đang bảo vệ site.**
> Trên `hkled.com` chỉ có **một** bản ghi Item Reorder (`Thành phẩm 1` / `Kho thành phẩm - HKL`)
> và nó để `custom_max_stock_qty = 0`. Mã lõi lọc `if mq > 0` (`mbwnext_advanced_stock/utils/stock_validation.py:158`),
> nên **luật này hiện không bao giờ nổ trên site**. Ca test chỉ chạy được vì đã tạm đặt một giá trị
> rồi trả lại. Ai đọc “Pass” mà bỏ qua dòng này sẽ tưởng có một lớp bảo vệ đang hoạt động — không có.
>
> Điều `TC-REGR-02` thật sự chứng minh: **thứ tự nạp**. Luật tồn kho tối đa của app lõi có mặt ở
> đúng ba chứng từ mà nó áp dụng (Chứng từ kho nội bộ · Đối soát tồn kho · Phiếu Nhập Kho Hàng Mua)
> và ở cả ba, nó đăng ký **trước** `chan_xuat_qua_ton_kha_dung`. Hook của HKLED **không thể che** nó.
> Đây là bảo đảm về cấu trúc, chắc hơn một ca test đơn lẻ. (Phiếu xuất kho hàng bán không có luật
> tồn kho tối đa — đúng, vì luật đó chỉ xét hàng **nhập vào** kho.)

## TC-ISO — cách ly app khách

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-ISO-01 | Code nằm trọn trong app khách | Xem đường dẫn | Chỉ `apps/mbwnext_hkled/` | Pass — `controllers/python_hook/chan_xuat_kho.py` + khai trong `hooks.py` của chính app | Pass |
| TC-ISO-02 | Không tạo Custom Field mới | Đọc code | Tính năng chỉ đọc, không thêm trường | Pass — dùng lại `custom_so_luong_giu_cho` và `custom_ghim_ton_kha_dung` của Phần IV | Pass |
| TC-ISO-03 | Site không cài `mbwnext_hkled` không bị chặn | `bench --site mbw.com migrate` (Tuấn chạy 04/09 **10:29**), rồi dựng Phiếu xuất kho **99.999** đơn vị và gọi `before_submit` | Không có lớp chặn nào | Pass — chứng từ **đi qua**, không câu chặn nào nổ; **0 hook** `mbwnext_hkled` đăng ký trên site đó. Nếu hook có rò rỉ sang thì 99.999 đơn vị chắc chắn phải bị chặn — chọn số lớn để ca này không thể Pass nhầm | Pass |
| TC-ISO-04 | Không lọt fixtures sang app lõi | `git status` ở 5 app lõi + `erpnext` | Sạch | Pass — 5 app lõi MBWNext **0 file**. ⚠ `erpnext` bẩn sẵn 2 file `Notification` từ **09/08**, không phải do tính năng này | Pass |

## TC-PWA

**Không áp dụng** — tính năng không có màn hình mobile.

---

## Việc còn treo, không thuộc phạm vi bộ test này

| Việc | Ghi chú |
|---|---|
| Điểm (b) anh Thắng chốt 25/08 — *"chỉ tự sinh BOM khi mặt hàng chưa có BOM nào"* | Luồng Ghim **không gọi** `auto_create_bom` nên không có rủi ro ghi đè ở đây. Nhưng `auto_create_bom` vẫn quyết định bằng `is_bom_tree_valid` (*BOM có khớp công thức mẫu không*) chứ không phải *có BOM hay chưa* — nút trên màn hình BOM và Kế hoạch sản xuất vẫn có thể **thay mất BOM sửa tay**. Đã báo Tuấn và phiên kia; cần chốt ai sửa |
| Điểm (d) — *"ghim rồi mà bổ sung rule/template thì phải ấn nút tính lại"* | Màn hình Kiểm Tra Tồn Kho tính lại mỗi lần bấm, không có bộ nhớ đệm. Nhưng **số đã ghim thì không tự đổi** khi template đổi. Cần hỏi anh Thắng: có cần nút tính lại phần ghim riêng không |
