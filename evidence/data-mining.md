# Đào data — cách đếm và kết quả

> Nguồn: menu quán trên GrabFood do nhóm (Thu) crawl. Script: `evidence/count_menu.py`. Data crawl **không commit** (quán thật); repo chỉ giữ số đã tổng hợp và vài ví dụ ngắn.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** `restaurants.csv` (258 quán) + `menu_items.csv` (11.322 món) crawl từ trang quán công khai trên GrabFood, khu vực quanh Vinhomes Ocean Park (Gia Lâm, Hà Nội). Ngày crawl: __ · cách lấy danh sách quán: __ *(Thu điền)*
- **Đếm gì · trên tập nào · lọc gì:** đếm trên **mọi món, mọi quán đã crawl**, không lọc:
  1. Món không có mô tả (cột `description` rỗng) — mẫu số: **mọi món** (11.322)
  2. Món có chữ "dị ứng" trong mô tả — mẫu số: **mọi món** (11.322)
  3. Quán có ≥1 món mà tên hoặc nhóm món có chữ "chay" — mẫu số: **mọi quán** (258)
- **Script:** `python evidence/count_menu.py <thư mục CSV>`

## 2. Đọc trước, đếm sau

Đã xem vài dòng đầu mỗi file, tên các cột và thống kê nhanh từng cột (Thu nên đọc thêm ~30–50 dòng và bổ sung). Các kiểu thấy được:
- Menu dài (trung bình 11.322 / 258 ≈ 44 món / quán), lẫn nhiều đồ uống, topping, món thêm.
- Nhiều món chỉ có tên, không có mô tả; món có mô tả thì thường ghi phần ăn kèm, ít khi ghi đủ nguyên liệu.
- Không quán nào có trường "chay" hay "thành phần" riêng; muốn biết phải đọc tên món.
- Hơn nửa số quán không ghi giờ mở cửa lúc crawl.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Món không có mô tả | 4.589 / 11.322 | 40,5% | Người chọn quán không biết món đó có gì |
| Mô tả có chữ "dị ứng" | 0 / 11.322 | 0% | Không quán nào cảnh báo dị ứng trên menu |
| Quán có ≥1 món ghi chữ "chay" | 19 / 258 | 7,4% | Người ăn chay phải lục nhiều quán mới thấy |

## 4. ≥5 ví dụ cụ thể (tên món trên menu công khai, không có mô tả)

1. Combo Cơm Thố Xá Xíu + Coca
2. Combo Cơm Thố Gà + Xá Xíu + Coca
3. Cocacola Lon
4. Combo Cơm Thố Đặc Biệt + Coca
5. Cam Ép Splash

*(5 món đầu theo thứ tự file trong số món không có mô tả, in ra từ script; nên bổ sung ví dụ là món chính thay cho đồ uống.)*

## 5. Giới hạn của data

- Chỉ một khu vực, một app, tại một thời điểm. Không đại diện cho mọi quán.
- Đếm "chay" theo chữ trong tên món, nên có thể sót món chay không ghi chữ "chay".
- Data cho biết **menu ghi gì**, không cho biết người chọn quán có thật sự gặp khó hay không, và **vì sao**.
- → Kiểm lại bằng khảo sát ≥20 người và phỏng vấn 3 người hay đứng ra chọn quán cho nhóm (Linh): chọn quán mất bao lâu, có ai không ăn được món của quán đã chọn không.
