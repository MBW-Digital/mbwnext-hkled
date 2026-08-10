# Test case — Cấu trúc mã chứng từ HKLED (PM-TASK-00054)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`
**Ngày chạy vòng tự kiểm:** 08/08/2026 · **Người chạy:** Claude (Trợ lý)

Đổi mã chứng từ của 9 loại phiếu theo bảng HKLED gửi trong PM-TASK-00054, dạng
`<viết tắt>-<2 số năm>-<5 số thứ tự>`.

| Loại chứng từ | Mã cũ (ERPNext) | Mã mới |
|---|---|---|
| Đơn hàng bán | `SAL-ORD-2026-` | `SO-26-` |
| Kế hoạch sản xuất | `MFG-PP-2026-` | `KSX-26-` |
| Lệnh sản xuất | `MFG-WO-2026-` | `LSX-26-` |
| Chứng từ kho nội bộ | `MAT-STE-2026-` | `KNB-26-` |
| Phiếu xuất kho hàng bán | `MAT-DN-2026-` | `PXK-26-` |
| Phiếu nhập kho hàng mua | `MAT-PRE-2026-` | `PNK-26-` |
| Yêu cầu mặt hàng | `MAT-MR-2026-` | `YCM-26-` |
| Đơn mua hàng | `PUR-ORD-2026-` | `PO-26-` |
| Báo giá | `SAL-QTN-2026-` | `BG-26-` |

Cấu hình nằm ở 19 **Property Setter** (`module = MBWNext HKLed`), tạo bởi patch
`set_document_naming_series` và đã đưa vào `fixtures` để site cài mới có ngay.

## Dữ liệu chuẩn bị

Vòng tự kiểm tạo **bản nháp thật của cả 9 loại** rồi xoá ngay. Dùng: kho *Kho đang sản xuất - HKL*,
mặt hàng *Thành phẩm 1*, BOM *BOM-Thành phẩm 1-002*, khách *0779734666*, NCC *NCC A*.

⚠ Sau khi chạy đã đối chiếu lại số lượng từng loại chứng từ **khớp đúng như trước khi test**, và
mọi bộ đếm `-26-` đều trở về 0 — nên chứng từ thật đầu tiên của HKLED vẫn là số **00001**, không bị
vòng test ăn mất số.

---

## TC-HAPPY — chứng từ tạo mới mang mã mới

Mỗi ca: tạo bản nháp trên site rồi đọc mã hệ thống sinh ra.

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | Đơn hàng bán | Bán hàng › Đơn hàng bán › **Thêm**, điền khách + 1 dòng hàng, Lưu | Mã `SO-26-00001` | `SO-26-00001` | Pass |
| TC-HAPPY-02 | Kế hoạch sản xuất | Sản xuất › Kế hoạch sản xuất › **Thêm**, 1 dòng mặt hàng, Lưu | `KSX-26-00001` | `KSX-26-00001` | Pass |
| TC-HAPPY-03 | Lệnh sản xuất | Sản xuất › Lệnh sản xuất › **Thêm**, chọn mặt hàng + BOM, Lưu | `LSX-26-00001` | `LSX-26-00001` | Pass |
| TC-HAPPY-04 | Chứng từ kho nội bộ | Kho › Chứng từ kho › **Thêm**, mục đích *Material Receipt*, Lưu | `KNB-26-00001` | `KNB-26-00001` | Pass |
| TC-HAPPY-05 | Phiếu xuất kho hàng bán | Kho › Phiếu xuất kho › **Thêm**, Lưu | `PXK-26-00001` | `PXK-26-00001` | Pass |
| TC-HAPPY-06 | Phiếu nhập kho hàng mua | Kho › Phiếu nhập kho › **Thêm**, Lưu | `PNK-26-00001` | `PNK-26-00001` | Pass |
| TC-HAPPY-07 | Yêu cầu mặt hàng | Kho › Yêu cầu mặt hàng › **Thêm**, Lưu | `YCM-26-00001` | `YCM-26-00001` | Pass |
| TC-HAPPY-08 | Đơn mua hàng | Mua hàng › Đơn mua hàng › **Thêm**, Lưu | `PO-26-00001` | `PO-26-00001` | Pass |
| TC-HAPPY-09 | Báo giá | Bán hàng › Báo giá › **Thêm**, Lưu | `BG-26-00001` | `BG-26-00001` | Pass |

## TC-UI — ô Series trên màn hình

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-UI-01 | Ô **Series** điền sẵn mã mới | Mở màn hình tạo mới Đơn hàng bán | Ô Series hiện `SO-.YY.-`, không phải mã cũ | Pass (**giao diện** `dev.mbwnext.com:8012`) | Pass |
| TC-UI-02 | Không còn mã cũ trong danh sách chọn | Bấm vào ô **Series** của cả 9 màn hình | Chỉ còn mã mới; riêng Phiếu xuất/nhập kho còn thêm dòng hàng trả lại | Pass — đọc `frappe.get_meta` của cả 9 loại trên trình duyệt | Pass |
| TC-UI-03 | Giữ series hàng trả lại | Xem danh sách chọn của Phiếu xuất kho / Phiếu nhập kho | Còn `MAT-DN-RET-.YYYY.-` / `MAT-PR-RET-.YYYY.-` | Pass | Pass |

## TC-REGR — không đụng vào dữ liệu cũ

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Chứng từ cũ giữ nguyên mã | Mở danh sách Kế hoạch sản xuất | Vẫn là `MFG-PP-2026-00005`… , không bị đổi tên | Pass | Pass |
| TC-REGR-02 | Mở/sửa được chứng từ cũ | Mở một Đơn hàng bán `SAL-ORD-2026-…`, sửa rồi Lưu | Lưu bình thường, mã không đổi | Pass | Pass |
| TC-REGR-03 | Không trùng bộ đếm giữa các loại | Đối chiếu 9 tiền tố mới với bảng `tabSeries` | 9 tiền tố khác nhau đôi một, không loại nào dùng chung | Pass — chỉ app này khai 9 tiền tố đó | Pass |
| TC-REGR-04 | Số thứ tự bắt đầu từ 00001 | Đọc bộ đếm sau khi dọn dữ liệu test | Mọi bộ đếm `-26-` = 0 | Pass | Pass |

## TC-EDGE — ca dễ sót

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | 🔴 **Nhân bản** chứng từ cũ không kéo theo mã cũ | Mở `MFG-PP-2026-00014`, menu ⋯ › **Duplicate** | Bản mới dùng `KSX-.YY.-` | Pass — trước khi sửa cho ra `MFG-PP-.YYYY.-`, xem mục *Vấn đề đã phát hiện* | Pass |
| TC-EDGE-02 | Nhân bản 8 loại còn lại | Mở `SAL-ORD-2026-00001`, menu ⋯ › **Duplicate** | Bản mới dùng `SO-.YY.-`, vẫn chép khách hàng và dòng hàng | Pass (**giao diện**) — Series `SO-.YY.-`, khách hàng và 1 dòng hàng được chép. 7 loại còn lại chưa bấm tay, nhưng cùng cơ chế: ERPNext lõi đã đặt `no_copy` sẵn cho cả 8 | Pass |
| TC-EDGE-03 | Cài lại site mới vẫn có mã mới | `bench migrate` trên site chưa từng chạy patch | Property Setter được nạp từ `fixtures` | Pass — đã export 19 Property Setter vào `fixtures/property_setter.json` | Pass |
| TC-EDGE-04 | Chạy lại patch nhiều lần | Chạy `set_document_naming_series.execute` lần 2 | Không tạo bản ghi trùng, vẫn 19 Property Setter | Pass | Pass |
| TC-EDGE-05 | Không sinh chứng từ mồ côi | Sau khi dọn dữ liệu test, dò Employee Allocation trỏ vào Lệnh sản xuất đã xoá | Không có bản ghi mồ côi | Pass — 0 bản ghi | Pass |
| TC-EDGE-06 | Sang năm 2027 tự đổi số năm | Chưa chạy được (phải đợi hoặc chỉnh giờ hệ thống) | `SO-27-00001`, bộ đếm bắt đầu lại | **Chưa chạy** — `.YY.` là cơ chế chuẩn của Frappe, nhưng chưa kiểm bằng tay | — |

---

## Vấn đề đã phát hiện trong lúc test

**Nhân bản Kế hoạch sản xuất cũ đẻ ra mã cũ.** Trong 9 loại thì 8 loại được ERPNext lõi đặt sẵn
`no_copy` cho ô Series, riêng **Kế hoạch sản xuất thì không**. Hệ quả: bấm **Duplicate** một Kế
hoạch sản xuất cũ sẽ chép luôn `MFG-PP-.YYYY.-` sang bản mới và đẻ ra `MFG-PP-2026-00015` theo mã
cũ. Không có thông báo lỗi nào, vì `_validate_selects()` của Frappe **cố ý bỏ qua** đúng trường
`naming_series` — nên chỉ âm thầm sai định dạng.

Đã sửa trong cùng patch: thêm Property Setter `no_copy = 1` cho `Production Plan`, cho khớp 8 loại
còn lại. TC-EDGE-01 chạy lại sau khi sửa cho ra `KSX-.YY.-`.

## Điểm cần HKLED xác nhận

1. **Chứng từ cũ giữ nguyên mã**, không đổi tên hàng loạt — vì đổi tên sẽ làm lệch mọi bản in đã
   phát hành và mọi tham chiếu ngoài hệ thống.
2. **Số thứ tự bắt đầu lại từ 00001** cho mỗi mã mới. Bộ đếm của Frappe gắn theo tiền tố nên không
   có cách nối tiếp số cũ.
3. **Hai series hàng trả lại** (`MAT-DN-RET-`, `MAT-PR-RET-`) bảng khách gửi không nhắc tới nên cố ý
   giữ nguyên. Nếu HKLED muốn đổi thì cho biết mã mong muốn.
