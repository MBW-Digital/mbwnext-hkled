# MBWNext HKLed

App Frappe/ERPNext triển khai "Tài liệu nghiệp vụ nâng cấp giai đoạn 1 HKLED" (công ty sản xuất đèn LED): tự động sinh BOM đa cấp theo biến thể sản phẩm (Phần I), quản lý bậc thợ/giờ công chuẩn (Phần II), và lịch sản xuất thông minh tự động tính thời gian hoàn thành Lệnh sản xuất theo nhân công (Phần III).
Site: `hkled.com` trên bench `/home/mbw/mbw-dev/cozy_dev` (xem mục *Cách chạy* để biết cổng).
Repo: remote `upstream` = `https://github.com/MBW-Digital/mbwnext-hkled.git`.

## Cấu trúc thư mục

```
mbwnext_hkled/
├── api/
│   ├── bom.py                          # Engine tự động tạo BOM đa cấp (Phần I)
│   ├── work_order_schedule.py          # Engine tính lịch sản xuất (Phần III) — phần lõi phức tạp nhất
│   ├── work_order_actions.py           # Nút "Bắt Đầu Sản Xuất" (GAP-3)
│   ├── work_team.py                    # Nhân sự theo đội + tạo nhanh lịch hàng loạt (GAP-2, GAP-6)
│   ├── production_plan.py              # Nút Kế Hoạch Sản Xuất trong Create của Đơn Bán (PM-TASK-00047)
│   └── employee_timeline.py            # Dữ liệu Biểu đồ tình hình làm việc (PHẦN V)
├── server_scripts/
│   └── bom_qty.py                       # BẢN GỐC của Server Script hkled_resolve_bom_qty (công thức số lượng NVL)
├── controllers/
│   ├── python_hook/
│   │   ├── work_order.py               # doc_events: dọn/đồng bộ Allocation, thừa hưởng từ PP, chia sản lượng, Khách Hàng + NV Bán Hàng
│   │   ├── production_plan.py          # doc_events: Thời Điểm Cần Hoàn Thành (GAP-4) + Ghi Chú Sản Xuất
│   │   ├── sales_order.py              # doc_events: Ghi Chú Sản Xuất chảy xuống dòng hàng (PM-TASK-00046)
│   │   ├── employee.py                 # doc_events: chặn Công nhân thiếu Bậc Thợ ở SERVER (C1)
│   │   └── stock_entry.py              # doc_events: sinh serial khi Finish (GAP-7)
│   └── js/
│       ├── bom.js                       # Chọn Mặt Hàng trên BOM -> điền sẵn NVL từ BOM Template
│       ├── bom_template.js              # Dialog "Tạo Rule" (chọn NVL theo tổ hợp đặc tính)
│       ├── production_plan.js           # Nút "Tạo BOM Tự Động" trên Production Plan Item
│       ├── sales_order.js               # Nút Kế Hoạch Sản Xuất + Ghi Chú Sản Xuất (PM-TASK-00046/47)
│       ├── employee.js                  # Cảnh báo khi Công nhân chưa gán Bậc Thợ (C1)
│       ├── employee_schedule_list.js     # Dialog "Tạo Nhanh" lịch theo đội (GAP-2) — LIST VIEW
│       ├── other_task.js                 # Kiểm tổng thời gian Công Việc Khác (GAP-8)
│       └── work_order.js                # Nút Tính Lại Lịch / Bắt Đầu Sản Xuất / Thêm Đội Sản Xuất
├── data/
│   ├── nhap_item.py                     # bộ nạp danh mục vật tư + Phương pháp bổ sung (PM-TASK-00061/67)
│   ├── danh_muc/*.csv                   # 12 sheet nguồn, chép nguyên xi từ bảng khách gửi
│   ├── thanh_pham/*.csv                 # 4 file Nhóm I–IV, 59.023 đèn thành phẩm, ĐỦ CỘT (PM-TASK-00126)
│   ├── doc_bom_sheet.py                 # ĐỌC file Excel BOM Template của khách -> spec.json (PM-TASK-00110)
│   ├── nhap_bom_template.py             # spec.json -> BOM Template + BOM Rule, có mô phỏng khớp trước khi ghi
│   └── bom_template/spec.json           # đặc tả 7 sheet đã đọc — bản trong git, diff được khi khách sửa file
├── patches/                             # 22 patch, chạy post_model_sync — xem "Dựng site từ số 0"
│   ├── add_production_plan_bom_button.py       # Custom Field "Tạo BOM Tự Động" trên Production Plan Item
│   ├── adjust_work_order_schedule_fields.py    # reqd/allow_on_submit cho field lịch trên Work Order
│   ├── rename_time_to_manufacture_field.py     # sửa lỗi chính tả custom_time_to_manufature -> ...manufacture
│   ├── set_custom_field_module.py              # gán module=MBWNext HKLed cho custom field để export-fixtures
│   ├── seed_bom_rule_group.py                  # nạp 6 Nhóm Công Thức + 15 BOM Component (nhóm sau đã bỏ)
│   ├── create_bom_qty_server_script.py         # cài Server Script hkled_resolve_bom_qty (KHÔNG ghi đè nếu đã có)
│   ├── add_work_team_fields.py                 # GAP-1: Employee.custom_work_team + ràng buộc Bậc Thợ (C1)
│   ├── add_sales_order_schedule_fields.py      # GAP-4: field trên Sales Order / Production Plan
│   ├── add_work_order_production_fields.py     # GAP-3 + GAP-7: cờ Đã Bắt Đầu + bảng Sản Lượng
│   ├── grant_production_read_on_employee.py    # cấp quyền ĐỌC Employee cho vai trò sản xuất
│   ├── migrate_bom_rule_cond_attrs.py          # BOM Rule sang cond_attrs, bảng bom_rule -> bom_rules
│   ├── drop_bom_rule_group.py                  # xoá DocType BOM Rule Group (chốt TungDA 07/08)
│   ├── cleanup_cancelled_work_order_allocations.py  # PM-TASK-00045: dọn Phân Công của lệnh đã huỷ
│   ├── add_production_note_fields.py           # PM-TASK-00046: Ghi Chú Sản Xuất các cấp
│   ├── add_work_order_sales_info.py            # PM-TASK-00050: Khách Hàng + NV Bán Hàng trên Lệnh sản xuất
│   ├── backfill_work_order_start_time.py       # lấp custom_start_time trống của lệnh cũ
│   ├── set_document_naming_series.py           # PM-TASK-00054: mã chứng từ riêng HKLED
│   ├── import_danh_muc_vat_tu.py               # PM-TASK-00061: nạp 12 sheet danh mục vật tư
│   ├── add_item_replenishment_method.py        # PM-TASK-00067: trường Phương pháp bổ sung trên Item
│   └── import_bom_template.py                  # PM-TASK-00110: nạp BOM Template từ file khách
├── fixtures/
│   ├── custom_field.json                # 30 Custom Field (Item/Employee/Sales Order/Production Plan/Work Order)
│   └── property_setter.json             # 19 Property Setter — mã chứng từ 9 loại phiếu (PM-TASK-00054)
├── locale/
│   ├── main.pot                         # bench generate-pot-file --app mbwnext_hkled
│   └── vi.po                            # dịch tên DocType + "Row #"→"Dòng #"; nhớ bench compile-po-to-mo
├── docs/                                # 4 giai đoạn: features / mockups / testcases / huong-dan
├── mbwnext_hkled/                       # Module chính (module: "MBWNext HKLed")
│   ├── page/
│   │   └── bieu_do_lich_lam_viec/       # PHẦN V — Desk Page biểu đồ tình hình làm việc
│   ├── workspace/
│   │   └── hkled/                       # Workspace "HKLed" gom màn hình của dự án
│   └── doctype/
│       ├── work_team/                   # PHẦN III — Đội Sản Xuất (GAP-1)
│       ├── employee_production/         # PHẦN IV — child table Sản Lượng Nhân Viên (GAP-7)
│       ├── other_task/                  # PHẦN IV — Công Việc Khác (GAP-8)
│       ├── other_task_table/            # PHẦN IV — child table nhân công của Công Việc Khác
│       ├── bom_component/               # PHẦN I — danh mục thành phần BOM
│       ├── bom_component_table/         # PHẦN I — child table: bảng thành phần BOM Template
│       ├── bom_rule/                    # PHẦN I — child table: chọn NVL theo tổ hợp đặc tính (cond_attrs)
│       ├── bom_template/                # PHẦN I — 2 tab: Thông Tin Chính / Công Thức Thành Phần
│       ├── employee_level/              # PHẦN II — Bậc Thợ
│       ├── employee_schedule/           # PHẦN III — lịch làm việc hàng ngày
│       ├── employee_allocation/         # PHẦN III — phân công nhân sự vào Work Order
│       └── work_order_employee/         # PHẦN III — child table trên Work Order
├── hooks.py
├── modules.txt                          # Module: MBWNext HKLed
└── patches.txt
```

## PHẦN I — BOM Template (tự động sinh BOM theo biến thể)

### Doctype
| Doctype | Loại | Vai trò |
|---|---|---|
| **BOM Component** | Master data | Danh mục tên thành phần BOM. **Tên bản ghi phải khớp CHÍNH XÁC khoá `COMPONENT_MAP` trong Server Script** — sai một dấu là không tra được công thức |
| **BOM Component Table** | Child table | Khai báo thành phần cần có trong 1 BOM Template — **2 kiểu**: `Cố Định` (item+qty nhập tay), `Theo Rule` (cả item lẫn qty tự xác định). ⚠ Kiểu thứ ba `Số Lượng Theo Công Thức` **đã bỏ** (Thắng chốt 26/08), gỡ khỏi mã nguồn 27/08 sau khi migrate đưa 4 dòng cuối cùng về `Theo Rule` |
| **BOM Rule** | Child table | Ánh xạ `(BOM Component, tổ hợp giá trị đặc tính) -> NVL`, điều kiện lưu ở `cond_attrs` dạng JSON `[{"name": "Nguồn", "values": [...]}]`. **Không** enumerate theo biến thể — ~9 dòng/template thay vì hàng nghìn |
| **BOM Template** | Doctype chính | Gắn với 1 Item Template (`Has Variants=1`), 2 tab: Bảng Thành Phần BOM + Công Thức BOM. Chỉ 1 template được `Hoạt Động` / item cha |

⚠ **`BOM Rule Group` và field `rule_group` đã bị BỎ** (chốt của TungDA 07/08 trên PM-FEAT-00007).
Khoá tra công thức giờ là **Mặt Hàng Cha**, bảng suy nhóm nằm trong Server Script `hkled_resolve_bom_qty`
— người dùng không còn phải tự chọn nhóm. Hai patch `migrate_bom_rule_cond_attrs` và
`drop_bom_rule_group` lo phần chuyển đổi. Tên nhóm (`P01_P03`, `D01_D05`…) vẫn còn **bên trong**
Server Script, chỉ là không còn DocType nào lưu chúng.

### Công thức số lượng NVL nằm ở Server Script — KHÔNG ở code app

Server Script API `hkled_resolve_bom_qty`. Đây là **quyết định nghiệp vụ, không phải tuỳ tiện**:
công thức đổi thường xuyên, HKLED phải sửa có hiệu lực ngay, không build/deploy lại app.

- Bản gốc để review/diff: `mbwnext_hkled/server_scripts/bom_qty.py` (biến `SCRIPT`)
- Cài lần đầu qua patch `create_bom_qty_server_script`, **cố ý KHÔNG ghi đè nếu script đã tồn tại**
  (ghi đè = mỗi lần `bench migrate` xoá sạch công thức khách vừa sửa)
- **Bắt buộc bật cờ toàn bench**: `bench set-config -g server_script_enabled 1` — Frappe không cho
  bật riêng từng site. Lên production phải bật lại, không thì Tạo BOM Tự Động báo lỗi.

⚠️ **Cạm bẫy sandbox đã mắc**: RestrictedPython **chặn `.format()`** ("format is an unsafe attribute").
Trong Server Script phải dùng **f-string**. Ngoài ra: không `import`, tên hàm không bắt đầu bằng `_`,
trả kết quả qua **`frappe.flags`** (dùng được cho cả HTTP lẫn `run_script` từ Python) — **không** dùng
`frappe.response` vì biến này không luôn tồn tại trong sandbox (background job / console).

### Nạp BOM Template từ file khách (PM-TASK-00110)

Khách gửi 1 Google Sheet, mỗi sheet = 1 mặt hàng cha. Đường đi:

```
file .xlsx  --doc_bom_sheet.py-->  data/bom_template/spec.json  --nhap_bom_template.py-->  BOM Template
```

Tách hai bước có lý do: `spec.json` nằm trong git nên **diff được** khi khách sửa file — đợt
18/08 khách sửa 4 lần trong một ngày, không có bản diff thì không biết cái gì vừa đổi.

Chạy lại khi khách sửa file:

```bash
python -m mbwnext_hkled.data.doc_bom_sheet <file.xlsx> > mbwnext_hkled/data/bom_template/spec.json
bench --site hkled.com execute mbwnext_hkled.patches.import_bom_template.execute
```

#### Bảy cách viết trong file khách — đọc sai là ra BOM sai mà không có gì báo

| Trong sheet | Nghĩa | Dựng thành |
|---|---|---|
| `Mọi biến thể đều chọn` | mọi biến thể dùng chung 1 NVL | 1 rule *Theo Rule*, điều kiện = một đặc tính chung, **tích đủ mọi giá trị** |
| `<Đặc tính>: <Giá trị>` (rule 1 dòng) | như trên nhưng có điều kiện | 1 rule; dòng kế tiếp cùng thành phần **bỏ trống cột đầu** |
| `tất cả` / `Tất cả` | không ràng buộc đặc tính đó | bỏ đặc tính khỏi điều kiện |
| `Còn lại` / `Các loại còn lại` | tổ hợp chưa bị rule phía trên chiếm | **liệt kê thẳng** các tổ hợp còn lại |
| `A và B` | nhiều giá trị trong một ô | OR các giá trị |
| `Không sử dụng` ở cột Mã NVL | biến thể đó không dùng thành phần này | 1 rule **tích ô `Không Sử Dụng`**, ô NVL để trống |

⚠ So khớp mấy chuỗi trên phải **KHÔNG phân biệt hoa thường** — khách viết cả `tất cả` lẫn
`Tất cả` trong cùng một sheet. Khớp cứng theo chữ thì rule thành điều kiện `Công suất = "Tất cả"`,
không biến thể nào có giá trị đó nên rule **chết lặng, không báo lỗi**.

⚠ `Còn lại` phải xét theo **tổ hợp nhiều đặc tính cùng lúc**, không xét từng đặc tính riêng.
DP01S/Module: rule trên chiếm (50W, Dọc) và (100W, Ngang); xét riêng thì *Kiểu lắp* còn lại là
**tập rỗng** — sai. Xét theo cặp thì còn 14 cặp, gom thành 2 rule.

⚠ Gặp cột điều kiện **điền dở** (một số dòng có giá trị, số khác trống) thì `doc_bom_sheet.py`
**`raise` và bỏ qua cả sheet**, không đoán. Cột trống hoàn toàn = đặc tính không dùng, bỏ qua.

#### Mô phỏng trước khi ghi — không ghi sheet nào còn cặp hỏng

`nhap_bom_template.kiem_khop()` thử khớp **từng cặp (biến thể × thành phần Theo Rule)** rồi mới
ghi, vì `find_rule_item` **throw** khi không rule nào khớp — một cặp hỏng = một BOM không tạo được.
Cặp không khớp chia ba nhóm, chỉ nhóm cuối chặn ghi:

- `co_y` — trùng tổ hợp khách ghi `Không sử dụng`
- `chua_co_du_lieu` — khai tường minh ở hằng số **`CHUA_CO_DU_LIEU`** (hiện: DP01S/DP03S ở 1200W
  và 1500W, khách chưa đặt sản xuất). Khách bổ sung thì **xoá mục đó đi**, bộ nạp tự đòi lại
- `hong` — thiếu ngoài dự kiến → **chặn ghi**

⚠ Đừng hạ ngưỡng kiểm để "cho chạy". Khai vào `CHUA_CO_DU_LIEU` thì chỗ thiếu ngoài dự kiến vẫn
bị chặn; nới `kiem_khop` thì mất luôn lưới an toàn.

#### `resolve_rules` cấm rule phủ trùng — chặt hơn engine lúc chạy

`BOMTemplate.resolve_rules` throw khi 2 rule cùng thành phần cùng phủ 1 biến thể, trong khi
`find_rule_item` chỉ lấy rule khớp **đầu tiên** theo `idx`. Nên **không dựng được** kiểu "rule cụ
thể ở trên, rule vét ở dưới" — đó là lý do `Còn lại` phải liệt kê tường minh.

Và `find_rule_item` lọc `if cond and variant_matches(...)`: rule **để trống điều kiện không bao
giờ khớp**. Không có khái niệm rule mặc định.

### Công thức cho module và vỏ (làm 22/08)

`PREFIX_GROUPS` thêm hai nhóm: **`MODULE_50`** (`M30S050*`, `M50S050*`) và **`VO_VDP0X`**
(`VDP0X`). Nguồn số liệu là **cột SL của chính sheet rule**, không phải 3 sheet *Nhóm I/II/III*.

**Module — 4/4 template chạy được** (112 biến thể, 0 hỏng). Hầu hết là số cố định (Chip LED 1,
Tản nhiệt 1, Lens 1, Gioăng chip 1, Ốc vít bắt chip 8, Ốc vít bắt lens 16); chỉ *Cầu đấu* và
*Ốc dây điện* đổi theo đặc tính **Kiểu đấu**:

| Kiểu đấu | Cầu đấu | Ốc dây điện |
|---|---|---|
| `Cầu đấu` | 1 | 0 |
| `Dây điện` | 30 | 1 |

⚠ File khách viết **"Dây diện"** (thiếu dấu). So theo giá trị THẬT trên biến thể, đừng chép
nguyên chuỗi trong file vào code.

⚠ Các hàm `calc_chip_led_qty`, `calc_lens_qty`, `calc_gioang_chip_qty`, `calc_oc_vit_bat_*`
viết cho **đèn thành phẩm** (chia theo công suất). Nhóm module phải rẽ nhánh riêng trả số cố
định — đây đúng là cái bẫy đã cảnh báo từ trước: áp nhầm công thức đèn sang module thì ra số
sai mà không có gì báo.

⚠ **Dòng khai "Cố Định" nhưng số lượng lại có điều kiện.** *Ốc dây điện* được khách khai
`Cố Định` mà SL là *"Kiểu đấu: Cầu đấu SL 0 | Kiểu đấu: Dây điện SL 1"* — mâu thuẫn: `Cố Định`
lấy thẳng ô Số Lượng, mà ô đó không điền được số nào đúng cho cả hai.

Bộ nạp **từng tự nâng lên `Số Lượng Theo Công Thức`** — **đã bỏ 26/08**. Gốc rễ hoá ra là đọc
nhầm bảng khách: chữ *"Theo rule"* của khách nghĩa là **số lượng** theo rule, còn `"Theo Rule"`
của hệ thống nghĩa là **NVL** theo rule. Bốn dòng đó nay khai thẳng `Theo Rule`, và `bom_qty.py`
vẫn ra đúng số vì `COMPONENT_MAP` được tra **trước** phần lấy số lượng từ dòng. Đừng dựng lại
phép tự nâng kiểu — xem chú thích trong `data/nhap_bom_template.py`.

**Vỏ VDP0X — 13/13 thành phần, 28/28 biến thể tạo được BOM (23/08).** Ba thành phần *Đế bắt
nguồn*, *Ốc vít bắt đế, hộp*, *Hộp nguồn* trước đây bị chặn vì bảng tính theo **loại nguồn và
hãng nguồn**, mà biến thể vỏ chỉ có 4 đặc tính (*Công suất · Màu sơn · Phân loại vỏ · Version*)
— cái vỏ không biết đèn lắp vào dùng nguồn gì. Đã báo Thắng, và **khách viết lại bảng bỏ hẳn
phụ thuộc vào nguồn**, giờ chỉ còn *Phân loại vỏ + Công suất*.

`vo_tra_bac()` khớp **nhánh đầu tiên thoả**, đúng thứ tự bảng khách — ca đặc biệt (Công suất 50,
Công suất 100) đặt TRƯỚC ngưỡng bao trùm, đảo thứ tự là ra số khác. Không nhánh nào thoả thì
throw nêu đích danh công suất: bảng liệt kê theo bậc rời rạc nên công suất mới sẽ rơi ra ngoài,
im lặng ở đây là BOM thiếu dòng. Đã kiểm 28/28 tổ hợp thật đều có nhánh phủ.

✅ `lambda` **chạy được** trong sandbox Server Script (đã thử thật) — khác với `.format()` và
`return` ở cấp module.

⚠ Dọc/Ngang của **vỏ** nằm ở đặc tính **`Phân loại vỏ`**, KHÔNG phải `Kiểu lắp` như đèn thành
phẩm. `vo_phan_loai()` đọc khoá đó và **chặn thẳng** nếu thiếu — đọc nhầm khoá thì mọi công thức
âm thầm rơi vào nhánh Ngang.

### ⚠ Một lỗ hổng engine còn lại (chờ TungDA — chốt của Thắng 18/08)

**1. Không có bộ công thức số lượng cho mặt hàng cha là module / vỏ.**
`resolve_formula_group` chỉ suy được theo tiền tố đèn thành phẩm (`DP01`, `DD01`…). `M30S050-A/B`,
`M50S050-A/B`, `VDP0X` không khớp tiền tố nào → throw *"chưa có bộ công thức số lượng"*, **0 biến
thể nào của 5 template đó tạo được BOM**. Script còn throw khi biến thể thiếu đặc tính `Công suất`,
mà biến thể module không có đặc tính này.
Đừng vá bằng cách thêm bừa vào `FORMULA_GROUP_BY_TEMPLATE`: `COMPONENT_MAP` đang có sẵn công thức
cho `Chip LED`, `Lens`, `Gioăng chip`… viết cho **đèn thành phẩm**, áp nhầm sang module thì ra số
sai mà không có gì báo.

**2. ✅ ĐÃ SỬA 21/08 — ô tích "Không Sử Dụng" trên BOM Rule.** *(chốt của Thắng 21/08)*

Trước: nhánh `component_type == "Theo Rule"` gọi `find_rule_item` và throw **trước** khối tính qty,
nên tổ hợp `Không sử dụng` **báo lỗi** thay vì bị bỏ dòng. Ảnh hưởng 640 biến thể mỗi sheet
DP01S/DP03S.

Đã cân nhắc hai hướng. **Không** chọn hướng "đảo thứ tự, tính qty trước rồi bỏ dòng khi qty ≤ 0":
hướng đó chỉ cứu được thành phần nào *tình cờ* có công thức trả 0, mà "không dùng" là do **khách
khai**, không có gì bảo đảm nó luôn trùng kết quả công thức.

Cách đang dùng — khai tường minh vào dữ liệu:

- `BOM Rule.khong_su_dung` (Check). Tích thì **bỏ trống** `item`.
- `item` **đã bỏ `reqd`** trên DocType. Ràng buộc KHÔNG mất, chuyển xuống
  `BOMTemplate.validate_rule_items`: chưa tích ô mà trống NVL → chặn; vừa tích ô vừa có NVL → chặn.
  ⚠ Sửa chỗ này phải giữ cả hai vế, bỏ `reqd` mà không bù là để lọt rule rỗng.
- `find_rule_item` trả **cả dòng rule**, không chỉ mã NVL — trả None thì không phân biệt được
  "khách khai không dùng" với "quên chưa đặt rule", hai thứ xử lý ngược nhau.
- Thân Server Script chạy ở **cấp module**, `return` là SyntaxError → thoát sớm bằng cờ `khong_dung`.
- `api/bom.py` **không phải sửa**: nhánh `qty <= 0: continue` có sẵn, dòng tự rụng.

Kết quả đo 21/08: 719 → **733 rule**, 16 dòng tích ô (đều ở *Cầu đấu* của DP01S/DP03S), nhóm `co_y`
trong `kiem_khop` từ 640 mỗi sheet về **0**. `DP01S050-3B3HT-AD` — ca Thắng nêu — giờ tạo được BOM
6 NVL, không có Cầu đấu. Mẫu 60 biến thể 200W vẫn đủ 8 NVL, không hồi quy.

### Công thức số lượng — bảng khách gửi 22/08 và 5 lỗi đã sửa

Nguồn chuẩn: Google Sheet *"công thức hoàn chỉnh"* Thắng gửi trên PM-TASK-00110 (22/08).
Sheet phủ **2 nhóm**: đèn pha P01–P03 (tức `DP01S`/`DP03S`) và đèn đường D01–D0x.
**Không** phủ module/vỏ — mục đó vẫn treo.

Đối chiếu 160 tổ hợp thật (Công suất × Kiểu lắp × Nguồn × Kiểu nguồn) của DP01S, đã sửa:

1. **Dây điện cấp nguồn bỏ sót điều kiện loại nguồn** — 98/160 tổ hợp. Trong sheet, cả cây
   Dọc/Ngang nằm dưới ô gộp `C37:C43 = "Nguồn nhỏ"`; *Nguồn to điện áp thấp/cao* đều **0**
   (dây đi kèm nguồn, không tính vào BOM đèn). Bản cũ không xét loại nguồn → cấp thừa dây.
2. **Thiếu nhánh chia hết cho nguồn to HKLED ở Kiểu lắp Ngang** (Nguồn + Cầu đấu).
   Sheet: ≤100 → 1/0 · ≤600 → 2 · rồi %300 → %250 → %200.
3. **Sai thứ tự ưu tiên chia hết cho nguồn to hãng khác ở Ngang**: đúng là **250 → 150 → 200**,
   bản cũ là 250 → 200 → 150. ⚠ Hai nhánh Ngang có thứ tự ƯU TIÊN KHÁC NHAU — đừng gộp cho
   gọn: 1200W ra 8 với 250/150/200 nhưng ra 6 với 250/200/150.
4. **Xốp góc = 4** (bản cũ 1). Đèn đường dùng thành phần tên khác: *Xốp chèn* = 2.
5. **Phân loại nguồn suy sai từ tên hãng.** Site có sẵn đặc tính **`Kiểu nguồn`** với đúng ba
   giá trị sheet dùng (*Nguồn nhỏ* / *Nguồn to điện áp thấp* / *Nguồn to điện áp cao*), có ở
   55 mặt hàng cha. Bản cũ suy trục nhỏ/to từ danh sách tên hãng hard-code nên
   **"Năng lượng mặt trời"** (Kiểu nguồn = *to điện áp thấp*) rơi nhầm vào *nhỏ* — 512 biến
   thể mỗi template tính sai cả Nguồn, Cầu đấu lẫn Dây điện. Nay trục nhỏ/to lấy từ
   `Kiểu nguồn`; chỉ trục HKLED-hay-hãng-khác mới đọc tên hãng, vì sheet tách theo hãng.

⚠ **Số cố định cũng để trong `COMPONENT_MAP`, đừng để ở ô Số Lượng của dòng thành phần.**
File khách để trống ô SL, bộ nạp buộc phải điền giá trị dự phòng, và giá trị đó đi thẳng vào
BOM. Xốp góc sai đúng kiểu đó — dự phòng 1 trong khi bảng ghi 4, và **không có gì báo**: cảnh
báo `qty_defaulted` chỉ bắn khi qty ≤ 0, mà bộ nạp lại ghi 1. Đã đổi bộ nạp ghi **0** cho ô SL
trống để cảnh báo bắn được.

⚠ **Bẫy khi tự kiểm: đừng nhận diện thành phần bằng tiền tố mã NVL.** `WPC-` vừa là Cầu đấu
(`WPC-MDF-…`) vừa là Nguồn của biến thể năng lượng mặt trời (`WPC-SLM-…`). Đếm bằng tiền tố ra
số sai. Hỏi engine theo **tên thành phần** (`resolve_qty_by_formula(ma, "Cầu đấu", …)`).

⚠ **Bộ đối chiếu phải để hai phía phân loại độc lập.** Bản đầu của hàm so sánh gọi chung
`classify_nguon` cho cả phía code lẫn phía bảng khách, nên **không thể** phát hiện lỗi số 5 —
báo "khớp hết" trong khi đang sai. Gieo thử một lỗi vào phía code để chắc bộ đối chiếu biết kêu.

**Thắng trả lời chiều 22/08** — bảng đổi cấu trúc, *Sheet 1* tách thành **Nhóm I (Module)**,
**Nhóm II (COB)**, **Nhóm III (Chip Module)**:

| Hỏi | Trả lời | Đã làm |
|---|---|---|
| 500 < CS ≤ 600 ở Ngang | mốc là **500 < CS ≤ 1000 → 200** | đã sửa, bỏ nhánh TODO |
| *"Công suất 100"* | đúng là **≤ 100** | code vốn đã đúng |
| Cầu đấu, nguồn nhỏ | đi **chung nhánh hãng khác** (khách liệt kê tường minh *HKLED Nhỏ*, *Done Nhỏ*, *Năng lượng mặt trời* vào cùng ô) | code vốn đã đúng |
| *Năng lượng mặt trời* | với **Nguồn** là dòng riêng, **1 phẳng** — không theo Kiểu lắp, không theo Công suất | đã sửa |
| **Công thức module/vỏ** | ❌ **VẪN CHƯA CÓ** | 5/7 template vẫn treo |

⚠ *"Năng lượng mặt trời"* nằm **dưới nhánh Nguồn to**, nên chỉ riêng thành phần **Nguồn** là đặc
biệt: Cầu đấu vẫn đi chung nhóm hãng khác, Dây điện cấp nguồn vẫn ra 0. Đừng nâng nó thành một
nhóm phân loại riêng trong `classify_nguon` — sẽ sai hai thành phần kia.

⚠ **Thắng bổ sung 4 nhóm đèn thành phẩm mới, KHÔNG phải module/vỏ.** Nhóm II phủ đèn pha
PTC/PTR/PXH/PTV/PVL/PKD, nhà xưởng XHB, **phòng nổ UFO NU1**; Nhóm III phủ đèn đường D11–D15.
Ba nhóm đầu đã có trong `PREFIX_GROUPS`; **NU1 thì chưa** — đây là một trong *10 mã đèn chưa có
nhóm công thức* nêu ở mục tài liệu giai đoạn 1. Bốn nhóm này **chưa được đối chiếu** với code
theo cách đã làm cho Nhóm I.

### ❌ ĐÍNH CHÍNH 22/08 — công thức module/vỏ VẪN CÓ trong file, lỗi ở phía mình

Suốt mấy vòng trao đổi tôi khẳng định *"khách chưa có công thức số lượng cho module/vỏ"* và ghi
cả vào đây. **Sai.** Thắng chỉ đúng chỗ: các sheet **rule** `M30S050-*` và `VDP0X` có **cột SL**
chứa đầy đủ công thức, dạng văn bản có điều kiện:

```
Khung module          Dọc: 2 · Ngang: 4
Tai                   Công suất <= 600: SL 2 · Công suất > 600: SL 4
Ốc ghép ngang         Dọc: SL 0 · Ngang: Công suất / 50
Đế bắt nguồn          Nguồn nhỏ, Dọc: <=200 SL 1 · >200 SL 2 · Nguồn nhỏ, Ngang: … (7 nhánh)
```

So bản 21/08 với 22/08: **giống hệt** — dữ liệu này có từ đầu, không phải Thắng mới thêm.

**Vì sao tôi tưởng là không có.** Ba sheet *Nhóm I/II/III* chỉ chứa thành phần đèn thành phẩm,
nên tôi tra thành phần module/vỏ ở đó, không thấy, rồi kết luận là thiếu — mà quên rằng số lượng
của module/vỏ nằm ở **cột SL của sheet rule**, khác chỗ với đèn thành phẩm. Phép tra của tôi
đúng nhưng tra nhầm chỗ, và tôi không kiểm lại giả định trước khi báo đi.

**Chặn thật sự nằm ở hai chỗ trong code, không phải ở dữ liệu khách:**

1. `resolve_formula_group` không suy được nhóm cho mặt hàng cha là module/vỏ → throw **trước cả**
   khi chạm tới số lượng.
2. `_so_luong()` trong `doc_bom_sheet.py` chỉ nhận **số thuần**; gặp văn bản có điều kiện thì xếp
   vào *"số lượng đổi theo đặc tính"* rồi bỏ qua. Mô hình hiện tại chưa biểu diễn được dạng này.

⚠ Và `data/bom_template/spec.json` trong git đang **cũ** — còn giữ bản đọc từ file 18/08, cột SL
của VDP0X ghi `"Ghi chú"`. Chạy lại `doc_bom_sheet.py` trên file hiện tại thì lấy đúng công thức.
Nhớ sinh lại spec mỗi lần khách sửa file, đừng đọc spec cũ rồi kết luận về file mới.

### ⚠ Thêm field vào lưới bảng con: hai chỗ chặn, chỉ giao diện mới lộ

Thêm `in_list_view` cho một field của child table **chưa chắc nó hiện trên lưới**. Đã vấp cả
hai chỗ khi thêm ô tích *Không Sử Dụng* vào `BOM Rule` (21–22/08):

1. **Lưới cấp tối đa 11 đơn vị cột, và Frappe LUÔN chèn field bắt buộc** dù không khai
   `in_list_view` (`bom_component`). Không khai `columns` thì Frappe tự chia, tổng vượt 11 và
   field **cuối** rụng khỏi lưới. ➜ Khai `columns` tường minh cho mọi field muốn thấy, tổng ≤ 11.
2. **`__UserSettings` lưu bố cục lưới THEO TỪNG NGƯỜI DÙNG** (`GridView` → tên doctype con →
   danh sách field). Bố cục đã lưu **đè lên** khai báo DocType, nên người từng chỉnh lưới sẽ
   không thấy field mới còn người chưa chỉnh thì thấy — khác nhau theo tài khoản, rất khó đoán.
   ➜ Patch `reset_bom_rule_grid_view` gỡ đúng khoá đó, giữ nguyên phần cài đặt khác của họ.

Cả hai đều **không** lộ ra khi kiểm bằng query hay API — dữ liệu vẫn đúng, chỉ là người dùng
không nhìn thấy cột. Phải mở giao diện thật mới thấy.

### Chi phí bảo trì của cách khai "Mọi biến thể đều chọn"

Rule kiểu này phải bám vào **một đặc tính** và liệt kê sẵn mọi giá trị của nó, nên bộ nạp chọn đặc
tính ít giá trị nhất. VDP0X ra điều kiện `Version: v3.0`. Khách ra vỏ `v4.0` là 9 rule đó **ngừng
khớp**, phải mở BOM Template tích thêm bằng tay. Dùng *Cố Định* thì không vướng, nhưng Thắng chốt
*Theo Rule* vì còn cần chạy công thức số lượng ở Server Script.

### UI: Dialog "Tạo Rule" (`bom_template.js`)
Trên dòng `Theo Rule` của Bảng Thành Phần BOM có nút **Tạo Rule** → dialog "Chọn NVL theo đặc tính":
mỗi **tổ hợp giá trị đặc tính đang thực sự được biến thể của item cha dùng** là 1 ô chọn Item.
Điền sẵn NVL đã chọn trước đó nên dùng lại để sửa được; bỏ trống = không tạo dòng. Không hỏi số lượng.

### UI: điền sẵn NVL khi làm BOM tay (`bom.js`)
Chọn **Mặt Hàng** trên form BOM → tra BOM Template của mặt hàng cha, điền sẵn bảng Nguyên Vật Liệu,
số lượng vẫn do Server Script tính. Mặt hàng không có BOM Template thì **không đụng gì tới form**,
giữ nguyên hành vi mặc định của ERPNext.

#### ⚠ HAI ĐƯỜNG TẠO BOM, HÀNH XỬ KHÁC NHAU — đọc trước khi sửa một trong hai

| Lối vào | Hàm | Làm gì |
|---|---|---|
| Nút trên **Kế hoạch sản xuất** (`Production Plan Item.custom_create_bom`) | `auto_create_bom` → `build_bom_tree` | dựng **CẢ CÂY** bottom-up, tạo BOM cho từng bán thành phẩm rồi nối `bom_no` |
| Chọn **Mặt Hàng** trên form **BOM** | `get_template_raw_materials` | chỉ **ĐIỀN PHẲNG** bảng Nguyên Vật Liệu |

Hai đường ra đời cách nhau một tháng (08/07 và 08/08) cho hai việc khác nhau, nhưng **người dùng gọi
cả hai là "tạo BOM tự động"** nên tưởng chúng giống nhau. Thắng phát hiện 24/08: cùng một mặt hàng,
đi từ Kế hoạch sản xuất thì ra đủ cây, đi từ form BOM thì bán thành phẩm không có BOM.

**Cây BOM 3 tầng là mô hình khách gửi, không phải ca hiếm.** File khách có 7 sheet, mỗi sheet một mặt
hàng cha, và bảng thành phần của `DP01S` trỏ thẳng sang mã của sheet khác. Trong 7 BOM Template đang
bật thì `VDP0X` + `M30S050-A/B` + `M50S050-A/B` **tự chúng là bán thành phẩm có template riêng**. Ví
dụ `DP01S200-6B3HN-AD`: 8 thành phần, 2 trong đó là bán thành phẩm có template. Đèn → vỏ + module →
linh kiện.

**Cách xử lý (chốt của TungDA/Thắng 24/08)** — `find_missing_sub_assembly_boms()` trong `api/bom.py`
dò thành phần nào có BOM Template riêng mà chưa có BOM, trả về kèm trong `get_template_raw_materials`;
`bom.js` hiện banner nêu **đích danh** và thêm nút *"Tạo BOM tự động cho bán thành phẩm"* gọi lại đúng
`auto_create_bom`. **Một hành vi, hai lối vào.**

⚠️ **KHÔNG tự tạo BOM ngầm lúc người dùng vừa chọn Mặt Hàng.** `create_bom` submit BOM mới rồi **gỡ cờ
`is_default` của bản cũ** — app này đã vấp đúng chuyện đó một lần, ghi đè `is_default` lên BOM đang
được Work Order thật tham chiếu, phải cancel + khôi phục tay (xem "Bài học quan trọng"). Tạo/duyệt
chứng từ thật luôn phải qua một cú bấm rõ ràng, có hộp thoại xác nhận.

#### 🔴 BẪY: `add_child` hàng loạt rồi bắn trigger SONG SONG làm MẤT DỮ LIỆU

Không riêng BOM — **chỗ nào thêm nhiều dòng bảng con rồi gọi `frm.script_manager.trigger()` trong
vòng lặp đều dính** (Sales Order, Work Order…).

Triệu chứng: mọi dòng trống trường, **trừ đúng dòng cuối**. Thắng báo 23/08 vì thấy cột UOM trống
7/8 dòng.

Cơ chế — không phải quên set giá trị mà là **bị xoá**:
1. Trigger `item_code` của ERPNext gọi `frappe.call({doc: doc, ...})` — dạng `run_doc_method`, tức
   **gửi nguyên cả tài liệu lên server**.
2. `frappe/handler.py` `run_doc_method` trả lại **chính bản chụp client vừa gửi** (`frappe.response.docs`).
3. `request.js` chạy `frappe.model.sync` **TRƯỚC** callback → `update_in_locals` ghi đè bảng con, rồi
   `clear_keys` **XOÁ** những trường không có trong bản chụp.
4. Callback mới `$.extend(d, r.message)` — chỉ cho đúng dòng của nó.

Bắn N lệnh song song thì phản hồi thứ N xoá sạch dòng 1…N-1. Cái về cuối cùng thắng.

Mất **12 trường** chứ không riêng `uom`: `item_name`, `description`, `stock_uom`, `uom`,
`conversion_factor`, **`bom_no`**, `rate`, `base_rate`, `stock_qty`, `image`,
`include_item_in_manufacturing`, `sourced_by_supplier`. Nghĩa là BOM ra **giá 0** và bán thành phẩm
**mất liên kết BOM con** — hai thứ này im lặng, chỉ `uom` lộ ra vì nó là trường bắt buộc.

**Cách sửa: gọi TUẦN TỰ** — `await` từng trigger trước khi thêm dòng sau. Bản chụp gửi lên khi đó đã
chứa dữ liệu các dòng trước nên vòng sync không xoá gì. `script_manager.trigger` trả về
`frappe.after_server_call()` (resolve khi `ajax_count` về 0), `await` được vì `$(document).ajaxSend`
tăng biến đếm ngay lúc `$.ajax` chạy.

Đo thật trên `VDP0X-1K0-N-GY-v3.0` (13 NVL): trước 12/13 dòng trống UOM → sau **13/13 đủ**.

⚠️ Đặc tính điều kiện trên site thật tên là **`Nguồn`**, KHÔNG phải `Loại nguồn` như tài liệu thiết kế viết.

### Engine tự động tạo BOM (`api/bom.py`, whitelisted `auto_create_bom(item_code, company)`)
Gọi từ nút **"Tạo BOM Tự Động"** trên Production Plan (bảng Select Items to Manufacture, field `custom_create_bom`).

Luồng xử lý:
1. Xác định Item cha (`variant_of`) → tìm BOM Template đang `is_active=1`
2. Đệ quy dựng cây BOM theo thứ tự **bottom-up** (post-order DFS): thành phần `Cố Định` đọc trực tiếp; 2 loại còn lại gọi Server Script `hkled_resolve_bom_qty` (`resolve_qty_by_formula`) để lấy qty (và NVL nếu là `Theo Rule`); nếu thành phần đó tự nó là 1 Item biến thể có BOM Template riêng → đệ quy tiếp (bán thành phẩm nhiều cấp)
3. So sánh cây BOM vừa dựng với BOM Default hiện tại (nếu có) ở **mọi cấp** — nếu khớp hoàn toàn thì giữ nguyên (`status: "valid"`), nếu bất kỳ cấp nào lệch thì **tạo lại toàn bộ cây** (không chỉ cấp lệch), submit theo thứ tự con→cha, gán Default mới, bỏ Default cũ

⚠️ **Công thức trả về 0 thì BỎ HẲN dòng** khỏi BOM, không thêm với qty = 0: `BOM Item` không nhận
qty = 0, và 0 ở đây có nghĩa nghiệp vụ là "biến thể này không dùng thành phần đó" (VD Cầu đấu ≤ 50W).

### Tài liệu giai đoạn 1 (bản nâng cấp Phần I, 2026-07-31)
Nguồn: PM `PM-PRJ-00003` › `BOM_Template_Design_HKLED` (`PM-DOC-00046`). Chi tiết phân tích + 9 vấn đề
dữ liệu còn chờ HKLED xác nhận: `docs/features/bom-template-theo-bien-the.md` (trong app này).

Đáng chú ý: còn **10 Item Template đèn thật chưa thuộc nhóm công thức nào** (`DNU1C*` — đèn phòng nổ
UFO NU1, `DX01S*` — đèn nhà xưởng UFO X01). Từ khi bỏ `rule_group`, việc suy nhóm nằm trong Server
Script — 10 mã này rơi vào nhánh `frappe.throw("Chưa cấu hình công thức …")`, tức **báo lỗi rõ ràng
thay vì tính sai**. Vẫn là câu hỏi còn treo với HKLED, không phải chuyện đã xong.

### Hộp thoại "Chọn Điều Kiện" — nút Tạo Rule

`controllers/js/bom_template.js` + `bom_template.py::get_condition_attributes`.

**Giá trị đặc tính trả về TOÀN BỘ danh mục**, kèm `used_values` đánh dấu giá trị nào đang thật sự có
biến thể dùng; client làm mờ và gắn dấu `°` cho giá trị chưa có biến thể (PM-TASK-00105).
⚠ Bản đầu chỉ trả giá trị đã có biến thể, với lập luận "chọn giá trị chưa ai dùng thì rule vô nghĩa"
— **khách báo sai**: họ cần đặt rule TRƯỚC cho hàng sắp có. Cách cũ giấu mất 11/24 mức Công suất,
6/10 Chip LED, 8/18 Nguồn của `DP01S`.

Thuộc tính lấy từ **bảng đặc tính khai trên chính Mặt Hàng Cha**, giữ nguyên thứ tự khai — không suy
từ biến thể rồi sắp theo bảng chữ cái. Mỗi mặt hàng cha một bộ khác nhau (DP01S 7, DD11S/DPVDS/DXHBC 5).
Giá trị đã bị xoá khỏi danh mục mà biến thể còn dùng thì **vẫn giữ**, nếu không rule cũ trỏ vào nó
sẽ không sửa được.

Mỗi dòng đặc tính có ô **Chọn tất cả**, đồng bộ hai chiều: tick tay đủ hết thì tự bật, bỏ bớt một giá
trị thì tự tắt và chuyển `indeterminate` (PM-TASK-00102).

⚠ **Mỗi lần tick là một lượt gọi `count_matched_variants` mất ~1 giây** (quét toàn bộ biến thể của
mặt hàng cha — DP01S có 5.120). Tick nhanh vài ô là các lượt chồng nhau và **lượt về sau cùng chưa
chắc là lượt mới nhất** → hiện số biến thể sai. Đã đánh số lượt (`update_counts._luot`) và chỉ nhận
kết quả của lượt mới nhất. Sửa hàm này phải giữ cơ chế đó.

## PHẦN II — Bậc Thợ & Giờ Công Chuẩn

| Field/Doctype | Vị trí | Ghi chú |
|---|---|---|
| **Employee Level** (Bậc Thợ) | Doctype mới | `employee_level` (tên/PK), `earnings_per_minute`, `performance_factor`, `team_fund_contribution_rate` |
| `custom_time_to_manufacture` | Item, tab Manufacturing | Phút sản xuất 1 sản phẩm |
| `custom_employee_type` | Employee | Select: Công nhân / Bán hàng / Kế toán (**đã có sẵn**, không phải field tôi tạo) |
| `custom_employee_level` | Employee | Link → Employee Level (**đã có sẵn**) |
| `custom_performance_factor_` | Employee | Fetch từ `custom_employee_level.performance_factor`, read-only (**đã có sẵn**, tên field có `_` thừa — giữ nguyên, không đổi) |

Ràng buộc C1 — Công nhân bắt buộc có Bậc Thợ — làm ở **hai lớp**:

- `employee.js`: cảnh báo sớm ngay khi đổi Loại nhân sự, để người dùng biết trước lúc bấm Lưu.
- `controllers/python_hook/employee.py::validate_employee_level`: **chặn hẳn** bằng `frappe.throw`.

Phải có lớp server vì `mandatory_depends_on` chỉ chạy phía client. Lý do chặn chứ không cảnh báo
suông: engine tính lịch đọc `custom_performance_factor_` (fetch từ Bậc Thợ), công nhân thiếu Bậc Thợ
lọt vào bảng Nhân Công Tham Gia sẽ làm `recalculate_schedule` báo *"chưa có Nguồn Lực (%) hợp lệ"* —
lỗi nổ ở chỗ khác hẳn nơi dữ liệu bị nhập sai, rất khó lần ra.

⚠ Bản đầu **cố ý chỉ cảnh báo mềm** vì lúc audit 33/38 nhân sự thật chưa có Bậc Thợ. Đã siết lại
sau khi dữ liệu được điền. Nếu import nhân sự hàng loạt mà vỡ ở đây thì là do dữ liệu nguồn thiếu
Bậc Thợ, không phải lỗi hook.

## PHẦN III — Lịch Sản Xuất Thông Minh

### Doctype
| Doctype | Vai trò |
|---|---|
| **Employee Schedule** | Lịch làm việc hàng ngày (ca sáng/chiều/tăng ca). `start`/`end` fetch từ Shift Type; `start_time`/`end_time` = Date+giờ, tự tính, read-only |
| **Employee Allocation** | Khoảng thời gian 1 nhân sự tham gia 1 Work Order cụ thể. Validate chống trùng lịch (overlap) cho cùng nhân sự |
| **Work Order Employee** (child) | Gắn trên Work Order (`custom_work_order_employee`). Có `lock_start`/`lock_end` để khoá thủ công, `allocation_record` link tới Employee Allocation tương ứng |

Custom field trên Work Order: `custom_start_time` (mandatory), `custom_end_time`, `custom_estimated_completion_time_minutes`, `custom_required_completion_date__time` — 3 field sau **allow_on_submit=1** vì bị tính lại giữa chừng khi WO đã submit. Thêm `custom_customer` + `custom_sales_person` (PM-TASK-00050, lấy từ Đơn Bán Hàng của lệnh) và `custom_note` (Ghi Chú Sản Xuất, PM-TASK-00046).

⚠ `custom_start_time` là **mandatory nhưng ERPNext tạo Lệnh sản xuất bằng `ignore_mandatory`**, nên
vẫn có lệnh lọt vào DB với ô này trống — và những lệnh đó không mở ra sửa/lưu lại được. Đã vấp thật:
5/34 lệnh trên site khách. Hook `ensure_start_time` lấp lúc tạo, patch `backfill_work_order_start_time`
lấp cho dữ liệu cũ. Thêm field mandatory nào nữa lên Work Order thì phải tính tới đường này.

### Engine tính lịch (`api/work_order_schedule.py`, whitelisted `recalculate_schedule(work_order)`)
Gọi từ nút **"Tính Lại Lịch"** trên Work Order (`work_order.js`). Đây là phần thuật toán phức tạp nhất trong cả 3 phần:

1. **Tính Start Time từng nhân sự chưa khoá** — thời điểm sớm nhất thoả: không sớm hơn giờ bắt đầu WO, nằm trong 1 khoảng Employee Schedule hợp lệ, không trùng Employee Allocation nào khác (loại trừ allocation của chính WO này)
2. **Tính Giới Hạn Tham Gia (available_until)** — nếu nhân sự có 1 Employee Allocation khác (WO khác) bắt đầu sau đó, giới hạn = điểm kết thúc của chuỗi Employee Schedule liên tục cuối cùng trước cam kết đó; không có cam kết nào → không giới hạn
3. **Dựng danh sách interval khả dụng** cho mỗi nhân sự (tìm kiếm xuôi Employee Schedule tối đa 60 ngày, cắt tại `available_until`/`lock_end`)
4. **Sweep-line qua toàn bộ mốc thời gian** của tất cả nhân sự: mỗi đoạn `[t1,t2)`, Năng Lực = tổng `performance_factor/100` của nhân sự đang hoạt động, tiêu thụ dần khối lượng công việc chuẩn (`qty × time_to_manufacture`) cho đến khi hết → ra `end_time` + `estimated_completion_time_minutes`
5. Ghi lại `start_time`/`end_time`/`available_until` từng dòng, tự tạo/cập nhật Employee Allocation tương ứng (qua `allocation_record`)

Dòng có `lock_start`/`lock_end` giữ nguyên giá trị người dùng nhập, không bị tính lại — đây chính là cơ chế xử lý "nhân sự nghỉ giữa chừng" / "nhân sự mới vào giữa chừng" mà không cần code riêng, chỉ cần gọi lại `recalculate_schedule`.

`controllers/python_hook/work_order.py` (`doc_events.Work Order.on_update`): khi WO chuyển `status="Completed"`, đồng bộ `end_time` của các Employee Allocation liên kết theo `actual_end_date` thực tế.

**Đã kiểm chứng khớp 100%** với ví dụ tính toán chi tiết trong tài liệu gốc (Item 100 sản phẩm × 10 phút, 3 nhân sự A/B/C) → 478 phút, kết thúc 8h28 ngày kế tiếp, đúng từng mốc start/end/available_until.

### Dữ liệu demo — CHÚ Ý: phụ thuộc từng bench
Bộ demo Phần I (`Den pha` → `Module LED Test` → `Chip LED Module Test`, BOM Template `BT-DEN-PHA`…) và
Phần III (`PIII-TEST Nhan Su A/B/C`, `PIII-TEST-ITEM-A`, `MFG-WO-2026-00129` = 478 phút / 8h28 ngày sau)
được dựng trên bench cũ `/home/pc/test_core`, **KHÔNG có** trên bench `mbwnext_project` hiện tại.

Site `hkled.com` của bench này là **bản backup dữ liệu khách ngày 30/07/2026**: 310 Item Template,
35.713 Item, 3 BOM + 3 Work Order (đều trên item test cũ `Thành phẩm 1`), 5 Bậc Thợ,
11 Employee Schedule, 6 Employee Allocation. Kiểm tra lại bằng query trước khi tin số liệu ở đây.

Sau các đợt nhập dữ liệu khách: **60.784 Item** (PM-TASK-00061/67) và **7 BOM Template** —
`DP01S`, `DP03S`, `M30S050-A/B`, `M50S050-A/B`, `VDP0X` (PM-TASK-00110) — **733 rule** sau đợt
bổ sung ô tích *Không Sử Dụng* ngày 21/08.

### Nút "Thêm Đội Sản Xuất" — lý do không tính được % thời gian rảnh

`api/work_team.py::tinh_thoi_gian_ranh` trả thêm `free_time_note` khi mốc kết thúc **không sau** mốc
bắt đầu, kèm giá trị cụ thể của cả hai mốc. `controllers/js/work_order.js` khi thiếu trường thì nêu
**đích danh trường nào** còn trống.

⚠ Trước đây cả hai trường hợp — thiếu mốc, và có đủ mốc nhưng ngược thứ tự — đều hiện chung câu
"Điền Thời Gian Bắt Đầu và Thời Điểm Cần Hoàn Thành". Khách nhìn thấy cả hai trường **đã có sẵn trên
màn hình**, đọc câu bảo đi điền, kết luận chức năng hỏng. Trên site có 19/35 lệnh thiếu mốc và 3/35
lệnh có mốc kết thúc trước mốc bắt đầu.

### Hai bẫy giao diện Frappe đã dính

**`frm.set_intro` NỐI THÊM banner, không thay thế.** `Layout.show_message()` dùng `appendTo`; chỉ
chuỗi rỗng mới gọi `empty()`. Đổi giá trị vài lần là chồng một cột banner. Phải gọi `frm.set_intro("")`
ở đầu handler.

⚠ Hệ quả nặng hơn khi có **từ 2 banner độc lập trở lên** trên cùng một form: không thể gọi
`frm.set_intro` trực tiếp ở hai chỗ, vì cập nhật chỗ này sẽ nhân đôi hoặc đè chỗ kia — nhất là khi
một banner cần vẽ lại sau một thao tác. `bom.js` có 2 banner (số lượng tạm tính, và bán thành phẩm
thiếu BOM) nên phải gom qua `set_banner_section(frm, key, html)` + `render_banners(frm)`: giữ các
mục trong một object, mỗi lần đổi thì **xoá sạch rồi vẽ lại cả khối**.

**`frappe.msgprint` ra hộp thoại RỖNG** nếu gọi ngay sau khi điền bảng con — chuỗi trigger `item_code`
của ERPNext còn đang chạy và nó dọn hộp thoại msgprint dùng chung. Dùng banner `frm.set_intro()` thay thế.

## Hooks đăng ký (hooks.py)

```
doctype_js:
  BOM              -> controllers/js/bom.js
  BOM Template     -> controllers/js/bom_template.js
  Production Plan  -> controllers/js/production_plan.js
  Sales Order      -> controllers/js/sales_order.js
  Employee         -> controllers/js/employee.js
  Work Order       -> controllers/js/work_order.js
  Other Task       -> controllers/js/other_task.js

doctype_list_js:
  Employee Schedule -> controllers/js/employee_schedule_list.js   # nút "Tạo Nhanh" ở LIST VIEW

doc_events:
  Work Order.update_status              -> sync_employee_allocation_on_finish
                                        -> split_employee_production_on_finish
  Work Order.before_insert              -> clear_copied_allocation_record   # PM-TASK-00045
                                        -> inherit_from_production_plan
                                        -> set_sales_info                   # PM-TASK-00050
                                        -> ensure_start_time                # PHẢI sau inherit_…
  Work Order.validate                   -> validate_employee_production
                                        -> set_sales_info
  Work Order.before_update_after_submit -> validate_employee_production
  Work Order.on_cancel / on_trash       -> cleanup_employee_allocation      # PM-TASK-00045 (C6)
  Production Plan.validate              -> set_required_completion_time
                                        -> set_item_production_note         # PM-TASK-00046
  Sales Order.validate                  -> fill_item_production_note        # PM-TASK-00046
  Employee.validate                     -> employee.validate_employee_level   # C1, chặn ở SERVER
  Stock Entry.before_submit             -> stock_entry.set_serial_no_on_manufacture

fixtures:
  Custom Field    where module = "MBWNext HKLed"   # tự bắt field mới, không phải sửa tay
  Property Setter where module = "MBWNext HKLed"   # mã chứng từ 9 loại phiếu (PM-TASK-00054)
```

⚠ Thứ tự trong `before_insert` của Work Order **không được đảo**: `inherit_from_production_plan`
lấy giờ từ Kế Hoạch, `ensure_start_time` chỉ lấp chỗ còn trống. Đảo lại là luôn lấy giá trị dự phòng.

⚠ `mandatory_depends_on` của Frappe **chỉ chạy phía client** (`frappe/public/js/frappe/form/save.js`),
không có dòng Python nào kiểm — nên ràng buộc C1 phải làm bằng hook `Employee.validate`, không thì
lưu bằng script/API/Data Import vẫn lọt.

### ⚠ Ba cạm bẫy hook đã mắc phải trong app này

1. **`Work Order.on_update` là code chết.** Work Order không có method `on_update`, và status
   chuyển sang `Completed` bằng `db_set` trong `WorkOrder.update_status()` — `db_set` không chạy
   hook. Ngoài ra WO lúc đó đã submit nên Frappe chỉ gọi `on_update_after_submit`.
   ➜ Hook đúng là **`update_status`**, chỗ `Stock Entry.update_work_order()` gọi bằng
   `run_method()` (có compose doc_events). Kèm theo: `set_actual_dates()` chạy **sau**
   `update_status()` nên `doc.actual_end_date` lúc hook chạy vẫn là giá trị cũ — phải tự tính.
2. **`validate` không chạy cho document đã submit.** Ràng buộc nào áp dụng sau khi submit
   (vd. tổng Sản Lượng Nhân Viên, C12) phải khai **cả** `before_update_after_submit`.
3. **`allow_on_submit` phải đặt trên TỪNG FIELD của child DocType**, không chỉ trên field bảng
   ở cha. Frappe kiểm `allow_on_submit` của từng field con trong `validate_update_after_submit`.
   Thiếu là báo *"Not allowed to change … after submission"* rất khó đoán.

### ⚠ `fetch_from` chạy TRƯỚC `before_insert` — dòng hook thêm vào bị lỡ vòng fetch

Trong `Document.insert()` thứ tự là:

```
self._validate_links()            # <- Frappe áp fetch_from ở đây (qua get_invalid_links)
self.check_permission("create")
self.run_method("before_insert")  # <- hook append dòng con SAU đó
```

Nên dòng con thêm ở `before_insert` **không bao giờ** được `fetch_from` điền. Đã vấp thật: WO tạo
từ Kế Hoạch Sản Xuất có đủ nhân sự của đội nhưng `employee_level` trống và `performance_factor_` = 0,
làm `recalculate_schedule` báo "chưa có Nguồn Lực (%) hợp lệ".

Phía client cũng vậy: `frm.add_child(...)` **không** kích hoạt vòng fetch của Link field.

➜ Cứ thêm dòng con bằng code (server hay client) thì **tự điền luôn các trường `fetch_from`**,
đừng trông vào cơ chế fetch. Cùng họ với bẫy Employee Schedule: `fetch_from` chỉ chạy trong
`_validate()`, tức SAU `validate()` — nên `set_datetime_fields()` không thấy `start`/`end`.

### ⚠ Custom DocPerm THAY THẾ sạch DocPerm chuẩn

`Meta.set_custom_permissions()` (frappe/model/meta.py): hễ một DocType có **bất kỳ** bản ghi
`Custom DocPerm` nào thì Frappe vứt toàn bộ DocPerm chuẩn và chỉ dùng các dòng Custom đó.

➜ Muốn thêm quyền cho một DocType của app lõi (vd cấp read `Employee` cho vai trò sản xuất),
**phải** dùng `frappe.permissions.add_permission()` — hàm này gọi `setup_custom_perms()` để sao
chép hết quyền chuẩn sang Custom DocPerm trước rồi mới thêm dòng mới. Tự `frappe.get_doc(...).insert()`
2 dòng Custom DocPerm là **xoá luôn** quyền của HR Manager / HR User, hỏng cả phân hệ nhân sự.

Cũng vì vậy **không khai `Custom DocPerm` vào `fixtures`**: fixtures sẽ chụp lại toàn bộ quyền của
DocType đó trên site này rồi áp sang site khác khi cài app. Dùng patch, chỉ thêm đúng phần cần.

### Dựng site từ số 0 — thứ tự bắt buộc

`bench migrate` trên site cài mới phải dựng lại được **toàn bộ** 62.054 mặt hàng. Chuỗi
patch làm việc đó, theo đúng thứ tự trong `patches.txt`:

| # | Patch | Dựng ra |
|---|---|---|
| 1 | `seed_item_attribute` | 77 Item Attribute (vỏ rỗng) + chốt tiền đề UOM `Cái` |
| 2 | `import_danh_muc_vat_tu` | 12 file đợt 1 |
| 3 | `add_item_replenishment_method` | Custom Field `custom_replenishment_method` |
| 4 | `import_danh_muc_vat_tu_dot_2` | 18 file đợt 2 → tổng 2.972 mã vật tư |
| 5 | `import_thanh_pham` | 4 file Nhóm I–IV → 59.023 đèn thành phẩm |
| 6 | `import_bom_template` | BOM Template + BOM Rule |

⚠ **Thứ tự có ý nghĩa.** `import_bom_template` tra biến thể bằng
`frappe.get_all("Item", filters={"variant_of": ...})` — chạy trước khi có mặt hàng thì nó ra
0 rule, in cảnh báo rồi `bench migrate` **vẫn báo thành công**. Đây là kiểu hỏng im lặng tệ
nhất: site "cài xong" mà không có đèn nào và không có BOM nào. Site đã chạy rồi thì đổi thứ
tự trong `patches.txt` vô hại — `Patch Log` ghi theo tên patch, không theo vị trí dòng.

⚠ **Thứ tự cài app cũng bắt buộc.** `mbwnext_hkled` phải cài **sau**:

- `mbwnext_localization` — tạo UOM `Cái` trong `after_install`; thiếu nó thì mọi
  `_tao_item()` vỡ ở `LinkValidationError: Could not find Default Unit of Measure: Cái`.
  `seed_item_attribute` chặn sớm và báo đúng nguyên nhân.
- `mbwnext_advanced_selling` — tạo `Item.custom_item_line`, là `insert_after` của
  `custom_replenishment_method`; thiếu nó thì Custom Field không insert được.

⚠ **Item Attribute không nằm trong `fixtures`.** `_bao_dam_gia_tri()` cố ý `frappe.throw`
khi đặc tính chưa tồn tại thay vì tự tạo — một cột gõ sai chính tả sẽ lặng lẽ đẻ ra đặc tính
mới. Danh sách chốt nằm ở `DAC_TINH` trong `seed_item_attribute.py`. Thêm cột đặc tính mới
vào CSV thì phải thêm tên vào đó; patch tự in cảnh báo liệt kê cột chưa khai.

### ⚠ Fixtures ghi đè patch

`sync_fixtures` chạy **sau** patches trong `bench migrate`. Field nào đã có trong
`fixtures/custom_field.json` thì giá trị trong file đó **thắng** giá trị patch vừa set.
Đã vấp: patch đặt `mandatory_depends_on` cho `Employee-custom_employee_level` (C1) nhưng bị
fixtures ghi đè về rỗng ngay trong cùng lần migrate. ➜ Thuộc tính lâu dài phải nằm trong
fixtures; patch chỉ để tạo lần đầu. Sửa xong nhớ `bench --site hkled.com export-fixtures --app mbwnext_hkled`.

Server Script **cố ý KHÔNG khai trong `fixtures`**: fixtures ghi đè mỗi lần migrate, sẽ xoá công thức
khách vừa sửa. Cài một lần qua patch, sau đó script trên site là nguồn chạy thật.

## Mã chứng từ riêng của HKLED (`PM-TASK-00054`, 08/08/2026)

9 loại phiếu dùng mã `<viết tắt>-<2 số năm>-<5 số>`: `SO-` Đơn hàng bán, `KSX-` Kế hoạch sản xuất,
`LSX-` Lệnh sản xuất, `KNB-` Chứng từ kho nội bộ, `PXK-` Phiếu xuất kho hàng bán, `PNK-` Phiếu nhập
kho hàng mua, `YCM-` Yêu cầu mặt hàng, `PO-` Đơn mua hàng, `BG-` Báo giá.

Cấu hình nằm ở **Property Setter** (`module = MBWNext HKLed`), tạo bởi `patches/set_document_naming_series.py`
và **có trong `fixtures`** — nên sửa danh sách series phải sửa trong patch rồi `export-fixtures` lại,
thêm bằng giao diện sẽ bị ghi đè ở lần `bench migrate` kế tiếp.

⚠ **`naming_series` không được Frappe kiểm tra giá trị.** `_validate_selects()`
(`frappe/model/base_document.py`) bỏ qua đúng trường này, nên một series không nằm trong danh sách
chọn vẫn được dùng bình thường, không có thông báo lỗi — chỉ âm thầm sinh mã sai định dạng. Đã vấp:
`Production Plan` là doctype duy nhất trong 9 loại mà ERPNext lõi **không** đặt `no_copy` cho
`naming_series`, nên bấm **Duplicate** một kế hoạch cũ đẻ ra `MFG-PP-2026-…` theo mã cũ. Đã bù bằng
Property Setter `no_copy = 1`.

Chứng từ cũ **giữ nguyên mã**; số thứ tự của mã mới **bắt đầu lại từ 00001** (bộ đếm `tabSeries` gắn
theo tiền tố). Hai series hàng trả lại `MAT-DN-RET-` / `MAT-PR-RET-` cố ý giữ nguyên vì bảng khách
gửi không nhắc tới. Test case: `docs/testcases/ma-chung-tu-hkled.md`.

## ⚠️ Bài học quan trọng — LUÔN kiểm tra dữ liệu thật trước khi tạo mới

**Cả 3 phần đều gặp cùng một tình huống**: nhân viên `thangdo@mbw.vn` đã tự xây phần lớn doctype/custom field trực tiếp trên UI Desk của site `hkled.com` **trước khi** công việc này bắt đầu — hoàn toàn không có trong git. Việc không kiểm tra trước đã khiến 2 lần xảy ra sự cố:

1. **Phần I**: BOM Template test trỏ nhầm vào `Module LED`/`Chip LED Module` (item template THẬT), engine tạo BOM mới và ghi đè `is_default` lên BOM đang được Work Order thật tham chiếu. Phải cancel + xoá BOM sai, khôi phục lại default cũ dựa theo Work Order nào đang thực sự tham chiếu BOM nào.
2. **Phần II**: tạo trùng 4 custom field (`custom_employee_role`, `custom_performance_factor`, `custom_time_to_manufacture` bản đầu, `custom_worker_grade_section`) trong khi field tương đương đã tồn tại (`custom_employee_type`, `custom_performance_factor_`, `custom_time_to_manufature` lỗi chính tả) — phải xoá field trùng, đổi tên field lỗi chính tả bằng `frappe.model.utils.rename_field` để giữ dữ liệu.
3. **Phần III**: cả 3 doctype + field trên Work Order đã tồn tại sẵn (module gốc là `HR`/`Manufacturing`, không phải `MBWNext HKLed`) nhưng chưa có bất kỳ logic nghiệp vụ nào — chỉ phần thuật toán là thực sự mới.

**Quy tắc rút ra cho mọi việc tiếp theo trên app này**:
- Trước khi tạo Doctype/Custom Field mới, luôn `frappe.db.exists("DocType", "...")` / query `Custom Field` trước.
- Trước khi cho BOM Template / BOM Rule / bất kỳ engine nào trỏ vào 1 Item thật, kiểm tra Item đó đã có BOM Default / được Work Order nào tham chiếu chưa.
- Khi cần dữ liệu test, đặt tên rõ ràng, khác biệt tuyệt đối với item/nhân sự thật (tiền tố `Test`, `PIII-TEST`, item không dấu như `Den pha` thay vì `Đèn pha` thật).
- `frappe.db.set_value`/`frappe.rename_doc` không ghi Version log — không dựa vào Version history để suy ra trạng thái "trước khi sửa"; thay vào đó tra cứu chứng từ thật đang tham chiếu (Work Order, v.v.) để xác định giá trị đúng cần khôi phục.
- **Tên đặc tính / giá trị đặc tính trong tài liệu có thể KHÔNG khớp site thật** — luôn query
  `Item Attribute` + `Item Attribute Value` trước khi hard-code chuỗi. Lần làm giai đoạn 1 (2026-07-31),
  tài liệu ghi `Loại nguồn` nhưng site chỉ có `Nguồn`; nếu không kiểm thì mọi công thức trả về sai âm thầm.
- **Đếm số lượng master data từ ERPNext, không từ file Excel khách gửi** — tài liệu ghi 199 Item Template,
  thực tế 310 (277 đèn + 23 phụ kiện), và lộ ra 10 mã đèn chưa có nhóm công thức nào.

## Quy ước code

- Python: tab indent, double quote, line-length 110 (ruff, theo `pyproject.toml`)
- Server hooks: `controllers/python_hook/<doctype>.py`, khai báo qua `doc_events`
- API whitelisted: `api/<domain>.py`
- Client hooks: `controllers/js/<doctype>.js`, khai báo qua `doctype_js` — **không đặt trong `public/js/`** (chuẩn chung MBWNext, khớp app lõi)
- Patch một lần (sửa dữ liệu/field đã tồn tại): `patches/`, khai báo trong `patches.txt` mục `[post_model_sync]`, luôn viết idempotent (check tồn tại trước khi tạo/sửa)
- Bản dịch: label/thông báo viết thẳng tiếng Việt trong source, NHƯNG **tên DocType vẫn phải dịch
  qua `locale/vi.po`** (breadcrumb/list view/nút Add hiện msgid tiếng Anh với user chọn Tiếng Việt).
  Thêm DocType mới → generate-pot-file → update-po-files → dịch → **compile-po-to-mo** (bước hay quên)

## Cách chạy

```bash
cd /home/mbw/mbw-dev/cozy_dev            # bench hiện tại (máy dev chung)
bench set-config -g server_script_enabled 1   # BẮT BUỘC cho Phần I (công thức nằm ở Server Script)
bench start
bench --site hkled.com migrate
bench build --app mbwnext_hkled
bench --site hkled.com export-fixtures --app mbwnext_hkled   # sau khi thêm Custom Field mới (nhớ set module=MBWNext HKLed)
```

**Cổng truy cập**: `Procfile` của bench khai `bench serve --port 8012` — giá trị này ĐÈ
`webserver_port` (8006) trong `common_site_config.json`, đừng tin field đó.
- Ngay trên máy dev: `http://localhost:8012`
- Từ máy khác (cổng test dùng chung): `http://dev.mbwnext.com:8012`

Bench này còn chứa site `mbw.com`; site của app là `hkled.com` — luôn truyền `--site hkled.com`.

Nạp lại Server Script từ bản gốc trong app (chỉ khi cần reset, sẽ **mất** chỉnh sửa trên site):

```python
# bench --site hkled.com console
from mbwnext_hkled.server_scripts.bom_qty import SCRIPT, SCRIPT_NAME
doc = frappe.get_doc("Server Script", SCRIPT_NAME); doc.script = SCRIPT; doc.save(); frappe.db.commit()
```

## Tài liệu liên quan

Nguồn yêu cầu trên app PM: dự án `PM-PRJ-00003` (HKLed) › Tài liệu › Tài Liệu Giai Đoạn 1
- `PM-DOC-00044` — TÀI LIỆU NGHIỆP VỤ NÂNG CẤP GIAI ĐOẠN 1 HKLED.docx — ⚠ **chỉ có PHẦN II trở đi**
  (mở ra là "PHẦN II: BẬC THỢ VÀ GIỜ CÔNG CHUẨN", 415 đoạn). Dòng này trước ghi "Phần I/II/III bản đầu"
  là **SAI** — sửa 25/08 sau khi hai phiên Claude cùng đi tìm Phần I và đều không có.
- ⚠ **KHÔNG CÓ tài liệu nghiệp vụ PHẦN I trên PM.** `auto_create_bom` ghi nguồn là "PHẦN I mục 7 tài
  liệu nghiệp vụ HKLED" và `BOM_Template_Design_HKLED` cũng viện dẫn "Phần I.7", nhưng tài liệu đó
  **không có trong thư mục tài liệu khách của `PM-FEAT-00007`**. Hệ quả thật: không ai đối chiếu được
  phạm vi "Tạo BOM tự động" tới đâu, và chính vì thiếu nó mà phần điền form BOM (07/08) bị làm như một
  việc rời, để lọt lỗ hổng cây BOM bên dưới. Đã xin Thắng up lên (PM-FEAT-00007, 24/08).
- `PM-DOC-00046` — `BOM_Template_Design_HKLED.md` (spec nâng cấp Phần I, đã implement 2026-07-31)
- `PM-DOC-00043` — Danh sách thành phẩm (MBW).xlsx (dữ liệu gốc của công thức số lượng)

Tài liệu 4 giai đoạn nằm TRONG app này (`apps/mbwnext_hkled/docs/` — quy ước mới của PM Feature,
không còn đặt ở gốc bench):
Mỗi tính năng dùng **một tên gốc chung cho cả 4 thư mục** để tra chéo được:

| Tên gốc | PM Feature | features | mockups | testcases | huong-dan |
|---|---|---|---|---|---|
| `bom-template-theo-bien-the` | PM-FEAT-00007 | ✔ | ✔ (.md) | ✔ A–H | — |
| `bac-tho-lich-san-xuat` | PM-FEAT-00008 | ✔ | ✔ (.html) | ✔ 61 ca | ✔ cấu hình + vận hành + `anh/` |
| `bieu-do-gantt-lich-lam-viec` | PM-FEAT-00009 | ✔ | ✔ (.html) | ✔ 31 ca | ✔ vận hành + `anh/` |

Test case của các PM Task rời (không thuộc feature nào) đặt theo nhóm việc:
`ghi-chu-san-xuat-va-ke-hoach-tu-don-ban.md` (PM-TASK-00046/47/49/50),
`ma-chung-tu-hkled.md` (PM-TASK-00054),
`danh-muc-vat-tu-hkled.md` + `danh-muc-vat-tu-van-de-theo-sheet.md` +
`danh-muc-vat-tu-ten-can-sua.md` + `danh-muc-lens.md` (PM-TASK-00061/108),
`phuong-phap-bo-sung.md` (PM-TASK-00067),
`bom-template-hkled.md` (PM-TASK-00110) — tất cả trong `docs/testcases/`.

## PHẦN V — Biểu đồ tình hình làm việc của nhân sự (`PM-FEAT-00009`, xong 08/08/2026)

Màn hình Desk **chỉ đọc** tại `/app/bieu-do-lich-lam-viec`: mỗi công nhân một dòng,
đỏ = đang làm Lệnh sản xuất, xanh = rảnh trong ca, xám = ngoài ca. Xem được **khoảng nhiều ngày**
(Từ ngày / Đến ngày, tối đa 31 ngày), mỗi ngày là một dải 08:00–24:00 nối nhau, kèm cột **Rảnh**
hiện `% rảnh` và `phút rảnh / tổng phút theo lịch` của đúng khoảng đang lọc.

⚠ Khoảng 00:00–08:00 bị **cắt bỏ hẳn** khỏi trục, không vẽ đủ 24 giờ: không ai làm việc trong khoảng
đó, mà giữ lại thì mỗi ca bị bóp còn khoảng hai phần ba bề rộng. Biểu đồ luôn **co vừa màn hình**,
không có thanh cuộn ngang; nhãn giờ thưa dần theo độ dài khoảng và bỏ hẳn khi xem quá 7 ngày.

⚠ **Điểm cốt lõi**: `Employee Allocation` chỉ lưu HAI ĐẦU MÚT của cả quá trình tham gia nên trùm cả
nghỉ trưa và ban đêm. Mọi chỗ tính thời gian phải **giao với `Employee Schedule`** trước:
`đoạn bận = Allocation ∩ Schedule`, `đoạn rảnh = Schedule − Allocation`. Vẽ/tính thẳng từ Allocation
là sai. Áp dụng cho cả `api/employee_timeline.py` lẫn `api/work_team.py::tinh_thoi_gian_ranh`.

- `api/employee_timeline.py` — `get_timeline(from_date, to_date, work_teams)`, `get_work_teams()`
- `mbwnext_hkled/page/bieu_do_lich_lam_viec/` — Desk Page (js + css, không thư viện ngoài)
- `mbwnext_hkled/workspace/hkled/` — workspace **HKLed** gom các màn hình của dự án
- Tài liệu: `docs/features/`, `docs/mockups/`, `docs/testcases/`, `docs/huong-dan/` cùng tên
  `bieu-do-gantt-lich-lam-viec`

⚠ KHÔNG dùng chế độ xem Gantt sẵn có của Frappe: `gantt_view.js` kéo/thả ghi bằng
`frappe.db.set_value` với định dạng `"YYYY-MM-DD"` → **cắt cụt phần giờ của Datetime**, và bỏ qua
`recalculate_schedule`.

## Nạp master data bằng patch — và cái giá của nó

Hai patch đang nạp master data: `seed_bom_rule_group` (nhóm công thức + BOM Component) và
`import_danh_muc_vat_tu` (11 sheet danh mục vật tư — 215 mặt hàng cha + 1.506 biến thể, nguồn ở
`data/danh_muc/*.csv`, phần xử lý ở `data/nhap_item.py`).

Lý do: HKLED cần đúng bộ đó trên máy chủ thật, mà Data Import bằng tay không để lại dấu vết trong git.

⚠ **Cái giá**: patch idempotent theo kiểu *"có rồi thì bỏ qua"*, nên khách **xoá một bản ghi trên
giao diện thì lần `bench migrate` sau nó sống lại**. Muốn bỏ hẳn phải xoá khỏi file nguồn trong app.
Nói rõ điều này với khách khi bàn giao, đừng để họ tự phát hiện.

⚠ **`standard_rate` là trường BẮT BUỘC của Item trên bench này**, nằm thẳng trong
`erpnext/stock/doctype/item/item.json` — không phải Property Setter nên grep Property Setter sẽ không
ra. Ràng buộc chỉ chặn khi trường **để trống**; `0` vẫn qua vì `_get_missing_mandatory_fields()` so
bằng `cstr(value).strip()`. Tạo Item bằng code thì **đặt `standard_rate = 0`**, đừng dùng
`ignore_mandatory` — cùng họ với bẫy `custom_start_time`, sẽ đẻ ra bản ghi mở lên không lưu lại được.

⚠ **Cây Nhóm Sản Phẩm của site này phẳng hoàn toàn**: 60 nhóm đều `parent_item_group = NULL` và
**không có gốc `All Item Groups`**. Tạo nhóm mới cứ để phẳng cho khớp, đừng "sửa cho đúng chuẩn".

⚠ **Tên mặt hàng cha không được trùng tên biến thể của chính nó.** Bảng nguồn để cột *Tên sản phẩm*
của cha chép nguyên tên biến thể đầu tiên kèm cả công suất — 25 mặt hàng cha ở sheet Vỏ đèn dính,
trên danh sách Item hiện hai dòng chữ y hệt. `ten_mat_hang_cha()` bỏ đuôi *"Công suất …W"* **chỉ khi
thật sự trùng**. Kèm `sua_ten_neu_lech()` vì bộ nạp vốn chỉ-thêm-mới: không có nó thì item đã nằm sẵn
trên site giữ tên cũ vĩnh viễn — đã bắt được 2 mặt hàng cha còn mang tên từ trước lúc khách sửa bảng.

⚠ **Bảng nguồn của khách có lỗi thật, và bộ nạp CỐ Ý không sửa hộ** — không tự chế mã, không tự điền
ô trống, không chọn hộ giữa hai dòng mâu thuẫn; dòng nào không xử lý được thì bỏ qua và ghi vào báo
cáo để hỏi khách. Vòng đầu bỏ 158/1.516 dòng; sau hai lượt HKLED sửa bảng thì **nạp hết 1.516/1.516**.
Nguyên tắc: **thà bỏ qua còn hơn đoán**.

⚠ **Khách đổi mã hàng loạt thì phải dọn item mã cũ.** Bộ nạp chỉ biết thêm mới, không biết mã nào vừa
bị đổi tên — hai lượt sửa bảng của HKLED để lại 491 + 3 item mồ côi. Cách rà: lấy tập mã trong CSV, so
với item trên site thuộc các nhóm đó, phần thừa thì kiểm **không dính chứng từ nào** (Stock Ledger
Entry, BOM Item, Sales/Purchase Order Item, Item Price, Bin) rồi mới xoá. Bỏ bước này thì site có cả
hai bộ mã mà đối soát vẫn báo "khớp".

⚠ **Biến thể KHÔNG bắt buộc có đủ đặc tính của mặt hàng cha.** Bản đầu của bộ nạp bỏ thêm 5 mặt hàng
cha vì tôi tin ngược lại — Thắng phản biện, chạy thử thì thấy: cha 3 đặc tính, biến thể khai 2 vẫn
tạo được; khai đủ dòng nhưng để trống giá trị thì ERPNext tự bỏ dòng đó. Thứ nó thật sự chặn là hai
biến thể **đụng cùng một tổ hợp giá trị** (`ItemVariantExistsError`). Bài học: đừng suy ràng buộc của
ERPNext từ trực giác, dựng 3 bản ghi nháp chạy thử là xong.

⚠ **`abbr` của Item Attribute Value phải duy nhất trong một đặc tính**
(`item_attribute.py::validate_duplication`). Đã vấp: `Công suất` trên site lưu **số trần** (`1`, `2`,
`30`) còn `abbr` mới là `1W`, `30W` — thêm giá trị `1W` là đụng abbr của `1`. Bài học rộng hơn:
trước khi thêm giá trị đặc tính, xem site đang viết kiểu gì, đừng thêm bản sao viết khác kiểu.

⚠ **Mã biến thể do ERPNext tự sinh KHÔNG theo quy ước của HKLED.** Chức năng *Create Variant* sinh
ra `OBL-M5-M5-20mm-RT-S-H-T`, trong khi khách dùng `OBL-M5x20-RT-S-H-T`. Nạp bằng patch thì ép thẳng
`item_code` từ file nguồn nên không dính; nhưng người dùng thêm biến thể trên giao diện phải tự sửa
mã trước khi lưu. Đang chờ HKLED quyết có làm quy tắc sinh mã tự động không.

## Tài khoản test phân quyền trên site `hkled.com`

Hai tài khoản tạo sẵn để kiểm phân quyền thay vì lúc nào cũng chạy bằng Administrator, đều
`Manufacturing User` + `Desk User`:

| Tài khoản | User Permission | Dùng để kiểm |
|---|---|---|
| `test.gioihan.nhansu@hkled.test` | Employee = `Anh A` | người chỉ được thấy 1 nhân sự |
| `test.gioihan.lenh@hkled.test` | Work Order = `MFG-WO-2026-00004` | người chỉ được thấy 1 lệnh sản xuất |

**Không đặt mật khẩu** — dùng `frappe.set_user("<email>")` trong `bench console`, đừng tạo mật khẩu
rồi đăng nhập bằng tay.

Kiểm quyền phải chú ý `frappe.get_list` (có áp User Permission) khác `frappe.get_all` (**không** áp).
Dùng nhầm `get_all` trong API là người dùng bị hạn chế vẫn thấy hết dữ liệu của người khác.
