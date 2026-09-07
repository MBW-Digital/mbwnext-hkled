# Ca test — Phòng Ban thực hiện sản xuất (PM-TASK-00143)

> **Tổng kết 07/09 chiều:** **11 ca · 11 Pass · 4 cần người test** (đợt 1).
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

## Cần người test — 4 ca, đều là thao tác thật trên giao diện

Máy không thay được, vì đây là phần nhìn thấy và bấm được.

| Mã | Tình huống | Cách thử | Vì sao máy không thay được |
|---|---|---|---|
| TC-UI-01 | Ô **Phòng Ban** hiện trong lưới *Assembly Items* | Mở một Kế hoạch sản xuất, xem cột Phòng Ban có trong lưới không | `in_list_view` chỉ có tác dụng khi lưới được vẽ |
| TC-UI-02 | Danh sách đội **bị lọc** theo phòng của lệnh | Mở Lệnh sản xuất, khai Phòng Ban, bấm ô Đội Sản Xuất | `set_query` chạy ở trình duyệt |
| TC-UI-03 | Đổi phòng ban thì **đội cũ bị bỏ chọn** kèm lời nhắc | Chọn đội, rồi đổi sang phòng khác | Cần thấy `show_alert` hiện ra |
| TC-UI-04 | Lệnh chưa khai phòng thì ô Đội **hiện hết** đội, không rỗng | Để trống Phòng Ban rồi bấm ô Đội | Kiểm điều kiện `return {}` — lọc theo ô trống sẽ ra danh sách rỗng khó hiểu |

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
