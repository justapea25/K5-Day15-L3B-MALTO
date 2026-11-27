# Data card — dữ liệu bản chạy thử dùng

> Bản đầu (CP2). Phụ trách: Thu (crawl, mở rộng) · Minh (script dựng `restaurants.json`). Chấm ở rubric R4.

## Dataset 1 · Quán và menu dựng giả (synthetic, có seed) — nguồn cho agent

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ `search_restaurants`, `get_menu`, `check_constraints` (`codebase/tools.py`) · nền cho bộ câu thử |
| Từ đâu | **Nhóm tự sinh** bằng `scripts/gen_synthetic.py`, seed 42. Tên quán là tên dựng, món ghép từ mẫu tên món phổ biến |
| Cách sinh | Giá theo loại món, số món mỗi quán, khoảng cách, đánh giá, tỉ lệ món có mô tả, tỉ lệ quán ghi giờ mở cửa lấy theo **phân bố đo từ Dataset 2** (bảng `STATS` trong script). Riêng món chay được **tăng** (có 6 quán chay) để bộ câu thử có ca ăn chay. Nhãn `loai`, `chay`, `co_nhac`, `thit` gắn bằng cùng bộ từ khoá với `scripts/build_data.py`, chỉ dựa trên phần quán "ghi" (tên + mô tả) |
| Số dòng | 40 quán · 1.207 món · 66% món có mô tả · 219 món chay · 6 quán ghi giờ mở cửa |
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
