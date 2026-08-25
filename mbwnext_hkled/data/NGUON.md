# Nguồn của các file CSV trong `data/`

**Cập nhật:** 25/08/2026

File CSV trong `danh_muc/` và `thanh_pham/` **không do code nào sinh ra**. Chúng được **tải tay**
từ Google Sheet của HKLED rồi commit. Không có mã tải trong repo.

Hệ quả phải biết:

| Rủi ro | Đọc-theo-tên-cột có đỡ được không? |
|---|---|
| Khách **đảo thứ tự cột** hoặc đổi cách đặt dấu nháy | ✅ đỡ được — chỉ tạo diff toàn file khó rà, dữ liệu vẫn đúng |
| Khách **sửa giá trị** trên sheet mà không ai tải lại | ❌ **không** — repo và sheet lệch âm thầm, `bench migrate` vẫn chạy và vẫn báo thành công |
| Khách **bỏ hẳn một cột** đang dùng | ❌ **không** — vỡ ở tầng bộ nạp |
| Không biết bản đang có chụp lúc nào | ❌ lúc số liệu lệch thì không lần được là khách đổi hay mình nạp sót |

Bảng dưới để trả lời câu hỏi đầu tiên khi số liệu lệch: **bản này cũ tới đâu, lấy từ đâu.**

⚠ Cột *Ngày vào repo* lấy từ commit đầu tiên thêm file, tức **cận trên** của ngày tải thật —
không phải mốc chính xác. Từ nay tải file mới thì ghi thẳng ngày tải vào đây.

## Sổ nguồn

| File | Số dòng | sha256 (12 ký tự đầu) | Ngày vào repo |
|---|---|---|---|
| `00-o-oc-vit-bulong.csv` | 48 | `18bf3c8202e2` | 2026-08-11 |
| `01-pcb.csv` | 44 | `5526d54e32c0` | 2026-08-11 |
| `02-led.csv` | 32 | `e63ed8fc729a` | 2026-08-11 |
| `03-c-chip-led.csv` | 626 | `a8baeb4a4543` | 2026-08-11 |
| `04-m-module.csv` | 152 | `bdb151bb9dc5` | 2026-08-11 |
| `05-v-vo-den.csv` | 265 | `78f0e38a4a8c` | 2026-08-11 |
| `06-n-nguon.csv` | 263 | `8a7b6536e55d` | 2026-08-11 |
| `07-spd-chong-set.csv` | 16 | `f804ab807ccb` | 2026-08-11 |
| `08-wpc-cau-dau.csv` | 34 | `359b90dfa59e` | 2026-08-11 |
| `09-linh-phu-kien-gia-cong-co-khi.csv` | 43 | `1c41663d5746` | 2026-08-11 |
| `10-ptn-tan-nhiet-phan-truc-tiep.csv` | 200 | `fa094429caa0` | 2026-08-11 |
| `11-pls-lens.csv` | 82 | `eaf34a0e2536` | 2026-08-19 |
| `12-pca-chao-den.csv` | 23 | `8e8e486fb9c3` | 2026-08-25 |
| `13-pcd-tru-bat-can-den.csv` | 15 | `3bbfc23af6ce` | 2026-08-25 |
| `14-pdd-phan-dau-den-duong.csv` | 10 | `8c5236f8c41a` | 2026-08-25 |
| `15-pgn-gong-nep-khoa-gai.csv` | 23 | `8e57e1bbbc4c` | 2026-08-25 |
| `16-phn-hop-nguon-khoang-nguon.csv` | 32 | `c24b41d5b0f2` | 2026-08-25 |
| `17-pki-kinh.csv` | 119 | `f05fae92a185` | 2026-08-25 |
| `18-pmt-moc-treo.csv` | 5 | `b9366db26971` | 2026-08-25 |
| `19-pnh-nap-hop.csv` | 107 | `87294f17f3e0` | 2026-08-25 |
| `20-pnl-nap-thanh-che-day-dien.csv` | 29 | `3104abd074ad` | 2026-08-25 |
| `21-ppq-choa-phan-quang.csv` | 94 | `0d8907468e4b` | 2026-08-25 |
| `22-pqu-quai-den.csv` | 61 | `57f8cebaf542` | 2026-08-25 |
| `23-pta-tai.csv` | 13 | `8f9911e98c67` | 2026-08-25 |
| `24-pvi-vien-mat-truoc.csv` | 74 | `ff14905f0c80` | 2026-08-25 |
| `25-pzn-gioang-vien-hop-nguon.csv` | 101 | `a97587d86e82` | 2026-08-25 |
| `26-slp-linh-phu-kien-tru-cot.csv` | 8 | `743ea604ce07` | 2026-08-25 |
| `27-tse-linh-phu-kien-nlmt.csv` | 77 | `8c1a6152c46c` | 2026-08-25 |
| `28-pzk-gioang-kinh-lens.csv` | 118 | `50c0a4f90325` | 2026-08-25 |
| `29-hct-hop-carton.csv` | 94 | `b33cca4c62f9` | 2026-08-25 |
| `01-nhom-i-module.csv` | 33640 | `398cee3b3e9c` | 2026-08-17 |
| `02-nhom-ii-cob.csv` | 12516 | `ea0ac26b1cb9` | 2026-08-17 |
| `03-nhom-iii-chip-module.csv` | 4800 | `6f55158f505d` | 2026-08-17 |
| `04-nhom-iv-khac.csv` | 8012 | `e7e0cb17ff99` | 2026-08-17 |

## Sheet nguồn đã biết

Bốn sheet dưới đây là các workbook đã dùng để tải. **Chưa map được từng file → từng sheet/gid**,
trừ trường hợp ghi rõ bên dưới.

| Workbook | Dùng cho |
|---|---|
| `13WwnFkR4RjsQ0Dx5RcirO9k7UD8f7StLIeUwuJoMig8` | *(chưa xác định)* |
| `1bu7QScvClDFbZHske_YtIPCdhc_Pv2Pj5hJD9rs4PEc` | *(chưa xác định)* |
| `1J9-mwkS8a4uKhEv0p6iAYM2w45n7K4nM56AOEpS2NHQ` | *(chưa xác định)* |
| `1jX3qxiPOvM2rif23s6hcmztRM9V9CLIAb2KTtYqx1tc` | *(chưa xác định)* |

Trường hợp đã truy được rõ:

- `danh_muc/04-m-module.csv` — sheet **`(M) Module`**, `gid=1424293139`, tải **25/08/2026** sau khi
  khách sửa 56 mã B5/B3. Sheet cũ khách đổi tên thành *"(M) Module (cũ không dùng nữa)"*.
  ⚠ Tải sheet theo `&sheet=<tên>` **không hoạt động** với link chia sẻ ẩn danh — nó lặng lẽ trả về
  sheet đầu tiên. Phải dùng `&gid=<số>`, lấy gid bằng cách bấm vào tab rồi đọc trên thanh địa chỉ.
- `thanh_pham/01..04-*.csv` — 4 sheet *Nhóm I–IV*, tải **25/08/2026**, thay bản 3 cột cũ bằng bản
  đủ 11–13 cột.

## Lỗ hổng đã biết trong dữ liệu nguồn

### `danh_muc/04-m-module.csv` — trống cột *Nhóm sản phẩm*, cả 152 dòng

Phát hiện 25/08/2026 khi dựng thử site trắng `test.com`. Đây là file **duy nhất** trong 34 file
có ô nhóm để trống, và nó trống **toàn bộ**: 152/152 dòng, 8 mã cha
(`M30C050`, `M30S030`, `M30S050-A`, `M30S050-B`, `M30S200`, `M50S050-A`, `M50S050-B`, `M50S200`).

Không phải lỗi lúc tải — file này là 1 trong 2 file truy được rõ nguồn (sheet `(M) Module`,
`gid=1424293139`), tải lại vẫn thế. **Sheet của khách thật sự không có nhóm cho 8 mã này.**

Vì sao chưa ai thấy: trên `hkled.com` cả 8 mã đã tồn tại từ trước với `item_group = (M) Module`,
nên bộ nạp gặp `frappe.db.exists` là bỏ qua, không bao giờ chạm tới ô trống. Chỉ site trắng mới lộ.

⚠ **Không tự điền `(M) Module` vào file.** Suy từ tên file ra giá trị dữ liệu là đúng đúng-một-lần
rồi thành thói quen — lần sau tên file không nói lên nhóm thì sai mà vẫn chạy. Nhóm sản phẩm là
dữ liệu của khách, phải do khách điền vào sheet rồi tải lại.

Trong lúc chờ: bộ nạp bỏ qua 8 mã cha này kèm mọi biến thể của chúng và in ra danh sách
(`bo_qua["thieu_nhom"]`). Site mới sẽ **thiếu 152 dòng module** cho tới khi khách bổ sung —
mà module là linh kiện BOM Template tra tới, nên phải bổ sung trước khi dựng cổng thật.

### Thiếu hẳn 2 nhóm sản phẩm trong bộ file khách gửi

`data/danh_muc/` có 30 file, phủ ốc vít, PCB, LED, chip, module, vỏ, nguồn, chống sét, cầu đấu,
tản nhiệt, lens, chảo, trụ, gông, kính, móc treo, nắp, choá, quai, tai, viền, gioăng, hộp carton…
**Không có file nào cho dây điện và mút xốp.** Hai nhóm này tồn tại trên `hkled.com` nhưng không
có trong bất kỳ CSV nào — do Administrator tạo tay.

| Nhóm | Số mã trên site | Có trong CSV | Chặn BOM Template? |
|---|---|---|---|
| `(W) Dây điện` | 7 | **0 — thiếu cả nhóm** | ✅ `W-2x0.75-BK` (4 rule), `W-3x0.75-BK` (2 rule) |
| `(XOP) Mút, xốp` | 6 | **0 — thiếu cả nhóm** | ✅ `XOP-GOC-110x110x120mm` (2 rule) |
| `(O) Ốc, vít, bulong` | 70 | 66 (`00-o-oc-vit-bulong.csv`) | ❌ 4 mã `OPG*` thiếu nhưng **0 rule tra tới** |

Cách hỏi khách cho gọn: **xin danh mục 2 nhóm `(W) Dây điện` và `(XOP) Mút, xốp`** — 13 mã, trong
đó 2 là mặt hàng cha (`WIRE`, `XOP-GOC`). Đừng hỏi thành "19 mã lẻ": 4 mã `OPG*` thuộc nhóm đã có
file sẵn (chỉ thiếu dòng, không chặn gì), còn `DD11S050` và `dịch vụ gia công` là mã thử.

## Việc nên làm, chưa làm

1. **Map từng file → sheet + gid.** Hiện chỉ biết workbook, không biết tab. Thiếu cái này thì
   không tải lại đúng bản được.
2. **Script đối chiếu** — tải lại về thư mục tạm, so sha256 với bảng trên, in ra file nào đã lệch.
   Chỉ đọc và báo, **không tự ghi đè**: khách sửa sheet có thể là sửa đúng, cũng có thể là sửa
   nhầm, không để máy tự quyết.
3. Ghi ngày tải thật ngay lúc tải, thay cho cột *Ngày vào repo* mang tính cận trên.
