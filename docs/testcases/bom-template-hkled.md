# Test case — BOM Template theo file khách gửi (PM-TASK-00110)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Ngày chạy vòng tự kiểm:** 18/08/2026 · **Người chạy:** Claude (Trợ lý)

Yêu cầu: dựng BOM Template cho các mặt hàng cha theo file Google Sheet trong mô tả task.
File **lớn dần trong lúc làm**: 3 sheet ban đầu → +`M30S050-B`, `M50S050-A`, `M50S050-B`
→ +`DP03S`. Hiện **7 sheet**.

| Sheet | Mặt hàng cha | Biến thể | Rule dựng ra | Trạng thái |
|---|---|---|---|---|
| DP01S | đèn pha P01 (vỏ xám) | 5.120 | 308 | ✅ ghi đè bản cũ |
| DP03S | đèn pha P03 (vỏ đen) | 5.120 | 308 | ✅ |
| M30S050-A | module 30S050 loại A | 40 | 18 | ✅ |
| M30S050-B | module 30S050 loại B | 40 | 18 | ✅ |
| M50S050-A | module 50S050 loại A | 16 | 10 | ✅ |
| M50S050-B | module 50S050 loại B | 16 | 10 | ✅ |
| VDP0X | vỏ đèn pha | 28 | 45 | ✅ |

## Cách tự kiểm — mô phỏng trước khi ghi

Không thể mở tay 5.260 biến thể. Bộ nạp **mô phỏng khớp rule cho TỪNG cặp (biến thể ×
thành phần Theo Rule) trước khi ghi**, và **không ghi sheet nào còn cặp hỏng ngoài dự
kiến**. Phải chặn cứng vì `find_rule_item` trong Server Script `frappe.throw` khi không
rule nào khớp — một cặp hỏng là một BOM không tạo được, không phải cảnh báo nhẹ.

Cặp không khớp được xếp ba nhóm, chỉ nhóm cuối mới chặn ghi:

| Nhóm | Nghĩa | DP01S | 5 sheet còn lại |
|---|---|---|---|
| `co_y` | khách ghi "Không sử dụng" | ~~640 mỗi sheet~~ → **0** từ 21/08 (đã có rule tích ô) | 0 |
| `chua_co_du_lieu` | khách xác nhận chưa khai (`CHUA_CO_DU_LIEU`) | 2.368 mỗi sheet | 0 |
| `hong` | thiếu ngoài dự kiến → **chặn ghi** | **0** | **0** |

(cột "DP01S" áp dụng cho cả `DP03S` — hai sheet cấu trúc y hệt)

---

## TC-HAPPY — dựng đúng dữ liệu khách

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Tạo đủ Thành Phần BOM còn thiếu | Chạy patch | 15 bản ghi mới | Pass — 15 → 30 | Pass |
| TC-HAPPY-02 | Dựng đủ 7 BOM Template | Chạy patch | 7 template, `Hoạt Động` bật | Pass | Pass |
| TC-HAPPY-03 | 🔴 Không còn cặp hỏng ngoài dự kiến | Mô phỏng toàn bộ 82.668 cặp | 0 | Pass — **0** | Pass |
| TC-HAPPY-04 | 🔴 Sinh được NVL thật | Gọi `get_template_raw_materials` trên mẫu 122 biến thể DP01S và 122 của DP03S | ra danh sách NVL + số lượng | Pass — **99/122 cả hai sheet**, 23 ca lỗi đều nằm trong hai nhóm đã biết | Pass |
| TC-HAPPY-05 | Số lượng theo công thức đúng | `DP01S300-3B3HT-AD` (300W Dọc) | 6 Module, 12 ốc (=6×2) | Pass — 6 và 12 | Pass |
| TC-HAPPY-06 | Mỗi biến thể khớp đúng 1 rule | `resolve_rules` chặn phủ trùng | lưu được | Pass | Pass |
| TC-HAPPY-07 | Ghi đè, không tạo bản song song | Chạy patch nhiều lần | vẫn 6 template, số rule không đổi | Pass | Pass |

## TC-VALID — bảy cách viết đặc biệt trong sheet

Chốt của Thắng 18/08 trên PM-TASK-00110.

| Mã | Cách viết | Dựng thành | KQ thực tế | P/F |
|---|---|---|---|---|
| TC-VALID-01 | `Mọi biến thể đều chọn` | *Theo Rule*, tích đủ mọi giá trị một đặc tính | Pass — VDP0X 13 thành phần phủ 28/28 | Pass |
| TC-VALID-02 | `tất cả` / `Tất cả` | bỏ đặc tính khỏi điều kiện | Pass | Pass |
| TC-VALID-03 | 🔴 `Còn lại` | liệt kê thẳng tổ hợp chưa bị rule trên chiếm | Pass — Module: 96 dòng sheet → 128 rule, 5.120/5.120 khớp đúng 1 rule | Pass |
| TC-VALID-04 | `Các loại còn lại` | như `Còn lại`, dùng ở cột Nguồn khối Cầu đấu | Pass | Pass |
| TC-VALID-05 | `A và B` trong một ô | OR nhiều giá trị | Pass — `HKLED Dim 1 Cấp và HKLED Dim 5 Cấp` → 2 giá trị | Pass |
| TC-VALID-06 | `Không sử dụng` | không tạo rule | Pass — 8 tổ hợp; **lộ lỗi engine**, xem mục B | Pass |
| TC-VALID-07 | Ánh xạ tên đặc tính | `Loại LED`→`Chip LED`, `Kiểu lắp`→`Phân loại vỏ` | Pass — VDP0X `Quai` từ 28 cặp hỏng về 0 | Pass |
| TC-VALID-08 | Rule một dòng `<Đặc tính>: <Giá trị>` | `Tai \| Màu sơn: Xám \| PTA-…` | Pass — khách đổi `Tai` và `Hộp nguồn` sang dạng này, dòng sau bỏ trống cột thành phần | Pass |

## TC-EDGE — chỗ dễ đọc sai file

| Mã | Mục tiêu | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|
| TC-EDGE-01 | 🔴 `Còn lại` xét theo **tổ hợp**, không theo từng đặc tính | còn 14 cặp (CS, KL) | Pass — xét riêng từng đặc tính ra **tập rỗng**, sai | Pass |
| TC-EDGE-02 | 🔴 `Tất cả` viết hoa | vẫn hiểu là "không ràng buộc" | Pass — bản đầu so khớp phân biệt hoa thường, rule *Năng lượng mặt trời* thành `Công suất = "Tất cả"` và **chết lặng** | Pass |
| TC-EDGE-03 | Rule rỗng điều kiện | không tạo | Pass — `find_rule_item` lọc `if cond and …` nên rule rỗng không bao giờ khớp | Pass |
| TC-EDGE-04 | Cột điều kiện điền dở | **dừng, không đoán** | Pass — bộ đọc `raise`, bỏ qua cả sheet | Pass |
| TC-EDGE-05 | Cột điều kiện trống hoàn toàn | bỏ đặc tính đó | Pass | Pass |
| TC-EDGE-06 | Ô số lượng nhiều nhánh | giữ nguyên văn cả cụm, báo lên | Pass — bản đọc đầu chỉ lấy 1 cột, **mất nhánh "SL 30"**; đã sửa | Pass |
| TC-EDGE-07 | Kiểm trên giao diện — bảng rule | Cột *Điều kiện* và *Biến Thể Khớp* hiện đúng | Pass (**giao diện**) — VDP0X: `Tai` 14 Xám / 14 Đen, `Quai` 6+8 mỗi màu, 9 thành phần dùng chung phủ 28/28 | Pass |
| TC-EDGE-08 | 🔴 Kiểm trên giao diện — tạo BOM thật | Chọn Mặt Hàng trên form BOM thì tự điền NVL | Pass (**giao diện**) — `DP03S300-3B3HT-AD`: *"Đã điền 8 nguyên vật liệu từ BOM Template BOM Template DP03S"*, dòng đầu `VDP0X-300-D-BK-v3.0` (**vỏ đen**), Module x6, ốc x12 | Pass |
| TC-EDGE-09 | So chéo DP01S / DP03S | cùng cấu hình chỉ khác phần vỏ | Pass (**giao diện**) — `DP01S300-…` ra `VDP0X-300-D-GY-v3.0`, `DP03S300-…` ra `-BK-`, 7 dòng còn lại giống hệt | Pass |
| TC-EDGE-10 | Ca lỗi không chặn form | biến thể 50W/Dọc | Pass (**giao diện**) — hiện hộp thoại *"Chưa điền được Nguyên Vật Liệu"* kèm nguyên văn lý do, form **vẫn nhập tay được**, không bị khoá | Pass |
| TC-KSD-01 | Biến thể khách ghi *Không sử dụng* tạo được BOM | `DP01S050-3B3HT-AD` ra BOM, **không có Cầu đấu** | Pass — 6 NVL, không dòng `WPC-`; trước đây throw *"Chưa thiết lập NVL cho thành phần Cầu đấu"* | Pass |
| TC-KSD-02 | Không hồi quy biến thể bình thường | `DP01S300-3B3HT-AD` vẫn đủ 8 NVL, **có** Cầu đấu | Pass — mẫu 60 biến thể 200W: 60/60 tạo được, 60/60 có `WPC-` | Pass |
| TC-KSD-03 | Biến thể 50W không có Cầu đấu | 0/60 có Cầu đấu | Pass — mẫu 60 biến thể 50W: **0** có Cầu đấu.
  ⚠ Số cũ ghi "16 vẫn có Cầu đấu" là **SAI**: đếm bằng tiền tố mã `WPC-`, mà `WPC-SLM-…` là *Nguồn*
  của biến thể năng lượng mặt trời chứ không phải Cầu đấu. Đếm lại bằng tên thành phần ra 0. |
| TC-KSD-04 | Nhóm `co_y` trong `kiem_khop` về 0 | 0 | Pass — trước 640 mỗi sheet DP01S/DP03S, nay 0; `hong` vẫn 0 | Pass |
| TC-KSD-05 | 🔴 Chặn rule rỗng | không NVL + không tích ô → **chặn** | Pass — *"Rule #11 (Chip LED): chưa chọn Nguyên Vật Liệu. Nếu biến thể này không dùng thành phần đó thì tích ô Không Sử Dụng."* | Pass |
| TC-KSD-06 | 🔴 Chặn tích ô mà vẫn chọn NVL | **chặn** | Pass — *"đã tích Không Sử Dụng thì phải bỏ trống Nguyên Vật Liệu"* | Pass |
| TC-KSD-07 | Tích ô + bỏ trống NVL là hợp lệ | lưu được | Pass | Pass |
| TC-KSD-08 | Số rule sau khi nạp lại | tăng đúng bằng số tổ hợp *Không sử dụng* | Pass — 719 → **733**, 16 dòng tích ô, đều ở *Cầu đấu* của DP01S/DP03S; 0 rule mồ côi | Pass |
| TC-CT-01 | Đối chiếu 5 công thức với bảng khách 22/08 | 0 tổ hợp lệch | Pass — 160/160 tổ hợp thật của DP01S khớp, sau khi sửa 5 lỗi | Pass |
| TC-CT-02 | Dây điện cấp nguồn khi dùng nguồn to | **0** (dây đi kèm nguồn) | Pass — `DP01S300-3B3HT-AD` không còn dòng `W-3x0.75-BK`; trước cấp thừa 98/160 tổ hợp | Pass |
| TC-CT-03 | Nguồn/Cầu đấu, Ngang, nguồn to HKLED, CS>600 | ưu tiên %300 → %250 → %200 | Pass — 1000W ra 4, trước ra 2 | Pass |
| TC-CT-04 | Nguồn/Cầu đấu, Ngang, nguồn to hãng khác | ưu tiên %250 → **%150** → %200 | Pass — 1200W ra 8, trước ra 6 | Pass |
| TC-CT-05 | Xốp góc | **4** | Pass — mọi biến thể DP01S/DP03S ra 4; trước ra 1 | Pass |
| TC-CT-06 | 🔴 Phân loại nguồn theo `Kiểu nguồn`, không theo tên hãng | *Năng lượng mặt trời* = nguồn **to** | Pass — trước bị xếp nhầm *nhỏ*, sai 512 biến thể mỗi template | Pass |
| TC-CT-07 | Đèn đường: nguồn to HKLED | luôn **1** bất kể công suất | Pass — chưa template nào dùng nhóm này, mới kiểm bằng hàm | Pass |
| TC-CT-08 | 🔴 Bộ đối chiếu tự bắt được lỗi | gieo lỗi phân loại → phải báo lệch | Pass — gieo lỗi ra **112 tổ hợp lệch**; bản đầu của bộ đối chiếu dùng chung hàm phân loại cho cả 2 phía nên **mù** với lỗi TC-CT-06 |
| TC-CT-09 | Ô Số Lượng trống → cảnh báo bắn được | bộ nạp ghi **0**, không ghi 1 | Pass — ghi 1 thì `qty_defaulted` không bao giờ bắn, đúng cách Xốp góc lọt lưới |
| TC-KSD-09 | Giao diện — ô tích trong hộp thoại *Tạo Rule* | tích ô thì ô NVL ẩn và hết bắt buộc | Pass (**giao diện**) — tích xong trường *Nguyên Vật Liệu* biến mất hẳn | Pass |
| TC-CT-10 | *Năng lượng mặt trời* → Nguồn | **1 phẳng**, mọi công suất/kiểu lắp | Pass — 1000W Ngang ra 1; trước ra 4 (đi nhánh hãng khác) | Pass |
| TC-CT-11 | *Năng lượng mặt trời* → Cầu đấu và Dây điện | vẫn xử lý như **nguồn to** | Pass — 1000W Ngang: Cầu đấu 4, Dây điện 0 | Pass |
| TC-CT-12 | Khoảng 500 < CS ≤ 1000 ở Ngang (dây điện) | **200** | Pass — khách lấp khoảng trống 22/08, đã bỏ nhánh TODO | Pass |
| TC-CT-13 | Đối chiếu lại sau bản khách sửa 22/08 chiều | 0 tổ hợp lệch, 0 ô bỏ trống | Pass — 160/160 khớp, không còn ô nào không kết luận được | Pass |
| TC-UI-01 | 🔴 Giao diện — cột *Không Sử Dụng* hiện trên lưới rule | có cột, dòng tích ô để trống NVL | Pass (**giao diện**) — DP01S dòng 245/247/259/261 tích ô, ô NVL trống. ⚠ Ban đầu **KHÔNG hiện**: tổng `columns` vượt 11 *và* `__UserSettings` giữ bố cục cũ. Xem patch `reset_bom_rule_grid_view` | Pass |
| TC-UI-02 | Giao diện — tạo BOM `DP01S300-3B3HT-AD` | 7 dòng, Xốp góc **4**, **không** có dây điện | Pass (**giao diện**) — trước là 8 dòng có `W-3x0.75-BK` 100m và Xốp góc 1 | Pass |
| TC-UI-03 | Giao diện — tạo BOM `DP01S1K0-3B3HT-AN` (1000W Ngang HKLED) | Nguồn **4**, Cầu đấu **4** | Pass (**giao diện**) — trước cả hai ra 2; Module 20, ốc 40, Xốp góc 4 | Pass |
| TC-UI-04 | Giao diện — biến thể 1200W (khách chưa khai NVL) | báo lỗi rõ, **không khoá form** | Pass (**giao diện**) — hộp thoại *"Chưa điền được Nguyên Vật Liệu"* nêu đích danh thành phần và biến thể | Pass |

## TC-REGR — không đụng thứ khác

| Mã | Mục tiêu | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|
| TC-REGR-01 | Không đụng template ngoài phạm vi | `thành phẩm 1` (DD11S050) giữ nguyên | Pass | Pass |
| TC-REGR-02 | Không sửa công thức số lượng | Server Script không đổi | Pass — chốt của Thắng, chờ anh Tùng | Pass |
| TC-REGR-03 | Không đụng danh mục mặt hàng | mã NVL trong file đều đã có sẵn | Pass — 0 mã phải tạo mới | Pass |
| TC-REGR-04 | Ghi đè không để lại dòng con mồ côi | 0 | Pass — bản DP01S cũ 17 rule đã gỡ sạch; `parentfield` toàn `bom_rules`; `idx` liên tục 1..308 không trùng | Pass |
| TC-REGR-05 | Mỗi mặt hàng cha chỉ 1 template Hoạt Động | 0 vi phạm | Pass | Pass |

---

## Hai lỗi engine — Thắng chốt chờ anh Tùng

### A. Không có bộ công thức số lượng cho module và vỏ

5 template module/vỏ lưu được và tra NVL đúng 100%, nhưng **0/140 biến thể sinh được BOM**:

> Mặt hàng cha M30S050-A chưa có bộ công thức số lượng.

`resolve_formula_group` chỉ suy được cho đèn thành phẩm (tiền tố `DP01`, `DD01`…). Module
và vỏ không khớp tiền tố nào. Script còn `throw` khi biến thể thiếu đặc tính `Công suất` —
biến thể module không có đặc tính này.

Số lượng của 4 sheet module đã có sẵn trong file (1 / 8 / 16), nên hướng gọn nhất là thêm
một nhóm **"lấy số lượng ngay trên dòng thành phần"**. Không tự làm: `COMPONENT_MAP` đang
có sẵn công thức cho `Chip LED`, `Lens`, `Gioăng chip`, `Ốc vít bắt chip` — viết cho đèn
thành phẩm, áp nhầm sang module thì ra số sai mà không có gì báo.

### B. Tra rule chạy TRƯỚC khi tính số lượng

Tổ hợp `Không sử dụng` **báo lỗi** thay vì bỏ dòng: nhánh `component_type == "Theo Rule"`
tra NVL và `throw` trước khối tính số lượng, dù `calc_cau_dau_qty` trả đúng 0 cho chính
các tổ hợp ấy và `resolve_components` đã có sẵn đoạn bỏ dòng khi số lượng ≤ 0.

Kiểm chứng trên site: `DP01S050-3B3HT-AD` (50W Dọc) →
*"Chưa thiết lập NVL cho thành phần Cầu đấu"*. Ảnh hưởng **640 biến thể**.

Sửa: tính số lượng trước, ≤ 0 thì bỏ qua bước tra rule.

## Số lượng chưa có

| Nơi | Sheet ghi | Đang để |
|---|---|---|
| VDP0X — cả 13 thành phần | ô SL còn nguyên nhãn `Ghi chú` | 1 |
| 4 sheet module — `Cầu đấu` | `Kiểu đấu: Cầu đấu SL 1 \| Dây diện SL 30` | 1 |
| 4 sheet module — `Ốc dây điện` | `Kiểu đấu: Cầu đấu SL 0 \| Dây diện SL 1` | 1 |

Manh mối cho VDP0X: mã `Khung module` cho vỏ Ngang luôn là **nửa công suất** của đèn
(100W→`PKG-VDP0X-050`, 1000W→`PKG-VDP0X-500`), đều đặn ở cả 8 mức — nhiều khả năng vỏ
Ngang lắp **2 khung**. Chưa xác nhận nên vẫn để 1.

## Đã hỏi và đã được trả lời — không phải lỗi

- **VDP0X `Quai`**: `Dọc → PQU-VDP0X-N-…`, `Ngang → PQU-VDP0X-D-…` nhìn như đảo mã. Thắng
  xác nhận **N/D ở đây là ngắn/dài**, không phải Ngang/Dọc. Đúng như file.
- **VDP0X màu đen — hoá ra sai thật.** Vòng đầu em báo: 14 biến thể `Màu sơn = Đen` đang
  lắp linh kiện `-GY-`, dù cả 26 mã `-GY-` trong sheet đều có bản `-BK-` trên phần mềm.
  Thắng trả lời "khách xác nhận không sai". Sau đó khách báo lại là **nhầm** và đã sửa
  file: VDP0X giờ có `Màu sơn` trong điều kiện, 16 mã xám + 16 mã đen, 27 → 45 rule.
- **DP01S 1200W/1500W**: 640 biến thể chưa có NVL cho Bộ vỏ đèn, Hộp carton, Cầu đấu,
  Nguồn. Thắng: *"tạm thời chưa đặt sản xuất, chưa có BOM chính xác nên bỏ trống đã"*. Khai
  ở `CHUA_CO_DU_LIEU` trong `data/nhap_bom_template.py`; xoá mục đó đi là bộ nạp đòi lại.

## Chi phí bảo trì đã biết trước

Nhìn trên giao diện thấy rõ: 9 rule "Mọi biến thể đều chọn" của VDP0X hiện điều kiện
**`Version: v3.0`** — đó là đặc tính ít giá trị nhất nên bộ nạp chọn làm trục. Khách ra vỏ
`v4.0` thì 9 rule đó **ngừng khớp**, BOM báo thiếu NVL.

Các rule `Mọi biến thể đều chọn` liệt kê sẵn mọi giá trị của một đặc tính. Khách thêm một
giá trị mới (màu sơn mới, mức công suất mới) thì rule **không tự phủ** — phải mở BOM
Template tích thêm. Đã đề xuất dùng *Cố Định* để tránh, Thắng chọn *Theo Rule* vì còn cần
chạy công thức số lượng ở Server Script.
