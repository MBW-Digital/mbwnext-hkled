# Mockup — Dialog "Tạo Rule — Chọn NVL theo Nguồn" (BOM Template, app `mbwnext_hkled`)

- Tính năng: `apps/mbwnext_hkled/docs/features/bom-template-theo-bien-the.md`
- Trạng thái: **ĐÃ DUYỆT 2026-07-31** (quandm@mbw.vn) — giữ nguyên như bản dựng, không sửa gì.
  3 câu hỏi mục 5: giữ danh sách phẳng, không thêm nút xoá dòng, giữ nhãn "Giá Trị Điều Kiện (Nguồn)".
- Xem thật: `http://localhost:8047/app/bom-template/new` → Mặt Hàng Cha = `DD11S200`
  → dòng 1: Thành Phần BOM = `Nguồn`, Kiểu Thành Phần = `Theo Rule` → mở dòng → nút **Tạo Rule**

---

## 1. Vì sao đổi giao diện cũ

Popup cũ 2 bước (**Chọn Điều Kiện** → **Chọn Nguyên Vật Liệu**) cho người dùng tick tổ hợp đặc tính,
rồi sinh **1 dòng BOM Rule cho mỗi biến thể khớp**. Với dữ liệu thật, nhóm `P01_P03` có **17.184 biến thể**
— cách này sinh ra hàng nghìn dòng cho một template.

Tài liệu thiết kế mục 2.4 chốt lại: việc chọn NVL cho "Nguồn" **chỉ phụ thuộc giá trị đặc tính `Nguồn`**,
nên chỉ cần **1 dòng / 1 giá trị `Nguồn`** (~9 dòng). Số lượng không hỏi ở đây nữa vì đã có công thức tính.

## 2. Bố cục dialog

```
┌────────────────────────────────────────────────────────────────┐
│  Tạo Rule — Chọn NVL theo Nguồn                            [×] │
├────────────────────────────────────────────────────────────────┤
│  Thành Phần BOM: **Nguồn** · Mặt Hàng Cha: **DD11S200**        │
│  Chọn Nguyên Vật Liệu cho từng giá trị **Nguồn**.              │
│  Bỏ trống = không tạo dòng.                                    │
│  Số lượng do công thức tự tính khi Tạo BOM, không nhập ở đây.  │
│                                                                │
│  Done Dim 1 Cấp            [ Link → Item              🔍 ]     │
│  Done Nhỏ                  [ Link → Item              🔍 ]     │
│  HKLED Dim 1 Cấp           [ Link → Item              🔍 ]     │
│  HKLED Dim 5 Cấp           [ Link → Item              🔍 ]     │
│  HKLED Nhỏ                 [ Link → Item              🔍 ]     │
│  Inventronics Dim 5 Cấp    [ Link → Item              🔍 ]     │
│  Meanwell Dim 1 Cấp        [ Link → Item              🔍 ]     │
│  Philips Dim 1 Cấp         [ Link → Item              🔍 ]     │
│  Philips Dim 10 Cấp        [ Link → Item              🔍 ]     │
│                                                                │
│                                            [  Xác Nhận  ]      │
└────────────────────────────────────────────────────────────────┘
```

## 3. Quy tắc hành vi

| Điểm | Quy tắc |
|---|---|
| Danh sách giá trị | Lấy **distinct `Nguồn` của các biến thể thật** thuộc item cha (DD11S200 → đúng 9 giá trị). Item cha chưa có biến thể thì lấy toàn bộ giá trị khai trong Item Attribute `Nguồn` (12 giá trị) |
| Sắp xếp | Theo alphabet, để vị trí dòng không nhảy giữa các lần mở |
| Điền sẵn | Nếu `(Thành Phần BOM, giá trị Nguồn)` đã có dòng BOM Rule → điền sẵn NVL cũ ⇒ **dùng lại dialog để SỬA**, không chỉ để tạo |
| Bỏ trống | Không tạo/không xoá dòng nào cho giá trị đó |
| Filter NVL | Chỉ Item `has_variants = 0` |
| Không nhập Số Lượng | Cố ý — số lượng do Server Script `hkled_resolve_bom_qty` tính lúc Tạo BOM |
| Xác nhận | Thêm dòng mới / cập nhật dòng cũ tại chỗ (không nhân bản), rồi hiện alert `Đã thêm {n} dòng, cập nhật {m} dòng` |
| Chưa chọn gì | Báo "Chưa chọn Nguyên Vật Liệu nào", **không** đóng dialog |
| Chặn trước khi mở | Chưa chọn Mặt Hàng Cha → "Vui lòng chọn Mặt Hàng Cha trước". Chưa chọn Thành Phần BOM → "Vui lòng chọn Thành Phần BOM trước" |

## 4. Thay đổi giao diện kèm theo trên form BOM Template

1. **Field mới "Nhóm Công Thức"** (bắt buộc) ở cột phải, ngay dưới "Mặt Hàng Cha".
2. **Tự điền Nhóm Công Thức** theo prefix mã khi chọn Mặt Hàng Cha — chỉ điền khi đang trống,
   người dùng sửa lại được. VD `DD11S200` → `D11_D15`, `DP01...` → `P01_P03`.
3. **Bảng Thành Phần BOM** có thêm lựa chọn `Số Lượng Theo Công Thức` ở cột "Kiểu Thành Phần";
   với lựa chọn này thì **hiện** cột "Mặt Hàng" (bắt buộc) và **ẩn** cột "Số Lượng".
4. Tab **Công Thức Thành Phần**: bảng BOM Rule giờ 3 cột — Thành Phần BOM · Giá Trị Điều Kiện (Nguồn) ·
   Nguyên Vật Liệu (đã bỏ cột "Mặt Hàng Sản Xuất" và "Số Lượng").

## 5. Điểm cần người duyệt cho ý kiến

1. Dialog dạng **danh sách phẳng 9 dòng Link** — có cần thêm ô tìm kiếm/nhóm lại khi số giá trị `Nguồn`
   tăng lên không? (hiện tối đa 12 giá trị nên chưa cần)
2. Có muốn thêm nút **"Xoá dòng của thành phần này"** trong dialog không? Hiện muốn xoá phải vào
   tab Công Thức Thành Phần xoá tay.
3. Nhãn "Giá Trị Điều Kiện (Nguồn)" — giữ hay đổi thẳng thành "Nguồn"?
