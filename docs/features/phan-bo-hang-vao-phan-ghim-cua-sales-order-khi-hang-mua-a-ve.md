# Phân bổ hàng vào phần ghim của Sales Order khi hàng mua đã về

> **PM-FEAT-00036 · Phần IV.2 · Phân bổ hàng về vào phần đã ghim của Đơn bán hàng**
> Tên trên PM khác tên file này — nối hai bên bằng MÃ, không bằng tên. Xem `CLAUDE.md`.

**Khách hàng:** HKLED
**Người cung cấp thông tin:** anh Thắng (MBW) — viết đầu bài trên PM 31/08/2026 12:02
**Ngày dựng file:** 2026-09-03
**PM Project:** PM-PRJ-00003 · **PM Feature:** PM-FEAT-00036 · hạn 14/09/2026
**Trạng thái:** 🟡 **ĐANG CODE từ 04/09 tối** — 5 câu ở mục 4 đã chốt đủ (04/09 16:21), thiết kế bảng lưu ở mục 8.

> Mọi con số trong file này **đo trên cổng 8012 ngày 03/09/2026**, không lấy theo trí nhớ.

---

## 1. Đầu bài gốc (nguyên văn anh Thắng)

> Đây là 1 tính năng bổ sung trực tiếp trên phiếu Purchase Receipt, khi hàng về, người dùng tạo
> phiếu Purchase Receipt xong có thể ấn nút phân bổ, sau khi ấn nút thì những mặt hàng đang có số
> tồn khả dụng sẽ được phân bổ vào phần ghim hàng của những đơn Sales Order chưa ghim đủ. Ví dụ tồn
> khả dụng mặt hàng A đang là 0, đơn hàng A có ngày cần giao hàng là 26/8 số lượng là 5, mới được
> ghim 3, còn thiếu 2. đơn hàng B có ngày cần giao là 30/8 số lượng là 5, ghim 0. đơn hàng C có
> ngày cần giao là 2/9 số lượng 6, ghim 0. Hôm nay là ngày 28/8 hàng về số lượng 10. Sau khi ấn nút
> phân bổ, đơn hàng A sẽ được phân bổ trước -> đơn hàng A được ghim hiện tại là 5 -> tồn khả dụng
> còn 8. tiếp theo sẽ phân bổ sang đơn hàng B số lượng 5 -> tồn khả dụng còn 3 -> sau đó mới ghim
> đến đơn hàng C số lượng 3 -> đơn hàng C được ghim 3, còn thiếu 3. Ưu tiên phân bổ theo thứ tự
> hàng cần gấp trước.

Đã tính lại ví dụ: **khớp**. Về 10, A lấy 2 (3→5) còn 8, B lấy 5 còn 3, C lấy 3 và vẫn thiếu 3.

## 2. Hiểu lại bằng chữ của mình

Một vòng lặp chia hàng, không có gì bí ẩn:

	tồn khả dụng của mã X  =  tồn thực tế (5 kho hợp lệ) − phần các đơn khác đang ghim
	xếp các đơn còn thiếu X theo NGÀY CẦN GIAO tăng dần
	với mỗi đơn:  cho thêm = min(phần đơn còn thiếu, phần hàng còn lại)

Một điểm tốt sẵn có: nếu tồn khả dụng vẫn định nghĩa là `tồn − đã ghim` thì **bấm nút hai lần không
nhân đôi** — lần hai tự thấy hết hàng. Không cần cờ "đã phân bổ".

## 3. Đo hiện trạng — bốn con số đổi cách làm

| Đo được | Hệ quả |
|---|---|
| **0 / 1.825** mã *Mua hàng* từng xuất hiện trên dòng Đơn Bán | ⛔ chặn ở tiền đề, xem 4.1 |
| `custom_so_luong_giu_cho` và `custom_ghim_ton_kha_dung` đều **`allow_on_submit = 0`** | ⛔ chưa ghi được vào đơn đã duyệt, xem 4.2 |
| **0** Phiếu nhập mua đã duyệt trên site · **0 / 16** đơn đang mở có bật Ghim | không có dữ liệu để nghiệm thu, xem mục 6 |
| **1** đơn (`SAL-ORD-2026-00009`) có các dòng mang **2 ngày giao khác nhau** | "cần gấp" là ngày nào, xem 4.3 |

Kho bị loại khỏi mọi phép tính tồn (đã dựng từ PM-FEAT-00023): `Kho hàng lỗi cần sửa chữa`,
`Kho hàng lỗi/trả`, `Kho đang sản xuất`, `Kho trung chuyển`.

## 4. Năm câu phải chốt trước khi viết dòng code nào

> 🔒 **04/09 16:21 — ANH THẮNG ĐÃ TRẢ LỜI ĐỦ 5 CÂU.** Chốt gốc ở bình luận `kr9kb372ut` (15:59)
> và `24mlium3l1` (16:21) trên PM-FEAT-00036. Năm mục con bên dưới **giữ nguyên** vì chúng là lý
> do vì sao phải hỏi; phần chốt nằm ở đây.
>
> | Câu | Chốt | Nguồn |
> |---|---|---|
> | 4.1 Rót vào đâu | **Cách B** — ghim vật tư = bóc định mức phần *còn phải sản xuất*, kẹp ở tồn khả dụng. Hàng về thì rót vào chính phần vật tư đó | `kr9kb372ut` |
> | 4.2 Ghi vào đơn đã duyệt | **Mở khoá ô ghim** (`allow_on_submit = 1`) — *"Ô ghim em cho phép mở khóa khi đơn đã duyệt nhé"*. Không dùng `db_set` | `kr9kb372ut` |
> | 4.3 Ngày ưu tiên | **Ngày trên ĐẦU ĐƠN**, không phải ngày từng dòng — *"thực tế bên họ chỉ có 1 ngày trên đơn thôi"*; đơn `SAL-ORD-2026-00009` có 2 ngày là anh Thắng tạo nhầm. **Cùng ngày thì đơn tạo trước được trước** | `kr9kb372ut` + `24mlium3l1` |
> | 4.4 Đơn chưa bật Ghim | **Không chia** — *"đơn không bật ghim thì cũng đâu ghim được gì, bản chất là nó đang ghim 0"* | `kr9kb372ut` |
> | 4.5 Đơn tự đi đặt mua | **Không ưu tiên** — chia thuần theo ngày cần hàng | `kr9kb372ut` |
>
> **Ba chốt phát sinh trong cùng buổi chiều** (quan trọng ngang 5 câu trên):
>
> 1. **Sản xuất xong thì NHẢ vật tư, chuyển thành ghim thành phẩm** (`24mlium3l1`): *"cần 5A
>    nhưng chỉ còn 3A → ghim 3A → ghim nguyên vật liệu để sản xuất 2A → sau khi sản xuất xong
>    thì sẽ thành ghim 5A"*. Ví dụ 15:59 của anh Thắng cho SO1 giữ cả 5A **lẫn** 3B+2C là anh
>    viết nhầm, đã tự đính chính lúc 16:21 (*"à em nói đúng, nãy chắc anh viết nhầm đoạn đó"*).
> 2. **Lệnh sản xuất không bắt buộc gắn Đơn Bán** (`6mk75sbgr4`, `a2s3rb97h4`): hàng làm để tồn
>    kho thì không lên từ đơn bán; đơn nào thiếu thì họ tạo **Kế hoạch sản xuất từ đơn** rồi tạo
>    lệnh từ kế hoạch. ➜ Đường nối `Lệnh sản xuất → Kế hoạch sản xuất → Đơn Bán` **đã làm xong**
>    ở PM-FEAT-00034 (commit `ae1750a`, `TC-EDGE-18/19`).
> 3. **Vật tư thực tiêu hao không cần trùng vật tư đã ghim** — nhả đúng phần đã ghim theo tỉ lệ
>    sản xuất, không đối chiếu. Đề xuất của tôi ở `3e71p77v53`, anh Thắng không phản đối và đã
>    chuyển sang chốt tiếp; **ghi lại như một giả định**, không phải câu trả lời trực tiếp.


### 4.1 ⛔ Vật tư về thì rót vào đâu?

Đây là câu nặng nhất. Ô *Số Lượng Giữ Chỗ* **chỉ tồn tại trên dòng Đơn Bán**. Mà đo được **0 trên
1.825** mã *Mua hàng* từng nằm trên dòng Đơn Bán: hàng mua về là **vật tư**, dòng Đơn Bán là **đèn
thành phẩm**. Hai tập này hiện **không giao nhau một mã nào**.

Nghĩa là chạy đúng nguyên văn đầu bài thì **nút Phân bổ sẽ không tìm thấy gì để phân bổ**.

- **Cách A** — chỉ áp dụng cho mã vừa mua vừa bán (mua đi bán lại). Đúng nguyên văn, rẻ, nhưng
  phạm vi hôm nay là **0 mã**.
- **Cách B** — vật tư về thì quy ngược qua định mức: đơn nào đang thiếu vật tư đó ở Bảng 2 thì được
  tính là đã có hàng. Đây mới là thứ khách cần, nhưng **Bảng 2 không có ô ghim** — phải dựng thêm
  chỗ chứa, và phải trả lời "ghim vật tư cho đơn" nghĩa là gì khi vật tư còn phải qua sản xuất.

### 4.2 ⛔ Ghi vào đơn ĐÃ DUYỆT bằng đường nào?

Cả tính năng ghi vào đơn đã duyệt, mà hai trường ghim đang `allow_on_submit = 0`.

- **Bật `allow_on_submit`** — `doc.save()` chạy được, `validate` chạy theo nên lớp chặn
  `chan_giu_cho_vuot_ton` vẫn bảo vệ, có lưu vết sửa đổi. Đổi lại: **người dùng cũng sửa tay được**
  số ghim trên đơn đã duyệt, không chỉ nút Phân bổ.
- **Dùng `db_set`** — không phải bật cờ, nhưng **bỏ qua luôn `validate`**, tức bỏ qua lớp chặn
  giữ-chỗ-vượt-tồn, và không để lại vết trong lịch sử.

Tôi nghiêng về **bật `allow_on_submit`**: mất lớp chặn ở đường `db_set` là mất đúng cái vừa dựng
sáng 03/09 sau khi phát hiện luật "không cho vượt tồn" chưa từng chạy.

### 4.3 "Cần gấp trước" là ngày nào?

Đầu đơn (`Sales Order.delivery_date`) hay từng dòng (`Sales Order Item.delivery_date`)? Đã có **1
đơn thật** mà các dòng mang 2 ngày khác nhau. Phân bổ là việc **của từng mã**, nên tôi nghiêng về
**ngày của dòng**, lấy ngày đầu đơn làm dự phòng khi dòng trống.

Và **hai đơn cùng ngày thì ai trước?** Đề xuất: đơn nào tạo trước thì trước — cần một quy tắc cố
định, nếu không hai lần bấm cho ra hai kết quả khác nhau.

### 4.4 Đơn CHƯA bật Ghim có được phân bổ không?

Trong ví dụ, "đơn hàng B ghim 0" — là *đã bật Ghim nhưng chưa nhập số*, hay *chưa bật Ghim*?

Khác nhau rất lớn: hiện **0/16 đơn đang mở có bật Ghim**, nên nếu chỉ phân bổ cho đơn đã bật thì
hôm nay nút không làm gì cả. Còn nếu tự bật Ghim hộ người dùng thì **nút Phân bổ đang đổi trạng
thái đơn của người khác** mà họ không biết.

Đề xuất: **chỉ phân bổ cho đơn đã bật Ghim**, và sau khi chạy thì **báo rõ** "có N đơn đang thiếu
mã này nhưng chưa bật Ghim nên không được chia" — để người dùng tự quyết, thay vì im lặng bỏ qua.

### 4.5 Đơn đã tự đi đặt mua có được ưu tiên không?

Chuỗi truy ngược **đã có sẵn trong lõi, không phải dựng**: `Purchase Receipt Item.sales_order`,
`Purchase Order Item.sales_order`, `Material Request Item.sales_order` — và
`api/kiem_tra_ton_kho.py::tao_yeu_cau_mua_hang` **đã đóng dấu `sales_order`** lên từng dòng phiếu
nó sinh ra.

Nên hệ thống **biết chính xác lô hàng này được mua cho đơn nào**. Câu hỏi:

> Sale của đơn A tự đi lập phiếu mua 10 cái cho chính đơn A. Hàng về, đơn B có ngày giao gấp hơn
> nên theo quy tắc "gấp trước" thì **B lấy sạch**, A trắng tay dù A là người bỏ công đặt.

- **Giữ nguyên quy tắc gấp trước** — đơn giản, công bằng theo ngày giao, đúng nguyên văn đầu bài.
- **Trả về đơn đã đặt trước, phần dư mới chia theo ngày gấp** — giữ được cam kết, nhưng đơn gấp có
  thể trễ hàng.

⚠ Đây **không phải chức năng nhường hàng giữa hai đơn** mà khách đã bác 31/08 (*"A chỉ cần nhả ra,
ai lấy thì lấy"*). Chỗ đó nói về **nhả** hàng đang giữ; chỗ này nói về **chia** hàng mới về.

## 5. Ba cái bẫy đã thấy trước

1. **Kho nhận hàng có thể nằm ngoài tập kho được tính.** Nhập vào `Kho trung chuyển` hoặc
   `Kho đang sản xuất` thì hàng về thật mà hệ thống vẫn thấy tồn 0 → bấm Phân bổ không ra gì, và
   **không có lời nào giải thích**. Phải bắt ca này và nói thẳng ra.
2. **Phiếu nhập mua bị huỷ hoặc trả hàng.** Hàng đã chia vào ghim rồi mới huỷ phiếu → tồn tụt
   xuống dưới phần đã ghim. Lớp `chan_giu_cho_vuot_ton` cố ý **chỉ chặn khi TĂNG**, nên không tự
   gỡ. Cần chốt: gỡ ghim theo, hay để nguyên và báo?
3. **Nút phải chạy trên phiếu ĐÃ DUYỆT.** Hàng chỉ thực sự vào kho khi phiếu nhập mua được duyệt;
   bấm trên phiếu nháp thì `Bin.actual_qty` chưa đổi, chia ra sẽ là chia hàng chưa có.

## 6. Không nghiệm thu được nếu không có dữ liệu

Trên cổng 8012 hiện có **0 Phiếu nhập mua đã duyệt** và **0/16 đơn đang mở bật Ghim**. Trước khi
test, nhờ anh Thắng:

- bật Ghim + nhập số giữ chỗ cho **ít nhất 3 đơn** cùng một mã, **ngày giao khác nhau**;
- tạo và duyệt **1 phiếu nhập mua** cho mã đó, số lượng **ít hơn tổng phần thiếu** (để thấy đơn
  cuối bị chia thiếu, đúng như ví dụ trong đầu bài).

Cùng loại việc với đề nghị tạo đơn mua có *Required By* tương lai để nghiệm thu cột *Ngày hàng về*
ở PM-FEAT-00023 mục 12.

## 8. Thiết kế bảng lưu phần ghim vật tư (viết 04/09 tối, TRƯỚC khi code)

Tám bất biến phải giữ nằm ở **mục 12e** của `kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md`.
Mục này trả lời: *dựng cái gì để giữ được chúng.*

### 8.1 Vì sao phải LƯU, không suy ra như mọi con số khác

Đây là câu tôi tự vặn lại mình trước khi dựng, vì tính năng này tới giờ **không lưu gì cả** — và
dữ liệu suy ra thì tự dọn, còn dữ liệu lưu thì không.

Hai lý do bắt buộc phải lưu, cả hai đều đến từ chốt của anh Thắng:

1. **Chia hàng là việc phụ thuộc THỨ TỰ, không phải phép tính.** Tồn 2 `B`, hai đơn cùng cần —
   ai được là do *ai tới trước*, không suy ra được từ dữ liệu hiện tại. Suy lại lần sau, một đơn
   mới gấp hơn chen vào là kết quả đổi.
2. **Ghim là một CAM KẾT.** Đơn đã được chia hàng rồi thì thao tác của người khác không được làm
   nó tụt xuống (bất biến #8). Con số suy ra không giữ được cam kết — nó luôn là hàm của hiện tại.

➜ Nên bảng này là **sổ cam kết**: cấp phát tại một thời điểm rõ ràng, giữ nguyên tới khi có một
sự kiện nhả nó ra. Đúng loại dữ liệu mà mục 12e cảnh báo là "không tự dọn" — nên toàn bộ thiết kế
dưới đây xoay quanh việc **biến việc dọn thành cấu trúc**, thay vì trông vào trí nhớ của code.

### 8.2 Bảng CON của Đơn Bán, không phải DocType đứng riêng

Quyết định quan trọng nhất của mục này.

| | Bảng con của Đơn Bán | DocType đứng riêng |
|---|---|---|
| Bất biến #3 (đơn huỷ/đóng ➜ biến mất) | **Cấu trúc lo** — mọi truy vấn đã lọc `docstatus` + `status` của đơn cha, y hệt `ghim_boi_don_khac` đang làm | phải nhớ viết hook `on_cancel`, `on_update` cho *ba* trạng thái; quên một cái là hàng bị giam vĩnh viễn |
| Bất biến #7 (amend) | **Cấu trúc lo** — bản cũ `docstatus = 2` nên rơi khỏi bộ lọc, bản mới chép dòng sang | hai bản cùng sống trong bảng ➜ ghim nhân đôi, đúng ca `TC-EDGE-05` |
| Xoá đơn | dòng con xoá theo | mồ côi |
| Phân quyền | **thừa kế Đơn Bán** — không thêm truy vấn nào để phải tự nhớ lọc | phải khai `DocPerm` mới, và phải tự nhớ lọc theo User Permission (đúng chỗ đã rò ở `TC-PERM-02`) |
| Sửa trên đơn đã duyệt | cần `allow_on_submit = 1` — **anh Thắng đã đồng ý mở khoá ô ghim** | ghi thẳng, không vướng |

Bốn trong tám bất biến chuyển từ *"phải nhớ dọn"* sang *"không thể bẩn"*.

> 🔴 **Đo 04/09 tối — bảng con KHÔNG kín về phân quyền, và đó là hành vi của Frappe lõi.**
>
> Tôi định ghi *"thừa kế quyền Đơn Bán nên không rò rỉ"*. Đo lại thì sai. User
> `test.gioihan.sales@hkled.test` (bị User Permission giới hạn `Customer = a`) **không đọc được**
> `SO-26-00026` — `frappe.get_doc(...).check_permission("read")` ném `PermissionError`, và đơn đó
> không nằm trong 14 đơn user thấy. Nhưng:
>
>     frappe.client.get_list("HKLed Pinned Material", parent="Sales Order",
>                            filters={"parent": "SO-26-00026"})   ➜ trả về đủ 5 dòng
>
> **Không phải lỗi của bảng mới.** Chạy y hệt trên `Sales Order Item` của lõi cũng trả về dòng
> của chính đơn đó. Truy vấn bảng con chỉ kiểm quyền **ở cấp DocType cha**, không đi qua User
> Permission từng bản ghi. Nghĩa là mọi bảng con của Đơn Bán trên site này đều đang hở như nhau,
> từ trước khi có tính năng này.
>
> ➜ Ghi lại làm **hiện trạng đã đo**, không phải hạng mục của PM-FEAT-00036. Cùng họ với
> `TC-PERM-02`. Chọn bảng con vẫn đúng vì DocType đứng riêng còn phải tự dựng lớp lọc — tức thêm
> một chỗ nữa để sai, chứ không phải bớt. Đổi lại đúng một bất
tiện: ghi vào đơn đã duyệt phải qua `allow_on_submit`, mà chốt 4.2 đã cho phép.

➜ **Chọn bảng con.** `Sales Order` ➜ field `custom_ghim_vat_tu` (Table), child DocType
`HKLED Ghim Vat Tu`.

### 8.3 Cấu trúc dòng

| Trường | Kiểu | Vì sao có |
|---|---|---|
| `item_code` | Link Item | mã vật tư bị ghim |
| `tu_ma` | Link Item | thành phẩm nào sinh ra nhu cầu này — truy vết, và là chìa để cắt phần dư khi dòng hàng đổi (bất biến #5) |
| `so_luong` | Float | **số đang thực sự ghim** — con số duy nhất mà mọi phép cộng dùng |
| `nhu_cau` | Float | nhu cầu theo định mức lúc cấp phát. `nhu_cau − so_luong` = phần còn thiếu, chính là phần nút *Phân bổ* sẽ rót vào |
| `dinh_muc` | Link BOM | **bất biến #6** — ghim theo định mức nào |
| `dinh_muc_sua_luc` | Datetime | `BOM.modified` lúc cấp phát. Lệch với hiện tại ➜ định mức đã đổi sau khi ghim, phải cảnh báo chứ không âm thầm dùng số cũ |
| `cap_nhat_luc` | Datetime | lúc dòng này được cấp phát/sửa lần cuối |

⚠ Một dòng cho mỗi cặp **(thành phẩm sinh ra nhu cầu, vật tư)**, không gộp theo vật tư. Gộp thì
mất `tu_ma` và `dinh_muc`, và bất biến #5 + #6 hết đường kiểm.

### 8.4 Tồn tự do — chỗ duy nhất được lấy hàng ra để cấp phát

	tồn tự do(X) = tồn thực tế(X, tập kho hợp lệ)
	               − Σ custom_so_luong_giu_cho(X) của mọi đơn còn sống
	               − Σ so_luong(X) trong bảng ghim vật tư của mọi đơn còn sống

**Chỉ cấp phát từ tồn tự do.** Bất biến #1 (Σ ghim ≤ tồn thực tế) khi đó **đúng theo cấu trúc**,
không phải nhờ một phép kiểm chạy sau. Đây là chỗ khác hẳn cách làm cũ: `_kha_dung()` hiện kẹp
`min(ghim, tồn)` **lúc đọc** — tức vẫn cho ghim vượt rồi che đi lúc hiển thị. Bảng lưu thì không
được phép ghi con số vượt vào.

*"Đơn còn sống"* = `docstatus = 1` **và** `custom_ghim_ton_kha_dung = 1` **và**
`status ∉ {Closed, Completed, Cancelled}` — **cùng một bộ lọc** với `ghim_boi_don_khac`, cố ý
dùng chung một hàm để hai bên không bao giờ hiểu khác nhau (bất biến #2, #3, #4).

### 8.5 Cấp phát — đệ quy theo cấp, kẹp ở mỗi cấp

Đúng ví dụ anh Thắng viết 15:59, tổng quát hoá cho định mức nhiều cấp:

	nhu cầu cấp 0 = số ghim thành phẩm người dùng nhập (đã bị `chan_giu_cho_vuot_ton` chặn không cho vượt)
	lặp từng cấp:
	    phần còn phải sản xuất = nhu cầu − tồn đã có (hàm `_con_phai_lam` sẵn có)
	    bóc định mức MỘT cấp   = nhu cầu vật tư của cấp dưới (hàm `_con_mot_cap` sẵn có)
	    cấp phát               = min(nhu cầu vật tư, tồn tự do), theo thứ tự ưu tiên giữa các đơn
	    phần chưa được cấp     → nếu vật tư đó là hàng SẢN XUẤT thì xuống cấp tiếp
	                             nếu là hàng MUA thì dừng — đó là phần phải đi mua

Thứ tự ưu tiên giữa các đơn (chốt 4.3): **`delivery_date` đầu đơn tăng dần, cùng ngày thì
`creation` tăng dần**. Cố định, nên hai lần chạy cho cùng một kết quả.

⚠ Khác một điểm so với `ghim_boi_don_khac` hôm nay: hàm đó gọi `boc_dinh_muc` **bóc thẳng xuống
lá**, nên bán thành phẩm ở giữa không được ghim dù trong kho đang có. Ghim đúng phải **dừng ở
cấp nào có hàng thật** — hàng có thật mới đặt riêng ra được. Đây là thay đổi hành vi, phải có ca
test riêng.

### 8.6 Nhả — năm đường, ba đường là cấu trúc

| Sự kiện | Cách nhả | Loại |
|---|---|---|
| Đơn Huỷ / Đóng / Hoàn thành | rơi khỏi bộ lọc "đơn còn sống" | **cấu trúc** |
| Bỏ tích *Ghim tồn khả dụng* | rơi khỏi bộ lọc (`custom_ghim_ton_kha_dung = 0`) | **cấu trúc** |
| Amend đơn | bản cũ `docstatus = 2` ➜ rơi khỏi bộ lọc | **cấu trúc** |
| Giảm số ghim thành phẩm / xoá dòng hàng | tính lại nhu cầu, **cắt phần dư** ở dòng có `tu_ma` tương ứng | phải viết code |
| Sản xuất xong | cộng phần ghim thành phẩm ➜ vật tư tự nhả theo | **đã làm 04/09 tối**, xem 8.8 |

⚠ Bỏ tích *không xoá* dòng trong bảng, đúng luật 2 của mục 2 đặc tả (*"bỏ tích không xoá số đã
nhập"*). Nó chỉ ngừng có hiệu lực. Tích lại thì cam kết cũ còn nguyên — **nhưng** trong lúc bỏ
tích, hàng đó đã thành tồn tự do và đơn khác có thể đã lấy mất. Nên lúc tích lại phải chạy lại
phép kiểm bất biến #1 và **cắt xuống** nếu không còn đủ hàng. Đây là ca test bắt buộc.

### 8.7 Phép kiểm bất biến — chạy được bằng một lệnh

`kiem_bat_bien()` quét toàn bộ bảng và khẳng định:

1. mỗi mã: Σ ghim (thành phẩm + vật tư, mọi đơn còn sống) **≤** tồn thực tế
2. tổng theo mã của bảng **khớp** phần vật tư mà `ghim_boi_don_khac()` trả về
3. không có dòng nào thuộc đơn đã chết
4. không có dòng nào `so_luong > nhu_cau`
5. mọi `dinh_muc` còn `is_active` và `dinh_muc_sua_luc` khớp `BOM.modified`

Mục 12e đòi *"mỗi lần chạy phải kèm một phép kiểm tổng thể"* — đây chính là nó. Rẻ (3 truy vấn),
và bắt được cả đường hỏng chưa ai nghĩ ra.

### 8.8 Sản xuất xong ➜ nhả vật tư, chuyển thành ghim thành phẩm (làm 04/09 tối)

🔒 Anh Thắng chốt 04/09 16:21: *"cần 5A nhưng hiện tại chỉ còn 3A, lúc này chỉ ghim được 3A ➜
ghim nguyên vật liệu để sản xuất 2A ➜ sau khi sản xuất xong thì sẽ thành ghim 5A"*.

**Cơ chế chỉ có một dòng việc: cộng phần ghim thành phẩm. Vật tư tự nhả.**

Không có đoạn code nào đi xoá dòng vật tư. Nhu cầu vật tư sinh ra từ `cần − đã giao − đã ghim`
(8.5); cộng vào phần ghim thành phẩm là số đó tự tụt, và lần đồng bộ chạy trong **cùng lần lưu**
cắt các dòng vật tư xuống mức mới. Đo thật: sản xuất 5 chiếc ➜ ghim 31 → 36, phải làm 9 → 4,
`NVL 1` 8 → 3, `NVL 2` 16 → 6, nhu cầu `NVL 3` 24 → 9.

➜ Ba vướng tôi nêu với anh Thắng lúc 16:23 **tự giải** nhờ cách này:

| Vướng | Cách này trả lời |
|---|---|
| 2 — sản xuất **từng phần** | Không cần luật riêng: làm 5 trong 9 thì cộng 5, phần vật tư tụt theo đúng tỉ lệ |
| 3 — **khe hở** lúc vừa sản xuất xong | Không có khe: chạy trong `on_submit`, cùng giao dịch với bút toán kho |
| 4 — vật tư **thực tiêu hao** khác vật tư đã ghim | Không đối chiếu, đúng như đề nghị: phần ghim là hàm của *còn phải làm*, không của *đã tiêu hao* |

**Ba trần khi cộng**, thiếu cái nào cũng sai: phần đơn còn thiếu · số vừa sản xuất còn lại (một
lệnh có thể chia cho nhiều đơn) · **tồn tự do**.

**Huỷ chứng từ sản xuất** thì kéo ngược phần ghim xuống — hàng đã bay khỏi kho, không kéo xuống
là đơn giữ nhiều hơn số đang có (bất biến #1). Đo thật: huỷ xong mọi con số về đúng như trước.

⚠ Lệnh sản xuất **không nối được về Đơn Bán** (17/33 lệnh, làm để tồn kho) thì không chuyển gì —
đúng thiết kế, xem `api/ghim_vat_tu.don_ban_cua_lsx`.

### 8.9 Nút Phân Bổ (làm 05/09 sáng)

Trên **Phiếu nhập mua đã duyệt**, đúng chỗ anh Thắng chỉ trong đầu bài gốc.

Chia **hai loại thiếu**, không phải một: hàng bán thẳng thì rót vào ô *Số Lượng Giữ Chỗ*; vật tư
thì rót vào sổ cam kết. Ví dụ của anh Thắng là loại thứ nhất, nhưng chốt cách B nói hàng mua về
là **vật tư** — mà đo được 0/1.825 mã *Mua hàng* từng nằm trên dòng Đơn Bán, nên chỉ làm loại thứ
nhất thì nút bấm xong không tìm thấy gì để phân bổ.

Cả hai loại đi **chung một vòng lặp** theo thứ tự ưu tiên. Tách hai vòng thì đơn gấp nhất chỉ
được ưu tiên trong loại của nó, còn đơn xếp sau lại lấy trước ở loại kia.

**Không cần cờ "đã phân bổ"** — cả hai loại chỉ lấy từ tồn tự do, mà tồn tự do đã trừ phần đã
ghim. Bấm lần hai tự thấy hết hàng. Đo thật: lần hai rót thêm 0 dòng.

Ba thứ hộp thoại **phải nói ra** thay vì im lặng: kho nhận hàng nằm ngoài tập tính tồn · đơn đang
thiếu mã đó nhưng chưa bật Ghim · phiếu chưa duyệt.

### 8.10 Sửa tay phần ghim vật tư + thu hồi khi huỷ phiếu (làm 05/09, chốt sáng 05/09)

**Sửa tay** — anh Thắng 09:20: *"anh muốn sửa được không, vì có thể có trường hợp các bạn nhường
nhau 1 vài nguyên vật liệu trong đó"*.

Không phải chỉ mở khoá. Bảng được **tính lại mỗi lần lưu đơn**, nên mở khoá suông thì người dùng
sửa xong, lưu phát nữa là số cũ quay lại mà không có thông báo nào. Ba thứ phải đi cùng:

1. Máy **đánh dấu** dòng vừa bị can thiệp (so số trên form với số dưới database).
2. Dòng đã đánh dấu: máy **chỉ được cắt xuống khi hết hàng**, không tự ghim thêm.
3. Gõ vượt phần giữ được thì **kẹp xuống và nói ra** — cùng lối với ô *Số Lượng Giữ Chỗ*.

⚠ Riêng **nút Phân Bổ thì chia lại bình thường** theo thứ tự ưu tiên, không kiêng dòng đã đánh
dấu (anh Thắng chốt 09:39). Ranh giới nằm ở đó: *lần lưu tự động* tôn trọng con số người đặt,
*cú bấm nút* thì chia lại.

**Thu hồi khi huỷ phiếu nhập** — anh Thắng duyệt 09:39 đúng thứ tự:

1. lấy lại từ **đúng đơn đã được chia từ phiếu đó**;
2. còn vượt tồn thì cắt tiếp của đơn **ít gấp nhất**;
3. **liệt kê rõ** đã cắt của ai bao nhiêu, không cắt im lặng.

Bước 1 cần nhớ *đã chia cho ai* — sổ ghim chỉ lưu *đơn nào giữ mã nào bao nhiêu*. Nên nút Phân Bổ
ghi **nhật ký** vào chính phiếu nhập (`Purchase Receipt.custom_ghim_da_phan_bo`), **cộng dồn**
chứ không ghi đè.

⚠ Bước 2 không bỏ được: đơn được chia có thể đã **mang vật tư đi sản xuất** rồi, phần ghim đã
tiêu, không còn gì để trả — mà tồn vẫn tụt. Ai đó vẫn phải nhả, và người đó không phải người đã
nhận.

> 🔴 **Ca này đã xảy ra thật trên cổng 8012 ngày 05/09, do anh Thắng tự chạy thử trước khi hỏi.**
> 09:08 tạo `PNK-26-00004` 10 `NVL 3` ➜ bấm *Phân Bổ* ➜ 10 cái vào `SO-26-00028`; 09:09 **huỷ
> phiếu** ➜ tồn tụt về 7 nhưng phần ghim vẫn **17**. Hậu quả: `NVL 3` còn 7 cái thật mà mọi đơn
> đều thấy tồn khả dụng **0** — hàng bị giam, không một thông báo nào.
>
> **Phép kiểm bất biến ở mục 8.7 bắt được chỗ này**, đúng việc nó sinh ra để làm. Đã sửa dữ liệu
> thật: dựng nhật ký hồi tố cho `PNK-26-00004` (bằng chứng lấy từ lịch sử sửa đổi của
> `SO-26-00028` lúc 09:08:22, dòng qty 0 → 10) rồi chạy thu hồi ➜ cắt đúng 10 của
> `SO-26-00028`, `SO-26-00026` không bị đụng.

### 8.11 Vẫn CHƯA làm

- **Ghim vượt cấp cho bán thành phẩm mua ngoài** — 8.5 đổi hành vi, cần đo lại trên dữ liệu thật.
- 🔴 **Bảng 2 phải trừ bán thành phẩm đang có trong kho** — anh Thắng chốt 05/09 09:20: *"thiếu 2
  bán thành phẩm, 1 cái đã có sẵn tồn khả dụng rồi thì chỉ cần bóc nguyên vật liệu của 1 bán
  thành phẩm thôi"*. Tức **24 đúng, 27 sai**. Đây là sửa vào phép bóc định mức của PM-FEAT-00023
  — một tính năng **đã nghiệm thu** — và cột *Thiếu* chảy thẳng vào phiếu Yêu Cầu Mặt Hàng, nên
  **số đi mua sẽ giảm**. Phải làm riêng một nhánh và chạy lại cả 49 ca cũ, đồng thời rà xem Phần
  V có dùng chung phép bóc đó không.

---

## 7. Liên quan

- `kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md` — nguồn của định nghĩa *tồn khả dụng*, tập
  kho hợp lệ, và hai trường ghim. **Đổi định nghĩa ở đó là đổi luôn tính năng này.**
- `ghim-ton-kha-dung-toan-canh.md` — vì sao không dùng `Stock Reservation Entry` của lõi.
- **PM-FEAT-00037** — bảng Kho mặc định + tồn kho tối thiểu; ảnh hưởng kho nhận hàng.
- ⚠ Một câu ở PM-FEAT-00023 **chưa được trả lời** và chạm thẳng vào đây: *tồn khả dụng cộng trên
  tất cả kho, hay chỉ kho ghi trên dòng hàng?* Chốt cách nào thì tính năng này chia theo cách đó.
