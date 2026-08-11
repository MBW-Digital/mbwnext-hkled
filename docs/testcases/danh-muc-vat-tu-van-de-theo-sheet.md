# Vấn đề trong bảng nguồn — liệt kê theo từng sheet (PM-TASK-00061)

Số dòng ghi theo **đúng số dòng trong Google Sheet** (đã tính dòng tiêu đề), mở bảng là thấy ngay.

| Sheet | Tổng dòng | Nạp được | Chưa nạp |
|---|---|---|---|
| (O) Ốc, vít, bulong | 46 | 46 | **0** |
| PCB | 44 | 44 | **0** |
| LED | 32 | 32 | **0** |
| (C) Chip LED | 626 | 559 | **67** |
| (M) Module | 136 | 104 | **32** |
| (V) Vỏ đèn | 265 | 252 | **13** |
| (N) Nguồn | 74 | 51 | **23** |
| (SPD) Chống sét | 16 | 16 | **0** |
| (WPC) Cầu đấu | 34 | 34 | **0** |
| Linh phụ kiện gia công cơ khí | 43 | 37 | **6** |
| (PTN) Tản nhiệt (Phần trực tiếp gắn chip LED) | 200 | 183 | **17** |

---

## (C) Chip LED

### Trùng mã biến thể, nội dung khác nhau — 22 mã

| Dòng | Mã biến thể | Khác nhau ở |
|---|---|---|
| 108, 112 | `C30C050-3B3-5C` | **Số lượng LED**: 49 vs 50 |
| 96, 100 | `C30C050-3P3-5C` | **Số lượng LED**: 49 vs 50 |
| 107, 111 | `C30C050-4B3-5C` | **Số lượng LED**: 49 vs 50 |
| 95, 99 | `C30C050-4P3-5C` | **Số lượng LED**: 49 vs 50 |
| 106, 110 | `C30C050-5B3-5C` | **Số lượng LED**: 49 vs 50 |
| 94, 98 | `C30C050-5P3-5C` | **Số lượng LED**: 49 vs 50 |
| 105, 109 | `C30C050-6B3-5C` | **Số lượng LED**: 49 vs 50 |
| 93, 97 | `C30C050-6P3-5C` | **Số lượng LED**: 49 vs 50 |
| 29, 33 | `CM30S050-3B3-5C` | **Số lượng LED**: 64 vs 50 |
| 13, 17 | `CM30S050-3P3-5C` | **Số lượng LED**: 64 vs 50 |
| 28, 32 | `CM30S050-4B3-5C` | **Số lượng LED**: 64 vs 50 |
| 12, 16 | `CM30S050-4P3-5C` | **Số lượng LED**: 64 vs 50 |
| 27, 31 | `CM30S050-5B3-5C` | **Số lượng LED**: 64 vs 50 |
| 11, 15 | `CM30S050-5P3-5C` | **Số lượng LED**: 64 vs 50 |
| 26, 30 | `CM30S050-6B3-5C` | **Số lượng LED**: 64 vs 50 |
| 10, 14 | `CM30S050-6P3-5C` | **Số lượng LED**: 64 vs 50 |
| 120, 123 | `COBC050-3CR` | **Điện áp**: 30VDC vs 42VDC |
| 126, 129, 132 | `COBC050-3TF` | **Điện áp**: 30VDC vs 24VDC vs 12VDC |
| 119, 122 | `COBC050-4CR` | **Điện áp**: 30VDC vs 42VDC |
| 125, 128, 131 | `COBC050-4TF` | **Điện áp**: 30VDC vs 24VDC vs 12VDC |
| 118, 121 | `COBC050-6CR` | **Điện áp**: 30VDC vs 42VDC |
| 124, 127, 130 | `COBC050-6TF` | **Điện áp**: 30VDC vs 24VDC vs 12VDC |

### Mặt hàng cha có biến thể lệch bộ đặc tính — 2 cha

**`C30C030`**

| Dòng | Có giá trị ở các cột | Thiếu |
|---|---|---|
| 82, 83, 84, 85, 86, 87, 88, 89 | Màu ánh sáng, Loại LED, Công suất, Mạch, Điện áp, Kích thước LED, Số lượng LED | — |
| 90, 91, 92 | Màu ánh sáng, Loại LED, Công suất, Điện áp | Mạch, Kích thước LED, Số lượng LED |

**`C30C050`**

| Dòng | Có giá trị ở các cột | Thiếu |
|---|---|---|
| 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104 … | Màu ánh sáng, Loại LED, Công suất, Mạch, Điện áp, Kích thước LED, Số lượng LED | — |
| 117 | Màu ánh sáng, Loại LED, Công suất, Kích thước LED | Mạch, Điện áp, Số lượng LED |

## (M) Module

### Trùng mã biến thể, nội dung khác nhau — 16 mã

| Dòng | Mã biến thể | Khác nhau ở |
|---|---|---|
| 33, 41 | `M30S050-3B5-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 81, 89 | `M30S050-3B5-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 13, 21 | `M30S050-3P3-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 61, 69 | `M30S050-3P3-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 32, 40 | `M30S050-4B5-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 80, 88 | `M30S050-4B5-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 12, 20 | `M30S050-4P3-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 60, 68 | `M30S050-4P3-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 31, 39 | `M30S050-5B5-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 79, 87 | `M30S050-5B5-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 11, 19 | `M30S050-5P3-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 59, 67 | `M30S050-5P3-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 30, 38 | `M30S050-6B5-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 78, 86 | `M30S050-6B5-5C-CD-B` | **Số lượng LED**: 64 vs 50 |
| 10, 18 | `M30S050-6P3-5C-CD-A` | **Số lượng LED**: 64 vs 50 |
| 58, 66 | `M30S050-6P3-5C-CD-B` | **Số lượng LED**: 64 vs 50 |

## (V) Vỏ đèn

### Trùng mã biến thể, nội dung khác nhau — 1 mã

| Dòng | Mã biến thể | Khác nhau ở |
|---|---|---|
| 143, 145, 147 | `-BN` | **Công suất**: 100 vs 150 vs 200 |

### Mặt hàng cha có biến thể lệch bộ đặc tính — 1 cha

**`VDPXH`**

| Dòng | Có giá trị ở các cột | Thiếu |
|---|---|---|
| 99, 100, 101 | Công suất, Phân loại vỏ | — |
| 92, 93, 94, 95, 96, 97, 98 | Công suất | Phân loại vỏ |

## (N) Nguồn

### Mặt hàng cha có biến thể lệch bộ đặc tính — 1 cha

**`NHK`**

| Dòng | Có giá trị ở các cột | Thiếu |
|---|---|---|
| 23, 24 | Model, Công suất, Điện áp vào, Điện áp ra, Tương thích chip LED, Dimming, Tính năng, Xuất xứ | — |
| 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 … | Model, Công suất, Điện áp vào, Điện áp ra, Tương thích chip LED, Dimming, Xuất xứ | Tính năng |

## Linh phụ kiện gia công cơ khí

### Hai mã khác nhau nhưng tổ hợp đặc tính giống hệt

| Dòng | Các mã | Thiếu cột phân biệt |
|---|---|---|
| 28, 31 | `PQU-VDP0X-D-WH-T-3.0mm-v2.0`, `PQU-VDP0X-N-WH-T-3.0mm-v2.0` | bảng không có cột nào tả khác biệt giữa chúng |
| 29, 32 | `PQU-VDP0X-D-BK-T-3.0mm-v2.0`, `PQU-VDP0X-N-BK-T-3.0mm-v2.0` | bảng không có cột nào tả khác biệt giữa chúng |
| 30, 33 | `PQU-VDP0X-D-GY-T-3.0mm-v2.0`, `PQU-VDP0X-N-GY-T-3.0mm-v2.0` | bảng không có cột nào tả khác biệt giữa chúng |

## (PTN) Tản nhiệt (Phần trực tiếp gắn chip LED)

### Trùng mã biến thể, nội dung khác nhau — 1 mã

| Dòng | Mã biến thể | Khác nhau ở |
|---|---|---|
| 73, 74 | `PTN-VDD13S250` | **Công suất**: 250 vs 300 |

### Mặt hàng cha có biến thể lệch bộ đặc tính — 1 cha

**`PTN-VDPXH`**

| Dòng | Có giá trị ở các cột | Thiếu |
|---|---|---|
| 35, 36, 37 | Công suất, Hình dạng | — |
| 27, 28, 29, 30, 31, 32, 33, 34 | Công suất | Hình dạng |

### Hai mã khác nhau nhưng tổ hợp đặc tính giống hệt

| Dòng | Các mã | Thiếu cột phân biệt |
|---|---|---|
| 197, 198 | `PTN-VDNP1S200-YL`, `PTN-VDNP1S400-YL` | bảng không có cột nào tả khác biệt giữa chúng |
| 200, 201 | `PTN-VDNP1S200-MG`, `PTN-VDNP1S400-MG` | bảng không có cột nào tả khác biệt giữa chúng |


---

# Vấn đề về TÊN HIỂN THỊ — cũng theo từng sheet

Không chặn việc nạp, nhưng ảnh hưởng trực tiếp tới người dùng khi chọn hàng.

| Sheet | Biến thể bị cắt tên trùng nhau | Cha trùng tên với biến thể | Tên có 2 dấu cách |
|---|---|---|---|
| (O) Ốc, vít, bulong | 0 cha / 0 biến thể | 0 | 0 |
| PCB | 0 cha / 0 biến thể | 0 | 0 |
| LED | 2 cha / 8 biến thể | 0 | 8 |
| (C) Chip LED | 63 cha / 533 biến thể | 0 | 0 |
| (M) Module | 6 cha / 120 biến thể | 0 | 0 |
| (V) Vỏ đèn | 3 cha / 33 biến thể | 25 | 0 |
| (N) Nguồn | 0 cha / 0 biến thể | 0 | 2 |
| (SPD) Chống sét | 0 cha / 0 biến thể | 0 | 0 |
| (WPC) Cầu đấu | 0 cha / 0 biến thể | 0 | 0 |
| Linh phụ kiện gia công cơ khí | 1 cha / 2 biến thể | 0 | 0 |
| (PTN) Tản nhiệt (Phần trực tiếp gắn chip LED) | 3 cha / 19 biến thể | 0 | 0 |

## LED

**Biến thể hiện chữ y hệt nhau trên danh sách** (55 ký tự đầu trùng) — 2 mặt hàng cha:

| Mặt hàng cha | Số biến thể | Đoạn chữ người dùng nhìn thấy |
|---|---|---|
| `LED-EMC5050` | 4 | EMC - LED EMC 5050 6V 2W/6V/300mA/300-330LM .Ra70 1936*… |
| `LED-EMC7070` | 4 | EMC - LED EMC 7070 54V 5W/54V/100mA /800-900LM ,Ra90 22… |

**Tên có hai dấu cách liền** — 8 dòng: 2 (`EMC3030UWF2C-D160-VN`), 3 (`EMC3030UZF2C-D160-VN`), 4 (`EMC3030UNF2C-D160-VN`), 5 (`EMC3030USF2C-D160-VN`), 14 (`PCT3030UWF2C-K140-VN`), 15 (`PCT3030UZF2C-K140-VN`), 16 (`PCT3030UNF2C-K140-VN`), 17 (`PCT3030USF2C-K140-VN`)

## (C) Chip LED

**Biến thể hiện chữ y hệt nhau trên danh sách** (55 ký tự đầu trùng) — 63 mặt hàng cha:

| Mặt hàng cha | Số biến thể | Đoạn chữ người dùng nhìn thấy |
|---|---|---|
| `CM30S050` | 32 | Chip Module SMD 50W LED 3030 - Sử dụng: Module SMD 50W;… |
| `C30C050` | 25 | Chip COB 50W LED 3030 - Sử dụng: Các mẫu COB: PTC, PTR,… |
| `CM30S030` | 8 | Chip Module SMD 30W LED 3030 - Sử dụng: Module SMD 10W,… |
| `CM50S050` | 8 | Chip Module SMD 50W LED 5050 - Sử dụng: Module SMD 50W;… |
| `CM30C050` | 8 | Chip Module SMD 50W LED 3030 - Sử dụng: Module COB 50W … |
| `CM30S200` | 8 | Chip Module SMD 200W LED 3030 - Sử dụng: Module SMD 200… |
| `CM50S200` | 8 | Chip Module SMD 200W LED 5050 - Sử dụng: Module SMD 200… |
| `C30C010` | 8 | Chip COB 10W LED 3030 - Sử dụng: Các mẫu sử dụng chip C… |
| `C50C100` | 8 | Chip COB 100W LED 5050 - Sử dụng: Các mẫu COB: PTC, PTR… |
| `C30DD7XS050` | 8 | Chip đèn đường 50W LED 3030 - Sử dụng: Đèn đường BRP37X… |
| `C50DD7XS050` | 8 | Chip đèn đường 50W LED 5050 - Sử dụng: Đèn đường BRP37X… |
| `C30DD9XS100` | 8 | Chip đèn đường 100W LED 3030 - Sử dụng: Đèn đường BRP39… |
| … | | còn 51 mặt hàng cha nữa |

## (M) Module

**Biến thể hiện chữ y hệt nhau trên danh sách** (55 ký tự đầu trùng) — 6 mặt hàng cha:

| Mặt hàng cha | Số biến thể | Đoạn chữ người dùng nhìn thấy |
|---|---|---|
| `M30S050-A` | 40 | Module SMD 50W LED 3030 (Mẫu A) - Sử dụng: P01-03; D01-… |
| `M30S050-B` | 40 | Module SMD 50W LED 3030 (Mẫu B) - Sử dụng: P01-03; D01-… |
| `M30C050` | 16 | Module COB 50W LED 3030 - Sử dụng: P01-03; D01-06; NCX … |
| `M30S030` | 8 | Module SMD 30W LED 3030 - Sử dụng: P02 10W, 20W, 30W | … |
| `M50S050-A` | 8 | Module SMD 50W LED 5050 (Mẫu A) - Sử dụng: P01-03; D01-… |
| `M50S050-B` | 8 | Module SMD 50W LED 5050 (Mẫu B) - Sử dụng: P01-03; D01-… |

## (V) Vỏ đèn

**Biến thể hiện chữ y hệt nhau trên danh sách** (55 ký tự đầu trùng) — 3 mặt hàng cha:

| Mặt hàng cha | Số biến thể | Đoạn chữ người dùng nhìn thấy |
|---|---|---|
| `VDDQL` | 18 | Vỏ đèn đường quạt (đèn đường lá) DQL Chip COB Công suất… |
| `VDPXH` | 10 | Vỏ đèn pha rọi xám hộp nguồn sau PXH Chip COB Công suất… |
| `VDPVL` | 5 | Vỏ đèn pha viền mắt lồi hộp nguồn sau PVL Chip COB Công… |

**Mặt hàng cha trùng tên y hệt với một biến thể của nó** — 25:

| Mã cha | Mã biến thể trùng tên | Dòng | Tên |
|---|---|---|---|
| `VDPXH` | `VDPXHC010` | 92 | Vỏ đèn pha rọi xám hộp nguồn sau PXH Chip COB Công suất 10W |
| `VDPKD` | `VDPKDC050` | 108 | Vỏ đèn pha kẻ dọc PKD Chip COB Công suất 50W |
| `VDPVL` | `VDPVLC100` | 113 | Vỏ đèn pha viền mắt lồi hộp nguồn sau PVL Chip COB Công suất 100W |
| `VDPCT` | `VDPCTC500` | 124 | Vỏ đèn pha cẩu tháp PCT Chip COB Công suất 500W |
| `VDPVD` | `VDPVDS200` | 127 | Vỏ đèn pha sân vận động PVD Chip SMD Công suất 200W |
| `VDXHB` | `VDXHBC050` | 130 | Vỏ đèn nhà xưởng highbay XHB Công suất 50W |
| `VDX01` | `VDX01S050` | 138 | Vỏ đèn nhà xưởng UFO X01 Công suất 50W |
| `VDX03` | `VDX03S100` | 148 | Vỏ đèn nhà xưởng UFO X03 Công suất 100W |
| `VDXTT` | `VDXTTS050` | 152 | Vỏ đèn nhà xưởng thể thao XTT Công suất 50W |
| `VDNU1` | `VDNU1C050` | 157 | Vỏ đèn phòng nổ UFO NU1 Chip COB Công suất 50W |
| `VDNU2` | `VDNU2S100` | 162 | Vỏ đèn phòng nổ UFO NU2 Chip SMD Công suất 100W |
| `VDNCX` | `VDNCX-100` | 165 | Vỏ đèn phòng nổ cây xăng NCX Công suất 100W |
| `VDD11` | `VDD11S050` | 190 | Vỏ đèn đường D11 Chip LED SMD Công suất 50W |
| `VDD12` | `VDD12S050` | 196 | Vỏ đèn đường D12 Chip LED SMD Công suất 50W |
| `VDD13` | `VDD13S050` | 202 | Vỏ đèn đường D13 Chip LED SMD Công suất 50W |
| `VDD14` | `VDD14S050` | 208 | Vỏ đèn đường D14 Chip LED SMD Công suất 50W |
| `VDD15` | `VDD15S050` | 214 | Vỏ đèn đường D15 Chip LED SMD Công suất 50W |
| `VDD21` | `VDD21S050` | 230 | Vỏ đèn đường D21 Chip LED SMD Công suất 50W |
| `VDD22` | `VDD22S050` | 235 | Vỏ đèn đường D22 Chip LED SMD Công suất 50W |
| `VDD23` | `VDD23S050` | 240 | Vỏ đèn đường D23 Chip LED SMD Công suất 50W |
| `VDD24` | `VDD24S050` | 245 | Vỏ đèn đường D24 Chip LED SMD Công suất 50W |
| `VDD25` | `VDD25S050` | 250 | Vỏ đèn đường D25 Chip LED SMD Công suất 50W |
| `VDD26` | `VDD26S050` | 255 | Vỏ đèn đường D26 Chip LED SMD Công suất 50W |
| `VDD7X` | `VDD71S150` | 260 | Vỏ đèn đường BRP371 Chip LED SMD Công suất 150W |
| `VDD9X` | `VDD91S100` | 264 | Vỏ đèn đường BRP391 Chip LED SMD Công suất 100W |

## (N) Nguồn

**Tên có hai dấu cách liền** — 2 dòng: 48 (`NPLD-065W`), 59 (`NPLT-150W300X`)

## Linh phụ kiện gia công cơ khí

**Biến thể hiện chữ y hệt nhau trên danh sách** (55 ký tự đầu trùng) — 1 mặt hàng cha:

| Mặt hàng cha | Số biến thể | Đoạn chữ người dùng nhìn thấy |
|---|---|---|
| `PHN-VDP0X` | 2 | Hộp nguồn vỏ đèn pha P0X - Dùng chung P01, P03, X01, X0… |

## (PTN) Tản nhiệt (Phần trực tiếp gắn chip LED)

**Biến thể hiện chữ y hệt nhau trên danh sách** (55 ký tự đầu trùng) — 3 mặt hàng cha:

| Mặt hàng cha | Số biến thể | Đoạn chữ người dùng nhìn thấy |
|---|---|---|
| `PTN-VDPTC` | 7 | Tản nhiệt vỏ dùng chung đèn pha PTC/PTR Chip LED COB Cô… |
| `PTN-VDPVL` | 6 | Tản nhiệt vỏ đèn pha viền mắt lồi PVL Chip LED COB Công… |
| `PTN-VDD13` | 6 | Tản nhiệt vỏ đèn đường dùng chung D13 và D14 Chip LED S… |

