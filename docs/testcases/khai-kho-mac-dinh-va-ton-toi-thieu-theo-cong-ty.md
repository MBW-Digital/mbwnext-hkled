# Test case — Phần IV · Khai kho mặc định và tồn tối thiểu theo công ty (PM-FEAT-00037)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`, mở bằng
`http://dev.mbwnext.com:8012`
**Ngày chạy vòng tự kiểm:** 04/09/2026 · **Người chạy:** Claude (Trợ lý HKLed 2)

Đầu bài: `docs/features/khai-kho-mac-dinh-va-ton-toi-thieu-theo-cong-ty.md`
Code: **không có mã nghiệp vụ mới.** Tính năng là **một Custom Field** thêm vào bảng con
`Item Default` của lõi — `patches/them_ton_toi_thieu_vao_kho_mac_dinh.py` + `fixtures/custom_field.json`.

**Tổng kết:** **22 ca · 19 Pass · 3 cần người test.**

> ### ⚠ Đọc trước: tính năng này KHÔNG có logic riêng, nên rủi ro nằm chỗ khác
>
> Không có hàm nào mới để gọi sai. Cái có thể hỏng là: **trường biến mất khỏi site khác**
> (fixtures/module), **cột biến mất khỏi lưới** (trần độ rộng), và **dữ liệu bị xoá trắng khi
> nhập Excel**. Ba thứ đó không lộ ra bằng cách bấm thử một lần rồi thấy chạy được.

---

## Điều kiện chuẩn bị

| Cần gì | Giá trị |
|---|---|
| **Địa chỉ site** | `http://dev.mbwnext.com:8012` |
| **Tài khoản** | `administrator`; **thêm** `test.gioihan.sales@hkled.test` (*Sales User* + *Desk User*, User Permission Customer = `a`) cho nhóm TC-PERM |
| **Cách vào tính năng** | Thanh tìm kiếm → **Mặt hàng** → mở một mặt hàng → tab **Kế toán** (*Accounting*) → bảng **Mặc định cho mặt hàng** (*Item Defaults*) |
| **Dữ liệu cần có** | 6 mặt hàng đã khai sẵn: `Thành phẩm 1` (kho thành phẩm · 20) · `Bán thành phẩm 1`, `Bán thành phẩm 2` (kho bán thành phẩm · 5) · `NVL 1` (50) · `NVL 2` (40) · `NVL 3` (10) — đều kho nguyên vật liệu. Mặt hàng `Vỏ test A-100` dùng cho ca ghi/huỷ |

⚠ **Đường bấm ở trên đã kiểm bằng máy**, không phải nhớ: `item_defaults` nằm ở tab `Accounting`.
Đặc tả mục 2 ghi *"tab Tồn kho"* là **sai** — đã sửa.

---

## TC-HAPPY — luồng đúng

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Trường có mặt, đúng thuộc tính | Đọc Custom Field `Item Default-custom_ton_kho_kha_dung_toi_thieu` | Float · neo sau *Kho mặc định* · hiện trên lưới · không âm · module của app khách | Pass — `fieldtype=Float`, `insert_after=default_warehouse`, `in_list_view=1`, `columns=2`, `non_negative=1`, `module=MBWNext HKLed`, `reqd=0` | Pass |
| TC-HAPPY-02 | Khai rồi đọc lại ra đúng số | Đọc 6 mặt hàng đã khai | Đúng cặp *kho + tồn tối thiểu* theo từng công ty | Pass — `Thành phẩm 1` kho thành phẩm/**20** · `Bán thành phẩm 1` và `2` kho bán thành phẩm/**5** · `NVL 1` **50** · `NVL 2` **40** · `NVL 3` **10**, cả 6 đều công ty `HKLED` | Pass |
| TC-HAPPY-03 | Gõ số trên lưới rồi Lưu | Mở `Vỏ test A-100` → tab Kế toán → gõ `500` vào *Tồn Kho Khả Dụng Tối Thiểu* → Lưu → mở lại | Vẫn là 500 | Pass — **giao diện 03/09**: gõ 500, Lưu, mở lại vẫn 500; dọn về 0 cũng đúng | Pass |
| TC-HAPPY-04 | Hai cột là một cặp, khai cùng lúc | Xem thứ tự cột trên lưới | *Tồn Kho Khả Dụng Tối Thiểu* nằm **ngay sau** *Kho mặc định* | Pass — `insert_after = default_warehouse` | Pass |

## TC-VALID — kiểm tra dữ liệu

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | 🔴 **Số âm bị chặn ở MÁY CHỦ** | Đặt `custom_ton_kho_kha_dung_toi_thieu = -5` rồi `save()` — **đi đường máy chủ, không qua lưới** | Chặn, nêu đúng tên cột | Pass — `NonNegativeError: Item Default Row #1: Value cannot be negative for Tồn Kho Khả Dụng Tối Thiểu`. Đã `rollback`, giá trị trên máy vẫn **0.0** như trước | Pass |
| TC-VALID-02 | ⚠ Gõ số âm trên lưới **không chứng minh được gì** | Trên giao diện gõ `-5` rồi Lưu | Ô tự kẹp về 0 **trước khi gửi đi** — nên lưu được, và điều đó **không** nghĩa là máy chủ không chặn | Pass — **giao diện 03/09**: lưu được, nhưng máy chủ chưa hề nhận số âm nào. Bài học: *"thao tác trên màn hình thành công"* không chứng minh lớp máy chủ có chạy hay không — phải đẩy bằng đường khác (TC-VALID-01) | Pass |
| TC-VALID-03 | Bỏ trống là hợp lệ | Không điền gì | Không bắt buộc, không chặn lưu | Pass — `reqd=0`; 62.049/62.055 dòng đang trống và không dòng nào gây lỗi | Pass |

## TC-EDGE — biên & lặp

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | 🔴 **Trần độ rộng lưới — thêm cột là mất cột, KHÔNG báo gì** | Cộng độ rộng các cột đang hiện trên `Item Default` theo đúng luật `grid.js` | Tổng ≤ 11, còn biết **thêm được bao nhiêu** | Pass — 1 + `company` 2 + `default_warehouse` 2 + **cột mới 2** + `default_price_list` 2 = **9/11**. ⚠ **Đính chính đặc tả**: mục 5 ghi *"đúng sát trần 11/11"* là **sai** — nó tưởng Link rộng 3, nhưng `update_default_colsize` chỉ cho **Small Text = 3, Check = 1, còn lại = 2**. Thực tế **còn thêm được đúng 1 cột rộng 2**; cột thứ hai mới bị bỏ âm thầm (`total_colsize > 11` thì `return false`) | Pass |
| TC-EDGE-02 | Bảng chưa được khai gần hết | Đếm dòng có kho mặc định | Biết rõ độ phủ | Pass — **6 / 62.055** dòng có kho. Bảng đúng nhưng **chưa có đường khai hàng loạt** — xem TC-EDGE-03 | Pass |
| TC-EDGE-03 | 🔴 **Nhập Excel GHI ĐÈ CẢ DÒNG — cột không có trong file bị xoá trắng** | Trên `Vỏ test A-100` (đang có *Tài khoản doanh thu* 511): nạp file Excel chỉ gồm 2 cột *Công ty* + *Kho mặc định* | Kho vào đúng, **nhưng ô 511 bị xoá sạch** | Pass — **đo thật 03/09 trên giao diện**: kho vào đúng, ô 511 **mất**. Thử biến thể có kèm cả cột ID của dòng — **vẫn mất**. Đây là cách lõi làm việc với bảng con, không phải lỗi của tính năng. Đã hoàn nguyên, ô 511 còn nguyên | Pass |
| TC-EDGE-04 | Cách nhập Excel an toàn | Vào *Nhập dữ liệu* → bấm **Xuất** lấy file đủ cột → chỉ sửa 2 cột → nạp ngược lên | Cột không đụng tới vẫn còn nguyên | **Cần người test** — cần thao tác nhập/xuất thật trên giao diện với file Excel. Đây là **cách làm sẽ hướng dẫn khách**, phải có người xác nhận trước khi đưa cho khách |
| TC-EDGE-05 | Mức độ rủi ro hôm nay | Đếm dòng có cột khác đã điền | Biết bao nhiêu dòng sẽ bị xoá nếu nhập sai cách | Pass — **6/62.055** dòng có cột khác được điền, cả 6 chỉ có mỗi *Tài khoản doanh thu 511*. ⚠ Rủi ro **tăng vọt** sau khi khách khai xong tài khoản/nhà cung cấp mặc định cho cả danh mục rồi mới nhập Excel lần hai | Pass |

## TC-PERM — phân quyền

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-PERM-01 | Người không có quyền sửa Mặt hàng thì không khai được | Dưới `test.gioihan.sales@hkled.test`, kiểm quyền đọc/ghi `Item` | Đọc được, **không ghi được** | Pass — `has_permission("Item","read") = True`, `write = False`. Bảng nằm trong Mặt hàng nên quyền đi theo Mặt hàng, không cần phân quyền riêng | Pass |
| TC-PERM-02 | Người bị giới hạn phạm vi **vẫn đọc được** bảng này | Dưới đúng user đó, đọc `Item Default` | Đọc được — danh mục mặt hàng không giới hạn theo khách hàng | Pass — trả về 5 dòng. ⚠ **Ghi rõ để không ai tưởng là sót**: trường này **không đặt permlevel**, nên ai đọc được Mặt hàng thì thấy được mức tồn tối thiểu của mọi mặt hàng. Đúng với dữ liệu danh mục; nếu sau này khách coi con số này là nhạy cảm thì phải đặt permlevel — **hiện chưa ai yêu cầu** | Pass |
| TC-PERM-03 | Trả lại phiên đăng nhập sau khi thử | Sau TC-PERM-01/02 | Về `Administrator` | Pass — đã `set_user` trả lại, kiểm lại đúng `Administrator` | Pass |

## TC-REGR — regression app lõi

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Phần IV đọc được kho mặc định | Gọi `_kho_mac_dinh({...}, "HKLED")` | Trả đúng kho của từng mã, mã không có thì vắng mặt | Pass — `NVL 1/2/3` → *Kho nguyên vật liệu - HKL*, `Thành phẩm 1` → *Kho thành phẩm - HKL*, `MA-KHONG-CO` **không có mặt**. Công ty không tồn tại → `{}`; tập rỗng → `{}`. ⚠ Hàm nhận **một TẬP mã**, truyền chuỗi thì `list("NVL 1")` thành từng ký tự và ra `{}` — **trông y như lỗi** | Pass |
| TC-REGR-02 | Phần V đọc được cột tồn tối thiểu | Đọc `api/nhu_cau_vat_tu.py` | Có truy vấn `custom_ton_kho_kha_dung_toi_thieu as toi_thieu`, lọc theo `company` | Pass — `nhu_cau_vat_tu.py:134`, lọc đúng `parent in (...)` + `company`. ⚠ Đính chính đặc tả mục 6c *"chưa ai dùng cột tồn tối thiểu"* — **Phần V đã dùng rồi** | Pass |
| TC-REGR-03 | Không dựng bảng mới, dùng bảng lõi | Đọc code | Chỉ thêm 1 cột vào `Item Default` | Pass — không có DocType mới; các chức năng sẵn có của ERPNext (mua hàng, chuyển kho, sản xuất) vẫn đọc `default_warehouse` như cũ | Pass |

## TC-ISO — cách ly app khách

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-ISO-01 | Custom Field gán đúng module | Đọc trường `module` | Module của app khách | Pass — `MBWNext HKLed`. Thiếu cái này thì trường **không đi theo app** và biến mất ở lần deploy site mới | Pass |
| TC-ISO-02 | Có trong fixtures, không chỉ trong patch | Đọc `fixtures/custom_field.json` | Có mặt | Pass — có `Item Default-custom_ton_kho_kha_dung_toi_thieu`; file hiện **34 trường**. ⚠ Đặc tả mục 6d ghi *"35 trường"* — đếm lại là **34** | Pass |
| TC-ISO-03 | Site không cài app không có trường này | Trên `mbw.com` (không cài `mbwnext_hkled`), tìm trường | Không có | **Cần người test** — đã đo trên `mbw.com` là **không có** trường `custom_ton_kho_kha_dung_toi_thieu` (kiểm cùng lượt `bench migrate` 04/09 10:29), nhưng chưa thao tác Mặt hàng trên site đó để khẳng định luồng lõi không đổi |
| TC-ISO-04 | Patch chưa chạy trên site hiện tại | Tra `Patch Log` | Biết rõ trạng thái | **Cần người test / cần lượt migrate** — `them_ton_toi_thieu_vao_kho_mac_dinh` **CHƯA CHẠY** trên `hkled.com`. Trường vẫn có (fixtures đã nạp), nên hôm nay không ảnh hưởng; nhưng patch **sẽ chạy** ở lần `bench migrate` tới và cần xác nhận nó không ghi đè gì |

## TC-PWA

**Không áp dụng** — tính năng không có màn hình mobile.

---

## Hạn chế đã biết — không phải lỗi mới phát sinh

| Việc | Ảnh hưởng |
|---|---|
| **Chưa có đường khai hàng loạt** | 6/62.055 dòng có kho. Anh Thắng chốt 03/09 16:02 là **nhập từ Excel**, khách tự làm. Không phải viết code, nhưng **phải hướng dẫn kèm bẫy ở TC-EDGE-03** |
| **Ba trường nghĩa gần nhau** | `Item Default.custom_ton_kho_kha_dung_toi_thieu` (theo **công ty**) · `Item Reorder.warehouse_reorder_level` (theo **kho**, của lõi) · `Item.custom_ton_kho_toi_thieu` (**một số cho cả mặt hàng**, của Phần V). Khách sẽ khai nhầm nếu không gỡ bớt. Anh Thắng chốt 03/09 15:46 **dùng ô này, gỡ ô số 2** — ô của Phần V thuộc commit phiên khác, **chưa gỡ**, đang chờ Tuấn |
| `Item Reorder` đang có 1 bản ghi mức **0** | *Thành phẩm 1 · Kho thành phẩm · mức 0*, do anh Thắng tạo 21/07. Đọc như *"đã khai, mức 0"* chứ không phải *"chưa khai"* — và mức 0 khiến luật tồn kho tối đa của app lõi **không bao giờ nổ** (xem `TC-REGR-02` của PM-FEAT-00034) |
