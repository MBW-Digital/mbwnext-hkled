# Khai kho mặc định và tồn tối thiểu theo công ty

> **PM-FEAT-00037 · Phần IV · Khai kho mặc định và tồn tối thiểu theo công ty**
> Tên trên PM khác tên file này — nối hai bên bằng MÃ, không bằng tên. Xem `CLAUDE.md`.

**Khách hàng:** HKLED
**Người cung cấp thông tin:** anh Thắng (MBW) — viết đầu bài trên PM 03/09/2026 11:10
**Ngày dựng file:** 2026-09-03 · **PM Project:** PM-PRJ-00003 · hạn 17/09/2026

> Mọi con số **đo trên cổng 8012 ngày 03/09/2026**.

---

## 1. Đầu bài gốc (nguyên văn anh Thắng)

> Đây là 1 bảng bổ sung ngay trực tiếp trong mặt hàng, bảng này sẽ ghi nhận 3 thông tin chính:
> Công ty, Kho mặc định, Tồn kho khả dụng tối thiểu. Ví dụ người dùng thiết lập dòng thứ nhất:
> công ty A, kho mặc định: Kho nguyên vật liệu - A, tồn kho khả dụng tối thiểu 500. Có nghĩa là
> kho Nguyên vật liệu - A là kho chứa mặc định cho mặt hàng này nếu thuộc các chứng từ của công ty
> A. Và tồn kho khả dụng tối thiểu của mặt hàng này ở công ty A là 500. Bảng này sau này sẽ áp
> dụng cho 1 số phần liên quan đến việc chọn kho khi tạo yêu cầu mặt hàng, tính năng ghi nhận hàng
> lỗi (sắp tới anh bổ sung),...

## 2. Việc phải làm rút xuống còn ĐÚNG MỘT CỘT

Lõi ERPNext **đã có sẵn đúng cái bảng này**: `Item.item_defaults` (bảng con `Item Default`), tên
hiển thị **Mặc định của mặt hàng**, nằm trong tab *Tồn kho* của mỗi mặt hàng.

| Anh Thắng cần | Lõi đã có? |
|---|---|
| Công ty | ✅ `company` |
| Kho mặc định | ✅ `default_warehouse` |
| Tồn kho khả dụng tối thiểu | ❌ **phải thêm** |

Và bảng **không rỗng**: đo được **62.055 dòng đã tồn tại**, mỗi mặt hàng đúng một dòng cho công ty
HKLED (site hiện chỉ có 1 công ty). Chỉ là **`default_warehouse` đang trống 62.055/62.055**.

**Ba lý do không dựng bảng riêng** — không phải để tiết kiệm công:

1. Khai vào bảng lõi thì **các chức năng sẵn có của ERPNext cũng đọc theo**: mua hàng, chuyển kho,
   sản xuất đều đã biết `default_warehouse`. Bảng riêng thì chỉ app mình đọc, phần còn lại của hệ
   thống vẫn mù.
2. Không đẻ ra **hai chỗ khai kho** để rồi lệch nhau mà không ai biết chỗ nào đúng.
3. Khách khai **một lần**.

## 3. Đã làm

`patches/them_ton_toi_thieu_vao_kho_mac_dinh.py` — thêm một trường vào `Item Default`:

	Tồn Kho Khả Dụng Tối Thiểu   (Float, không âm)
	  neo sau Kho mặc định — hai cột là một cặp, khai cùng lúc cho cùng công ty
	  hiện thẳng trên lưới (in_list_view), rộng 2 đơn vị

**Hiện thẳng trên lưới** là bắt buộc chứ không phải cho đẹp: bảng này khai bằng cách gõ vào từng
dòng, bắt mở từng dòng ra mới thấy ô thì khai 62.055 mặt hàng là không tưởng.

⚠ Lưới Frappe có **trần tổng độ rộng cột** (`grid.js::setup_visible_columns`, tổng > 11 thì cột sau
bị bỏ **âm thầm**) — đúng cái đã vấp ở cột *Số Lượng Giữ Chỗ* sáng 03/09. Bảng này đang hiện 3 cột
(*Công ty · Kho mặc định · Bảng giá*) và **chưa có bố cục riêng của người dùng** (`__UserSettings`
trống cho Mặt hàng), nên còn chỗ.

**Phần ĐỌC kho mặc định thì đã có từ trước:** `api/kiem_tra_ton_kho.py::_kho_mac_dinh()` đọc bảng
này để chọn kho khi lập Yêu Cầu Mặt Hàng — anh Thắng chốt *cách A* ngày 03/09 11:12. Nên tính năng
này **không phải viết lại phần đọc**, chỉ lo phần khai.

## 4. ⚠ BA TRƯỜNG NGHĨA GẦN NHAU — đừng khai nhầm chỗ

| Trường | Chi tiết tới đâu | Ai dùng |
|---|---|---|
| **`Item Default.custom_ton_kho_kha_dung_toi_thieu`** — *Tồn Kho Khả Dụng Tối Thiểu* | theo **công ty** | PM-FEAT-00037 |
| `Item Reorder.warehouse_reorder_level` — *Mức đặt hàng lại* (lõi) | theo **từng kho** | cơ chế tự sinh Yêu cầu mặt hàng của lõi |
| `Item.custom_ton_kho_toi_thieu` — *Tồn kho tối thiểu* | **một số cho cả mặt hàng** | PM-FEAT-00030 (Phần V) |

⛔ **Trường thứ ba giờ là thừa.** Nó ra đời cho Phần V (commit `e9e03b1`, phiên `cozy-dev-0c`) khi
chưa ai nói tới "theo công ty". Chốt của anh Thắng 03/09 11:10 làm nó cùng nghĩa với trường mới
nhưng thô hơn một bậc — và hai ô cùng tên gần giống nhau nằm trên cùng màn hình Mặt hàng thì khách
**sẽ** khai nhầm.

Đo 03/09: **0 / 62.055 mặt hàng có giá trị** ở trường đó → gỡ đi **không mất dữ liệu nào**.

**Patch này KHÔNG tự gỡ.** Trường thuộc commit của phiên khác và đang chờ Tuấn quyết (nó cũng chính
là cột DDL lỡ nằm lại trên 8012 lúc 10:28). Ghi ra đây để người gỡ có sẵn căn cứ.

## 5. Còn thiếu — nói rõ để không ai tưởng đã xong

**a) Chưa kiểm bằng mắt trên giao diện.** `bench clear-cache` làm phiên trình duyệt đăng xuất giữa
chừng nên chưa mở được màn hình Mặt hàng để nhìn cột mới. Cột lưới là **đúng chỗ đã hỏng một lần
hôm nay** — chưa nhìn thì chưa được coi là xong.

**b) Chưa có đường khai hàng loạt.** Bảng đúng rồi nhưng **0/62.055 dòng có kho**, và khai tay
62.055 mặt hàng là không làm nổi. Anh Thắng chưa nói khai bằng cách nào. Ba đường:

- **Nhập từ Excel** (Data Import của lõi) — khách tự làm được, không cần code, nhưng phải hướng dẫn.
- **Điền theo nhóm hàng** — vd. mọi mặt hàng thuộc nhóm *Ốc vít* → *Kho nguyên vật liệu*. Rẻ và
  khớp cách khách nghĩ, nhưng cần khách chốt bảng ánh xạ nhóm → kho.
- **Khai tay** — chỉ khả thi nếu khách chỉ cần vài trăm mặt hàng quan trọng.

**c) Chưa ai dùng cột tồn tối thiểu.** Đầu bài của anh Thắng nói *"sau này sẽ áp dụng cho..."* — nên
tính năng này chỉ dựng **chỗ khai**. Bên tiêu thụ là Phần V và tính năng ghi nhận hàng lỗi (chưa có).

**d) Chưa nạp fixtures.** Phải chạy `bench --site hkled.com export-fixtures --app mbwnext_hkled` để
trường sống trên site mới. Chưa chạy vì còn chờ (a).

## 6. Liên quan

- `kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md` (PM-FEAT-00023) — nơi `_kho_mac_dinh()` đọc
  bảng này; mục *"Kho trên phiếu mua — anh Thắng chốt CÁCH A"*.
- `phan-v-tinh-toan-nhu-cau-vat-tu-can-mua-theo-ky.md` (PM-FEAT-00030) — chủ của trường sắp bị gỡ.
