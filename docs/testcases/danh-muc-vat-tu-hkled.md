# Test case — Nạp danh mục vật tư HKLED, 11 sheet (PM-TASK-00061)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Ngày chạy vòng tự kiểm:** 10/08/2026 · **Người chạy:** Claude (Trợ lý)

Nạp toàn bộ Google Sheet đính trong PM-TASK-00061 — **11 sheet, 1.516 dòng**. Bản đầu (10/08 sáng)
chỉ làm sheet *(O) Ốc, vít, bulong*; Thắng duyệt rồi giao làm nốt 10 sheet còn lại.

Nguồn chép nguyên xi thành `mbwnext_hkled/data/danh_muc/*.csv`, xử lý ở
`mbwnext_hkled/data/nhap_item.py`, chạy bằng patch `import_danh_muc_vat_tu`.

| Sheet | Dòng | Sheet | Dòng |
|---|---|---|---|
| (O) Ốc, vít, bulong | 46 | (V) Vỏ đèn | 265 |
| PCB | 44 | (N) Nguồn | 74 |
| LED | 32 | (SPD) Chống sét | 16 |
| (C) Chip LED | 626 | (WPC) Cầu đấu | 34 |
| (M) Module | 136 | Linh phụ kiện gia công cơ khí | 43 |
| (PTN) Tản nhiệt | 200 | | |

## Dữ liệu trước khi chạy

Site có **59.063 Item**, 60 Nhóm Sản Phẩm. Không mã nào trong 1.675 mã của bảng trùng với item cũ.

---

## TC-HAPPY — nạp đúng và đủ

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Nạp toàn bộ 11 sheet | Chạy patch | Không lỗi giữa chừng | Pass | Pass |
| TC-HAPPY-02 | Số item tạo ra | Đếm tổng Item trước/sau | 59.063 → 60.784 (+1.721) | Pass — 215 cha + 1.503 biến thể + 3 hàng đơn lẻ | Pass |
| TC-HAPPY-03 | 🔴 **Đối soát từng dòng nguồn** | Mỗi dòng phải rơi vào đúng một trạng thái: đã nạp, hoặc bị bỏ có lý do | 1.516 dòng, không dòng nào rơi ra ngoài | Pass — **1.516/1.516 nạp hết**, 0 bỏ qua | Pass |
| TC-HAPPY-04 | 🔴 Nội dung từng item khớp bảng | So `item_name`, nhóm, đơn vị, giá, `variant_of` và toàn bộ cặp (đặc tính, giá trị) | Khớp tuyệt đối | Pass — **0/1.516 sai lệch** | Pass |
| TC-HAPPY-05 | Nhóm sản phẩm mới | Đếm nhóm trước/sau | 60 → 80 | Pass — 20 nhóm mới cho cả task (19 ở lần chạy này, nhóm *(O) Ốc, vít, bulong* đã tạo từ vòng trước) | Pass |
| TC-HAPPY-06 | Mã giữ đúng quy ước khách | Xem mã sinh ra | Ép thẳng từ bảng, không để ERPNext tự đặt | Pass | Pass |
| TC-HAPPY-07 | Đơn vị tính và giá | Đọc `stock_uom`, `standard_rate` | Cái / 0 | Pass — 1.516/1.516 | Pass |

## TC-VALID — bỏ qua đúng chỗ, không đoán bừa

Nguyên tắc: **thà bỏ qua còn hơn đoán**. Bốn nhóm dưới đây bộ nạp cố ý không xử lý.

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | Trùng mã, nội dung khác | Rà mã biến thể lặp | Bỏ toàn bộ, ghi vào báo cáo | Pass — 40 mã / 84 dòng | Pass |
| TC-VALID-02 | Trùng mã, nội dung giống hệt | Rà dòng lặp | Giữ dòng đầu, **không** coi là lỗi | Pass — 10 dòng | Pass |
| TC-VALID-03 | 🔴 Biến thể **được phép** thiếu đặc tính của cha | Cha 3 đặc tính, biến thể khai 2; và khai đủ nhưng để trống giá trị | Tạo được cả hai; ô trống bị ERPNext tự bỏ | Pass — **luật cũ của bộ nạp là sai, đã gỡ**, xem mục dưới | Pass |
| TC-VALID-04 | Hai mã đụng cùng tổ hợp đặc tính | Rà tổ hợp trong từng cha | Bỏ đúng các mã đụng, phần còn lại của cha vẫn nạp | Pass — 10 mã | Pass |
| TC-VALID-05 | Đặc tính chưa có trên site | Gọi `_bao_dam_gia_tri` với đặc tính lạ | **Báo lỗi**, không tự tạo Item Attribute | Pass — chặn bằng `frappe.throw` | Pass |

## TC-REGR — không đụng dữ liệu cũ

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Item cũ nguyên vẹn | Đếm Item cũ | 59.063 | Pass | Pass |
| TC-REGR-02 | Không trùng mã với item cũ | Đối chiếu 1.675 mã của bảng với site | 0 trùng | Pass | Pass |
| TC-REGR-03 | Nhóm sản phẩm cũ không đổi cha | Xem `parent_item_group` 60 nhóm cũ | Vẫn NULL | Pass — nhóm mới cũng tạo phẳng | Pass |
| TC-REGR-04 | Không đẻ đặc tính mới | Đếm Item Attribute trước/sau | Không đổi — chỉ thêm **giá trị** | Pass — Item Attribute vẫn 54, chỉ thêm 6 giá trị (Loại LED 8→10, Mạch 4→8) | Pass |

## TC-EDGE — ca dễ sót

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | Chạy lại không đẻ trùng | Chạy patch lần 2 | Thêm 0 | Pass — vẫn 60.784 | Pass |
| TC-EDGE-02 | `standard_rate` bắt buộc | Tạo item không gán giá | Đặt `0`, không dùng `ignore_mandatory` | Pass — item mở lên lưu lại được | Pass |
| TC-EDGE-03 | `abbr` của giá trị đặc tính phải duy nhất | Thêm giá trị `1W` vào *Công suất* | Không đụng abbr của giá trị `1` đang có | Pass — sau khi chuẩn hoá thì không phải thêm nữa | Pass |
| TC-EDGE-04 | Chuẩn hoá giá trị viết khác kiểu | Sheet LED ghi `1W/2W/5W`, site dùng số trần | Quy về `1/2/5`, không đẻ giá trị trùng nghĩa | Pass — 32 dòng | Pass |
| TC-EDGE-05 | Ánh xạ đặc tính trùng nghĩa | `Dimming`, `Tương thích chip LED` | Dùng đặc tính có sẵn, không tạo mới | Pass — giá trị trùng khít 100% | Pass |
| TC-EDGE-06 | Mã biến thể trùng mã cha | 3 dòng ở sheet PTN | Tạo thành **hàng đơn lẻ** (không biến thể) | Pass — 3 item | Pass |
| TC-EDGE-07 | Tên hụt mảnh (sheet ốc vít) | Xem 18 tên có nhãn cụt | Dọn mảnh trống | Pass | Pass |
| TC-EDGE-08 | 10 sheet còn lại không bị dọn nhầm tên | Rà nhãn cụt ở 10 sheet kia | Không sheet nào dính, giữ nguyên xi | Pass | Pass |
| TC-EDGE-09 | Kiểm trên giao diện | Mở danh sách theo nhóm + form item cha/biến thể trên Desk (`localhost:8012`) | Hiện đúng | Pass — dữ liệu đúng, nhưng lộ thêm 1 vấn đề hiển thị, xem mục 4c | Pass |
| TC-EDGE-12 | Đổi tên mặt hàng cha trùng tên biến thể | Chạy lại bộ nạp | 25 cha đổi tên, 0 cặp trùng tên còn lại | Pass — thêm 2 cha vốn còn tên cũ từ trước cũng được sửa theo | Pass |
| TC-EDGE-13 | Không đổi tên nhầm cha khác | Rà mọi cha có đuôi *Công suất …W* nhưng không trùng biến thể | Giữ nguyên xi | Pass | Pass |
| TC-EDGE-11 | Soi chuỗi hiển thị thay cho giao diện | Dựng lại đúng text danh sách Item sẽ hiện, dò bất thường trên 1.557 mã | Không có dấu phân cách rỗng, nhãn cụt, `#REF`, tên rỗng | Pass với 2 ghi nhận — xem mục 4 | Pass |
| TC-EDGE-10 | Xoá dòng khỏi CSV rồi migrate | Chưa chạy | Mã đã tạo vẫn ở lại | **Chưa chạy** | — |

---

## Vấn đề trong bảng nguồn — ĐÃ SỬA XONG (11/08)

Vòng đầu có **158 dòng chưa nạp được**. Sau hai lượt trao đổi với Thắng, giờ **nạp hết 1.516/1.516**.

| Lượt | Việc | Còn lại |
|---|---|---|
| 10/08 tối | Bản đầu — bộ nạp bỏ 4 nhóm | 158 dòng |
| 11/08 08:46 | Thắng phản biện luật *"biến thể phải đủ đặc tính của cha"* → **luật sai, đã gỡ** | 94 dòng |
| 11/08 10:10 | Thắng đặt lại mã 523 dòng (thêm hậu tố `-8LED`, `-49LED`…; tách `-BN`) | 15 dòng |
| 11/08 11:24 | Thắng tách nốt 6 mã trùng theo Điện áp (`COBC050-*-30VDC` / `-42VDC`…) | **0** |

⚠ **Đổi mã hàng loạt để lại rác trên site.** Mỗi lượt Thắng đặt lại mã, những item đã nạp theo mã cũ
trở thành mồ côi: lượt 1 để lại **491 item**, lượt 2 thêm **3 item**. Bộ nạp chỉ biết thêm mới, không
biết mã nào vừa bị đổi tên. Phải rà thủ công: lấy tập mã trong bảng, so với item trên site thuộc các
nhóm đó, phần thừa thì **kiểm không dính chứng từ nào** (kho, BOM, đơn hàng, bảng giá) rồi mới xoá.
Lần sau khách đổi mã hàng loạt thì nhớ bước này, nếu không site có cả hai bộ mã mà đối soát vẫn báo
"khớp".

### 4. Hai ghi nhận từ vòng soi chuỗi hiển thị (không chặn, nhưng nên sửa bảng)

**a) ~~25/215 mặt hàng cha trùng tên với chính một biến thể của nó~~ — ĐÃ SỬA 11/08**

Chốt của Thắng: *"em chỉ cần sửa lại giúp anh tên mặt hàng cha trùng với biến thể là được, những cái
tên dài kệ nó"*. Bộ nạp bỏ đuôi *"Công suất …W"* khỏi tên mặt hàng cha **chỉ khi nó trùng y hệt tên
một biến thể** (`ten_mat_hang_cha()`), và thêm `sua_ten_neu_lech()` để sửa cả item đã nằm sẵn trên
site — vốn bộ nạp chỉ biết thêm mới, không sửa. Kết quả: **0 cặp trùng tên tuyệt đối** trên toàn bộ
1.721 item.

Chi tiết cũ:

**a-cũ) 25/215 mặt hàng cha trùng tên với chính một biến thể của nó** — toàn bộ ở sheet *(V) Vỏ đèn*.
Cột *Tên sản phẩm* của cha chép nguyên tên biến thể đầu tiên, kèm cả công suất:

| Mã | Vai trò | Tên hiển thị |
|---|---|---|
| `VDD11` | mặt hàng cha | Vỏ đèn đường D11 Chip LED SMD **Công suất 50W** |
| `VDD11S050` | biến thể | Vỏ đèn đường D11 Chip LED SMD **Công suất 50W** |

Cha bao trùm mọi công suất nên tên cha không nên mang một mức công suất cụ thể. Trên danh sách Item
sẽ thấy hai dòng chữ y hệt nhau, chỉ phân biệt bằng mã và nhãn *Template*. Bộ nạp **giữ nguyên** vì
đây là nội dung khách viết, không phải mảnh thừa của công thức như ca `Ren , Đầu , Khe ,`.

Đủ 24 mã: `VDD7X`, `VDD9X`, `VDD11`…`VDD15`, `VDD21`…`VDD26`, `VDXHB`, `VDXTT`, `VDX01`, `VDX03`,
`VDPCT`, `VDPKD`, `VDPVD`, `VDPVL`, `VDNCX`, `VDNU1`, `VDNU2`.

**b) 10 mã ở sheet LED có hai dấu cách liền** trong tên: `…Ra80␣␣| Trung tính…`. Thuần thẩm mỹ,
cũng giữ nguyên.

**c) 🔴 710/1.503 biến thể (47%) không phân biệt được trên danh sách Item** — chỉ thấy khi mở giao
diện, truy vấn không bao giờ báo. Tên đặt theo khuôn *phần chung trước, phần riêng sau*, mà cột
*Item Name* cắt ở khoảng 55 ký tự, nên phần phân biệt (màu ánh sáng, mạch, số LED) nằm ngoài vùng
nhìn thấy:

    Chip Module SMD 200W LED 5050 - Sử dụng: Module SMD 20…    CM50S200-3B5-5C
    Chip Module SMD 200W LED 5050 - Sử dụng: Module SMD 20…    CM50S200-4B5-5C
    Chip Module SMD 200W LED 5050 - Sử dụng: Module SMD 20…    CM50S200-5B5-5C

Ảnh hưởng **78/215 mặt hàng cha**, nặng nhất là *Chip LED đèn đường* (33 cha), *Chip LED đèn pha*
(9), *(M) Module* (6). Độ dài tên: trung vị 105 ký tự, dài nhất 140.

Người dùng buộc phải đọc cột mã để phân biệt. Cách sửa nằm ở bảng nguồn — đưa phần riêng lên trước
(`Trắng 6000K, 5C, 64LED — Chip Module SMD 200W…`) hoặc bỏ bớt đoạn *"Sử dụng: …"* khỏi tên và
chuyển xuống Mô tả. Bộ nạp **không tự đổi**, chờ HKLED quyết.

## Quyết định đã tự chốt

1. **Hai cột đặc tính ánh xạ vào đặc tính có sẵn** thay vì tạo mới: `Dimming` → *Khả năng điều chỉnh
   công suất*, `Tương thích chip LED` → *Phù hợp với chip LED*. Căn cứ: tập giá trị trùng khít 100%
   (`{Không, Dim 1/5/10 Cấp}` và `{5C, 40C, 5C / 7C / 8C}`), tức site đã dựng sẵn từ chính bảng này.
2. **`Công suất` quy về số trần**: sheet LED ghi `1W/2W/5W`, 10 sheet còn lại và cả site đều dùng
   `1/2/5` (phần "W" nằm ở `abbr`). Không quy về là site có cả `1` lẫn `1W` cho cùng một công suất.
3. **`Loại LED` thêm `3030`, `5050` làm giá trị mới** — KHÁC `Lumileds 3030`: PCB không kén hãng chip.
4. **`Mạch` thêm `5Cx2 … 5Cx5`** — giá trị mới thật, 269 dòng dùng.
5. **3 dòng có mã biến thể trùng mã cha** (sheet PTN) tạo thành hàng đơn lẻ, không biến thể.
