# Phân bổ hàng vào phần ghim của Sales Order khi hàng mua đã về

> **PM-FEAT-00036 · Phần IV.2 · Phân bổ hàng về vào phần đã ghim của Đơn bán hàng**
> Tên trên PM khác tên file này — nối hai bên bằng MÃ, không bằng tên. Xem `CLAUDE.md`.

**Khách hàng:** HKLED
**Người cung cấp thông tin:** anh Thắng (MBW) — viết đầu bài trên PM 31/08/2026 12:02
**Ngày dựng file:** 2026-09-03
**PM Project:** PM-PRJ-00003 · **PM Feature:** PM-FEAT-00036 · hạn 14/09/2026
**Trạng thái:** ⛔ **CHƯA CODE — đang chờ anh Thắng trả lời 5 câu ở mục 4.**

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

## 7. Liên quan

- `kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md` — nguồn của định nghĩa *tồn khả dụng*, tập
  kho hợp lệ, và hai trường ghim. **Đổi định nghĩa ở đó là đổi luôn tính năng này.**
- `ghim-ton-kha-dung-toan-canh.md` — vì sao không dùng `Stock Reservation Entry` của lõi.
- **PM-FEAT-00037** — bảng Kho mặc định + tồn kho tối thiểu; ảnh hưởng kho nhận hàng.
- ⚠ Một câu ở PM-FEAT-00023 **chưa được trả lời** và chạm thẳng vào đây: *tồn khả dụng cộng trên
  tất cả kho, hay chỉ kho ghi trên dòng hàng?* Chốt cách nào thì tính năng này chia theo cách đó.
