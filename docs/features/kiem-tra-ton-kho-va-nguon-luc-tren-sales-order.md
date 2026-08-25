# Kiểm tra tồn kho và nguồn lực trên Đơn Bán

**Khách hàng:** HKLED
**Người cung cấp thông tin:** Thắng (thangdo@mbw.vn) — thuật lại lời khách
**Người trực tiếp thao tác đã trao đổi:** ❌ **chưa** — xem "Còn thiếu ở khâu khảo sát"
**Ngày khảo sát:** 19/08/2026
**PM Project:** PM-PRJ-00003 · **PM Feature:** PM-FEAT-00023

> ⚠ **Khách không có tài liệu gốc**, chỉ trao đổi miệng. Phần "Đầu bài gốc" dưới đây là
> lời anh Thắng thuật lại, không phải nguyên văn khách. Đã hỏi và anh Thắng xác nhận
> không có file/ảnh/biên bản nào.

## Đầu bài gốc (anh Thắng thuật lại, 19/08)

> Khi nhân viên bán hàng tạo đơn hàng bán có thể check được tình hình tồn kho hiện tại
> có đủ không để có thể báo cho khách hàng. Mặt hàng thuộc phương pháp bổ sung mua hàng
> thì check tồn còn đủ không; mặt hàng thuộc sản xuất hoặc gia công thì check tồn hiện
> tại còn đủ không, nếu không đủ thì cần sản xuất hoặc gia công, lúc ấy check tiếp
> nguyên vật liệu còn lại có đủ để sản xuất hoặc gia công không. Nếu không đủ nhân viên
> bán hàng có thể tư vấn khách đổi mẫu khác hoặc hẹn ngày giao hàng xa hơn, mục đích
> chỉ để tham khảo.

## Bối cảnh

- **Vì sao cần bây giờ:** nhân viên bán hàng đang nhận đơn mà không biết có giao được không.
- **Quyết định người dùng đưa ra sau khi xem kết quả:** nhận đơn · đổi mẫu khác · hẹn ngày
  giao xa hơn. Đây là 3 lối ra, và là lý do kết quả **chỉ mang tính tham khảo** — không
  ghim vào đơn, không sinh chứng từ.
- **Người bấm nút:** nhân viên bán hàng, ngay trên form Đơn Bán.

## Phạm vi

✅ Làm lần này
- Nút tính toán trên Đơn Bán, kết quả hiện trong popup **3 bảng** (xem PM Feature/Notes).
- Tồn khả dụng tùy chỉnh riêng, điều khiển bằng checkbox **Ghim tồn khả dụng**.

❌ Không làm lần này
- Không sinh Yêu cầu mặt hàng / Đơn mua / Lệnh sản xuất. Chỉ hiển thị.
- Không ghi kết quả xuống Đơn Bán, không ảnh hưởng Stock Balance / Stock Ledger / Bin.
- Kế hoạch mua theo kỳ là **PM-FEAT-00030 (Phần V)**, tính năng riêng.

## Quy mô sử dụng

| | |
|---|---|
| Item trên site | 61.142 (60.822 mặt hàng thường) |
| BOM trên site | **5** — xem rủi ro R1. Đo lại 20/08: **1/59.692** mặt hàng “Sản xuất” có BOM hoạt động |
| Item có Thời Gian Sản Xuất > 0 | **3** — xem rủi ro R2 |
| Nhân sự loại *Công nhân* | 3 |
| Số dòng một đơn hàng thật | **1–2 mặt hàng**, hiếm khi hơn (khách trả lời 20/08) |
| Thời gian chờ chấp nhận được | *càng nhanh càng tốt* — chưa ra số, nhưng quy mô trên cho phép dưới 1 giây |

## Rủi ro đã phát hiện — chặn việc viết spec

**R1 — Gần như không có BOM để bóc tách.** 61.142 Item / 5 BOM. Chưa chốt: mặt hàng Sản
xuất mà không có BOM thì (a) báo lỗi · (b) coi như phải mua · (c) tự sinh từ BOM Template.
Đây là quyết định kiến trúc, ảnh hưởng cả tốc độ lẫn kết quả.

**R2 — Thời Gian Sản Xuất (Phút) gần như chưa khai.** 3/60.822 mặt hàng có giá trị.
Bảng 3 sẽ ra gần 0 phút và **luôn kết luận "Đủ"** — sai mà không có gì báo. Loại lỗi tệ
nhất: im lặng và ra số đẹp.

**R4 — Ngày giao hứa với khách suy từ dữ liệu rỗng.** *(phát sinh 20/08)* Khách xin nút
**Hẹn lại ngày giao** gợi ý ngày sớm nhất lấy được hàng. Ba nguồn để tính đều trống: thời
gian sản xuất **3/61.143**, BOM hoạt động **1/59.692**, thời gian mua hàng về **0/61.143**
(và 0 mặt hàng có nhà cung cấp mặc định). Nặng hơn R2: R2 chỉ sai trong nội bộ, R4 là con
số sai được sale đọc lên rồi **hứa với khách hàng**.

**R3 — Đơn đang kiểm có tự trừ chính nó không?** Nếu chính nó cũng tích *Ghim tồn khả dụng*
thì theo công thức nó tự trừ số lượng của mình, báo thiếu nhiều hơn thực tế.

## Còn thiếu ở khâu khảo sát

Theo `erpnext-mbwnext-requirement-analysis`, bốn mục dưới đây đáng ra phải có trước khi
sang giai đoạn sau. Ghi lại để không ai tưởng đã khảo sát đủ:

- [ ] **Chưa hỏi người trực tiếp thao tác** — mới qua anh Thắng, chưa gặp nhân viên bán hàng.
- [~] **Tài liệu khách** — vẫn không có Excel/mẫu giấy, nhưng 20/08 đã có **ảnh chụp trao đổi với khách**
  (PM-FEAT-00023, bình luận `s3da1fpj7t`). Đây là nguồn gốc đầu tiên không qua thuật lại.
- [~] **Ngoại lệ** — đã hỏi được một vế: *không có đơn nào được miễn kiểm* (kể cả đơn mẫu,
  đơn nội bộ, đơn có tồn sẵn). Còn thiếu: hiện khách đang làm tay ra sao và sai ở đâu.
- [x] **Quy mô** — đã hỏi được 20/08: 1–2 mặt hàng/đơn, BOM dưới 10 NVL. Rủi ro tốc độ coi như gỡ.

Mockup ở giai đoạn 2 chính là để lấp mấy chỗ này: đưa màn hình cụ thể cho khách chê thì
moi được nhiều hơn hỏi mở.

## Yêu cầu chi tiết

Giữ bản chuẩn duy nhất ở **PM-FEAT-00023 → mục Notes**, không chép sang đây để tránh hai
bản lệch nhau. Bản phân tích của anh Thắng: PM-DOC-00294.

---

# Spec kỹ thuật

> Viết 24/08/2026, sau khi anh Thắng chốt R1/R2/R3 và 5 mục phản hồi của khách
> (PM-FEAT-00023 bình luận `511jt3rrru`, đã chép vào Notes mục 9).
> Yêu cầu gốc giữ ở **Notes**; file này chỉ nói **làm thế nào**.

## 1. Tầng và chỗ đặt code

Toàn bộ nằm ở **app khách `mbwnext_hkled`** — logic tồn kho này bám vào *Phương pháp bổ sung*
và BOM Template, cả hai đều là thứ riêng của HKLED. Không đụng app lõi.

| Việc | File |
|---|---|
| API tính toán | `api/kiem_tra_ton_kho.py` (mới) |
| Nút + popup trên Đơn Bán | `controllers/js/sales_order.js` (đã có, thêm vào) |
| Custom Field | `patches/add_sales_order_ghim_fields.py` (mới) + `fixtures/custom_field.json` |
| Chặn xuất kho (mục 7.3) | `controllers/python_hook/stock_entry.py` (đã có, thêm hàm) |

⚠ Thuộc tính lâu dài của Custom Field phải nằm trong **fixtures**, patch chỉ để tạo lần đầu —
`sync_fixtures` chạy **sau** patches nên fixtures thắng. Đã vấp ở C1 (`mandatory_depends_on`).

## 2. Custom Field mới

| DocType | Field | Kiểu | Ghi chú |
|---|---|---|---|
| Sales Order | `custom_ghim_ton_kha_dung` | Check | Tích = giữ chỗ tồn cho đơn này |

Chỉ **một** field mới. `custom_reserved_qty` **không** tạo cột trên `Bin` — tính động lúc bấm
nút. Đây là ràng buộc đã chốt: *không đụng Stock Balance / Stock Ledger / Bin*.

> ✅ **ĐÃ CHỐT 25/08 — GIỮ `custom_ghim_ton_kha_dung`.** PM-FEAT-00034 chốt **tự làm**
> (đường B): cơ chế `Stock Reservation Entry` của lõi chỉ tính tồn theo **một kho** và chỉ giữ
> chỗ được **mặt hàng trên đơn**, không giữ được NVL trong BOM — hai thứ HKLED đều cần. Nên
> field của mình không phải bản sao, nó làm việc mà lõi không làm được.
>
> ⚠ **NHƯNG hai ô tích vẫn sẽ cùng hiện — và đây là vấn đề THẬT, không còn là giả định.**
> `Sales Order.reserve_stock` của lõi có `depends_on: eval: (doc.docstatus == 0 || doc.reserve_stock)`,
> tức **không** phụ thuộc `enable_stock_reservation`. Lõi chỉ ẩn nó bằng JS
> (`selling/doctype/sales_order/sales_order.js:120-123`) khi tính năng **tắt**.
>
> Trên `hkled.com` ngày 25/08 lúc 11:20 `enable_stock_reservation` đã được bật **0 → 1** để thử
> nghiệm cơ chế lõi. Kiểm trên form thật lúc 14h: ô *Reserve Stock* **đang hiện**. Nghĩa là khi
> dựng `custom_ghim_ton_kha_dung`, người dùng sẽ thấy hai ô cùng nghĩa.
>
> Tệ hơn ô tích: bật tính năng thì lõi ghi `Bin.reserved_stock` thật (hiện đang có 26 trên
> `Thành phẩm 1`), thành **hai sổ giữ chỗ chạy song song** — đúng cái bẫy trừ trùng đã ghi ở
> §4 của `chan-xuat-kho-qua-ton-kha-dung.md`. Bảng 1 của Phần IV tính tồn khả dụng theo logic
> riêng, sẽ lệch với con số lõi đang giữ mà không ai giải thích được vì sao.
>
> ➜ **Trước khi code Phần IV, phải tắt `enable_stock_reservation` về 0** và dọn SRE do đợt thử
> nghiệm sinh ra. Không tắt thì dev và test đều đo trên nền đã nhiễu.
> Xem `chan-xuat-kho-qua-ton-kha-dung.md`.

## 3. Tập kho

Tồn (cả thực tế lẫn khả dụng) **loại trừ** kho con của hai nhóm:

- `Nhóm kho lỗi - HKL`
- `Nhóm kho trung chuyển - HKL`

Hai nhóm này là `Warehouse` có `is_group = 1`, con của `Kho Tổng - HKL`. Lấy kho hợp lệ bằng
`lft/rgt` của cây Warehouse chứ **đừng so tên**: tên có hậu tố công ty (`- HKL`) và sẽ đổi khi
lên site khác.

⚠ `MBWNext System Setting` có sẵn `warehouse_error` / `bad_stock_warehouse` nhưng **đang để
trống**. Đừng đọc hai trường đó — hiện không mang giá trị nào.

## 4. Thuật toán — 4 bước, đúng thứ tự

Thứ tự này là **quy tắc nghiệp vụ đã chốt** (Notes mục 4), không phải chuyện tối ưu:

**Bước 1 — Gom nhu cầu mặt hàng trên đơn.** Cộng dồn theo `item_code` (một đơn có thể có cùng
mặt hàng ở nhiều dòng).

**Bước 2 — Trừ tồn cho mặt hàng trên đơn.** `thiếu = cần − tồn_khả_dụng`. Ra **Bảng 1**.

**Bước 3 — Bóc BOM cho phần CÒN THIẾU.** Chỉ bóc `thiếu`, không bóc cả `cần` — bóc cả thì mua
thừa đúng bằng phần đang có trong kho.

- Mặt hàng *Mua hàng* (hoặc **trống** — coi như Mua hàng): không bóc, chính nó là thứ cần mua.
- Mặt hàng *Sản xuất / Gia công*: lấy BOM mặc định. **Không có BOM → sinh từ BOM Template**
  (phương án (c), anh Thắng chốt 24/08) qua `api/bom.auto_create_bom`. Không có cả BOM Template
  → ghi vào cảnh báo, coi như phải mua.
- Đệ quy xuống bán thành phẩm. Khách khẳng định **không có BOM lặp vòng**, nhưng vẫn phải chặn
  bằng tập `đã_thăm` — đó là tình trạng dữ liệu, không phải ràng buộc hệ thống.

**Bước 4 — Gom toàn bộ nhu cầu NVL rồi mới trừ tồn MỘT LẦN.** Không trừ tồn ngay tại từng nhánh
BOM. Trừ sớm thì cùng một lượng tồn bị đếm nhiều lần cho nhiều nhánh. Ra **Bảng 2**.

## 5. Công thức tồn khả dụng

```
tồn_khả_dụng(mặt hàng) = tồn_thực_tế − ghim_bởi_đơn_khác

tồn_thực_tế       = Σ Bin.actual_qty trên tập kho hợp lệ (mục 3)
ghim_bởi_đơn_khác = Σ (qty − delivered_qty) của mọi Sales Order thoả:
                      · docstatus = 1, status không thuộc (Closed, Completed, Cancelled)
                      · custom_ghim_ton_kha_dung = 1
                      · name ≠ đơn đang kiểm            ← R3, anh Thắng chốt 5.3
```

Dòng cuối là **bắt buộc**, anh Thắng nhắc lại 24/08 (`ptmjq2t3nj`): *"check box Ghim tồn khả dụng
phải không ảnh hưởng đến số tồn khả dụng ở bảng 1 của chính đơn đó"*. Thiếu nó thì đơn vừa tích
ghim tự trừ số lượng của chính mình và báo thiếu nhiều gấp đôi.

**Ghim lan xuống NVL** (anh Thắng bổ sung 24/08): với đơn đã ghim, mặt hàng *Sản xuất/Gia công*
thì **NVL bóc từ BOM mặc định cũng bị ghim theo**. Nghĩa là `ghim_bởi_đơn_khác` phải chạy chính
bước 3–4 ở trên cho từng đơn đã ghim, không chỉ cộng dòng trên đơn.

⚠ Đây là chỗ **tốn nhất** của cả tính năng: mỗi lần bấm nút phải bóc BOM cho *mọi đơn đang ghim*,
không riêng đơn hiện tại. Xem mục 9.

## 6. Ba bảng + dòng kết luận

**Bảng 1 — mặt hàng trên đơn.** Cột: Mặt hàng · ĐVT · Cần · **Tồn thực tế** · Tồn khả dụng ·
Thiếu · Bổ sung bằng.

**Bảng 2 — cần mua sau khi bóc BOM.** Cột: Nguyên vật liệu · ĐVT · Cần · **Tồn thực tế** ·
Tồn khả dụng · Thiếu · **Ngày hàng về (dự kiến)** · Nguồn nhu cầu. Cột *Nguồn nhu cầu* giữ nguyên
tên Thành Phần BOM (`Bộ vỏ đèn`, `Nguồn`…) vì **dòng kết luận gộp lấy tên khâu từ đúng cột này**.
Cột *Ngày hàng về* tính theo mục 8.2.

**Bảng 3 — nguồn lực nhân sự.** Tổng theo lịch · Đã phân bổ · Còn lại · Đơn này cần · kết luận.
Kèm danh sách **mặt hàng Sản xuất/Gia công chưa khai Thời Gian Sản Xuất hoặc = 0** (anh Thắng
chốt 5.2) — đây là cách duy nhất khiến R2 không im lặng.

**Chân popup — ba lối ra.** Hai nút đầu chỉ đóng popup. Nút **Hẹn lại ngày giao** trả về ngày
gợi ý theo mục 8.3.

**Dòng kết luận gộp** ở đầu popup: gom dòng thiếu của Bảng 2 theo *Nguồn nhu cầu*, cộng trạng
thái nhân lực từ Bảng 3 → *"Đơn này vướng ở 3 khâu vật tư. Nhân lực đủ."*

## 7. Danh sách đơn đang chiếm tồn (mục 7.2)

Hiện khi tồn khả dụng không đủ. **"Chiếm tồn" = đơn đang tích *Ghim tồn khả dụng***.

> ⚠ Chỗ này **đã đảo một lần**. Bản viết sáng 24/08 ghi *"chiếm tồn = đơn đã xuất kho"*, lấy từ
> `Stock Ledger Entry` âm → `Delivery Note Item.against_sales_order`. Anh Thắng sửa lại chiều tối
> cùng ngày (`ptmjq2t3nj`): *"đơn đang chiếm tồn là đơn đang được tích Ghim"*.

Ghi lại **vì sao bản mới đúng hơn**, để không ai đảo ngược lần thứ hai: con số *Tồn khả dụng* ở
Bảng 1 bị trừ đúng bởi tập đơn đã ghim (công thức mục 5). Bảng này tồn tại để **giải thích phần
chênh đó** — nên nó phải liệt kê đúng tập ấy. Đơn đã xuất kho thì hàng đã rời `Bin` từ trước,
nằm ngoài phần chênh, liệt kê ra chỉ khiến sale cộng trừ nhầm.

**Dùng lại đúng truy vấn `ghim_bởi_đơn_khác` ở mục 5, không viết truy vấn thứ hai.** Hai chỗ lệch
nhau dù chỉ một điều kiện `status` là bảng giải thích sai chính con số nó đang giải thích — loại
lỗi không ai phát hiện được bằng mắt.

Hiện **mã đơn · người phụ trách · số lượng đang ghim · ngày lấy hàng dự kiến**, sắp xếp ngày
**giảm dần**, lấy tối đa **5** đơn xa nhất.

- Số lượng đang ghim = `qty − delivered_qty` của dòng chứa mặt hàng đang thiếu — đúng đại lượng
  đã trừ vào tồn khả dụng, không phải tổng số lượng đơn.
- Người phụ trách = **`owner` của Sales Order** (người tạo đơn). Site có 0 dòng `Sales Team`.
- **Không hiện tên khách hàng** — khách đã chốt, và đó cũng là cách gỡ lo ngại lộ thông tin giữa
  các sale.

## 8. Ngày giao dự kiến

Hai nguồn khác hẳn nhau: phần **mua hàng** suy từ đơn mua đang chạy, phần **sản xuất** suy từ
lịch nhân sự. Nhưng chúng **nối tiếp nhau**, không phải hai số song song — xem 8.3.

### 8.1 Phần sản xuất (mục 7.4)

Dùng lại **engine Phần III** (`api/work_order_schedule.py`): nó đã biết quét `Employee Schedule`,
trừ `Employee Allocation` đã có, rồi lấp khối lượng vào chỗ trống bằng sweep-line.

Khối lượng cần lấp = `Σ (số lượng × Thời Gian Sản Xuất (Phút))` của mặt hàng Sản xuất/Gia công.
Không tạo `Employee Allocation` thật — chỉ mô phỏng, vì kết quả *chỉ để tham khảo*.

### 8.2 Ngày hàng về của NVL mua hàng (mục 7.5)

Anh Thắng chốt 24/08 (`ptmjq2t3nj`): lấy **`schedule_date` (Required By) của đơn mua gần nhất có
chứa mặt hàng đó**. Ví dụ của anh ấy: hôm nay 15, có đơn về ngày 20 và đơn về ngày 30 → hiện
**ngày 20**.

```
ngày_hàng_về(mặt hàng) = MIN(poi.schedule_date) với mọi Purchase Order Item thoả:
                           · po.docstatus = 1
                           · po.status không thuộc (Closed, Completed, Cancelled)
                           · poi.qty − poi.received_qty > 0        ← còn thiếu mới tính
                           · poi.schedule_date >= hôm nay          ← quá hạn thì vô nghĩa
```

Không có dòng nào thoả → hiện **"chưa có đơn mua"**, *không* bỏ trống. Ô trống đọc như "về ngay",
đó là kiểu sai im lặng mà R2/R4 đã dính một lần.

⚠ **Nguồn này thay cho `lead_time_days`.** Site có **1.115** mặt hàng *Mua hàng* và **0** mặt hàng
khai `lead_time_days` — trường đó không dùng được. Cách của anh Thắng đọc từ dữ liệu thật.

⚠ **Chưa nghiệm thu được trên site này.** Đo 24/08: **2** Purchase Order đã submit, cả hai đều có
`schedule_date` nhưng **đều quá hạn** (21/08 và 10/08) và là dữ liệu thử (`dịch vụ gia công`,
`Thành phẩm 1`). Số dòng còn thiếu có ngày **trong tương lai: 0**. Viết được, nhưng lúc bàn giao
cột này sẽ toàn *"chưa có đơn mua"* — cần vài PO thật trước khi test.

### 8.3 Ngày gợi ý cho nút *Hẹn lại ngày giao* (anh Thắng chốt 24/08, `ssvcj7q0rq`)

> *"Ở phần cuối có nút Hẹn lại ngày giao, em cho nó hiện 1 ngày gợi ý em nhé, dựa vào phần 7.4"*

⚠ **7.4 một mình là chưa đủ.** 7.4 chỉ tính công lao động. Nếu đơn còn thiếu NVL phải mua thì thợ
rảnh cả tháng cũng không sản xuất được trước ngày hàng về. Chạy 7.4 tính từ hôm nay ra ngày
**sớm hơn thực tế** — đúng hướng nguy hiểm: hứa sớm rồi trễ hẹn.

Hai vế phải **nối tiếp**, không lấy `max()`:

```
mốc_bắt_đầu = MAX(ngày_hàng_về của mọi NVL còn thiếu)      ← mục 8.2
ngày_gợi_ý  = engine 8.1 lấp khối lượng sản xuất, TÍNH TỪ mốc_bắt_đầu
```

Không thiếu NVL nào → `mốc_bắt_đầu` = hôm nay.

**Ba trạng thái trả về — không bao giờ trả về một con số trần.**

| Trạng thái | Điều kiện | Trả về |
|---|---|---|
| **Đủ** | mọi NVL thiếu đều có ngày về, mọi mặt hàng Sản xuất/Gia công đều có Thời Gian Sản Xuất | ngày + **cách ra ngày đó** (mốc vật tư + số ngày công) |
| **Thiếu định mức** | có mặt hàng Sản xuất/Gia công thiếu Thời Gian Sản Xuất | ngày, kèm câu *"mới tính được phần vật tư"* + **danh sách mặt hàng thiếu** — dùng lại đúng danh sách của Bảng 3, không dựng bảng thứ hai. Ghi rõ ngày thật sẽ **muộn hơn** |
| **Thiếu ngày về** | có NVL thiếu mà **không có đơn mua nào đang mở** | **KHÔNG trả về ngày nào cả** + danh sách vật tư chưa có đơn mua |

⚠ Trạng thái thứ ba là **cố ý**, đừng "sửa cho tiện" thành trả về ngày ước lượng. Một ô trống có
giải thích thì sale còn đi hỏi mua hàng; một ngày sai thì sale hứa thẳng với khách. Đây chính là
rủi ro **R4** ở phần đầu file — R4 chưa mất, chỉ được rào lại.

⚠ **Dữ liệu hôm nay khiến gần như mọi đơn rơi vào trạng thái 2 hoặc 3.** Đo 24/08: **3/61.144**
mặt hàng có Thời Gian Sản Xuất > 0, trong khi **59.692** mặt hàng khai *Phương pháp bổ sung =
Sản xuất*. Đây là hiện trạng dữ liệu, **không phải tính năng hỏng** — nó tự khỏi khi khách khai
định mức. Nhưng phải nói trước với khách, đừng để họ tự phát hiện lúc nghiệm thu.

## 9. Hiệu năng

Quy mô đã chốt: **1–2 mặt hàng/đơn**, **BOM dưới 10 NVL**, mục tiêu **dưới 1 giây**.

Chỗ tốn không nằm ở đơn hiện tại mà ở mục 5: phải bóc BOM cho **mọi đơn đang ghim**. Cách giữ
trong ngân sách:

1. Một query `Bin` cho toàn bộ mặt hàng liên quan, `item_code IN (...)` — **không** gọi trong
   vòng lặp. Đây là bẫy N+1 kinh điển của Frappe.
2. Một query gom mọi dòng của mọi đơn đang ghim, rồi bóc BOM theo **tập mặt hàng khác nhau**,
   không theo từng đơn.
3. Nhớ kết quả bóc BOM theo `item_code` trong một lần bấm nút.

⚠ `frappe.get_list` áp User Permission còn `frappe.get_all` **thì không**. Ở đây phải dùng
`get_all` — sale cần thấy tồn kho tổng, không phải phần mình được phép xem. Nhưng danh sách đơn
ở mục 7 thì ngược lại: cân nhắc kỹ trước khi chọn hàm.

## 10. Còn treo

**Không còn mục nào chặn việc code Phần IV.** Ba mục treo của bản 24/08 sáng đã đóng:

| Mục cũ | Kết cục |
|---|---|
| 10.1 — Lệnh sản xuất không gắn Đơn Bán | **Chuyển sang PM-FEAT-00034**, vì chỉ ảnh hưởng mục 7.3 vốn đã tách ra (mục 11) |
| 10.2 — Ngày có hàng cho NVL Mua hàng | **Đóng** — anh Thắng chốt lấy Required By của đơn mua, xem mục 8.2 |
| 10.3 — Mục 7.2 không demo được | **Tan** — bảng không còn đọc `Delivery Note Item.against_sales_order` nữa, xem mục 7 |

Còn lại là hai chỗ **dữ liệu mỏng**, không phải chỗ chưa quyết — đã ghi tại chính mục liên quan:
mục 8.2 (0 đơn mua có ngày trong tương lai) và rủi ro R1/R2/R4 ở phần đầu file.

## 11. Mục 7.3 — đã tách ra tính năng riêng

**Anh Thắng chốt 24/08** (`ptmjq2t3nj`): *"phần 7.3 em tách thành 1 task riêng giúp anh nhé"*.

→ **PM-FEAT-00034** · `docs/features/chan-xuat-kho-qua-ton-kha-dung.md`

Lý do tách, giữ lại ở đây để tra ngược: chặn xuất quá tồn khả dụng **đổi bản chất** tính năng
này, từ *chỉ hiển thị* thành *chặn chứng từ* — phải chặn ở `Stock Entry`, `Delivery Note`,
`Material Request`, tức mọi đường xuất kho. Phần IV sai thì sale đọc nhầm một con số; phần chặn
sai thì **dừng việc của kho**.

Mục treo **10.1** (26/39 lệnh sản xuất không lần ra Đơn Bán) theo sang PM-FEAT-00034, vì nó chỉ
ảnh hưởng luật chặn.

## 12. Việc kế tiếp

1. ✅ **Anh Thắng duyệt mockup 24/08** (`ssvcj7q0rq`: *"được rồi đó em"*). Bản 5 thêm ngày gợi ý
   ở nút *Hẹn lại ngày giao* theo yêu cầu cùng bình luận đó.
2. Code theo thứ tự: tập kho → tồn khả dụng → bóc BOM → 3 bảng → ngày giao dự kiến.
3. Test case theo `erpnext-mbwnext-testcase`. **Không** còn cần `TC-REGR` cho app lõi ở tính năng
   này — mục 7.3 đã tách sang PM-FEAT-00034, Phần IV giờ thuần đọc, không chạm `doc_events`.
4. Trước khi nghiệm thu mục 8.2: nhờ anh Thắng tạo vài Purchase Order có Required By trong tương
   lai, nếu không cột *Ngày hàng về* sẽ toàn *"chưa có đơn mua"* và không ai biết đúng hay sai.

> Bản 24/08 chiều: sửa mục 5 · 6 · 7 · 8 · 10 · 11 · 12 theo bình luận `ptmjq2t3nj`;
> thêm mục **8.3** theo bình luận `ssvcj7q0rq`.
