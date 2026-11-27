# Đào data — cách đếm và kết quả

> Nhóm MALTO · Track D. Script đếm: `evidence/count.py` (chạy ở thư mục gốc repo: `python evidence/count.py`, người khác chạy lại ra cùng số).
> Repo chỉ chứa số đã tổng hợp — không chép lại nguyên file data. File thô `grab_raw*.json` không commit.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: `data/grab/restaurants.csv`, `menu_items.csv`, `promotions.csv` — lấy từ GrabFood VN (`food.grab.com/vn/vi/restaurants`), vị trí giao hàng đặt tại VinUni, **một lần lấy ngày 2026-11-27** (giá và khuyến mãi đổi theo ngày). Lấy từ nội dung hiển thị công khai trên trang, **không cần đăng nhập**, không dùng API nội bộ; danh sách quán lấy từ trang danh sách của Grab với vị trí VinUni, sau đó mở từng quán để đọc menu và khuyến mãi, có nghỉ giữa các lần.
- Đếm gì: các đặc điểm của quán và món mà một nhóm bạn có nhiều yêu cầu khác nhau (ngân sách, ăn chay / dị ứng, giao nhanh, đang mở cửa, có ưu đãi) sẽ vướng khi tự chọn quán trên Grab · trên tập nào: quán và món trong 3 CSV · lọc gì: bỏ 12 quán `no_menu` (không có menu, bỏ khỏi tìm kiếm).
- **Mẫu số là gì:** với số đếm theo quán: **246 quán có menu** (258 − 12 `no_menu`). Với số đếm theo món: **11.322 món** (toàn bộ `menu_items.csv`).
- Script / công thức: `python evidence/count.py`. Kiểm tra chất lượng data: `python data/grab/check_data.py` (không có lỗi nặng).

## 2. Đọc trước, đếm sau

Đã đọc dòng đầu của 3 CSV và từ điển cột (`data/SCHEMA.md`). Các *kiểu* thấy được trước khi định nghĩa thứ cần đếm:
- Hơn một nửa quán hiện "Closed" lúc lấy, nên không có lịch mở cửa — người chọn quán dễ chọn trúng quán đang đóng.
- Nhiều món không có mô tả nên không biết thành phần; ai ăn chay / dị ứng không tự kiểm được bằng cách đọc menu.
- Ưu đãi nằm rải rác ở từng quán (giảm món, giảm theo đơn, giảm phí giao), mỗi loại có điều kiện riêng; chỉ một số ít quán có.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Quán hiện "Closed" lúc lấy | 136/246 | 55% | không có lịch mở cửa (`closed_at_crawl`); lấy lúc ~08:40 sáng, nên tỉ lệ này chịu ảnh hưởng giờ lấy |
| Quán giao nhanh (ETA ≤ 20 phút) | 11/246 | 4% | ETA là ước tính của Grab lúc lấy |
| Quán có giảm phí giao | 16/246 | 7% | |
| Quán có voucher còn hạn | 86/246 | 35% | 100 khuyến mãi, 0 cái hết hạn |
| Quán mức giá cheap / mid / high | 53 / 140 / 53 trên 246 | 22% / 57% / 22% | theo giá món trung vị: < 40k / 40–80k / > 80k |
| Quán đồ uống | 73/246 | 30% | còn lại là quán ăn |
| Quán không đoán được khu vực | 116/246 | 47% | `area` đoán từ tên quán |
| Món không có mô tả (không biết thành phần) | 4.589/11.322 | 41% | xử lý như không an toàn khi lọc chay / dị ứng |
| Món qua được bộ lọc chay | 2.882/11.322 | 25% | có mô tả và không chứa từ khoá thịt/cá trong `MEAT_KEYWORDS`; xấp xỉ, bộ lọc trong công cụ so khớp có dấu nên có thể lệch vài điểm % |
| Quán có ≥ 1 món qua bộ lọc chay | 198/246 | 80% | nhưng chỉ 25% món, nên chọn được quán chưa chắc chọn được món |
| Món đang giảm giá | 299/11.322 | 3% | |
| Món không có giá dùng được | 21/11.322 | 0,2% | thường là món chọn size |

## 4. ≥5 ví dụ cụ thể (mã quán, tên như hiển thị công khai trên Grab)

Chạy `python evidence/count.py` rồi lấy các dòng thật trong `restaurants.csv` / `menu_items.csv` — mỗi ví dụ ghi `restaurant_id` hoặc `item_id`:

1. Quán `closed_at_crawl`: Cơm Tấm Mẹ Sóc - Cơm Văn Phòng Vinhomes Ocean Park (`5-C4LUTRNKVCJCV6`)
2. Món không có mô tả, không biết thành phần: "Bò Húc Thái" (`5-C763NRAVVYBCR2#034`)
3. Món không có giá vì phải chọn size: "Phê Latte (hạt Colom, Ethi) - Đá" — `price_flag = missing`
4. Voucher kèm điều kiện đơn tối thiểu: "Giảm 1.000₫ phí giao hàng khi đặt đơn tối thiểu 99.000₫" (`5-C763NRAVVYBCR2`, `promotions.csv`)
5. Quán `no_menu` bị loại khỏi tìm kiếm: `5-C8CFJKBHUAJEFE`, `5-C8KZVUA3SAABBA` (Arirang và LA'NUT - Pizza & Steak - Ocean Park 1 nằm trong 12 quán này)

## 5. Giới hạn của data

Data cho biết quán và món **có gì**, không cho biết **vì sao** nhóm bạn khó chọn, hay họ có thực sự gặp các vướng mắc trên. Thiếu / lệch:
- Một lần lấy (2026-11-27, buổi sáng): trạng thái mở cửa, giá, khuyến mãi chỉ đúng thời điểm đó.
- Chỉ quán Grab giao tới VinUni (xa nhất 4.6 km), lệch về khu Vinhomes Ocean Park.
- Không có phí giao thực tế, không có dữ liệu hành vi đặt món của nhóm nhiều người.
- Không phải bằng chứng pain: pain phải kiểm bằng khảo sát / phỏng vấn của Linh.

→ Kiểm lại bằng: khảo sát ≥ 20 người và phỏng vấn 3 người (`evidence/survey/`, `evidence/interviews/`, Linh phụ trách).
