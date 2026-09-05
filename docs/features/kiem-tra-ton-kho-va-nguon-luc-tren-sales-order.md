# Kiểm tra tồn kho và nguồn lực trên Đơn Bán

> **PM-FEAT-00023 · Phần IV · Kiểm tra tồn kho và nguồn lực trên Đơn bán hàng**
> Tên trên PM khác tên file này — nối hai bên bằng MÃ, không bằng tên. Xem `CLAUDE.md`.

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
| Sales Order | `custom_ghim_ton_kha_dung` | Check | Công tắc chung cho cả đơn |
| Sales Order Item | `custom_so_luong_giu_cho` | Float | Số lượng đơn này thực sự giữ, **theo từng dòng** |

> ✅ **ĐỔI 02/09 — THÊM Ô SỐ LƯỢNG, GIỮ CẢ Ô TÍCH** (anh Thắng chốt `12:32` và `12:40`).
>
> Bản đầu chỉ có ô tích. Không đủ: khách nêu tình huống A nhường một phần hàng cho B
> (phản hồi 27/08), mà ô tích thì **chỉ nhả được cả đơn**, không nhả một phần — A định
> nhường 4 cái *item 1* nhưng mất luôn 2 cái *item 2* vì bỏ tích là nhả sạch.
>
> Ba luật đã chốt:
>
> 1. **Ô tích ở cấp ĐƠN, ô số lượng ở TỪNG DÒNG.** Tích một cái là hệ thống điền mức tối đa
>    cho mọi dòng — đơn 20 dòng không phải gõ 20 ô.
> 2. **Bỏ tích KHÔNG xoá số đã nhập**, chỉ làm mờ và ngừng áp dụng. Tích lại thì số cũ còn
>    nguyên. Sale sửa tay 20 dòng rồi lỡ bỏ tích mà mất sạch thì không có đường lấy lại.
> 3. **Sửa tay KHÔNG được vượt tồn khả dụng** — anh Thắng chốt 12:40, chặn cứng ở mức tối đa.
>
> ⚠ Luật 3 đảo lại đề xuất ban đầu của tôi (cho gõ vượt + chữ đỏ). Lý do tôi phản đối là
> *"phần thiếu biến mất khỏi màn hình"*; anh Thắng gỡ đúng chỗ đó bằng cách cho phần thiếu
> ra thành một cột riêng — xem mục 5b. Lo ngại được giải, không phải bị bỏ qua. `custom_reserved_qty` **không** tạo cột trên `Bin` — tính động lúc bấm
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
>
> **✅ ĐÃ XỬ LÝ 26/08/2026** — anh Thắng tắt và dọn. Đo lại trên `hkled.com`:
> `enable_stock_reservation = 0` · **0** Bin có `reserved_stock` · 4 đơn thử `SO-26-00007→00010`
> đã xoá · **0** đơn còn `reserve_stock = 1`. Nền đo đã sạch, đoạn cảnh báo trên hết hiệu lực.

### ⚠ ĐO PHẦN TỒN BỊ GIỮ CHỖ BẰNG `Bin.reserved_stock`, ĐỪNG CỘNG `Stock Reservation Entry`

Ghi lại vì suýt đọc sai ngay trong lần dọn trên. Sau khi dọn, bảng SRE **vẫn còn 1 bản ghi**
`MAT-SRE-2026-00001`, và nó **vẫn mang `reserved_qty = 26`**:

	Stock Reservation Entry  docstatus = 2 (Đã huỷ)  ·  sum(reserved_qty) = 26.0
	Bin                      sum(reserved_stock)     = 0.0

Thực tế không giữ gì — `Bin` mới là nơi ghi phần tồn bị chiếm. Con số 26 trên SRE là **giá trị
lịch sử nằm trên chứng từ đã huỷ**, Frappe không xoá và không đưa về 0.

Ai đo tồn khả dụng bằng cách cộng `Stock Reservation Entry.reserved_qty` mà quên lọc
`docstatus < 2` sẽ ra **26** — một con số trông y hệt số thật, không lệch kiểu, không lỗi.
Đúng loại sai âm thầm mà cả tính năng này sinh ra để chặn.

➜ Nguồn đúng là **`Bin.reserved_stock`**. Dùng SRE thì bắt buộc lọc `docstatus`.

## 3. Tập kho

> 🔒 **CHỐT LẠI 03/09/2026 15:33 — đừng lật lần nữa.** Anh Thắng dùng chữ *"tồn khả dụng nên cộng
> trên TẤT CẢ kho"* lúc 11:25, chữ "tất cả" đọc ra được hai nghĩa nên tôi hỏi lại kèm tên đúng 4
> kho đang bị loại. Anh trả lời: *"«Tất cả» = tất cả kho trừ 2 nhóm trên — tức giữ nguyên như đang
> chạy em nhé."*
>
> Đây là **định nghĩa gốc mà 4 tính năng dựa vào** (Phần IV, IV.1, IV.2 và Phần V). Ai thấy chữ
> "tất cả kho" ở tài liệu khác thì đọc kèm dòng này, đừng bỏ luật loại trừ.
>
> ⚠ Lý do phải hỏi dù gần như chắc: bỏ loại trừ là **tính hàng ở Kho hàng lỗi/trả thành hàng bán
> được** — hệ thống báo đủ, sale không đi mua phần thật sự thiếu.
>
> 📌 Hỏi lúc đó **không tốn gì**: đo cùng ngày, 4 kho bị loại đang **trống hoàn toàn** (0 mặt hàng
> có tồn), nên hai cách cho ra con số y hệt. Chốt luật trước khi có hàng lỗi phát sinh thì sau này
> không ai phải sửa lại.

Tồn (cả thực tế lẫn khả dụng) **loại trừ** kho con của hai nhóm:

- `Nhóm kho lỗi - HKL`
- `Nhóm kho trung chuyển - HKL`

Hai nhóm này là `Warehouse` có `is_group = 1`, con của `Kho Tổng - HKL`. Lấy kho hợp lệ bằng
`lft/rgt` của cây Warehouse chứ **đừng so tên**: tên có hậu tố công ty (`- HKL`) và sẽ đổi khi
lên site khác.

⚠ `MBWNext System Setting` có sẵn `warehouse_error` / `bad_stock_warehouse` nhưng **đang để
trống**. Đừng đọc hai trường đó — hiện không mang giá trị nào.

**Đo trên `hkled.com` 03/09** — 9 kho lá, loại 4, còn **5** kho được tính tồn:

	Kho Tổng
	├── Kho Sản xuất
	│   ├── Kho thành phẩm · Kho nguyên vật liệu · Kho bán thành phẩm    ✅ tính
	│   └── Kho ký gửi · Kho khuyến mãi/hàng mẫu                          ✅ tính
	├── Nhóm kho lỗi        → Kho hàng lỗi/trả · Kho hàng lỗi cần sửa chữa   ❌ loại
	└── Nhóm kho trung chuyển → Kho trung chuyển · **Kho đang sản xuất**     ❌ loại

⚠ **`Kho đang sản xuất` bị loại**, và đây là chỗ dễ bị báo nhầm là lỗi. Nó nằm dưới *Nhóm kho
trung chuyển* nên rơi đúng vào luật đã chốt. Về nghiệp vụ cũng đúng: vật tư đã xuất cho sản xuất
thì không còn rảnh để bán cho đơn khác. Nhưng người dùng nhìn tên kho sẽ tưởng là hàng đang có.
Nếu về sau khách muốn tính kho này thì đó là **đổi luật**, phải chốt lại, không phải sửa lỗi.

## 4. Thuật toán — 4 bước, đúng thứ tự

Thứ tự này là **quy tắc nghiệp vụ đã chốt** (Notes mục 4), không phải chuyện tối ưu:

**Bước 1 — Gom nhu cầu mặt hàng trên đơn.** Cộng dồn theo `item_code` (một đơn có thể có cùng
mặt hàng ở nhiều dòng).

**Bước 2 — Trừ tồn cho mặt hàng trên đơn.** `thiếu = cần − tồn_khả_dụng` (xem 5b). Ra **Bảng 1**.

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
ghim_bởi_đơn_khác = Σ custom_so_luong_giu_cho của mọi dòng Sales Order Item thoả:
                      · đơn cha docstatus = 1, status không thuộc (Closed, Completed, Cancelled)
                      · đơn cha custom_ghim_ton_kha_dung = 1
                      · đơn cha name ≠ đơn đang kiểm    ← R3, anh Thắng chốt 5.3
```

> ⚠ **ĐỔI 03/09 — đọc trường lưu sẵn, KHÔNG suy từ `qty − delivered_qty` nữa.** Từ khi ghim là
> một con số (mục 2), phần đơn khác giữ chỗ chính là giá trị họ đã nhập, không phải toàn bộ phần
> chưa giao của họ. Đơn giữ 1 trên dòng 5 cái thì chỉ chiếm 1.
>
> Kèm theo: phần **đã giao** không còn phải trừ ở đây. Giao hàng làm `Bin.actual_qty` giảm thật,
> nên nếu vẫn trừ `delivered_qty` một lần nữa là **trừ hai lần**.

Dòng cuối là **bắt buộc**, anh Thắng nhắc lại 24/08 (`ptmjq2t3nj`): *"check box Ghim tồn khả dụng
phải không ảnh hưởng đến số tồn khả dụng ở bảng 1 của chính đơn đó"*. Thiếu nó thì đơn vừa tích
ghim tự trừ số lượng của chính mình và báo thiếu nhiều gấp đôi.

**Ghim lan xuống NVL** (anh Thắng bổ sung 24/08): với đơn đã ghim, mặt hàng *Sản xuất/Gia công*
thì **NVL bóc từ BOM mặc định cũng bị ghim theo**.

> 🔴 **SỬA 02/09 — CHỈ BÓC PHẦN CHƯA SẢN XUẤT. Lỗi đếm hai lần, do khách chỉ ra.**
>
> Khách hỏi (27/08): *"sản xuất xong 5 sản phẩm rồi thì có chuyển từ ghim NVL sang ghim thành
> phẩm không?"* Theo bản viết trước thì **không chuyển, mà ghim cả hai** — và đó là lỗi:
>
> `delivered_qty` chỉ giảm khi **giao cho khách**, không giảm khi **sản xuất xong**. Nên sau khi
> sản xuất: NVL đã tiêu hao vào thành phẩm (`Bin.actual_qty` đã giảm thật), mà công thức vẫn bóc
> BOM ra ghim tiếp → **cùng một lượng vật tư bị trừ hai lần**, đơn khác thấy *thiếu ảo*.
>
> ```
> lượng bóc BOM = qty − delivered_qty − đã_sản_xuất
> đã_sản_xuất   = Σ produced_qty của Work Order gắn với đơn đó, cho mặt hàng đó
> ```
>
> Phần đã sản xuất xong thì chuyển sang **ghim thành phẩm**, đúng như khách hình dung. Nghĩa là `ghim_bởi_đơn_khác` phải chạy chính
bước 3–4 ở trên cho từng đơn đã ghim, không chỉ cộng dòng trên đơn.

⚠ Đây là chỗ **tốn nhất** của cả tính năng: mỗi lần bấm nút phải bóc BOM cho *mọi đơn đang ghim*,
không riêng đơn hiện tại. Xem mục 9.

## 5b. Công thức cột *Thiếu* — GIỮ NGUYÊN `cần − tồn_khả_dụng` (chốt 02/09 13:15)

```
thiếu = cần − tồn_khả_dụng          ← KHÔNG phụ thuộc số lượng giữ chỗ
```

Mục này ghi lại **một đề xuất của tôi đã bị bác, và vì sao bác là đúng** — để không ai
mở lại.

**Tôi đề xuất** đổi thành `cần − số_lượng_giữ_chỗ` khi đơn có tích ghim, lấy ca sau làm
lý do: đơn A cần 5, tồn khả dụng 5, A tự hạ giữ chỗ xuống 1 để nhường cho B → công thức
cũ ra `thiếu 0` trong khi A chỉ giữ 1; rồi con số **tự nhảy** lên 4 ngay khi B ghim, dù
không ai đụng vào đơn A.

**Anh Thắng bác, và lý do quyết định là ở chỗ cột này dùng để làm gì:**

> *"khi sales tạo đơn, họ thấy mặt hàng bị thiếu là họ tự tạo yêu cầu mặt hàng theo số
> đó rồi, không cần quan tâm họ ghim bao nhiêu"*

Cột *Thiếu* là **đầu vào để lập Yêu Cầu Mặt Hàng**, không phải thước đo "tôi đã giữ chắc
bao nhiêu". Với công thức của tôi, A giữ chỗ 1 trên tồn 5 sẽ ra `thiếu 4` → sale lập đơn
mua 4 cái **trong khi 4 cái đó đang nằm trong kho, chưa ai lấy**. Đó là **mua thừa**, và
là lỗi đắt hơn hẳn lỗi tôi định chặn.

Còn chuyện "con số tự nhảy": nó nhảy vì **thế giới thật vừa đổi** — B đã lấy hàng. Trước
lúc B lấy, 4 cái đó vẫn dùng được cho A thật. Con số cũ không sai, nó phản ánh đúng hiện
trạng chứ không phản ánh *ý định* của A.

⚠ Hệ quả phải chấp nhận, ghi rõ để người sau không tưởng là lỗi: trên cùng một dòng có
thể thấy `cần 5 · giữ chỗ 1 · thiếu 0`. Đọc đúng là: **1 cái đã giữ chắc, 4 cái còn
trong kho nhưng chưa ai giữ**. Số lượng đã lập Yêu Cầu Mặt Hàng **không đổi theo** phần
ghim về sau — anh Thắng chốt: *"sau này dù họ có ghim thêm do người khác nhả ra thì số
lượng yêu cầu mặt hàng vẫn vậy"*.

## 6. Ba bảng + dòng kết luận

**Bảng 1 — mặt hàng trên đơn.** Cột: Mặt hàng · ĐVT · Cần · **Tồn thực tế** · Tồn khả dụng ·
**Giữ chỗ** · Thiếu · Bổ sung bằng. Cột *Giữ chỗ* là ô nhập (mục 2); *Thiếu* **không** phụ thuộc nó — xem 5b.

**Bảng 2 — cần mua sau khi bóc BOM.** Cột: Nguyên vật liệu · ĐVT · Cần · **Tồn thực tế** ·
Tồn khả dụng · Thiếu · **Ngày hàng về (dự kiến)** · **SL về** · Nguồn nhu cầu.

> ✅ **BỔ SUNG 02/09 theo phản hồi của khách 27/08.** Hai cột/khối mới:
>
> **Cột `SL về`** — khách hỏi *"ngoài ngày dự kiến hàng về thì hiển thị thêm số lượng hàng về"*,
> anh Thắng xác nhận lấy theo **đúng đơn mua đã dùng để ra ngày** (mục 8.2), tức
> `poi.qty − poi.received_qty` của chính dòng đó.
> ⚠ Đặt **cạnh** cột *Thiếu*, không thay nó: số về **có thể nhỏ hơn** phần thiếu (thiếu 100 mà
> đơn về sớm nhất chỉ có 30). Chỉ thấy *"20/9 có hàng"* mà không thấy về bao nhiêu thì sale
> nhận đơn rồi vẫn thiếu.
>
> **Khối "đơn nào đang ghim" cho Bảng 2** — khách hỏi *"trên Bảng 2 vẫn chưa thấy, do mockup
> chưa làm thôi hay gặp khó khăn gì"*. Trả lời: **thiếu ở mockup, không phải khó.** Nhưng hiện
> **khác Bảng 1**: đơn kia *không có dòng NVL đó trên đơn* — NVL bị ghim là do **bóc BOM của
> đơn kia** (mục 5). Nên số lượng hiện ở đây là lượng NVL bóc ra, không phải số lượng trên đơn. Cột *Nguồn nhu cầu* giữ nguyên
tên Thành Phần BOM (`Bộ vỏ đèn`, `Nguồn`…) vì **dòng kết luận gộp lấy tên khâu từ đúng cột này**.
Cột *Ngày hàng về* tính theo mục 8.2.

**Bảng 3 — nguồn lực nhân sự.** Tổng theo lịch · Đã phân bổ · Còn lại · Đơn này cần · kết luận.
Kèm danh sách **mặt hàng Sản xuất/Gia công chưa khai Thời Gian Sản Xuất hoặc = 0** (anh Thắng
chốt 5.2) — đây là cách duy nhất khiến R2 không im lặng.

**Chân popup — ba lối ra.** Hai nút đầu chỉ đóng popup. Nút **Hẹn lại ngày giao** trả về ngày
gợi ý theo mục 8.3.

**Dòng kết luận gộp** ở đầu popup: gom dòng thiếu của Bảng 2 theo *Nguồn nhu cầu*, cộng trạng
thái nhân lực từ Bảng 3 → *"Đơn này vướng ở 3 khâu vật tư. Nhân lực đủ."*

## 6b. Bảng 1b và Bảng 2b — bung ra xem ĐƠN NÀO đang giữ (làm 03/09)

> 🔴 **Vì sao mục này sinh ra muộn — đọc trước khi sửa mockup lần sau.**
> Hai bảng này đã có trong **mockup bản 6 (25/08)** và **bản 7**, nhưng **không ai kéo sang bản
> đặc tả này**. Code đọc đặc tả nên bỏ sót cả hai; anh Thắng phát hiện thiếu ngày **03/09 16:30**,
> tức 9 ngày sau khi chốt. Bài học ghi thẳng vào đây: **mockup đổi thì đặc tả phải đổi theo trong
> cùng lượt**, vì mockup là thứ để chốt với khách, còn đặc tả mới là thứ để viết code.

**Bảng 1b** bung ra từ **một dòng của Bảng 1** — cột *Đơn khác giữ* là chỗ bấm.
**Bảng 2b** bung ra từ **một dòng của Bảng 2**, nút nằm ngay dưới mã vật tư (Bảng 2 không có cột
*Đơn khác giữ* để đặt nút).

| | Bảng 1b | Bảng 2b |
|---|---|---|
| Trả lời câu hỏi | ai đang giữ **chính mặt hàng này** | ai đang giữ **vật tư này**, qua định mức của thứ họ bán |
| Cột | Mã đơn · Người phụ trách · Đang ghim · Ngày lấy hàng dự kiến | thêm **Bóc ra từ** — mã thành phẩm và định mức hiệu dụng |

Ba luật đã chốt, **không** được đổi khi sửa code:

1. **Không hiện tên khách hàng.** Chỉ *Người phụ trách* (Nhân viên kinh doanh, trống thì lấy người
   tạo đơn). Anh Thắng chốt ở mockup bản 6.
2. **Tối đa 5 đơn, ưu tiên ngày lấy hàng XA NHẤT** — đó là đơn dễ thương lượng nhả hàng nhất.
   Còn dư thì ghi *"…và N đơn nữa"*, và **dòng Cộng vẫn tính đủ tất cả**, không chỉ 5 dòng hiện ra.
3. **Dòng Cộng phải nói đúng phần ĐÃ TRỪ, không phải tổng ghim.** Hai số này lệch nhau khi đơn khác
   ghim nhiều hơn số đang có trong kho — xem mục 6c. Lúc đó ghi rõ cả hai:
   *"Cộng 9 — nhưng kho không đủ nên chỉ trừ 7 khỏi tồn khả dụng"*.

⚠ Cột *Bóc ra từ* ghi **định mức hiệu dụng qua nhiều tầng**, không phải định mức một tầng: cây 3
tầng thì *"3 × 3,00"* nghĩa là 3 cái thành phẩm ăn hết 9 cái vật tư này.

⚠ Dữ liệu lấy bằng `frappe.get_all` nên **không áp User Permission** — người bị giới hạn phạm vi
vẫn thấy mã đơn và người phụ trách của đơn họ không đọc được. Cố ý để khớp con số đã trừ (con số
đó cũng tính trên toàn bộ đơn). **Đang chờ anh Thắng chốt** có cần giấu bớt không.

## 6c. Tồn khả dụng KHÔNG được âm (sửa 03/09)

> Anh Thắng bắt được **03/09 16:34**: *"tồn khả dụng sao âm được em nhỉ, như này thì nó dẫn đến
> việc mua thừa"*.

Luật: **không ai giữ chỗ được nhiều hơn số đang có trong kho.**

```
ghim_hiệu_lực = min(đơn_khác_ghim, max(0, tồn_thực_tế))
tồn_khả_dụng  = tồn_thực_tế − ghim_hiệu_lực
```

Trước đó tính thẳng `tồn − ghim` nên ra số âm, rồi `thiếu = cần − tồn_khả_dụng` **cộng luôn phần
âm vào đơn đang xem** → hai đơn cùng mua một lượng hàng. Đo trên `SO-26-00010`: `Bán thành phẩm 2`
thiếu 173 thay vì 171.

⚠ Phép tính này nằm ở **một hàm dùng chung `_kha_dung`** cho cả bốn chỗ: Bảng 1, Bảng 2,
`tinh_can_mua` (số đi vào phiếu Yêu Cầu Mặt Hàng) và hook `chan_giu_cho_vuot_ton`. Trước đây bốn
chỗ chép lại cùng một phép trừ — sửa ba chỗ quên một chỗ thì màn hình và phiếu lệch nhau mà không
ai phát hiện.

⚠ Tồn **âm thật** (Bin âm) thì giữ nguyên số âm, không kẹp về 0 — đó là tồn kho lệch thật, phải
mua bù thật. Hiện `hkled.com` có 0 bản ghi Bin âm.

### 🔒 Cách B — anh Thắng chốt 03/09 16:51

> *"Chọn cách B em nhé."*

Gốc rễ của chuyện ghim vượt tồn: phần ghim lan xuống vật tư giữ cả cho thành phẩm **đã có sẵn
trong kho**. Ca thật: hai đơn ghim tổng 31 `Thành phẩm 1` trong khi kho có đúng 31 — không phải
sản xuất cái nào, nhưng bản cũ vẫn giữ 31 bộ vật tư, mà `NVL 3` chỉ có 7.

**Luật mới:** chỉ lan xuống vật tư cho phần **còn phải sản xuất**.

```
còn_phải_làm = max(0, tổng_ghim − tồn_thành_phẩm)
vật_tư_bị_giữ = bóc_định_mức(còn_phải_làm)
```

⚠ Trừ tồn ở mức **TỔNG**, không trừ theo từng đơn — nhiều đơn cùng ghim một mã thì chúng chia
nhau đúng một lượng tồn. Trừ từng đơn là mỗi đơn được "che" bởi cùng số hàng đó.

⚠ Bảng 1b/2b phải **chia đúng lượng tồn đó cho từng đơn**, nếu không tổng bảng chi tiết lệch con
số đã trừ. Thứ tự chia: **ngày lấy hàng SỚM NHẤT trước** — đơn giao gần lấy hàng đang có, đơn giao
xa còn kịp sản xuất.

📌 Phép kẹp ở trên (mục 6c) **vẫn giữ**: cách B làm ghim gián tiếp không còn vượt tồn, nhưng ghim
**trực tiếp** vẫn có thể vượt nếu tồn tụt sau khi ghim (giao hàng, kiểm kê giảm). Kẹp là lưới an
toàn, không phải bản vá tạm.

## 6d. Nút Tạo Yêu Cầu Mặt Hàng — lấy thẳng cột Thiếu (đổi 03/09)

> 🔒 **Anh Thắng chốt 03/09 16:51:** *"em cứ cho tạo dựa theo số lượng ở cột thiếu em nhé, không
> cần phải tính trừ các đơn đã đặt mua đâu. Vì phần này anh đã thống nhất với khách là đơn nào
> thiếu bao nhiêu thì tự đặt yêu cầu mua bằng đó, rồi muốn xin người khác nhường ghim hay như nào
> thì tự xin sau"*

**Đây là đảo ngược luật chốt 28/08** (`cần mua = đang thiếu − phiếu YCM đang chờ − đơn mua chưa
về`, PM-TASK-00140). Hàm `_da_co_nguoi_lo` dựng cho luật cũ **đã gỡ khỏi code**.

```
cần_mua = Thiếu(Bảng 1, chỉ mã KHÔNG phải Sản xuất/Gia công) + Thiếu(Bảng 2)
```

⚠ **Hệ quả anh Thắng đã cân nhắc và vẫn chọn:** bấm nút hai lần trên cùng một đơn ra **hai phiếu
cho cùng một phần thiếu**. Hệ thống không tự trừ nữa; điều phối giữa các đơn là thoả thuận giữa
người với nhau. Chỗ duy nhất còn nhắc là dòng cảnh báo "đơn này đã có phiếu" trong
`tao_yeu_cau_mua_hang` — **đừng gỡ nó đi**.

⚠ Mã xuất hiện ở **cả hai bảng** (vừa bán thẳng, vừa là vật tư của mã khác) thì hai dòng `Thiếu`
của nó đều đã được cùng một lượng tồn che, nên cộng lại là đặt mua dôi ra đúng phần tồn đó. Luật
mới là cộng thẳng nên code **không tự trừ** — chỉ thêm một dòng cảnh báo nêu đích danh mã đó.

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

### 7.1 Hiện ở đâu, và đơn nhiều dòng thì sao (anh Thắng hỏi 25/08, `6l9rin0adf`)

Anh Thắng hỏi: *"đơn đó nhiều mặt hàng thì nó hiện mỗi mặt hàng 5 dòng như vậy à, hay chỉ chuột
vào dòng mặt hàng nào nó mới hiện"*. Mockup bản 5 **không trả lời được** — ví dụ trong đó chỉ có
đúng một mặt hàng bị ghim nên luật hiển thị không lộ ra. Chốt ở bản 6:

1. Bảng này **gập sẵn**, không hiện cho tới khi người dùng bấm.
2. Chỉ dòng nào **đang bị đơn khác ghim** mới có nút bung — điều kiện đúng là
   `tồn_khả_dụng < tồn_thực_tế`. Dòng không bị ghim hiện chữ mờ *"không đơn nào ghim"*, không có
   nút.
3. Nút nằm ngay trong ô **Tồn khả dụng** của Bảng 1, dạng `▸ 18 đang ghim` — con số chính là
   phần đã bị trừ, nên người đọc thấy ngay nút này giải thích cái gì.
4. Bấm dòng nào bung bảng của **riêng dòng đó**, bấm lần nữa gập lại. Mỗi lúc chỉ cần một bảng.
5. Bỏ tick **Ghim Tồn Khả Dụng** thì không còn gì bị trừ → ẩn luôn cả nút bung lẫn chữ mờ, và
   gập bảng lại.

**Vì sao gập chứ không bung sẵn.** Đơn 20 dòng mà 12 dòng bị ghim thì bung sẵn ra 12 bảng, hơn
60 dòng, phải cuộn hết mới tới Bảng 2. Thứ tự công việc của sale là: trước hết trả lời *"đơn này
nhận được không"*, rồi mới đi hỏi nhường hàng cho **một** mặt hàng cụ thể. Đi hỏi ai là **bước
hai** — để sau một cú bấm là đúng chỗ của nó.

⚠ Khi code: nút chỉ được hiện khi thật sự có đơn khác ghim. Đừng hiện nút rồi bung ra bảng rỗng —
người dùng sẽ hiểu là hệ thống hỏng chứ không hiểu là "không có đơn nào".

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

## 11b. Hai việc đã tách sang tính năng khác (02/09)

Ghi ở đây để người đọc mục 5b và mục 2 lần ra được phần còn lại, vì cả hai **dùng chung con số
`custom_so_luong_giu_cho`** — đọc một mình một tính năng sẽ không hiểu vì sao lại có bước phân bổ.

| Việc | Đi đâu | Vì sao tách |
|---|---|---|
| **Phân bổ hàng vào phần ghim khi hàng mua đã về** | **PM-FEAT-00036** · `phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve` · hạn 14/09 | Anh Thắng mở 02/09. Hệ quả trực tiếp của luật *chặn cứng ở tồn khả dụng*: đơn cần 6 chỉ giữ được 4, hai cái còn lại phải được ghim **tự động** khi hàng về, không thì sale phải nhớ quay lại bấm tay |
| **Tạo Phiếu Yêu Cầu Mua Hàng** — ⚠ **quay lại tính năng này 03/09** | **PM-TASK-00140**, hạn 07/09. Anh Thắng tách ra 31/08, Tuấn giao phiên khác, rồi giao lại cho tôi vì nó dùng chung `kiem_tra()`. Code nằm trong `api/kiem_tra_ton_kho.py`, xem mục 12b | Khách yêu cầu 28/08. Cách tính đã chốt: `cần mua = đang thiếu − phiếu YCM đang chờ − đơn mua chưa về`, **không huỷ phiếu cũ, không chồng phiếu**. Lõi ERPNext đã làm sẵn phép trừ này cho mặt hàng trên đơn (`sales_order.py::get_requested_item_qty`); phần **Bảng 2 (NVL) phải tự tính** vì NVL không nằm trên đơn |

⚠ **Không có chức năng nhường hàng giữa hai đơn** — khách chốt 31/08 chọn *"A chỉ cần nhả ra, ai
lấy thì lấy"*. Nghĩa là phần A nhả ra vào **kho chung**, không đến đích danh B; hai bên tự gọi
điện cho nhau. Đừng dựng lại chức năng này nếu không có yêu cầu mới.

## 12b. Tạo Yêu Cầu Mặt Hàng từ phần thiếu (PM-TASK-00140)

`tinh_can_mua()` + `tao_yeu_cau_mua_hang()` trong `api/kiem_tra_ton_kho.py`.

**Chỉ lấy mặt hàng *Mua hàng*** (hoặc trống — coi như Mua hàng), theo đúng mô tả task. Mặt hàng
*Sản xuất/Gia công* trên đơn **không** vào phiếu: phần thiếu của chúng đã được bóc thành nguyên
vật liệu ở Bảng 2 rồi, đưa cả hai vào là mua cả thành phẩm lẫn vật tư làm ra nó.

### ⚠ KHÔNG cộng thẳng `thieu` của Bảng 1 với `thieu` của Bảng 2

Hai bảng **cùng trừ vào một lượng tồn**. Mã vừa bán trên đơn vừa là thành phần của mã khác sẽ
được tồn "che" hai lần, ra số thiếu **ÍT hơn thực tế** → mua hụt.

	X: cần 10 ở Bảng 1 + 6 ở Bảng 2, tồn khả dụng 4
	  cộng mù cột `thiếu`   →  (10−4) + (6−4) = 8   ❌ hụt 4
	  gom nhu cầu rồi trừ 1 lần → (10+6) − 4  = 12  ✅

Nên `tinh_can_mua` gom **nhu cầu** theo mã trước, rồi mới trừ tồn một lần. Đo 03/09: chỉ 3 mã
trên site vừa bán vừa là thành phần, cả 3 là dữ liệu thử — chưa hỏng thật, nhưng đừng để tới lúc
hỏng mới sửa.

### Trừ phần đã có người lo

	cần mua = nhu cầu − tồn khả dụng − Yêu Cầu Mặt Hàng đang chờ − Đơn mua chưa về

Không trừ thì bấm nút hai lần là đặt mua hai lần. Đây là chỗ đã hứa với anh Thắng 28/08.

⚠ Phần **Đơn mua chưa về** ở đây **không lọc ngày**, khác với cột *Ngày hàng về* (mục 8.2) vốn
chỉ hiện đơn có hạn trong tương lai. Hàng về muộn vẫn là hàng đã đặt; đặt thêm là mua thừa.

### Ba cái bẫy đã vấp khi dựng phiếu, đều chỉ lộ lúc LƯU

1. **`schedule_date` không được nhỏ hơn `transaction_date`** —
   `buying_controller.validate_schedule_date` throw. Đo 03/09: **8/8 đơn trên site có ngày giao
   trong quá khứ**, nên gần như đơn nào cũng vỡ nếu không kẹp về hôm nay.
2. **`Material Request Item.warehouse` là bắt buộc với hàng tồn kho** —
   `buying/utils.py::validate_stock_item_warehouse` throw. Lấy theo thứ tự: kho của Đơn Bán →
   kho trên dòng hàng → mặc định hệ thống. **Không gõ cứng tên kho**, tên mang hậu tố công ty.
3. **Phiếu để NHÁP, không `insert()` từ server.** Trả tài liệu chưa lưu cho client mở ra dạng
   form mới. Bấm nút mà đẻ ngay chứng từ là ngược luật đã ghi ở `CLAUDE.md`, và người bấm nhầm
   sẽ để lại phiếu rác.

### Đã đo trên 8012 (03/09)

Dựng một Đơn Bán thiếu hàng **trong giao dịch rồi `rollback`** — cách duy nhất chạy được nhánh
"có phiếu" vì mọi đơn thật trên site đều đủ tồn:

	đơn 100 vỏ VDP0X   →  13 dòng, lưu được, gắn đúng `sales_order`
	đơn ngày giao 24/08 (quá khứ)  →  phiếu lấy ngày hôm nay, `ngay_bi_kep = true`
	sau rollback       →  0 rò rỉ, không còn Đơn Bán lẫn phiếu thử nào

## 12c. Ba thứ chỉ lộ ra khi mở giao diện (03/09 chiều)

Cả ba đều **chạy đúng** dưới `bench execute` — không lệnh nào báo sai. Chúng chỉ lộ khi ngồi bấm
thật trên cổng 8012.

### 1. Ô tích nằm trong mục GẬP, người bán hàng không thấy

`custom_ghim_ton_kha_dung` neo sau `custom_note`, mà `custom_note` nằm trong mục **Thông Tin Sản
Xuất** — mục này mặc định **gập lại**. Mở đơn ra không có ô tích nào cả; phải bấm bung một mục tên
"Thông Tin Sản Xuất" thì nhân viên bán hàng mới thấy, và họ không có lý do gì để bấm vào đó.

➜ Neo lại sau `set_warehouse` (*Chọn kho xuất*), mục **Mật Hàng**, **không gập được**, nằm ngay
trên lưới hàng hoá mà nó điều khiển. `add_sales_order_ghim_fields.py` có thêm bước `_nan_vi_tri()`
sửa cả những site đã chạy bản patch cũ — `_create` bỏ qua trường đã tồn tại nên không tự sửa được.

**Bài học chung:** `insert_after` quyết định trường rơi vào MỤC nào, và mục có thể đang gập.
Chọn neo phải nhìn cả mục chứ không chỉ nhìn trường đứng cạnh.

### 2. Cột Giữ Chỗ LUÔN hiện, `depends_on` không giấu được cột lưới

`custom_so_luong_giu_cho` khai `depends_on: eval:parent.custom_ghim_ton_kha_dung`. Điều đó đúng
với ô nhập trong form chi tiết dòng, **không đúng với cột trên lưới**: `grid.js::setup_visible_columns`
dựng cột từ `user_defined_columns` (`__UserSettings.GridView`) và không hề đọc `depends_on`.

Đã thử `grid.toggle_display("custom_so_luong_giu_cho", false)` trên cổng 8012: **không ăn**. Nó đặt
`hidden` lên docfield toàn cục, còn `setup_user_defined_columns()` lấy docfield bằng
`frappe.meta.get_docfield(doctype, fieldname)` rồi tự gán `in_list_view = 1` đè lên; thêm nữa
`setup_visible_columns()` **thoát sớm** nếu `visible_columns` đã dựng.

➜ **Chấp nhận cột luôn hiện**, giá trị 0 khi đơn không ghim. Không đi ép cột ẩn động: phải viết
lại `user_defined_columns` lúc chạy, tức ghi vào cài đặt lưới dùng chung của người dùng — đắt và
dễ hỏng hơn nhiều so với một chữ số 0.

⚠ Chỗ này tôi **đã báo sai cho anh Thắng** ("cột chỉ hiện khi tích ô") trước khi mở giao diện ra
xem. Đã đính chính trên PM.

### 3. "Không cho nhập vượt tồn khả dụng" chưa hề được thực thi

Anh Thắng chốt 02/09 12:40, mockup bản 7 đã diễn cảnh gõ 99 tự về 15. Nhưng trong mã nguồn
**không có chỗ nào chặn**: `dien_muc_toi_da` chỉ kẹp lúc TỰ ĐIỀN, người dùng gõ tay sau đó thì
không ai kiểm. Gõ 99 trên tồn 31, bấm Lưu — lưu được.

Nguy ở chỗ con số này **không chỉ nằm trên đơn của mình**: `ghim_boi_don_khac` đọc thẳng nó rồi
trừ khỏi tồn khả dụng của **mọi đơn khác**. Một dòng ghim 99 trên tồn 31 làm các đơn còn lại thấy
thiếu ảo 68 cái và đi mua hàng không cần mua.

➜ Chặn ở **hai lớp**:

| Lớp | Ở đâu | Làm gì |
|---|---|---|
| Giao diện | `sales_order.js::kep_giu_cho` | gõ quá thì kéo về trần ngay, báo đỏ tại chỗ |
| Máy chủ | `python_hook/sales_order.py::chan_giu_cho_vuot_ton` | chặn thật, kể cả đường API / Data Import |

Hai điểm tinh trong hàm máy chủ:

- **Chỉ chặn khi người dùng TĂNG số.** Tồn tụt sau khi đơn đã lưu là chuyện bình thường; chặn cứng
  theo trần hiện tại sẽ khoá luôn những sửa đổi chẳng liên quan gì tới ghim — đúng cái bẫy
  `validate_schedule_date` của lõi đã giăng ở Yêu Cầu Mặt Hàng.
- **Cộng dồn theo mã, không xét từng dòng.** Nhiều dòng cùng một mã ăn chung một lượng tồn; xét
  riêng lẻ thì đơn 3 dòng × 20 trên tồn 20 lọt cả ba.

⚠ Bẫy đã vấp ngay khi viết: `ghim_khac, _ = ghim_boi_don_khac(...)` — `_` là **hàm dịch của
Frappe**, gán đè lên nó thì `_("...")` ở câu thông báo nổ `'list' object is not callable`. Chỗ nổ
nằm **trong nhánh chặn**, nên nhìn từ ngoài vẫn thấy "đã chặn thành công", chỉ sai câu thông báo.
Không có test in ra nguyên văn câu lỗi thì không ai phát hiện.

### Đã đo lại sau khi sửa (cổng 8012, 03/09)

	ô tích:  mục "Mật Hàng", không gập      → mở đơn là thấy ngay
	gõ 99 trên lưới (tồn 31, cần 20)        → tự về 20, báo đỏ
	lưu 99 bằng API                          → CHẶN, câu thông báo đúng chữ
	lưu 20 / lưu 0 / bỏ tích rồi lưu 99      → cho qua (đúng)
	giả lập tồn tụt còn 5, cũ 5 → mới 5 / 4  → cho qua (không tăng thì không khoá)
	                            cũ 5 → mới 6  → CHẶN
	2 dòng cùng mã, 3+3 trên tồn 5           → CHẶN ở dòng thứ hai

### 4. Anh Thắng bấm thật và tìm ra 2 lỗi nữa (03/09 10:32)

Anh dựng `SO-26-00009` và báo hai chuyện. Cả hai đều đúng, và cả hai đều **do chính tôi tự chặn**.

**a) Tích ghim trên đơn MỚI thì không có gì xảy ra.** Nguyên văn: *"lúc mới tạo phiếu anh chọn sản
phẩm xong tích ghim thì không thấy nó tính"*. Trong `sales_order.js` tôi viết
`if (!frm.doc.custom_ghim_ton_kha_dung || frm.is_new()) return;` — tự tay bỏ qua đơn chưa lưu, và
**không nói một lời nào** về việc đó. Nút *Kiểm Tra Tồn Kho* cũng bị gác sau `if (!frm.is_new())`.

Lý do lúc viết: `kiem_tra` nhận **tên đơn** rồi `frappe.get_doc` — đơn chưa lưu có tên
`new-sales-order-…` không tồn tại trong cơ sở dữ liệu. Nhưng cách xử lý đúng là **cho API nhận cả
tài liệu chưa lưu**, chứ không phải tắt tính năng đi trong im lặng.

➜ `kiem_tra(sales_order=None, doc=None)` + `_lay_don()`: client gửi nguyên `frm.doc` khi
`frm.is_new()`. `_gom_nhu_cau` giờ nhận **danh sách dòng** thay vì tên đơn — đơn chưa lưu không có
dòng nào trong cơ sở dữ liệu để mà truy vấn. Tên đơn trả về là `None` để `ghim_boi_don_khac` không
đi loại trừ một cái tên không tồn tại.

⚠ Nút *Tạo Yêu Cầu Mặt Hàng* **vẫn phải tắt** khi đơn chưa lưu — phiếu bắt buộc trỏ ngược về số Đơn
Bán, mà số đó chỉ có sau khi Lưu. Popup ghi rõ lý do thay vì để nút xám không giải thích.

**b) "Bán thành phẩm 1 giữ chỗ được 1 mà tồn đang 0."** — Đây **không phải lỗi**, và câu trả lời
nằm ở chỗ khác chứ không ở phép tính:

	Bán thành phẩm 1
	  Kho bán thành phẩm - HKL   actual_qty = 1   ← tồn thật nằm ở đây
	  Kho thành phẩm - HKL       actual_qty = 0   ← kho ghi trên DÒNG HÀNG, anh nhìn ô này

Tồn khả dụng cộng trên **cả 5 kho hợp lệ** (mục 3), không theo kho ghi trên dòng hàng. Anh nhìn
thấy 0 vì dòng hàng đang trỏ *Kho thành phẩm*.

➜ **Đã hỏi lại anh Thắng**: giữ cách cộng toàn kho (giữ chỗ được, nhưng lúc giao phải chuyển kho),
hay chỉ tính kho trên dòng hàng. Chưa tự đổi — đây là đổi định nghĩa "tồn khả dụng" của cả tính năng.

**c) Lỗi thứ ba tự lộ khi thử lại (2 dòng cùng mã).** `dien_muc_toi_da` tính từng dòng độc lập nên
đơn 2 dòng × 5 cái trên tồn 1 được điền **1 + 1**, rồi lớp kẹp mới dọn về **0 + 1** kèm một dòng
báo **ĐỎ**. Con số cuối đúng, nhưng người dùng chỉ tích một ô mà tưởng mình vừa làm hỏng gì đó —
và dòng nào về 0 thì tuỳ thứ tự callback, không đoán trước được.

➜ Chia theo thứ tự dòng và **trừ dần** (`con_lai[mã]`), thêm cờ `frm.__hkled_dang_dien` để lớp kẹp
không chen vào giữa lượt tự điền. Đo lại: 2 dòng × 5 trên tồn 1 → **1 và 0**, một dòng báo xanh,
không có báo đỏ nào.

### Kho trên phiếu mua — anh Thắng chốt CÁCH A (03/09 11:12)

Câu hỏi: phiếu Yêu Cầu Mặt Hàng sinh từ Bảng 2 cho **13 dòng vật tư về "Kho thành phẩm"** vì đó là
kho của Đơn Bán — sai về nghiệp vụ. Anh Thắng chốt **cách A**: khách khai kho mặc định cho mặt hàng,
hệ thống lấy theo đó. Anh mở luôn **PM-FEAT-00037** *"Bảng Kho mặc định và tồn kho tối thiểu của
từng mặt hàng"* để chứa phần khai.

Thứ tự ưu tiên mới trong `tao_yeu_cau_mua_hang`:

	kho mặc định CỦA MẶT HÀNG (Item Default, theo công ty)
	  → kho của Đơn Bán → kho trên dòng hàng → mặc định hệ thống

📌 **Lõi ERPNext đã có sẵn bảng này** — `Item.item_defaults` (child `Item Default`), mỗi dòng một
công ty, đã có cột `company` + `default_warehouse`. Trên site **đã có đủ 62.055 dòng**, chỉ là cột
kho đang trống (0/62.055). Nên PM-FEAT-00037 **không cần dựng bảng mới**: thêm đúng một cột *Tồn kho
khả dụng tối thiểu* vào bảng có sẵn là đủ. Đã báo anh Thắng.

⚠ Lõi còn một bảng nữa dễ nhầm: `Item.reorder_levels` (child `Item Reorder`) có
`warehouse_reorder_level` — cũng là "tồn tối thiểu" nhưng **theo KHO**, không theo công ty. Trên
site mới có 1 bản ghi. Chốt dùng bảng nào là việc của PM-FEAT-00037, đừng khai vào cả hai.

**Đo sau khi sửa (03/09, dựng đơn trong giao dịch rồi hoàn tác):**

	chưa khai kho mặc định  → 13/13 dòng vào "Kho thành phẩm"   (y như cũ, đúng: chưa có gì để lấy)
	khai 3 mã vật tư        → 3 mã đó vào "Kho nguyên vật liệu", 10 mã còn lại giữ kho Đơn Bán
	sau hoàn tác            → 0/62.055 Item Default có kho, 0 phiếu, 0 đơn rò rỉ

Tức là **hôm nay đổi thứ tự này chưa ra kết quả khác**; nó chỉ có tác dụng sau khi khách khai.
Viết trước để lúc khai xong là chạy đúng ngay.

### Còn một câu hỏi ĐANG CHỜ ANH THẮNG

Phiếu Yêu Cầu Mặt Hàng sinh từ Bảng 2 đang cho **13 dòng vật tư về "Kho thành phẩm"**, vì đó là
kho của Đơn Bán. Đo trên site: **0 / 62.055** bản ghi *Item Default* có khai kho mặc định, và
`Stock Settings.default_warehouse` cũng trống — nên hôm nay kho của Đơn Bán là **nguồn duy nhất**
có thể lấy, không phải lỗi lập trình. Nhưng vật tư về kho thành phẩm thì sai về nghiệp vụ.
**Chưa tự đổi** — đổi thứ tự ưu tiên là đổi hành vi anh Thắng chưa duyệt, và hôm nay đổi cũng
không ra kết quả khác vì không mặt hàng nào khai kho.

## 12d. Bảng 3 — nguồn lực nhân sự (làm 03/09)

`nguon_luc_nhan_su()` trong `api/kiem_tra_ton_kho.py`, hiện trong popup dưới Bảng 2.

### Đơn vị là PHÚT CHUẨN, không phải phút đồng hồ

Mục 8.1 định nghĩa khối lượng = `Σ(số lượng × Thời Gian Sản Xuất)`. Engine Phần III tiêu thụ khối
lượng đó với tốc độ `Σ(Năng Lực/100)`. Nên muốn so hai vế thì **Năng Lực phải nhân vào phía CUNG**:

	một người 90% ngồi 100 phút chỉ làm xong 90 phút chuẩn

Không nhân là so phút đồng hồ với phút chuẩn — hai đơn vị khác nhau, và sai **về phía báo đủ**.

	Tổng theo lịch = Σ (phút Employee Schedule trong kỳ × Năng Lực)
	Đã phân bổ     = Σ (phút Employee Allocation CHỒNG LÊN kỳ × Năng Lực)
	Còn lại        = Tổng − Đã phân bổ
	Đơn này cần    = Σ (số lượng × Thời Gian Sản Xuất) của mặt hàng Sản xuất/Gia công

Kỳ tính = **hôm nay → ngày giao của đơn**. Ngày giao đã qua thì kẹp về hôm nay và **nói ra**,
cùng cách với ngày trên Yêu Cầu Mặt Hàng.

### ⚠ R2 nặng hơn dự đoán: CẢ HAI VẾ đều rỗng

Đầu bài cảnh báo *"Bảng 3 sẽ ra gần 0 phút và luôn kết luận Đủ"*. Đo 03/09 thì tệ hơn — không
phải một vế rỗng mà **cả hai**:

	Employee Schedule   149 dòng / 3 người, nhưng chỉ tới 31/08  →  từ hôm nay: 0 dòng
	Employee Allocation còn hiệu lực trong tương lai:            0
	Mặt hàng Sản xuất/Gia công CHƯA khai Thời Gian Sản Xuất:     59.743 / 59.746

**0 so với 0 thì mọi phép so sánh đều ra "đủ".** Nên hàm trả về **bốn** trạng thái, không phải hai:

| Trạng thái | Khi nào | Hiện ra sao |
|---|---|---|
| `du` | đo được cả hai vế, còn lại ≥ cần | xanh |
| `khong_du` | đo được cả hai vế, còn lại < cần | đỏ |
| `chua_tinh_duoc` | **một trong hai vế chưa có dữ liệu** | cam + nói rõ thiếu gì |
| `khong_ap_dung` | đơn không có mặt hàng Sản xuất/Gia công | xám |

⚠ Chỗ dễ làm sai: khi **không ai có lịch**, đừng kết luận "không đủ". Không có lịch nghĩa là
**chưa ai xếp lịch**, không phải "hết người". Nói "không đủ" là đem một phỏng đoán ra trình bày
như sự thật — sale sẽ đi hẹn lại ngày giao với khách vì một con số không có thật.

Danh sách mặt hàng thiếu *Thời Gian Sản Xuất* hiện ngay dưới bảng (anh Thắng chốt 5.2) — đây là
cách duy nhất khiến R2 không im lặng.

⚠ Khi đo được một phần (`đơn này cần` > 0 nhưng vẫn còn mã chưa khai), kết luận **vẫn tính**
nhưng kèm câu *"thực tế sẽ CAO HƠN"*. Im lặng ở đây là báo đủ trong khi thiếu.

### Dòng kết luận gộp

Gộp trạng thái vật tư + nhân lực thành một câu (mục 6). Hai chi tiết cố ý:

- **Chỉ kể vế nào thật sự thiếu.** Bản đầu luôn in cả hai vế nên ra câu *"1 mặt hàng trên đơn và
  0 loại vật tư chưa đủ tồn"* — đọc như thể số 0 cũng là một vấn đề.
- **Nhân lực chưa đo được hoặc không đủ thì KHÔNG để nền xanh.** Người đọc lướt chỉ nhìn màu.

### Đã đo trên cổng 8012 (03/09)

	SO-26-00009 (không có lịch)      → 0/0/0 · cần 85 · CHƯA TÍNH ĐƯỢC, nêu lý do        ✅
	SO-26-00004 (hàng SX, ngày quá hạn) → cần 200 (= 20 × 10 phút), kẹp ngày về hôm nay  ✅
	SO-26-00002 (không có hàng SX)   → KHÔNG ÁP DỤNG                                      ✅
	đơn chưa lưu, 100 vỏ VDP0X       → CHƯA TÍNH ĐƯỢC + nêu đúng mã thiếu định mức        ✅
	dựng lịch 3 người × 1 ngày 8-17h → 1.566 phút chuẩn (540+540+540×0,9) · ĐỦ NHÂN LỰC   ✅
	thêm 1 phân bổ 08:20-09:00       → đã phân bổ 40, còn lại giảm đúng 40                ✅
	dọn xong                          → Employee Schedule về đúng 149 dòng, 0 rò rỉ       ✅

⚠ Bẫy đã vấp khi dựng dữ liệu thử: `Employee Schedule.start_time/end_time` là **trường chỉ đọc**,
hệ thống tự dựng từ `date` + `start`/`end`. Gán thẳng `start_time` thì bị ghi đè, khoảng thời gian
co về gần 0 và `Tổng theo lịch` ra `0,00015` phút. **Số vô lý là dấu hiệu dữ liệu thử sai, không
phải công thức sai** — đừng sửa công thức cho khớp số vô lý.

## 12f. 🔒 Bảng 2 TRỪ bán thành phẩm đang có trong kho (chốt 05/09/2026)

> **Anh Thắng 09:20:** *"Bảng 2 em cũng phải trừ bán thành phẩm đang có trong kho nhé, nói chung
> là nó cần phải bóc tách để tính ra được số nguyên vật liệu thiếu chính xác. Ví dụ thiếu 2 bán
> thành phẩm, 1 bán thành phẩm đã có sẵn tồn khả dụng rồi thì chỉ cần bóc nguyên vật liệu của 1
> bán thành phẩm thôi."*

Trước đó Bảng 2 chỉ trừ tồn ở **cấp 0** (phần thiếu của Bảng 1) rồi bóc **thẳng xuống lá**, coi
như trong kho không có bán thành phẩm nào. Hệ quả: hệ thống bảo đi mua nguyên vật liệu để làm ra
thứ đang nằm sẵn trong kho.

Nay `boc_dinh_muc_tru_ton` đi **từng cấp**, trừ **tồn khả dụng** ở mỗi cấp bằng một **bể dùng
chung** — bể chung để một cái hàng trong kho không che được nhiều nhánh cùng lúc, đúng cảnh báo
đã ghi từ đầu ở `boc_dinh_muc`.

**Đo thật trên `SO-26-00026` (05/09, đơn phải làm 9 `Thành phẩm 1`, kho có 6 `Bán thành phẩm 1`
và 1 `Bán thành phẩm 2`):**

| Mã | Cần — cách cũ | Cần — cách mới | Thiếu (mới) |
|---|---|---|---|
| `NVL 1` | 9 | **3** | 0 |
| `NVL 2` | 18 | **6** | 0 |
| `NVL 3` | 27 | **24** | 17 |

⚠ **Đây là con số đi mua hàng thật**, không phải hiển thị: cột *Thiếu* chảy thẳng vào phiếu Yêu
Cầu Mặt Hàng qua `tinh_can_mua`. Số cần mua `NVL 3` của đơn này giảm 20 → 17.

⚠ **Dòng đã đủ hàng vẫn phải hiện.** Bản đầu của hàm mới chỉ trả về phần còn thiếu, làm Bảng 2
mất hẳn dòng `NVL 1` và `NVL 2` — giảm thông tin âm thầm, đúng loại lỗi mục này sinh ra để chặn.
Hàm trả về **hai** thứ: nhu cầu gộp của mọi mã lá (để dựng bảng) và phần thật sự phải mua.

⚠ **Phần V KHÔNG dùng chung phép bóc này** — `api/nhu_cau_vat_tu.py` có đường nổ định mức riêng
(BOM → BOM Template → liệt kê). Đã rà 05/09. Câu hỏi *"Phần V có phải trừ bán thành phẩm không"*
là câu **chưa hỏi anh Thắng**, đừng tự suy từ chốt này.

➜ `boc_dinh_muc` cũ đã **xoá hẳn** sau khi đổi: để lại một hàm bóc-không-trừ nằm cạnh hàm
bóc-có-trừ là mời người sau gọi nhầm, mà gọi nhầm thì hệ thống mua dư chứ không báo lỗi.

---

## 12e. 🔴 Bảng lưu phần ghim vật tư — BẤT BIẾN PHẢI GIỮ (viết TRƯỚC khi code)

Anh Thắng chốt 04/09 11:04: **cần một bảng ghi lại số nguyên vật liệu đã ghim**. Mục này viết
trước khi có dòng code nào, vì thay đổi này **đổi loại dữ liệu của cả tính năng** và loại lỗi
đi kèm cũng đổi theo.

### Vì sao nguy hơn mọi thứ đã làm

Tới giờ mọi con số của tính năng đều **suy ra**: hỏi lại là tính lại từ đơn + định mức + tồn.
Dữ liệu suy ra có một tính chất quý mà không ai để ý vì nó miễn phí — **nó tự dọn**. Đơn bị huỷ
thì biến khỏi truy vấn; dòng hàng bị xoá thì không còn được cộng; định mức đổi thì lần sau ra số
mới. Không cần ai nhớ đi dọn.

**Bảng lưu thì không tự dọn.** Ghi vào rồi thì nó nằm đó tới khi có người xoá. Nên toàn bộ nhóm
lỗi dưới đây **chưa từng tồn tại** trong tính năng này, và bộ 49 ca hiện có **không ca nào chạm
tới** — vì trước đây chúng không thể xảy ra.

### Bất biến — mỗi dòng là một ca test bắt buộc

| # | Bất biến | Hỏng thì sao |
|---|---|---|
| 1 | Σ(ghim mọi đơn cho mã X) **≤ tồn thực tế** của X | Giữ nhiều hơn số đang có ➜ đúng con số âm anh Thắng bắt 03/09 16:34, quay lại bằng đường khác |
| 2 | Tổng trong bảng **khớp** số `ghim_boi_don_khac` trừ ra | Màn hình và lớp chặn xuất kho nói hai chuyện khác nhau; lệch **im lặng**, không nổ lỗi |
| 3 | Đơn **Huỷ / Đóng / Hoàn thành** ➜ phần ghim **biến khỏi bảng** | 🔴 **Nguy nhất.** Hàng bị một đơn đã chết giữ vĩnh viễn. Không ai phát hiện được bằng mắt vì màn hình chỉ hiện "đơn khác giữ" |
| 4 | **Bỏ tích Ghim** ➜ nhả sạch | Người dùng bỏ ghim để nhường hàng, tưởng đã nhả, thực tế vẫn giữ |
| 5 | **Xoá dòng hàng** khỏi đơn ➜ nhả phần vật tư của dòng đó | Vật tư mồ côi, không đơn nào dùng mà vẫn bị giữ |
| 6 | **Sửa định mức / BOM** ➜ bảng phải nói rõ đang theo định mức nào | Ghim theo công thức cũ, sản xuất theo công thức mới ➜ thiếu vật tư mà bảng báo đủ |
| 7 | **Huỷ rồi sửa lại đơn** (amend) ➜ bản mới kế thừa hay ghim lại từ đầu | Ghim nhân đôi: bản cũ chưa nhả, bản mới đã ghim. Cùng họ với `TC-EDGE-05` của Phần IV.1 |
| 8 | Ghim lại **chỉ tăng hoặc giữ nguyên** (nếu anh Thắng chốt đường (i)) | Cam kết tự tụt vì một thao tác không liên quan |

### Cách test phải khác trước

Bảy trong tám dòng trên **không kiểm được bằng "gọi hàm, so kết quả"** — đó là cách toàn bộ 49 ca
hiện nay đang làm. Chúng là **bất biến sau một CHUỖI thao tác**, nên phải test theo kịch bản:
ghim ➜ đổi ➜ huỷ ➜ đo lại, rồi so với bất biến.

➜ Mỗi lần chạy phải kèm một **phép kiểm tổng thể**: quét cả bảng, khẳng định 1 và 2 còn đúng.
Rẻ, và nó bắt được cả những đường hỏng chưa ai nghĩ ra.

### Chưa code được cho tới khi chốt xong Phần IV.2

Bảng này **chính là chỗ** Phần IV.2 (Phân bổ hàng về) rót hàng vào — hai thứ là một thiết kế.
Dựng bảng trước khi chốt 5 câu bên đó là dựng sai hình dạng rồi phải đập đi.

---

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
