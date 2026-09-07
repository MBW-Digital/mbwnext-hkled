# Ca test — Phòng Ban thực hiện sản xuất (PM-TASK-00143)

> **Tổng kết 07/09 chiều:** **23 ca · 22 Pass · 1 chờ dữ liệu** (đợt 1 + 1b + bấm thật trên giao diện).
> Ba con số này **đếm bằng máy** từ chính các bảng dưới. Bản nháp đầu tôi gõ tay ra `22 ca · 21 Pass` — sai cả hai, đúng cái bẫy đếm ghi ngay dòng dưới.
> Con số đếm bằng máy từ chính bảng dưới, không gõ tay.
> Đếm bằng `grep '^| TC-'` sẽ **thừa 4** vì bảng *Cần người test* cũng có dòng `| TC-`.

Tính năng: ghi nhận **phòng ban nào sản xuất mặt hàng nào** ở Kế hoạch sản xuất; Lệnh sản xuất
thừa hưởng phòng ban đó; trưởng phòng phân đội ngay tại Lệnh sản xuất, và chỉ chọn được đội
thuộc phòng mình.

🔒 **Chốt của anh Thắng 07/09 10:27** (PM-TASK-00143):

> *"mình sẽ dùng luôn Phòng ban của ERPNext lõi. Khách chốt lại là ở phần kế hoạch sản xuất mình
> chỉ cần ghi nhận phòng ban nào thực hiện sản xuất mặt hàng nào thôi, không cần gán đội sản xuất
> nữa. Khi tạo lệnh sản xuất thì các trưởng phòng ban sẽ tự vào lệnh sản xuất để phân đội em nhé.
> đối với thành phẩm chính mình sẽ gán phòng ban ở bảng Assembly Items em nhé"*

Cộng ý anh thêm 03/09 14:57: *"cho Đội Sản Xuất gắn phòng ban để trưởng phòng chỉ chọn được đội
của phòng mình"*.

---

## 🔴 Trước khi đọc kết quả: tính năng này CHƯA DÙNG ĐƯỢC vì thiếu dữ liệu

Đo trên cổng 8012 lúc 07/09 11:0x:

| Thứ | Số đo | Nghĩa |
|---|---|---|
| `Department` | **14 bản ghi, toàn mặc định ERPNext** | Không có *Phòng kỹ thuật* / *Phòng KCS* — đúng hai phòng khách nêu |
| Cây phòng ban | **phẳng**, cả 14 đều `parent = All Departments` | Chưa có cấp cha–con nào |
| `Employee.department` | **0 / 4** | Chưa ai thuộc phòng nào |
| `Work Team.custom_department` | **0 / 2** | Hai đội chưa gắn phòng |
| Dòng kế hoạch có khai phòng | **0** | Chưa ai khai |

Cùng hình dạng với `Item Default` **6/62.055** của PM-FEAT-00037: code đúng, màn hình vẫn trống.
Đã hỏi anh Thắng ngày 07/09 (danh sách phòng thật + ai gán nhân sự vào phòng) **trước khi code**,
không phải sau.

⚠ Vì vậy **mọi ca dưới đây dựng dữ liệu tạm trong giao dịch rồi `rollback`** — chạy trên logic
thật, không để lại một bản ghi nào. Kiểm sau khi chạy: `0 dòng kế hoạch / 0 đội` có phòng ban,
đúng như trước khi chạy.

---

## TC-KE — thừa hưởng phòng ban từ Kế hoạch sản xuất

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-KE-01 | Lệnh sinh từ bảng **Assembly Items** (thành phẩm chính) | Lấy phòng của đúng dòng đó | `Production` | ✅ Pass |
| TC-KE-02 | Lệnh có **cả hai** dòng — Assembly và Sub Assembly khai hai phòng khác nhau | Bán thành phẩm thắng, cùng thứ tự với `_plan_row_for` đã có | `Quality Management` | ✅ Pass |
| TC-KE-03 | Người dùng **đã nhập tay** phòng ban trên lệnh | Giữ nguyên, không ghi đè | Giữ nguyên | ✅ Pass |
| TC-KE-04 | Lệnh **không gắn kế hoạch** nào (tạo tay / nội bộ) | Để trống, **không báo lỗi** — không được chặn sản xuất | `None`, không nổ | ✅ Pass |
| TC-KE-05 | Dòng kế hoạch **chưa khai** phòng ban | Để trống | `None` | ✅ Pass |
| TC-KE-06 | Hook nhận nhầm doctype khác (`Sales Order`) | Bỏ qua, không nổ | Không nổ | ✅ Pass |

## TC-CHAN — đội phải thuộc đúng phòng của lệnh

Chặn ở **server** (`validate`), không chỉ ở màn hình: API và nhập liệu hàng loạt đi vòng qua
được phần lọc của giao diện.

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-CHAN-01 | Lệnh phòng **A**, chọn đội thuộc phòng **B** | **Chặn**, câu báo nói rõ đội thuộc phòng nào | *"Đội **Đội 1** thuộc phòng **Production**, không thuộc phòng **Quality Management** của lệnh này"* | ✅ Pass |
| TC-CHAN-02 | Lệnh phòng A, chọn đội thuộc phòng A | Cho qua | Cho qua | ✅ Pass |
| TC-CHAN-03 | Đội **chưa gắn** phòng ban (dữ liệu cũ — cả 2 đội trên site) | Cho qua, **không chặn** | Cho qua | ✅ Pass |
| TC-CHAN-04 | Lệnh **chưa khai** phòng ban | Cho qua — không có gì để đối chiếu | Cho qua | ✅ Pass |
| TC-CHAN-05 | **Không chọn** đội | Cho qua — phân đội là việc làm sau | Cho qua | ✅ Pass |

> Ba ca cho qua (03·04·05) là **cố ý**, không phải lỗ hổng. Chặn ở đó thì với dữ liệu hiện tại
> (0 đội có phòng, 0 dòng kế hoạch khai phòng) sẽ **không tạo nổi một lệnh sản xuất nào** —
> đứng cả nhà máy để bảo vệ một ô chưa ai dùng.

---

## TC-UI — đã bấm thật trên giao diện `dev.mbwnext.com:8012` (07/09 11:0x)

Đăng nhập bằng `bench browse` (một lần, không gõ mật khẩu), thao tác trên **form Lệnh sản xuất
mới chưa lưu** nên không đụng bản ghi thật nào. Kiểm sau khi xong: `Work Order` **39 → 39**,
`Employee Allocation` **39 → 39**, không có lệnh nào được tạo trong 30 phút.

| Mã | Tình huống | KQ thực tế | Đạt |
|---|---|---|---|
| TC-UI-01 | Ô **Phòng Ban** hiện trong lưới *Assembly Items* | Cột *Phòng Ban* hiện đúng ở cuối lưới trên `KSX-26-00001` | ✅ Pass |
| TC-UI-02 | Khai Phòng Ban rồi bấm ô **Đội Sản Xuất** | Hiện `Đội 1`, `Đội 2` **kèm dòng** *"Filters applied for Phong Ban = Phòng kỹ thuật - HKL"* — bộ lọc có chạy, và không giấu mất đội nào | ✅ Pass |
| TC-UI-04 | **Chưa khai** Phòng Ban rồi bấm ô Đội | Hiện đủ `Đội 1`, `Đội 2`, không rỗng | ✅ Pass |
| TC-UI-05 | Ô Phòng Ban và Đội Sản Xuất hiện đúng nhãn + mô tả trên form | Đúng nhãn tiếng Việt, mô tả hiện dưới ô | ✅ Pass |
| TC-UI-03 | Đổi phòng ban thì **đội cũ bị bỏ chọn** kèm lời nhắc | ⏳ **Chưa chạy được** — cần ít nhất một đội đã khai phòng ban, mà `Work Team` hiện **0/2**. Nhánh này chỉ kích hoạt khi đội *có* phòng và phòng đó *khác* phòng của lệnh | — |

> Console lúc thao tác: **0 lỗi từ mã của tính năng này**. Bốn lỗi thấy được đều có sẵn từ trước
> và không liên quan (`chart.min.js` import, socket.io không kết nối được).

### 🔴 TC-UI-02 tìm ra một lỗi THẬT — và nó là cái bẫy `IN (NULL)` lần thứ ba trong ngày

Bản đầu của bộ lọc viết ở JS:

```js
filters: [["Work Team", "custom_department", "in", [doc.custom_department, ""]]]
```

Đo trên site trước khi sửa: `Đội 1` và `Đội 2` đều `custom_department` **IS NULL** — không phải
chuỗi rỗng. Mà trong SQL, **`NULL` không khớp `IN` bất kể danh sách có gì**, kể cả có `NULL` trong
đó. Kết quả:

| Cách viết | Số đội khớp |
|---|---|
| `custom_department IN ('Phòng kỹ thuật - HKL', '')` | **0 / 2** |
| `ifnull(custom_department,'') IN ('Phòng kỹ thuật - HKL', '')` | **2 / 2** |

Nghĩa là chỉ cần lệnh có Phòng Ban là ô Đội Sản Xuất **rỗng trắng** — đúng cái mà chú thích trong
chính file JS đó viết ra để tránh. Bộ ca phía server **không bắt được**, vì nó kiểm `validate`
chứ không kiểm truy vấn của ô Link.

Đã sửa: chuyển sang truy vấn riêng `doi_theo_phong_ban` có `ifnull` ở server, rồi bấm lại trên
giao diện (ảnh trong TC-UI-02).

⚠ **Cùng cái bẫy đã vấp 2 lần khác trong ngày 07/09:** đếm đơn trống *Thời Gian Bắt Đầu* bằng
`filters={"custom_start_time": ["in", [None, ""]]}` ra **0** trong khi thật ra là **9**. Luật:
**cột nào có thể `NULL` mà đem so bằng `in` thì phải `ifnull` trước** — và phép so đó im lặng,
không báo lỗi, chỉ trả ít kết quả hơn.

---

## Chỗ CỐ Ý chưa làm ở đợt 1

**1. Chọn đội ở lệnh chưa tự điền danh sách công nhân — và lý do vừa thay đổi trong ngày.**
Đường tự điền (`work_order.ensure_start_time` dòng 273–286) **đang lỗi `NameError: work_team`**:
biến được gán ở `inherit_from_production_plan:220` nhưng bị tiêu thụ trong một hàm khác, nên không
phải "hiếm khi chạy" mà là **nổ mỗi lần chạm tới**. Chạy thật 07/09 ra lỗi trên 2 ca; đặt sai hàm
từ commit đầu `8299675`; `Error Log` 0 bản ghi nên **chưa nổ lần nào trên thực tế**, vì hai cửa
thoát ở đầu hàm che gần hết đường.

🔄 **Cập nhật 07/09 chiều — đã vá, commit `fe2dd6f`** (cửa sổ giữ Phần II–III, Tuấn duyệt hướng):
khối đó chuyển về cuối `inherit_from_production_plan`, nơi `work_team` đang sống. Vá nằm ở
**commit riêng của họ**, không thuộc đợt này.

Từ `fe2dd6f`, WO tạo từ Kế hoạch **bắt đầu tự điền công nhân** — kéo theo `Employee Allocation` và
**đổi số Bảng 3** của PM-FEAT-00008 đã nghiệm thu. ⚠ **Chỉ Lệnh sản xuất tạo MỚI; số cũ không bị
tính lại** — hook chạy ở `before_insert` nên không có gì hồi tố. Đã kiểm bằng `hooks.py:274`.

Hai bên **đã chạy chung**: họ tạo Lệnh sản xuất thật qua trọn chuỗi 5 hook `before_insert` (gồm cả
`inherit_department` của đợt này) rồi `rollback` — WO tạo được, `custom_department = None` (đúng,
chưa ai khai), bảng nhân sự vẫn đủ 3 dòng có `employee_level` và `performance_factor_`. Hai phần
độc lập thật, không phải chỉ trên lý thuyết. `Employee Allocation` 39 → 39 sau khi xoá WO,
`TC-HAPPY-13` vẫn 202,5.

⚠ **Chỉnh lại một câu quá mạnh ở bản trước của tài liệu này:** tôi từng viết tính năng *"chưa từng
hoạt động ngày nào"*. **Không chứng minh được.** Bằng chứng chỉ đủ nói: hỏng **từ `8299675`
(08/08) tới 07/09**. Trước đó không kiểm được — xem mục *Pass cũ* ở cuối.

**2. Ô Đội Sản Xuất cũ ở Kế hoạch vẫn còn.** Anh Thắng nói *"không cần gán đội sản xuất nữa"*,
nhưng gỡ ô là phải mổ vào chính hàm đang lỗi ở trên. Đã báo anh Thắng 07/09 và xin để đợt sau.
Hiện `Production Plan Sales Order` 1/11 dòng và `Production Plan Sub Assembly Item` 1/4 dòng có
khai đội — gỡ cũng gần như không mất dữ liệu, nhưng rủi ro không cân xứng.

**3. Cây phòng ban cha–con** (khách nêu *Phòng kỹ thuật > Đội 1, Đội 2*). `Department` của ERPNext
vốn đã là cây `nested set` sẵn, không phải viết gì thêm — nhưng chưa khai được vì chưa có danh
sách phòng thật. Chờ anh Thắng.

---

## Ghi chú kỹ thuật cho người đọc sau

- **"Bảng Assembly Items" = `po_items` / `Production Plan Item`**, không phải `sub_assembly_items`.
  Đã kiểm bằng meta: nhãn màn hình của `po_items` đúng là *Assembly Items* và nó đang chứa
  `Thành phẩm 1`; bảng bán thành phẩm nằm dưới mục *Sub Assembly Items* và không có nhãn riêng.
  Anh Thắng gọi đúng tên trên màn hình — đừng "sửa hộ" thành `sub_assembly_items`.
- `Work Order.production_plan_item` và `.production_plan_sub_assembly_item` là **Data chứa TÊN
  dòng**, không phải Link. Phải `db.get_value` theo tên. Cùng cái bẫy đã ghi ở PM-TASK-00046.
- Mã đặt ở **file riêng** `python_hook/work_order_phong_ban.py` + `js/work_order_phong_ban.js`,
  không viết chen vào `work_order.py` / `work_order.js` của cửa sổ kia. `doctype_js` nhận danh
  sách nên hai file JS cùng chạy. Gỡ tính năng = bỏ 2 dòng trong `hooks.py`.
- Hook `inherit_department` khai **trước** `ensure_start_time` có chủ đích: hàm kia đang lỗi ở
  nhánh cuối, chạy trước thì phần phòng ban không phụ thuộc số phận của nó.


---

## TC-NS — Phòng Ban của nhân sự bám theo Đội Sản Xuất (đợt 1b)

🔒 **Anh Thắng 07/09 10:55:** *"khi chọn đội cho nhân sự thì phòng ban của đội đó được gán vào
nhân sự đó luôn có được không, vì dễ có trường hợp nhân sự thuộc đội 1, đội 1 thuộc phòng kĩ
thuật nhưng ở nhân sự mình lại gán nhầm sang phòng kcs"*

Đây là **một sự thật khai hai nơi** — kiểu dữ liệu bao giờ cũng lệch. Chữa bằng cách chọn một nơi
làm gốc rồi suy ra nơi kia. Anh Thắng chọn **Đội là gốc**.

⚠ Hook này **cố ý GHI ĐÈ**, khác mọi hook thừa hưởng khác của app (vốn chỉ điền chỗ trống). Nếu
chỉ điền chỗ trống thì **đúng cái sai anh Thắng mô tả sẽ không bao giờ được sửa** — người đã bị
gán nhầm sang Phòng KCS sẽ ở lại đó vĩnh viễn vì ô không trống.

| Mã | Tình huống | KQ mong đợi | KQ thực tế | Đạt |
|---|---|---|---|---|
| TC-NS-01 | Người gán nhầm **KCS**, đội thuộc **Kỹ thuật** | Kéo về đúng phòng của đội — chính ca anh Thắng nêu | `Phòng kỹ thuật - HKL` | ✅ Pass |
| TC-NS-02 | Đang đúng sẵn | Giữ nguyên, không báo gì | Giữ nguyên | ✅ Pass |
| TC-NS-03 | Người **chưa có** phòng ban | Điền theo đội | `Phòng kỹ thuật - HKL` | ✅ Pass |
| TC-NS-04 | **Đội chưa khai** phòng ban | **Không** xoá phòng của người — trống là tệ hơn hiện trạng | Giữ `Phòng KCS - HKL` | ✅ Pass |
| TC-NS-05 | Người **không thuộc đội nào** | Giữ nguyên phòng nhập tay | Giữ `Phòng KCS - HKL` | ✅ Pass |
| TC-NS-06 | Hook nhận nhầm doctype khác | Bỏ qua, không nổ | Không nổ | ✅ Pass |
| TC-NS-07 | **Đội đổi phòng** | Người của đội đổi theo | `Phòng KCS - HKL` | ✅ Pass |

> Khi có thứ bị đổi thì hook **nói ra** bằng `msgprint`, kèm phòng cũ → phòng mới và lý do.
> Đổi âm thầm ô phòng ban của một người đúng là loại *"số đổi mà không ai đụng gì"* mà cả dự án
> này đang đi săn — người bấm Lưu phải thấy mình vừa gây ra gì.

**Vì sao không dùng `fetch_from`:** nó chỉ điền khi ô đích còn trống (không sửa được bản ghi đã
gán nhầm) và chỉ chạy phía client (lọt đường script/API). Hai chỗ đã bẫy app này rồi — xem C1 ở
`python_hook/employee.py` và `set_sales_info` ở `work_order.py`.

### 🔴 Chưa có hiệu lực cho tới khi khai Đội → Phòng Ban

Đo 07/09 11:0x, **sau khi** anh Thắng nạp dữ liệu:

| Thứ | Số đo | |
|---|---|---|
| `Department` | **16** — có `Phòng kỹ thuật - HKL` và `Phòng KCS - HKL` (tạo 10:50) | ✅ xong |
| `Employee.department` | **4/4** đã gán | ✅ xong |
| `Work Team.custom_department` | **0/2** — `Đội 1` và `Đội 2` đều trống | ❌ **còn thiếu** |

Nên hôm nay hook chưa đổi một ai. Đã báo anh Thắng: cần khai ô *Phòng Ban* trên **hai bản ghi Đội
Sản Xuất**, đó là ô cuối cùng còn thiếu.

---

## ⚠ Ô Pass cũ không bảo chứng cho mã hiện tại

Ghi lại vì nó suýt làm cả hai cửa sổ kết luận sai, và nó làm hỏng đúng thứ ta dùng để tự trấn an.

`TC-HAPPY-05` trong `docs/testcases/bac-tho-lich-san-xuat.md` ghi **Pass ngày 03/08** cho đúng
hành vi *"WO thừa hưởng thời gian + nhân sự đội"* — thứ mà hôm nay đo ra là **NameError**. Commit
làm hỏng là `8299675` ngày **08/08**, tức **5 ngày SAU** lượt test đó.

Ở dự án này **cây làm việc chính là bản đang chạy trên 8012**, nên một lượt test hoàn toàn có thể
chạy trên mã **chưa commit**, rồi mã được commit sau đó lại là một bản khác. Ô Pass ấy **đúng lúc
chạy** và **sai lúc đọc lại**, mà không có gì trên bảng báo điều đó.

**Luật rút ra:** ghi ngày chạy vào từng ô là **chưa đủ**. Ô nào đo một hành vi mà mã của hành vi đó
đã đổi sau ngày chạy thì **phải chạy lại**, không được đọc ô Pass cũ như bằng chứng cho hôm nay.
