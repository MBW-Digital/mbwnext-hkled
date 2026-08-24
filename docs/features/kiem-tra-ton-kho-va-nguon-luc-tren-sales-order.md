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

**Ghim lan xuống NVL** (anh Thắng bổ sung 24/08): với đơn đã ghim, mặt hàng *Sản xuất/Gia công*
thì **NVL bóc từ BOM mặc định cũng bị ghim theo**. Nghĩa là `ghim_bởi_đơn_khác` phải chạy chính
bước 3–4 ở trên cho từng đơn đã ghim, không chỉ cộng dòng trên đơn.

⚠ Đây là chỗ **tốn nhất** của cả tính năng: mỗi lần bấm nút phải bóc BOM cho *mọi đơn đang ghim*,
không riêng đơn hiện tại. Xem mục 9.

## 6. Ba bảng + dòng kết luận

**Bảng 1 — mặt hàng trên đơn.** Cột: Mặt hàng · ĐVT · Cần · **Tồn thực tế** · Tồn khả dụng ·
Thiếu · Bổ sung bằng.

**Bảng 2 — cần mua sau khi bóc BOM.** Thêm cột **Tồn thực tế**; cột *Nguồn nhu cầu* giữ nguyên
tên Thành Phần BOM (`Bộ vỏ đèn`, `Nguồn`…) vì **dòng kết luận gộp lấy tên khâu từ đúng cột này**.

**Bảng 3 — nguồn lực nhân sự.** Tổng theo lịch · Đã phân bổ · Còn lại · Đơn này cần · kết luận.
Kèm danh sách **mặt hàng Sản xuất/Gia công chưa khai Thời Gian Sản Xuất hoặc = 0** (anh Thắng
chốt 5.2) — đây là cách duy nhất khiến R2 không im lặng.

**Dòng kết luận gộp** ở đầu popup: gom dòng thiếu của Bảng 2 theo *Nguồn nhu cầu*, cộng trạng
thái nhân lực từ Bảng 3 → *"Đơn này vướng ở 3 khâu vật tư. Nhân lực đủ."*

## 7. Danh sách đơn đang chiếm tồn (mục 7.2)

Hiện khi tồn khả dụng không đủ. **"Chiếm tồn thực tế" = đơn ĐÃ XUẤT KHO** — không phải đơn đang
ghim. Nguồn: `Stock Ledger Entry` âm trên tập kho hợp lệ, lần về `Delivery Note Item` →
`against_sales_order`.

Hiện **mã đơn + người phụ trách + ngày lấy hàng dự kiến**, sắp xếp ngày **giảm dần**, lấy tối đa
**5** đơn xa nhất.

- Người phụ trách = **`owner` của Sales Order** (người tạo đơn). Site có 0 dòng `Sales Team`.
- **Không hiện tên khách hàng** — khách đã chốt, và đó cũng là cách gỡ lo ngại lộ thông tin giữa
  các sale.

## 8. Ngày giao dự kiến (mục 7.4 / 7.5)

Dùng lại **engine Phần III** (`api/work_order_schedule.py`): nó đã biết quét `Employee Schedule`,
trừ `Employee Allocation` đã có, rồi lấp khối lượng vào chỗ trống bằng sweep-line.

Khối lượng cần lấp = `Σ (số lượng × Thời Gian Sản Xuất (Phút))` của mặt hàng Sản xuất/Gia công.
Không tạo `Employee Allocation` thật — chỉ mô phỏng, vì kết quả *chỉ để tham khảo*.

⚠ **Chỉ áp cho phần SẢN XUẤT.** NVL *Mua hàng* không có công đoạn nào để lấp vào lịch — xem mục
10.2, đang treo.

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

## 10. Còn treo — chưa code được phần này

**10.1 — Lệnh sản xuất không gắn Đơn Bán (ảnh hưởng mục 7.3).** Chuỗi lần vết có thật:
`Stock Entry.work_order → Work Order.sales_order`, và `Work Order.production_plan →
Production Plan Sales Order.sales_order`. Nhưng đo trên site: **13/39** lệnh có `sales_order`;
26 lệnh còn lại không lần ra đơn nào, nên luật *"phiếu thuộc đơn đã ghim thì vẫn được xuất"*
không đánh giá được → **chặn oan**. Claude đề nghị **cho qua**; chờ anh Thắng chốt.

**10.2 — Ngày có hàng cho NVL Mua hàng.** Site có **1.115** mặt hàng *Mua hàng* và **0** mặt
hàng khai `lead_time_days`. Chưa có căn cứ nào. Chờ khách trả lời lấy thời gian đặt hàng ở đâu.

**10.3 — Mục 7.2 chưa demo được trên site này.** `Delivery Note Item.against_sales_order` đang
có **0** dòng, nên bảng đơn-đã-xuất-kho sẽ rỗng khi test. Không phải lỗi thiết kế.

## 11. Mục 7.3 — đề nghị tách thành tính năng riêng

Chặn xuất quá tồn khả dụng **đổi bản chất** tính năng này: từ *chỉ hiển thị* thành *chặn chứng
từ*. Phải chặn ở `Stock Entry`, `Delivery Note`, `Material Request` — tức mọi đường xuất kho.

Ba lý do nên tách:

1. Phần IV này khách cần sớm để sale dùng; phần chặn thì **dừng được việc kho** nếu sai, phải
   thử kỹ hơn nhiều.
2. Còn treo mục 10.1 — chưa chốt thì chưa code đúng được.
3. ERPNext v15 **đã có Stock Reservation Entry**, trên site đang tắt. Trước khi dựng cơ chế ghim
   song song, nên cân nhắc bật cái có sẵn — hai hệ thống giữ chỗ chạy cùng lúc sẽ trừ trùng nhau.

## 12. Việc kế tiếp

1. Chốt 10.1 và 10.2 với anh Thắng.
2. Cập nhật mockup: thêm cột *Tồn thực tế*, bảng đơn-đã-xuất-kho, danh sách mặt hàng chưa khai
   thời gian sản xuất. Khách duyệt lại.
3. Code theo thứ tự: tập kho → tồn khả dụng → bóc BOM → 3 bảng → ngày giao dự kiến.
4. Test case theo `erpnext-mbwnext-testcase`, có `TC-REGR` cho app lõi vì mục 7.3 chạm doc_events
   của Stock Entry.
