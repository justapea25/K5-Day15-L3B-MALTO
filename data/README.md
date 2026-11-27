# Thư mục data

Dữ liệu quán ăn **không nằm trong repo** (đã chặn bằng `.gitignore`). Bạn cần nhận 3 file CSV từ Thu (người phụ trách data) và lưu vào đúng thư mục này:

    data/grab/restaurants.csv
    data/grab/menu_items.csv
    data/grab/promotions.csv

Bắt buộc đúng thư mục và đúng tên file, vì `codebase/tools.py` đọc dữ liệu từ đường dẫn này. Thiếu file thì 3 công cụ `search_restaurants`, `get_menu`, `check_constraints` sẽ báo lỗi.

Kiểm tra đã đủ dữ liệu chưa (chạy ở thư mục gốc repo):

    python -c "from codebase.tools import search_restaurants; print(search_restaurants(limit=1)['total_matches'])"

Có in ra một con số lớn hơn 0 là dùng được.

Ý nghĩa từng cột xem `data/SCHEMA.md`. Nguồn, giới hạn và cách làm sạch dữ liệu xem `data/DATA_CARD.md`.
