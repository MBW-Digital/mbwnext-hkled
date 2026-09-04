# Test case — Phần IV.2 · Sổ cam kết ghim vật tư (PM-FEAT-00036, đợt 1)

**App:** `mbwnext_hkled` · **Site thử:** `hkled.com` trên bench `cozy_dev`, mở bằng
`http://dev.mbwnext.com:8012`
**Ngày chạy vòng tự kiểm:** 04/09/2026 tối · **Người chạy:** Claude (Trợ lý HKLed 2)

Đầu bài: `docs/features/phan-bo-hang-vao-phan-ghim-cua-sales-order-khi-hang-mua-a-ve.md` **mục 8**
Bất biến phải giữ: `docs/features/kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md` **mục 12e**
Code: `api/ghim_vat_tu.py` · DocType con `HKLed Pinned Material` ·
`patches/them_bang_ghim_vat_tu.py` · hook trong `controllers/python_hook/sales_order.py`

> ### ⚠ Đây là ĐỢT 1 — nút *Phân Bổ* CHƯA CÓ
>
> Đợt này dựng **chỗ chứa · luật cấp phát · việc nhả vật tư khi sản xuất xong**. Còn thiếu đúng
> một thứ: **nút *Phân bổ hàng về***. Xem mục 8.9 của đầu bài. Đừng đọc bảng dưới như đã nghiệm
> thu cả tính năng.
>
> ### ⚠ Cách chạy vòng một — đọc trước khi tin cột KQ thực tế
>
> Mọi kịch bản đổi dữ liệu đều chạy **trong một giao dịch rồi `frappe.db.rollback()`** — tạo đơn,
> huỷ đơn, hạ tồn kho, sửa định mức đều không để lại vết. **Ngoại lệ duy nhất:** lần đồng bộ đầu
> tiên cho `SO-26-00026` đã **ghi thật** (`TC-HAPPY-01`), vì đó chính là hành vi tính năng phải
> có kể từ khi bật.
>
> **✅ Bổ sung 04/09 tối — vòng hai đã chạy THẬT trên giao diện cổng 8012.** Bốn ca dưới đây
> (`TC-HAPPY-07`, `TC-EDGE-12`, `TC-VALID-04`, `TC-REGR-06`) được bấm trên màn hình thật, không
> qua console. Đã dọn: `SO-26-00026` trả về đúng ghim 31, Phiếu xuất kho thử nghiệm đã **xoá bản
> nháp**, tồn `NVL 3` vẫn 7 — **0 bút toán kho**.
>
> Sau **mỗi** kịch bản đều chạy `kiem_bat_bien()` — phép quét toàn bảng mà mục 12e đòi hỏi. Cột
> KQ thực tế ghi cả kết quả phép quét đó, không chỉ kết quả của thao tác.

---

## Điều kiện chuẩn bị

| Cần gì | Giá trị |
|---|---|
| **Địa chỉ site** | `http://dev.mbwnext.com:8012` |
| **Tài khoản** | tài khoản của anh Thắng trên cổng 8012; ca phân quyền dùng `test.gioihan.sales@hkled.test` (bị giới hạn `Customer = a`) |
| **Cách vào tính năng** | Mở một **Đơn Bán đã duyệt** → tích **Ghim Tồn Khả Dụng** → bảng **Ghim Vật Tư** hiện ngay dưới lưới hàng hoá. Bảng chỉ đọc, máy tự điền |
| **Đơn dùng chạy** | `SO-26-00026` — 40 `Thành phẩm 1`, đã ghim 31, giao 17/09 |

**Dữ liệu nền đo lúc 04/09 20:0x** (đổi thì kết quả đổi theo, đo lại trước khi kết luận Fail):

| Mã | Tồn | Ghi chú |
|---|---|---|
| `Thành phẩm 1` | 31 | 24 ở Kho thành phẩm + 7 ở Kho bán thành phẩm |
| `Bán thành phẩm 1` | 1 | có định mức: 1 `NVL 1` + 2 `NVL 2` |
| `Bán thành phẩm 2` | 1 | có định mức: 3 `NVL 3` |
| `NVL 1` · `NVL 2` · `NVL 3` | 68 · 32 · 7 | hàng mua ngoài, là lá của cây định mức |

Định mức `Thành phẩm 1` = 1 `Bán thành phẩm 1` + 1 `Bán thành phẩm 2`.

---

## TC-HAPPY — luồng đúng

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-HAPPY-01 | Đơn đã duyệt, cần 40, ghim 31 ➜ còn 9 phải sản xuất | Sổ sinh dòng vật tư theo định mức của 9 chiếc | 5 dòng: `BTP1 1/9`, `BTP2 1/9`, `NVL1 8/8`, `NVL2 16/16`, `NVL3 7/24` | ✅ Pass |
| TC-HAPPY-02 | Kẹp ở tồn tự do | Không dòng nào ghim quá phần chưa ai giữ | `NVL 3` cần 24, kho có 7 ➜ ghim đúng **7**; `BTP1` cần 9, kho có 1 ➜ ghim **1** | ✅ Pass |
| TC-HAPPY-03 | Định mức nhiều cấp | Cấp dưới chỉ bóc cho phần **chưa cấp phát được** ở cấp trên | `BTP1` thiếu 8 ➜ bóc ra `NVL1 8` + `NVL2 16`; `BTP2` thiếu 8 ➜ `NVL3 24`. Không bóc cho 1 chiếc đã có sẵn | ✅ Pass |
| TC-HAPPY-04 | Dừng ở hàng *Mua hàng* | `NVL 1/2/3` là lá, không bóc tiếp | Đúng — 5 dòng, không có cấp thứ tư | ✅ Pass |
| TC-HAPPY-05 | Bảng 1b/2b (`ghim_chi_tiet`) đọc từ sổ | Tổng chi tiết khớp `ghim_boi_don_khac` | 6 mã, tổng khớp, `kiem_bat_bien()` **sạch** | ✅ Pass |
| TC-HAPPY-06 | Cột *định mức hiệu dụng* trên Bảng 2b | Là định mức thật, không phải phần được cấp | `BTP1`: 9/9 = **1**, không phải 1/9 = 0,111 (đã sửa trong lúc chạy — xem ghi chú dưới) | ✅ Pass |
| TC-HAPPY-07 | **Trên giao diện thật:** mở `SO-26-00026`, bảng *Ghim Vật Tư* hiện ngay dưới lưới hàng hoá | Đủ 5 dòng, cột Việt hoá, không sửa tay được | Đủ 5 dòng · mọi ô `read_only` · không có nút *Thêm dòng* ở lưới. Bảng 2b của đơn khác hiện *"7 đang ghim"* với định mức **3,00** | ✅ Pass |
| TC-HAPPY-08 | **Sản xuất xong 5 chiếc** cho đơn đang ghim | Ghim thành phẩm tăng, vật tư nhả theo | Ghim 31 → **36** · phải làm 9 → **4** · `NVL 1` 8 → 3 · `NVL 2` 16 → 6 · nhu cầu `NVL 3` 24 → 9. Quét bất biến sạch | ✅ Pass |

> **Ghi chú TC-HAPPY-06 — lỗi bắt được trong chính vòng chạy này.** Bản đầu chia
> `đã ghim / phải làm`, nên `Bán thành phẩm 1` hiện định mức **0,111** thay vì **1**. Con số đó
> không sai kiểu, không nổ lỗi, và **tụt xuống mỗi khi kho hết hàng** — đúng loại sai âm thầm mà
> Phần IV sinh ra để chặn. Đã đổi sang chia `nhu cầu / phải làm`.

## TC-VALID — kiểm tra dữ liệu

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-VALID-01 | Sửa *Số Lượng Giữ Chỗ* lên 40 (tồn 31) trên đơn **ĐÃ DUYỆT** | Bị chặn, câu lỗi nêu đúng mức tối đa | *"Dòng 1 — Thành phẩm 1: chỉ giữ chỗ được tối đa **31**, không được 40"* | ✅ Pass |
| TC-VALID-02 | Bảng ghim vật tư có sửa tay được không | Không — máy ghi, người chỉ đọc | `read_only = 1` ở cả trường bảng lẫn mọi cột con | ✅ Pass |
| TC-VALID-03 | Mã *Sản xuất* chưa có định mức | Phải nói ra, không im lặng bỏ qua | `C28DX03S100-328-40C-280LED: chưa có định mức, phần còn phải sản xuất (40) không ghim được vật tư` — hiện dạng toast màu cam | ✅ Pass |
| TC-VALID-04 | **Trên giao diện thật:** gõ 40 vào *Số Lượng Giữ Chỗ* (tồn 31) rồi lưu | Không lọt | Lớp giao diện **kẹp trước**: *"Thành phẩm 1: chỉ giữ chỗ được 31 — đã sửa lại giúp anh/chị"*, giá trị về 31 rồi mới lưu. Lớp server (TC-VALID-01) là lưới thứ hai cho đường API | ✅ Pass |

> 🔴 **TC-VALID-01 là ca quan trọng nhất của đợt này.** Anh Thắng chốt mở khoá ô ghim trên đơn đã
> duyệt. Frappe **không chạy `validate`** trên đường update-after-submit, nên nếu chỉ bật cờ
> `allow_on_submit` mà không treo lại `chan_giu_cho_vuot_ton` vào `before_update_after_submit`
> thì lớp chặn thủng **đúng ngay lúc vừa mở khoá** — và thủng im lặng, vì thao tác vẫn lưu thành
> công. Ca này chứng minh đã treo đúng.

## TC-EDGE — biên, lặp, và 8 bất biến của mục 12e

| Mã | Bất biến | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|---|
| TC-EDGE-01 | #4 | Bỏ tích *Ghim Tồn Khả Dụng* | Nhả sạch, nhưng **không xoá** số đã lưu | 5 dòng còn nằm lại; `ghim_vat_tu()` trả `{}` — hết hiệu lực. Quét sạch | ✅ Pass |
| TC-EDGE-02 | #8 | Tích lại | Cam kết cũ quay lại, kẹp theo tồn hiện tại | Đủ 5 dòng, số y như trước. Quét sạch | ✅ Pass |
| TC-EDGE-03 | #5 | Giảm ghim thành phẩm 31 → 20 | Phần phải sản xuất tăng ➜ nhu cầu vật tư tăng theo | `NVL1 19/19`, `NVL2 32/38` (kẹp đúng ở tồn 32), `NVL3 7/57`. Quét sạch | ✅ Pass |
| TC-EDGE-04 | #3 | Đơn chuyển **Closed** | Phần ghim biến khỏi mọi phép cộng | Dòng còn trong database nhưng `ghim_vat_tu()` trả `{}`. Quét sạch | ✅ Pass |
| TC-EDGE-05 | #8 | Đơn thứ hai **giao sớm hơn** được duyệt | Chỉ lấy phần **tự do**; cam kết đơn cũ không tụt | Đơn mới lấy `NVL1 5`, `NVL2 10`, `NVL3 **0**` (7 đã có chủ). Đồng bộ lại đơn cũ: y nguyên. Quét sạch | ✅ Pass |
| TC-EDGE-06 | #7 | Sao chép / amend đơn | Bản mới **không kế thừa** cam kết, phải giành lại | Bản sao ra số của riêng nó (`NVL1 5`, không phải 8 của bản gốc) | ✅ Pass |
| TC-EDGE-07 | #1 | **Tồn tụt sau khi đã ghim** (bẫy 2 mục 5: huỷ phiếu nhập) | Phép quét phải bắt được, đồng bộ lại phải cắt xuống | Quét báo `[#1] NVL 3: tổng ghim 7 > tồn thực tế 6`; đồng bộ lại ➜ cắt còn 6; quét lại sạch | ✅ Pass |
| TC-EDGE-08 | #6 | Định mức bị sửa **sau** khi ghim | Phải báo, không âm thầm dùng số cũ | `[#5] SO-26-00026 · NVL 3: định mức BOM-Bán thành phẩm 2-001 đã sửa lúc 2026-12-31, phần ghim tính theo bản 2026-07-29` | ✅ Pass |
| TC-EDGE-09 | #7 | Đơn còn **nháp** | Bảng phải rỗng — chưa duyệt thì chưa giữ chỗ của ai | 0 dòng | ✅ Pass |
| TC-EDGE-10 | — | Đơn đã duyệt nhưng **chưa từng** ghim vật tư | Không sinh dòng rác | 0 dòng, không cảnh báo | ✅ Pass |
| TC-EDGE-11 | #2 | Đơn **Huỷ** rồi amend, cả hai bản cùng tồn tại | Chỉ bản còn sống được tính | Chưa chạy — `SO-26-00026` đang gắn Kế hoạch sản xuất `KSX-26-00001` nên **không huỷ được**. Cần một đơn không có ràng buộc | ⏳ Chưa chạy |
| TC-EDGE-12 | #5 | **Trên giao diện thật:** giảm ghim 31 → 20 rồi lưu | Bảng chạy lại ngay trên màn hình | `Phải Làm` 9 → **20**, `NVL 2` thành **32/38** (kẹp đúng ở tồn 32), `NVL 3` thành **7/57**. Trả về 31 thì bảng về đúng số cũ | ✅ Pass |
| TC-EDGE-13 | #1 | **Huỷ** chứng từ sản xuất vừa duyệt | Kéo ngược phần ghim xuống, hàng đã bay khỏi kho | Ghim 36 → **31**, cả 5 dòng vật tư về đúng số cũ. Quét sạch | ✅ Pass |
| TC-EDGE-14 | — | Sản xuất **nhiều hơn** phần đơn còn thiếu (20 trên 9) | Kẹp ở số lượng trên dòng, phần dư để tự do | Ghim → **40** (đúng trần), sổ vật tư còn **0 dòng** — hết phải sản xuất thì không giữ vật tư nào. Quét sạch | ✅ Pass |
| TC-EDGE-15 | — | Lệnh sản xuất **không nối được về Đơn Bán** (làm để tồn kho) | Không chuyển gì | Ghim giữ nguyên 31. Đúng thiết kế — 17/33 lệnh trên site thuộc loại này | ✅ Pass |
| TC-EDGE-16 | — | Chứng từ **Chuyển vật tư đi sản xuất** (chưa phải Manufacture) | Không chuyển gì — hàng chưa làm xong | Ghim giữ nguyên 31 | ✅ Pass |

## TC-PERM — phân quyền

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-PERM-01 | `Guest` đọc bảng ghim vật tư | Bị chặn | `PermissionError` ở cả `client.get_list` lẫn `Sales Order` | ✅ Pass |
| TC-PERM-02 | User bị giới hạn `Customer = a` đọc bảng con của đơn **không thuộc phạm vi** | Không được thấy | ❌ **THẤY ĐỦ 5 DÒNG** của `SO-26-00026` — đơn mà chính user đó `get_doc` ra `PermissionError` | ❌ Fail — xem ô dưới |
| TC-PERM-03 | So sánh với bảng con của **lõi** | Để biết đây là lỗi mới hay hiện trạng | `Sales Order Item` của lõi **rò y hệt** trên cùng đơn đó | ✅ Pass (đo được) |

> 🔴 **TC-PERM-02 Fail — nhưng KHÔNG phải do tính năng này.**
>
> Truy vấn bảng con trong Frappe chỉ kiểm quyền **ở cấp DocType cha**, không đi qua User
> Permission từng bản ghi. `Sales Order Item` của app lõi rò đúng như vậy trên cùng một đơn, nên
> mọi bảng con của Đơn Bán trên site này đều đang hở như nhau, từ trước khi có bảng ghim.
>
> Ghi Fail chứ không ghi *"không áp dụng"*: người đọc file này cần biết dữ liệu ghim **đọc ra
> được** bằng API, kể cả bởi người không mở được đơn. Nó chỉ không phải hạng mục đóng được trong
> phạm vi PM-FEAT-00036. Cùng họ với ca rò rỉ đã báo ở Phần IV.

## TC-REGR — regression

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-REGR-01 | Lớp chặn xuất kho (PM-FEAT-00034) với mã **nay bị ghim vật tư** | Chặn, câu lỗi nêu đúng số | Xuất 5 `NVL 3` không gắn đơn ➜ *"NVL 3: xuất 5, tồn khả dụng còn 0"* | ✅ Pass |
| TC-REGR-02 | Miễn trừ qua Lệnh sản xuất của chính đơn đang ghim | Cho qua — đơn không tự chặn hàng của mình | `_don_duoc_mien` ra `{SO-26-00026}`, chứng từ **cho qua** | ✅ Pass |
| TC-REGR-03 | Màn hình *Kiểm Tra Tồn Kho* (Bảng 1·2·3) | Vẫn chạy, không cảnh báo lệch | 3 bảng ra đủ, `canh_bao = []` | ✅ Pass |
| TC-REGR-04 | Engine Phần V (`nhu_cau_vat_tu.tinh_nhu_cau`) | Vẫn chạy | 3 dòng vật tư, cảnh báo duy nhất là ca *thiếu Thời Gian Bắt Đầu* đã có từ trước | ✅ Pass |
| TC-REGR-05 | `ghim_boi_don_khac` sau khi đổi nguồn | Trả cả thành phẩm lẫn vật tư, khớp sổ | `{Thành phẩm 1: 31, NVL1: 8, NVL2: 16, NVL3: 7, BTP1: 1, BTP2: 1}` — khớp | ✅ Pass |
| TC-REGR-06 | **Trên giao diện thật:** lập Phiếu xuất kho 5 `NVL 3` rồi bấm **Gửi** | Bị chặn, hộp thoại đỏ nêu đúng số | *"Xuất quá tồn khả dụng — NVL 3: xuất 5, tồn khả dụng còn 0. Phần chênh đang được các Đơn Bán khác giữ chỗ."* Đã xoá bản nháp `KNB-26-00005`, tồn vẫn 7 | ✅ Pass |
| TC-REGR-07 | `_don_duoc_mien` của PM-FEAT-00034 sau khi dùng chung hàm nối Lệnh sản xuất → Đơn Bán | Miễn trừ không đổi | `MFG-WO-2026-00005` (chỉ có Kế hoạch sản xuất) vẫn ra `{SO-26-00026}`, chứng từ vẫn cho qua | ✅ Pass |

> ⚠ **Đổi hành vi có thật, phải nói với anh Thắng trước khi bật cho khách:** trước đợt này, phần
> vật tư mà `ghim_boi_don_khac` trả về **luôn rỗng** (`_con_phai_lam` tính `ghim − tồn`, mà lớp
> chặn không cho ghim vượt tồn — hai luật triệt tiêu nhau). Từ nay vật tư **bị ghim thật**, nên
> lớp chặn xuất kho bắt đầu chặn những chứng từ trước đây đi lọt. `TC-REGR-01` là bằng chứng.

## TC-ISO — cách ly app khách

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-ISO-01 | DocType mới có đúng `module` | `MBWNext HKLed` | `istable = 1`, `module = MBWNext HKLed` | ✅ Pass |
| TC-ISO-02 | Custom Field mới có đúng `module` | Đi theo app | `Sales Order-custom_ghim_vat_tu`, `module = MBWNext HKLed`, đã vào `fixtures/custom_field.json` | ✅ Pass |
| TC-ISO-03 | Site **không cài** app (`mbw.com` trên cùng bench) chạy `migrate` | Không lỗi | ⏳ Chưa chạy — `migrate` là việc độc quyền toàn máy, phải hẹn giờ | ⏳ Chưa chạy |
| TC-ISO-04 | App lõi có bị bẩn không | `git status` các app lõi sạch | ⏳ Chưa chạy | ⏳ Chưa chạy |

## TC-PWA

Không áp dụng — tính năng không có màn hình mobile.

---

## Tổng kết vòng một

**42 ca · 38 Pass · 1 Fail (ngoài phạm vi, xem TC-PERM-02) · 3 chưa chạy.** Trong đó **4 ca chạy trên giao diện thật**.

> Con số trên **đếm bằng máy** từ chính bảng, không gõ tay — đã đếm nhầm ba lần ở các bộ trước.

Chưa chạy: `TC-EDGE-11` (cần đơn không vướng Kế hoạch sản xuất), `TC-ISO-03`, `TC-ISO-04`.

**Chưa có test cho phần chưa code:** còn đúng **nút *Phân Bổ***.

Việc *nhả vật tư khi sản xuất xong* đã làm và đã test (`TC-HAPPY-08`, `TC-EDGE-13` → `TC-EDGE-16`),
nên lo ngại "giam hàng" tôi nêu với anh Thắng buổi tối đã được gỡ ở đường sản xuất. Đường còn lại
là hàng **mua** về — chính là việc của nút Phân Bổ.
