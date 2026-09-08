# Hướng dẫn cấu hình: Giữ chỗ vật tư và chia hàng khi hàng mua về

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED (`PM-FEAT-00036`)
> **Đối tượng:** Quản trị hệ thống, tư vấn triển khai
> **Cập nhật:** 2026-09-08
> **Mục đích:** Dựng đủ điều kiện để tính năng giữ chỗ và chia hàng chạy đúng trên site khách.

Phần thao tác hằng ngày xem
[phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve-van-hanh.md](phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve-van-hanh.md).

---

## Mục lục

1. [Cần dựng gì trước khi bật](#1-cần-dựng-gì-trước-khi-bật)
2. [Kho nào được tính là tồn dùng được](#2-kho-nào-được-tính-là-tồn-dùng-được)
3. [Phân quyền](#3-phân-quyền)
4. [Các trường được thêm vào](#4-các-trường-được-thêm-vào)
5. [Những luật nghiệp vụ đã chốt — đừng tự đổi](#5-những-luật-nghiệp-vụ-đã-chốt--đừng-tự-đổi)
6. [Kiểm tra sau khi cài](#6-kiểm-tra-sau-khi-cài)

---

## 1. Cần dựng gì trước khi bật

| Việc | Vì sao |
|---|---|
| **Định mức (BOM)** cho mọi mặt hàng *Sản xuất* / *Gia công* | Không có định mức thì hệ thống không bóc được xuống vật tư, bảng **Ghim Vật Tư** sẽ trống |
| **Phương pháp bổ sung** trên mặt hàng (*Mua hàng* / *Sản xuất* / *Gia công*) | Quyết định mặt hàng nào bóc tiếp xuống cấp dưới, mặt hàng nào dừng lại vì phải đi mua |
| **Ngày giao** trên Đơn Bán Hàng | Đây là căn cứ duy nhất để xếp thứ tự chia hàng. Đơn không có ngày giao bị xếp sau cùng |

⚠ Mặt hàng *Sản xuất* mà **thiếu định mức** thì hệ thống không im lặng bỏ qua — nó hiện cảnh báo
dạng thông báo nhanh khi lưu đơn. Đây là dữ liệu khách phải khai, không phải lỗi.

---

## 2. Kho nào được tính là tồn dùng được

Hệ thống **loại bỏ** mọi kho nằm dưới hai nhóm kho sau khi tính tồn khả dụng:

```
Nhóm kho lỗi
Nhóm kho trung chuyển
```

Kho nằm dưới hai nhóm này thì hàng **có thật trong kho nhưng không được coi là dùng được**, nên
không giữ chỗ được và không chia được.

Đo trên site HKLED ngày 08/09: **5 / 9** kho lá được tính tồn — tức **4 kho đang bị loại**. Cả hai
nhóm đều có thật trên site (`Nhóm kho lỗi - HKL`, `Nhóm kho trung chuyển - HKL`).

⚠ **Đây là nguyên nhân số một của câu hỏi "hàng về rồi mà sao không chia được".** Nếu khách nhập
hàng vào một kho mới, kiểm xem kho đó có vô tình nằm dưới hai nhóm trên không. Hộp thoại **Phân
Bổ** có cảnh báo riêng cho ca này — *"Có mặt hàng nhập vào kho không được tính tồn"*.

Tên hai nhóm kho **khớp theo tên nhóm**, nên đổi tên nhóm kho trên site là đổi hành vi. Muốn thêm
nhóm bị loại thì sửa hằng số `NHOM_KHO_LOAI` trong `api/kiem_tra_ton_kho.py`, không có màn hình
cấu hình cho việc này.

---

## 3. Phân quyền

### Ai bấm được nút Phân Bổ

**Chốt của anh Thắng 05/09 11:09: thủ kho và nhân viên mua hàng được bấm.** Không thắt thêm.

Nhưng có **một điều kiện kỹ thuật bắt buộc**: tài khoản phải **xem được toàn bộ Đơn Bán Hàng đang
giữ chỗ**. Lý do: nút này chia hàng cho *tất cả* đơn theo thứ tự cần gấp — người chỉ thấy một
phần đơn mà bấm thì sẽ chia sai thứ tự mà không ai biết.

Hệ thống tự kiểm và chặn với thông báo **Không đủ quyền phân bổ**, có nêu rõ *xem được **a** trên
**b** đơn*.

➜ Nếu khách dùng **User Permission** để giới hạn Đơn Bán Hàng theo nhân viên kinh doanh, thì
những tài khoản đó **sẽ không bấm được nút này**. Đó là chủ ý, không phải lỗi. Cách xử lý: bỏ
giới hạn cho đúng tài khoản thủ kho và mua hàng.

### Hai tài khoản kiểm thử có sẵn trên site

| Tài khoản | Giới hạn | Dùng để kiểm |
|---|---|---|
| `test.thukho@hkled.test` | — | thủ kho bấm được nút |
| `test.mua.gioihan@hkled.test` | User Permission trên **Khách hàng** ➜ chỉ thấy đơn của khách đó | phải bị chặn |

⚠ Giới hạn **không cần đặt thẳng lên Đơn Bán Hàng** mới chặn được. Tài khoản trên chỉ bị giới hạn
ở **Khách hàng**, nhưng vì Đơn Bán Hàng có trỏ tới khách nên nó vẫn chỉ thấy một phần đơn — và
vẫn bị nút Phân Bổ chặn. Rà quyền thì phải rà cả các giới hạn gián tiếp kiểu này.

---

## 4. Các trường được thêm vào

Tất cả đều là **Custom Field**, đi theo app qua `fixtures/custom_field.json`, module
`MBWNext HKLed`.

| Chứng từ | Nhãn hiển thị | Kiểu | Ghi chú |
|---|---|---|---|
| Đơn Bán Hàng | **Ghim Tồn Khả Dụng** | Check | Mở khoá sau khi duyệt |
| Đơn Bán Hàng | **Ghim Vật Tư** | Bảng | Mở khoá sau khi duyệt |
| Dòng hàng Đơn Bán | **Số Lượng Giữ Chỗ** | Số | Mở khoá sau khi duyệt |
| Phiếu Nhập Mua | **Đã Phân Bổ Cho** | Văn bản ngắn | Nhật ký đã chia cho đơn nào — dùng để thu hồi khi huỷ phiếu |

⚠ Ba trường đầu **cố ý mở khoá sau khi duyệt** (chốt của anh Thắng 04/09 15:59). Nghĩa là ràng
buộc phải kiểm ở **cả hai** đường lưu — lúc duyệt và lúc sửa sau duyệt. Đừng gỡ một trong hai.

⚠ Bảng con **Ghim Vật Tư** có trường số lượng đặt tên riêng, **không** trùng tên trường của
ERPNext lõi. Đây không phải chuyện thẩm mỹ: đặt trùng tên sẽ kích nhầm phép tính tổng chứng từ
của lõi và làm **không lưu được đơn**, với câu lỗi nói về một ô hoàn toàn không liên quan. Đừng
đổi tên trường ở bảng này.

---

## 5. Những luật nghiệp vụ đã chốt — đừng tự đổi

| Luật | Chốt |
|---|---|
| Chỉ giữ chỗ trong phần tồn **thật sự rảnh**, đã trừ phần đơn khác giữ | 04/09 10:48 |
| Thứ tự chia: **ngày giao sớm trước**; cùng ngày thì **đơn tạo trước** | 04/09 15:59 và 16:21 |
| **Chỉ chia** cho đơn đang bật *Ghim Tồn Khả Dụng* | 04/09 15:59 |
| **Không ưu tiên** khách hàng hay loại đơn nào | 04/09 15:59 |
| Người dùng **sửa tay được** số ghim, để nhường nhau | 05/09 09:20 |
| Bấm **Phân Bổ** thì chia lại bình thường, kể cả dòng đã sửa tay | 05/09 09:39 |
| Sản xuất xong thì ghim vật tư **nhả ra**, chuyển thành ghim thành phẩm | 04/09 16:21 |
| Thủ kho và mua hàng **được** bấm Phân Bổ | 05/09 11:09 |
| Nút **Tạo Yêu Cầu Mặt Hàng** lấy thẳng cột *Thiếu*, **không** trừ phiếu đã xin trước | 03/09 16:51 |

⚠ Luật cuối có hệ quả anh Thắng đã cân nhắc và vẫn chọn: **bấm nút hai lần trên cùng một đơn ra
hai phiếu cho cùng phần thiếu**. Hệ thống bù lại bằng hai câu cảnh báo — một câu cho phần *đơn
này* đã xin, một câu cho phần *toàn nhà máy* đang chờ. Đừng gỡ hai câu đó đi.

---

## 6. Kiểm tra sau khi cài

Chạy trên `bench console` của site:

```python
from mbwnext_hkled.api.ghim_vat_tu import kiem_bat_bien
loi = kiem_bat_bien()
print("SẠCH" if not loi else loi)
```

Hàm này quét toàn bộ sổ giữ chỗ và khẳng định các điều kiện phải luôn đúng — trong đó có: tổng
phần đang giữ của mọi đơn **không vượt tồn thật**, và không dòng nào giữ nhiều hơn nhu cầu của
chính nó.

**Chạy lại hàm này sau mỗi lần**: đổi cây kho, đổi định mức, nhập tồn kho hàng loạt, hoặc huỷ
hàng loạt chứng từ. Danh sách rỗng nghĩa là sổ sạch.

### Kiểm nhanh bằng mắt

1. Mở một Đơn Bán Hàng đã duyệt có bật **Ghim Tồn Khả Dụng** → bảng **Ghim Vật Tư** phải có dòng.
2. Mở một Phiếu Nhập Mua **đã duyệt** → phải thấy nút **Phân Bổ**.
3. Mở một Phiếu Nhập Mua **còn nháp** → **không** được có nút đó.
