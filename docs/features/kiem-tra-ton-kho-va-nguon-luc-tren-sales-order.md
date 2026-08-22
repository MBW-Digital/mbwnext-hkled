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

⏳ **Chưa viết.** Theo quy trình, spec viết nối tiếp phía dưới file này **sau khi mockup
được duyệt** (giai đoạn 4). Hiện đang ở giai đoạn 2 — mockup.

Chốt được **R1** là viết được spec.
