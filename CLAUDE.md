# MBWNext HKLed

App Frappe/ERPNext triển khai "Tài liệu nghiệp vụ nâng cấp giai đoạn 1 HKLED" (công ty sản xuất đèn LED): tự động sinh BOM đa cấp theo biến thể sản phẩm (Phần I), quản lý bậc thợ/giờ công chuẩn (Phần II), và lịch sản xuất thông minh tự động tính thời gian hoàn thành Lệnh sản xuất theo nhân công (Phần III).
Site: `hkled.com`. Repo: chưa xác định remote (khởi tạo local).

## Cấu trúc thư mục

```
mbwnext_hkled/
├── api/
│   ├── bom.py                          # Engine tự động tạo BOM đa cấp (Phần I)
│   └── work_order_schedule.py          # Engine tính lịch sản xuất (Phần III) — phần lõi phức tạp nhất
├── controllers/
│   └── python_hook/
│       └── work_order.py               # doc_events: đồng bộ Employee Allocation khi WO Finish
├── patches/                             # 5 patch, chạy post_model_sync
│   ├── add_production_plan_bom_button.py       # Custom Field "Tạo BOM Tự Động" trên Production Plan Item
│   ├── adjust_work_order_schedule_fields.py    # reqd/allow_on_submit cho field lịch trên Work Order
│   ├── rename_time_to_manufacture_field.py     # sửa lỗi chính tả custom_time_to_manufature -> ...manufacture
│   └── set_custom_field_module.py              # gán module=MBWNext HKLed cho custom field để export-fixtures
├── fixtures/
│   └── custom_field.json                # 11 Custom Field (Item/Employee/Production Plan Item/Work Order)
├── public/js/
│   ├── bom_template.js                  # Popup "Tạo Rule" 2 bước trên BOM Template
│   ├── production_plan.js               # Nút "Tạo BOM Tự Động" trên Production Plan Item
│   ├── employee.js                      # Cảnh báo mềm khi Công nhân chưa gán Bậc Thợ
│   └── work_order.js                    # Nút "Tính Lại Lịch" trên Work Order
├── mbwnext_hkled/                       # Module chính (module: "MBWNext HKLed")
│   └── doctype/
│       ├── bom_component/               # PHẦN I — danh mục thành phần BOM
│       ├── bom_component_table/         # PHẦN I — child table: bảng thành phần BOM Template
│       ├── bom_rule/                    # PHẦN I — child table: công thức NVL theo biến thể
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
| **BOM Component** | Master data | Danh mục tên thành phần BOM (Nguồn, Vỏ đèn pha, Module LED, ...) |
| **BOM Component Table** | Child table | Khai báo thành phần cần có trong 1 BOM Template — kiểu `Cố Định` (item+qty cố định) hoặc `Theo Rule` (tra theo BOM Rule) |
| **BOM Rule** | Child table | Ánh xạ `(Item biến thể, BOM Component) -> (NVL, số lượng)` |
| **BOM Template** | Doctype chính | Gắn với 1 Item Template (`Has Variants=1`), 2 tab: Bảng Thành Phần BOM + Công Thức BOM. Chỉ 1 template được `Hoạt Động` / item cha |

### UI: Popup "Tạo Rule" (`bom_template.js`)
Trên dòng `Theo Rule` của Bảng Thành Phần BOM có nút **Tạo Rule** → popup 2 bước:
1. **Chọn Điều Kiện** — hiện toàn bộ đặc tính + giá trị đặc tính của Item cha, người dùng tick chọn tổ hợp (multi-check mỗi đặc tính)
2. **Chọn Nguyên Vật Liệu** — chọn NVL + số lượng

Xác nhận → server tính cartesian product các tổ hợp đã chọn, tìm toàn bộ Item biến thể khớp, tự sinh/ghi đè dòng vào bảng Công Thức BOM (không tạo trùng — nếu đã có dòng cùng `(item_to_manufacture, bom_component)` thì UPDATE tại chỗ).

### Engine tự động tạo BOM (`api/bom.py`, whitelisted `auto_create_bom(item_code, company)`)
Gọi từ nút **"Tạo BOM Tự Động"** trên Production Plan (bảng Select Items to Manufacture, field `custom_create_bom`).

Luồng xử lý:
1. Xác định Item cha (`variant_of`) → tìm BOM Template đang `is_active=1`
2. Đệ quy dựng cây BOM theo thứ tự **bottom-up** (post-order DFS): với mỗi thành phần `Theo Rule`, tra BOM Rule theo `(item_code, bom_component)`; nếu thành phần đó tự nó là 1 Item biến thể có BOM Template riêng → đệ quy tiếp (bán thành phẩm nhiều cấp)
3. So sánh cây BOM vừa dựng với BOM Default hiện tại (nếu có) ở **mọi cấp** — nếu khớp hoàn toàn thì giữ nguyên (`status: "valid"`), nếu bất kỳ cấp nào lệch thì **tạo lại toàn bộ cây** (không chỉ cấp lệch), submit theo thứ tự con→cha, gán Default mới, bỏ Default cũ

### Dữ liệu demo (giữ lại theo yêu cầu người dùng)
Chuỗi 3 cấp hoàn toàn cô lập, không đụng item thật: `Den pha` → `Den pha-200W-Tr-DN-HKLED` → `Module LED Test-Tr-Led Philips` → `Chip LED Module Test-Tr-Led Philips`. BOM Template: `BT-DEN-PHA`, `BT-MODULE-LED-TEST`, `BT-CHIP-LED-MODULE-TEST`.

## PHẦN II — Bậc Thợ & Giờ Công Chuẩn

| Field/Doctype | Vị trí | Ghi chú |
|---|---|---|
| **Employee Level** (Bậc Thợ) | Doctype mới | `employee_level` (tên/PK), `earnings_per_minute`, `performance_factor`, `team_fund_contribution_rate` |
| `custom_time_to_manufacture` | Item, tab Manufacturing | Phút sản xuất 1 sản phẩm |
| `custom_employee_type` | Employee | Select: Công nhân / Bán hàng / Kế toán (**đã có sẵn**, không phải field tôi tạo) |
| `custom_employee_level` | Employee | Link → Employee Level (**đã có sẵn**) |
| `custom_performance_factor_` | Employee | Fetch từ `custom_employee_level.performance_factor`, read-only (**đã có sẵn**, tên field có `_` thừa — giữ nguyên, không đổi) |

`employee.js`: cảnh báo mềm (`frappe.show_alert`, không chặn save) khi Loại nhân sự = Công nhân nhưng chưa gán Bậc Thợ. **Cố ý không bật ràng buộc bắt buộc** vì 33/38 nhân sự thật lúc audit chưa có dữ liệu.

## PHẦN III — Lịch Sản Xuất Thông Minh

### Doctype
| Doctype | Vai trò |
|---|---|
| **Employee Schedule** | Lịch làm việc hàng ngày (ca sáng/chiều/tăng ca). `start`/`end` fetch từ Shift Type; `start_time`/`end_time` = Date+giờ, tự tính, read-only |
| **Employee Allocation** | Khoảng thời gian 1 nhân sự tham gia 1 Work Order cụ thể. Validate chống trùng lịch (overlap) cho cùng nhân sự |
| **Work Order Employee** (child) | Gắn trên Work Order (`custom_work_order_employee`). Có `lock_start`/`lock_end` để khoá thủ công, `allocation_record` link tới Employee Allocation tương ứng |

Custom field trên Work Order: `custom_start_time` (mandatory), `custom_end_time`, `custom_estimated_completion_time_minutes`, `custom_required_completion_date__time` — 3 field sau **allow_on_submit=1** vì bị tính lại giữa chừng khi WO đã submit.

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

### Dữ liệu demo (giữ lại)
Nhân sự `PIII-TEST Nhan Su A/B/C` (`HR-EMP-00010/11/12`), Item `PIII-TEST-ITEM-A`, Work Order chính `MFG-WO-2026-00129` (đã reset về baseline khớp tài liệu: 478 phút / 8h28 ngày sau), cộng 2 Work Order phụ tạo xung đột lịch cho nhân sự A/C.

## Hooks đăng ký (hooks.py)

```
doctype_js:
  BOM Template     -> public/js/bom_template.js
  Production Plan  -> public/js/production_plan.js
  Employee         -> public/js/employee.js
  Work Order       -> public/js/work_order.js

doc_events:
  Work Order.on_update -> controllers.python_hook.work_order.sync_employee_allocation_on_finish

fixtures:
  Custom Field where module = "MBWNext HKLed"   # tự động bắt field mới, không cần sửa tay khi thêm field
```

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

## Quy ước code

- Python: tab indent, double quote, line-length 110 (ruff, theo `pyproject.toml`)
- Server hooks: `controllers/python_hook/<doctype>.py`, khai báo qua `doc_events`
- API whitelisted: `api/<domain>.py`
- Client hooks: `public/js/<doctype>.js`, khai báo qua `doctype_js`
- Patch một lần (sửa dữ liệu/field đã tồn tại): `patches/`, khai báo trong `patches.txt` mục `[post_model_sync]`, luôn viết idempotent (check tồn tại trước khi tạo/sửa)

## Cách chạy

```bash
cd /home/pc/test_core
bench start
bench --site hkled.com migrate
bench build --app mbwnext_hkled
bench --site hkled.com export-fixtures --app mbwnext_hkled   # sau khi thêm Custom Field mới (nhớ set module=MBWNext HKLed)
```

## Tài liệu liên quan

Tài liệu nghiệp vụ gốc: `TÀI LIỆU NGHIỆP VỤ NÂNG CẤP GIAI ĐOẠN 1 HKLED.docx` (không lưu trong repo). Bộ test case tay (Artifact, chưa lưu file trong repo):
- Phần I — BOM Template & Tạo BOM Tự Động: 20 test case (A–F)
- Phần II — Bậc Thợ & Giờ Công Chuẩn: 11 test case (A–C)
- Phần III — Lịch Sản Xuất Thông Minh: 18 test case (A–E)
