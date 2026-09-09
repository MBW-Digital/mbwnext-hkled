# Hướng dẫn cấu hình: Cập nhật chi phí BOM tự động

> **Phạm vi:** Chức năng sẵn có của ERPNext (không phải phần bên mình viết thêm)
> **Đối tượng:** Quản trị hệ thống, tư vấn triển khai
> **Cập nhật:** 2026-09-09 · đo trên cổng 8012 (`hkled.com`)
> **Bối cảnh:** PM-TASK-00194 — anh Thắng tích ô này lúc 14:43 ngày 09/09 và không
> thấy chi phí BOM tự đổi, vẫn phải bấm **Cập nhật chi phí** trong từng BOM.

---

## 1. 🔴 ĐỌC TRƯỚC: ô này chạy MỖI NGÀY MỘT LẦN, không chạy ngay

Ô **Cài đặt sản xuất → BOM → Update BOM Cost Automatically** không phải là "tự động
cập nhật khi giá thay đổi". Nó chỉ **bật một tác vụ chạy nền lúc 00:00 hằng đêm**.

Tích xong thì **trong ngày hôm đó không có gì xảy ra cả** — đó chính xác là chuyện
anh Thắng gặp:

| Mốc | Giờ đo được |
|---|---|
| Tác vụ đêm chạy lần gần nhất | **09/09 lúc 00:00:27** |
| Anh Thắng tích ô | **09/09 lúc 14:43:59** |
| Lần chạy kế tiếp | **10/09 lúc ~00:00** |

Tích **sau** lần chạy của ngày hôm đó **14 giờ 44 phút**. Không có gì hỏng — chỉ là
chưa tới giờ.

### Vì sao không có thông báo gì

Hệ thống không báo *"đã ghi nhận, sẽ chạy đêm nay"*. Người dùng tích xong, mở BOM ra
xem, thấy y nguyên, và kết luận là chức năng hỏng. **Nên khi bàn giao phải nói trước
câu này**, đừng để khách tự phát hiện.

---

## 2. Hai đường cập nhật chi phí — khác nhau chỗ nào

| | Nút **Cập nhật chi phí** trong BOM | Ô **Update BOM Cost Automatically** |
|---|---|---|
| Chạy lúc nào | Ngay khi bấm | 00:00 hằng đêm, mỗi ngày một lần |
| Phạm vi | Đúng **một** BOM đang mở | **Tất cả** BOM đã duyệt + đang hoạt động |
| BOM còn **nháp** | ✅ Có làm | ❌ **Bỏ qua** — xem mục 4 |
| Lấy giá ở đâu | Theo ô *Rate Of Materials Based On* của chính BOM đó | Y hệt — cùng một phép tính |

**Cả hai gọi cùng một hàm tính** (`calculate_cost`). Bật ô tự động **không** làm chi phí
chính xác hơn, chỉ đỡ phải bấm tay từng BOM.

➜ **Vẫn cần bấm tay khi nào:** khi vừa nhập hàng / vừa sửa giá và muốn thấy chi phí
mới **ngay trong hôm nay**. Ô tự động không thay được việc này.

---

## 3. Ô này KHÔNG chọn nguồn giá — mỗi BOM tự chọn

Dòng mô tả dưới ô ghi *"based on the latest Valuation Rate / Price List Rate / Last
Purchase Rate"* rất dễ hiểu nhầm là ô này chọn một trong ba.

Không phải. Nguồn giá nằm ở **từng BOM**, tại *Cost Configuration → Rate Of Materials
Based On*. Ô cài đặt chỉ quyết định **có chạy lại hằng đêm hay không**.

Đo ngày 09/09 trên cổng 8012: **13/13 BOM** đang để **Valuation Rate** (giá vốn).

⚠ **Hệ quả:** giá vốn chỉ có khi vật tư **đã từng nhập kho**. Mặt hàng chưa nhập lần
nào thì giá vốn = 0, và tác vụ đêm chạy xong chi phí **vẫn là 0**. Bật ô này **không
sinh ra giá** cho vật tư chưa có lịch sử nhập. Muốn ra số thì hoặc nhập kho, hoặc đổi
BOM sang *Price List* rồi khai bảng giá.

---

## 4. ⚠ BOM còn nháp: nút bấm được, tác vụ đêm bỏ qua

Đây là chỗ dễ mất công nhất.

- **Nút *Cập nhật chi phí* hiện trên cả BOM nháp** — đã mở `BOM-DP01S300-6P3HN-BN-001`
  (trạng thái *Draft*) trên cổng 8012 ngày 09/09 và nút vẫn nằm đó, bấm được.
- **Tác vụ đêm chỉ lấy BOM `đã duyệt` + `đang hoạt động`.** BOM nháp không bao giờ
  được nó chạm tới.

Không có cảnh báo nào cho biết điều đó. BOM nháp cứ nằm im với chi phí cũ, trông y hệt
một BOM "đã cập nhật rồi mà không có gì đổi".

Đo 09/09: **2 / 13 BOM đang ở trạng thái nháp** (`BOM-DP01S300-6P3HN-BN-001`,
`BOM-DP01S200-3B3DN-AD-001`) ➜ hai BOM này nằm ngoài vùng phủ của ô tự động.

➜ **Quy tắc bàn giao:** muốn BOM được cập nhật hằng đêm thì phải **duyệt** nó.

---

## 5. Đêm nay sẽ đổi những gì (chạy thử 09/09, đã hoàn tác)

Đã chạy đúng chuỗi hàm của tác vụ đêm trên dữ liệu thật rồi `rollback` — kiểm lại sau
khi hoàn tác: **0 BOM còn lệch**, dữ liệu nguyên vẹn.

Kết quả: **5 / 13 BOM sẽ đổi chi phí**.

| BOM | Trước | Sau |
|---|---|---|
| `BOM-Bán thành phẩm 1-001` | 0 | 90.000 |
| `BOM-Bán thành phẩm 2-001` | 0 | 120.000 |
| `BOM-Test Gia Công-001` | 20.000 | 110.000 |
| `BOM-Thành phẩm 1-001` | 0 | 210.000 |
| `BOM-Thành phẩm 1-002` | 50.000 | 140.000 |

8 BOM còn lại giữ nguyên: 2 vì đang nháp, 6 vì vật tư chưa có giá vốn (mục 3).

Tác vụ chạy **theo tầng từ dưới lên**: bán thành phẩm trước, thành phẩm sau — nên
`Thành phẩm 1-001` đổi là **hệ quả** của `Bán thành phẩm 1` + `2` vừa đổi ở tầng dưới,
chứ không phải tự nó.

---

## 6. ⚠ Chỗ có thể làm tác vụ đêm im lặng ngừng 10 ngày

Mỗi đêm, trước khi chạy, hệ thống kiểm tra xem có bản ghi *BOM Update Log* nào đang
**Queued / In Progress** không. Nếu có **và bản ghi đó chưa quá 10 ngày** thì nó **bỏ
qua đêm đó** — không log, không báo lỗi.

Nghĩa là **một lần chạy bị kẹt sẽ tắt cập nhật tự động trong 10 ngày liền**, và triệu
chứng nhìn y hệt lúc này: tích ô rồi mà chi phí không đổi.

**Cách kiểm khi khách báo "bật rồi mà không chạy":**

1. Vào danh sách **BOM Update Log**, lọc *Update Type = Update Cost*.
2. Thấy dòng **Queued** hoặc **In Progress** để lâu ➜ đó là thủ phạm.
3. Đối chiếu **Scheduled Job Type** `bom_update_tool.auto_update_latest_price_in_all_boms`
   — xem *Last Execution* có nhảy sang ngày mới không, và ô *Stopped* có bị tích không.

Đo 09/09: **BOM Update Log rỗng (0 bản ghi)**, tác vụ **không bị dừng**, chạy đều mỗi
sáng 00:00 suốt 04→09/09. Nên hiện tại không dính chỗ kẹt này.

---

## 7. Tóm tắt cho khách

1. Tích ô là **đúng**, không cần sửa gì thêm.
2. **Sáng mai mới thấy kết quả** — nó chạy 00:00 hằng đêm, không chạy ngay lúc tích.
3. **Vẫn giữ thói quen bấm nút** khi cần thấy chi phí mới ngay trong ngày.
4. **BOM còn nháp thì phải duyệt** mới được cập nhật tự động.
5. Vật tư **chưa từng nhập kho** thì chi phí vẫn ra 0 — đây không phải lỗi của ô này.
