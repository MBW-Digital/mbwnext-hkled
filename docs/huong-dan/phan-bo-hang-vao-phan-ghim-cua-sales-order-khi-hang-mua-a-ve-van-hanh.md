# Hướng dẫn sử dụng: Giữ chỗ vật tư và chia hàng khi hàng mua về

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED (`PM-FEAT-00036`)
> **Đối tượng:** Nhân viên kinh doanh · Thủ kho · Nhân viên mua hàng
> **Cập nhật:** 2026-09-08
> **Mục đích:** Giữ trước phần vật tư mà đơn hàng của mình cần, và chia hàng vừa mua về cho các đơn đang thiếu theo đúng thứ tự cần gấp.

---

## Mục lục

1. [Tính năng này dùng để làm gì](#1-tính-năng-này-dùng-để-làm-gì)
2. [Chuẩn bị trước khi dùng](#2-chuẩn-bị-trước-khi-dùng)
3. [Các bước thực hiện](#3-các-bước-thực-hiện)
4. [Kiểm tra kết quả](#4-kiểm-tra-kết-quả)
5. [Thông báo lỗi thường gặp](#5-thông-báo-lỗi-thường-gặp)
6. [Câu hỏi thường gặp](#6-câu-hỏi-thường-gặp)

---

## 1. Tính năng này dùng để làm gì

Khi một Đơn Bán Hàng cần hàng mà kho không đủ, hệ thống **giữ trước phần đang có** cho đơn đó, và
**bóc tiếp theo định mức** xem còn thiếu những vật tư nào. Phần đã giữ thì đơn khác không dùng
được nữa.

Khi hàng mua về, người mua hàng bấm một nút để **chia phần vừa về** cho các đơn đang thiếu — đơn
nào cần gấp hơn được chia trước.

**Ví dụ tình huống:** Đơn `SO-26-00026` cần 40 chiếc *Thành phẩm 1*, kho chỉ còn 31. Hệ thống giữ
31 chiếc đó cho đơn này, rồi tính 9 chiếc còn lại cần những vật tư gì để sản xuất, và giữ luôn
phần vật tư đang có. Hôm sau hàng mua về, bấm **Phân Bổ** là phần vừa về tự chảy vào chỗ còn
thiếu.

---

## 2. Chuẩn bị trước khi dùng

- **Quyền cần có:**
  - Bật giữ chỗ trên đơn: người sửa được Đơn Bán Hàng.
  - Bấm **Phân Bổ**: thủ kho hoặc nhân viên mua hàng — nhưng **phải xem được tất cả Đơn Bán
    đang giữ chỗ**. Xem mục [5](#5-thông-báo-lỗi-thường-gặp) nếu bị chặn.
- **Dữ liệu phải khai trước:** mặt hàng cần sản xuất phải có **định mức (BOM)**, nếu không hệ
  thống không bóc được xuống vật tư.
- **Cấu hình liên quan:** xem
  [phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve-cau-hinh.md](phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve-cau-hinh.md).

---

## 3. Các bước thực hiện

> 📌 **Màn hình của bạn có thể đang chạy tiếng Anh.** Site HKLED đặt ngôn ngữ mặc định là
> **English**, và hiện **8/10 tài khoản** để tiếng Anh. Nên các ô **do MBWNext thêm** hiện tiếng
> Việt (*Ghim Tồn Khả Dụng*, *Đã Ghim*…), còn **nút và tên màn hình của hệ thống** hiện tiếng
> Anh. Dưới đây ghi kèm cả hai ở lần nhắc đầu.

### Bước 1 — Bật giữ chỗ cho đơn hàng

1. Mở **Đơn Bán Hàng** (*Sales Order*) cần giữ chỗ.
2. Tích ô **Ghim Tồn Khả Dụng** — nằm ở **phần đầu đơn, ngay dưới ô *Set Source Warehouse***.
3. Bấm **Lưu** (*Save*), rồi **Duyệt** (*Submit*) đơn.

> ⚠️ **Đơn chưa duyệt thì chưa giữ chỗ được.** Tích ô rồi bấm Lưu trên đơn nháp, bảng
> **Ghim Vật Tư** sẽ để trống và hệ thống hiện câu nhắc:
> *"Đơn chưa duyệt nên chưa giữ chỗ được vật tư — bảng cam kết để trống là đúng, không phải lỗi.
> Duyệt đơn thì phần ghim mới có hiệu lực."*
> Đây là đúng, không phải hỏng. Duyệt đơn xong bảng sẽ có số.

### Bước 2 — Xem hệ thống đã giữ được những gì

Ngay dưới lưới hàng hoá của đơn có bảng **Ghim Vật Tư**:

| Cột | Nghĩa |
|---|---|
| **Từ Mặt Hàng** | vật tư này bóc ra từ mặt hàng nào trên đơn |
| **Vật Tư** | mã vật tư |
| **Phải Làm** | còn phải sản xuất bao nhiêu chiếc mặt hàng cha |
| **Nhu Cầu** | tổng vật tư cần cho phần phải làm đó |
| **Đã Ghim** | phần đã giữ được — **luôn ≤ phần kho đang còn rảnh** |
| **Giữ Nguyên** | xem [Bước 4](#bước-4--nhường-bớt-hàng-cho-đơn-khác) |

> 📌 Mở một dòng ra (bấm vào dòng) sẽ thấy thêm ba ô: **Định Mức**, **Định Mức Sửa Lúc**,
> **Cập Nhật Lúc**. Đó là **dấu vết kỹ thuật** để đối chiếu khi cần, **không phải đụng tới**.

Hệ thống **chỉ giữ phần kho thật sự đang rảnh**, đã trừ phần các đơn khác giữ trước. Nên *Đã Ghim*
nhỏ hơn *Nhu Cầu* là bình thường — phần chênh là phần phải đi mua.

### Bước 3 — Chia hàng khi hàng mua về

1. Mở **Phiếu Nhập Mua** đã **Duyệt**.
2. Bấm nút **Phân Bổ** ở góc trên bên phải.
3. Đọc hộp thoại kết quả rồi đóng lại.

Hộp thoại liệt kê **đã chia gì cho đơn nào** — mặt hàng, đơn bán, số ghim thêm.

> ⚠️ Nút **Phân Bổ** chỉ hiện trên phiếu **đã duyệt**. Phiếu còn nháp thì chưa có nút, vì hàng
> chưa vào kho.

> ⚠️ Bấm **Phân Bổ** là **chia ngay**, không có bước xác nhận. Nhưng bấm nhiều lần cũng không
> nhân đôi: lần thứ hai sẽ báo *"Không chia được gì thêm — hoặc các đơn đã ghim đủ, hoặc hàng
> vừa về đã có chủ."*

**Thứ tự chia:** đơn nào **ngày giao sớm hơn** được chia trước; hết phần của đơn đó mới sang đơn
kế tiếp. Hai đơn cùng ngày thì đơn tạo trước được ưu tiên. **Chỉ chia cho đơn đang bật *Ghim Tồn
Khả Dụng***.

Hộp thoại còn cảnh báo ba việc, đọc kỹ vì đây là phần dễ bỏ sót:

- **Hàng nhập vào kho không được tính tồn** — hàng về thật nhưng nằm ở kho lỗi hoặc kho trung
  chuyển nên hệ thống chưa coi là dùng được, không chia được.
- **Đơn đang thiếu mã này nhưng chưa bật *Ghim Tồn Khả Dụng*** — đơn đó không được chia, vì nó
  không giữ chỗ.
- Phần còn thiếu của từng đơn sau khi chia.

### Bước 4 — Nhường bớt hàng cho đơn khác

Khi hai đơn cần cùng một vật tư và muốn nhường nhau:

1. Mở đơn đang giữ nhiều.
2. Gõ số nhỏ hơn vào ô **Đã Ghim** của dòng cần nhường.
3. Bấm **Lưu**.

Dòng vừa sửa sẽ được tích ô **Giữ Nguyên**, nghĩa là *"người dùng tự đặt số này — hệ thống đừng
tự ghim lại"*. Phần nhả ra thành hàng rảnh, đơn khác dùng được ngay.

> ⚠️ Ô **Giữ Nguyên** chỉ nên do **người dùng** làm cho bật lên. Nếu thấy nó tự bật mà không ai
> sửa gì thì báo lại — đó là lỗi.

> 🔴 **Giữ Nguyên chống cái gì, và KHÔNG chống cái gì — đọc kỹ chỗ này.**
>
> Ô **Giữ Nguyên** giữ số bạn vừa đặt qua các lần **Lưu đơn** — hệ thống sẽ không tự ghim lại.
>
> Nó **không** giữ qua lần **Phân Bổ** kế tiếp. Hàng mới về thì chia lại từ đầu theo thứ tự cần
> gấp, kể cả dòng đang tích Giữ Nguyên (chốt của anh Thắng 05/09 09:39).
>
> **Nghĩa là:** nếu bạn vừa nhường hàng cho đơn khác mà sau đó có người bấm **Phân Bổ**, phần
> bạn nhường **có thể quay lại đơn bạn** — và bạn **phải nhường lại**. Muốn chắc thì báo người
> mua hàng biết trước khi họ bấm.

### Bước 5 — Huỷ phiếu nhập mua

Nếu phải huỷ một Phiếu Nhập Mua đã bấm **Phân Bổ**, hệ thống **tự thu hồi** đúng phần đã chia từ
phiếu đó. Không phải làm gì thêm.

Nếu đơn nhận hàng đã mang vật tư đi sản xuất mất rồi thì không còn gì để trả, hệ thống sẽ **cắt
của đơn ít gấp nhất** và ghi rõ đã cắt của ai bao nhiêu.

---

## 4. Kiểm tra kết quả

- **Trên đơn bán:** bảng **Ghim Vật Tư** có dòng, cột *Đã Ghim* có số.
- **Sau khi bấm Phân Bổ:** hộp thoại liệt kê phần đã chia; mở lại đơn thấy *Đã Ghim* tăng lên.
- **Trên phiếu nhập mua:** ô **Đã Phân Bổ Cho** ghi lại đã chia cho những đơn nào — dùng để đối
  chiếu về sau.
- **Sản xuất xong:** phần ghim vật tư **tự nhả ra** và chuyển thành ghim thành phẩm. Ví dụ cần 5
  chiếc, kho có 3 nên ghim 3 và ghim vật tư để làm 2 chiếc; sản xuất xong 2 chiếc thì thành ghim
  đủ 5 chiếc, phần vật tư biến mất khỏi bảng.

---

## 5. Thông báo lỗi thường gặp

| Thông báo | Nguyên nhân | Cách xử lý |
|---|---|---|
| *Dòng **N** — **mã hàng**: chỉ giữ chỗ được tối đa **X**, không được **Y**. Tồn khả dụng còn **Z** (đã trừ phần các đơn khác đang giữ), đơn này cần **W**.* | Gõ một số lớn hơn phần kho đang rảnh vào cột **Số Lượng Giữ Chỗ** — cột này nằm **trong lưới hàng hoá, ngay cạnh cột Số Lượng**, không phải ở đầu đơn | Sửa lại cột đó xuống tối đa **X** rồi Lưu. Muốn nhiều hơn thì phải đợi hàng về, hoặc xin đơn khác nhường |
| **Không đủ quyền phân bổ** — *Nút Phân Bổ chia hàng cho **tất cả** Đơn Bán đang ghim theo thứ tự cần gấp, nên chỉ người xem được toàn bộ đơn mới bấm được. Tài khoản của anh/chị đang xem được **a** trên **b** đơn đang ghim.* | Tài khoản bị giới hạn chỉ xem được một phần Đơn Bán Hàng | Nhờ quản trị bỏ giới hạn xem Đơn Bán Hàng cho tài khoản này, hoặc nhờ người khác bấm |
| **Chưa duyệt phiếu** — *Phiếu nhập mua chưa được duyệt nên hàng chưa vào kho — chưa phân bổ được.* | Bấm Phân Bổ trên phiếu còn nháp | Duyệt phiếu nhập mua trước, rồi bấm lại |

### Không phải lỗi — đọc cho biết

| Thông báo | Nghĩa |
|---|---|
| *Đơn chưa duyệt nên chưa giữ chỗ được vật tư…* | Đúng, duyệt đơn xong sẽ có số |
| *Không chia được gì thêm — hoặc các đơn đã ghim đủ, hoặc hàng vừa về đã có chủ.* | Không còn hàng rảnh để chia, không phải hỏng |

### 🔴 Không phải lỗi — nhưng PHẢI đọc trước khi bấm gửi

| Thông báo | Vì sao phải dừng lại đọc |
|---|---|
| *Toàn nhà máy đang có phiếu yêu cầu **ĐÃ DUYỆT** mà chưa thành đơn mua: …* | Đây là **tiền thật**. Hệ thống **không tự trừ** phần đang chờ đó, nên nếu bạn xin thêm mà không nhìn con số này thì nhà máy **mua thừa**. Đo ngày 08/09: `NVL 3` đang chờ **99**, `NVL 2` **70**, `NVL 1` **20** — trong đó một phiếu từ **13/08** giữ 60 `NVL 3` suốt một tháng. Thấy phần mình cần đã nằm trong đó thì **giục mua**, đừng xin thêm |

---

## 6. Câu hỏi thường gặp

**Hỏi:** Tôi tích **Ghim Tồn Khả Dụng** rồi bấm Lưu mà bảng **Ghim Vật Tư** trống trơn?
**Đáp:** Đơn đang ở trạng thái nháp. Duyệt đơn thì bảng mới có số.

**Hỏi:** Vì sao *Đã Ghim* ít hơn *Nhu Cầu*?
**Đáp:** Hệ thống chỉ giữ được phần kho **thật sự còn rảnh**, đã trừ phần các đơn khác giữ trước.
Phần chênh chính là phần cần đi mua.

**Hỏi:** Tôi bấm **Phân Bổ** hai lần thì có bị chia đôi không?
**Đáp:** Không. Lần thứ hai sẽ báo không chia được gì thêm.

**Hỏi:** Tôi bấm **Tạo Yêu Cầu Mặt Hàng** hai lần thì sao?
**Đáp:** **Sẽ ra hai phiếu cho cùng một phần thiếu** — hệ thống cố ý không tự trừ phiếu cũ. Trước
khi gửi, đọc kỹ hai câu nhắc: một câu cho biết **đơn này** đã xin bao nhiêu, một câu cho biết
**toàn nhà máy** đang có bao nhiêu phiếu đã duyệt mà chưa thành đơn mua. Nếu phần đó sắp về thì
giục mua thay vì xin thêm.

**Hỏi:** Ô **Giữ Nguyên** dùng để làm gì?
**Đáp:** Đánh dấu dòng do **người dùng tự đặt số**, để lần lưu sau hệ thống không ghi đè. Bấm
**Phân Bổ** thì vẫn chia lại bình thường.

**Hỏi:** Huỷ phiếu nhập mua rồi thì phần đã chia có tự trả lại không?
**Đáp:** Có, tự động. Nếu đơn nhận hàng đã mang đi sản xuất mất thì hệ thống cắt của đơn ít gấp
nhất và ghi rõ đã cắt của ai.

**Hỏi:** Hàng về rồi mà bấm Phân Bổ vẫn không chia được?
**Đáp:** Xem hộp thoại có báo *"Có mặt hàng nhập vào kho không được tính tồn"* không — hàng có thể
đang nằm ở kho lỗi hoặc kho trung chuyển. Hoặc đơn đang thiếu chưa bật **Ghim Tồn Khả Dụng**.
