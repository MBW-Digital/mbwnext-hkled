# Danh sách item cần sửa TÊN — PM-TASK-00061

Dữ liệu đã nạp đủ **1.516/1.516 dòng**, không có lỗi. Tài liệu này chỉ nói về **tên hiển thị**.

Số dòng ghi theo **đúng số dòng trong Google Sheet**.

## Tóm tắt

| Vấn đề | Số item | Ghi chú |
|---|---|---|
| A. Mặt hàng cha trùng tên y hệt với một biến thể của nó | 25 cặp | lỗi rõ ràng, sửa nhanh |
| B. Nhiều item hiện cùng một đoạn chữ trên danh sách | 1074 item / 182 nhóm | tên quá dài, phần phân biệt bị cắt |

## Vì sao không tự sắp xếp lại tên hộ được

Em đã thử mô phỏng 3 cách sắp xếp máy móc trên toàn bộ 1721 item, đếm xem còn bao nhiêu item bị trùng đoạn hiển thị:

| Cách làm | Còn trùng |
|---|---|
| giữ nguyên | 1074 item (62%) |
| bỏ đoạn 'Sử dụng: …' | 942 item (55%) |
| đảo phần riêng lên trước | 757 item (44%) |
| làm cả hai | 805 item (47%) |

Không cách nào đủ, vì bản thân phần phân biệt cũng dài và chỉ khác nhau ở đoạn cuối
(`… Bridgelux 3030, 5C, 30VDC, **50LED**` vs `… **64LED**`). Nên tên phải được **rút ngắn thật**,
và chỉ HKLED quyết được bỏ chữ nào.

Gợi ý dạng ngắn cho một dòng ở nhóm nặng nhất:

> hiện tại: `Module SMD 50W LED 3030 (Mẫu A) - Sử dụng: P01-03; D01-06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 5C, 30VDC, 50LED | Cầu đấ`

> gợi ý:  `Module SMD 50W 3030 Mẫu A · 3000K · Bridgelux · 5C · 30V · 50LED`

Phần *"Sử dụng: P01-03; D01-06; NCX"* nên chuyển xuống ô **Mô tả** — nó giống nhau ở mọi biến thể.

---

## A. Mặt hàng cha trùng tên với chính biến thể của nó — 25 cặp

Tên của mặt hàng cha đang mang một mức công suất cụ thể, trong khi cha bao trùm mọi công suất.

| Sheet | Dòng | Mã cha | Biến thể trùng tên | Tên hiện tại | Đề xuất |
|---|---|---|---|---|---|
| (V) Vỏ đèn | 190 | `VDD11` | `VDD11S050` | Vỏ đèn đường D11 Chip LED SMD Công suất 50W | Vỏ đèn đường D11 Chip LED SMD |
| (V) Vỏ đèn | 196 | `VDD12` | `VDD12S050` | Vỏ đèn đường D12 Chip LED SMD Công suất 50W | Vỏ đèn đường D12 Chip LED SMD |
| (V) Vỏ đèn | 202 | `VDD13` | `VDD13S050` | Vỏ đèn đường D13 Chip LED SMD Công suất 50W | Vỏ đèn đường D13 Chip LED SMD |
| (V) Vỏ đèn | 208 | `VDD14` | `VDD14S050` | Vỏ đèn đường D14 Chip LED SMD Công suất 50W | Vỏ đèn đường D14 Chip LED SMD |
| (V) Vỏ đèn | 214 | `VDD15` | `VDD15S050` | Vỏ đèn đường D15 Chip LED SMD Công suất 50W | Vỏ đèn đường D15 Chip LED SMD |
| (V) Vỏ đèn | 230 | `VDD21` | `VDD21S050` | Vỏ đèn đường D21 Chip LED SMD Công suất 50W | Vỏ đèn đường D21 Chip LED SMD |
| (V) Vỏ đèn | 235 | `VDD22` | `VDD22S050` | Vỏ đèn đường D22 Chip LED SMD Công suất 50W | Vỏ đèn đường D22 Chip LED SMD |
| (V) Vỏ đèn | 240 | `VDD23` | `VDD23S050` | Vỏ đèn đường D23 Chip LED SMD Công suất 50W | Vỏ đèn đường D23 Chip LED SMD |
| (V) Vỏ đèn | 245 | `VDD24` | `VDD24S050` | Vỏ đèn đường D24 Chip LED SMD Công suất 50W | Vỏ đèn đường D24 Chip LED SMD |
| (V) Vỏ đèn | 250 | `VDD25` | `VDD25S050` | Vỏ đèn đường D25 Chip LED SMD Công suất 50W | Vỏ đèn đường D25 Chip LED SMD |
| (V) Vỏ đèn | 255 | `VDD26` | `VDD26S050` | Vỏ đèn đường D26 Chip LED SMD Công suất 50W | Vỏ đèn đường D26 Chip LED SMD |
| (V) Vỏ đèn | 260 | `VDD7X` | `VDD71S150` | Vỏ đèn đường BRP371 Chip LED SMD Công suất 150W | Vỏ đèn đường BRP371 Chip LED SMD |
| (V) Vỏ đèn | 264 | `VDD9X` | `VDD91S100` | Vỏ đèn đường BRP391 Chip LED SMD Công suất 100W | Vỏ đèn đường BRP391 Chip LED SMD |
| (V) Vỏ đèn | 165 | `VDNCX` | `VDNCX-100` | Vỏ đèn phòng nổ cây xăng NCX Công suất 100W | Vỏ đèn phòng nổ cây xăng NCX |
| (V) Vỏ đèn | 157 | `VDNU1` | `VDNU1C050` | Vỏ đèn phòng nổ UFO NU1 Chip COB Công suất 50W | Vỏ đèn phòng nổ UFO NU1 Chip COB |
| (V) Vỏ đèn | 162 | `VDNU2` | `VDNU2S100` | Vỏ đèn phòng nổ UFO NU2 Chip SMD Công suất 100W | Vỏ đèn phòng nổ UFO NU2 Chip SMD |
| (V) Vỏ đèn | 124 | `VDPCT` | `VDPCTC500` | Vỏ đèn pha cẩu tháp PCT Chip COB Công suất 500W | Vỏ đèn pha cẩu tháp PCT Chip COB |
| (V) Vỏ đèn | 108 | `VDPKD` | `VDPKDC050` | Vỏ đèn pha kẻ dọc PKD Chip COB Công suất 50W | Vỏ đèn pha kẻ dọc PKD Chip COB |
| (V) Vỏ đèn | 127 | `VDPVD` | `VDPVDS200` | Vỏ đèn pha sân vận động PVD Chip SMD Công suất 200W | Vỏ đèn pha sân vận động PVD Chip SMD |
| (V) Vỏ đèn | 113 | `VDPVL` | `VDPVLC100` | Vỏ đèn pha viền mắt lồi hộp nguồn sau PVL Chip COB Công suất 100W | Vỏ đèn pha viền mắt lồi hộp nguồn sau PVL Chip COB |
| (V) Vỏ đèn | 92 | `VDPXH` | `VDPXHC010` | Vỏ đèn pha rọi xám hộp nguồn sau PXH Chip COB Công suất 10W | Vỏ đèn pha rọi xám hộp nguồn sau PXH Chip COB |
| (V) Vỏ đèn | 138 | `VDX01` | `VDX01S050` | Vỏ đèn nhà xưởng UFO X01 Công suất 50W | Vỏ đèn nhà xưởng UFO X01 |
| (V) Vỏ đèn | 148 | `VDX03` | `VDX03S100` | Vỏ đèn nhà xưởng UFO X03 Công suất 100W | Vỏ đèn nhà xưởng UFO X03 |
| (V) Vỏ đèn | 130 | `VDXHB` | `VDXHBC050` | Vỏ đèn nhà xưởng highbay XHB Công suất 50W | Vỏ đèn nhà xưởng highbay XHB |
| (V) Vỏ đèn | 152 | `VDXTT` | `VDXTTS050` | Vỏ đèn nhà xưởng thể thao XTT Công suất 50W | Vỏ đèn nhà xưởng thể thao XTT |

## B. Nhiều item hiện cùng một đoạn chữ — 182 nhóm

| Sheet | Số nhóm | Số item |
|---|---|---|
| (C) Chip LED | 83 | 661 |
| (V) Vỏ đèn | 50 | 137 |
| (PTN) Tản nhiệt | 16 | 67 |
| (M) Module | 10 | 140 |
| Linh phụ kiện gia công cơ khí | 9 | 18 |
| LED | 8 | 29 |
| (WPC) Cầu đấu | 6 | 22 |

### (M) Module — 41 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 50W LED 3030 (Mẫu A) - Sử dụng: P01-03; D01-…`

Dòng trong sheet: 10, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M30S050-3B5-5C-50LED-CD-A` | …06; NCX |
| `M30S050-3B5-5C-64LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 3030, 5C,  |
| `M30S050-3B5-5C-64LED-DD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 3030, 7C,  |
| `M30S050-3B5-7C-49LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 3030, 8C,  |
| `M30S050-3B5-8C-64LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 3030, 5C, 3 |
| `M30S050-3P3-5C-50LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 3030, 7C, 4 |
| `M30S050-3P3-5C-64LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 3030, 8C, 4 |
| `M30S050-3P3-5C-64LED-DD-A` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 50LED | |
| `M30S050-3P3-7C-49LED-CD-A` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 64LED | |
| `M30S050-3P3-8C-64LED-CD-A` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 7C, 42VDC, 49LED | |
| `M30S050-4B5-5C-50LED-CD-A` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 8C, 48VDC, 64LED | |
| `M30S050-4B5-5C-64LED-CD-A` | …06; NCX | Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 50LED |  |
| `M30S050-4B5-5C-64LED-DD-A` | …06; NCX | Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 64LED |  |
| `M30S050-4B5-7C-49LED-CD-A` | …06; NCX | Trắng (5.000K), Lumileds 3030, 7C, 42VDC, 49LED |  |
| `M30S050-4B5-8C-64LED-CD-A` | …06; NCX | Trắng (5.000K), Lumileds 3030, 8C, 48VDC, 64LED |  |
| `M30S050-4P3-5C-50LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 3030, 5C, 30VDC |
| `M30S050-4P3-5C-64LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 3030, 7C, 42VDC |
| `M30S050-4P3-5C-64LED-DD-A` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 3030, 8C, 48VDC |
| `M30S050-4P3-7C-49LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 3030, 5C, 30VDC, |
| `M30S050-4P3-8C-64LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 3030, 7C, 42VDC, |
| `M30S050-5B5-5C-50LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 3030, 8C, 48VDC, |
| `M30S050-5B5-5C-64LED-CD-A` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 5C, 30VDC, |
| `M30S050-5B5-5C-64LED-DD-A` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 7C, 42VDC, |
| `M30S050-5B5-7C-49LED-CD-A` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 8C, 48VDC, |
| `M30S050-5B5-8C-64LED-CD-A` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 3030, 5C, 30VDC,  |
| `M30S050-5P3-5C-50LED-CD-A` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 3030, 7C, 42VDC,  |
| `M30S050-5P3-5C-64LED-CD-A` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 3030, 8C, 48VDC,  |
| `M30S050-5P3-5C-64LED-DD-A` | … |
| `M30S050-5P3-7C-49LED-CD-A` | … |
| `M30S050-5P3-8C-64LED-CD-A` | … |
| `M30S050-6B5-5C-50LED-CD-A` | … |
| `M30S050-6B5-5C-64LED-CD-A` | … |
| `M30S050-6B5-5C-64LED-DD-A` | … |
| `M30S050-6B5-7C-49LED-CD-A` | … |
| `M30S050-6B5-8C-64LED-CD-A` | … |
| `M30S050-6P3-5C-50LED-CD-A` | … |
| `M30S050-6P3-5C-64LED-CD-A` | … |
| `M30S050-6P3-5C-64LED-DD-A` | … |
| `M30S050-6P3-7C-49LED-CD-A` | … |
| `M30S050-6P3-8C-64LED-CD-A` | … |
| `M30S050-A` | … |

### (M) Module — 41 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 50W LED 3030 (Mẫu B) - Sử dụng: P01-03; D01-…`

Dòng trong sheet: 58, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M30S050-3B5-5C-50LED-CD-B` | …06; NCX |
| `M30S050-3B5-5C-64LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 3030, 5C,  |
| `M30S050-3B5-5C-64LED-DD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 3030, 7C,  |
| `M30S050-3B5-7C-49LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 3030, 8C,  |
| `M30S050-3B5-8C-64LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 3030, 5C, 3 |
| `M30S050-3P3-5C-50LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 3030, 7C, 4 |
| `M30S050-3P3-5C-64LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 3030, 8C, 4 |
| `M30S050-3P3-5C-64LED-DD-B` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 50LED | |
| `M30S050-3P3-7C-49LED-CD-B` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 64LED | |
| `M30S050-3P3-8C-64LED-CD-B` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 7C, 42VDC, 49LED | |
| `M30S050-4B5-5C-50LED-CD-B` | …06; NCX | Trắng (5.000K), Bridgelux 3030, 8C, 48VDC, 64LED | |
| `M30S050-4B5-5C-64LED-CD-B` | …06; NCX | Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 50LED |  |
| `M30S050-4B5-5C-64LED-DD-B` | …06; NCX | Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 64LED |  |
| `M30S050-4B5-7C-49LED-CD-B` | …06; NCX | Trắng (5.000K), Lumileds 3030, 7C, 42VDC, 49LED |  |
| `M30S050-4B5-8C-64LED-CD-B` | …06; NCX | Trắng (5.000K), Lumileds 3030, 8C, 48VDC, 64LED |  |
| `M30S050-4P3-5C-50LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 3030, 5C, 30VDC |
| `M30S050-4P3-5C-64LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 3030, 7C, 42VDC |
| `M30S050-4P3-5C-64LED-DD-B` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 3030, 8C, 48VDC |
| `M30S050-4P3-7C-49LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 3030, 5C, 30VDC, |
| `M30S050-4P3-8C-64LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 3030, 7C, 42VDC, |
| `M30S050-5B5-5C-50LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 3030, 8C, 48VDC, |
| `M30S050-5B5-5C-64LED-CD-B` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 5C, 30VDC, |
| `M30S050-5B5-5C-64LED-DD-B` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 7C, 42VDC, |
| `M30S050-5B5-7C-49LED-CD-B` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 3030, 8C, 48VDC, |
| `M30S050-5B5-8C-64LED-CD-B` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 3030, 5C, 30VDC,  |
| `M30S050-5P3-5C-50LED-CD-B` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 3030, 7C, 42VDC,  |
| `M30S050-5P3-5C-64LED-CD-B` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 3030, 8C, 48VDC,  |
| `M30S050-5P3-5C-64LED-DD-B` | … |
| `M30S050-5P3-7C-49LED-CD-B` | … |
| `M30S050-5P3-8C-64LED-CD-B` | … |
| `M30S050-6B5-5C-50LED-CD-B` | … |
| `M30S050-6B5-5C-64LED-CD-B` | … |
| `M30S050-6B5-5C-64LED-DD-B` | … |
| `M30S050-6B5-7C-49LED-CD-B` | … |
| `M30S050-6B5-8C-64LED-CD-B` | … |
| `M30S050-6P3-5C-50LED-CD-B` | … |
| `M30S050-6P3-5C-64LED-CD-B` | … |
| `M30S050-6P3-5C-64LED-DD-B` | … |
| `M30S050-6P3-7C-49LED-CD-B` | … |
| `M30S050-6P3-8C-64LED-CD-B` | … |
| `M30S050-B` | … |

### (C) Chip LED — 33 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip Module SMD 50W LED 3030 - Sử dụng: Module SMD 50W;…`

Dòng trong sheet: 10, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `CM30S050` | … D11-15 |
| `CM30S050-3B3-5C-50LED` | … D11-15 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, |
| `CM30S050-3B3-5C-64LED` | … D11-15 | Trung tính (4.000K - 4.200K), Lumileds 3030, 50W,  |
| `CM30S050-3B3-7C-49LED` | … D11-15 | Trắng (5.000K), Bridgelux 3030, 50W, 5C, 30VDC, 50 |
| `CM30S050-3B3-8C-64LED` | … D11-15 | Trắng (5.000K), Bridgelux 3030, 50W, 5C, 30VDC, 64 |
| `CM30S050-3P3-5C-50LED` | … D11-15 | Trắng (5.000K), Bridgelux 3030, 50W, 7C, 42VDC, 49 |
| `CM30S050-3P3-5C-64LED` | … D11-15 | Trắng (5.000K), Bridgelux 3030, 50W, 8C, 48VDC, 64 |
| `CM30S050-3P3-7C-49LED` | … D11-15 | Trắng (5.000K), Lumileds 3030, 50W, 5C, 30VDC, 50L |
| `CM30S050-3P3-8C-64LED` | … D11-15 | Trắng (5.000K), Lumileds 3030, 50W, 5C, 30VDC, 64L |
| `CM30S050-4B3-5C-50LED` | … D11-15 | Trắng (5.000K), Lumileds 3030, 50W, 7C, 42VDC, 49L |
| `CM30S050-4B3-5C-64LED` | … D11-15 | Trắng (5.000K), Lumileds 3030, 50W, 8C, 48VDC, 64L |
| `CM30S050-4B3-7C-49LED` | … D11-15 | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5C,  |
| `CM30S050-4B3-8C-64LED` | … D11-15 | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 7C,  |
| `CM30S050-4P3-5C-50LED` | … D11-15 | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 8C,  |
| `CM30S050-4P3-5C-64LED` | … D11-15 | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5C, 3 |
| `CM30S050-4P3-7C-49LED` | … D11-15 | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 7C, 4 |
| `CM30S050-4P3-8C-64LED` | … D11-15 | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 8C, 4 |
| `CM30S050-5B3-5C-50LED` | … D11-15 | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5C, 3 |
| `CM30S050-5B3-5C-64LED` | … D11-15 | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 7C, 4 |
| `CM30S050-5B3-7C-49LED` | … D11-15 | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 8C, 4 |
| `CM30S050-5B3-8C-64LED` | … D11-15 | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5C, 30 |
| `CM30S050-5P3-5C-50LED` | … D11-15 | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 7C, 42 |
| `CM30S050-5P3-5C-64LED` | … D11-15 | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 8C, 48 |
| `CM30S050-5P3-7C-49LED` | … |
| `CM30S050-5P3-8C-64LED` | … |
| `CM30S050-6B3-5C-50LED` | … |
| `CM30S050-6B3-5C-64LED` | … |
| `CM30S050-6B3-7C-49LED` | … |
| `CM30S050-6B3-8C-64LED` | … |
| `CM30S050-6P3-5C-50LED` | … |
| `CM30S050-6P3-5C-64LED` | … |
| `CM30S050-6P3-7C-49LED` | … |
| `CM30S050-6P3-8C-64LED` | … |

### (C) Chip LED — 25 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 50W LED 3030 - Sử dụng: Các mẫu COB: PTC, PTR,…`

Dòng trong sheet: 93, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30C050` | … DQL,... |
| `C30C050-3B3-5C-49LED` | … DQL,... | Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W |
| `C30C050-3B3-5C-50LED` | … DQL,... | Trung tính (4.000K - 4.200K), Lumileds 3030, 50W, |
| `C30C050-3B3-7C-49LED` | … DQL,... | Trắng (5.000K), Bridgelux 3030, 50W, 5C, 30VDC, 4 |
| `C30C050-3P3-5C-49LED` | … DQL,... | Trắng (5.000K), Bridgelux 3030, 50W, 5C, 30VDC, 5 |
| `C30C050-3P3-5C-50LED` | … DQL,... | Trắng (5.000K), Bridgelux 3030, 50W, 7C, 42VDC, 4 |
| `C30C050-4B3-5C-49LED` | … DQL,... | Trắng (5.000K), Lumileds 3030, 50W, 5C, 30VDC, 49 |
| `C30C050-4B3-5C-50LED` | … DQL,... | Trắng (5.000K), Lumileds 3030, 50W, 5C, 30VDC, 50 |
| `C30C050-4B3-7C-49LED` | … DQL,... | Trắng (5.000K), Lumileds 3030, 50W, 7C, 42VDC, 49 |
| `C30C050-4P3-5C-49LED` | … DQL,... | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5C, |
| `C30C050-4P3-5C-50LED` | … DQL,... | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 7C, |
| `C30C050-4P3-7C-49LED` | … DQL,... | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5C,  |
| `C30C050-5B3-5C-49LED` | … DQL,... | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 7C,  |
| `C30C050-5B3-5C-50LED` | … DQL,... | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5C,  |
| `C30C050-5B3-7C-49LED` | … DQL,... | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 7C,  |
| `C30C050-5P3-5C-49LED` | … DQL,... | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5C, 3 |
| `C30C050-5P3-5C-50LED` | … DQL,... | Đổi màu, Bridgelux 3030, 50W |
| `C30C050-5P3-7C-49LED` | … |
| `C30C050-6B3-5C-49LED` | … |
| `C30C050-6B3-5C-50LED` | … |
| `C30C050-6B3-7C-49LED` | … |
| `C30C050-6P3-5C-49LED` | … |
| `C30C050-6P3-5C-50LED` | … |
| `C30C050-6P3-7C-49LED` | … |
| `C30C050-CB3` | … |

### (V) Vỏ đèn — 19 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường quạt (đèn đường lá) DQL Chip COB Công suất…`

Dòng trong sheet: 172, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDDQL` | … 100W | Chưa sơn |
| `VDDQLC030-BK` | … 100W | Xám |
| `VDDQLC030-GY` | … 100W | Đen |
| `VDDQLC030-NO` | … 150W | Chưa sơn |
| `VDDQLC050-BK` | … 150W | Xám |
| `VDDQLC050-GY` | … 150W | Đen |
| `VDDQLC050-NO` | … 200W | Chưa sơn |
| `VDDQLC100-BK` | … 200W | Xám |
| `VDDQLC100-GY` | … 200W | Đen |
| `VDDQLC100-NO` | … 250W | Chưa sơn |
| `VDDQLC150-BK` | … 250W | Xám |
| `VDDQLC150-GY` | … 250W | Đen |
| `VDDQLC150-NO` | … 30W |
| `VDDQLC200-BK` | … 30W | Chưa sơn |
| `VDDQLC200-GY` | … 30W | Xám |
| `VDDQLC200-NO` | … 30W | Đen |
| `VDDQLC250-BK` | … 50W | Chưa sơn |
| `VDDQLC250-GY` | … 50W | Xám |
| `VDDQLC250-NO` | … 50W | Đen |

### (M) Module — 16 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module COB 50W LED 3030 - Sử dụng: P01-03; D01-06; NCX …`

Dòng trong sheet: 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M30C050-3B5-5C-49LED-CD-A` | …| Trung tính (4.000K - 4.200K), Bridgelux 3030, 5C, 30VDC, 4 |
| `M30C050-3B5-5C-49LED-DD-A` | …| Trung tính (4.000K - 4.200K), Lumileds 3030, 5C, 30VDC, 49 |
| `M30C050-3P3-5C-49LED-CD-A` | …| Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 49LED | Cầu đấu |
| `M30C050-3P3-5C-49LED-DD-A` | …| Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 49LED | Dây điệ |
| `M30C050-4B5-5C-49LED-CD-A` | …| Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 49LED | Cầu đấu |
| `M30C050-4B5-5C-49LED-DD-A` | …| Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 49LED | Dây điện |
| `M30C050-4P3-5C-49LED-CD-A` | …| Trắng (6.000K - 6.500K), Bridgelux 3030, 5C, 30VDC, 49LED  |
| `M30C050-4P3-5C-49LED-DD-A` | …| Trắng (6.000K - 6.500K), Lumileds 3030, 5C, 30VDC, 49LED | |
| `M30C050-5B5-5C-49LED-CD-A` | …| Vàng (3.000K - 3.200K), Bridgelux 3030, 5C, 30VDC, 49LED | |
| `M30C050-5B5-5C-49LED-DD-A` | …| Vàng (3.000K - 3.200K), Lumileds 3030, 5C, 30VDC, 49LED |  |
| `M30C050-5P3-5C-49LED-CD-A` | … |
| `M30C050-5P3-5C-49LED-DD-A` | … |
| `M30C050-6B5-5C-49LED-CD-A` | … |
| `M30C050-6B5-5C-49LED-DD-A` | … |
| `M30C050-6P3-5C-49LED-CD-A` | … |
| `M30C050-6P3-5C-49LED-DD-A` | … |

### (C) Chip LED — 13 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 50W LED TF - Sử dụng: Các mẫu COB: PTC, PTR, D…`

Dòng trong sheet: 118, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `COBC050` | …QL,... |
| `COBC050-3TF-12VDC` | …QL,... | Trung tính (4.000K - 4.200K), TF, 50W, 12VDC |
| `COBC050-3TF-24VDC` | …QL,... | Trung tính (4.000K - 4.200K), TF, 50W, 24VDC |
| `COBC050-3TF-30VDC` | …QL,... | Trung tính (4.000K - 4.200K), TF, 50W, 30VDC |
| `COBC050-4TF-12VDC` | …QL,... | Trắng (6.000K - 6.500K), TF, 50W, 12VDC |
| `COBC050-4TF-24VDC` | …QL,... | Trắng (6.000K - 6.500K), TF, 50W, 24VDC |
| `COBC050-4TF-30VDC` | …QL,... | Trắng (6.000K - 6.500K), TF, 50W, 30VDC |
| `COBC050-6TF-12VDC` | …QL,... | Vàng (3.000K - 3.200K), TF, 50W, 12VDC |
| `COBC050-6TF-24VDC` | …QL,... | Vàng (3.000K - 3.200K), TF, 50W, 24VDC |
| `COBC050-6TF-30VDC` | …QL,... | Vàng (3.000K - 3.200K), TF, 50W, 30VDC |
| `COBC050-BTF-30VDC` | …QL,... | Xanh dương, TF, 50W, 30VDC |
| `COBC050-GTF-30VDC` | …QL,... | Xanh lá, TF, 50W, 30VDC |
| `COBC050-RTF-30VDC` | …QL,... | Đỏ, TF, 50W, 30VDC |

### (V) Vỏ đèn — 11 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha rọi xám hộp nguồn sau PXH Chip COB Công suất…`

Dòng trong sheet: 92, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPXH` | … 100W |
| `VDPXHC010` | … 10W |
| `VDPXHC020` | … 150W |
| `VDPXHC050` | … 200W |
| `VDPXHC100` | … 20W |
| `VDPXHC150` | … 300W | 2 hàng LED |
| `VDPXHC200` | … 30W |
| `VDPXHC300` | … 400W | 2 hàng LED |
| `VDPXHC300-2H` | … 500W | 2 hàng LED |
| `VDPXHC400-2H` | … 50W |
| `VDPXHC500-2H` | … |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 10W LED 3030 - Sử dụng: Các mẫu sử dụng chip C…`

Dòng trong sheet: 74, 74, 75, 76, 77, 78, 79, 80, 81

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30C010` | …OB 10W: PTR, PXH |
| `C30C010-3B3-5C-9LED` | …OB 10W: PTR, PXH | Trung tính (4.000K - 4.200K), Bridgelux 3 |
| `C30C010-3P3-5C-9LED` | …OB 10W: PTR, PXH | Trung tính (4.000K - 4.200K), Lumileds 30 |
| `C30C010-4B3-5C-9LED` | …OB 10W: PTR, PXH | Trắng (5.000K), Bridgelux 3030, 10W, 5C,  |
| `C30C010-4P3-5C-9LED` | …OB 10W: PTR, PXH | Trắng (5.000K), Lumileds 3030, 10W, 5C, 3 |
| `C30C010-5B3-5C-9LED` | …OB 10W: PTR, PXH | Trắng (6.000K - 6.500K), Bridgelux 3030,  |
| `C30C010-5P3-5C-9LED` | …OB 10W: PTR, PXH | Trắng (6.000K - 6.500K), Lumileds 3030, 1 |
| `C30C010-6B3-5C-9LED` | …OB 10W: PTR, PXH | Vàng (3.000K - 3.200K), Bridgelux 3030, 1 |
| `C30C010-6P3-5C-9LED` | …OB 10W: PTR, PXH | Vàng (3.000K - 3.200K), Lumileds 3030, 10 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 30W LED 3030 - Sử dụng: Các mẫu COB: PTC, PTR,…`

Dòng trong sheet: 82, 82, 83, 84, 85, 86, 87, 88, 89

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30C030` | … DQL,... |
| `C30C030-3B3-5C-30LED` | … DQL,... | Trung tính (4.000K - 4.200K), Bridgelux 3030, 30W |
| `C30C030-3P3-5C-30LED` | … DQL,... | Trung tính (4.000K - 4.200K), Lumileds 3030, 30W, |
| `C30C030-4B3-5C-30LED` | … DQL,... | Trắng (5.000K), Bridgelux 3030, 30W, 5C, 30VDC, 3 |
| `C30C030-4P3-5C-30LED` | … DQL,... | Trắng (5.000K), Lumileds 3030, 30W, 5C, 30VDC, 30 |
| `C30C030-5B3-5C-30LED` | … DQL,... | Trắng (6.000K - 6.500K), Bridgelux 3030, 30W, 5C, |
| `C30C030-5P3-5C-30LED` | … DQL,... | Trắng (6.000K - 6.500K), Lumileds 3030, 30W, 5C,  |
| `C30C030-6B3-5C-30LED` | … DQL,... | Vàng (3.000K - 3.200K), Bridgelux 3030, 30W, 5C,  |
| `C30C030-6P3-5C-30LED` | … DQL,... | Vàng (3.000K - 3.200K), Lumileds 3030, 30W, 5C, 3 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 3030 - Sử dụng: Đèn đường D22/D2…`

Dòng trong sheet: 248, 248, 249, 250, 251, 252, 253, 254, 255

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD2XS050` | …3/D25/D26 |
| `C30DD2XS050-3B3-5Cx2-96LED` | …3/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 50 |
| `C30DD2XS050-3P3-5Cx2-96LED` | …3/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 3030, 50W |
| `C30DD2XS050-4B3-5Cx2-96LED` | …3/D25/D26 | Trắng (5.000K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD2XS050-4P3-5Cx2-96LED` | …3/D25/D26 | Trắng (5.000K), Lumileds 3030, 50W, 5Cx2, 30VDC, |
| `C30DD2XS050-5B3-5Cx2-96LED` | …3/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5C |
| `C30DD2XS050-5P3-5Cx2-96LED` | …3/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5Cx |
| `C30DD2XS050-6B3-5Cx2-96LED` | …3/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5Cx |
| `C30DD2XS050-6P3-5Cx2-96LED` | …3/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5Cx2 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 3030 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 264, 264, 265, 266, 267, 268, 269, 270, 271

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD2XS100` | …23/D25/D26 |
| `C30DD2XS100-3B3-5Cx3-144LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 1 |
| `C30DD2XS100-3P3-5Cx3-144LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 3030, 10 |
| `C30DD2XS100-4B3-5Cx3-144LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 3030, 100W, 5Cx3, 30V |
| `C30DD2XS100-4P3-5Cx3-144LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 3030, 100W, 5Cx3, 30VD |
| `C30DD2XS100-5B3-5Cx3-144LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 3030, 100W,  |
| `C30DD2XS100-5P3-5Cx3-144LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 3030, 100W, 5 |
| `C30DD2XS100-6B3-5Cx3-144LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 3030, 100W, 5 |
| `C30DD2XS100-6P3-5Cx3-144LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 3030, 100W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 150W LED 3030 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 280, 280, 281, 282, 283, 284, 285, 286, 287

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD2XS150` | …23/D25/D26 |
| `C30DD2XS150-3B3-5Cx4-240LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 1 |
| `C30DD2XS150-3P3-5Cx4-240LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 3030, 15 |
| `C30DD2XS150-4B3-5Cx4-240LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 3030, 150W, 5Cx4, 30V |
| `C30DD2XS150-4P3-5Cx4-240LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 3030, 150W, 5Cx4, 30VD |
| `C30DD2XS150-5B3-5Cx4-240LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 3030, 150W,  |
| `C30DD2XS150-5P3-5Cx4-240LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 3030, 150W, 5 |
| `C30DD2XS150-6B3-5Cx4-240LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 3030, 150W, 5 |
| `C30DD2XS150-6P3-5Cx4-240LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 3030, 150W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 200W LED 3030 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 296, 296, 297, 298, 299, 300, 301, 302, 303

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD2XS200` | …23/D25/D26 |
| `C30DD2XS200-3B3-5Cx5-300LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 2 |
| `C30DD2XS200-3P3-5Cx5-300LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 3030, 20 |
| `C30DD2XS200-4B3-5Cx5-300LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 3030, 200W, 5Cx5, 30V |
| `C30DD2XS200-4P3-5Cx5-300LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 3030, 200W, 5Cx5, 30VD |
| `C30DD2XS200-5B3-5Cx5-300LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 3030, 200W,  |
| `C30DD2XS200-5P3-5Cx5-300LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 3030, 200W, 5 |
| `C30DD2XS200-6B3-5Cx5-300LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 3030, 200W, 5 |
| `C30DD2XS200-6P3-5Cx5-300LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 3030, 200W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 250W LED 3030 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 312, 312, 313, 314, 315, 316, 317, 318, 319

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD2XS250` | …23/D25/D26 |
| `C30DD2XS250-3B3-5Cx5-300LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 2 |
| `C30DD2XS250-3P3-5Cx5-300LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 3030, 25 |
| `C30DD2XS250-4B3-5Cx5-300LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 3030, 250W, 5Cx5, 30V |
| `C30DD2XS250-4P3-5Cx5-300LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 3030, 250W, 5Cx5, 30VD |
| `C30DD2XS250-5B3-5Cx5-300LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 3030, 250W,  |
| `C30DD2XS250-5P3-5Cx5-300LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 3030, 250W, 5 |
| `C30DD2XS250-6B3-5Cx5-300LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 3030, 250W, 5 |
| `C30DD2XS250-6P3-5Cx5-300LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 3030, 250W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 3030 - Sử dụng: Đèn đường BRP37X…`

Dòng trong sheet: 144, 144, 145, 146, 147, 148, 149, 150, 151

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD7XS050` | … |
| `C30DD7XS050-3B3-5C-48LED` | … | Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, 5C, 30 |
| `C30DD7XS050-3P3-5C-48LED` | … | Trung tính (4.000K - 4.200K), Lumileds 3030, 50W, 5C, 30V |
| `C30DD7XS050-4B3-5C-48LED` | … | Trắng (5.000K), Bridgelux 3030, 50W, 5C, 30VDC, 48LED |
| `C30DD7XS050-4P3-5C-48LED` | … | Trắng (5.000K), Lumileds 3030, 50W, 5C, 30VDC, 48LED |
| `C30DD7XS050-5B3-5C-48LED` | … | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5C, 30VDC,  |
| `C30DD7XS050-5P3-5C-48LED` | … | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5C, 30VDC, 4 |
| `C30DD7XS050-6B3-5C-48LED` | … | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5C, 30VDC, 4 |
| `C30DD7XS050-6P3-5C-48LED` | … | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5C, 30VDC, 48 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 3030 - Sử dụng: Đèn đường BRP39…`

Dòng trong sheet: 160, 160, 161, 162, 163, 164, 165, 166, 167

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD9XS100` | …X |
| `C30DD9XS100-3B3-5Cx2-100LED` | …X | Trung tính (4.000K - 4.200K), Bridgelux 3030, 100W, 5Cx2 |
| `C30DD9XS100-3P3-5Cx2-100LED` | …X | Trung tính (4.000K - 4.200K), Lumileds 3030, 100W, 5Cx2, |
| `C30DD9XS100-4B3-5Cx2-100LED` | …X | Trắng (5.000K), Bridgelux 3030, 100W, 5Cx2, 30VDC, 100LE |
| `C30DD9XS100-4P3-5Cx2-100LED` | …X | Trắng (5.000K), Lumileds 3030, 100W, 5Cx2, 30VDC, 100LED |
| `C30DD9XS100-5B3-5Cx2-100LED` | …X | Trắng (6.000K - 6.500K), Bridgelux 3030, 100W, 5Cx2, 30V |
| `C30DD9XS100-5P3-5Cx2-100LED` | …X | Trắng (6.000K - 6.500K), Lumileds 3030, 100W, 5Cx2, 30VD |
| `C30DD9XS100-6B3-5Cx2-100LED` | …X | Vàng (3.000K - 3.200K), Bridgelux 3030, 100W, 5Cx2, 30VD |
| `C30DD9XS100-6P3-5Cx2-100LED` | …X | Vàng (3.000K - 3.200K), Lumileds 3030, 100W, 5Cx2, 30VDC |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn phòng nổ 200W LED 3030 - Sử dụng: Pha phòng nổ…`

Dòng trong sheet: 604, 604, 605, 606, 607, 608, 609, 610, 611

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DNP1S200` | … SMD NP1 |
| `C30DNP1S200-3B3` | … SMD NP1 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 200 |
| `C30DNP1S200-3P3` | … SMD NP1 | Trung tính (4.000K - 4.200K), Lumileds 3030, 200W |
| `C30DNP1S200-4B3` | … SMD NP1 | Trắng (5.000K), Bridgelux 3030, 200W |
| `C30DNP1S200-4P3` | … SMD NP1 | Trắng (5.000K), Lumileds 3030, 200W |
| `C30DNP1S200-5B3` | … SMD NP1 | Trắng (6.000K - 6.500K), Bridgelux 3030, 200W |
| `C30DNP1S200-5P3` | … SMD NP1 | Trắng (6.000K - 6.500K), Lumileds 3030, 200W |
| `C30DNP1S200-6B3` | … SMD NP1 | Vàng (3.000K - 3.200K), Bridgelux 3030, 200W |
| `C30DNP1S200-6P3` | … SMD NP1 | Vàng (3.000K - 3.200K), Lumileds 3030, 200W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn phòng nổ 400W LED 3030 - Sử dụng: Pha phòng nổ…`

Dòng trong sheet: 612, 612, 613, 614, 615, 616, 617, 618, 619

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DNP1S400` | … SMD NP1 |
| `C30DNP1S400-3B3` | … SMD NP1 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 400 |
| `C30DNP1S400-3P3` | … SMD NP1 | Trung tính (4.000K - 4.200K), Lumileds 3030, 400W |
| `C30DNP1S400-4B3` | … SMD NP1 | Trắng (5.000K), Bridgelux 3030, 400W |
| `C30DNP1S400-4P3` | … SMD NP1 | Trắng (5.000K), Lumileds 3030, 400W |
| `C30DNP1S400-5B3` | … SMD NP1 | Trắng (6.000K - 6.500K), Bridgelux 3030, 400W |
| `C30DNP1S400-5P3` | … SMD NP1 | Trắng (6.000K - 6.500K), Lumileds 3030, 400W |
| `C30DNP1S400-6B3` | … SMD NP1 | Vàng (3.000K - 3.200K), Bridgelux 3030, 400W |
| `C30DNP1S400-6P3` | … SMD NP1 | Vàng (3.000K - 3.200K), Lumileds 3030, 400W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn phòng nổ 100W LED 3030 - Sử dụng: UFO phòng nổ…`

Dòng trong sheet: 572, 572, 573, 574, 575, 576, 577, 578, 579

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DNU2S100` | … SMD NU2 |
| `C30DNU2S100-3B3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 100 |
| `C30DNU2S100-3P3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Lumileds 3030, 100W |
| `C30DNU2S100-4B3` | … SMD NU2 | Trắng (5.000K), Bridgelux 3030, 100W |
| `C30DNU2S100-4P3` | … SMD NU2 | Trắng (5.000K), Lumileds 3030, 100W |
| `C30DNU2S100-5B3` | … SMD NU2 | Trắng (6.000K - 6.500K), Bridgelux 3030, 100W |
| `C30DNU2S100-5P3` | … SMD NU2 | Trắng (6.000K - 6.500K), Lumileds 3030, 100W |
| `C30DNU2S100-6B3` | … SMD NU2 | Vàng (3.000K - 3.200K), Bridgelux 3030, 100W |
| `C30DNU2S100-6P3` | … SMD NU2 | Vàng (3.000K - 3.200K), Lumileds 3030, 100W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn phòng nổ 150W LED 3030 - Sử dụng: UFO phòng nổ…`

Dòng trong sheet: 580, 580, 581, 582, 583, 584, 585, 586, 587

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DNU2S150` | … SMD NU2 |
| `C30DNU2S150-3B3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 150 |
| `C30DNU2S150-3P3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Lumileds 3030, 150W |
| `C30DNU2S150-4B3` | … SMD NU2 | Trắng (5.000K), Bridgelux 3030, 150W |
| `C30DNU2S150-4P3` | … SMD NU2 | Trắng (5.000K), Lumileds 3030, 150W |
| `C30DNU2S150-5B3` | … SMD NU2 | Trắng (6.000K - 6.500K), Bridgelux 3030, 150W |
| `C30DNU2S150-5P3` | … SMD NU2 | Trắng (6.000K - 6.500K), Lumileds 3030, 150W |
| `C30DNU2S150-6B3` | … SMD NU2 | Vàng (3.000K - 3.200K), Bridgelux 3030, 150W |
| `C30DNU2S150-6P3` | … SMD NU2 | Vàng (3.000K - 3.200K), Lumileds 3030, 150W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn phòng nổ 200W LED 3030 - Sử dụng: UFO phòng nổ…`

Dòng trong sheet: 588, 588, 589, 590, 591, 592, 593, 594, 595

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DNU2S200` | … SMD NU2 |
| `C30DNU2S200-3B3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 200 |
| `C30DNU2S200-3P3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Lumileds 3030, 200W |
| `C30DNU2S200-4B3` | … SMD NU2 | Trắng (5.000K), Bridgelux 3030, 200W |
| `C30DNU2S200-4P3` | … SMD NU2 | Trắng (5.000K), Lumileds 3030, 200W |
| `C30DNU2S200-5B3` | … SMD NU2 | Trắng (6.000K - 6.500K), Bridgelux 3030, 200W |
| `C30DNU2S200-5P3` | … SMD NU2 | Trắng (6.000K - 6.500K), Lumileds 3030, 200W |
| `C30DNU2S200-6B3` | … SMD NU2 | Vàng (3.000K - 3.200K), Bridgelux 3030, 200W |
| `C30DNU2S200-6P3` | … SMD NU2 | Vàng (3.000K - 3.200K), Lumileds 3030, 200W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn phòng nổ 250W LED 3030 - Sử dụng: UFO phòng nổ…`

Dòng trong sheet: 596, 596, 597, 598, 599, 600, 601, 602, 603

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DNU2S250` | … SMD NU2 |
| `C30DNU2S250-3B3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Bridgelux 3030, 250 |
| `C30DNU2S250-3P3` | … SMD NU2 | Trung tính (4.000K - 4.200K), Lumileds 3030, 250W |
| `C30DNU2S250-4B3` | … SMD NU2 | Trắng (5.000K), Bridgelux 3030, 250W |
| `C30DNU2S250-4P3` | … SMD NU2 | Trắng (5.000K), Lumileds 3030, 250W |
| `C30DNU2S250-5B3` | … SMD NU2 | Trắng (6.000K - 6.500K), Bridgelux 3030, 250W |
| `C30DNU2S250-5P3` | … SMD NU2 | Trắng (6.000K - 6.500K), Lumileds 3030, 250W |
| `C30DNU2S250-6B3` | … SMD NU2 | Vàng (3.000K - 3.200K), Bridgelux 3030, 250W |
| `C30DNU2S250-6P3` | … SMD NU2 | Vàng (3.000K - 3.200K), Lumileds 3030, 250W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 1000W LED 3030 - Sử dụng: Pha cầu cảng (PC…`

Dòng trong sheet: 528, 528, 529, 530, 531, 532, 533, 534, 535

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPCCC1K0` | …C) |
| `C30DPCCC1K0-3B3-5C-1380LED` | …C) | Trung tính (4.000K - 4.200K), Bridgelux 3030, 1000W, 5C |
| `C30DPCCC1K0-3P3-5C-1380LED` | …C) | Trung tính (4.000K - 4.200K), Lumileds 3030, 1000W, 5C, |
| `C30DPCCC1K0-4B3-5C-1380LED` | …C) | Trắng (5.000K), Bridgelux 3030, 1000W, 5C, 30VDC, 1380L |
| `C30DPCCC1K0-4P3-5C-1380LED` | …C) | Trắng (5.000K), Lumileds 3030, 1000W, 5C, 30VDC, 1380LE |
| `C30DPCCC1K0-5B3-5C-1380LED` | …C) | Trắng (6.000K - 6.500K), Bridgelux 3030, 1000W, 5C, 30V |
| `C30DPCCC1K0-5P3-5C-1380LED` | …C) | Trắng (6.000K - 6.500K), Lumileds 3030, 1000W, 5C, 30VD |
| `C30DPCCC1K0-6B3-5C-1380LED` | …C) | Vàng (3.000K - 3.200K), Bridgelux 3030, 1000W, 5C, 30VD |
| `C30DPCCC1K0-6P3-5C-1380LED` | …C) | Vàng (3.000K - 3.200K), Lumileds 3030, 1000W, 5C, 30VDC |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 400W LED 3030 - Sử dụng: Pha cầu cảng (PCC…`

Dòng trong sheet: 512, 512, 513, 514, 515, 516, 517, 518, 519

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPCCC400` | …) |
| `C30DPCCC400-3B3-5C-550LED` | …) | Trung tính (4.000K - 4.200K), Bridgelux 3030, 400W, 5C,  |
| `C30DPCCC400-3P3-5C-550LED` | …) | Trung tính (4.000K - 4.200K), Lumileds 3030, 400W, 5C, 3 |
| `C30DPCCC400-4B3-5C-550LED` | …) | Trắng (5.000K), Bridgelux 3030, 400W, 5C, 30VDC, 550LED |
| `C30DPCCC400-4P3-5C-550LED` | …) | Trắng (5.000K), Lumileds 3030, 400W, 5C, 30VDC, 550LED |
| `C30DPCCC400-5B3-5C-550LED` | …) | Trắng (6.000K - 6.500K), Bridgelux 3030, 400W, 5C, 30VDC |
| `C30DPCCC400-5P3-5C-550LED` | …) | Trắng (6.000K - 6.500K), Lumileds 3030, 400W, 5C, 30VDC, |
| `C30DPCCC400-6B3-5C-550LED` | …) | Vàng (3.000K - 3.200K), Bridgelux 3030, 400W, 5C, 30VDC, |
| `C30DPCCC400-6P3-5C-550LED` | …) | Vàng (3.000K - 3.200K), Lumileds 3030, 400W, 5C, 30VDC,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 600W LED 3030 - Sử dụng: Pha cầu cảng (PCC…`

Dòng trong sheet: 520, 520, 521, 522, 523, 524, 525, 526, 527

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPCCC600` | …) |
| `C30DPCCC600-3B3-5C-830LED` | …) | Trung tính (4.000K - 4.200K), Bridgelux 3030, 600W, 5C,  |
| `C30DPCCC600-3P3-5C-830LED` | …) | Trung tính (4.000K - 4.200K), Lumileds 3030, 600W, 5C, 3 |
| `C30DPCCC600-4B3-5C-830LED` | …) | Trắng (5.000K), Bridgelux 3030, 600W, 5C, 30VDC, 830LED |
| `C30DPCCC600-4P3-5C-830LED` | …) | Trắng (5.000K), Lumileds 3030, 600W, 5C, 30VDC, 830LED |
| `C30DPCCC600-5B3-5C-830LED` | …) | Trắng (6.000K - 6.500K), Bridgelux 3030, 600W, 5C, 30VDC |
| `C30DPCCC600-5P3-5C-830LED` | …) | Trắng (6.000K - 6.500K), Lumileds 3030, 600W, 5C, 30VDC, |
| `C30DPCCC600-6B3-5C-830LED` | …) | Vàng (3.000K - 3.200K), Bridgelux 3030, 600W, 5C, 30VDC, |
| `C30DPCCC600-6P3-5C-830LED` | …) | Vàng (3.000K - 3.200K), Lumileds 3030, 600W, 5C, 30VDC,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 1000W LED 3030 - Sử dụng: Pha cẩu tháp (PC…`

Dòng trong sheet: 544, 544, 545, 546, 547, 548, 549, 550, 551

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPCTC1K0` | …T) |
| `C30DPCTC1K0-3B3` | …T) | Trung tính (4.000K - 4.200K), Bridgelux 3030, 1000W |
| `C30DPCTC1K0-3P3` | …T) | Trung tính (4.000K - 4.200K), Lumileds 3030, 1000W |
| `C30DPCTC1K0-4B3` | …T) | Trắng (5.000K), Bridgelux 3030, 1000W |
| `C30DPCTC1K0-4P3` | …T) | Trắng (5.000K), Lumileds 3030, 1000W |
| `C30DPCTC1K0-5B3` | …T) | Trắng (6.000K - 6.500K), Bridgelux 3030, 1000W |
| `C30DPCTC1K0-5P3` | …T) | Trắng (6.000K - 6.500K), Lumileds 3030, 1000W |
| `C30DPCTC1K0-6B3` | …T) | Vàng (3.000K - 3.200K), Bridgelux 3030, 1000W |
| `C30DPCTC1K0-6P3` | …T) | Vàng (3.000K - 3.200K), Lumileds 3030, 1000W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 1500W LED 3030 - Sử dụng: Pha cẩu tháp (PC…`

Dòng trong sheet: 552, 552, 553, 554, 555, 556, 557, 558, 559

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPCTC1K5` | …T) |
| `C30DPCTC1K5-3B3` | …T) | Trung tính (4.000K - 4.200K), Bridgelux 3030, 1500W |
| `C30DPCTC1K5-3P3` | …T) | Trung tính (4.000K - 4.200K), Lumileds 3030, 1500W |
| `C30DPCTC1K5-4B3` | …T) | Trắng (5.000K), Bridgelux 3030, 1500W |
| `C30DPCTC1K5-4P3` | …T) | Trắng (5.000K), Lumileds 3030, 1500W |
| `C30DPCTC1K5-5B3` | …T) | Trắng (6.000K - 6.500K), Bridgelux 3030, 1500W |
| `C30DPCTC1K5-5P3` | …T) | Trắng (6.000K - 6.500K), Lumileds 3030, 1500W |
| `C30DPCTC1K5-6B3` | …T) | Vàng (3.000K - 3.200K), Bridgelux 3030, 1500W |
| `C30DPCTC1K5-6P3` | …T) | Vàng (3.000K - 3.200K), Lumileds 3030, 1500W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 500W LED 3030 - Sử dụng: Pha cẩu tháp (PCT…`

Dòng trong sheet: 536, 536, 537, 538, 539, 540, 541, 542, 543

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPCTC500` | …) |
| `C30DPCTC500-3B3` | …) | Trung tính (4.000K - 4.200K), Bridgelux 3030, 500W |
| `C30DPCTC500-3P3` | …) | Trung tính (4.000K - 4.200K), Lumileds 3030, 500W |
| `C30DPCTC500-4B3` | …) | Trắng (5.000K), Bridgelux 3030, 500W |
| `C30DPCTC500-4P3` | …) | Trắng (5.000K), Lumileds 3030, 500W |
| `C30DPCTC500-5B3` | …) | Trắng (6.000K - 6.500K), Bridgelux 3030, 500W |
| `C30DPCTC500-5P3` | …) | Trắng (6.000K - 6.500K), Lumileds 3030, 500W |
| `C30DPCTC500-6B3` | …) | Vàng (3.000K - 3.200K), Bridgelux 3030, 500W |
| `C30DPCTC500-6P3` | …) | Vàng (3.000K - 3.200K), Lumileds 3030, 500W |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 50W LED 3030 - Sử dụng: Đèn nhà thi …`

Dòng trong sheet: 472, 472, 473, 474, 475, 476, 477, 478, 479

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DXTTS050` | …đấu XTT |
| `C30DXTTS050-3B3-8C-63LED` | …đấu XTT | Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, |
| `C30DXTTS050-3P3-8C-63LED` | …đấu XTT | Trung tính (4.000K - 4.200K), Lumileds 3030, 50W,  |
| `C30DXTTS050-4B3-8C-63LED` | …đấu XTT | Trắng (5.000K), Bridgelux 3030, 50W, 8C, 48VDC, 63 |
| `C30DXTTS050-4P3-8C-63LED` | …đấu XTT | Trắng (5.000K), Lumileds 3030, 50W, 8C, 48VDC, 63L |
| `C30DXTTS050-5B3-8C-63LED` | …đấu XTT | Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 8C,  |
| `C30DXTTS050-5P3-8C-63LED` | …đấu XTT | Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 8C, 4 |
| `C30DXTTS050-6B3-8C-63LED` | …đấu XTT | Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 8C, 4 |
| `C30DXTTS050-6P3-8C-63LED` | …đấu XTT | Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 8C, 48 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 100W LED 3030 - Sử dụng: Đèn nhà thi…`

Dòng trong sheet: 480, 480, 481, 482, 483, 484, 485, 486, 487

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DXTTS100` | … đấu XTT |
| `C30DXTTS100-3B3-8C-105LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Bridgelux 3030, 100 |
| `C30DXTTS100-3P3-8C-105LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Lumileds 3030, 100W |
| `C30DXTTS100-4B3-8C-105LED` | … đấu XTT | Trắng (5.000K), Bridgelux 3030, 100W, 8C, 48VDC,  |
| `C30DXTTS100-4P3-8C-105LED` | … đấu XTT | Trắng (5.000K), Lumileds 3030, 100W, 8C, 48VDC, 1 |
| `C30DXTTS100-5B3-8C-105LED` | … đấu XTT | Trắng (6.000K - 6.500K), Bridgelux 3030, 100W, 8C |
| `C30DXTTS100-5P3-8C-105LED` | … đấu XTT | Trắng (6.000K - 6.500K), Lumileds 3030, 100W, 8C, |
| `C30DXTTS100-6B3-8C-105LED` | … đấu XTT | Vàng (3.000K - 3.200K), Bridgelux 3030, 100W, 8C, |
| `C30DXTTS100-6P3-8C-105LED` | … đấu XTT | Vàng (3.000K - 3.200K), Lumileds 3030, 100W, 8C,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 150W LED 3030 - Sử dụng: Đèn nhà thi…`

Dòng trong sheet: 488, 488, 489, 490, 491, 492, 493, 494, 495

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DXTTS150` | … đấu XTT |
| `C30DXTTS150-3B3-8C-154LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Bridgelux 3030, 150 |
| `C30DXTTS150-3P3-8C-154LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Lumileds 3030, 150W |
| `C30DXTTS150-4B3-8C-154LED` | … đấu XTT | Trắng (5.000K), Bridgelux 3030, 150W, 8C, 48VDC,  |
| `C30DXTTS150-4P3-8C-154LED` | … đấu XTT | Trắng (5.000K), Lumileds 3030, 150W, 8C, 48VDC, 1 |
| `C30DXTTS150-5B3-8C-154LED` | … đấu XTT | Trắng (6.000K - 6.500K), Bridgelux 3030, 150W, 8C |
| `C30DXTTS150-5P3-8C-154LED` | … đấu XTT | Trắng (6.000K - 6.500K), Lumileds 3030, 150W, 8C, |
| `C30DXTTS150-6B3-8C-154LED` | … đấu XTT | Vàng (3.000K - 3.200K), Bridgelux 3030, 150W, 8C, |
| `C30DXTTS150-6P3-8C-154LED` | … đấu XTT | Vàng (3.000K - 3.200K), Lumileds 3030, 150W, 8C,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 200W LED 3030 - Sử dụng: Đèn nhà thi…`

Dòng trong sheet: 496, 496, 497, 498, 499, 500, 501, 502, 503

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DXTTS200` | … đấu XTT |
| `C30DXTTS200-3B3-8C-203LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Bridgelux 3030, 200 |
| `C30DXTTS200-3P3-8C-203LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Lumileds 3030, 200W |
| `C30DXTTS200-4B3-8C-203LED` | … đấu XTT | Trắng (5.000K), Bridgelux 3030, 200W, 8C, 48VDC,  |
| `C30DXTTS200-4P3-8C-203LED` | … đấu XTT | Trắng (5.000K), Lumileds 3030, 200W, 8C, 48VDC, 2 |
| `C30DXTTS200-5B3-8C-203LED` | … đấu XTT | Trắng (6.000K - 6.500K), Bridgelux 3030, 200W, 8C |
| `C30DXTTS200-5P3-8C-203LED` | … đấu XTT | Trắng (6.000K - 6.500K), Lumileds 3030, 200W, 8C, |
| `C30DXTTS200-6B3-8C-203LED` | … đấu XTT | Vàng (3.000K - 3.200K), Bridgelux 3030, 200W, 8C, |
| `C30DXTTS200-6P3-8C-203LED` | … đấu XTT | Vàng (3.000K - 3.200K), Lumileds 3030, 200W, 8C,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 250W LED 3030 - Sử dụng: Đèn nhà thi…`

Dòng trong sheet: 504, 504, 505, 506, 507, 508, 509, 510, 511

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DXTTS250` | … đấu XTT |
| `C30DXTTS250-3B3-8C-252LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Bridgelux 3030, 250 |
| `C30DXTTS250-3P3-8C-252LED` | … đấu XTT | Trung tính (4.000K - 4.200K), Lumileds 3030, 250W |
| `C30DXTTS250-4B3-8C-252LED` | … đấu XTT | Trắng (5.000K), Bridgelux 3030, 250W, 8C, 48VDC,  |
| `C30DXTTS250-4P3-8C-252LED` | … đấu XTT | Trắng (5.000K), Lumileds 3030, 250W, 8C, 48VDC, 2 |
| `C30DXTTS250-5B3-8C-252LED` | … đấu XTT | Trắng (6.000K - 6.500K), Bridgelux 3030, 250W, 8C |
| `C30DXTTS250-5P3-8C-252LED` | … đấu XTT | Trắng (6.000K - 6.500K), Lumileds 3030, 250W, 8C, |
| `C30DXTTS250-6B3-8C-252LED` | … đấu XTT | Vàng (3.000K - 3.200K), Bridgelux 3030, 250W, 8C, |
| `C30DXTTS250-6P3-8C-252LED` | … đấu XTT | Vàng (3.000K - 3.200K), Lumileds 3030, 250W, 8C,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 100W LED 5050 - Sử dụng: Các mẫu COB: PTC, PTR…`

Dòng trong sheet: 136, 136, 137, 138, 139, 140, 141, 142, 143

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50C100` | …, DQL,... |
| `C50C100-3B5-5C-20LED` | …, DQL,... | Trung tính (4.000K - 4.200K), Bridgelux 5050, 10 |
| `C50C100-3P5-5C-20LED` | …, DQL,... | Trung tính (4.000K - 4.200K), Lumileds 5050, 100 |
| `C50C100-4B5-5C-20LED` | …, DQL,... | Trắng (5.000K), Bridgelux 5050, 100W, 5C, 30VDC, |
| `C50C100-4P5-5C-20LED` | …, DQL,... | Trắng (5.000K), Lumileds 5050, 100W, 5C, 30VDC,  |
| `C50C100-5B5-5C-20LED` | …, DQL,... | Trắng (6.000K - 6.500K), Bridgelux 5050, 100W, 5 |
| `C50C100-5P5-5C-20LED` | …, DQL,... | Trắng (6.000K - 6.500K), Lumileds 5050, 100W, 5C |
| `C50C100-6B5-5C-20LED` | …, DQL,... | Vàng (3.000K - 3.200K), Bridgelux 5050, 100W, 5C |
| `C50C100-6P5-5C-20LED` | …, DQL,... | Vàng (3.000K - 3.200K), Lumileds 5050, 100W, 5C, |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 5050 - Sử dụng: Đèn đường D22/D2…`

Dòng trong sheet: 256, 256, 257, 258, 259, 260, 261, 262, 263

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD2XS050` | …3/D25/D26 |
| `C50DD2XS050-3B5-5Cx2-24LED` | …3/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 5050, 50 |
| `C50DD2XS050-3P5-5Cx2-24LED` | …3/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 5050, 50W |
| `C50DD2XS050-4B5-5Cx2-24LED` | …3/D25/D26 | Trắng (5.000K), Bridgelux 5050, 50W, 5Cx2, 30VDC |
| `C50DD2XS050-4P5-5Cx2-24LED` | …3/D25/D26 | Trắng (5.000K), Lumileds 5050, 50W, 5Cx2, 30VDC, |
| `C50DD2XS050-5B5-5Cx2-24LED` | …3/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 5050, 50W, 5C |
| `C50DD2XS050-5P5-5Cx2-24LED` | …3/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 5050, 50W, 5Cx |
| `C50DD2XS050-6B5-5Cx2-24LED` | …3/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 5050, 50W, 5Cx |
| `C50DD2XS050-6P5-5Cx2-24LED` | …3/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 5050, 50W, 5Cx2 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 5050 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 272, 272, 273, 274, 275, 276, 277, 278, 279

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD2XS100` | …23/D25/D26 |
| `C50DD2XS100-3B5-5Cx3-36LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 5050, 1 |
| `C50DD2XS100-3P5-5Cx3-36LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 5050, 10 |
| `C50DD2XS100-4B5-5Cx3-36LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 5050, 100W, 5Cx3, 30V |
| `C50DD2XS100-4P5-5Cx3-36LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 5050, 100W, 5Cx3, 30VD |
| `C50DD2XS100-5B5-5Cx3-36LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 5050, 100W,  |
| `C50DD2XS100-5P5-5Cx3-36LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 5050, 100W, 5 |
| `C50DD2XS100-6B5-5Cx3-36LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 5050, 100W, 5 |
| `C50DD2XS100-6P5-5Cx3-36LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 5050, 100W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 150W LED 5050 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 288, 288, 289, 290, 291, 292, 293, 294, 295

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD2XS150` | …23/D25/D26 |
| `C50DD2XS150-3B5-5Cx4-60LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 5050, 1 |
| `C50DD2XS150-3P5-5Cx4-60LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 5050, 15 |
| `C50DD2XS150-4B5-5Cx4-60LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 5050, 150W, 5Cx4, 30V |
| `C50DD2XS150-4P5-5Cx4-60LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 5050, 150W, 5Cx4, 30VD |
| `C50DD2XS150-5B5-5Cx4-60LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 5050, 150W,  |
| `C50DD2XS150-5P5-5Cx4-60LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 5050, 150W, 5 |
| `C50DD2XS150-6B5-5Cx4-60LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 5050, 150W, 5 |
| `C50DD2XS150-6P5-5Cx4-60LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 5050, 150W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 200W LED 5050 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 304, 304, 305, 306, 307, 308, 309, 310, 311

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD2XS200` | …23/D25/D26 |
| `C50DD2XS200-3B5-5Cx5-76LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 5050, 2 |
| `C50DD2XS200-3P5-5Cx5-76LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 5050, 20 |
| `C50DD2XS200-4B5-5Cx5-76LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 5050, 200W, 5Cx5, 30V |
| `C50DD2XS200-4P5-5Cx5-76LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 5050, 200W, 5Cx5, 30VD |
| `C50DD2XS200-5B5-5Cx5-76LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 5050, 200W,  |
| `C50DD2XS200-5P5-5Cx5-76LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 5050, 200W, 5 |
| `C50DD2XS200-6B5-5Cx5-76LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 5050, 200W, 5 |
| `C50DD2XS200-6P5-5Cx5-76LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 5050, 200W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 250W LED 5050 - Sử dụng: Đèn đường D22/D…`

Dòng trong sheet: 320, 320, 321, 322, 323, 324, 325, 326, 327

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD2XS250` | …23/D25/D26 |
| `C50DD2XS250-3B5-5Cx5-76LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Bridgelux 5050, 2 |
| `C50DD2XS250-3P5-5Cx5-76LED` | …23/D25/D26 | Trung tính (4.000K - 4.200K), Lumileds 5050, 25 |
| `C50DD2XS250-4B5-5Cx5-76LED` | …23/D25/D26 | Trắng (5.000K), Bridgelux 5050, 250W, 5Cx5, 30V |
| `C50DD2XS250-4P5-5Cx5-76LED` | …23/D25/D26 | Trắng (5.000K), Lumileds 5050, 250W, 5Cx5, 30VD |
| `C50DD2XS250-5B5-5Cx5-76LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Bridgelux 5050, 250W,  |
| `C50DD2XS250-5P5-5Cx5-76LED` | …23/D25/D26 | Trắng (6.000K - 6.500K), Lumileds 5050, 250W, 5 |
| `C50DD2XS250-6B5-5Cx5-76LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Bridgelux 5050, 250W, 5 |
| `C50DD2XS250-6P5-5Cx5-76LED` | …23/D25/D26 | Vàng (3.000K - 3.200K), Lumileds 5050, 250W, 5C |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 5050 - Sử dụng: Đèn đường BRP37X…`

Dòng trong sheet: 152, 152, 153, 154, 155, 156, 157, 158, 159

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD7XS050` | … |
| `C50DD7XS050-3B5-5C-16LED` | … | Trung tính (4.000K - 4.200K), Bridgelux 5050, 50W, 5C, 30 |
| `C50DD7XS050-3P5-5C-16LED` | … | Trung tính (4.000K - 4.200K), Lumileds 5050, 50W, 5C, 30V |
| `C50DD7XS050-4B5-5C-16LED` | … | Trắng (5.000K), Bridgelux 5050, 50W, 5C, 30VDC, 16LED |
| `C50DD7XS050-4P5-5C-16LED` | … | Trắng (5.000K), Lumileds 5050, 50W, 5C, 30VDC, 16LED |
| `C50DD7XS050-5B5-5C-16LED` | … | Trắng (6.000K - 6.500K), Bridgelux 5050, 50W, 5C, 30VDC,  |
| `C50DD7XS050-5P5-5C-16LED` | … | Trắng (6.000K - 6.500K), Lumileds 5050, 50W, 5C, 30VDC, 1 |
| `C50DD7XS050-6B5-5C-16LED` | … | Vàng (3.000K - 3.200K), Bridgelux 5050, 50W, 5C, 30VDC, 1 |
| `C50DD7XS050-6P5-5C-16LED` | … | Vàng (3.000K - 3.200K), Lumileds 5050, 50W, 5C, 30VDC, 16 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip Module SMD 30W LED 3030 - Sử dụng: Module SMD 10W,…`

Dòng trong sheet: 2, 2, 3, 4, 5, 6, 7, 8, 9

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `CM30S030` | … 20W, 30W |
| `CM30S030-3B3-5C-30LED` | … 20W, 30W | Trung tính (4.000K - 4.200K), Bridgelux 3030, 30 |
| `CM30S030-3P3-5C-30LED` | … 20W, 30W | Trung tính (4.000K - 4.200K), Lumileds 3030, 30W |
| `CM30S030-4B3-5C-30LED` | … 20W, 30W | Trắng (5.000K), Bridgelux 3030, 30W, 5C, 30VDC,  |
| `CM30S030-4P3-5C-30LED` | … 20W, 30W | Trắng (5.000K), Lumileds 3030, 30W, 5C, 30VDC, 3 |
| `CM30S030-5B3-5C-30LED` | … 20W, 30W | Trắng (6.000K - 6.500K), Bridgelux 3030, 30W, 5C |
| `CM30S030-5P3-5C-30LED` | … 20W, 30W | Trắng (6.000K - 6.500K), Lumileds 3030, 30W, 5C, |
| `CM30S030-6B3-5C-30LED` | … 20W, 30W | Vàng (3.000K - 3.200K), Bridgelux 3030, 30W, 5C, |
| `CM30S030-6P3-5C-30LED` | … 20W, 30W | Vàng (3.000K - 3.200K), Lumileds 3030, 30W, 5C,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip Module SMD 200W LED 3030 - Sử dụng: Module SMD 200…`

Dòng trong sheet: 58, 58, 59, 60, 61, 62, 63, 64, 65

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `CM30S200` | …W |
| `CM30S200-3B3-5C-288LED` | …W | Trung tính (4.000K - 4.200K), Bridgelux 3030, 200W, 5C,  |
| `CM30S200-3P3-5C-288LED` | …W | Trung tính (4.000K - 4.200K), Lumileds 3030, 200W, 5C, 3 |
| `CM30S200-4B3-5C-288LED` | …W | Trắng (5.000K), Bridgelux 3030, 200W, 5C, 30VDC, 288LED |
| `CM30S200-4P3-5C-288LED` | …W | Trắng (5.000K), Lumileds 3030, 200W, 5C, 30VDC, 288LED |
| `CM30S200-5B3-5C-288LED` | …W | Trắng (6.000K - 6.500K), Bridgelux 3030, 200W, 5C, 30VDC |
| `CM30S200-5P3-5C-288LED` | …W | Trắng (6.000K - 6.500K), Lumileds 3030, 200W, 5C, 30VDC, |
| `CM30S200-6B3-5C-288LED` | …W | Vàng (3.000K - 3.200K), Bridgelux 3030, 200W, 5C, 30VDC, |
| `CM30S200-6P3-5C-288LED` | …W | Vàng (3.000K - 3.200K), Lumileds 3030, 200W, 5C, 30VDC,  |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip Module SMD 50W LED 5050 - Sử dụng: Module SMD 50W;…`

Dòng trong sheet: 42, 42, 43, 44, 45, 46, 47, 48, 49

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `CM50S050` | … D11-15 |
| `CM50S050-3B5-5C-16LED` | … D11-15 | Trung tính (4.000K - 4.200K), Bridgelux 5050, 50W, |
| `CM50S050-3P5-5C-16LED` | … D11-15 | Trung tính (4.000K - 4.200K), Lumileds 5050, 50W,  |
| `CM50S050-4B5-5C-16LED` | … D11-15 | Trắng (5.000K), Bridgelux 5050, 50W, 5C, 30VDC, 16 |
| `CM50S050-4P5-5C-16LED` | … D11-15 | Trắng (5.000K), Lumileds 5050, 50W, 5C, 30VDC, 16L |
| `CM50S050-5B5-5C-16LED` | … D11-15 | Trắng (6.000K - 6.500K), Bridgelux 5050, 50W, 5C,  |
| `CM50S050-5P5-5C-16LED` | … D11-15 | Trắng (6.000K - 6.500K), Lumileds 5050, 50W, 5C, 3 |
| `CM50S050-6B5-5C-16LED` | … D11-15 | Vàng (3.000K - 3.200K), Bridgelux 5050, 50W, 5C, 3 |
| `CM50S050-6P5-5C-16LED` | … D11-15 | Vàng (3.000K - 3.200K), Lumileds 5050, 50W, 5C, 30 |

### (C) Chip LED — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip Module SMD 200W LED 5050 - Sử dụng: Module SMD 200…`

Dòng trong sheet: 66, 66, 67, 68, 69, 70, 71, 72, 73

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `CM50S200` | …W |
| `CM50S200-3B5-5C-72LED` | …W | Trung tính (4.000K - 4.200K), Bridgelux 5050, 200W, 5C,  |
| `CM50S200-3P5-5C-72LED` | …W | Trung tính (4.000K - 4.200K), Lumileds 5050, 200W, 5C, 3 |
| `CM50S200-4B5-5C-72LED` | …W | Trắng (5.000K), Bridgelux 5050, 200W, 5C, 30VDC, 72LED |
| `CM50S200-4P5-5C-72LED` | …W | Trắng (5.000K), Lumileds 5050, 200W, 5C, 30VDC, 72LED |
| `CM50S200-5B5-5C-72LED` | …W | Trắng (6.000K - 6.500K), Bridgelux 5050, 200W, 5C, 30VDC |
| `CM50S200-5P5-5C-72LED` | …W | Trắng (6.000K - 6.500K), Lumileds 5050, 200W, 5C, 30VDC, |
| `CM50S200-6B5-5C-72LED` | …W | Vàng (3.000K - 3.200K), Bridgelux 5050, 200W, 5C, 30VDC, |
| `CM50S200-6P5-5C-72LED` | …W | Vàng (3.000K - 3.200K), Lumileds 5050, 200W, 5C, 30VDC,  |

### (M) Module — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 50W LED 5050 (Mẫu A) - Sử dụng: P01-03; D01-…`

Dòng trong sheet: 50, 50, 51, 52, 53, 54, 55, 56, 57

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M50S050-3B5-5C-16LED-CD-A` | …06; NCX |
| `M50S050-3P5-5C-16LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 5050, 5C,  |
| `M50S050-4B5-5C-16LED-CD-A` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 5050, 5C, 3 |
| `M50S050-4P5-5C-16LED-CD-A` | …06; NCX | Trắng (5.000K), Bridgelux 5050, 5C, 30VDC, 16LED | |
| `M50S050-5B5-5C-16LED-CD-A` | …06; NCX | Trắng (5.000K), Lumileds 5050, 5C, 30VDC, 16LED |  |
| `M50S050-5P5-5C-16LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 5050, 5C, 30VDC |
| `M50S050-6B5-5C-16LED-CD-A` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 5050, 5C, 30VDC, |
| `M50S050-6P5-5C-16LED-CD-A` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 5050, 5C, 30VDC, |
| `M50S050-A` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 5050, 5C, 30VDC,  |

### (M) Module — 9 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 50W LED 5050 (Mẫu B) - Sử dụng: P01-03; D01-…`

Dòng trong sheet: 98, 98, 99, 100, 101, 102, 103, 104, 105

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M50S050-3B5-5C-16LED-CD-B` | …06; NCX |
| `M50S050-3P5-5C-16LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Bridgelux 5050, 5C,  |
| `M50S050-4B5-5C-16LED-CD-B` | …06; NCX | Trung tính (4.000K - 4.200K), Lumileds 5050, 5C, 3 |
| `M50S050-4P5-5C-16LED-CD-B` | …06; NCX | Trắng (5.000K), Bridgelux 5050, 5C, 30VDC, 16LED | |
| `M50S050-5B5-5C-16LED-CD-B` | …06; NCX | Trắng (5.000K), Lumileds 5050, 5C, 30VDC, 16LED |  |
| `M50S050-5P5-5C-16LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Bridgelux 5050, 5C, 30VDC |
| `M50S050-6B5-5C-16LED-CD-B` | …06; NCX | Trắng (6.000K - 6.500K), Lumileds 5050, 5C, 30VDC, |
| `M50S050-6P5-5C-16LED-CD-B` | …06; NCX | Vàng (3.000K - 3.200K), Bridgelux 5050, 5C, 30VDC, |
| `M50S050-B` | …06; NCX | Vàng (3.000K - 3.200K), Lumileds 5050, 5C, 30VDC,  |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 3030 - Sử dụng: Đèn đường D20 | …`

Dòng trong sheet: 168, 169, 170, 171, 172, 173, 174, 175

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD20S050-3B3-5Cx2-96LED` | …Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, 5Cx2, 30V |
| `C30DD20S050-3P3-5Cx2-96LED` | …Trung tính (4.000K - 4.200K), Lumileds 3030, 50W, 5Cx2, 30VD |
| `C30DD20S050-4B3-5Cx2-96LED` | …Trắng (5.000K), Bridgelux 3030, 50W, 5Cx2, 30VDC, 96LED |
| `C30DD20S050-4P3-5Cx2-96LED` | …Trắng (5.000K), Lumileds 3030, 50W, 5Cx2, 30VDC, 96LED |
| `C30DD20S050-5B3-5Cx2-96LED` | …Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5Cx2, 30VDC, 9 |
| `C30DD20S050-5P3-5Cx2-96LED` | …Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5Cx2, 30VDC, 96 |
| `C30DD20S050-6B3-5Cx2-96LED` | …Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5Cx2, 30VDC, 96 |
| `C30DD20S050-6P3-5Cx2-96LED` | …Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5Cx2, 30VDC, 96L |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 3030 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 184, 185, 186, 187, 188, 189, 190, 191

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD20S100-3B3-5Cx3-128LED` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 100W, 5Cx3, 3 |
| `C30DD20S100-3P3-5Cx3-128LED` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 100W, 5Cx3, 30 |
| `C30DD20S100-4B3-5Cx3-128LED` | … Trắng (5.000K), Bridgelux 3030, 100W, 5Cx3, 30VDC, 128LED |
| `C30DD20S100-4P3-5Cx3-128LED` | … Trắng (5.000K), Lumileds 3030, 100W, 5Cx3, 30VDC, 128LED |
| `C30DD20S100-5B3-5Cx3-128LED` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 100W, 5Cx3, 30VDC, |
| `C30DD20S100-5P3-5Cx3-128LED` | … Trắng (6.000K - 6.500K), Lumileds 3030, 100W, 5Cx3, 30VDC,  |
| `C30DD20S100-6B3-5Cx3-128LED` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 100W, 5Cx3, 30VDC,  |
| `C30DD20S100-6P3-5Cx3-128LED` | … Vàng (3.000K - 3.200K), Lumileds 3030, 100W, 5Cx3, 30VDC, 1 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 150W LED 3030 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 200, 201, 202, 203, 204, 205, 206, 207

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD20S150-3B3-5Cx4-240LED` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 150W, 5Cx4, 3 |
| `C30DD20S150-3P3-5Cx4-240LED` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 150W, 5Cx4, 30 |
| `C30DD20S150-4B3-5Cx4-240LED` | … Trắng (5.000K), Bridgelux 3030, 150W, 5Cx4, 30VDC, 240LED |
| `C30DD20S150-4P3-5Cx4-240LED` | … Trắng (5.000K), Lumileds 3030, 150W, 5Cx4, 30VDC, 240LED |
| `C30DD20S150-5B3-5Cx4-240LED` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 150W, 5Cx4, 30VDC, |
| `C30DD20S150-5P3-5Cx4-240LED` | … Trắng (6.000K - 6.500K), Lumileds 3030, 150W, 5Cx4, 30VDC,  |
| `C30DD20S150-6B3-5Cx4-240LED` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 150W, 5Cx4, 30VDC,  |
| `C30DD20S150-6P3-5Cx4-240LED` | … Vàng (3.000K - 3.200K), Lumileds 3030, 150W, 5Cx4, 30VDC, 2 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 200W LED 3030 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 216, 217, 218, 219, 220, 221, 222, 223

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD20S200-3B3-5Cx5-320LED` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 200W, 5Cx5, 3 |
| `C30DD20S200-3P3-5Cx5-320LED` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 200W, 5Cx5, 30 |
| `C30DD20S200-4B3-5Cx5-320LED` | … Trắng (5.000K), Bridgelux 3030, 200W, 5Cx5, 30VDC, 320LED |
| `C30DD20S200-4P3-5Cx5-320LED` | … Trắng (5.000K), Lumileds 3030, 200W, 5Cx5, 30VDC, 320LED |
| `C30DD20S200-5B3-5Cx5-320LED` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 200W, 5Cx5, 30VDC, |
| `C30DD20S200-5P3-5Cx5-320LED` | … Trắng (6.000K - 6.500K), Lumileds 3030, 200W, 5Cx5, 30VDC,  |
| `C30DD20S200-6B3-5Cx5-320LED` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 200W, 5Cx5, 30VDC,  |
| `C30DD20S200-6P3-5Cx5-320LED` | … Vàng (3.000K - 3.200K), Lumileds 3030, 200W, 5Cx5, 30VDC, 3 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 250W LED 3030 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 232, 233, 234, 235, 236, 237, 238, 239

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD20S250-3B3-5Cx5-320LED` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 250W, 5Cx5, 3 |
| `C30DD20S250-3P3-5Cx5-320LED` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 250W, 5Cx5, 30 |
| `C30DD20S250-4B3-5Cx5-320LED` | … Trắng (5.000K), Bridgelux 3030, 250W, 5Cx5, 30VDC, 320LED |
| `C30DD20S250-4P3-5Cx5-320LED` | … Trắng (5.000K), Lumileds 3030, 250W, 5Cx5, 30VDC, 320LED |
| `C30DD20S250-5B3-5Cx5-320LED` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 250W, 5Cx5, 30VDC, |
| `C30DD20S250-5P3-5Cx5-320LED` | … Trắng (6.000K - 6.500K), Lumileds 3030, 250W, 5Cx5, 30VDC,  |
| `C30DD20S250-6B3-5Cx5-320LED` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 250W, 5Cx5, 30VDC,  |
| `C30DD20S250-6P3-5Cx5-320LED` | … Vàng (3.000K - 3.200K), Lumileds 3030, 250W, 5Cx5, 30VDC, 3 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 3030 - Sử dụng: Đèn đường D21 | …`

Dòng trong sheet: 368, 369, 370, 371, 372, 373, 374, 375

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD21S050-3B3-5Cx2` | …Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, 5Cx2, 30V |
| `C30DD21S050-3P3-5Cx2` | …Trung tính (4.000K - 4.200K), Lumileds 3030, 50W, 5Cx2, 30VD |
| `C30DD21S050-4B3-5Cx2` | …Trắng (5.000K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD21S050-4P3-5Cx2` | …Trắng (5.000K), Lumileds 3030, 50W, 5Cx2, 30VDC |
| `C30DD21S050-5B3-5Cx2` | …Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD21S050-5P3-5Cx2` | …Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5Cx2, 30VDC |
| `C30DD21S050-6B3-5Cx2` | …Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD21S050-6P3-5Cx2` | …Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5Cx2, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 3030 - Sử dụng: Đèn đường D21 |…`

Dòng trong sheet: 376, 377, 378, 379, 380, 381, 382, 383

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD21S100-3B3-5Cx3` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 100W, 5Cx3, 3 |
| `C30DD21S100-3P3-5Cx3` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 100W, 5Cx3, 30 |
| `C30DD21S100-4B3-5Cx3` | … Trắng (5.000K), Bridgelux 3030, 100W, 5Cx3, 30VDC |
| `C30DD21S100-4P3-5Cx3` | … Trắng (5.000K), Lumileds 3030, 100W, 5Cx3, 30VDC |
| `C30DD21S100-5B3-5Cx3` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 100W, 5Cx3, 30VDC |
| `C30DD21S100-5P3-5Cx3` | … Trắng (6.000K - 6.500K), Lumileds 3030, 100W, 5Cx3, 30VDC |
| `C30DD21S100-6B3-5Cx3` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 100W, 5Cx3, 30VDC |
| `C30DD21S100-6P3-5Cx3` | … Vàng (3.000K - 3.200K), Lumileds 3030, 100W, 5Cx3, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 150W LED 3030 - Sử dụng: Đèn đường D21 |…`

Dòng trong sheet: 384, 385, 386, 387, 388, 389, 390, 391

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD21S150-3B3-5Cx4` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 150W, 5Cx4, 3 |
| `C30DD21S150-3P3-5Cx4` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 150W, 5Cx4, 30 |
| `C30DD21S150-4B3-5Cx4` | … Trắng (5.000K), Bridgelux 3030, 150W, 5Cx4, 30VDC |
| `C30DD21S150-4P3-5Cx4` | … Trắng (5.000K), Lumileds 3030, 150W, 5Cx4, 30VDC |
| `C30DD21S150-5B3-5Cx4` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 150W, 5Cx4, 30VDC |
| `C30DD21S150-5P3-5Cx4` | … Trắng (6.000K - 6.500K), Lumileds 3030, 150W, 5Cx4, 30VDC |
| `C30DD21S150-6B3-5Cx4` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 150W, 5Cx4, 30VDC |
| `C30DD21S150-6P3-5Cx4` | … Vàng (3.000K - 3.200K), Lumileds 3030, 150W, 5Cx4, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 200W LED 3030 - Sử dụng: Đèn đường D21 |…`

Dòng trong sheet: 392, 393, 394, 395, 396, 397, 398, 399

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD21S200-3B3-5Cx5` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 200W, 5Cx5, 3 |
| `C30DD21S200-3P3-5Cx5` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 200W, 5Cx5, 30 |
| `C30DD21S200-4B3-5Cx5` | … Trắng (5.000K), Bridgelux 3030, 200W, 5Cx5, 30VDC |
| `C30DD21S200-4P3-5Cx5` | … Trắng (5.000K), Lumileds 3030, 200W, 5Cx5, 30VDC |
| `C30DD21S200-5B3-5Cx5` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 200W, 5Cx5, 30VDC |
| `C30DD21S200-5P3-5Cx5` | … Trắng (6.000K - 6.500K), Lumileds 3030, 200W, 5Cx5, 30VDC |
| `C30DD21S200-6B3-5Cx5` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 200W, 5Cx5, 30VDC |
| `C30DD21S200-6P3-5Cx5` | … Vàng (3.000K - 3.200K), Lumileds 3030, 200W, 5Cx5, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 250W LED 3030 - Sử dụng: Đèn đường D21 |…`

Dòng trong sheet: 400, 401, 402, 403, 404, 405, 406, 407

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD21S250-3B3-5Cx5` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 250W, 5Cx5, 3 |
| `C30DD21S250-3P3-5Cx5` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 250W, 5Cx5, 30 |
| `C30DD21S250-4B3-5Cx5` | … Trắng (5.000K), Bridgelux 3030, 250W, 5Cx5, 30VDC |
| `C30DD21S250-4P3-5Cx5` | … Trắng (5.000K), Lumileds 3030, 250W, 5Cx5, 30VDC |
| `C30DD21S250-5B3-5Cx5` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 250W, 5Cx5, 30VDC |
| `C30DD21S250-5P3-5Cx5` | … Trắng (6.000K - 6.500K), Lumileds 3030, 250W, 5Cx5, 30VDC |
| `C30DD21S250-6B3-5Cx5` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 250W, 5Cx5, 30VDC |
| `C30DD21S250-6P3-5Cx5` | … Vàng (3.000K - 3.200K), Lumileds 3030, 250W, 5Cx5, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 3030 - Sử dụng: Đèn đường D24 | …`

Dòng trong sheet: 328, 329, 330, 331, 332, 333, 334, 335

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD24S050-3B3-5Cx2` | …Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, 5Cx2, 30V |
| `C30DD24S050-3P3-5Cx2` | …Trung tính (4.000K - 4.200K), Lumileds 3030, 50W, 5Cx2, 30VD |
| `C30DD24S050-4B3-5Cx2` | …Trắng (5.000K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD24S050-4P3-5Cx2` | …Trắng (5.000K), Lumileds 3030, 50W, 5Cx2, 30VDC |
| `C30DD24S050-5B3-5Cx2` | …Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD24S050-5P3-5Cx2` | …Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5Cx2, 30VDC |
| `C30DD24S050-6B3-5Cx2` | …Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5Cx2, 30VDC |
| `C30DD24S050-6P3-5Cx2` | …Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5Cx2, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 3030 - Sử dụng: Đèn đường D24 |…`

Dòng trong sheet: 336, 337, 338, 339, 340, 341, 342, 343

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD24S100-3B3-5Cx3` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 100W, 5Cx3, 3 |
| `C30DD24S100-3P3-5Cx3` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 100W, 5Cx3, 30 |
| `C30DD24S100-4B3-5Cx3` | … Trắng (5.000K), Bridgelux 3030, 100W, 5Cx3, 30VDC |
| `C30DD24S100-4P3-5Cx3` | … Trắng (5.000K), Lumileds 3030, 100W, 5Cx3, 30VDC |
| `C30DD24S100-5B3-5Cx3` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 100W, 5Cx3, 30VDC |
| `C30DD24S100-5P3-5Cx3` | … Trắng (6.000K - 6.500K), Lumileds 3030, 100W, 5Cx3, 30VDC |
| `C30DD24S100-6B3-5Cx3` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 100W, 5Cx3, 30VDC |
| `C30DD24S100-6P3-5Cx3` | … Vàng (3.000K - 3.200K), Lumileds 3030, 100W, 5Cx3, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 150W LED 3030 - Sử dụng: Đèn đường D24 |…`

Dòng trong sheet: 344, 345, 346, 347, 348, 349, 350, 351

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD24S150-3B3-5Cx4` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 150W, 5Cx4, 3 |
| `C30DD24S150-3P3-5Cx4` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 150W, 5Cx4, 30 |
| `C30DD24S150-4B3-5Cx4` | … Trắng (5.000K), Bridgelux 3030, 150W, 5Cx4, 30VDC |
| `C30DD24S150-4P3-5Cx4` | … Trắng (5.000K), Lumileds 3030, 150W, 5Cx4, 30VDC |
| `C30DD24S150-5B3-5Cx4` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 150W, 5Cx4, 30VDC |
| `C30DD24S150-5P3-5Cx4` | … Trắng (6.000K - 6.500K), Lumileds 3030, 150W, 5Cx4, 30VDC |
| `C30DD24S150-6B3-5Cx4` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 150W, 5Cx4, 30VDC |
| `C30DD24S150-6P3-5Cx4` | … Vàng (3.000K - 3.200K), Lumileds 3030, 150W, 5Cx4, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 200W LED 3030 - Sử dụng: Đèn đường D24 |…`

Dòng trong sheet: 352, 353, 354, 355, 356, 357, 358, 359

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD24S200-3B3-5Cx5` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 200W, 5Cx5, 3 |
| `C30DD24S200-3P3-5Cx5` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 200W, 5Cx5, 30 |
| `C30DD24S200-4B3-5Cx5` | … Trắng (5.000K), Bridgelux 3030, 200W, 5Cx5, 30VDC |
| `C30DD24S200-4P3-5Cx5` | … Trắng (5.000K), Lumileds 3030, 200W, 5Cx5, 30VDC |
| `C30DD24S200-5B3-5Cx5` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 200W, 5Cx5, 30VDC |
| `C30DD24S200-5P3-5Cx5` | … Trắng (6.000K - 6.500K), Lumileds 3030, 200W, 5Cx5, 30VDC |
| `C30DD24S200-6B3-5Cx5` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 200W, 5Cx5, 30VDC |
| `C30DD24S200-6P3-5Cx5` | … Vàng (3.000K - 3.200K), Lumileds 3030, 200W, 5Cx5, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 250W LED 3030 - Sử dụng: Đèn đường D24 |…`

Dòng trong sheet: 360, 361, 362, 363, 364, 365, 366, 367

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DD24S250-3B3-5Cx5` | … Trung tính (4.000K - 4.200K), Bridgelux 3030, 250W, 5Cx5, 3 |
| `C30DD24S250-3P3-5Cx5` | … Trung tính (4.000K - 4.200K), Lumileds 3030, 250W, 5Cx5, 30 |
| `C30DD24S250-4B3-5Cx5` | … Trắng (5.000K), Bridgelux 3030, 250W, 5Cx5, 30VDC |
| `C30DD24S250-4P3-5Cx5` | … Trắng (5.000K), Lumileds 3030, 250W, 5Cx5, 30VDC |
| `C30DD24S250-5B3-5Cx5` | … Trắng (6.000K - 6.500K), Bridgelux 3030, 250W, 5Cx5, 30VDC |
| `C30DD24S250-5P3-5Cx5` | … Trắng (6.000K - 6.500K), Lumileds 3030, 250W, 5Cx5, 30VDC |
| `C30DD24S250-6B3-5Cx5` | … Vàng (3.000K - 3.200K), Bridgelux 3030, 250W, 5Cx5, 30VDC |
| `C30DD24S250-6P3-5Cx5` | … Vàng (3.000K - 3.200K), Lumileds 3030, 250W, 5Cx5, 30VDC |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 50W LED 5050 - Sử dụng: Đèn đường D20 | …`

Dòng trong sheet: 176, 177, 178, 179, 180, 181, 182, 183

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD20S050-3B5-5Cx2-24LED` | …Trung tính (4.000K - 4.200K), Bridgelux 5050, 50W, 5Cx2, 30V |
| `C50DD20S050-3P5-5Cx2-24LED` | …Trung tính (4.000K - 4.200K), Lumileds 5050, 50W, 5Cx2, 30VD |
| `C50DD20S050-4B5-5Cx2-24LED` | …Trắng (5.000K), Bridgelux 5050, 50W, 5Cx2, 30VDC, 24LED |
| `C50DD20S050-4P5-5Cx2-24LED` | …Trắng (5.000K), Lumileds 5050, 50W, 5Cx2, 30VDC, 24LED |
| `C50DD20S050-5B5-5Cx2-24LED` | …Trắng (6.000K - 6.500K), Bridgelux 5050, 50W, 5Cx2, 30VDC, 2 |
| `C50DD20S050-5P5-5Cx2-24LED` | …Trắng (6.000K - 6.500K), Lumileds 5050, 50W, 5Cx2, 30VDC, 24 |
| `C50DD20S050-6B5-5Cx2-24LED` | …Vàng (3.000K - 3.200K), Bridgelux 5050, 50W, 5Cx2, 30VDC, 24 |
| `C50DD20S050-6P5-5Cx2-24LED` | …Vàng (3.000K - 3.200K), Lumileds 5050, 50W, 5Cx2, 30VDC, 24L |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 100W LED 5050 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 192, 193, 194, 195, 196, 197, 198, 199

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD20S100-3B5-5Cx3-32LED` | … Trung tính (4.000K - 4.200K), Bridgelux 5050, 100W, 5Cx3, 3 |
| `C50DD20S100-3P5-5Cx3-32LED` | … Trung tính (4.000K - 4.200K), Lumileds 5050, 100W, 5Cx3, 30 |
| `C50DD20S100-4B5-5Cx3-32LED` | … Trắng (5.000K), Bridgelux 5050, 100W, 5Cx3, 30VDC, 32LED |
| `C50DD20S100-4P5-5Cx3-32LED` | … Trắng (5.000K), Lumileds 5050, 100W, 5Cx3, 30VDC, 32LED |
| `C50DD20S100-5B5-5Cx3-32LED` | … Trắng (6.000K - 6.500K), Bridgelux 5050, 100W, 5Cx3, 30VDC, |
| `C50DD20S100-5P5-5Cx3-32LED` | … Trắng (6.000K - 6.500K), Lumileds 5050, 100W, 5Cx3, 30VDC,  |
| `C50DD20S100-6B5-5Cx3-32LED` | … Vàng (3.000K - 3.200K), Bridgelux 5050, 100W, 5Cx3, 30VDC,  |
| `C50DD20S100-6P5-5Cx3-32LED` | … Vàng (3.000K - 3.200K), Lumileds 5050, 100W, 5Cx3, 30VDC, 3 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 150W LED 5050 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 208, 209, 210, 211, 212, 213, 214, 215

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD20S150-3B5-5Cx4-60LED` | … Trung tính (4.000K - 4.200K), Bridgelux 5050, 150W, 5Cx4, 3 |
| `C50DD20S150-3P5-5Cx4-60LED` | … Trung tính (4.000K - 4.200K), Lumileds 5050, 150W, 5Cx4, 30 |
| `C50DD20S150-4B5-5Cx4-60LED` | … Trắng (5.000K), Bridgelux 5050, 150W, 5Cx4, 30VDC, 60LED |
| `C50DD20S150-4P5-5Cx4-60LED` | … Trắng (5.000K), Lumileds 5050, 150W, 5Cx4, 30VDC, 60LED |
| `C50DD20S150-5B5-5Cx4-60LED` | … Trắng (6.000K - 6.500K), Bridgelux 5050, 150W, 5Cx4, 30VDC, |
| `C50DD20S150-5P5-5Cx4-60LED` | … Trắng (6.000K - 6.500K), Lumileds 5050, 150W, 5Cx4, 30VDC,  |
| `C50DD20S150-6B5-5Cx4-60LED` | … Vàng (3.000K - 3.200K), Bridgelux 5050, 150W, 5Cx4, 30VDC,  |
| `C50DD20S150-6P5-5Cx4-60LED` | … Vàng (3.000K - 3.200K), Lumileds 5050, 150W, 5Cx4, 30VDC, 6 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 200W LED 5050 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 224, 225, 226, 227, 228, 229, 230, 231

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD20S200-3B5-5Cx5-80LED` | … Trung tính (4.000K - 4.200K), Bridgelux 5050, 200W, 5Cx5, 3 |
| `C50DD20S200-3P5-5Cx5-80LED` | … Trung tính (4.000K - 4.200K), Lumileds 5050, 200W, 5Cx5, 30 |
| `C50DD20S200-4B5-5Cx5-80LED` | … Trắng (5.000K), Bridgelux 5050, 200W, 5Cx5, 30VDC, 80LED |
| `C50DD20S200-4P5-5Cx5-80LED` | … Trắng (5.000K), Lumileds 5050, 200W, 5Cx5, 30VDC, 80LED |
| `C50DD20S200-5B5-5Cx5-80LED` | … Trắng (6.000K - 6.500K), Bridgelux 5050, 200W, 5Cx5, 30VDC, |
| `C50DD20S200-5P5-5Cx5-80LED` | … Trắng (6.000K - 6.500K), Lumileds 5050, 200W, 5Cx5, 30VDC,  |
| `C50DD20S200-6B5-5Cx5-80LED` | … Vàng (3.000K - 3.200K), Bridgelux 5050, 200W, 5Cx5, 30VDC,  |
| `C50DD20S200-6P5-5Cx5-80LED` | … Vàng (3.000K - 3.200K), Lumileds 5050, 200W, 5Cx5, 30VDC, 8 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn đường 250W LED 5050 - Sử dụng: Đèn đường D20 |…`

Dòng trong sheet: 240, 241, 242, 243, 244, 245, 246, 247

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C50DD20S250-3B5-5Cx5-80LED` | … Trung tính (4.000K - 4.200K), Bridgelux 5050, 250W, 5Cx5, 3 |
| `C50DD20S250-3P5-5Cx5-80LED` | … Trung tính (4.000K - 4.200K), Lumileds 5050, 250W, 5Cx5, 30 |
| `C50DD20S250-4B5-5Cx5-80LED` | … Trắng (5.000K), Bridgelux 5050, 250W, 5Cx5, 30VDC, 80LED |
| `C50DD20S250-4P5-5Cx5-80LED` | … Trắng (5.000K), Lumileds 5050, 250W, 5Cx5, 30VDC, 80LED |
| `C50DD20S250-5B5-5Cx5-80LED` | … Trắng (6.000K - 6.500K), Bridgelux 5050, 250W, 5Cx5, 30VDC, |
| `C50DD20S250-5P5-5Cx5-80LED` | … Trắng (6.000K - 6.500K), Lumileds 5050, 250W, 5Cx5, 30VDC,  |
| `C50DD20S250-6B5-5Cx5-80LED` | … Vàng (3.000K - 3.200K), Bridgelux 5050, 250W, 5Cx5, 30VDC,  |
| `C50DD20S250-6P5-5Cx5-80LED` | … Vàng (3.000K - 3.200K), Lumileds 5050, 250W, 5Cx5, 30VDC, 8 |

### (C) Chip LED — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip Module SMD 50W LED 3030 - Sử dụng: Module COB 50W …`

Dòng trong sheet: 50, 51, 52, 53, 54, 55, 56, 57

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `CM30C050-3B3-5C-49LED` | …| Trung tính (4.000K - 4.200K), Bridgelux 3030, 50W, 5C, 30V |
| `CM30C050-3P3-5C-49LED` | …| Trung tính (4.000K - 4.200K), Lumileds 3030, 50W, 5C, 30VD |
| `CM30C050-4B3-5C-49LED` | …| Trắng (5.000K), Bridgelux 3030, 50W, 5C, 30VDC, 49LED |
| `CM30C050-4P3-5C-49LED` | …| Trắng (5.000K), Lumileds 3030, 50W, 5C, 30VDC, 49LED |
| `CM30C050-5B3-5C-49LED` | …| Trắng (6.000K - 6.500K), Bridgelux 3030, 50W, 5C, 30VDC, 4 |
| `CM30C050-5P3-5C-49LED` | …| Trắng (6.000K - 6.500K), Lumileds 3030, 50W, 5C, 30VDC, 49 |
| `CM30C050-6B3-5C-49LED` | …| Vàng (3.000K - 3.200K), Bridgelux 3030, 50W, 5C, 30VDC, 49 |
| `CM30C050-6P3-5C-49LED` | …| Vàng (3.000K - 3.200K), Lumileds 3030, 50W, 5C, 30VDC, 49L |

### (M) Module — 8 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 30W LED 3030 - Sử dụng: P02 10W, 20W, 30W | …`

Dòng trong sheet: 2, 3, 4, 5, 6, 7, 8, 9

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M30S030-3B5-5C-30LED-DD-A` | …Trung tính (4.000K - 4.200K), Bridgelux 3030, 5C, 30VDC, 30L |
| `M30S030-3P3-5C-30LED-DD-A` | …Trung tính (4.000K - 4.200K), Lumileds 3030, 5C, 30VDC, 30LE |
| `M30S030-4B5-5C-30LED-DD-A` | …Trắng (5.000K), Bridgelux 3030, 5C, 30VDC, 30LED | Dây điện |
| `M30S030-4P3-5C-30LED-DD-A` | …Trắng (5.000K), Lumileds 3030, 5C, 30VDC, 30LED | Dây điện |
| `M30S030-5B5-5C-30LED-DD-A` | …Trắng (6.000K - 6.500K), Bridgelux 3030, 5C, 30VDC, 30LED |  |
| `M30S030-5P3-5C-30LED-DD-A` | …Trắng (6.000K - 6.500K), Lumileds 3030, 5C, 30VDC, 30LED | D |
| `M30S030-6B5-5C-30LED-DD-A` | …Vàng (3.000K - 3.200K), Bridgelux 3030, 5C, 30VDC, 30LED | D |
| `M30S030-6P3-5C-30LED-DD-A` | …Vàng (3.000K - 3.200K), Lumileds 3030, 5C, 30VDC, 30LED | Dâ |

### (PTN) Tản nhiệt — 7 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường dùng chung D13 và D14 Chip LED S…`

Dòng trong sheet: 69, 69, 70, 71, 72, 73, 74

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDD13` | …MD |
| `PTN-VDD13S050` | …MD Công suất 100W |
| `PTN-VDD13S100` | …MD Công suất 150W |
| `PTN-VDD13S150` | …MD Công suất 200W |
| `PTN-VDD13S200` | …MD Công suất 250W |
| `PTN-VDD13S250` | …MD Công suất 300W |
| `PTN-VDD13S300` | …MD Công suất 50W |

### (PTN) Tản nhiệt — 7 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ dùng chung đèn pha PTC/PTR Chip LED COB Cô…`

Dòng trong sheet: 15, 16, 17, 18, 19, 20, 21

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDPTCC050` | …ng suất 100W |
| `PTN-VDPTCC100` | …ng suất 250W |
| `PTN-VDPTCC250` | …ng suất 300W |
| `PTN-VDPTCC300` | …ng suất 400W |
| `PTN-VDPTCC400` | …ng suất 500W |
| `PTN-VDPTCC500` | …ng suất 50W |
| `PTN-VDPTCC600` | …ng suất 600W |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 100W LED 3030 - Sử dụng: UFO X01 | T…`

Dòng trong sheet: 408, 409, 410, 412, 413, 414

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX01S100-4B3-5C-110LED` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 100W, 5C, 30VDC |
| `C30DX01S100-4P3-5C-110LED` | …rung tính (4.000K - 4.200K), Lumileds 3030, 100W, 5C, 30VDC, |
| `C30DX01S100-5B3-5C-110LED` | …rắng (5.000K), Bridgelux 3030, 100W, 5C, 30VDC, 110LED |
| `C30DX01S100-5P3-5C-110LED` | …rắng (5.000K), Lumileds 3030, 100W, 5C, 30VDC, 110LED |
| `C30DX01S100-6B3-5C-110LED` | …rắng (6.000K - 6.500K), Bridgelux 3030, 100W, 5C, 30VDC, 110 |
| `C30DX01S100-6P3-5C-110LED` | …rắng (6.000K - 6.500K), Lumileds 3030, 100W, 5C, 30VDC, 110L |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 150W LED 3030 - Sử dụng: UFO X01 | T…`

Dòng trong sheet: 416, 417, 418, 420, 421, 422

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX01S150-4B3-5C-170LED` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 150W, 5C, 30VDC |
| `C30DX01S150-4P3-5C-170LED` | …rung tính (4.000K - 4.200K), Lumileds 3030, 150W, 5C, 30VDC, |
| `C30DX01S150-5B3-5C-170LED` | …rắng (5.000K), Bridgelux 3030, 150W, 5C, 30VDC, 170LED |
| `C30DX01S150-5P3-5C-170LED` | …rắng (5.000K), Lumileds 3030, 150W, 5C, 30VDC, 170LED |
| `C30DX01S150-6B3-5C-170LED` | …rắng (6.000K - 6.500K), Bridgelux 3030, 150W, 5C, 30VDC, 170 |
| `C30DX01S150-6P3-5C-170LED` | …rắng (6.000K - 6.500K), Lumileds 3030, 150W, 5C, 30VDC, 170L |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 200W LED 3030 - Sử dụng: UFO X01 | T…`

Dòng trong sheet: 424, 425, 426, 428, 429, 430

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX01S200-4B3-5C-220LED` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 200W, 5C, 30VDC |
| `C30DX01S200-4P3-5C-220LED` | …rung tính (4.000K - 4.200K), Lumileds 3030, 200W, 5C, 30VDC, |
| `C30DX01S200-5B3-5C-220LED` | …rắng (5.000K), Bridgelux 3030, 200W, 5C, 30VDC, 220LED |
| `C30DX01S200-5P3-5C-220LED` | …rắng (5.000K), Lumileds 3030, 200W, 5C, 30VDC, 220LED |
| `C30DX01S200-6B3-5C-220LED` | …rắng (6.000K - 6.500K), Bridgelux 3030, 200W, 5C, 30VDC, 220 |
| `C30DX01S200-6P3-5C-220LED` | …rắng (6.000K - 6.500K), Lumileds 3030, 200W, 5C, 30VDC, 220L |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 100W LED 3030 - Sử dụng: UFO X02 | T…`

Dòng trong sheet: 448, 449, 450, 452, 453, 454

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX02S100-4B3-7C` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 100W, 7C, 42VDC |
| `C30DX02S100-4P3-7C` | …rung tính (4.000K - 4.200K), Lumileds 3030, 100W, 7C, 42VDC |
| `C30DX02S100-5B3-7C` | …rắng (5.000K), Bridgelux 3030, 100W, 7C, 42VDC |
| `C30DX02S100-5P3-7C` | …rắng (5.000K), Lumileds 3030, 100W, 7C, 42VDC |
| `C30DX02S100-6B3-7C` | …rắng (6.000K - 6.500K), Bridgelux 3030, 100W, 7C, 42VDC |
| `C30DX02S100-6P3-7C` | …rắng (6.000K - 6.500K), Lumileds 3030, 100W, 7C, 42VDC |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 150W LED 3030 - Sử dụng: UFO X02 | T…`

Dòng trong sheet: 456, 457, 458, 460, 461, 462

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX02S150-4B3-7C-196LED` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 150W, 7C, 42VDC |
| `C30DX02S150-4P3-7C-196LED` | …rung tính (4.000K - 4.200K), Lumileds 3030, 150W, 7C, 42VDC, |
| `C30DX02S150-5B3-7C-196LED` | …rắng (5.000K), Bridgelux 3030, 150W, 7C, 42VDC, 196LED |
| `C30DX02S150-5P3-7C-196LED` | …rắng (5.000K), Lumileds 3030, 150W, 7C, 42VDC, 196LED |
| `C30DX02S150-6B3-7C-196LED` | …rắng (6.000K - 6.500K), Bridgelux 3030, 150W, 7C, 42VDC, 196 |
| `C30DX02S150-6P3-7C-196LED` | …rắng (6.000K - 6.500K), Lumileds 3030, 150W, 7C, 42VDC, 196L |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 200W LED 3030 - Sử dụng: UFO X02 | T…`

Dòng trong sheet: 464, 465, 466, 468, 469, 470

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX02S200-4B3-7C` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 200W, 7C, 42VDC |
| `C30DX02S200-4P3-7C` | …rung tính (4.000K - 4.200K), Lumileds 3030, 200W, 7C, 42VDC |
| `C30DX02S200-5B3-7C` | …rắng (5.000K), Bridgelux 3030, 200W, 7C, 42VDC |
| `C30DX02S200-5P3-7C` | …rắng (5.000K), Lumileds 3030, 200W, 7C, 42VDC |
| `C30DX02S200-6B3-7C` | …rắng (6.000K - 6.500K), Bridgelux 3030, 200W, 7C, 42VDC |
| `C30DX02S200-6P3-7C` | …rắng (6.000K - 6.500K), Lumileds 3030, 200W, 7C, 42VDC |

### (C) Chip LED — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 50W LED CREE - Sử dụng: Các mẫu COB: PTC, PTR,…`

Dòng trong sheet: 118, 119, 120, 121, 122, 123

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `COBC050-3CR-30VDC` | … DQL,... | Trung tính (4.000K - 4.200K), CREE, 50W, 30VDC |
| `COBC050-3CR-42VDC` | … DQL,... | Trung tính (4.000K - 4.200K), CREE, 50W, 42VDC |
| `COBC050-4CR-30VDC` | … DQL,... | Trắng (6.000K - 6.500K), CREE, 50W, 30VDC |
| `COBC050-4CR-42VDC` | … DQL,... | Trắng (6.000K - 6.500K), CREE, 50W, 42VDC |
| `COBC050-6CR-30VDC` | … DQL,... | Vàng (3.000K - 3.200K), CREE, 50W, 30VDC |
| `COBC050-6CR-42VDC` | … DQL,... | Vàng (3.000K - 3.200K), CREE, 50W, 42VDC |

### (M) Module — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 200W LED 3030 - Sử dụng: Đèn pha P04 SMD | T…`

Dòng trong sheet: 122, 123, 124, 126, 127, 128

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M30S200-4B5-5C-288LED-DD` | …rung tính (4.000K - 4.200K), Bridgelux 3030, 5C, 30VDC, 288L |
| `M30S200-4P3-5C-288LED-DD` | …rung tính (4.000K - 4.200K), Lumileds 3030, 5C, 30VDC, 288LE |
| `M30S200-5B5-5C-288LED-DD` | …rắng (5.000K), Bridgelux 3030, 5C, 30VDC, 288LED | Dây điện |
| `M30S200-5P3-5C-288LED-DD` | …rắng (5.000K), Lumileds 3030, 5C, 30VDC, 288LED | Dây điện |
| `M30S200-6B5-5C-288LED-DD` | …rắng (6.000K - 6.500K), Bridgelux 3030, 5C, 30VDC, 288LED |  |
| `M30S200-6P3-5C-288LED-DD` | …rắng (6.000K - 6.500K), Lumileds 3030, 5C, 30VDC, 288LED | D |

### (M) Module — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 200W LED 5050 - Sử dụng: Đèn pha P04 SMD | T…`

Dòng trong sheet: 130, 131, 132, 134, 135, 136

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M50S200-4B5-5C-72LED-DD` | …rung tính (4.000K - 4.200K), Bridgelux 5050, 5C, 30VDC, 72LE |
| `M50S200-4P5-5C-72LED-DD` | …rung tính (4.000K - 4.200K), Lumileds 5050, 5C, 30VDC, 72LED |
| `M50S200-5B5-5C-72LED-DD` | …rắng (5.000K), Bridgelux 5050, 5C, 30VDC, 72LED | Dây điện |
| `M50S200-5P5-5C-72LED-DD` | …rắng (5.000K), Lumileds 5050, 5C, 30VDC, 72LED | Dây điện |
| `M50S200-6B5-5C-72LED-DD` | …rắng (6.000K - 6.500K), Bridgelux 5050, 5C, 30VDC, 72LED | D |
| `M50S200-6P5-5C-72LED-DD` | …rắng (6.000K - 6.500K), Lumileds 5050, 5C, 30VDC, 72LED | Dâ |

### (PTN) Tản nhiệt — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường DQL Chip LED SMD Công suất 50W |…`

Dòng trong sheet: 128, 129, 130, 143, 144, 145

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDDQLC050-H-BK` | … Vỏ nặng, Chưa sơn |
| `PTN-VDDQLC050-H-GY` | … Vỏ nặng, Xám |
| `PTN-VDDQLC050-H-NO` | … Vỏ nặng, Đen |
| `PTN-VDDQLC050-M-BK` | … Vỏ thường, Chưa sơn |
| `PTN-VDDQLC050-M-GY` | … Vỏ thường, Xám |
| `PTN-VDDQLC050-M-NO` | … Vỏ thường, Đen |

### (PTN) Tản nhiệt — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường DQL Chip LED SMD Công suất 100W …`

Dòng trong sheet: 131, 132, 133, 146, 147, 148

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDDQLC100-H-BK` | …| Vỏ nặng, Chưa sơn |
| `PTN-VDDQLC100-H-GY` | …| Vỏ nặng, Xám |
| `PTN-VDDQLC100-H-NO` | …| Vỏ nặng, Đen |
| `PTN-VDDQLC100-M-BK` | …| Vỏ thường, Chưa sơn |
| `PTN-VDDQLC100-M-GY` | …| Vỏ thường, Xám |
| `PTN-VDDQLC100-M-NO` | …| Vỏ thường, Đen |

### (PTN) Tản nhiệt — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường DQL Chip LED SMD Công suất 150W …`

Dòng trong sheet: 134, 135, 136, 149, 150, 151

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDDQLC150-H-BK` | …| Vỏ nặng, Chưa sơn |
| `PTN-VDDQLC150-H-GY` | …| Vỏ nặng, Xám |
| `PTN-VDDQLC150-H-NO` | …| Vỏ nặng, Đen |
| `PTN-VDDQLC150-M-BK` | …| Vỏ thường, Chưa sơn |
| `PTN-VDDQLC150-M-GY` | …| Vỏ thường, Xám |
| `PTN-VDDQLC150-M-NO` | …| Vỏ thường, Đen |

### (PTN) Tản nhiệt — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường DQL Chip LED SMD Công suất 200W …`

Dòng trong sheet: 137, 138, 139, 152, 153, 154

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDDQLC200-H-BK` | …| Vỏ nặng, Chưa sơn |
| `PTN-VDDQLC200-H-GY` | …| Vỏ nặng, Xám |
| `PTN-VDDQLC200-H-NO` | …| Vỏ nặng, Đen |
| `PTN-VDDQLC200-M-BK` | …| Vỏ thường, Chưa sơn |
| `PTN-VDDQLC200-M-GY` | …| Vỏ thường, Xám |
| `PTN-VDDQLC200-M-NO` | …| Vỏ thường, Đen |

### (PTN) Tản nhiệt — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường DQL Chip LED SMD Công suất 250W …`

Dòng trong sheet: 140, 141, 142, 155, 156, 157

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDDQLC250-H-BK` | …| Vỏ nặng, Chưa sơn |
| `PTN-VDDQLC250-H-GY` | …| Vỏ nặng, Xám |
| `PTN-VDDQLC250-H-NO` | …| Vỏ nặng, Đen |
| `PTN-VDDQLC250-M-BK` | …| Vỏ thường, Chưa sơn |
| `PTN-VDDQLC250-M-GY` | …| Vỏ thường, Xám |
| `PTN-VDDQLC250-M-NO` | …| Vỏ thường, Đen |

### (PTN) Tản nhiệt — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn pha viền mắt lồi PVL Chip LED COB Công…`

Dòng trong sheet: 42, 43, 44, 45, 46, 47

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDPVLC100` | … suất 100W |
| `PTN-VDPVLC150` | … suất 150W |
| `PTN-VDPVLC200` | … suất 200W |
| `PTN-VDPVLC250` | … suất 250W |
| `PTN-VDPVLC300` | … suất 300W |
| `PTN-VDPVLC400` | … suất 400W |

### (V) Vỏ đèn — 6 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha viền mắt lồi hộp nguồn sau PVL Chip COB Công…`

Dòng trong sheet: 113, 113, 114, 115, 116, 117

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPVL` | … suất 100W |
| `VDPVLC100` | … suất 150W |
| `VDPVLC150` | … suất 200W |
| `VDPVLC200` | … suất 300W |
| `VDPVLC300` | … suất 400W |
| `VDPVLC400` | … |

### (C) Chip LED — 5 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn indoor 8W LED 2835 - Sử dụng: Panel 600x600 / …`

Dòng trong sheet: 620, 624, 625, 626, 627

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C28DIPNS008` | …300x1200 / 600x1200 |
| `C28DIPNS008-3O2-8C-8LED` | …300x1200 / 600x1200 | Trung tính (4.000K - 4.200K), Osram 28 |
| `C28DIPNS008-4O2-8C-8LED` | …300x1200 / 600x1200 | Trắng (5.000K), Osram 2835, 8W, 8C, 48 |
| `C28DIPNS008-5O2-8C-8LED` | …300x1200 / 600x1200 | Trắng (6.000K - 6.500K), Osram 2835, 8 |
| `C28DIPNS008-6O2-8C-8LED` | …300x1200 / 600x1200 | Vàng (3.000K - 3.200K), Osram 2835, 8W |

### (C) Chip LED — 5 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 1000W LED CREE - Sử dụng: Pha sân vận động…`

Dòng trong sheet: 568, 568, 569, 570, 571

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPVDS1K0` | … (PVD) |
| `C30DPVDS1K0-3CR` | … (PVD) | Trung tính (4.000K - 4.200K), CREE, 1000W |
| `C30DPVDS1K0-4CR` | … (PVD) | Trắng (5.000K), CREE, 1000W |
| `C30DPVDS1K0-5CR` | … (PVD) | Trắng (6.000K - 6.500K), CREE, 1000W |
| `C30DPVDS1K0-6CR` | … (PVD) | Vàng (3.000K - 3.200K), CREE, 1000W |

### (C) Chip LED — 5 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 200W LED CREE - Sử dụng: Pha sân vận động …`

Dòng trong sheet: 560, 560, 561, 562, 563

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPVDS200` | …(PVD) |
| `C30DPVDS200-3CR` | …(PVD) | Trung tính (4.000K - 4.200K), CREE, 200W |
| `C30DPVDS200-4CR` | …(PVD) | Trắng (5.000K), CREE, 200W |
| `C30DPVDS200-5CR` | …(PVD) | Trắng (6.000K - 6.500K), CREE, 200W |
| `C30DPVDS200-6CR` | …(PVD) | Vàng (3.000K - 3.200K), CREE, 200W |

### (C) Chip LED — 5 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn pha 600W LED CREE - Sử dụng: Pha sân vận động …`

Dòng trong sheet: 564, 564, 565, 566, 567

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DPVDS600` | …(PVD) |
| `C30DPVDS600-3CR` | …(PVD) | Trung tính (4.000K - 4.200K), CREE, 600W |
| `C30DPVDS600-4CR` | …(PVD) | Trắng (5.000K), CREE, 600W |
| `C30DPVDS600-5CR` | …(PVD) | Trắng (6.000K - 6.500K), CREE, 600W |
| `C30DPVDS600-6CR` | …(PVD) | Vàng (3.000K - 3.200K), CREE, 600W |

### LED — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `PCT - LED 3030 - PCT - 1W/18V-60mA, 140-150lm/W; Ra80. …`

Dòng trong sheet: 18, 19, 20, 21

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `3030UN18V1W-H2` | …| Trung tính (4.000K - 4.200K) |
| `3030US18V1W-H2` | …| Trắng (5.000K) |
| `3030UW18V1W-H2` | …| Trắng (6.000K - 6.500K) |
| `3030UZ18V1W-H2` | …| Vàng (3.000K - 3.200K) |

### LED — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `PCT - LED 2835 - PCT - 1W/18V-60mA, 110-120lm/W; Ra80 |…`

Dòng trong sheet: 30, 31, 32, 33

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `E2835UN18V1W-E1/ Ra70` | … Trung tính (4.000K - 4.200K) |
| `E2835US18V1W-E1/ Ra70` | … Trắng (5.000K) |
| `E2835UW18V1W-E1/ Ra70` | … Trắng (6.000K - 6.500K) |
| `E2835UZ18V1W-E1/ Ra70` | … Vàng (3.000K - 3.200K) |

### LED — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `PCT - LED 2835 - PCT - 1W/6V-150mA, 110-120lm/W; Ra80 |…`

Dòng trong sheet: 26, 27, 28, 29

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `E2835UN6V1W-E2/ Ra70` | … Trung tính (4.000K - 4.200K) |
| `E2835US6V1W-E2/ Ra70` | … Trắng (5.000K) |
| `E2835UW6V1W-E2/ Ra70` | … Trắng (6.000K - 6.500K) |
| `E2835UZ6V1W-E2/ Ra70` | … Vàng (3.000K - 3.200K) |

### LED — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `EMC - LED EMC 5050 6V 2W/6V/300mA/300-330LM .Ra70 1936*…`

Dòng trong sheet: 6, 7, 8, 9

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `EMC5050UNY2C4B-G330-VN` | …8 | Trung tính (4.000K - 4.200K) |
| `EMC5050USY2C4B-G330-VN` | …8 | Trắng (5.000K) |
| `EMC5050UWY2C4B-G330-VN` | …8 | Trắng (6.000K - 6.500K) |
| `EMC5050UZY2C4B-G330-VN` | …8 | Vàng (3.000K - 3.200K) |

### LED — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `EMC - LED EMC 7070 54V 5W/54V/100mA /800-900LM ,Ra90 22…`

Dòng trong sheet: 10, 11, 12, 13

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `EMC7070UNY18C-H900-VN` | …35*18 | Trung tính (4.000K - 4.200K) |
| `EMC7070USY18C-H900-VN` | …35*18 | Trắng (5.000K) |
| `EMC7070UWY18C-H900-VN` | …35*18 | Trắng (6.000K - 6.500K) |
| `EMC7070UZY18C-H900-VN` | …35*18 | Vàng (3.000K - 3.200K) |

### LED — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `PCT - LED 3030 - PCT - 1W/6V-150mA, 140-145lm/W; Ra80. …`

Dòng trong sheet: 14, 15, 16, 17

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PCT3030UNF2C-K140-VN` | … | Trung tính (4.000K - 4.200K) |
| `PCT3030USF2C-K140-VN` | … | Trắng (5.000K) |
| `PCT3030UWF2C-K140-VN` | … | Trắng (6.000K - 6.500K) |
| `PCT3030UZF2C-K140-VN` | … | Vàng (3.000K - 3.200K) |

### (V) Vỏ đèn — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 100W - Dùng ch…`

Dòng trong sheet: 21, 22, 23, 24

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-100-D-BK-v3.0` | …ung cho P01 và P03 (Lắp ngang) | Xám, v3.0, Ngang |
| `VDP0X-100-D-GY-v3.0` | …ung cho P01 và P03 (Lắp ngang) | Đen, v3.0, Ngang |
| `VDP0X-100-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Dọc |
| `VDP0X-100-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Dọc |

### (V) Vỏ đèn — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 200W - Dùng ch…`

Dòng trong sheet: 27, 28, 29, 30

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-200-D-BK-v3.0` | …ung cho P01 và P03 (Lắp ngang) | Xám, v3.0, Ngang |
| `VDP0X-200-D-GY-v3.0` | …ung cho P01 và P03 (Lắp ngang) | Đen, v3.0, Ngang |
| `VDP0X-200-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Dọc |
| `VDP0X-200-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Dọc |

### (V) Vỏ đèn — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 300W - Dùng ch…`

Dòng trong sheet: 33, 34, 35, 36

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-300-D-BK-v3.0` | …ung cho P01 và P03 (Lắp ngang) | Xám, v3.0, Ngang |
| `VDP0X-300-D-GY-v3.0` | …ung cho P01 và P03 (Lắp ngang) | Đen, v3.0, Ngang |
| `VDP0X-300-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Dọc |
| `VDP0X-300-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Dọc |

### (WPC) Cầu đấu — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Cầu đấu cái Module (F Type - IP68) | M15-2P, Loại: 2 ch…`

Dòng trong sheet: 8, 13, 18, 23

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `WPC-MDF-M15-2P-2B-NT-CD` | …ân (100W), Nối tiếp, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-2B-NT-DD` | …ân (100W), Nối tiếp, Đầu vào: Vít dây (Cầu đấu 2P) |
| `WPC-MDF-M15-2P-2B-SS-CD` | …ân (100W), Song song, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-2B-SS-DD` | …ân (100W), Song song, Đầu vào: Vít dây (Cầu đấu 2P) |

### (WPC) Cầu đấu — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Cầu đấu cái Module (F Type - IP68) | M15-2P, Loại: 3 ch…`

Dòng trong sheet: 9, 14, 19, 24

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `WPC-MDF-M15-2P-3B-NT-CD` | …ân (150W), Nối tiếp, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-3B-NT-DD` | …ân (150W), Nối tiếp, Đầu vào: Vít dây (Cầu đấu 2P) |
| `WPC-MDF-M15-2P-3B-SS-CD` | …ân (150W), Song song, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-3B-SS-DD` | …ân (150W), Song song, Đầu vào: Vít dây (Cầu đấu 2P) |

### (WPC) Cầu đấu — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Cầu đấu cái Module (F Type - IP68) | M15-2P, Loại: 4 ch…`

Dòng trong sheet: 10, 15, 20, 25

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `WPC-MDF-M15-2P-4B-NT-CD` | …ân (200W), Nối tiếp, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-4B-NT-DD` | …ân (200W), Nối tiếp, Đầu vào: Vít dây (Cầu đấu 2P) |
| `WPC-MDF-M15-2P-4B-SS-CD` | …ân (200W), Song song, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-4B-SS-DD` | …ân (200W), Song song, Đầu vào: Vít dây (Cầu đấu 2P) |

### (WPC) Cầu đấu — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Cầu đấu cái Module (F Type - IP68) | M15-2P, Loại: 5 ch…`

Dòng trong sheet: 11, 16, 21, 26

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `WPC-MDF-M15-2P-5B-NT-CD` | …ân (250W), Nối tiếp, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-5B-NT-DD` | …ân (250W), Nối tiếp, Đầu vào: Vít dây (Cầu đấu 2P) |
| `WPC-MDF-M15-2P-5B-SS-CD` | …ân (250W), Song song, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-5B-SS-DD` | …ân (250W), Song song, Đầu vào: Vít dây (Cầu đấu 2P) |

### (WPC) Cầu đấu — 4 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Cầu đấu cái Module (F Type - IP68) | M15-2P, Loại: 6 ch…`

Dòng trong sheet: 12, 17, 22, 27

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `WPC-MDF-M15-2P-6B-NT-CD` | …ân (300W), Nối tiếp, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-6B-NT-DD` | …ân (300W), Nối tiếp, Đầu vào: Vít dây (Cầu đấu 2P) |
| `WPC-MDF-M15-2P-6B-SS-CD` | …ân (300W), Song song, Đầu vào: Keo cos (Dây 2x0.75) |
| `WPC-MDF-M15-2P-6B-SS-DD` | …ân (300W), Song song, Đầu vào: Vít dây (Cầu đấu 2P) |

### (C) Chip LED — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 100W LED 2835 - Sử dụng: UFO X03 | T…`

Dòng trong sheet: 432, 433, 434

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C28DX03S100-428-40C-280LED` | …rung tính (4.000K - 4.200K), 2835, 100W, 40C, Điện áp cao, 2 |
| `C28DX03S100-528-40C-280LED` | …rắng (5.000K), 2835, 100W, 40C, Điện áp cao, 280LED |
| `C28DX03S100-628-40C-280LED` | …rắng (6.000K - 6.500K), 2835, 100W, 40C, Điện áp cao, 280LED |

### (C) Chip LED — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 150W LED 2835 - Sử dụng: UFO X03 | T…`

Dòng trong sheet: 436, 437, 438

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C28DX03S150-428-40C-280LED` | …rung tính (4.000K - 4.200K), 2835, 150W, 40C, Điện áp cao, 2 |
| `C28DX03S150-528-40C-280LED` | …rắng (5.000K), 2835, 150W, 40C, Điện áp cao, 280LED |
| `C28DX03S150-628-40C-280LED` | …rắng (6.000K - 6.500K), 2835, 150W, 40C, Điện áp cao, 280LED |

### (C) Chip LED — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 200W LED 2835 - Sử dụng: UFO X03 | T…`

Dòng trong sheet: 440, 441, 442

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C28DX03S200-428-40C-640LED` | …rung tính (4.000K - 4.200K), 2835, 200W, 40C, Điện áp cao, 6 |
| `C28DX03S200-528-40C-640LED` | …rắng (5.000K), 2835, 200W, 40C, Điện áp cao, 640LED |
| `C28DX03S200-628-40C-640LED` | …rắng (6.000K - 6.500K), 2835, 200W, 40C, Điện áp cao, 640LED |

### (C) Chip LED — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 300W LED 2835 - Sử dụng: UFO X03 | T…`

Dòng trong sheet: 444, 445, 446

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C28DX03S300-428-40C-920LED` | …rung tính (4.000K - 4.200K), 2835, 300W, 40C, Điện áp cao, 9 |
| `C28DX03S300-528-40C-920LED` | …rắng (5.000K), 2835, 300W, 40C, Điện áp cao, 920LED |
| `C28DX03S300-628-40C-920LED` | …rắng (6.000K - 6.500K), 2835, 300W, 40C, Điện áp cao, 920LED |

### (C) Chip LED — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip COB 30W LED TF - Sử dụng: Các mẫu COB: PTC, PTR, D…`

Dòng trong sheet: 90, 91, 92

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30C030-BTF` | …QL,... | Xanh dương, TF, 30W, 30VDC |
| `C30C030-GTF` | …QL,... | Xanh lá, TF, 30W, 30VDC |
| `C30C030-RTF` | …QL,... | Đỏ, TF, 30W, 30VDC |

### LED — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `EMC - LED 3030-EMC-1W/6V-150mA, 135-145lm/W; Ra80  | Tr…`

Dòng trong sheet: 2, 3, 4

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `EMC3030UNF2C-D160-VN` | …ung tính (4.000K - 4.200K) |
| `EMC3030UWF2C-D160-VN` | …ắng (5.000K) |
| `EMC3030UZF2C-D160-VN` | …ắng (6.000K - 6.500K) |

### (PTN) Tản nhiệt — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt module SMD Công suất 50W | Nhôm đùn trắng, An…`

Dòng trong sheet: 3, 4, 5

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-M30S050-A-HK-CG` | …ode hóa, HKLED, Vây tản nhiệt cong |
| `PTN-M30S050-A-HK-PG` | …ode hóa, HKLED, Vây tản nhiệt phẳng |
| `PTN-M30S050-A-OEM-PG` | …ode hóa, OEM, Vây tản nhiệt phẳng |

### (V) Vỏ đèn — 3 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 50W - Dùng chu…`

Dòng trong sheet: 19, 19, 20

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X` | …ng cho P01 và P03 |
| `VDP0X-050-D-BK-v3.0` | …ng cho P01 và P03 | Xám, v3.0, Dọc |
| `VDP0X-050-D-GY-v3.0` | …ng cho P01 và P03 | Đen, v3.0, Dọc |

### (C) Chip LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 100W LED 3030 - Sử dụng: UFO X01 | V…`

Dòng trong sheet: 411, 415

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX01S100-3B3-5C-110LED` | …àng (3.000K - 3.200K), Bridgelux 3030, 100W, 5C, 30VDC, 110L |
| `C30DX01S100-3P3-5C-110LED` | …àng (3.000K - 3.200K), Lumileds 3030, 100W, 5C, 30VDC, 110LE |

### (C) Chip LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 150W LED 3030 - Sử dụng: UFO X01 | V…`

Dòng trong sheet: 419, 423

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX01S150-3B3-5C-170LED` | …àng (3.000K - 3.200K), Bridgelux 3030, 150W, 5C, 30VDC, 170L |
| `C30DX01S150-3P3-5C-170LED` | …àng (3.000K - 3.200K), Lumileds 3030, 150W, 5C, 30VDC, 170LE |

### (C) Chip LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 200W LED 3030 - Sử dụng: UFO X01 | V…`

Dòng trong sheet: 427, 431

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX01S200-3B3-5C-220LED` | …àng (3.000K - 3.200K), Bridgelux 3030, 200W, 5C, 30VDC, 220L |
| `C30DX01S200-3P3-5C-220LED` | …àng (3.000K - 3.200K), Lumileds 3030, 200W, 5C, 30VDC, 220LE |

### (C) Chip LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 100W LED 3030 - Sử dụng: UFO X02 | V…`

Dòng trong sheet: 451, 455

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX02S100-3B3-7C` | …àng (3.000K - 3.200K), Bridgelux 3030, 100W, 7C, 42VDC |
| `C30DX02S100-3P3-7C` | …àng (3.000K - 3.200K), Lumileds 3030, 100W, 7C, 42VDC |

### (C) Chip LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 150W LED 3030 - Sử dụng: UFO X02 | V…`

Dòng trong sheet: 459, 463

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX02S150-3B3-7C-196LED` | …àng (3.000K - 3.200K), Bridgelux 3030, 150W, 7C, 42VDC, 196L |
| `C30DX02S150-3P3-7C-196LED` | …àng (3.000K - 3.200K), Lumileds 3030, 150W, 7C, 42VDC, 196LE |

### (C) Chip LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Chip đèn nhà xưởng 200W LED 3030 - Sử dụng: UFO X02 | V…`

Dòng trong sheet: 467, 471

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `C30DX02S200-3B3-7C` | …àng (3.000K - 3.200K), Bridgelux 3030, 200W, 7C, 42VDC |
| `C30DX02S200-3P3-7C` | …àng (3.000K - 3.200K), Lumileds 3030, 200W, 7C, 42VDC |

### (M) Module — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 200W LED 3030 - Sử dụng: Đèn pha P04 SMD | V…`

Dòng trong sheet: 125, 129

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M30S200-3B5-5C-288LED-DD` | …àng (3.000K - 3.200K), Bridgelux 3030, 5C, 30VDC, 288LED | D |
| `M30S200-3P3-5C-288LED-DD` | …àng (3.000K - 3.200K), Lumileds 3030, 5C, 30VDC, 288LED | Dâ |

### (M) Module — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Module SMD 200W LED 5050 - Sử dụng: Đèn pha P04 SMD | V…`

Dòng trong sheet: 133, 137

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `M50S200-3B5-5C-72LED-DD` | …àng (3.000K - 3.200K), Bridgelux 5050, 5C, 30VDC, 72LED | Dâ |
| `M50S200-3P5-5C-72LED-DD` | …àng (3.000K - 3.200K), Lumileds 5050, 5C, 30VDC, 72LED | Dây |

### LED — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `PCT - LED 5050 2W/6V/300mA/300-330LM.Ra70 1936*8 | Trắn…`

Dòng trong sheet: 22, 23

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PCT5050UWY2C4B-G330-VN` | …g (5.000K) |
| `PCT5050UZY2C4B-G330-VN` | …g (6.000K - 6.500K) |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Hộp nguồn vỏ đèn pha P0X - Dùng chung P01, P03, X01, X0…`

Dòng trong sheet: 40, 41

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PHN-VDP0X-BK-T-0.7mm-v1.1` | …3 | v1.1, Sơn: Xám, Vật liệu: Thép, Dày: 0.7mm |
| `PHN-VDP0X-GY-T-0.7mm-v1.1` | …3 | v1.1, Sơn: Đen, Vật liệu: Thép, Dày: 0.7mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 50W - Dùng chung …`

Dòng trong sheet: 2, 3

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-050-BK-T-1.0mm-v3.0` | …P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-050-GY-T-1.0mm-v3.0` | …P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 100W - Dùng chung…`

Dòng trong sheet: 4, 5

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-100-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-100-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 150W - Dùng chung…`

Dòng trong sheet: 6, 7

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-150-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-150-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 200W - Dùng chung…`

Dòng trong sheet: 8, 9

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-200-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-200-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 250W - Dùng chung…`

Dòng trong sheet: 10, 11

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-250-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-250-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 300W - Dùng chung…`

Dòng trong sheet: 12, 13

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-300-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-300-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 400W - Dùng chung…`

Dòng trong sheet: 14, 15

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-400-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-400-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### Linh phụ kiện gia công cơ khí — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Khung vỏ đèn pha module P0X Công suất 500W - Dùng chung…`

Dòng trong sheet: 16, 17

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PKG-VDP0X-500-BK-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Xám, Vật liệu: Thép, Dày: 1.0mm |
| `PKG-VDP0X-500-GY-T-1.0mm-v3.0` | … P01, P03 | v3.0, Sơn: Đen, Vật liệu: Thép, Dày: 1.0mm |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt module COB Công suất 50W | Anode hóa, HKLED, …`

Dòng trong sheet: 7, 8

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-M30C050-HK-CG` | …Vây tản nhiệt cong |
| `PTN-M30C050-HK-PG` | …Vây tản nhiệt phẳng |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường NP1 Chip LED SMD Công suất 150W …`

Dòng trong sheet: 196, 199

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDNP1S150-MG` | …| Vàng |
| `PTN-VDNP1S150-YL` | …| Xanh rêu |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường NP1 Chip LED SMD Công suất 200W …`

Dòng trong sheet: 197, 200

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDNP1S200-MG` | …| Vàng |
| `PTN-VDNP1S200-YL` | …| Xanh rêu |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường NP1 Chip LED SMD Công suất 400W …`

Dòng trong sheet: 198, 201

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDNP1S400-MG` | …| Vàng |
| `PTN-VDNP1S400-YL` | …| Xanh rêu |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường X02 Chip LED SMD Công suất 100W …`

Dòng trong sheet: 163, 164

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDX02S100-BN` | …| Nâu |
| `PTN-VDX02S100-GY` | …| Xám |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường X02 Chip LED SMD Công suất 150W …`

Dòng trong sheet: 165, 166

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDX02S150-BN` | …| Nâu |
| `PTN-VDX02S150-GY` | …| Xám |

### (PTN) Tản nhiệt — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Tản nhiệt vỏ đèn đường X02 Chip LED SMD Công suất 200W …`

Dòng trong sheet: 167, 168

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `PTN-VDX02S200-BN` | …| Nâu |
| `PTN-VDX02S200-GY` | …| Xám |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D11 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 190, 190

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD11` | … |
| `VDD11S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D12 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 196, 196

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD12` | … |
| `VDD12S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D13 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 202, 202

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD13` | … |
| `VDD13S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D14 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 208, 208

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD14` | … |
| `VDD14S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D15 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 214, 214

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD15` | … |
| `VDD15S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D21 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 230, 230

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD21` | … |
| `VDD21S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D22 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 235, 235

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD22` | … |
| `VDD22S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D23 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 240, 240

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD23` | … |
| `VDD23S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D24 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 245, 245

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD24` | … |
| `VDD24S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D25 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 250, 250

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD25` | … |
| `VDD25S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường D26 Chip LED SMD Công suất 50W…`

Dòng trong sheet: 255, 255

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD26` | … |
| `VDD26S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường BRP371 Chip LED SMD Công suất 150W…`

Dòng trong sheet: 260, 260

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD71S150` | … |
| `VDD7X` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn đường BRP391 Chip LED SMD Công suất 100W…`

Dòng trong sheet: 264, 264

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDD91S100` | … |
| `VDD9X` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn phòng nổ cây xăng NCX Công suất 100W…`

Dòng trong sheet: 165, 165

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDNCX` | … |
| `VDNCX-100` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn phòng nổ UFO NU1 Chip COB Công suất 50W…`

Dòng trong sheet: 157, 157

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDNU1` | … |
| `VDNU1C050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn phòng nổ UFO NU2 Chip SMD Công suất 100W…`

Dòng trong sheet: 162, 162

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDNU2` | … |
| `VDNU2S100` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hộp P02 Công suất 30W - Dùng ch…`

Dòng trong sheet: 2, 2

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP02` | …ung P02 (SMD/COB) và P04 (COB) |
| `VDP02-030-D-WH-v2.1` | …ung P02 (SMD/COB) và P04 (COB) | Trắng, v2.1, Dọc |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hộp P02 Công suất 100W - Dùng c…`

Dòng trong sheet: 4, 5

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP02-100-D-WH-v2.1` | …hung P02 (SMD/COB) và P04 (COB) (Lắp ngang) | Trắng, v2.1, N |
| `VDP02-100-N-WH-v2.1` | …hung P02 (SMD/COB) và P04 (COB) | Trắng, v2.1, Dọc |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hộp P02 Công suất 200W - Dùng c…`

Dòng trong sheet: 7, 8

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP02-200-D-WH-v2.1` | …hung P02 (SMD/COB) và P04 (COB) (Lắp ngang) | Trắng, v2.1, N |
| `VDP02-200-N-WH-v2.1` | …hung P02 (SMD/COB) và P04 (COB) | Trắng, v2.1, Dọc |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hộp P02 Công suất 300W - Dùng c…`

Dòng trong sheet: 10, 11

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP02-300-D-WH-v2.1` | …hung P02 (SMD/COB) và P04 (COB) (Lắp ngang) | Trắng, v2.1, N |
| `VDP02-300-N-WH-v2.1` | …hung P02 (SMD/COB) và P04 (COB) | Trắng, v2.1, Dọc |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 150W - Dùng ch…`

Dòng trong sheet: 25, 26

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-150-D-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Dọc |
| `VDP0X-150-D-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Dọc |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 1000W - Dùng c…`

Dòng trong sheet: 45, 46

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-1K0-N-BK-v3.0` | …hung cho P01 và P03 | Xám, v3.0, Ngang |
| `VDP0X-1K0-N-GY-v3.0` | …hung cho P01 và P03 | Đen, v3.0, Ngang |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 250W - Dùng ch…`

Dòng trong sheet: 31, 32

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-250-D-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Dọc |
| `VDP0X-250-D-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Dọc |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 400W - Dùng ch…`

Dòng trong sheet: 37, 38

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-400-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Ngang |
| `VDP0X-400-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Ngang |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 500W - Dùng ch…`

Dòng trong sheet: 39, 40

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-500-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Ngang |
| `VDP0X-500-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Ngang |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 600W - Dùng ch…`

Dòng trong sheet: 41, 42

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-600-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Ngang |
| `VDP0X-600-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Ngang |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha module khung hở P0X Công suất 800W - Dùng ch…`

Dòng trong sheet: 43, 44

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDP0X-800-N-BK-v3.0` | …ung cho P01 và P03 | Xám, v3.0, Ngang |
| `VDP0X-800-N-GY-v3.0` | …ung cho P01 và P03 | Đen, v3.0, Ngang |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha cẩu tháp PCT Chip COB Công suất 500W…`

Dòng trong sheet: 124, 124

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPCT` | … |
| `VDPCTC500` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha kẻ dọc PKD Chip COB Công suất 50W…`

Dòng trong sheet: 108, 108

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPKD` | … |
| `VDPKDC050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 10W | …`

Dòng trong sheet: 74, 75

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC010-65` | …IP65 |
| `VDPTRC010-66` | …IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 20W | …`

Dòng trong sheet: 76, 77

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC020-65` | …IP65 |
| `VDPTRC020-66` | …IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 30W | …`

Dòng trong sheet: 78, 79

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC030-65` | …IP65 |
| `VDPTRC030-66` | …IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 50W | …`

Dòng trong sheet: 80, 81

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC050-65` | …IP65 |
| `VDPTRC050-66` | …IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 100W |…`

Dòng trong sheet: 82, 83

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC100-65` | … IP65 |
| `VDPTRC100-66` | … IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 150W |…`

Dòng trong sheet: 84, 85

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC150-65` | … IP65 |
| `VDPTRC150-66` | … IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 200W |…`

Dòng trong sheet: 86, 87

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC200-65` | … IP65 |
| `VDPTRC200-66` | … IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 300W |…`

Dòng trong sheet: 88, 89

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC300-65` | … IP65 |
| `VDPTRC300-66` | … IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha tròn chóa rộng PTR Chip COB Công suất 400W |…`

Dòng trong sheet: 90, 91

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPTRC400-65` | … IP65 |
| `VDPTRC400-66` | … IP66 |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn pha sân vận động PVD Chip SMD Công suất 200W…`

Dòng trong sheet: 127, 127

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDPVD` | … |
| `VDPVDS200` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn nhà xưởng UFO X01 Công suất 50W…`

Dòng trong sheet: 138, 138

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDX01` | … |
| `VDX01S050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn nhà xưởng UFO X03 Công suất 100W…`

Dòng trong sheet: 148, 148

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDX03` | … |
| `VDX03S100` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn nhà xưởng highbay XHB Công suất 50W…`

Dòng trong sheet: 130, 130

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDXHB` | … |
| `VDXHBC050` | … |

### (V) Vỏ đèn — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Vỏ đèn nhà xưởng thể thao XTT Công suất 50W…`

Dòng trong sheet: 152, 152

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `VDXTT` | … |
| `VDXTTS050` | … |

### (WPC) Cầu đấu — 2 item hiện cùng dòng chữ

Người dùng nhìn thấy: `Cầu đấu đực Module (F Type - IP68) | M15-2P, Loại: Ốc c…`

Dòng trong sheet: 6, 7

| Mã | Phần bị cắt mất (chính là phần phân biệt) |
|---|---|
| `WPC-MDM-M15-2P-PGM` | …hống nước (Ren mịn) |
| `WPC-MDM-M15-2P-PGT` | …hống nước (Ren thô) |

