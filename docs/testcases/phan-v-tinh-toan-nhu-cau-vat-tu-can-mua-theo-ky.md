# Test case — Phần V · Tính nhu cầu vật tư cần mua theo kỳ (PM-FEAT-00030)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`, mở bằng
`http://dev.mbwnext.com:8012`
**Ngày chạy vòng tự kiểm:** 05/09/2026 ~11:30 · **Người chạy:** Claude (Trợ lý HKLed 1)

Đầu bài: `docs/features/phan-v-tinh-toan-nhu-cau-vat-tu-can-mua-theo-ky.md`
Code: `api/nhu_cau_vat_tu.py` · Màn hình: `page/tinh_nhu_cau_vat_tu/`

> ### ⚠ Vì sao file này ra muộn — đọc trước
>
> Tính năng này **không có ca test nào** cho tới hôm nay, trong khi công thức đã **đổi hai lần**
> (cách B ngày 03/09, trừ bán thành phẩm trong kho ngày 05/09) và nó ra **con số đi mua hàng thật**.
> Hai lần đổi đó chỉ được đo tay rồi ghi vào đầu bài. File này là lưới an toàn cho lần sửa thứ ba.
>
> ### Cách chạy: gọi thẳng hàm, KHÔNG ghi gì
>
> Engine là **chỉ đọc** theo thiết kế, nên chạy nó không cần dựng chứng từ. Mọi ca dưới đây gọi
> thẳng hàm trong `api/nhu_cau_vat_tu.py`. `TC-REGR-02` chứng minh việc đó bằng cách đếm **8 bảng
> trước và sau** hai lượt chạy đầy đủ.
>
> ### ⚠ Bẫy khi chạy lại — mất 4 lượt của tôi
>
> `bench execute` **nuốt lỗi thật và in ra `NameError: name 'mbwnext_hkled' is not defined`**.
> Lỗi thật (`TypeError`, `KeyError`…) nằm **phía trên** trong vệt lỗi. Đừng đi tìm lỗi import —
> lọc bằng `grep -iE "^[A-Za-z]*(Error|Exception)"` rồi đọc dòng **đầu tiên**.
>
> ### 🔴 Số trên site đổi trong ngày — mọi con số dưới đây có mốc thời gian
>
> Anh Thắng dựng và duyệt đơn thật trong lúc bộ test chạy. Trong đúng buổi sáng 05/09, đơn mua của
> `NVL 3` đổi từ *2 dòng (hẹn 02-09 còn 7 · hẹn 05-09 còn 2)* thành *1 dòng (hẹn 07-09 còn 10)*.
> **Đo lại ra số khác thì đừng vội ghi Fail** — kiểm lại hiện trạng trước.

---

## Điều kiện chuẩn bị

| Cần gì | Giá trị |
|---|---|
| **Địa chỉ site** | `http://dev.mbwnext.com:8012` (KHÔNG dùng `hkled.com` — nó trỏ ra IP thật) |
| **Màn hình** | `/app/tinh-nhu-cau-vat-tu` |
| **Công ty** | `HKLED` |

**Hiện trạng đo lúc 05/09 11:3x** — mọi ca dưới đây dựa trên đây:

| Thứ | Giá trị |
|---|---|
| Phần ghim của đơn khác | `Thành phẩm 1` 31 · `NVL 2` 26 · `NVL 1` 13 · `NVL 3` 7 · `Bán thành phẩm 1` 6 · `Bán thành phẩm 2` 1 |
| Tồn `Thành phẩm 1` | 31 — **ghim đúng 31 nên tồn khả dụng bằng 0** |
| Đơn mua còn hàng chưa về | **đúng 1 dòng**: `PO-26-00004` · `NVL 3` · hẹn **07-09** · còn **10** |
| Đơn bán đã duyệt trống *Thời Gian Bắt Đầu* | **9** |
| Định mức lặp vòng | **0** (quét 32 cạnh BOM) |

> 🔴 **Đọc kỹ chỗ này trước khi kết luận một thay đổi là vô nghĩa.** Trên dữ liệu hiện tại, **mọi
> bán thành phẩm đều bị ghim hết nên tồn khả dụng bằng 0**. Nghĩa là phép trừ bán thành phẩm thêm
> ngày 05/09 **không làm đổi một con số nào** trên màn hình thật. Chạy thử thấy y hệt **không**
> chứng minh được là nó không hoạt động — phải chạy `TC-VALID-02/03` với phần ghim rỗng mới thấy.

---

## TC-HAPPY — luồng đúng

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-HAPPY-01 | **Công thức kéo tồn qua kỳ đúng bằng ví dụ của chính khách** | `_tinh_mot_ma(tồn đầu 60, tối thiểu 50, nhu cầu [30,0,100,0], đơn mua về [0,50,0,0])` — đúng ảnh chat khách 13/08 | Tổng cần mua **70** | Pass — kỳ1 cần 30 → mua 20, tồn cuối 50 · kỳ2 về 50 → mua 0, tồn 100 · kỳ3 cần 100 → mua 50, tồn 50 · kỳ4 mua 0. **Tổng 70** | Pass |
| TC-HAPPY-02 | Con số trong ngoặc **"120 (70)"** | Chạy lại ca trên với `bo_qua_po=True` | **120** — phần phải mua nếu chưa đặt gì | Pass — ra đúng **120**. Màn hình hiện `120 (70)` đúng ảnh chat khách | Pass |
| TC-HAPPY-03 | Nổ định mức theo BOM xuống tận lá | `no_dinh_muc({"Thành phẩm 1": 2})` | Ra nguyên vật liệu lá, không ra bán thành phẩm | Pass — `{NVL 1: 2, NVL 2: 4, NVL 3: 6}` | Pass |
| TC-HAPPY-04 | Kiểu 2 chạy được **và nói thật khi thiếu dữ liệu** | `tinh_nhu_cau(kieu=2, 01/09→30/09, lùi 12 tháng)` | Không ra bảng rỗng im lặng | Pass — khoảng tham chiếu `2025-09-01 → 2025-09-30`, cảnh báo *"không có đơn bán nào — không tính được nhu cầu Kiểu 2"*. **Nói ra thay vì trả 0** | Pass |
| TC-HAPPY-05 | Kiểu 1 xếp đơn vào kỳ theo *Thời Gian Bắt Đầu* | `tinh_nhu_cau(kieu=1, 03/08, 3 kỳ tuần)` | Chỉ đơn có giờ nằm trong kỳ mới được tính | Pass — 7 đơn rơi vào kỳ, 3 dòng vật tư ra bảng | Pass |

---

## TC-VALID — số phải đúng, sai số là mua sai tiền thật

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-VALID-01 | **Tồn khả dụng không bao giờ âm vì ghim** | `_kha_dung` với (1,3) · (0,5) · (10,4) | Kẹp về 0, phần ghim thừa trả riêng | Pass — `(1,3)→(0, 1, 2)` · `(0,5)→(0, 0, 5)` · `(10,4)→(6, 4, 0)` | Pass |
| TC-VALID-01b | Tồn **âm thật** thì GIỮ nguyên số âm | `_kha_dung(-5, 3)` | `-5`, không kẹp về 0 — đó là kho lệch thật, phải mua bù | Pass — `(-5.0, 0.0, 3.0)` | Pass |
| TC-VALID-02 | **Một bán thành phẩm trong kho chỉ che MỘT kỳ, và là kỳ sớm nhất** | Gọi `no_dinh_muc` 3 lượt liên tiếp dùng chung `be`, mỗi lượt cần 2 `Thành phẩm 1`, kho 31, ghim rỗng | Bể tồn trừ dần, không hồi lại ở kỳ sau | Pass — bể **31 → 29 → 27 → 25**, `da_dung` cộng dồn **2 → 4 → 6**. Kỳ sớm được che trước | Pass |
| TC-VALID-03 | Bể tồn dùng **chung cho cả cây**, không trừ lại từ đầu ở mỗi nhánh | `no_dinh_muc({"Thành phẩm 1": 20})`, kho 31, ghim rỗng | Không phải mua gì; bể còn 11 | Pass — nổ ra `{}`, `da_dung = 20`, bể còn **11** | Pass |
| TC-VALID-04 | 🔴 **Phần tồn đã tiêu ở tầng giữa phải trừ khỏi tồn tầng lá** | Chạy cả engine, đọc `ton_kha_dung` của mã vừa là bán thành phẩm vừa mua ngoài | Không đếm tồn hai lần | Pass — chứng minh bằng bất biến: `be` khởi tạo bằng tồn khả dụng rồi **chỉ giảm**, nên `da_dung ≤ khả dụng`; phép kẹp ở bước 3 luôn rơi vào nhánh tuyến tính. **Không có ca nào mất phần** | Pass |
| TC-VALID-05 | Cảnh báo đơn trống *Thời Gian Bắt Đầu* **nêu đích danh số đơn** | Chạy Kiểu 1 | Liệt kê mã đơn, không nói chung chung | Pass — *"9 đơn bán đã duyệt bị bỏ qua vì trống Thời Gian Bắt Đầu — không xếp được vào kỳ nào: SAL-ORD-2026-00001, …"* | Pass |

---

## TC-EDGE — biên, và chỗ dễ tưởng là lỗi

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-EDGE-01 | 🔴 **Đơn mua QUÁ HẠN vẫn được tính, dồn vào kỳ đầu** | Kỳ từ **14-09**, đơn mua hẹn **07-09** (đã quá hạn) | Không được bỏ — hàng vẫn đang trên đường | Pass — `NVL 3 → [10, 0]`, cả 10 vào kỳ đầu | Pass |
| TC-EDGE-02 | Đơn mua về **sau kỳ cuối** thì bỏ | Kỳ 17-08 → 30-08, đơn mua hẹn 07-09 | Bỏ — không giúp gì cho khoảng đang tính | Pass — trả `{}` | Pass |
| TC-EDGE-03 | Đơn mua rơi **đúng kỳ của nó**, không dồn hết vào kỳ 1 | Kỳ 31-08→06-09 và 07-09→13-09 | Vào kỳ 2 | Pass — `NVL 3 → [0, 10]` | Pass |
| TC-EDGE-04 | 🔴 **Đổi số kỳ thì `tồn khả dụng` ĐỔI THEO — đúng thiết kế, không phải lỗi** | Cùng `NVL 3`: chạy 3 kỳ, rồi chạy 12 kỳ từ 03-08 | Kỳ rộng hơn ⟹ nhiều đơn nằm **trong** kỳ hơn ⟹ được miễn trừ ⟹ ghim còn lại ít ⟹ khả dụng cao hơn | Pass — 3 kỳ: ghim ngoài kỳ `{NVL 3: 7}` → khả dụng **0**. 12 kỳ: ghim ngoài kỳ `{}` → khả dụng **7**. ⚠ Người kiểm thử đo hai lần ra hai số **sẽ tưởng là lỗi** | Pass |
| TC-EDGE-05 | Ghim thật trên site ⟹ bán thành phẩm **không che được gì** | `no_dinh_muc({"Thành phẩm 1": 2})` với phần ghim thật | Nổ đủ xuống lá, `da_dung` rỗng | Pass — `{NVL 1: 2, NVL 2: 4, NVL 3: 6}`, `da_dung = {}`, bể cả 3 bán thành phẩm đều **0** | Pass |
| TC-EDGE-06 | Định mức **lặp vòng** → cảnh báo rồi dừng, không treo | Cần một BOM lặp vòng | Cảnh báo *"định mức lặp vòng, dừng nổ tại đây"* | **Chưa chạy** — quét 32 cạnh BOM, **0 mã lặp vòng**. Không dựng được mà không ghi dữ liệu thật | — |
| TC-EDGE-07 | 🔴 **Kỳ rỗng KHÔNG được nói "không thiếu gì"** | Chạy Kiểu 1 trên khoảng không có đơn nào (04-01-2027, 2 kỳ tuần) | Phải phân biệt *chưa tính được gì* với *đủ hàng* | Pass — engine trả `co_nhu_cau = False` và cảnh báo *"Không có nhu cầu nào trong khoảng đã chọn"*; màn hình hiện *"Kỳ đã chọn không có đơn hàng nào — chưa tính được gì"*. Trước 05/09 cả hai trạng thái đều hiện *"Không có vật tư nào thiếu"* — ở ca này là **nói sai**, người đọc hiểu thành tồn đủ. Cùng họ với `"chưa có đơn mua"` của Phần IV | Pass |
| TC-EDGE-08 | Có nhu cầu và đủ hàng thì nói đúng câu còn lại | Kiểu 1 trên khoảng có đơn | `co_nhu_cau = True` | Pass — 01-09, 3 kỳ: `co_nhu_cau = True`, 2 dòng ra bảng. Kiểu 2 không có dữ liệu tham chiếu cũng trả `False` đúng | Pass |

---

## TC-REGR — không làm hỏng cái đang chạy

| Mã | Mục tiêu | Bước thực hiện | Kết quả mong đợi | KQ thực tế | P/F |
|---|---|---|---|---|---|
| TC-REGR-01 | Đổi 05/09 **không đụng chỗ gọi khác** | `no_dinh_muc(nhu_cau)` **không truyền `kho`** | Giữ nguyên hành vi cũ: nổ thẳng xuống lá | Pass — `kho=None` ra `{NVL 1: 2, NVL 2: 4, NVL 3: 6}`, y hệt trước khi đổi | Pass |
| TC-REGR-02 | 🔴 **Engine CHỈ ĐỌC** | Đếm 8 bảng trước/sau hai lượt chạy đầy đủ (Kiểu 1 4 kỳ + Kiểu 2) | Không bảng nào đổi | Pass — `Stock Ledger Entry` 79→79 · `BOM` 10→10 · `Sales Order` 34→34 · `Material Request` 3→3 · `Purchase Order` 1→1 · `Bin` 20→20 · `Item` 62.055→62.055 · `Comment` 46.541→46.541. **0 bảng đổi** | Pass |
| TC-REGR-03 | Không tự tạo BOM lúc bấm Tính toán | `BOM` trước/sau | Không đổi | Pass — 10 → 10. Engine dùng `resolve_components` (chỉ đọc), **không** gọi `auto_create_bom` | Pass |

---

## Chưa chạy — ghi ra thay vì giấu sau con số tổng

| Mã | Vì sao chưa chạy |
|---|---|
| TC-EDGE-06 | Site **không có** định mức lặp vòng; dựng một cái là ghi dữ liệu thật |
| TC-PERM-01 | Chưa kiểm màn hình dưới vai trò hạn chế. Trang là Frappe Page — **cần xác định ai được mở** |
| TC-ISO-01 | Chưa kiểm trên site không cài app khách |
| TC-UI-01 | Tab **Lập kế hoạch** (bước 4) **chưa làm** — chưa có gì để test |

**Tổng: 22 ca · 21 Pass · 1 chưa chạy** (`TC-EDGE-06`).

⚠ **Đừng đếm bằng `grep "^| TC-"`.** File này có **24** dòng bắt đầu bằng `| TC-`, nhưng 4 trong
đó là **dòng nhắc** ở bảng *Chưa chạy* ngay trên, không phải ca test. Đếm máy móc ra 24 là **thừa
4**. Bộ test Phần IV đã vấp đúng bẫy này ngày 04/09 và phải đính chính công khai — tôi vấp lại
lúc viết file này, sửa trước khi đăng.

---

## ⚠ Hạn chế đã biết

| Việc | Ảnh hưởng |
|---|---|
| Nhánh **định mức lặp vòng** trừ tồn hai lần | Mã Sản xuất đã tiêu bể tồn rồi rơi vào nhánh lặp vòng sẽ vào tập lá, và bước 3 trừ `da_dung` lần nữa. **Hiện không tới được** (0 mã lặp vòng). Sai về phía **mua dư**, không phải thiếu hàng — hướng an toàn hơn. Ghi lại chứ không vá |
| `be[m]` gọi `_ton_thuc_te([m], kho)` **từng mã một** | Hôm nay 4 lần / 6 mã / 0,09s vì site ít bán thành phẩm, và nhớ theo mã nên không nhân theo số kỳ. Nhưng **nhân theo số bán thành phẩm phân biệt** — ở quy mô anh Thắng nêu (>2.000 đơn/năm) thành vài trăm truy vấn lẻ. Gom theo lô được, như `bom.py` đã làm (43,9s → 12,8s) |
| Bảng **chưa khai tồn tối thiểu** | Chỉ **6 / 62.055** dòng *Mặc định của mặt hàng* có giá trị. Phần V **phụ thuộc PM-FEAT-00037**; cột đó đổi thì mọi mức tối thiểu tụt về 0 **mà không báo gì** |
