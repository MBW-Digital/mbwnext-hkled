# Ghim tồn khả dụng — toàn cảnh hai tính năng

> **Toàn cảnh mảng ghim — PM-FEAT-00023 · 00034 · 00036 · 00037 (Phần IV, IV.1, IV.2)**
> Tên trên PM khác tên file này — nối hai bên bằng MÃ, không bằng tên. Xem `CLAUDE.md`.

**Khách hàng:** HKLED · **Cập nhật:** 25/08/2026
**Phạm vi:** `PM-FEAT-00023` (Phần IV) và `PM-FEAT-00034`

> **File này KHÔNG thêm nội dung mới.** Nó chỉ vẽ lại quan hệ giữa hai tính năng, thứ tự làm,
> và những gì đang chặn. Đặc tả thật vẫn nằm ở hai file kia — sửa nội dung thì sửa ở đó, đừng
> sửa ở đây.
>
> Lý do có file này: phạm vi đã đổi **ba lần trong 36 giờ** (xem mục 4), lần nào cũng được cập
> nhật tại chỗ vào từng file, nên không ai còn cầm được bức tranh tổng. Đọc hai file spec cộng
> mười mấy bình luận PM mới ghép ra được — quá đắt cho một câu hỏi đơn giản là "đang vướng gì".

---

## 1. Hai tính năng thực chất là một

`PM-FEAT-00034` tách ra từ **mục 7.3 của chính Phần IV** ngày 24/08.

| | Tính năng | Việc |
|---|---|---|
| `PM-FEAT-00023` | Kiểm tra tồn kho và nguồn lực trên Đơn Bán | **hiển thị** con số |
| `PM-FEAT-00034` | Chặn xuất kho quá tồn khả dụng | **thi hành** con số đó |

Dùng chung bốn thứ, và đây là lý do không được viết hai lần:

1. Công thức **tồn khả dụng**
2. **Tập kho** hợp lệ — loại `Nhóm kho lỗi` và `Nhóm kho trung chuyển`, cả hai chiều
3. Ô tích **Ghim tồn khả dụng** (`custom_ghim_ton_kha_dung`)
4. Phép **bóc BOM** cho mặt hàng khai *Sản xuất* / *Gia công*

---

## 2. Cái tách ra lại chứa nền móng của cái gốc

Đây là nguồn rối chính, và nó không lộ ra lúc tách.

Lúc tách, `00034` tưởng là mẩu nhỏ — "chỉ chặn xuất kho". Nhưng bản phân tích của Thắng
(`PhanTich_TonKhaDung_va_CoCheGhim_v2`) cộng đáp của khách ngày 25/08 biến nó thành **cả engine**:
bảng phân bổ, netting BOM nhiều cấp, hàng đợi ưu tiên theo thời điểm ghim, cơ chế top-up khi hàng về.

Mà đó đúng là thứ **Bảng 1 của Phần IV cần để hiện được số**.

```
              ENGINE  —  thuộc PM-FEAT-00034
     tính pool nhiều kho · ghim · netting BOM theo cấp
                        │
        ┌───────────────┴───────────────┐
        ↓                               ↓
   PM-FEAT-00023                  PM-FEAT-00034
   HIỂN THỊ                       CHẶN XUẤT
   Bảng 1 · 1b · 2                hàm kiểm dùng chung
   ngày giao gợi ý                gọi từ 8 chứng từ
```

**Một lõi, hai chỗ dùng — không phải hai tính năng song song.**

➜ Hệ quả: **không code `00023` trước được**, nó không có gì để hiển thị.
➜ Hàm tính tồn khả dụng viết **một lần**, đặt ở chỗ engine, `00023` gọi lại. Không viết công
thức thứ hai — hai chỗ lệch nhau một điều kiện là ra hai con số mà nhìn mắt không thấy sai.

---

## 3. Chữ "Ghim" mang hai nghĩa ở hai tài liệu

Chỗ dễ nhầm nhất khi đọc chéo hai file:

| Ở | "Ghim" nghĩa là |
|---|---|
| `00023` §2 | ô tích quyết định đơn nào hiện ở **Bảng 1b** — chuyện hiển thị |
| `00034` | sinh bản ghi phân bổ, xếp **hàng đợi ưu tiên**, và **chặn** xuất kho |

Cùng một ô tích, hai tầm vóc. Khi code, nghĩa của `00034` là nghĩa đúng; `00023` chỉ đọc kết quả.

---

## 4. Phạm vi đã đổi ba lần — mốc để đọc lại bình luận cũ

Bình luận PM trước mốc gần nhất có thể đang nói về phương án đã bị bỏ. Bảng này để đối chiếu.

| Khi | Đổi thành | Còn hiệu lực? |
|---|---|---|
| 24/08 sáng | tách mục 7.3 ra thành `00034` | ✅ |
| 24/08 11:19 | phát hiện ERPNext v15 làm sẵn → "gần như không phải code" | ❌ **đã bị bác** |
| 25/08 11:45 | Thắng thử nghiệm thật, bác bỏ → **tự làm toàn bộ** | ✅ |
| 25/08 13:51 | khách thêm nhánh **tự sinh BOM** khi đủ rule + template | ✅ |

Đợt thử nghiệm 25/08 của Thắng: bật `enable_stock_reservation`, tạo `SO-26-00009` (Thành phẩm 1,
SL 30) → lõi giữ **26/30**; tạo `SO-26-00010` (SL 5) → giữ **0**. Chứng minh đúng hai giới hạn:
lõi chỉ tính tồn theo **một kho**, và chỉ giữ chỗ **mặt hàng trên đơn**, không giữ được NVL trong BOM.

---

## 5. Thứ tự làm — khác thứ tự đánh số

1. **Engine** (`00034`) — pool nhiều kho, ghim, netting BOM theo cấp
2. **Hiển thị** (`00023`) — Bảng 1, 1b, 2, ngày giao gợi ý
3. **Chặn xuất** (`00034`) — hàm kiểm dùng chung, gọi từ đủ **8 chứng từ**
4. **Test case** — `TC-REGR` liệt kê đủ 8 chứng từ; `TC-VALID` phủ ca mặt hàng *Sản xuất*
   không có BOM Template

---

## 6. Đang chặn — cập nhật 25/08

| # | Việc | Ai | Vì sao chặn |
|---|---|---|---|
| 1 | Tắt `enable_stock_reservation` về 0, dọn SRE của đợt thử | đội mình | Còn bật thì lõi ghi `Bin.reserved_stock` thật (đang có 26 trên *Thành phẩm 1*) → **hai sổ giữ chỗ song song**, mọi số đo đều nhiễu. Và ô *Reserve Stock* của lõi vẫn hiện trên form, dựng thêm ô của mình là người dùng thấy hai ô cùng nghĩa |
| 2 | Thắng duyệt mockup bản 5 của `00023` | Thắng | treo từ 24/08 14:04, `mockup_approved = 0` |
| 3 | 4 câu ở `00034`: quyền sinh BOM · ghi đè BOM mặc định · thời gian bấm Ghim · có nút Tính lại không | Thắng hỏi khách | quyết định cách code, không chặn duyệt mockup |
| 4 | Khách trả lời độ phủ BOM Template | Thắng hỏi khách | 8 template mới phủ 10.380/59.742 mặt hàng *Sản xuất* (~17%); 83% còn lại rơi vào nhánh *chỉ ghim thành phẩm* |

Việc 1 độc lập và làm được ngay. Việc 2, 3, 4 chạy song song.

---

## 7. Hạn

| Tính năng | Hạn đang ghi | Thực tế |
|---|---|---|
| `PM-FEAT-00023` | 26/08/2026 | **không còn hiệu lực** — mockup chưa duyệt, engine chưa có |
| `PM-FEAT-00034` | 05/09/2026 | hạn **tạm** để đủ trường bắt buộc của PM, chưa phải hạn khách chốt |

Đặt hạn thật sau khi có đáp cho việc 3 và 4 ở mục 6.

---

## 8. Tài liệu ở đâu

| Nội dung | Đường dẫn |
|---|---|
| Spec Phần IV | `docs/features/kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.md` |
| Spec chặn xuất kho | `docs/features/chan-xuat-kho-qua-ton-kha-dung.md` |
| Mockup Phần IV (bản 5) | `docs/mockups/kiem-tra-ton-kho-va-nguon-luc-tren-sales-order.html` |
| Mockup chặn xuất kho (bản 1) | `docs/mockups/chan-xuat-kho-qua-ton-kha-dung.html` |
| Phân tích của Thắng | PM Document `PM-DOC-00381` |
