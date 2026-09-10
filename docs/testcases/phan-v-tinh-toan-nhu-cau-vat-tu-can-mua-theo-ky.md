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
| TC-PERM-01 | Đã đo vai trò nào mở được (xem `TC-QUYEN`), nhưng **ai NÊN được mở** thì đang chờ anh Thắng |
| TC-ISO-01 | Chưa kiểm trên site không cài app khách |

**Tổng: 113 ca · 112 Pass · 1 chưa chạy** (`TC-EDGE-06`).

> Đếm bằng `grep -c '^| TC-.*| Pass |'`. Hai cách đếm SAI đã thử: `grep -c '| Pass |'` đếm cả dòng
> ghi chú này (dòng dặn cách đếm lại chứa chính chuỗi bị đếm), và `grep -c '^| TC-'` đếm cả bảng
> *lý do chưa chạy* bên dưới — bảng đó cũng mở đầu bằng mã ca.

> Cập nhật 08/09: thêm nhóm `TC-YCM` (9 ca) sau chốt (B) của anh Thắng — xem cuối file.
> Đếm bằng `grep -c '^| TC-.*| Pass |'` — **phải neo `^| TC-`**. Hai cách sai đã thử:
> `grep '^| TC-'` thừa 4 vì bảng *Chưa chạy* cũng có dòng `| TC-`; còn `grep '| Pass |'`
> thừa 1 vì **chính dòng ghi chú này** chứa chuỗi đó. Tài liệu tự làm hỏng phép đếm của
> chính nó — đúng loại bẫy cả bộ này đang đi săn.

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

---

## TC-YCM — nói ra phần Yêu Cầu Mặt Hàng đang chờ (08/09)

🔒 **Anh Thắng chốt 08/09 09:12 — phương án (B):** *"Giữ nguyên em nhé"*. Tức Phần V **KHÔNG trừ**
phiếu Yêu Cầu Mặt Hàng đang chờ khỏi số cần mua, nhưng **phải nói ra**.

Vì sao chỗ này đáng có bộ ca riêng: anh Thắng chấp nhận (B) dựa trên một lý do — *"số lượng mua kỳ
này nó cũng đã được tự trừ đi số lượng trên đơn hàng mua kia rồi nên không sợ bị trùng"* — mà lý do
đó **chỉ đúng khi phiếu đã thành Đơn Mua Hàng**. `_po_chua_ve` đọc Đơn Mua; **không** đọc Yêu Cầu
Mặt Hàng. Quãng giữa hai thứ đó là quãng màn hình mù, và nút *Tạo Yêu Cầu Mặt Hàng* của Phần IV đẻ
ra đúng loại phiếu nằm trong quãng ấy.

Đo 08/09 trên site: **NVL 3 99 · NVL 2 70 · NVL 1 20** đang chờ — **cả ba đều lớn hơn số hệ thống
bảo mua** (72 · 58 · 15). Không nói ra thì mỗi lần bấm là mua trùng bằng tiền thật.

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-YCM-01 | Đọc phần **đã duyệt, chưa thành đơn mua** | Đúng ba mã, đúng số | `{NVL 3: 99, NVL 2: 70, NVL 1: 20}` | Pass |
| TC-YCM-02 | Mã không có phiếu nào | Không sinh khoá rỗng | không có khoá | Pass |
| TC-YCM-03 | Danh sách rỗng | `{}`, không truy vấn | `{}` | Pass |
| TC-YCM-04 | Truyền `None` | `{}`, không nổ | `{}` | Pass |
| TC-YCM-05 | Phiếu còn **nháp** không được cộng vào | Bỏ qua | site có 15 NVL 3 đang nháp; kết quả vẫn 99, không gồm | Pass |
| TC-YCM-06 | Phần **đã thành đơn mua** không đếm lại | Trừ `ordered_qty` | có 30 đã đặt, không cộng lần hai | Pass |
| TC-YCM-07 | Mọi dòng kết quả mang trường `ycm_dang_cho` | Có | có | Pass |
| TC-YCM-08 | Đúng **một** câu cảnh báo, không lặp | 1 câu | 1 câu | Pass |
| TC-YCM-09 | 🔒 **Số cần mua KHÔNG bị trừ** — đúng chốt (B) | Giữ nguyên 72 | 72, không thành −27 | Pass |

> Chạy bằng cách gọi thẳng hàm, **không lưu tài liệu nào**. Kiểm sau: `Material Request` **10 → 10**.

⚠ `TC-YCM-09` là ca dễ bị "sửa hộ" nhất. Người sau đọc code thấy đo được phần đang chờ mà không
trừ sẽ tưởng quên, rồi trừ vào cho "đúng". **Đó là đảo chốt của khách.** Muốn đổi thì phải hỏi anh
Thắng lại, không tự sửa.

### Câu ở màn hình trống — hệ quả của chốt "tính vào kỳ khởi công"

Anh Thắng chốt 08/09: đơn tính vào **kỳ nó khởi công**. Hệ quả: đơn khởi công **trước** khoảng đang
xem thì không hiện, dù vẫn thiếu hàng thật — và vì mọi đơn đã duyệt trên site đều khởi công trước
hôm nay, **khoảng mặc định ra màn hình trống**. Đây là trạng thái *thường gặp*, không phải ngoại lệ.

Nên câu ở màn hình trống nay nói thêm **cách gỡ** thay vì chỉ báo trống: giải thích đơn xếp theo
*Thời Gian Bắt Đầu*, và gợi ý **kéo ngày bắt đầu về trước**. Cần người test xem câu đó có đọc hiểu
được không — máy không thay được phần này.

---

## Bước 4 — tab Lập kế hoạch và lập đơn mua (08/09)

Đây là **chỗ duy nhất của cả Phần V ghi dữ liệu**. Mọi ca dưới đây chạy trên site thật, hoặc trong
giao dịch rồi `rollback`, hoặc tạo thật rồi **xoá và đếm lại**. `Purchase Order` **3 → 3** sau khi
chạy xong toàn bộ.

### TC-LKH — gộp kỳ và ngày cần hàng

| Mã | Ca | Mong đợi | Thực tế | KQ |
|---|---|---|---|---|
| TC-LKH-01 | Thiếu ở kỳ 2 | Ngày đầu **kỳ 2** | `2026-09-15` | Pass |
| TC-LKH-02 | Thiếu ngay kỳ 1 | Ngày đầu kỳ 1 | `2026-09-08` | Pass |
| TC-LKH-03 | Không kỳ nào thiếu | Đầu khoảng, không vỡ | `2026-09-08` | Pass |
| TC-LKH-04 | Không có kỳ nào | `None`, không `IndexError` | `None` | Pass |
| TC-LKH-05 | Cần mua là số lẻ (0,5) | Vẫn tính là thiếu | đúng kỳ 2 | Pass |
| TC-LKH-06 | Gộp không mất dòng | Bằng số dòng bảng chính | 3 = 3 | Pass |
| TC-LKH-07 | Mọi dòng có ngày cần hàng | Có | 3/3 | Pass |
| TC-LKH-08 | Số lượng đặt mặc định = thiếu hụt | Bằng nhau | bằng | Pass |
| TC-LKH-09 | Ngày cần hàng luôn là ngày **đầu một kỳ** | Thuộc tập ngày đầu kỳ | đúng | Pass |
| TC-LKH-10 | Kết quả rỗng | Lưới rỗng, không lỗi | `[]` | Pass |
| TC-LKH-11 | Kết quả lỗi | Lưới rỗng, không lỗi | `[]` | Pass |

⚠ `_gop_dong` phải gọi ở **cả hai** đường — gọi thẳng và chạy nền. Bản đầu chỉ gộp ở
`gop_lap_ke_hoach`, mà màn hình đi đường chạy nền, nên lưới sẽ **trống** — trông y hệt "không phải
mua gì".

### TC-NCC — gợi ý nhà cung cấp

| Mã | Ca | Mong đợi | Thực tế | KQ |
|---|---|---|---|---|
| TC-NCC-01 | Luôn đủ 3 tiêu chí | 3 dòng | 3 | Pass |
| TC-NCC-02 | Tiêu chí nào cũng có **căn cứ**, kể cả khi trống | Có | có | Pass |
| TC-NCC-03 | Chưa đủ dữ liệu thì **không đoán tên** | `None` | `None` | Pass |
| TC-NCC-04 | Rổ rỗng | Không gợi ý | `[]` | Pass |
| TC-NCC-05 | Nhận chuỗi JSON (đường HTTP) | Như nhận mảng | giống hệt | Pass |
| TC-NCC-06 | Mã chưa từng mua | Cả 3 đều "chưa đủ dữ liệu" | đúng | Pass |

Đo 08/09 trên cổng 8012: **Giá tốt nhất** = NCC A (rẻ nhất ở 2/3 mã, so giữa **1** nhà cung cấp);
**Giao nhanh nhất** = chưa đủ dữ liệu (không phiếu nhập nào trỏ về đơn mua); **Chất lượng** = NCC A
100%, đo trên **1** dòng.

⚠ Câu *căn cứ* bắt buộc nêu **mẫu số**. "Rẻ nhất" khi trong sổ chỉ có một nhà cung cấp thì đúng về
chữ mà rỗng về nghĩa — người mua đọc thành "đã so giá rồi" và thôi hỏi thêm. Bản đầu thiếu chỗ này.

### TC-PO — lập đơn mua

| Mã | Ca | Mong đợi | Thực tế | KQ |
|---|---|---|---|---|
| TC-PO-01 | Thiếu nhà cung cấp | Chặn | chặn | Pass |
| TC-PO-02 | Nhà cung cấp không có thật | Chặn | chặn | Pass |
| TC-PO-03 | Rổ rỗng | Chặn | chặn | Pass |
| TC-PO-04 | Số lượng 0 | Chặn | chặn | Pass |
| TC-PO-05 | Số lượng âm | Chặn | chặn | Pass |
| TC-PO-06 | Mã không có thật | Chặn | chặn | Pass |
| TC-PO-07 | Mã rỗng | Chặn | chặn | Pass |
| TC-PO-08 | Hai dòng sai | Báo **cả hai** một lần | cả hai | Pass |
| TC-PO-09 | 7 ca chặn ở trên không tạo gì | Số đơn không đổi | 3 → 3 | Pass |
| TC-PO-10 | Đơn tạo ra ở trạng thái **nháp** | `docstatus = 0` | 0 | Pass |
| TC-PO-11 | 2 dòng chọn → **một** đơn 2 dòng | 1 đơn | 1 đơn | Pass |
| TC-PO-12 | Đúng nhà cung cấp đã chọn | NCC A | NCC A | Pass |
| TC-PO-13 | Dùng **số người dùng chốt**, không tính lại | 62 / 50 | 62 / 50 | Pass |
| TC-PO-14 | Mỗi dòng giữ **ngày riêng** | 15/09 và 22/09 | đúng | Pass |
| TC-PO-15 | Ngày của đơn = ngày sớm nhất trong rổ | 15/09 | 15/09 | Pass |
| TC-PO-16 | Luôn nói ra đơn còn nháp | Có câu | có | Pass |
| TC-PO-17 | Đơn nháp **được đếm** vào cảnh báo mua trùng | 62 / 50 | đúng | Pass |
| TC-PO-18 | Mã không có trong đơn nháp | Không bịa số | không có khoá | Pass |
| TC-PO-19 | Rollback sạch | 3 → 3 | 3 → 3 | Pass |
| TC-PO-20 | Đơn thử biến mất | Không tồn tại | không | Pass |
| TC-PO-21 | 🔴 **Ngày cần hàng ở quá khứ** | Vẫn tạo được | tạo được | Pass |
| TC-PO-22 | Ngày quá khứ kẹp về hôm nay | `08-09-2026` | đúng | Pass |
| TC-PO-23 | Và **nói ra** rằng phần này đã trễ | Có câu | có | Pass |
| TC-PO-24 | Nêu đích danh dòng nào, ngày gốc bao nhiêu | Có | `NVL 2 (01-08-2026)` | Pass |
| TC-PO-25 | Trộn quá khứ + tương lai — dòng quá khứ | Về hôm nay | đúng | Pass |
| TC-PO-26 | Trộn — dòng tương lai | **Giữ nguyên** | giữ nguyên | Pass |
| TC-PO-27 | Chỉ kể tên dòng **thật sự** trễ | Không vơ cả rổ | đúng | Pass |
| TC-PO-28 | Ngày đơn = sớm nhất **sau khi kẹp** | Hôm nay | đúng | Pass |
| TC-PO-29 | Dòng không có ngày cần hàng | Hôm nay, không vỡ | đúng | Pass |
| TC-PO-30 | Rollback sạch lần hai | 3 → 3 | 3 → 3 | Pass |

### TC-UI — bấm thật trên cổng 8012

| Mã | Ca | Mong đợi | Thực tế | KQ |
|---|---|---|---|---|
| TC-UI-01 | Bấm tab **Lập kế hoạch** khi chưa tính | Chặn, nhắc bấm Tính toán | chặn, có nhắc | Pass |
| TC-UI-02 | Sau khi tính, lưới hiện đủ dòng | 3 dòng | 3 | Pass |
| TC-UI-03 | Dòng nhắc YCM nằm **ngay dưới** dòng hàng | Đúng vị trí | đúng | Pass |
| TC-UI-04 | Sửa số lượng đặt | Đếm lại tổng | 150+122 = 272 | Pass |
| TC-UI-05 | Chưa tích thì nút **Lập đơn hàng** khoá | Khoá | khoá | Pass |
| TC-UI-06 | Hộp thoại hiện gợi ý, cảnh báo, bảng dòng | Đủ ba khối | đủ | Pass |
| TC-UI-07 | Bấm tên nhà cung cấp trong gợi ý | Điền vào ô | điền được | Pass |
| TC-UI-08 | Nhãn **đã trễ** hiện ở lưới và hộp thoại | Cả hai chỗ | cả hai | Pass |
| TC-UI-09 | Tạo đơn thật | Ra `PO-26-00007`, có link | ra, có link | Pass |
| TC-UI-10 | Dòng đã lập đơn bị **khoá và đánh dấu** | Mờ đi, ghi "đã vào PO-…" | đúng | Pass |
| TC-UI-11 | Lần tính sau **nói ra** đơn nháp đó | Có câu, đúng số | `NVL 2 (146), NVL 3 (122)` | Pass |
| TC-UI-12 | Dọn sạch sau khi thử | 4 → 3 | 4 → 3 | Pass |

> Đơn thử `PO-26-00007` đã **xoá**; ba đơn còn lại (`PO-26-00004/5/6`) là của Administrator, không
> đụng tới.

### 🔴 Ca mà 20/20 test server không bắt được

`TC-PO-21` sinh ra từ một lỗi **thật, chỉ hiện khi bấm nút**. ERPNext chặn `schedule_date` sớm hơn
`transaction_date`. Mà *Ngày cần hàng* là ngày đầu của **kỳ bị thiếu**, và kỳ bị thiếu thường đã
**trôi qua** — đo 08/09, kỳ mặc định bắt đầu 01/08 nên **mọi dòng thật đều bị chặn**.

Bản đầu qua sạch **20/20** ca test chỉ vì mọi ngày trong test đều ở tương lai. Đây đúng là lý do
anh Tuấn dặn *"test trên giao diện đi đã rồi mới comment"* — lần thứ hai trong hai ngày.

Cách sửa: kẹp về hôm nay **và nói ra**. Ngày cần hàng nằm ở quá khứ không phải lỗi dữ liệu — nó có
nghĩa là phần hàng đó **đã trễ**. Kẹp lặng lẽ là bôi mất đúng cái tin người mua cần biết.

### ⚠ Chỗ hở còn lại — đơn nháp không được trừ

Nút này cố ý tạo đơn ở trạng thái **nháp**: duyệt là cam kết tiền thật, mà đơn giá do ERPNext điền
từ bảng giá, mã chưa có giá thì ra 0. Máy không được chốt con số đó thay người mua.

Nhưng `_po_chua_ve` lọc `docstatus = 1`, tức **không thấy đơn nháp**. Nên lập đơn xong, bấm Tính
toán lại thì số thiếu **y nguyên** — mockup C2 lại hứa *"đơn mua vừa tạo sẽ được lần chạy sau trừ
đi"*. **Lời hứa đó chỉ đúng sau khi đơn được duyệt.**

Ba lớp che, không lớp nào thay được việc hỏi anh Thắng:

1. `_po_nhap_cho_duyet` đo và **cảnh báo** phần đang nằm trong đơn nháp (`TC-PO-17`, `TC-UI-11`);
2. dòng đã lập đơn bị **khoá ngay trên lưới**, ghi rõ đã vào đơn nào (`TC-UI-10`);
3. hộp thoại thành công **nói thẳng** đơn còn nháp nên số chưa giảm (`TC-PO-16`).

➜ **Cần hỏi anh Thắng:** đơn mua do máy lập nên để **nháp** (an toàn, số chưa trừ) hay **tự duyệt**
(số trừ ngay, nhưng chốt giá thay người mua)? Đừng tự đổi.

### TC-QUYEN — ai lập được đơn mua từ màn hình này (08/09)

Màn hình vốn **chỉ đọc**, nên ai mở được cũng vô hại. Từ bước 4 nó **tạo Đơn Mua Hàng**, mà hai
danh sách vai trò lệch nhau:

| Vai trò | Mở được màn hình | Tạo được đơn mua |
|---|---|---|
| System Manager · Purchase Manager · Purchase User | ✅ | ✅ |
| **Manufacturing Manager** | ✅ | **❌** |

| Mã | Ca | Mong đợi | Thực tế | KQ |
|---|---|---|---|---|
| TC-QUYEN-01 | Quản lý sản xuất không tạo được đơn mua | `has_permission` = False | False | Pass |
| TC-QUYEN-02 | Màn hình nhận cờ `duoc_lap_don` | `False` | `False` | Pass |
| TC-QUYEN-03 | Người có quyền thì cờ bật | `True` | `True` | Pass |
| TC-QUYEN-04 | Kết quả lỗi vẫn trả cờ, không vỡ | Có cờ, lưới rỗng | đúng | Pass |
| TC-QUYEN-05 | Server chặn bằng **câu của mình**, không phải câu lõi | Nêu rõ cần quyền mua hàng | đúng | Pass |
| TC-QUYEN-06 | Ca bị chặn không tạo đơn nào | 3 → 3 | 3 → 3 | Pass |
| TC-QUYEN-07 | Rollback sạch | 3 | 3 | Pass |
| TC-QUYEN-08 | Tài khoản thử biến mất | Không tồn tại | không | Pass |

⚠ **Đo 08/09 trên cổng 8012: 0 tài khoản dính** — cả ba tài khoản mở được màn hình đều có quyền
mua. Đây là lỗ hổng **tiềm ẩn**, không phải lỗi đang xảy ra. Nhưng *"quản lý sản xuất lập kế hoạch,
không đi mua"* là cách phân vai rất thường gặp, nên nó sẽ xảy ra.

⚠ `_gop_dong` phải nhận `nguoi_dung` ở đường chạy nền: job chạy trong worker nên
`frappe.session.user` ở đó **không phải người bấm nút**. Hỏi quyền nhầm người thì hoặc khoá nút của
người có quyền, hoặc — tệ hơn — mở nút cho người không có.

➜ **Đã hỏi anh Thắng:** quản lý sản xuất có được lập đơn mua từ màn hình này không? Nếu **có** thì
việc cần làm là cấp quyền `Purchase Order` cho vai trò đó, **không phải** gỡ chốt chặn này.

---

## TC-UI2 — bấm lại toàn bộ giao diện trên dữ liệu của ngày 09/09

Chạy trên cổng 8012, kỳ **mặc định** (bắt đầu hôm nay) — tức đúng thứ người dùng thấy khi mở màn
hình lần đầu, không phải một khoảng ngày chọn riêng cho vừa ca test.

Nền lúc đo **09/09 ~09:0x**: `Purchase Order` 3 · `Material Request` 10 · `Sales Order` 40 ·
`Work Order` 44 · `Production Plan` 15.

| Mã | Ca | Mong đợi | Thực tế | KQ |
|---|---|---|---|---|
| TC-UI2-01 | Kỳ mặc định có dữ liệu | Bảng có dòng | 3 vật tư · tổng 62 · 2 cảnh báo | Pass |
| TC-UI2-02 | Ngày cần hàng là **hôm nay** → **không** nhãn *đã trễ* | Không nhãn | không | Pass |
| TC-UI2-03 | Tích ô đầu bảng | Chọn hết | 3/3 · tổng **62** = khớp thẻ *Tổng còn phải mua* | Pass |
| TC-UI2-04 | Sửa một dòng về **0** | Tự bỏ tích dòng đó | còn 2/3 · tổng 56 | Pass |
| TC-UI2-05 | Sửa số lượng đặt 44 → **50** | Đếm lại theo số mới | tổng 62 | Pass |
| TC-UI2-06 | Bấm *Tạo đơn mua* khi **chưa chọn** nhà cung cấp | Chặn | *"Giá trị khuyết bắt buộc: Nhà cung cấp"* | Pass |
| TC-UI2-07 | Bấm tên trong bảng gợi ý | Điền vào ô nhà cung cấp | điền `NCC A` | Pass |
| TC-UI2-08 | Tạo đơn thật | 1 đơn **nháp**, 2 dòng | `PO-26-00007`, `docstatus = 0` | Pass |
| TC-UI2-09 | Đơn dùng **số người dùng chốt** | 50 và 12 | 50 và 12 | Pass |
| TC-UI2-10 | Dòng cho về 0 **không** vào đơn | Vắng mặt | không có `NVL 3` | Pass |
| TC-UI2-11 | 🆕 Mã **chưa khai giá mua** | Nói ra, không im | *"1 dòng chưa có đơn giá…: NVL 1. Điền giá trước khi duyệt."* · `rate = 0` | Pass |
| TC-UI2-12 | Dòng đã lập đơn bị khoá + đánh dấu | Mờ, ghi số đơn | *"đã vào PO-26-00007"* | Pass |
| TC-UI2-13 | Tính lại: cảnh báo đơn nháp xuất hiện | 2 → 3 cảnh báo | *"…CÒN NHÁP chứa: NVL 1 (12), NVL 2 (50)"* | Pass |
| TC-UI2-14 | Tính lại: số thiếu **KHÔNG** giảm | Giữ nguyên | 44 · 12 · 6 y nguyên | Pass |
| TC-UI2-15 | Dọn sạch sau test | 5 bảng về đúng số cũ | 3·10·40·44·15, không lệch bảng nào | Pass |

### 🆕 `TC-UI2-11` — nhánh chờ từ hôm qua, nay chạy thật

Ca *"mã chưa khai giá mua"* hôm 08/09 **không chạm tới được**: rổ hàng hôm đó mã nào cũng có lịch
sử mua nên `rate` luôn > 0, và nhánh cảnh báo nằm im. Hôm nay `NVL 1` lọt vào rổ và nó nổ đúng.

🔴 **Đây là bằng chứng thật cho câu đang hỏi anh Thắng** (đơn mua để **nháp** hay **tự duyệt**):
đơn tạo ra có một dòng **giá 0 đồng**. Nếu chọn *tự duyệt* thì hệ thống sẽ **tự duyệt một đơn mua
0 đồng** với nhà cung cấp. Trước hôm nay chỗ này mới chỉ là suy luận từ mã nguồn; giờ có `rate = 0`
thật kèm câu cảnh báo thật.

⚠ Vì sao đáng ghi thành ca riêng thay vì gộp: nó nhắc rằng **rổ hàng của lần test quyết định nhánh
nào được chạy**. Hai lượt bấm giống hệt nhau về thao tác, khác nhau về dữ liệu, và chỉ một lượt
chạm tới nhánh này.

### ⚠ Số nền đổi từng ngày — so sánh phải kèm giờ đo

`Work Order` trên 8012: **42 → 43 → 44** trong hai ngày. `Purchase Order` cũng đổi khi có ai lập
đơn. Nên mọi câu *"trước/sau không lệch"* chỉ có nghĩa khi hai lần đếm **cùng một buổi** — đừng lấy
số nền của hôm qua làm chuẩn cho hôm nay.
## 🔒 Anh Thắng chốt ba câu — 09/09/2026 09:20

Nguyên văn (`69lk5kd75e` trên PM-FEAT-00030):

> *1. đơn tạo ra ở dạng nháp em nhé, **vì sau này họ cài luồng duyệt trên đơn nữa***
> *2. người mua hàng được lập em nhé, vì chức năng này phục vụ cho phòng mua hàng*
> *3. hạn là 11/09 em nhé*

**Không phải sửa dòng code nào — hành vi đang chạy đã khớp cả ba.** Đo lại sau khi có chốt:

| Chốt | Code hiện tại | Khớp |
|---|---|---|
| Đơn ra dạng **nháp** | `tao_don_mua` chỉ `insert()`, **không** `submit()` | ✅ |
| Chỉ **người mua hàng** được lập | chặn bằng `has_permission("Purchase Order", "create")`; vai trò tạo được đơn = `Purchase Manager` · `Purchase User` | ✅ |
| Hạn 11/09 | — | ✅ đã cập nhật trên PM |

### 🔑 Lý do của anh Thắng MẠNH HƠN lý do của em — ghi lại kẻo người sau đảo ngược

Em lập luận giữ nháp vì **đơn giá ra 0 đồng** khi mã chưa khai giá (xem `TC-UI2-11`, có ca thật).
Anh Thắng cho một lý do khác và bền hơn: ***"vì sau này họ cài luồng duyệt trên đơn nữa"***.

Khác biệt quan trọng ở chỗ **lý do của em sẽ hết hạn, lý do của anh ấy thì không**. Ngày nào khách
khai đủ giá cho mọi mặt hàng, người đọc code sẽ nghĩ *"hết đơn 0 đồng rồi, cho tự duyệt cho nhanh"*
— và vẫn **sai**, vì tự duyệt sẽ nhảy qua luồng duyệt mà khách sắp dựng.

➜ **Đừng đổi `tao_don_mua` thành tự duyệt, kể cả khi mọi mặt hàng đã có giá.** Muốn đổi thì phải
hỏi lại anh Thắng, vì lý do thật nằm ở luồng duyệt chứ không ở giá.

### ⚠ Một chỗ anh Thắng KHÔNG nói tới — cố ý để nguyên

Anh ấy nói *"người mua hàng **được lập**"*, không nói ai **được mở** màn hình. Hiện *Quản lý sản
xuất* vẫn **xem được** bảng nhưng **không lập được đơn** (có câu giải thích ngay khi vẽ lưới, xem
nhóm `TC-QUYEN`). Hành vi này khớp đúng lời anh ấy, nên **giữ nguyên**, không tự thắt thêm.

Nếu sau này khách muốn giấu hẳn màn hình khỏi *Quản lý sản xuất* thì đó là một chốt mới, sửa ở
`page/tinh_nhu_cau_vat_tu.json`.

### Còn lại đúng một việc để đóng `testcase_passed`

**Người bên khách bấm thử.** Bộ test hiện **113 ca · 112 Pass**, nhưng toàn bộ do bên làm tự chạy.
`testcase_passed` là cổng của **người test**, không phải của tác giả — đã nêu rõ với anh Thắng
trong `r9ehtjv95m`, anh ấy chưa trả lời phần này.
