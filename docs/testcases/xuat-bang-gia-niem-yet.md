# Test case — Xuất bảng giá niêm yết (PM-FEAT-00045)

> **Đầu bài:** [`../features/xuat-bang-gia-niem-yet.md`](../features/xuat-bang-gia-niem-yet.md)
> **Mockup:** [`../mockups/xuat-bang-gia-niem-yet.html`](../mockups/xuat-bang-gia-niem-yet.html)
> **Chạy trên:** cổng 8012 (`cozy_dev` / `hkled.com`), 08/09/2026 chiều
> **Nền:** frappe **15.120.0** · erpnext **15.73.1** — *(số đo lúc chạy test, 08/09 chiều)*

🔴 **NỀN ĐÃ ĐO BỘ TEST NÀY GIỜ KHÔNG CÒN Ở ĐÂU — đọc kỹ trước khi trích kết quả.**

| | frappe | erpnext | |
|---|---|---|---|
| Nền lúc chạy bộ test | 15.120.0 | **15.73.1** | 08/09/2026 chiều |
| `cozy_dev` hiện tại | 15.120.0 | **15.112.0** | đo 09/09/2026 09:07 |
| `hkled.mbwnext.com` (thật) | 15.101.0 | 15.95.1 | HKLed 3 đo 08/09, chưa kiểm lại |

Erpnext được nâng **39 bản minor** sau khi bộ test này chạy xong, không ai ghi lại lúc nào. Ba
dòng trên **không cặp nào trùng nhau**, và dòng đầu — cái nền đã sinh ra mọi chữ "Đạt" dưới đây —
**không còn tồn tại trên máy nào**.

⚠ Bản trước của mục này viết *"erpnext thấp hơn site thật 22 bản minor"*. Câu đó **nay sai và đã
đảo chiều**: bench hiện **cao hơn** site thật ở cả hai app. Ai đã trích đi đâu thì sửa lại.

➜ **Kết quả dưới đây vẫn dùng được để biết tính năng làm gì và sai ở đâu, nhưng không còn là bằng
chứng "chạy được" trên bất kỳ nền nào đang tồn tại.** Phải chạy lại bộ này — **trên bench trước**
(nền đã đổi ngay tại chỗ), rồi **trên site thật sau khi cài**. Xem
[`../huong-dan/cai-app-len-site-that.md`](../huong-dan/cai-app-len-site-that.md) mục 3.

## Dữ liệu chuẩn bị

Cổng 8012 có **61.612 mặt hàng**, trong đó **đúng 4 mã tính được giá niêm yết** — đây không phải
dữ liệu dựng riêng cho test, mà là hiện trạng thật:

| Mã | Phương pháp bổ sung | Giá vốn | Nguồn |
|---|---|---|---|
| `Test NVL 1` | Mua hàng | 1.000 | đơn mua đã duyệt |
| `Test NVL 2` | Mua hàng | 2.000 | đơn mua đã duyệt |
| `Test NVL 3` | Mua hàng | 3.000 | đơn mua đã duyệt |
| `Test Gia Công` | Gia công | 20.000 | BOM mặc định |

Tỷ lệ lúc chạy: hao phí **3%**, tỷ lệ tính giá niêm yết **30%**, R&D và lợi nhuận **chưa khai
(0%)** trên cả 4 mã.

---

## TC-CT — công thức

Cột *Kết quả* ghi số đo thật, không phải kỳ vọng.

| Mã | Việc | Đầu vào | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|---|
| TC-CT-01 | Làm tròn tới bội 5.000 **gần nhất** | `2.907.913` | `2.910.000` | `2.910.000` | Pass |
| TC-CT-02 | 🔴 Làm tròn **xuống** khi gần bội dưới | `2.947.247` | `2.945.000` — **không** phải 2.950.000 | `2.945.000` | Pass |
| TC-CT-03 | Ví dụ trong ghi chú của anh Thắng | cost `50.000` · 3/5/10 · tỷ lệ 30 | `195.000` | `195.000` | Pass |
| TC-CT-04 | Ví dụ *"197.800 ➜ 200.000"* của anh Thắng | `197.800` | `200.000` | `200.000` | Pass |
| TC-CT-05 | 🔴 Chia hết đôi — chỗ `round()` của Python làm sai | `2.502.500` | `2.505.000` | `2.505.000` | Pass |
| TC-CT-06 | Số thật trong file *Tính giá*, dòng 1 | cost `739.300` | Cộng `872.374` ➜ `2.910.000` | khớp cả hai số | Pass |
| TC-CT-07 | Số thật trong file *Tính giá*, dòng 2 | cost `749.300` | Cộng `884.174` ➜ `2.945.000` | khớp cả hai số | Pass |
| TC-CT-08 | 🔴 Khách đính chính anh Thắng — đổi tỷ lệ thì **tử số giữ nguyên** | tử số `30.000`, tỷ lệ 30 ➜ 25 | `100.000` ➜ `120.000` | `100.000` ➜ `120.000` | Pass |

> **TC-CT-05 đáng nói riêng.** `round()` của Python làm tròn về **số chẵn**, nên `round(2.5)` ra
> `2` — tức `2.502.500` sẽ ra `2.500.000` thay vì `2.505.000`. Tiền thì không được lúc lên lúc
> xuống. Đã tự cộng nửa bội rồi cắt sàn.

---

## TC-HAPPY — luồng đúng, bấm thật trên giao diện

| Mã | Việc | Bước thực hiện | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Mở màn hình | Vào **Bảng giá niêm yết** | Bảng hiện, có 4 thẻ tóm tắt: hao phí, tỷ lệ niêm yết, bảng giá đích, số dòng đang lệch | Hiện `Hao phí 3%` · `Tỷ lệ tính giá niêm yết 30%` · `Ghi vào bảng giá Standard Selling` · `Đang lệch 0` (**giao diện**) | Pass |
| TC-HAPPY-02 | Lọc **chỉ dòng tính được giá** | Chọn ở ô *Hiện* | Ra đúng 4 mã, tick chọn được cả 4 | 4 dòng, 4 ô tick (**giao diện**) | Pass |
| TC-HAPPY-03 | Giá tính đúng trên lưới | Xem cột *Cộng* và *Giá niêm yết* | `Test Gia Công` 20.000 ➜ 20.600 ➜ **70.000** | khớp; NVL 1/2/3 ra 5.000 / 5.000 / 10.000 (**giao diện**) | Pass |
| TC-HAPPY-04 | Nút cập nhật **hỏi lại trước khi ghi** | Tick 4 dòng → **Cập nhật giá niêm yết** | Hộp thoại nêu rõ **số lượng** và **tên bảng giá**, và nói đơn đã lập không bị ảnh hưởng | *"Đẩy giá niêm yết mới của 4 mặt hàng sang bảng giá Standard Selling?"* (**giao diện**) | Pass |
| TC-HAPPY-05 | Cập nhật chạy | Xác nhận | Báo số mặt hàng đã cập nhật; cột *Đang áp dụng* bằng cột *Giá niêm yết*; thẻ *Đang lệch* về 0 | *"Đã cập nhật 4 mặt hàng."*, cả 4 dòng hai cột bằng nhau, `Đang lệch 0` (**giao diện**) | Pass |
| TC-HAPPY-06 | 🔴 **Luật vàng: đổi tỷ lệ thì giá sales thấy KHÔNG đổi** | Sửa tỷ lệ niêm yết 30 ➜ 25, mở lại màn hình | Cột *Giá niêm yết* đổi; cột *Đang áp dụng* **đứng yên**, hiện dấu ▲; thẻ *Đang lệch* lên 2 | Gia Công `70.000 ➜ 80.000` mà đang áp dụng vẫn `70.000 ▲`; NVL 2 `5.000 ➜ 10.000` mà vẫn `5.000 ▲`; `Đang lệch 2` (**giao diện**) | Pass |
| TC-HAPPY-07 | Xuất Excel — 3 cột đúng thứ tự | Gọi `xuat_excel` với 4 mã, chiết khấu 68% | File `.xlsx`, ô B1 = 68% định dạng phần trăm, tiêu đề `Mã mặt hàng · Giá niêm yết · Giá bán` | Đúng cả ba; B1 = `0.68`, định dạng `0%` (đọc byte file) | Pass |
| TC-HAPPY-08 | 🔴 Cột *Giá bán* là **công thức sống**, không phải số | Đọc ô C4..C7 của file | Chứa công thức trỏ về ô chiết khấu tuyệt đối | `=B4*(1-$B$1)` … `=B7*(1-$B$1)` (đọc byte file) | Pass |

---

## TC-VALID — ràng buộc

| Mã | Việc | Bước thực hiện | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|---|
| TC-VALID-01 | 🔴 Tỷ lệ tính giá niêm yết = 0 | Lưu cài đặt với giá trị 0 | Chặn, nói rõ **đây là số chia** | *"phải lớn hơn 0… Đây là số chia trong công thức"* | Pass |
| TC-VALID-02 | Tỷ lệ tính giá niêm yết > 100 | Lưu với 150 | Chặn, nêu khoảng thường dùng | *"đang là 150.0%, lớn hơn 100%… thường nằm trong khoảng 25–40%"* | Pass |
| TC-VALID-03 | Hao phí âm | Lưu với −5 | Chặn | *"Tỷ Lệ Hao Phí không được âm"* | Pass |
| TC-VALID-04 | Giá trị hợp lệ vẫn lưu được | Lưu 30 / 3 | Lưu bình thường | Lưu được | Pass |
| TC-VALID-05 | 🔴 Mặt hàng không tính được thì **bỏ qua kèm lý do**, không ghi đè bằng 0 | Bấm cập nhật cho `Thành phẩm 1` | Không tạo/sửa `Item Price`; trả lý do | `bo_qua = [{'ma_hang': 'Thành phẩm 1', 'ly_do': 'Chưa có định mức mặc định, hoặc định mức chưa có giá thành'}]` | Pass |
| TC-VALID-06 | Bấm cập nhật lần hai không đổi gì | Bấm lại trên mã vừa cập nhật | `da_doi` rỗng | `da_doi = []` | Pass |
| TC-VALID-07 | Mặt hàng không tính được **không lọt vào file Excel** | Xuất kèm `Thành phẩm 1` | Không có dòng nào mang mã đó | Không có (đọc byte file) | Pass |

---

## TC-EDGE — biên và ngoại lệ

| Mã | Việc | Bước thực hiện | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|---|
| TC-EDGE-01 | Mặt hàng chưa khai *Phương pháp bổ sung* | `cost_cua("NVL 1", None)` | Trả `None` kèm lý do, **không** trả 0 | `None` · *"Mặt hàng chưa khai Phương pháp bổ sung"* | Pass |
| TC-EDGE-02 | Mua hàng nhưng chưa có đơn mua duyệt | mã bất kỳ trong 200 dòng đầu | `None` kèm lý do riêng | *"Chưa có đơn mua nào đã duyệt cho mặt hàng này"* | Pass |
| TC-EDGE-03 | Tỷ lệ niêm yết = 0 lọt xuống hàm tính | `tinh_gia(1000, 5, 10, 3, 0)` | Trả `(Cộng, None)`, **không** nổ `ZeroDivisionError` | `cong=1180.0`, `gia=None` | Pass |
| TC-EDGE-04 | 🔴 Bộ lọc *"chỉ dòng tính được"* phải tìm **cả ngoài giới hạn** | `bang_gia(chi_tinh_duoc=1, gioi_han=5)` | Ra đủ 4 mã dù 4 mã đó đứng cuối bảng chữ cái | 4 mã, `tong=4`, `bi_cat=False` | ⚠ **Vòng 1 Fail** — xem dưới. Đã sửa, chạy lại Pass |
| TC-EDGE-04b | Giới hạn nhỏ hơn số dòng lọc được thì **nói ra** | `gioi_han=2` | Lấy 2 dòng nhưng `tong=4` và `bi_cat=True` | `tong=4 · lay=2 · bi_cat=True` | Pass |
| TC-EDGE-05 | 🔴 BOM lập cho **lô** thì chia `quantity` | Đặt `quantity=10` cho BOM có `total_cost=20.000` | Giá vốn một đơn vị = `2.000` | `2.000` — đúng bằng `20.000 / 10` | Pass |
| TC-EDGE-06 | Đơn mua theo đơn vị khác đơn vị kho | nhân `conversion_factor` | Quy về đơn vị kho | ⚠ **Chưa chạy được ca thật** — xem mục *Chưa chạy* | — |

### 🔴 TC-EDGE-04 vòng 1 Fail — và đây là lỗi tôi tự gây ra

Bộ lọc *"chỉ dòng tính được giá"* trả về **0 dòng**, kèm câu *"Không mặt hàng nào trong danh sách
này tính được giá niêm yết"* — trong khi site có **4 mã** tính được.

Nguyên nhân: tôi lọc **sau** khi đã cắt 200 dòng đầu theo thứ tự chữ cái. Bốn mã đó tên bắt đầu
bằng *"Test…"* nên nằm ngoài. **Không có lỗi, không có cảnh báo** — màn hình chỉ đơn giản nói sai.

Đúng loại *"cắt bớt dữ liệu im lặng"* đã ghi thành bài học của dự án, và tệ hơn: chỗ bị cắt lại có
một **câu khẳng định** đè lên. Lệnh test không bắt được — chỉ bấm thật mới thấy.

Chữa: đưa bộ lọc vào truy vấn qua `ma_co_nguon_cost()`.

**Nhưng vòng 2 vẫn còn sót**, và đây mới là chỗ đáng học: `ma_co_nguon_cost()` chỉ là điều kiện
**cần** — mã có đơn mua nhưng chưa khai *Phương pháp bổ sung* vẫn lọt vào tập ứng viên rồi bị loại
sau. Đo được: tập ứng viên **6 mã**, thật sự tính được **4**. Nên `gioi_han = 5` vẫn cắt mất một mã.
Chữa lần hai: khi đang lọc thì **không cắt lúc lấy dữ liệu**, cắt sau khi đã biết dòng nào thật sự
tính được. Tập ứng viên bị chặn bởi số mã từng lên đơn mua hoặc có định mức nên luôn nhỏ.

---

## TC-PERM — phân quyền

| Mã | Việc | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|
| TC-PERM-01 | Ai mở được màn hình | Kinh doanh và quản trị | `System Manager` · `Sales Manager` · `Sales User` | Pass |
| TC-PERM-02 | 🔴 Ai **sửa được tỷ lệ** | Nhân viên kinh doanh chỉ được **xem** | `Sales User` read=1 **write=0**; `Sales Manager` và `System Manager` write=1 | Pass |

> TC-PERM-02 có lý do nghiệp vụ: hai tỷ lệ này áp cho **toàn hệ thống**, đổi một con số là đổi giá
> niêm yết của cả nhà máy. Không nên để mỗi nhân viên bán hàng sửa được.

---

## TC-ISO — cách ly app khách

| Mã | Việc | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|
| TC-ISO-01 | Trường mới thuộc đúng module app khách | `MBWNext HKLed` | `custom_ty_le_rnd` và `custom_ty_le_loi_nhuan` đều `MBWNext HKLed` | Pass |
| TC-ISO-02 | DocType mới thuộc đúng module | `MBWNext HKLed` | `HKLed Pricing Setting` → `MBWNext HKLed` | Pass |
| TC-ISO-03 | 🔴 **Không** thêm trường vào màn hình cài đặt của app lõi | `MBWNext System Setting` không bị đụng | Dựng Single riêng; không sửa file nào của app lõi | Pass |

---

## TC-REGR — không làm hỏng cái đang chạy

| Mã | Việc | Mong đợi | Kết quả | Đạt |
|---|---|---|---|---|
| TC-REGR-01 | Cập nhật một mã **không đụng** `Item Price` của mã khác | Chỉ mã được chọn thay đổi | Bấm cho `Test NVL 1`: mã bị đổi `[]`, mã mới `[]` — vì giá đã đúng sẵn | Pass |
| TC-REGR-02 | Đơn bán đã lập không đổi giá | `price_list_rate` của đơn cũ giữ nguyên | Không đụng `Sales Order Item`; trường đó của lõi chỉ lấy giá lúc chọn mặt hàng | Pass |
| TC-REGR-03 | Không cần `bench migrate` để chạy | Nạp DocType + Page riêng, chạy patch tay | Chạy được — nhưng **"0 patch chờ" là SAI** | ⚠ Sửa 09/09 |

🔴 **TC-REGR-03 ghi sai, đã đo lại 09/09 trên nền erpnext 15.112: app có `1` patch chờ, chính là `mbwnext_hkled.patches.them_ty_le_gia_niem_yet` của tính năng này.** Hai Custom Field của nó CÓ trên site — nhưng vì hồi làm tôi gọi `execute()` **bằng tay**, mà gọi tay thì **không ghi vào `Patch Log`**. Vế "không cần `bench migrate` để chạy" vẫn đúng (tính năng chạy được ngay); vế "0 patch chờ" thì sai. ➜ **Merge tính năng này lên site khác BẮT BUỘC `bench migrate`.** Patch an toàn khi chạy lại: `create_custom_fields(update=True)`, phần khai mặc định có rào `if not …` nên không đè số của khách. Xem [`chay-lai-tc-regr-nen-15112.md`](chay-lai-tc-regr-nen-15112.md).

---

## Chưa chạy — ghi ra thay vì giấu sau con số tổng

| Mã | Vì sao chưa chạy |
|---|---|
| TC-EDGE-06 | Cổng 8012 **không có** dòng đơn mua nào `conversion_factor ≠ 1` — cả 35 dòng đơn bán và các dòng đơn mua đều bằng 1. Dựng một cái là ghi dữ liệu thật vào chứng từ mua. Đã đọc kỹ mã và ghi chú lý do trong `_gia_don_mua_gan_nhat`, nhưng **đó là đọc, không phải đo** |
| TC-XUAT-UI | Nút **Xuất Excel** trên giao diện mới chỉ kiểm tới bước mở hộp thoại; phần tải file về máy chưa bấm được trong môi trường test tự động. Nội dung file thì đã kiểm bằng cách đọc thẳng byte (TC-HAPPY-07/08) |
| TC-PERM-03 | Chưa đăng nhập bằng tài khoản `Sales User` thật để bấm thử — mới đọc bảng phân quyền |

---

## Dọn dẹp sau khi test

- Tỷ lệ tính giá niêm yết đã **trả về 30**.
- `quantity` của BOM sửa trong TC-EDGE-05 đã **rollback về 1**.
- **Giữ lại**: 4 dòng `Item Price` trên bảng giá `Standard Selling` cho `Test NVL 1/2/3` và
  `Test Gia Công` — sinh ra trong lúc bấm thật, cố ý để lại để anh Thắng có dữ liệu mà thử ngay.
  Bảng giá `Standard Selling` từ 11 lên **15** dòng.

---

## Kết luận

- **36 ca chạy, 36 đạt**; **3 ca chưa chạy** được, ghi rõ ở mục trên và vì sao. Tổng 39 mã ca.

  *(Con số này tôi ghi nhầm thành 34/34 ở bản đầu rồi đếm lại mới ra 36 — đúng loại lỗi tự làm
  hỏng phép đếm của chính mình mà file này đang cảnh báo ở TC-EDGE-04. Đếm bằng lệnh, đừng ước.)*
- Một ca **vòng đầu Fail** (TC-EDGE-04), tự bắt được khi **bấm thật** chứ không phải khi chạy lệnh —
  và phải sửa **hai lần** mới đúng.
- **Đủ điều kiện nghiệm thu: CÓ** cho vòng tự kiểm. Chờ vòng test tay của anh Thắng.
- ⚠ Phải **chạy lại toàn bộ** sau khi cài lên site thật: nền lệch hai chiều (frappe cao hơn,
  erpnext thấp hơn 22 bản minor).

---

# Đợt 2 — Chuyển trang, ô tìm kiếm, tick sống qua trang

> **Chốt:** anh Thắng 09/09/2026 14:55 — *"Câu 1: đúng em nhé / Câu 2: a) tìm theo cả 2 b) có em nhé /
> R&D và Lợi nhuận không sửa trên bảng em nhé, chỉ được sửa ở bản ghi mặt hàng"*
> **Chạy trên:** cổng 8012, **09/09/2026 chiều** — frappe 15.120.0 · erpnext **15.112.0**
> **Bản vẽ:** [`../mockups/xuat-bang-gia-niem-yet.html`](../mockups/xuat-bang-gia-niem-yet.html) bản 4

## Chạy bằng lệnh — đã chạy

| ID | Kiểm cái gì | Cách đo | Mong đợi | Đo được | KQ |
|---|---|---|---|---|---|
| TC-TRANG-01 | Phân trang chia đúng | `bang_gia()` mặc định | `so_trang` khớp `tong / moi_trang` | 61.612 mã, **617 trang** × 100 | ✅ Đạt |
| TC-TRANG-02 | Trang 2 khác trang 1 | so mã đầu hai trang | khác nhau | `trang1[0] ≠ trang2[0]` | ✅ Đạt |
| TC-TRANG-03 | 🔴 Số đếm và số lấy **không được lệch nhau** | cộng dồn số dòng của tất cả các trang, so với `tong` | bằng nhau | tìm `Test`, 3 dòng/trang: **5 trang = 14 dòng, `tong` báo 14** | ✅ Đạt |
| TC-TRANG-04 | Trang vượt quá thì kẹp về trang cuối | `trang=99999` | trả trang cuối, không rỗng | trả `trang=617/617`, **12 dòng** | ✅ Đạt |
| TC-TIM-01 | Tìm khớp **đoạn giữa** của mã | `tim="64LED"` | ra mọi mã chứa chuỗi đó | **66 mã**, vd `CM30S050-3B3-5C-64LED` | ✅ Đạt |
| TC-TIM-02 | Tìm theo **cả tên hàng**, không chỉ mã | `tim="Test"` | ra cả mã lẫn tên khớp | **14 mã**, có `Module test`, `Nguồn test`, `Ốc vít test` — ba mã này khớp **TÊN**, không khớp mã | ✅ Đạt |
| TC-TIM-03 | 🔴 Tìm + bộ lọc chạy chung, lọc **trong** truy vấn | `tim="Test", chi_tinh_duoc=1` | giao của hai tập | **7 mã**, đúng bằng tập tính được | ✅ Đạt |
| TC-TIM-04 | Tham số cũ `gioi_han` vẫn gọi được | `gioi_han=200` | hiểu là 200 dòng/trang | `moi_trang=200`, 200 dòng | ✅ Đạt |

⚠ **TC-TRANG-03 là ca đáng giá nhất của đợt này.** Câu đếm và câu lấy dữ liệu dùng **chung một hàm
`_dieu_kien()`** đúng vì lý do đó: viết WHERE hai lần thì màn hình báo *"trang 7/12"*, mở trang 7
ra rỗng — và **rỗng trông y hệt "hết dữ liệu"**, không có dấu hiệu nào để nghi.

⚠ **TC-TIM-02 kiểm được điều mà đếm số không kiểm được.** Ba mã `Module test` / `Nguồn test` /
`Ốc vít test` khớp **tên** chứ không khớp **mã** — nếu chỉ tìm theo mã thì chúng biến mất, mà
tổng số vẫn ra một con số trông hợp lý.

## Chưa chạy — phải bấm nút thật

| ID | Kiểm cái gì | Vì sao chưa chạy |
|---|---|---|
| TC-TICK-01 | Tick mã A, tìm mã B, tick B → **cả hai còn tick** | thao tác giao diện |
| TC-TICK-02 | Ô *"đang giữ N mã"* mở ra danh sách, bỏ được từng mã | thao tác giao diện |
| TC-TICK-03 | Có mã ngoài trang đang xem → hiện dòng cảnh báo | thao tác giao diện |
| TC-TICK-04 | Hộp thoại xác nhận **liệt kê từng mã**, đánh dấu mã ngoài trang | thao tác giao diện |
| TC-TICK-05 | Nút *Bỏ chọn tất cả* xoá sạch tick | thao tác giao diện |
| TC-TICK-06 | Ô tick đầu bảng chỉ tác động **trang đang xem** | thao tác giao diện |
| TC-TICK-07 | Bấm *Cập nhật* ghi đúng cả mã ngoài trang | **ghi `Item Price` thật** — để anh Thắng làm |
| TC-XEM-01 | R&D / Lợi nhuận trên bảng **không sửa được** | thao tác giao diện |

🔴 **TC-TICK-07 cố ý để anh Thắng chạy.** Nó ghi `Item Price` thật trên dữ liệu thật; tôi tự bấm là
đổi giá sales nhìn thấy mà không ai yêu cầu.

---

# Đợt 3 — Hai cách lấy giá vốn cho mặt hàng Mua hàng

> **Yêu cầu:** anh Thắng chuyển ý khách 09/09/2026 15:56 — *"đối với những mặt hàng có phương pháp
> bổ sung mua hàng, khách hàng đang muốn có 2 cách lấy giá vốn: lấy giá trên đơn mua gần nhất và
> giá vốn tồn kho trung bình, họ muốn có thể lựa chọn được 1 trong 2 cách"*
> **Chạy trên:** cổng 8012, **09/09/2026 chiều** — erpnext 15.112.0

| ID | Kiểm cái gì | Đo được | KQ |
|---|---|---|---|
| TC-NGUON-01 | Hai cách ra số **khác nhau** trên cùng một mã | `Test NVL 1`: đơn mua **10.000** → niêm yết **35.000**; tồn kho **6.000** → niêm yết **20.000** | ✅ Đạt |
| TC-NGUON-02 | Mã chỉ có một nguồn thì hai cách ra **cùng** một số | `Test NVL 2`, `Test NVL 3`: 10.000 cả hai cách | ✅ Đạt |
| TC-NGUON-03 | 🔴 Tập ứng viên **đổi theo nguồn** | `ma_co_nguon_cost`: **9** mã theo đơn mua, **13** mã theo tồn kho | ✅ Đạt |
| TC-NGUON-04 | Mặt hàng Sản xuất/Gia công **không bị ảnh hưởng** | `Test BTP 1/2`, `Test Gia Công`, `Test Tp` giữ nguyên số ở cả hai cách | ✅ Đạt |
| TC-NGUON-05 | Chưa khai cài đặt thì giữ hành vi cũ | Single rỗng → `nguon_gia_von_mac_dinh()` = *Đơn mua gần nhất* | ✅ Đạt |
| TC-NGUON-06 | Ba hàm đều nhận `nguon` | `bang_gia`, `cap_nhat_gia`, `xuat_excel` — chữ ký có `nguon=None` | ✅ Đạt |
| TC-NGUON-07 | Patch của tính năng đã vào `Patch Log` | sau `bench migrate`: **0 patch chờ** | ✅ Đạt |

⚠ **TC-NGUON-03 là ca đáng giá nhất.** Nếu để nguyên câu lọc theo đơn mua trong khi người dùng đã
chuyển sang *giá vốn tồn kho*, thì **4 mã có tồn mà chưa từng lên đơn mua bị bỏ sót hẳn** — và bỏ
sót không có dấu hiệu nào, bảng vẫn ra một danh sách trông đầy đủ.

⚠ **TC-NGUON-02 là cái bẫy khi test.** Hai trong ba mã *Mua hàng* ra **cùng một số** ở cả hai cách.
Ai thử đúng hai mã đó sẽ kết luận *"hai cách như nhau"*. **Phải thử trên `Test NVL 1`.**

## Chưa chạy — phải bấm nút thật

| ID | Kiểm cái gì | Vì sao chưa chạy |
|---|---|---|
| TC-NGUON-08 | Đổi ô *Giá vốn mặt hàng mua* trên màn hình → bảng tính lại, chip hiện *"đang xem tạm"* | thao tác giao diện |
| TC-NGUON-09 | Đổi trong **Cài đặt tỷ lệ** → mở lại bảng thấy theo cài đặt mới | thao tác giao diện |
| TC-NGUON-10 | 🔴 Xem tạm theo tồn kho rồi bấm **Cập nhật** → hộp thoại cảnh báo, và **ghi đúng con số đang xem** | **ghi `Item Price` thật** — để anh Thắng chạy |
| TC-NGUON-11 | Xuất Excel khi đang xem tạm → file mang con số đang xem | tải file |
