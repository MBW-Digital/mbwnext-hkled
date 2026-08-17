# Test case — Trường Phương pháp bổ sung trên Mặt hàng (PM-TASK-00067)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Ngày chạy vòng tự kiểm:** 12/08/2026 · **Người chạy:** Claude (Trợ lý)

Yêu cầu: thêm trường **Phương pháp bổ sung** (Select — *Sản xuất / Gia công / Mua hàng*) trên Mặt
hàng, rồi cập nhật cho danh mục. Sau này dùng cho chức năng dự báo tồn kho.

Nguồn dữ liệu nằm ở **hai chỗ**:

| Nguồn | Nội dung | Dòng |
|---|---|---|
| `data/danh_muc/*.csv` | vật tư, linh kiện — khách thêm cột vào 11 sheet của PM-TASK-00061 | 1.516 |
| `data/thanh_pham/*.csv` | đèn thành phẩm — 4 file *Nhóm I…IV* trong thư mục Drive của task này | 58.968 |

File thành phẩm chỉ giữ 3 cột cần dùng (*Mã sản phẩm, Mã biến thể, Phương pháp bổ sung*), không chép
cả bảng: bản gốc là 4 Google Sheet nặng ~10 MB với 30+ cột thuộc việc nhập danh mục đèn — không phải
việc của task này.

## Dữ liệu trước khi chạy

60.784 Mặt hàng. Chưa có Custom Field nào tương đương trên Item.

---

## TC-HAPPY — trường và dữ liệu

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Tạo được trường | Chạy patch | Custom Field trên Item | Pass | Pass |
| TC-HAPPY-02 | Đúng kiểu và danh sách giá trị | Đọc meta của Item | Select, 3 giá trị *Sản xuất / Gia công / Mua hàng*, kèm một dòng trống | Pass | Pass |
| TC-HAPPY-03 | Vị trí trên form | Xem thứ tự trường | Ngay dưới *Item Line*, trong tab Chi tiết (idx 7) | Pass | Pass |
| TC-HAPPY-04 | 🔴 Điền đúng theo nguồn | Đối chiếu từng dòng của cả 15 file với giá trị trên site | Khớp tuyệt đối | Pass — **60.484/60.484, 0 sai lệch** | Pass |
| TC-HAPPY-05 | 🔴 Mặt hàng cha KHÔNG mang giá trị | Đếm mặt hàng cha có giá trị | 0 | Pass — đã xoá 214 giá trị lỡ đặt ở vòng đầu | Pass |
| TC-HAPPY-06 | Phân bố giá trị | Đếm theo giá trị | Toàn bộ đèn thành phẩm là *Sản xuất* | Pass — 59.676 Sản xuất + 798 Mua hàng | Pass |

## TC-VALID — không đoán hộ khách

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | 🔴 Cha có biến thể khai khác nhau | `C30C050`: 24 biến thể *Sản xuất*, 1 biến thể *Mua hàng* | Cha để trống, 25 biến thể giữ giá trị riêng | Pass — đúng lý do Thắng nêu khi chốt bỏ giá trị ở cha | Pass |
| TC-VALID-02 | Mặt hàng ngoài phạm vi nguồn | Đếm mặt hàng thường còn trống | Chỉ còn hàng test cũ | Pass — 37 mã, đều là `Thành phẩm A-*`, `NVL 1`, `Vỏ test A-*`, `Module test`… | Pass |
| TC-VALID-03 | Không ép giá trị mặc định | Xem `default` của trường | Không có mặc định | Pass — có dòng trống đầu danh sách | Pass |

## TC-REGR — không đụng thứ khác

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Không đổi trường lõi | So `default_material_request_type` trước/sau | Vẫn `Purchase` cho toàn bộ | Pass — cố ý không đụng, xem mục dưới | Pass |
| TC-REGR-02 | Fixtures chỉ thêm đúng 1 | So `custom_field.json` trước/sau | 30 → 31, không trường cũ nào đổi nội dung | Pass | Pass |
| TC-REGR-03 | Không đụng dữ liệu item khác | Dùng `db_set`, không `doc.save()` | Không chạy lại validate của Item, không đổi `modified` | Pass | Pass |
| TC-REGR-04 | File nguồn chỉ thêm cột | So 11 CSV cũ/mới từng ô | Chỉ thêm cột *Phương pháp bổ sung*, 0 thay đổi khác | Pass | Pass |

## TC-EDGE — ca dễ sót

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | Chạy lại không đổi gì | Chạy patch lần 2 | Điền 0, không tạo trường trùng | Pass | Pass |
| TC-EDGE-02 | Lọc nhanh theo trường | Xem `in_standard_filter` | Lọc được ngay trên danh sách Mặt hàng | Pass — đã bật | Pass |
| TC-EDGE-03 | Kiểm trên giao diện | Mở `C28DX03S100-328-40C-280LED` trên Desk | Ô *Phương pháp bổ sung* nằm dưới *Item Line*, hiện *Sản xuất* | Pass (**giao diện**) | Pass |
| TC-EDGE-04 | Giá trị *Gia công* | Đọc danh sách lựa chọn của ô trên form | Có đủ 4 mục: trống, Sản xuất, Gia công, Mua hàng | Pass (**giao diện**) — dù bảng chưa dùng *Gia công* | Pass |

---

## Quyết định đã tự chốt

**Không dùng lại trường lõi `default_material_request_type`** dù nghĩa gần trùng (*Purchase /
Material Transfer / Material Issue / Manufacture / Customer Provided*). Hai lý do:

1. Nó **không có** giá trị tương ứng *"Gia công"* — ERPNext mô tả gia công bằng cờ
   `is_sub_contracted_item` + BOM, không phải một lựa chọn trong danh sách.
2. Trường lõi đang là `Purchase` cho cả 60.784 mặt hàng (giá trị mặc định, chưa ai đụng) và nó
   **điều khiển hành vi thật** của Yêu cầu mặt hàng. Ghi đè hàng loạt là đổi nghiệp vụ chứ không
   chỉ gắn nhãn phân loại.

Đã nêu với HKLED để họ biết có hai trường nghĩa gần nhau.

## Hai lần Thắng chỉnh hướng (12/08)

**1. Đèn thành phẩm có nguồn riêng.** Vòng đầu em để trống 59.064 đèn thành phẩm vì bảng danh mục
không phủ, và hỏi HKLED. Thắng chỉ ra 4 file *Nhóm I…IV* trong thư mục Drive chính là dữ liệu đèn —
đều đã có cột *Phương pháp bổ sung*. Đối chiếu: **58.968/58.968 mã trong 4 file đều có trên site**,
tất cả là *Sản xuất*.

**2. Mặt hàng cha không mang giá trị này.** Vòng đầu em điền cho cha khi mọi biến thể khai giống
nhau. Thắng bác: *"cùng 1 mặt hàng cha có biến thể là sản xuất, có biến thể là mua hàng"* — đúng, và
`C30C050` là ví dụ sống. Đã gỡ khỏi bộ nạp và **xoá 214 giá trị đã lỡ đặt**.

## Còn lại

37 mặt hàng thường chưa có giá trị, **đều là hàng test cũ trên site dev** (`Thành phẩm A-*` 24 mã,
`Vỏ test A-*` 4 mã, `NVL 1/2/3`, `Bán thành phẩm 1/2`, `Module test`, `Nguồn test`, `Ốc vít test`,
`Thành phẩm 1`). Không có sản phẩm thật nào bị bỏ sót.
