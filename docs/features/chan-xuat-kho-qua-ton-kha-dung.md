# Chặn xuất kho quá tồn khả dụng

**Khách hàng:** HKLED
**Người cung cấp thông tin:** Thắng (thangdo@mbw.vn) — thuật lại lời khách
**Người trực tiếp thao tác đã trao đổi:** ❌ **chưa** — người chịu ảnh hưởng là **thủ kho**
**Ngày tách:** 24/08/2026 · **Cập nhật:** 25/08/2026 (chốt đường B — xem §4)
**PM Project:** PM-PRJ-00003 · **PM Feature:** PM-FEAT-00034

> Tách ra từ **mục 7.3** của
> [Kiểm tra tồn kho và nguồn lực trên Đơn Bán](kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md)
> (PM-FEAT-00023). Anh Thắng chốt tách 24/08, bình luận `ptmjq2t3nj`.

## Đầu bài gốc (mục 7.3 của Phần IV)

> Không cho xuất kho quá số tồn khả dụng — tức phần tồn đã bị các Đơn Bán khác ghim thì
> không được đem xuất cho việc khác.

---

## 1. ERPNext v15 có sẵn cơ chế giữ chỗ — nhưng **KHÔNG dùng được cho HKLED**

> ⚠ **ĐỌC §4 TRƯỚC KHI DÙNG MỤC NÀY.** Mục 1 và 2 là bản khảo sát ngày 24/08, khi đó kết luận
> là "dùng thẳng cơ chế lõi". Kết luận đó **đã bị bác ngày 25/08** — hai yêu cầu của HKLED (gộp
> pool nhiều kho, và bóc BOM giữ chỗ NVL) đều nằm ngoài khả năng của cơ chế lõi. Chi tiết ở §4.
>
> Giữ nguyên mục 1–2 vì phần mô tả cơ chế lõi vẫn **đúng và vẫn hữu ích**: nó là chuẩn để đối
> chiếu khi tự dựng đường B, nhất là bảng 8 chứng từ ở §1.1 và cách lõi tự miễn trừ chứng từ của
> chính đơn đó ở §1.2. Chỉ **kết luận nên dùng** là sai, không phải phần mô tả.

Chuỗi có sẵn của lõi, đủ từ đầu đến cuối:

| Mắt xích | Ở đâu trong app `erpnext` |
|---|---|
| Ô tích **Reserve Stock** cấp chứng từ | `selling/doctype/sales_order/sales_order.json` |
| Ô tích từng dòng hàng, mặc định **1** | `selling/doctype/sales_order_item/sales_order_item.json` → `reserve_stock` |
| Submit đơn → sinh bản giữ chỗ | `sales_order.py:439` → `create_stock_reservation_entries()` |
| Cộng dồn vào kho | `Bin.reserved_stock` — `stock/doctype/bin/bin.py:225` |
| **Chỗ chặn xuất** | `stock/stock_ledger.py:2072` — `if args.reserved_stock: validate_reserved_stock(args)` |
| Cổng bật/tắt | `Stock Settings.enable_stock_reservation` (site đang để **0**) |

⚠ Nghĩa là ô **"Ghim Tồn Khả Dụng"** đang thiết kế ở Phần IV §2 chính là trường `reserve_stock`
sẵn có, chỉ khác nhãn. Chạy song song hai cơ chế giữ chỗ là **trừ trùng** — cùng một lượng tồn
bị giữ hai lần, không có gì báo.

### 1.1 Chỗ chặn của lõi đặt đúng hơn chỗ mình định đặt

Bản đầu định hook `Stock Entry` · `Delivery Note` · `Material Request`. Lõi chặn tại
**`make_sl_entries`** (`stock_ledger.py:55`) — nút cổ chai mà **mọi** chứng từ động vào kho đều
phải đi qua. Đếm chính xác: **8 chứng từ** gọi `self.update_stock_ledger()`, và **cả 8 đều có thể
làm giảm tồn** ở một chế độ nào đó:

| Chứng từ | Khi nào nó rút tồn |
|---|---|
| Delivery Note | xuất bán — *bản đầu có tính* |
| Stock Entry | xuất kho mọi mục đích — *bản đầu có tính* |
| **Sales Invoice** | khi tích `update_stock` — bán thẳng, không qua Phiếu xuất kho |
| **Subcontracting Receipt** | tiêu hao NVL đưa đi gia công — HKLED có dùng (`dịch vụ gia công`) |
| **Purchase Receipt** | phiếu **trả hàng** nhà cung cấp |
| **Purchase Invoice** | khi tích `update_stock`, bản trả hàng |
| **Stock Reconciliation** | kiểm kê điều chỉnh giảm |
| **Asset Capitalization** | tiêu hao vật tư để hình thành tài sản |

Bản đầu định hook 3 doctype ➜ **để thủng 6 chứng từ**, và kiểu thủng này chỉ lộ ra sau khi kho
đã xuất lọt.

### 1.2 Chỗ khó nhất cũng đã được giải sẵn

Bài toán *"phiếu thuộc chính đơn đã ghim thì vẫn phải cho xuất"* — thứ sinh ra chỗ treo
**26/39 Lệnh sản xuất không lần ra Đơn Bán** — lõi xử bằng **thứ tự thao tác lúc submit**
(`delivery_note.py:454`):

```python
self.update_stock_reservation_entries()   # nhả phần giữ chỗ CỦA CHÍNH ĐƠN NÀY trước
...
self.update_stock_ledger()                # rồi mới kiểm tra
```

Kèm nguyên chú thích của họ: *"Updating stock ledger should always be called after updating
prevdoc status, because updating reserved qty in bin depends upon updated delivered qty in SO"*.

➜ Không cần lần vết `Stock Entry → Work Order → Sales Order`. **Chỗ treo 26/39 tan**, không cần
anh Thắng quyết "cho qua hay chặn" nếu đi đường A.

---

### 1.3 Lõi chặn ở lúc XUẤT KHO, không chặn lúc lưu đơn — đo được trên site

Chỗ này dễ hiểu nhầm thành "bật `reserve_stock` của lõi là chặn được rồi". **Không phải.**

Đợt thử nghiệm 25/08 của Thắng cho bằng chứng trực tiếp — tồn `Thành phẩm 1` chỉ có **26**:

| Đơn | Tích ô cấp chứng từ | Đặt | Giữ chỗ được | Kết quả Submit |
|---|---|---|---|---|
| `SO-26-00009` | ✅ | 30 | **26** (thiếu 4) | **qua bình thường** |
| `SO-26-00010` | ✅ | 5 | **0** | **qua bình thường** |
| `SO-26-00007` | ❌ | 30 | 0 | qua bình thường |
| `SO-26-00008` | ❌ | 1 | 0 | qua bình thường |

Không cảnh báo, không chặn Submit, không dấu hiệu nào trên chứng từ nói "đơn này còn 4 cái chưa
giữ được". Lõi **giữ được bao nhiêu hay bấy nhiêu rồi cho qua**.

Phân vai chính xác:

| Lúc | Lõi có chặn? |
|---|---|
| Lưu / Submit **Đơn Bán** thiếu hàng | **Không** |
| **Xuất kho** ăn vào phần đơn khác đã giữ | **Có** — `stock_ledger.py:2073` gọi `validate_reserved_stock(args)` ngay trong đường ghi sổ kho |

➜ Đúng phần *chặn xuất kho* thì lõi làm được, và làm ở chỗ tốt hơn chỗ mình định đặt (§1.1).
Cái lõi không làm được vẫn là hai thứ ở §2: **pool nhiều kho** và **bóc BOM**.

⚠ Hai ô tích, hai mức: `Sales Order.reserve_stock` (cấp chứng từ) `default: 0` — **phải có người
tích**, cơ chế lõi không chạy ngầm. Nhưng `Sales Order Item.reserve_stock` (cấp dòng) `default: 1`,
nên **tích ô cấp chứng từ là mọi dòng hàng tồn kho ghim theo ngay**, không có bước chọn từng dòng.
Bằng chứng: `SO-26-00007/00008` có dòng tích sẵn mà giữ chỗ = 0, vì ô cấp chứng từ để trống.

➜ **Ghim thiếu thì cảnh báo hay chặn?** Câu này **đã có đáp**, không cần hỏi lại: mục 6.2 bản phân
tích của Thắng chốt *"mọi SO đều Ghim được, kể cả khi Available = 0"* — đơn vẫn vào hàng đợi, vẫn
hiện phần thiếu để lập Yêu cầu Vật tư. Trùng khít hành vi lõi đo được ở trên.

## 2. Chỗ cơ chế lõi KHÔNG làm được

`Stock Reservation Entry` gắn **cứng** vào dòng hàng của Đơn Bán:

- `voucher_detail_no` → `Sales Order Item`
- `update_reserved_qty_in_voucher()` ghi ngược `stock_reserved_qty` vào đúng dòng đó
- `validate_stock_reservation_settings()` chỉ cho `voucher_type = "Sales Order"`

➜ **Chỉ giữ chỗ cho mặt hàng nằm trên đơn. Không giữ được NVL bóc từ BOM.**

Mà Phần IV §5 — anh Thắng bổ sung 24/08 — yêu cầu đúng cái đó: *"đơn đã ghim thì NVL bóc từ BOM
mặc định cũng bị ghim theo"*. Đây là khoảng cách thật, **không lách được bằng cấu hình**.

Và với HKLED khoảng cách này có thể là phần quan trọng nhất: họ làm theo đơn, thành phẩm gần như
không có tồn — giữ chỗ thành phẩm là giữ một con số 0. Thứ đáng giữ là **vật tư cho lô sắp sản
xuất**. ⚠ Nhưng site chưa có giao dịch thật (**0** Phiếu xuất kho, **6** mặt hàng có tồn ≠ 0) nên
đây là **suy đoán cần hỏi**, không phải kết luận.

---

## 3. ~~Rủi ro~~ 59k mặt hàng khai serial/lô — **đã tan 25/08**

> ✅ Rủi ro trong mục này **không còn**, vì nó chỉ tồn tại nếu dùng cơ chế lõi. Đường B chốt ngày
> 25/08 tính tồn khả dụng ở tầng bỏ qua serial/lô hoàn toàn (chỉ tầng xuất kho thực tế mới tuân
> thủ), nên không còn chuyện bị bắt chỉ đích danh lô/serial có thật lúc giữ chỗ.
>
> Câu hỏi "59k mặt hàng khai serial/lô có đúng ý khách không" cũng đã có đáp: **đúng, cố ý**, đều
> là mặt hàng thành phẩm — xem §5. Giữ nguyên số đo bên dưới vì chúng vẫn cần cho tầng xuất kho.

Đo 24/08 trên `hkled.com`:

| | |
|---|---|
| Item có `has_serial_no` | **59.051** |
| Item có `has_batch_no` | **59.053** |
| Item có tồn ≠ 0 | **6** |
| Stock Reservation Entry hiện có | **0** |
| `enable_stock_reservation` | **0** |
| `allow_negative_stock` | 0 (đang chặn âm kho — tốt) |

Với mặt hàng có serial/lô, SRE chuyển sang `reservation_based_on = "Serial and Batch"` và đòi
**chỉ đích danh serial/lô có thật** lúc giữ chỗ (`auto_reserve_serial_and_batch`, mặc định bật).
Site chỉ 6 mặt hàng có tồn ➜ bật lên là phần lớn đơn giữ chỗ hỏng, hoặc giữ được 0.

**Phải thử trước khi hứa với khách.** Và nên hỏi lại: 59k mặt hàng khai serial/lô có đúng ý khách
không, hay là hệ quả của đợt nạp danh mục (PM-TASK-00061/67).

⚠ Thêm một chỗ phải khớp: SRE giữ chỗ theo **đúng kho ghi trên dòng Đơn Bán**, và **không nhận
kho nhóm**. Phần IV §3 lại loại trừ *Nhóm kho lỗi* / *Nhóm kho trung chuyển* khỏi tập kho. Nếu
dòng đơn trỏ vào kho trung chuyển thì Phần IV không đếm mà SRE vẫn giữ — hai số lệch nhau.

---

## 4. Ba đường đi

| | Cách làm | Được | Mất |
|---|---|---|---|
| **A** | Bật `enable_stock_reservation`, dùng thẳng `reserve_stock`, **bỏ custom field của Phần IV** | Gần như 0 dòng code · phủ đủ 8 chứng từ · tự miễn trừ đơn của chính nó · Frappe bảo trì | Không ghim được NVL |
| **B** | Tự làm hết: hàm kiểm dùng chung gọi từ `before_submit` của mọi đường xuất | Ghim được NVL theo BOM | Tự gánh 8 chứng từ · tự giải bài 26/39 · tự bảo trì · **bắt buộc tắt SRE** |
| **C** | A cho thành phẩm + B chỉ cho NVL, **một hàm tính duy nhất** | Đủ nghiệp vụ | Hai cơ chế cùng lúc — đúng bẫy trừ trùng. Phải tách tuyệt đối: SRE lo dòng trên đơn, custom lo NVL, **không chồng mặt hàng nào** |

### ⚠ ĐÃ CHỐT 25/08: đi đường B. Đường A **chết**, không phải "để sau"

Bản đầu của mục này đề nghị làm A trước. **Sai** — Thắng phản biện ngày 25/08 và em kiểm lại
trong code ERPNext thì cả hai lý do anh ấy nêu đều đứng:

| Yêu cầu của HKLED | Vì sao cơ chế lõi không đáp được |
|---|---|
| Tồn khả dụng gộp **toàn bộ kho**, trừ Nhóm kho lỗi và Nhóm kho trung chuyển | `get_available_qty_to_reserve(item_code, warehouse)` tính cho **đúng một kho**. Trỏ đơn vào **kho nhóm** để gộp thì lõi chặn thẳng ở 3 chỗ: `Stock cannot be reserved in group warehouse` |
| Ghim phải bóc BOM giữ chỗ NVL / bán thành phẩm | `Stock Reservation Entry.voucher_type` là `DF.Literal["", "Sales Order"]` — bản ghi giữ chỗ chỉ trỏ được về Đơn Bán, không trỏ được về NVL |

Hai giới hạn này chính là hai chỗ đã ghi ở §3 bên trên, lúc đó mới coi là "chỗ phải khớp".
Hoá ra chúng không phải chi tiết cần khớp — chúng là **hai bức tường** loại bỏ hẳn đường A.

Lập luận cũ "làm A trước không phí" cũng sai: A không phải tập con của B. A chặn ở tầng ghi sổ
kho theo từng kho; B phải chặn theo pool nhiều kho và theo cây BOM. Dựng A xong vẫn phải dựng
lại từ đầu.

**Hệ quả tốt duy nhất của việc A chết:** rủi ro 59k mặt hàng serial/lô ở §3 **tự tan**. Tầng tính
khả dụng của đường B bỏ qua serial/lô hoàn toàn (chỉ tầng xuất kho thực tế mới tuân thủ), nên
không còn chuyện bị bắt chỉ đích danh lô/serial có thật lúc giữ chỗ.

### Nếu chốt B — hai ràng buộc bắt buộc

1. **Không hook 3-4 doctype rời.** Một hàm kiểm dùng chung, gọi từ `before_submit` của từng
   đường, và **test hồi quy liệt kê đủ 8 chứng từ ở §1.1** — thiếu một cái là thủng.
2. **Dùng lại đúng hàm tính tồn khả dụng của Phần IV**, không viết công thức thứ hai. Cùng lý do
   đã ghi ở Phần IV §7: hai chỗ lệch nhau một điều kiện là chặn sai mà nhìn mắt không ra.

### Material Request rút khỏi danh sách chặn

Nó **không sinh Stock Ledger Entry**, không lấy hàng đi đâu. Chặn ở đó là chặn một *dự định* ➜
phải là **cảnh báo**, không phải `frappe.throw`. (Bản đầu của tài liệu này xếp nhầm nó ngang với
Phiếu xuất kho.)

---

## 5. Hai câu chặn — ĐÃ CÓ ĐÁP 25/08

1. **Ghim là để giữ *thành phẩm* hay giữ *vật tư*?** ➜ **Cả hai.** Giữ chỗ chính mặt hàng nếu
   còn tồn; phần thiếu mới bóc BOM giữ chỗ bán thành phẩm / NVL; bán thành phẩm thiếu thì bóc
   tiếp BOM của nó. Tức netting theo từng cấp. ➜ chốt đường B.
2. **59k mặt hàng khai serial/lô có đúng ý khách không?** ➜ **Đúng, cố ý**, và đều là mặt hàng
   thành phẩm. Không phải hệ quả của đợt nạp danh mục.

Thêm một số phải đính chính: **"1 mặt hàng Gia công" trên site là item Thắng tự thêm để test**,
không phải dữ liệu khách. Số thật của khách là **0** — khách có khai loại Gia công từ đầu nhưng
danh sách mặt hàng gửi sang chưa có mã nào thuộc loại đó.

Và một chỗ phải báo dù chưa ai hỏi: **Phần IV §2 đang khai custom field trùng chức năng với
`reserve_stock` của lõi** — chốt đường A thì phải bỏ field đó khỏi spec Phần IV **trước khi code**.

## 5b. Chỗ nặng nhất còn lại: lúc Ghim thì **chưa có BOM để bóc**

Phát hiện 25/08, sau khi đường B được chốt. Đây là chỗ có thể làm cả tính năng thành vô nghĩa,
nên phải giải trước khi dựng mockup.

**Ghim xảy ra ở Đơn Bán. Nhưng BOM ở app này chỉ sinh ra khi người dùng bấm nút *Tạo BOM Tự Động*
trên Kế Hoạch Sản Xuất** (`api/bom.py::auto_create_bom`, gọi từ `controllers/js/production_plan.js`)
— tức là **sau** Đơn Bán, có khi vài ngày sau.

Đo trên `hkled.com` ngày 25/08:

| | |
|---|---|
| Mặt hàng khai *Phương pháp bổ sung = Sản xuất* | **59.742** |
| Mặt hàng có `default_bom` | **5** |
| BOM đang `is_active` | **7** |

Nghĩa là ngay tại thời điểm bấm Ghim, gần như **không mặt hàng nào có bản ghi BOM**. Theo quy tắc
15 của bản phân tích Thắng gửi (*không có BOM active → coi như Mua hàng + cảnh báo*), engine nổ
BOM — đúng thứ vừa được dùng làm lý do loại bỏ đường A — **không có gì để chạy**.

### Đường ra: đọc BOM Template, không đọc bản ghi BOM

App đã có sẵn bộ giải thành phần từ template mà **không cần tạo BOM trước**, đều nằm trên nhánh
chính: `api/bom.py::get_active_template`, `resolve_components`, `get_template_raw_materials`.
Ghim nên đi qua đường này. Không phải viết mới, chỉ là đấu nối.

### ⚠ Ghim KHÔNG nên tạo BOM — chỉ đọc thành phần từ template

Ra ngày 25/08, sau khi đối chiếu chéo với phiên đang giữ mảng BOM (`ab01c6be`).

Khách chốt nguyên văn: *"đủ rule và có BOM Template thì **tự sinh BOM**, rồi chạy tính toán ghim"*.
Làm đúng chữ đó là gọi `auto_create_bom`, và kéo theo ba cái giá:

| Giá | Chi tiết |
|---|---|
| Quyền | `auto_create_bom` đòi `frappe.has_permission("BOM", "create")`. Người tích ô Ghim là nhân viên bán hàng |
| **Đổi dữ liệu gốc** | `create_bom` submit BOM mới rồi **gỡ cờ `is_default` của bản cũ**. App **đã vấp đúng chuyện này một lần** — ghi đè `is_default` lên BOM đang được Work Order thật tham chiếu, phải cancel và khôi phục tay (xem *Bài học quan trọng* trong `CLAUDE.md`) |
| Lỗi trộn lẫn | `auto_create_bom` throw ở **4** chỗ, và tầng dưới (`build_bom_tree` → `resolve_components` → Server Script `bom_qty.py`) còn ~30 chỗ throw nữa. Bắt exception làm luồng điều khiển sẽ nuốt cả **lỗi cấu hình hệ thống** lẫn *"chưa đủ rule"* vào chung một nhánh |

**Nhưng Ghim không cần bản ghi BOM.** Nó chỉ cần biết **NVL và số lượng** để trừ dần. Thứ đó lấy
được mà không tạo gì:

| Hàm (đã có sẵn, `api/bom.py`) | Trả về | Có throw? |
|---|---|---|
| `get_active_template(item_code)` | tên template, hoặc `None` | **không** — chỉ `db.get_value` |
| `get_template_raw_materials(item_code)` | `{}` nếu không template · `{"error": …}` nếu tính không ra · `items` + `qty_defaulted` nếu được | **không** với lỗi công thức (cố ý; nó còn cắt `frappe.local.message_log` để trình duyệt khỏi hiện cụm đỏ). Chỉ throw khi thiếu quyền `BOM Template read` |

➜ **Nhánh rẽ của khách viết được bằng đúng hai hàm này**, không cần `try/except` quanh
`auto_create_bom`, không cần viết vị từ mới:

```
tpl = get_active_template(ma)
nếu tpl là None                      -> chỉ ghim thành phẩm
kq = get_template_raw_materials(ma)
nếu kq rỗng, có "error", hoặc qty_defaulted khác rỗng
                                     -> chỉ ghim thành phẩm  (chưa đủ rule)
ngược lại                            -> netting theo kq["items"]
```

➜ Đi hướng này thì **hai câu đang treo ở §5b tự tan**: không cần cấp quyền `BOM create` cho nhân
viên bán hàng (chỉ cần `BOM Template read`), và không đụng `is_default`.

Tạo BOM thật vẫn xảy ra — nhưng ở **Production Plan / Work Order**, đúng chỗ nó đang nằm, do người
có quyền bấm.

⚠ Đây là chỗ **làm đúng chữ sẽ tệ hơn làm đúng ý**. Khách mô tả *cơ chế họ hình dung*
("tự sinh BOM"), còn thứ họ *cần* là ghim được xuống NVL. Phải hỏi lại khách trước khi code —
đã hỏi qua PM, dẫn chính tai nạn `is_default` ở trên làm căn cứ.

Nếu khách vẫn muốn sinh BOM ngay lúc Ghim thì phương án dự phòng là cách mảng BOM đang làm trên
form BOM: **bấm nút + hộp thoại xác nhận** nói rõ *"sẽ tạo và DUYỆT n BOM thật"*, không tạo ngầm.

---

### Nhưng độ phủ template mới ~17% — câu này cần khách trả lời

| | |
|---|---|
| BOM Template hiện có | **8** — `DP01S`, `DP03S`, `DD11S050`, `M30S050-A/B`, `M50S050-A/B`, `VDP0X` |
| Biến thể được 8 template phủ | **10.380** |
| Mặt hàng khai *Sản xuất* | 59.742 |

Còn **83%** không bóc được gì và sẽ rơi vào nhánh cảnh báo. Câu chặn: HKLED có dựng BOM Template
cho **hết các dòng đèn** không, hay chấp nhận 83% chỉ giữ chỗ ở mức thành phẩm? Nếu trả lời "dựng
dần" thì phải biết **dựng tới đâu mới bật tính năng** — không thì go-live xong tính năng chạy
đúng cho 17% mặt hàng, và không ai biết trước điều đó.

⚠ Đây là chỗ **tôi hỏi thiếu** hôm 24/08: mục "việc kế tiếp" khi đó chỉ liệt 2 câu ở §5, không có
câu này. Ghi lại để lần sau soát danh sách câu chặn theo *toàn bộ đường đi của dữ liệu*, không chỉ
theo phần mình vừa khảo sát.

---

## 6. Chỗ chặn cũ — đã đóng hoặc đổi trạng thái

| Bản đầu 24/08 | Giờ |
|---|---|
| Lệnh sản xuất không lần ra Đơn Bán (26/39) | **Tan nếu đi đường A** — lõi giải bằng thứ tự submit (§1.2). Chỉ còn là câu hỏi nếu chốt B |
| Bật `Stock Reservation` hay tự làm | **Vẫn là câu hỏi chính** — chính là lựa chọn A/B/C ở §4 |
| Chưa hỏi thủ kho | **Vẫn treo.** Cần biết có ca nào buộc phải xuất vượt, và lúc đó xử lý thế nào |

## 7. Việc kế tiếp

1. ~~Anh Thắng trả lời 2 câu ở §5~~ — **xong 25/08**, xem §5.
2. **Khách trả lời câu độ phủ BOM Template ở §5b.** Đây là câu chặn duy nhất còn lại.
3. Có đáp rồi mới dựng **mockup**: màn hình Ghim trên Đơn Bán + câu thông báo chặn (chữ thủ kho
   nhìn thấy) + cách hiển thị phần thiếu. Khách duyệt mockup rồi mới code.
4. Test case bắt buộc có `TC-REGR` liệt kê **đủ 8 chứng từ ở bảng §1.1** — đường B tự gánh cả 8,
   thiếu một cái là thủng.
5. Thêm cho đường B: `TC-VALID` phải phủ ca **mặt hàng Sản xuất không có template** (83% ở §5b) —
   đúng nhánh cảnh báo của quy tắc 15.

> Hạn 05/09/2026 để **tạm** cho đủ trường bắt buộc của PM — chưa phải hạn khách chốt.
