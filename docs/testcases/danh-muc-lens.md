# Test case — Nạp sheet (PLS) Lens (PM-TASK-00108)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Ngày chạy vòng tự kiểm:** 17/08/2026 · **Người chạy:** Claude (Trợ lý)

Sheet thứ 12 khách thêm vào workbook danh mục của PM-TASK-00061: **(PLS) Lens**, 82 dòng,
18 mặt hàng cha. Dùng lại nguyên bộ nạp sẵn có, chỉ thêm file nguồn
`data/danh_muc/11-pls-lens.csv`.

Lý do làm lẻ đợt này (chốt của Thắng 17/08): *"có thêm sheet này là đã có thể test được hoàn chỉnh
tính năng BOM Template"*. Phần còn lại của danh mục sẽ đợi khách sửa xong rồi up nốt một lần.

## Dữ liệu trước khi chạy

60.784 Mặt hàng. Nhóm *(PLS) Lens* chưa có. Không mã nào trong sheet trùng mã sẵn có.

---

## TC-HAPPY

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Nạp không lỗi | Chạy bộ nạp | Không dừng giữa chừng | Pass | Pass |
| TC-HAPPY-02 | Số item tạo ra | Đếm trước/sau | 60.784 → 60.872 (+88) | Pass — 18 cha + 70 biến thể | Pass |
| TC-HAPPY-03 | 🔴 Nội dung từng dòng | Đối chiếu tên, nhóm, đơn vị, giá, `variant_of`, đặc tính và *Phương pháp bổ sung* | Khớp tuyệt đối | Pass — **82/82, 0 sai lệch** | Pass |
| TC-HAPPY-04 | Tạo nhóm sản phẩm | Xem nhóm mới | *(PLS) Lens* | Pass | Pass |
| TC-HAPPY-05 | Phương pháp bổ sung | Xem giá trị 70 biến thể | *Mua hàng* | Pass — điền 70, cha không mang giá trị | Pass |
| TC-HAPPY-06 | Kiểm trên giao diện | Lọc danh sách theo nhóm *(PLS) Lens* | 88 dòng, Template/biến thể phân biệt được | Pass (**giao diện**) | Pass |

## TC-VALID

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | Dòng lặp y hệt | 6 mã lặp 3 lần, nội dung giống nhau từng ô | Giữ dòng đầu, không coi là lỗi | Pass — bỏ bớt 12 dòng | Pass |
| TC-VALID-02 | Cha lệch bộ đặc tính | `PLS-MDS`, `PLS-MDC`, `PLS-VDXHB` | Vẫn nạp, cha lấy hợp các đặc tính | Pass — đúng hành vi đã sửa theo phản biện của Thắng ở task 61 | Pass |
| TC-VALID-03 | Giá trị đặc tính mới | *Số mắt LED* thiếu 13 giá trị | Tự thêm, `abbr` không đụng nhau | Pass | Pass |
| TC-VALID-04 | Không tạo đặc tính mới | 5 cột đặc tính của sheet | Đều đã có sẵn trên site | Pass — 0 Item Attribute mới | Pass |

## TC-REGR

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Không đụng 11 sheet cũ | Chạy lại cả bộ | 11 file cũ thêm 0 item | Pass | Pass |
| TC-REGR-02 | Mặt hàng cha vẫn không mang *Phương pháp bổ sung* | Đếm cha có giá trị | 0 | Pass | Pass |
| TC-REGR-03 | Không sinh mã mồ côi | So tập mã nguồn với item trên site | 0 thừa | Pass | Pass |

## TC-EDGE

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | 🔴 Cột *Phương pháp bổ sung* không phải đặc tính | Chạy bộ nạp trên file có cột đó | Bỏ qua khi suy đặc tính | **Fail lần đầu → đã sửa**, xem mục dưới | Pass |
| TC-EDGE-02 | Chạy lại không đẻ trùng | Chạy lần 2 | Thêm 0 | Pass | Pass |

---

## Lỗi phát hiện trong lúc làm

**Bộ nạp coi *"Phương pháp bổ sung"* là một đặc tính biến thể.** Cột này khách thêm vào cả 12 sheet
ở PM-TASK-00067, nhưng `COT_CO_DINH` chưa liệt kê nó, nên `_cot_dac_tinh()` xếp nhầm nó vào nhóm đặc
tính rồi dừng ở *"Chưa có Item Attribute 'Phương pháp bổ sung' trên site"*.

Đáng nói là **lỗi này không lộ ra ở task 67**: hôm đó em chỉ chạy patch điền giá trị, không chạy lại
bộ nạp. Nó chỉ nổ khi nạp sheet mới — và trên **site cài mới thì `bench migrate` sẽ vỡ ngay**, vì
patch nạp danh mục chạy trên bộ CSV đã có cột đó. Đã thêm cột vào `COT_CO_DINH` kèm ghi chú.
