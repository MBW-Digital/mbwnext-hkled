# Hướng dẫn cấu hình: Khai kho mặc định và tồn tối thiểu theo công ty

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Quản trị hệ thống, tư vấn triển khai
> **Cập nhật:** 2026-09-04
> **Mục đích:** Khai hàng loạt cho cả danh mục mà **không xoá mất dữ liệu đang có**.

---

## 1. 🔴 ĐỌC TRƯỚC: nhập Excel GHI ĐÈ CẢ DÒNG

Đây là mục quan trọng nhất của tài liệu này.

Chức năng **Nhập dữ liệu** của hệ thống, khi nạp vào một **bảng con** như *Mặc định cho mặt
hàng*, **thay thế toàn bộ dòng** — chứ không cập nhật từng ô. **Cột nào không có trong file
Excel sẽ bị xoá trắng.**

### Đo thật trên cổng 8012 ngày 03/09

Mặt hàng `Vỏ test A-100` đang có *Tài khoản doanh thu* **511**. Nạp một file Excel chỉ gồm
**2 cột** *Công ty* + *Kho mặc định*:

- Kho mặc định vào đúng ✅
- Ô **511 bị xoá sạch** ❌

Thử lại kèm cả cột **ID của dòng** — **vẫn mất**. Đây là cách hệ thống làm việc với bảng con,
không phải lỗi của phần khai báo này.

### ✅ Cách làm đúng

1. Vào **Nhập dữ liệu** (*Data Import*), chọn doctype **Mặt hàng**.
2. Bấm **Xuất** để tải file có sẵn **dữ liệu hiện tại và đủ mọi cột**.
3. Trên file đó, **chỉ sửa hai cột** *Kho mặc định* và *Tồn Kho Khả Dụng Tối Thiểu*.
4. Nạp ngược file đó lên.

Làm vậy thì cột nào không đụng tới vẫn còn nguyên, vì chúng vẫn có mặt trong file.

### ⚠ Vì sao hôm nay rủi ro nhỏ, và vì sao nó sẽ lớn

Đo 04/09: **6 / 62.055** dòng có cột khác được điền, và cả 6 chỉ có mỗi *Tài khoản doanh thu 511*.
Nên nếu nhập sai cách hôm nay thì mất ít.

**Nhưng sau khi khách khai xong tài khoản, nhà cung cấp mặc định… cho cả danh mục rồi mới
nhập Excel lần hai — thì đúng cái bẫy này xoá sạch công đó.** Vì vậy phải hướng dẫn khách
cách làm đúng **ngay từ lần đầu**, đừng đợi tới lúc mất.

---

## 2. Ba trường nghĩa gần nhau — khai nhầm là số sai mà không ai biết

| Trường | Nhìn thấy ở đâu | Chi tiết tới đâu | Ai đọc |
|---|---|---|---|
| **Tồn Kho Khả Dụng Tối Thiểu** ← *dùng cái này* | Mặt hàng → tab Kế toán → *Mặc định cho mặt hàng* | theo **công ty** | Tính nhu cầu vật tư theo kỳ |
| *Mức đặt hàng lại* | Mặt hàng → *Mức tồn kho tối thiểu theo kho* | theo **từng kho** | cơ chế tự sinh Yêu cầu mặt hàng của ERPNext |
| ~~*Tồn kho tối thiểu*~~ | — | một số cho cả mặt hàng | **đã gỡ 04/09** |

Anh Thắng chốt 03/09 15:46: **dùng ô theo công ty, gỡ ô kia đi**. Ô thứ ba đã được gỡ khỏi
hệ thống; nếu còn thấy nó ở đâu thì đó là tàn dư, báo đội kỹ thuật.

📌 **Ô *Mức đặt hàng lại* hiện có đúng một bản ghi** — *Thành phẩm 1 · Kho thành phẩm · mức 0*,
do anh Thắng tạo 21/07. Mức **0** đọc như *"đã khai, mức 0"* chứ không phải *"chưa khai"*, và
nó khiến luật tồn kho tối đa của app lõi **không bao giờ chạy**. Không liên quan tính năng này,
nhưng đừng tưởng đang có lớp bảo vệ đó.

---

## 3. Không dựng bảng mới — cố ý

Bảng *Mặc định cho mặt hàng* là **bảng có sẵn của ERPNext**. Tính năng này chỉ **thêm một cột**
vào đó. Ba lý do:

1. Các chức năng sẵn có của ERPNext (mua hàng, chuyển kho, sản xuất) **đã biết đọc** cột *Kho
   mặc định* của bảng này. Bảng riêng thì chỉ app mình đọc, phần còn lại của hệ thống vẫn mù.
2. Không đẻ ra **hai chỗ khai kho** để rồi lệch nhau mà không biết chỗ nào đúng.
3. Khách khai **một lần**.

Bảng đã có sẵn **62.055 dòng** — mỗi mặt hàng một dòng cho công ty HKLED. Chỉ là cột kho đang
trống gần hết: đo 04/09 mới **6/62.055** dòng có kho.

---

## 4. ⚠ Lưới chỉ còn chỗ cho ĐÚNG MỘT cột nữa

Lưới bảng con của Frappe có trần tổng độ rộng. Vượt trần thì cột phía sau **bị bỏ âm thầm** —
không lỗi, không cảnh báo, chỉ là mất khỏi màn hình.

Hiện tại: `1 + Công ty 2 + Kho mặc định 2 + Tồn Kho Khả Dụng Tối Thiểu 2 + Bảng giá 2 = **9/11**`

Nên **thêm được một cột rộng 2 nữa**; **cột thứ hai là cột bắt đầu biến mất**. Ai định thêm cột
vào bảng này thì đọc dòng này trước.

---

## 5. Ai đang đọc hai con số này

| Con số | Nơi tiêu thụ |
|---|---|
| **Kho mặc định** | Nút *Tạo Yêu Cầu Mặt Hàng* trên màn hình Kiểm Tra Tồn Kho (Phần IV) — chọn kho cho phiếu |
| **Tồn Kho Khả Dụng Tối Thiểu** | Tính nhu cầu vật tư cần mua theo kỳ (Phần V) |

Nghĩa là **Phần V phụ thuộc vào tính năng này**. Khách chưa khai thì Phần V coi như mức tối
thiểu bằng 0.

---

## 6. Cách tự kiểm sau khi nâng cấp

```bash
cd <bench> && bench --site <site> console
```

```python
frappe.db.get_value("Custom Field", "Item Default-custom_ton_kho_kha_dung_toi_thieu", "module")
# phải ra "MBWNext HKLed" — thiếu module thì trường không đi theo app khi deploy site mới

frappe.db.sql("select count(*) from `tabItem Default` where ifnull(default_warehouse,'')<>''")
# đếm độ phủ đã khai tới đâu
```

Bộ test case đầy đủ: `docs/testcases/khai-kho-mac-dinh-va-ton-toi-thieu-theo-cong-ty.md` — 22 ca.

---

## 7. Việc còn treo

| Việc | Ghi chú |
|---|---|
| **Chưa có đường khai hàng loạt sẵn** | Anh Thắng chốt 03/09 16:02: **nhập từ Excel**, khách tự làm. Không phải viết thêm code, nhưng **phải hướng dẫn kèm bẫy ở mục 1** |
| **Patch `them_ton_toi_thieu_vao_kho_mac_dinh` chưa chạy** trên `hkled.com` | Trường vẫn có nhờ fixtures nên hôm nay không ảnh hưởng. Patch sẽ chạy ở lần `bench migrate` tới; nó có chốt *nếu đã tồn tại thì thoát* nên vô hại |
