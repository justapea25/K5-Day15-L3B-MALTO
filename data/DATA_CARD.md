# Data card — dữ liệu bản chạy thử dùng

> Bản đầu (CP2). Phụ trách: Thu (crawl, mở rộng) · Minh (script dựng `restaurants.json`). Chấm ở rubric R4.

## Dataset 1 · Quán và menu dựng giả (synthetic, có seed) — nguồn cho agent

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ `search_restaurants`, `get_menu`, `check_constraints` (`codebase/tools.py`) · nền cho bộ câu thử |
| Từ đâu | **Nhóm tự sinh** bằng `scripts/gen_synthetic.py` (+ `scripts/diverse_shops.py`), seed 42. 30 quán Việt (bún, phở, cơm, chay, mì, bánh mì, lẩu; đã bỏ bớt 10 quán trùng kiểu) + 30 quán thuộc 18 kiểu như trên Grab (Nhật, Hàn, Hoa, Thái, Đài Loan, Ấn, gà rán, pizza, hải sản, lẩu nướng, cháo, xôi, bánh cuốn, healthy, ăn vặt, cơm văn phòng, miền Trung, miền Nam). Tên quán là **tên dựng** ghép theo kiểu đặt tên thật trên Grab (tên chủ + món + toà / khu, viết hoa thường lộn xộn); món theo mẫu tên món phổ biến, khoảng giá theo mặt bằng giá trên Grab *(tự ước tính)* |
| Cách sinh | Giá theo loại món, số món mỗi quán, khoảng cách, đánh giá, tỉ lệ món có mô tả, tỉ lệ quán ghi giờ mở cửa lấy theo **phân bố đo từ Dataset 2** (bảng `STATS` trong script). Riêng món chay được **tăng** (có 6 quán chay) để bộ câu thử có ca ăn chay. **Khác data thật:** data thật chỉ 25/60 quán có sao và 7/60 ghi giờ mở cửa; bản giả bổ sung sao, số lượt đánh giá và giờ mở cửa cho mọi quán (sinh bằng RNG riêng, seed + 1, không đổi các trường khác) để giao diện và bước lọc giờ dùng được. Nhãn `loai`, `chay`, `co_nhac`, `thit` gắn bằng cùng bộ từ khoá với `scripts/build_data.py`, chỉ dựa trên phần quán "ghi" (tên + mô tả) |
| Số dòng | 60 quán · 1.142 món · 66% món có mô tả · 164 món chay · mọi quán có đánh giá (sao + số lượt) và giờ mở cửa · loại món: bun, pho, com, mi, banh_mi, lau, chao, xoi, sushi, ga_ran, pizza, nuong, an_vat, khac |
| Chạy lại | `python scripts/gen_synthetic.py --seed 42` ra đúng file đang commit |
| Nhãn | `synthetic` — **không phải quán thật, không phải bằng chứng pain** |
| Giới hạn | Không có phí ship · khoảng cách là số sinh, không theo vị trí người dùng · món ghép từ mẫu nên ít đa dạng hơn menu thật · không có khuyến mãi |

**Các trường của một món:** `loai` (bun · pho · com · mi · banh_mi · lau · khac) · `chay` (`true` nếu ghi chay, `null` = không rõ, coi như không chay) · `co_nhac` (chất gây dị ứng **được nhắc** trong tên / mô tả; không có trong danh sách **không** có nghĩa là món không chứa) · `thit` · `ghi_thanh_phan` (có mô tả hay không).

## Dataset 2 · Menu quán ăn trên GrabFood quanh Vinhomes Ocean Park — chỉ để đo số liệu và làm bằng chứng

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (đếm x/N, ghi ở `evidence/data-mining.md`) · đo phân bố để sinh Dataset 1. **Không đưa cho agent** |
| Từ đâu | Nhóm (Thu) crawl trang quán công khai trên GrabFood. Ngày crawl: __ · cách lấy danh sách quán: __ · có cần đăng nhập không: __ *(Thu điền)* |
| Quy mô | 258 quán · 11.322 món · 100 khuyến mãi (3 file CSV) |
| Lưu ở đâu | **Ngoài repo, không commit** (dữ liệu crawl của quán thật). Repo chỉ giữ số đã tổng hợp và vài ví dụ ngắn |
| Xử lý | `scripts/build_data.py` lọc món chính và gắn nhãn từ khoá, dùng để đo các số trong `STATS` của `scripts/gen_synthetic.py` |
| Giới hạn | Một khu vực, một app, tại một thời điểm · nhãn từ khoá có thể sót hoặc nhầm |
