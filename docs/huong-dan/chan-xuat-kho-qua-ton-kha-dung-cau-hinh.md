# Hướng dẫn cấu hình: Chặn xuất kho quá tồn khả dụng

> **Phạm vi:** App `mbwnext_hkled` — dành riêng khách HKLED
> **Đối tượng:** Quản trị hệ thống, tư vấn triển khai
> **Cập nhật:** 2026-09-04
> **Mục đích:** Biết điều gì quyết định con số "tồn khả dụng", và thao tác nào sẽ
> vô tình làm đổi nó.

---

## 1. Không có công tắc bật/tắt

Tính năng chạy **tự động** trên tám chứng từ rút tồn, ngay khi app được cài. Không
có ô cấu hình nào, không có Setting nào.

Muốn tắt thì phải gỡ khai báo trong `hooks.py` và deploy lại — đó là việc của đội
kỹ thuật, không phải việc cấu hình.

---

## 2. Điều DUY NHẤT bạn cấu hình được: tập kho hợp lệ

Con số *tồn khả dụng* chỉ cộng hàng nằm trong **tập kho hợp lệ**. Hàng ngoài tập đó
không được tính là hàng dùng được, nên rút đi cũng không bị chặn.

Luật hiện tại — anh Thắng chốt 03/09 15:33: **tất cả kho, trừ hai nhóm**.

**Đang được tính (5 kho):**

| Kho |
|---|
| Kho thành phẩm - HKL |
| Kho bán thành phẩm - HKL |
| Kho nguyên vật liệu - HKL |
| **Kho ký gửi - HKL** |
| **Kho khuyến mãi/hàng mẫu - HKL** |

**Bị loại trừ:** nhóm **Kho trung chuyển** và nhóm **Kho lỗi** — hàng đang đi đường
và hàng hỏng không phải hàng bán được.

---

## 3. ⚠ Thao tác dễ làm hỏng số liệu mà không ai biết

### Đừng "dọn" Kho ký gửi và Kho khuyến mãi/hàng mẫu vào nhóm loại trừ

Nhìn cây kho thì hai kho này trông như bị bỏ quên ngoài nhóm, rất dễ tưởng là thiếu
sót rồi kéo vào **Nhóm kho trung chuyển** cho gọn.

**Đừng.** Anh Thắng chốt 03/09 15:59 rằng hai kho đó **vẫn tính là hàng dùng được**.
Kéo chúng vào nhóm loại trừ là **tồn khả dụng tụt xuống trên toàn hệ thống**: đơn
đang giữ chỗ hợp lệ bỗng thành vượt tồn, phiếu xuất bị chặn oan, và Bảng 2 của tính
năng Kiểm tra tồn kho báo thiếu hàng không có thật.

Không có thông báo nào khi việc này xảy ra. Số chỉ đơn giản là đổi.

### Thêm kho mới

Kho mới **tự động** được tính, trừ khi bạn đặt nó dưới hai nhóm loại trừ. Không phải
khai báo gì thêm — nhưng hãy cân nhắc đúng nhóm ngay lúc tạo.

---

## 4. Quan hệ với cơ chế giữ chỗ sẵn có của ERPNext

ERPNext có sẵn *Stock Reservation*. HKLED **không dùng** nó — anh Thắng chốt 25/08
sau khi thử nghiệm, vì nó tính theo **một kho** và **không giữ được nguyên vật liệu**
bóc từ định mức, mà HKLED cần cả hai.

⚠ **Đừng bật `enable_stock_reservation`.** Bật lên là hai sổ giữ chỗ chạy song song,
số của cả hai đều nhiễu, và rất khó lần ra vì không bên nào báo lỗi. Việc này đã xảy
ra một lần trong đợt thử nghiệm 25/08.

---

## 5. Cách tự kiểm tính năng còn chạy đúng

Sau mỗi lần nâng cấp hoặc `bench migrate`:

```bash
cd <bench> && bench --site <site> console
```

```python
from mbwnext_hkled.api.kiem_tra_ton_kho import _kho_hop_le
print(len(_kho_hop_le()))      # phải ra 5 trên HKLED
frappe.get_hooks("doc_events")["Delivery Note"]["before_submit"]
# phải thấy chan_xuat_qua_ton_kha_dung
```

Bộ test case đầy đủ: `docs/testcases/chan-xuat-kho-qua-ton-kha-dung.md` — 39 ca,
đã chạy hết ngày 04/09.

---

## 6. Việc còn treo, cần biết trước khi triển khai thật

| Việc | Ảnh hưởng |
|---|---|
| **Bốn chứng từ không miễn trừ được** — Hóa Đơn Mua Hàng · Đối soát tồn kho · Subcontracting Receipt · Hạch toán tài sản | Chúng không có đường liên kết nào về Đơn hàng bán, nên nếu chứng từ đang thực hiện chính đơn đã ghim thì **vẫn bị chặn oan**. Ba cái hiếm dùng; riêng **Đối soát tồn kho** (kiểm kê) thì đáng hỏi lại khách |
| **`Subcontracting Receipt` chưa có bản dịch tiếng Việt** | Khách chạy giao diện tiếng Việt vẫn thấy tên tiếng Anh. Cần bổ sung vào `locale/vi.po` |
| **Luật tồn kho tối đa của app lõi hiện không hoạt động** | Bản ghi *Item Reorder* duy nhất trên site để `custom_max_stock_qty = 0`, mà mã lõi lọc `if mq > 0`. Không liên quan tính năng này, nhưng đừng tưởng đang có lớp bảo vệ đó |
