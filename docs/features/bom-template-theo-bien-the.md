# HKLED — BOM Template theo Biến Thể (Giai đoạn 1, Phần I bản nâng cấp)

- **App**: `mbwnext_hkled` (tầng 4 — riêng khách HKLED)
- **Site dev**: `hkled.com` (bench `mbwnext_project`, dev server cổng 8047)
- **Nguồn yêu cầu**: PM `PM-PRJ-00003` › Tài liệu › Tài Liệu Giai Đoạn 1 › `BOM_Template_Design_HKLED` (`PM-DOC-00046`)
- **Tài liệu nghiệp vụ gốc**: `PM-DOC-00044` (docx), dữ liệu công thức: `PM-DOC-00043` (xlsx)
- **Ngày làm**: 2026-07-31

---

## 1. GIAI ĐOẠN ĐẦU BÀI — Phân tích tài liệu

### 1.1 Nội dung tài liệu yêu cầu

Tài liệu `BOM_Template_Design_HKLED` là **spec kỹ thuật đã chốt** (không phải yêu cầu thô),
gồm 5 mục. Nội dung cần làm:

| Mục | Yêu cầu |
|---|---|
| 2.1 | DocType mới `BOM Rule Group` — danh mục Nhóm Công Thức, 6 bản ghi ban đầu |
| 2.2 | `BOM Template` thêm field `rule_group` (Link, bắt buộc) |
| 2.3 | `BOM Component Table` thêm loại thứ 3 `Số Lượng Theo Công Thức` |
| 2.4 | `BOM Rule` bỏ enumeration theo từng biến thể → chỉ 1 dòng / giá trị "Nguồn" |
| 3 | Server Script `hkled_resolve_bom_qty` chứa toàn bộ công thức số lượng |
| 5 | Cập nhật nút "Tạo Rule"; tích hợp vào flow "Tạo BOM tự động" |

**Quyết định kiến trúc quan trọng của tài liệu**: công thức **nằm trong Frappe Server Script**,
không nằm trong code app — vì công thức thay đổi thường xuyên và HKLED cần sửa có hiệu lực
ngay, không build/deploy lại app.

### 1.2 Đối chiếu tài liệu với dữ liệu thật trên site (BẮT BUỘC — bài học Phần I/II/III)

Trước khi viết code đã audit site `hkled.com`. Kết quả **lệch tài liệu ở 4 điểm**:

| # | Tài liệu nói | Dữ liệu thật trên site | Xử lý |
|---|---|---|---|
| 1 | Đặc tính điều kiện tên `Loại nguồn` | **Không tồn tại** `Loại nguồn`. Đặc tính đúng tên là **`Nguồn`** (12 giá trị, trong đó 7 giá trị "nguồn to" khớp CHÍNH XÁC chuỗi trong tài liệu) | Dùng `Nguồn`. Đây chính là mục 4.4 tài liệu yêu cầu "đối chiếu lại khi implement" |
| 2 | 199 Item Template | **310** Item Template (`has_variants=1`) | Trong đó 277 là đèn thật chia đúng 6 nhóm, 23 là phụ kiện (bulong/ecu/long đen/vít/xốp/hộp carton) không cần nhóm |
| 3 | 6 nhóm phủ hết | **Còn 10 Item Template đèn thật KHÔNG thuộc nhóm nào** (xem mục 4) | Chưa có công thức → chặn tạo BOM Template cho 10 mã này, chờ HKLED |
| 4 | — | **Server Script đang TẮT** trên bench (`server_script_enabled` chưa bật) | Đã bật (xem mục 3.4) |

Kiểm tra an toàn đã làm trước khi code:
- `BOM Rule Group` chưa tồn tại → tạo mới, không trùng.
- `BOM Template` / `BOM Rule` / `BOM Component Table` có DocType nhưng **0 bản ghi dữ liệu** →
  đổi cấu trúc `BOM Rule` (xoá 2 field) **không làm mất dữ liệu nào**.
- Site có 3 BOM + 3 Work Order, đều trỏ vào item test cũ (`NVL 1..3`, `Thành phẩm 1/2`,
  `Bán thành phẩm 1/2`), **không phải item đèn thật** → engine mới không đụng tới.

### 1.3 Phân bố Item Template thật theo nhóm công thức

| rule_group | Prefix mã | Số Item Template | Số biến thể | Công suất thật đang dùng (W) |
|---|---|---|---|---|
| P01_P03 | DP01, DP02, DP03 | 145 | 17.184 | 10…1500 (16 mốc) |
| D01_D05 | DD01, DD02, DD03 | 54 | 6.480 | 50…300 |
| PTX | DPTC, DPTR, DPTV, DPKD | 33 | 4.144 | 10…600 |
| XHB | DXHB | 8 | 1.152 | 50…400 |
| DQL | DDQL | 7 | 896 | 30…250 |
| D11_D15 | DD11…DD15 | 30 | 4.320 | 50…300 (khớp đúng bảng tra rời rạc) |
| **(chưa có nhóm)** | DNU1, DX01 | **10** | — | 50…250 |

Ghi chú: tài liệu viết nhóm `D01_D05` và `PTX` gồm cả D04/D05 và PXH/PVL, nhưng site
**không có** Item Template nào mang các prefix đó — mapping vẫn khai đủ để sau này thêm không cần sửa code.

### 1.4 Cập nhật sau khi restore dữ liệu khách (31/07, lần 2)

Site được restore bản backup khách mới hơn. Đã audit lại toàn bộ + chạy lại 57 assertion
công thức và 2 ca end-to-end — **tất cả PASS**, không phải sửa code. Thay đổi dữ liệu:

- Item: 35.713 → **37.053**. Item Template: 310 → **711**.
- **401 template mới toàn NVL/bán thành phẩm** (vỏ đèn `VD*`, `PCB-`, `PKG-`, chip `C28D/C30D/C50D`,
  module `M30S/M50S`, `NGUỒN*`, `SPD-`, `WPC-`, đóng gói `PTN-/PHN-`…) — **không cần nhóm công thức**,
  không trùng prefix với 6 nhóm đèn nên `suggest_rule_group` không gợi ý nhầm.
- 6 nhóm đèn thành phẩm **giữ nguyên y hệt**: 277 template / 34.176 biến thể, mốc công suất từng nhóm
  không đổi (D11_D15 vẫn đúng 6 mốc bảng tra; P01_P03 vẫn có 600W chạm khoảng trống 500–600).
- Các vấn đề mục 4 **còn nguyên**: 10 template đèn `DNU1*`/`DX01*` chưa có nhóm; `DDQLC080` vẫn thiếu
  `Công suất`; `DP02S010/020/030` vẫn thiếu `Kiểu lắp`; không có giá trị `Nguồn` mới/lạ nào.
- ⚠️ **Cờ `server_script_enabled` bị mất một lúc quanh thời điểm restore** — engine chặn đúng với
  thông báo hướng dẫn (khớp test case D11). Đây là bằng chứng thật cho lưu ý deploy: **sau mỗi lần
  restore/dựng lại bench phải kiểm tra lại cờ này** (`bench set-config -g server_script_enabled 1`).

---

## 2. GIAI ĐOẠN DEV — DocType & Custom Field

### 2.1 DocType mới: `BOM Rule Group` (Nhóm Công Thức)

`mbwnext_hkled/mbwnext_hkled/doctype/bom_rule_group/`

| Field | Type | Ràng buộc |
|---|---|---|
| `rule_group_code` | Data | Mandatory, Unique, `autoname = field:rule_group_code` |
| `mo_ta` | Data | Mô tả |

Quyền: System Manager (full), Manufacturing Manager (không delete) — giống `Employee Level`.

6 bản ghi nạp qua patch `seed_bom_rule_group`: `P01_P03`, `D01_D05`, `PTX`, `XHB`, `DQL`, `D11_D15`.

**Vì sao Link chứ không Select**: thêm nhóm mới = tạo 1 document, **không cần migrate**.

### 2.2 `BOM Template` — thêm `rule_group`

Link → `BOM Rule Group`, `reqd = 1`, `in_standard_filter = 1`, đặt sau `item_template`.

### 2.3 `BOM Component Table` — 3 loại thành phần

`component_type` options đổi thành `Cố Định\nSố Lượng Theo Công Thức\nTheo Rule`.

| Loại | Item | Qty | Ví dụ |
|---|---|---|---|
| Cố Định | nhập tay | nhập tay | Hộp carton, Xốp góc, Bộ vỏ đèn |
| **Số Lượng Theo Công Thức** *(mới)* | nhập tay | Server Script tính | Module, Ốc vít, Chip LED, Cầu đấu, Dây điện, Lens, Gioăng |
| Theo Rule | tra BOM Rule | Server Script tính | Nguồn |

Field `item`: `depends_on` / `mandatory_depends_on` đổi từ `== "Cố Định"` thành **`!= "Theo Rule"`**.
Field `qty` giữ nguyên `== "Cố Định"`. Nút `create_rule` giữ nguyên (chỉ hiện khi Theo Rule).

Controller `bom_component_table.py` thêm nhánh `Số Lượng Theo Công Thức`: bắt buộc `item`, xoá `qty`.

### 2.4 `BOM Rule` — bỏ enumeration theo biến thể

| | Trước | Sau |
|---|---|---|
| Fields | `item_to_manufacture`, `bom_component`, `item`, `qty` | `bom_component`, `condition_value`, `item` |
| Số dòng / template | 1 dòng / **biến thể** (tới hàng nghìn) | 1 dòng / **giá trị "Nguồn"** (~9 dòng) |

`condition_value` (Data, reqd) = giá trị đặc tính `Nguồn`, label "Giá Trị Điều Kiện (Nguồn)".

`bom_template.py` sửa theo:
- `validate_unique_rules`: key đổi từ `(item_to_manufacture, bom_component)` → **`(bom_component, condition_value)`**
- `validate_rule_items`: bỏ kiểm tra `item_to_manufacture` phải là biến thể (field đã xoá)

### 2.5 Danh mục `BOM Component` — 15 bản ghi

Bảng này **rỗng** trên site trước khi làm. Tên bản ghi phải khớp **CHÍNH XÁC** khoá trong
`COMPONENT_MAP` của Server Script — sai một dấu là engine không tra được công thức.
Đã nạp qua patch: 11 thành phần có công thức + `Nguồn` + 3 thành phần cố định mẫu.

---

## 3. GIAI ĐOẠN DEV — Logic

### 3.1 Server Script `hkled_resolve_bom_qty` (API)

- Bản gốc để review/diff trong git: `mbwnext_hkled/server_scripts/bom_qty.py` (biến `SCRIPT`)
- Cài lần đầu qua patch `create_bom_qty_server_script`
- **Patch cố ý KHÔNG ghi đè script đã tồn tại** — nếu ghi đè thì mỗi lần `bench migrate` sẽ xoá
  sạch công thức HKLED vừa sửa, phá đúng mục đích đặt logic ở Server Script

Tham số vào: `item_code`, `component_name`, `rule_group`, `bom_template`.
Trả về qua `frappe.flags.result` = `{"qty": n}` hoặc `{"item": ..., "qty": n}` (khi là `Nguồn`).

Toàn bộ công thức giữ **đúng** như tài liệu mục 3, chỉ khác 3 điểm (đều là sửa lỗi/bảo vệ):

1. `attrs.get("Loại nguồn")` → **`attrs.get("Nguồn")`** (tên đặc tính thật, mục 1.2)
2. **Chặn tính sai âm thầm**: thiếu đặc tính `Công suất` → `frappe.throw`, không cho ra số vô nghĩa.
   Thực tế có 1 template `DDQLC080` (80W theo tên mã) **chưa khai `Công suất`** → nếu không chặn,
   `flt(None)=0` và mọi công thức trả về số của "0W".
3. **Chặn thiếu `Kiểu lắp`** với nhóm `P01_P03` khi công suất > 50W (nhóm này phân biệt Dọc/Ngang
   từ mốc trên 50W). 3 template `DP02S010/020/030` không khai `Kiểu lắp` nhưng đều ≤ 30W nên
   không ảnh hưởng — cả 2 nhánh Dọc/Ngang đều cho cùng kết quả ở mức ≤ 50W.

Trả kết quả qua `frappe.flags` **chứ không phải `frappe.response`**: `frappe.response` không luôn
tồn tại trong sandbox (background job / console), còn `frappe.flags` dùng được cho cả 2 đường gọi
(HTTP `/api/method/hkled_resolve_bom_qty` và Python `run_script(...)`).

### 3.2 Tích hợp vào flow "Tạo BOM Tự Động" (`api/bom.py`)

`resolve_components()` xử lý 3 loại thành phần; `Cố Định` đọc trực tiếp, 2 loại còn lại gọi
`resolve_qty_by_formula()` → Server Script.

**Quy tắc bổ sung (tài liệu không nêu, nhưng bắt buộc)**: công thức trả về **0 thì BỎ HẲN dòng**
khỏi BOM, không thêm với qty = 0 — vì `BOM Item` không nhận qty = 0, và 0 ở đây có nghĩa nghiệp vụ
là "biến thể này không dùng thành phần đó". Các trường hợp thật cho ra 0: Cầu đấu ≤ 50W,
Dây điện cấp nguồn (P01_P03 Dọc ≤ 50W / Ngang ≤ 100W), Dây điện đấu chip (PTX nguồn nhỏ,
DQL < 100W, D11_D15 ở 50W).

Có kiểm tra chặn thân thiện khi Server Script bị tắt hoặc chưa cài, kèm câu lệnh cần chạy.

### 3.3 Client — `controllers/js/bom_template.js`

Viết lại hoàn toàn (bỏ popup 2 bước sinh ma trận biến thể cũ):

- Nút **Tạo Rule** → dialog "Tạo Rule — Chọn NVL theo Nguồn": 1 dòng Link Item cho **mỗi giá trị
  `Nguồn` đang thực sự được dùng bởi biến thể của item cha** (không phải toàn bộ giá trị khai trong
  Item Attribute), điền sẵn NVL đã chọn trước đó nên dùng lại được để sửa. Bỏ trống = không tạo dòng.
- **Gợi ý `rule_group`** theo prefix mã Item Template khi chọn Mặt Hàng Cha (chỉ điền khi đang trống,
  người dùng sửa được) — thực hiện việc "gán rule_group cho Item Template" ở checklist tài liệu mục 5.

Server helper mới trong `bom_template.py`: `get_rule_condition_values()`, `suggest_rule_group()`.
Đã **xoá** 2 helper chết `get_template_attributes()`, `get_matching_variants()` (chỉ phục vụ cách
enumeration cũ mà tài liệu mục 2.4 nói "không dùng được nữa").

### 3.4 Thay đổi cấu hình bench — ĐỌC KỸ

```bash
bench set-config -g server_script_enabled 1
```

Frappe **chỉ cho bật Server Script ở `common_site_config.json`**, không bật riêng từng site → cờ này
có tác dụng cho **toàn bench** (`ailinh.com`, `tamdaimoc.com`, `mbw.com`, `hkled.com`).
Không có rò rỉ dữ liệu giữa khách (document Server Script là dữ liệu riêng từng site), nhưng
**khi lên production phải bật lại cờ này**, nếu không tính năng Tạo BOM Tự Động sẽ báo lỗi.

### 3.5 Bản dịch (bổ sung 31/07 — trước đó bị bỏ sót)

Ban đầu bỏ qua với lý do "label đã viết thẳng tiếng Việt" — **chưa đủ**: tên DocType
("BOM Rule Group", "Employee Level"…) vẫn hiện tiếng Anh trên breadcrumb/list view/nút Add
với người dùng chọn ngôn ngữ Tiếng Việt. Đã bổ sung:

- `locale/main.pot` + `locale/vi.po` (lần đầu của app, phủ cả Phần I lẫn II/III): dịch tên
  DocType (BOM Rule Group → Nhóm Công Thức, Employee Level → Bậc Thợ, Employee Allocation →
  Phân Công Nhân Sự, Employee Schedule → Lịch Làm Việc Nhân Sự, Work Order Employee → Nhân Công
  Tham Gia…), 2 description `= Date + Start/End`, và đổi tiền tố "Row #{0}" → "Dòng #{0}"
  trong 11 thông báo lỗi. "BOM Template" giữ nguyên theo đúng chữ khách dùng trong tài liệu.
- Lệnh: `bench generate-pot-file` → `bench create-po-file vi` → dịch → **`bench compile-po-to-mo`**
  (không chỉ update-po-files) → clear-cache. Đã verify `_()` trả đúng với lang=vi.
- Lưu ý: site đang để System Settings language = `en` và user chưa ai đặt `vi` — bản dịch chỉ
  hiện khi người dùng chọn Tiếng Việt. Việc đổi ngôn ngữ mặc định site là quyết định của khách.

---

## 4. Vấn đề cần HKLED xác nhận (chưa giải quyết)

Giữ nguyên 7 vấn đề ở mục 4 tài liệu gốc, **cập nhật thêm bằng số liệu thật**:

1. **Khoảng trống 500W–600W** ở "Dây điện cấp nguồn" nhóm `P01_P03` Kiểu lắp Ngang — code tạm gán 100.
   ➜ Site **có** biến thể 600W nhóm này, nên đây là khoảng trống chạm dữ liệu thật, không phải giả thiết.
2. **"Dây điện đấu chip" nhóm `D11_D15`** là bảng tra rời rạc (50/100/150/200/250/300W).
   ➜ Đã kiểm tra: công suất thật của nhóm này **đúng bằng 6 mốc đó**, chưa có mốc lạ. Tạm thời an toàn.
3. **Quy tắc làm tròn** — đang dùng `ceil`. Cần HKLED xác nhận.
4. **Chuỗi giá trị attribute** — ĐÃ ĐỐI CHIẾU: đặc tính đúng là `Nguồn`, `Kiểu lắp` = "Dọc"/"Ngang",
   `Công suất` là số không đơn vị. ⚠️ Còn 5 giá trị `Nguồn` **chưa được phân loại rõ trong công thức**:
   `HKLED Nguồn tròn`, `Philips Nguồn tròn`, `Suncom Nguồn tròn` (hiện rơi vào nhóm "nhỏ" theo mặc định),
   và `HKLED Nhỏ`, `Done Nhỏ` (đúng là "nhỏ"). Hiện **không có biến thể đèn nào dùng 3 giá trị "Nguồn tròn"**
   nên chưa gây sai, nhưng cần HKLED xác nhận trước khi có sản phẩm dùng tới.
5. **Phân nhóm toàn bộ Item Template** — ĐÃ ĐẾM TRÊN ERPNEXT: 310 template, 277 đèn chia đúng 6 nhóm,
   23 phụ kiện không cần nhóm. ⚠️ **Còn 10 template đèn thật chưa có nhóm công thức nào**:
   - `DNU1C050/100/150/200/250` — Đèn LED phòng nổ UFO NU1 Chip LED COB
   - `DX01S050/100/100-C/150/200` — Đèn LED nhà xưởng UFO X01 Chip LED SMD

   ➜ Đây đúng là "nhóm thứ 7" mà tài liệu mục 4.5 lo ngại. **Không tự suy công thức**. Hiện trạng:
   `rule_group` là field bắt buộc nên không tạo được BOM Template cho 10 mã này → hệ thống chặn
   thay vì tính sai. Cần HKLED cung cấp công thức (hoặc xác nhận 10 mã này dùng chung công thức
   của nhóm `XHB`, vì đều là đèn nhà xưởng/UFO — **chỉ là phỏng đoán, chưa áp dụng**).
6. **Nhóm PTX không có danh sách biến thể trong Excel** — ĐÃ LẤY TỪ ERPNEXT: 33 template / 4.144 biến thể
   (prefix DPTC, DPTR, DPTV, DPKD). Tương tự XHB (8), DQL (7), D11_D15 (30). Vấn đề này **đã xử lý xong**.
7. **Bug nhóm `D11_D15`** đã sửa trong tài liệu — code implement theo bản đã sửa.

**Phát hiện thêm khi implement (chưa có trong tài liệu):**

8. **`DDQLC080` chưa khai đặc tính `Công suất`** (tên mã hàm ý 80W). Lỗi dữ liệu master, không phải lỗi code.
   Hiện engine báo lỗi rõ ràng thay vì tính theo 0W. Cần HKLED bổ sung giá trị `Công suất` cho template này —
   lưu ý 80 **chưa có** trong danh sách giá trị của Item Attribute `Công suất`, phải thêm giá trị trước.
9. **`DP02S010/020/030` chưa khai `Kiểu lắp`** — không ảnh hưởng vì đều ≤ 30W (Dọc/Ngang cho cùng kết quả),
   nhưng nên bổ sung cho nhất quán.

---

## 5. Checklist tài liệu mục 5 — trạng thái

- [x] Đối chiếu công thức với dữ liệu Excel gốc *(đã làm ở bước trước, 2026-07-29)*
- [x] Gán `rule_group` cho Item Template — làm bằng **gợi ý tự động theo prefix** khi tạo BOM Template
      (site chưa có BOM Template nào nên không có gì phải gán ngược lại)
- [x] Cập nhật nút "Tạo Rule" sinh dòng `BOM Rule` theo distinct "Nguồn"
- [x] Tích hợp `hkled_resolve_bom_qty` vào flow "Tạo BOM tự động"
- [x] Viết test case cho từng `rule_group` × mốc công suất biên → `apps/mbwnext_hkled/docs/testcases/bom-template-theo-bien-the.md`
- [x] Lấy danh sách Item/biến thể nhóm PTX/XHB/DQL/D11_D15 → lấy từ ERPNext (mục 1.3)
- [ ] **Xác nhận 9 vấn đề dữ liệu ở mục 4 với HKLED trước khi go-live** *(còn mở — cần khách trả lời)*

---

## 6. Kết quả tự test (Claude chạy trên dev)

| Bộ test | Kết quả |
|---|---|
| Công thức từng thành phần × 6 nhóm × mốc công suất biên (14 ca, 57 assertion) | **57/57 PASS** |
| End-to-end `auto_create_bom` nhóm D11_D15 200W (10 dòng BOM) | **PASS** |
| End-to-end `auto_create_bom` nhóm P01_P03 50W — kiểm tra bỏ dòng qty = 0 | **PASS** |
| UI: danh mục 6 Nhóm Công Thức, field Nhóm Công Thức, gợi ý theo prefix, dialog Tạo Rule | **PASS** (kiểm bằng trình duyệt thật) |

Dữ liệu test dùng NVL tiền tố `ZZTEST-NVL-*` tạo mới rồi xoá sạch — **không đụng item thật**.
Sau test: site còn đúng 3 BOM ban đầu, 0 BOM Template, 0 item ZZTEST.

**⚠️ Vẫn cần người test tay lại qua UI thật** — đây là bước bắt buộc, đã 2 lần bắt được lỗi mà
Claude tự test không thấy (xem `apps/mbwnext_hkled/CLAUDE.md`).

## 7. Khai báo trên app PM (31/07/2026)

Đã khai vào tab **Doctype** / **Trường tùy chỉnh** của `PM-PRJ-00003`:

| Loại | Số lượng | Ghi chú |
|---|---|---|
| DocType | 9 | `BOM Rule Group` là **MỚI** của tính năng này; 4 DocType Phần I bị **sửa** (BOM Template thêm `rule_group`; BOM Component Table thêm loại thứ 3; BOM Rule đổi cấu trúc; BOM Component nạp 15 bản ghi) |
| Custom Field | 11 | Tính năng này **không thêm Custom Field nào** — `rule_group` là field trong DocType riêng của app, không phải Custom Field. 11 dòng là toàn bộ Custom Field sẵn có của dự án (Phần I/II/III) |

## 8. Lệnh triển khai

```bash
bench set-config -g server_script_enabled 1     # BẮT BUỘC, toàn bench
bench --site hkled.com migrate                  # tạo DocType + nạp danh mục + cài Server Script
bench build --app mbwnext_hkled
```
