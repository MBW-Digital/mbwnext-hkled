# Test case — HKLED BOM Template theo Biến Thể (Giai đoạn 1)

- Tính năng: `apps/mbwnext_hkled/docs/features/bom-template-theo-bien-the.md`
- App: `mbwnext_hkled` · Site: `hkled.com` · Dev server: `http://localhost:8047`
- Nguyên tắc: **Claude tự chạy thử trước (mục A–B) → người dùng test tay qua UI thật (mục C–G)**.
  Không dùng `FrappeTestCase`.

⚠️ **Quy tắc an toàn khi test**: mọi NVL test đặt tiền tố `ZZTEST-`. **Không** trỏ BOM Template test
vào Item Template đèn thật đã có BOM Default đang được Work Order tham chiếu (bài học Phần I).

---

## A. Công thức số lượng — Claude đã chạy: 57/57 PASS

Gọi trực tiếp Server Script với biến thể thật, đối chiếu giá trị **tính tay từ tài liệu**.

| Ca | Nhóm | CS (W) | Kiểu lắp | Nguồn | Biến thể thật | Kỳ vọng |
|---|---|---|---|---|---|---|
| A | P01_P03 | 50 | Dọc | HKLED Nhỏ | DP01C050-3B3HN-D | Module 1 · Ốc vít module 2 · Cầu đấu 0 · Dây cấp nguồn 0 · Nguồn 1 |
| B | P01_P03 | 200 | Ngang | HKLED Dim 1 Cấp | DP01C200-3B3HT-N | Module 4 · Ốc vít 8 · Cầu đấu 2 · Dây cấp nguồn 100 · Nguồn 2 |
| C | P01_P03 | 600 | Ngang | Philips Dim 1 Cấp | DP01C600-3B3PT-N | Module 12 · Ốc vít 24 · Cầu đấu 3 · Dây cấp nguồn 100 · Nguồn 3 |
| D | P01_P03 | 300 | Dọc | Done Dim 1 Cấp | DP01C300-3B3DT-D | Cầu đấu 2 · Dây cấp nguồn 100 · Nguồn 2 |
| E | D01_D05 | 250 | — | HKLED Dim 5 Cấp | DD01C250-3B3HD | Module 5 · Ốc vít 10 · Cầu đấu 1 · Dây cấp nguồn 70 · Nguồn 1 |
| F | D01_D05 | 300 | — | Philips Dim 10 Cấp | DD01C300-3B3PD | Cầu đấu 2 · Nguồn 2 |
| G | PTX | 150 | — | HKLED Nhỏ | DPKDC150-3B3HN | Chip LED 3 · Ốc vít chip 12 · Dây cấp nguồn 50 · Dây đấu chip Đỏ/Đen 0 · Nguồn 3 |
| H | PTX | 300 | — | HKLED Dim 1 Cấp | DPKDC300-3B3HT | Dây đấu chip 150 · Nguồn 1 |
| I | PTX | 500 | — | Meanwell Dim 1 Cấp | DPTRC500-3B3MT | Dây đấu chip 250 · Nguồn 2 |
| J | XHB | 400 | — | HKLED Nhỏ | DXHBC400-3B3HN | Chip LED 8 · Ốc vít chip 32 · Dây đấu chip 240 · Dây cấp nguồn 50 · Nguồn 8 |
| K | DQL | 50 | — | Done Nhỏ | DDQLC050-3B3DN | Chip LED 1 · Ốc vít chip 4 · Dây đấu chip 0 · Dây cấp nguồn 70 · Nguồn 1 |
| L | D11_D15 | 200 | — | HKLED Dim 1 Cấp | DD11S200-3B3HT | Chip LED 4 · Ốc vít chip 32 · Dây đấu chip 140 · Lens 4 · Gioăng 4 · Ốc vít lens 64 · Dây cấp nguồn 70 · Nguồn 1 |
| M | D11_D15 | 300 | — | Philips Dim 1 Cấp | DD11S300-3B3PT | Dây đấu chip 270 · Nguồn 2 |
| N | D11_D15 | 100 | — | HKLED Nhỏ | DD11S100-3B3HN | Dây đấu chip 50 · Nguồn 2 |

Ca C và I kiểm đúng luật **ưu tiên chia hết** (`resolve_modulo_priority`):
600W nguồn to khác → chia 200 (không chia 250) ⇒ 3. Ca H: 300W nguồn to HKLED → chia 300 ⇒ 1.

## B. End-to-end "Tạo BOM Tự Động" — Claude đã chạy: 2/2 PASS

| Ca | Nội dung | Kỳ vọng | Kết quả |
|---|---|---|---|
| B1 | D11_D15 / DD11S200-3B3HT, 8 thành phần công thức + 1 cố định + 1 Theo Rule | BOM 10 dòng, đúng số lượng ca L | PASS |
| B2 | P01_P03 / DP01C050-3B3HN-D, 4 thành phần công thức + 1 cố định + 1 Theo Rule | BOM chỉ **4 dòng** — Cầu đấu (0) và Dây cấp nguồn (0) **bị bỏ hẳn** | PASS |
| B3 | Dọn dữ liệu test | Site về đúng 3 BOM ban đầu, 0 BOM Template, 0 item ZZTEST | PASS |

---

## B2. Luồng chính qua UI thật — Claude đã chạy bằng trình duyệt (31/07): PASS

Chạy trọn luồng trên Chrome (site dev, user thật): tạo BOM Template `ZZTEST-BT-UI-DD11`
(Mặt Hàng Cha DD11S200 → tự gợi ý `D11_D15`), 3 dòng đủ 3 kiểu thành phần, dialog Tạo Rule
chọn NVL cho "HKLED Dim 1 Cấp", Lưu, rồi sang Production Plan chọn `DD11S200-3B3HT` và bấm
nút **Tạo BOM Tự Động** ngoài grid.

| Đã kiểm qua UI | Kết quả |
|---|---|
| C2 — gợi ý Nhóm Công Thức theo prefix | PASS |
| C4/C5/C6 — ẩn/hiện Số Lượng + Mặt Hàng theo 3 kiểu thành phần (cả trong grid) | PASS |
| C7 — dialog Tạo Rule liệt kê đúng 9 giá trị Nguồn thật | PASS |
| C8 (1 giá trị) — sinh đúng 1 dòng Công Thức BOM | PASS |
| C11 — lưu template có Hoạt Động | PASS |
| C12 — nút Tạo BOM Tự Động: "Đã Tạo BOM Mới", BOM No tự điền, nội dung BOM đúng (Hộp carton 1 / Chip LED 4 / Nguồn 1) | PASS |
| C13 — bấm lần 2: "BOM Hiện Tại Hợp Lệ", không tạo BOM mới | PASS |

Ghi nhận thêm: khi chọn item chưa có BOM vào Production Plan, ERPNext lõi hiện thông báo
"Default BOM for ... not found" — hành vi chuẩn, không phải lỗi (nút Tạo BOM Tự Động sinh
BOM ngay sau đó). Toast "Valuation Rate not found" chỉ do NVL test không có giá.

**Người test vẫn cần chạy tay**: C3, C9, C10, C14, toàn bộ D (lỗi), E (sửa công thức
không cần deploy), F (regression), G (isolation). Dữ liệu test đã dọn sạch sau khi chạy.

---

## C. TC-HAPPY — Người test làm tay (luồng chính)

Chuẩn bị: tạo trước 3 item NVL tên `ZZTEST-NVL-A/B/C` (Nhóm hàng bất kỳ, có `standard_rate`).

| # | Bước | Kết quả mong đợi |
|---|---|---|
| C1 | Vào **BOM Rule Group** (Nhóm Công Thức) | Có đúng 6 bản ghi: P01_P03, D01_D05, PTX, XHB, DQL, D11_D15, kèm mô tả |
| C2 | Tạo BOM Template mới, chọn Mặt Hàng Cha = `DD11S200` | **Nhóm Công Thức tự điền `D11_D15`** |
| C3 | Đổi Mặt Hàng Cha sang `DP01S050-A` | Nhóm Công Thức **giữ nguyên giá trị cũ** (chỉ gợi ý khi đang trống) — xoá trắng rồi chọn lại thì mới gợi ý `P01_P03` |
| C4 | Dòng 1: Thành Phần BOM = `Hộp carton`, Kiểu = `Cố Định` | Hiện cả **Số Lượng** và **Mặt Hàng**, cả hai bắt buộc |
| ~~C5~~ | ~~Dòng 2: Thành Phần BOM = `Module`, Kiểu = `Số Lượng Theo Công Thức`~~ | **KHÔNG CÒN ÁP DỤNG từ 27/08** — kiểu này đã bỏ, ô chọn chỉ còn `Cố Định` và `Theo Rule` |
| C6 | Dòng 3: Thành Phần BOM = `Nguồn`, Kiểu = `Theo Rule` | **Ẩn cả** Số Lượng và Mặt Hàng; hiện nút **Tạo Rule** |
| C7 | Bấm **Tạo Rule** | Dialog "Tạo Rule — Chọn NVL theo Nguồn", liệt kê các giá trị `Nguồn` thật của item cha, mỗi giá trị 1 ô chọn Item |
| C8 | Chọn NVL cho 2 giá trị, bỏ trống phần còn lại → **Xác Nhận** | Alert "Đã thêm 2 dòng, cập nhật 0 dòng"; tab **Công Thức Thành Phần** có đúng 2 dòng |
| C9 | Bấm **Tạo Rule** lại | NVL đã chọn **hiện sẵn** đúng ô của nó |
| C10 | Đổi NVL 1 ô → Xác Nhận | Alert "…cập nhật 1 dòng"; **không** sinh dòng trùng |
| C11 | Tick **Hoạt Động**, đặt Mã BOM Template, Lưu | Lưu thành công |
| C12 | Production Plan → thêm biến thể của item cha vào bảng Select Items to Manufacture → bấm **Tạo BOM Tự Động** | Tạo BOM mới; số lượng khớp bảng mục A của nhóm tương ứng |
| C13 | Bấm **Tạo BOM Tự Động** lần 2 (không đổi gì) | Báo "BOM hiện tại hợp lệ", **không** tạo BOM mới |
| C14 | Sửa Số Lượng của dòng Cố Định trên BOM Template → Tạo BOM Tự Động lại | Tạo lại BOM và gán Default mới, BOM cũ bỏ Default |

## D. TC-ERROR — Thông báo lỗi phải rõ ràng

| # | Bước | Kết quả mong đợi |
|---|---|---|
| D1 | Bấm **Tạo Rule** khi chưa chọn Mặt Hàng Cha | "Vui lòng chọn Mặt Hàng Cha trước" |
| D2 | Bấm **Tạo Rule** khi chưa chọn Thành Phần BOM | "Vui lòng chọn Thành Phần BOM trước" |
| D3 | Mở dialog rồi **Xác Nhận** mà không chọn NVL nào | "Chưa chọn Nguyên Vật Liệu nào", dialog **không đóng** |
| D4 | Lưu BOM Template mà bỏ trống **Nhóm Công Thức** | Bị chặn (field bắt buộc) |
| D5 | Tạo BOM Tự Động cho biến thể có `Nguồn` **chưa** khai trong BOM Rule | "Chưa thiết lập NVL cho Nguồn: `<giá trị>`" |
| D6 | Tạo BOM Tự Động khi bảng thành phần có `Cầu đấu` mà nhóm là `D11_D15` | "Chưa cấu hình công thức Cầu đấu cho nhóm D11_D15" |
| D7 | Tạo BOM Tự Động cho biến thể của `DDQLC080` (template chưa khai Công suất) | "Mặt hàng … chưa khai báo đặc tính Công suất — không thể tính số lượng …" |
| D8 | Khai 2 dòng BOM Rule cùng (Thành Phần BOM, Giá Trị Điều Kiện) rồi Lưu | "Công Thức BOM bị trùng cho Thành Phần BOM … và Giá Trị Điều Kiện …" |
| D9 | Khai 2 dòng Bảng Thành Phần BOM cùng Thành Phần BOM rồi Lưu | Báo trùng Thành Phần BOM |
| D10 | Tick Hoạt Động cho template thứ 2 của cùng item cha | "Mặt hàng cha … đã có BOM Template … đang hoạt động" |
| D11 | `bench set-config -g server_script_enabled 0` rồi Tạo BOM Tự Động | "Server Script đang tắt nên không tính được công thức số lượng. Cần bật bằng: bench set-config -g server_script_enabled 1" — **nhớ bật lại sau khi test** |
| D12 | Production Plan: chọn item biến thể **chưa có BOM** vào Select Items to Manufacture | ERPNext lõi báo "Default BOM for `<item>` not found" — **hành vi chuẩn, KHÔNG log bug**. Đóng thông báo, bấm **Tạo BOM Tự Động** → BOM No được điền, không cần chọn lại item *(đã kiểm qua UI 31/07)* |
| D13 | Tạo BOM Tự Động với NVL **chưa có Valuation Rate** (item mới, chưa nhập kho/chưa có giá) | Hiện toast info "Valuation Rate not found for item ..." nhưng BOM **vẫn tạo thành công** — cảnh báo giá của ERPNext lõi, KHÔNG phải lỗi engine *(đã kiểm qua UI 31/07)*. Với item thật có giá thì không hiện |

## E. TC-Sửa-công-thức-không-cần-deploy (điểm cốt lõi của thiết kế)

| # | Bước | Kết quả mong đợi |
|---|---|---|
| E1 | Vào **Server Script** → `hkled_resolve_bom_qty` | Mở được, script_type = API, api_method = `hkled_resolve_bom_qty` |
| E2 | Sửa 1 hằng số trong công thức (VD `calc_lens_qty` chia 50 → chia 25) rồi **Save** | Lưu được, **không cần** bench build / restart |
| E3 | Tạo BOM Tự Động lại cho biến thể D11_D15 | Số lượng Lens đổi **ngay** theo công thức mới |
| E4 | Sửa trả lại giá trị gốc, Save | Về đúng số lượng cũ |
| E5 | Chạy `bench --site hkled.com migrate` | Script **KHÔNG bị ghi đè về bản gốc** (patch cố ý không overwrite) |
| E6 | Trong Server Script thử viết `import math` rồi Save | Bị chặn (sandbox không cho `import`) — đúng thiết kế |
| E7 | Trong Server Script thử dùng `"...{0}".format(x)` rồi chạy Tạo BOM Tự Động | Lỗi "format is an unsafe attribute" — RestrictedPython chặn `.format()`, phải dùng **f-string**. *(Bug thật đã gặp và sửa khi dev 31/07 — dòng này chống tái phát khi khách tự sửa công thức)* |

## F. TC-Regression-Core — Không được làm hỏng app lõi

| # | Bước | Kết quả mong đợi |
|---|---|---|
| F1 | Tạo **BOM tay** (không qua Tạo BOM Tự Động) cho 1 item bất kỳ | Bình thường như trước, không bị ảnh hưởng |
| F2 | Kiểm tra 3 BOM có sẵn trên site (`NVL 1..3`, `Thành phẩm 1/2`, `Bán thành phẩm 1/2`) | Vẫn còn, vẫn đúng Default, không bị engine mới đụng tới |
| F3 | Mở 3 Work Order có sẵn | Vẫn tham chiếu đúng BOM cũ |
| F4 | Work Order: nút **Tính Lại Lịch** (Phần III) | Vẫn chạy đúng, không bị ảnh hưởng bởi thay đổi Phần I |
| F5 | Employee: cảnh báo chưa gán Bậc Thợ (Phần II) | Vẫn hoạt động |
| F6 | Production Plan: các chức năng lõi khác (Get Items, Create Work Order…) | Bình thường |

## G. TC-Isolation — Không rò rỉ sang khách khác

| # | Bước | Kết quả mong đợi |
|---|---|---|
| G1 | Site `ailinh.com` / `tamdaimoc.com`: tìm DocType **BOM Rule Group**, **BOM Template** | **Không tồn tại** (app `mbwnext_hkled` không cài trên các site đó) |
| G2 | Site khác: danh sách **Server Script** | **Không có** `hkled_resolve_bom_qty` (Server Script là dữ liệu riêng từng site) |
| G3 | Site khác: form Item / Production Plan / Work Order | Không xuất hiện field hay nút nào của HKLED |
| G4 | Site khác: tính năng lõi (bán hàng, mua hàng, kho, kế toán) | Không bị ảnh hưởng bởi việc bật `server_script_enabled` toàn bench |

⚠️ Lưu ý G4: cờ `server_script_enabled` bật ở mức **toàn bench** (Frappe không cho bật riêng site).
Việc bật chỉ **cho phép** dùng Server Script, không tự tạo script nào ở site khác.

---

## H. Việc chưa test được — cần HKLED cung cấp dữ liệu

| # | Nội dung | Vì sao chưa test |
|---|---|---|
| H1 | Nhóm công thức cho `DNU1*` (5 template) và `DX01*` (5 template) | Chưa có công thức — chưa biết thuộc nhóm nào |
| H2 | Biến thể có `Nguồn` = "HKLED/Philips/Suncom Nguồn tròn" | Chưa có biến thể đèn nào dùng 3 giá trị này |
| H3 | Biến thể `P01_P03` Ngang trong khoảng 500 < CS ≤ 600 (Dây điện cấp nguồn) | Công thức đang tạm gán 100, chờ HKLED xác nhận |
| H4 | Quy tắc làm tròn khi công thức ra số lẻ | Đang dùng `ceil`, chờ xác nhận |
| H5 | Biến thể D11_D15 có công suất ngoài 6 mốc bảng tra | Hiện dữ liệu chỉ có đúng 6 mốc |
