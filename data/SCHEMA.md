# Schema dữ liệu quán và menu

Nguồn: GrabFood, quán giao tới VinUni, lấy ngày 27/11/2026 (chi tiết và giới hạn: `data/DATA_CARD.md`).
Sinh bằng `python data/grab/normalize_grab.py data/grab/grab_raw_final.json`, kiểm bằng `python data/grab/check_data.py`.
Công cụ đọc ba file CSV (UTF-8, có BOM) trong `data/grab/`; không sửa tay, sửa script rồi chạy lại.

Quy ước: tiền là đồng (VND, số nguyên) · khoảng cách là km từ VinUni · cột bool là `True` / `False` ·
ô rỗng = không có thông tin (không phải 0).

## `restaurants.csv` — 1 dòng / quán (258 dòng)

| Cột | Ý nghĩa |
|---|---|
| `restaurant_id` | khoá chính, lấy từ link Grab (vd `5-C763NRAVVYBCR2`) |
| `name` | tên quán trên Grab |
| `area` | khu vực, **đoán từ tên quán** (vd "Vinhomes Ocean Park"); 121 quán để trống |
| `cuisine` / `cuisine_tags` | loại món Grab ghi / tách thành thẻ, ngăn bằng `\|` |
| `main_type` | `food` (quán ăn) hoặc `drink` (quán đồ uống, suy từ `cuisine`) |
| `distance_km` | khoảng cách tới VinUni theo Grab |
| `eta_min` / `is_fast` | thời gian giao ước tính của Grab (phút) / `True` nếu ≤ 20 phút |
| `rating` | điểm đánh giá (0–5), có thể rỗng |
| `open_hours` / `open_status` | giờ mở cửa hôm lấy dữ liệu · `has_hours` (có giờ), `closed_at_crawl` (Grab hiện "Closed" lúc lấy, không có lịch), `no_menu` (không có menu, bỏ khỏi tìm kiếm) |
| `n_items` | số món sau khi khử trùng |
| `min_price_vnd` / `median_price_vnd` / `max_price_vnd` | giá món thấp nhất / trung vị / cao nhất |
| `price_level` | `cheap` (< 40k), `mid` (40k–80k), `high` (> 80k) theo giá món trung vị |
| `has_voucher` / `has_freeship` | có khuyến mãi còn hạn / có ưu đãi giảm phí giao còn hạn |
| `n_discounted_items` / `max_item_discount_pct` | số món đang giảm giá / mức giảm cao nhất |
| `promo_summary` | tiêu đề các khuyến mãi còn hạn, ngăn bằng ` ; ` |
| `url` | trang quán trên Grab |
| `menu_crawled` / `promo_crawled` | đã lấy menu / đã lấy chi tiết khuyến mãi |

## `menu_items.csv` — 1 dòng / món (11.322 dòng)

| Cột | Ý nghĩa |
|---|---|
| `item_id` | khoá chính, dạng `<restaurant_id>#<số thứ tự>` |
| `restaurant_id` | khoá ngoại → `restaurants.csv` |
| `category` | nhóm món theo quán (vd "Cơm Thố", "Đồ Uống") |
| `item_name` | tên món, giữ nguyên chữ của quán |
| `price_vnd` | giá bán hiện tại; **rỗng** khi Grab không hiện giá (món chọn size mới có giá) hoặc giá không hợp lệ |
| `price_flag` | `missing` (Grab không hiện giá) · `invalid_lt_1000` (giá < 1.000đ, dòng ghi chú bị đọc nhầm) · rỗng nếu giá dùng được |
| `original_price_vnd` / `discount_vnd` / `discount_pct` | giá gốc, số tiền giảm, % giảm — chỉ có khi món đang giảm giá |
| `kcal` | calo Grab ghi (nếu có). Không dùng để tư vấn dinh dưỡng |
| `description` | mô tả món của quán, đã bỏ phần calo; **rỗng nghĩa là quán không ghi thành phần** |
| `has_description` | `True` nếu `description` không rỗng |
| `only_in_promo_section` | `True` nếu món chỉ xuất hiện ở mục "Ưu đãi / Dành cho bạn" nên `category` có thể không chính xác |

## `promotions.csv` — 1 dòng / khuyến mãi (100 dòng)

| Cột | Ý nghĩa |
|---|---|
| `restaurant_id` | khoá ngoại → `restaurants.csv` |
| `type` | `delivery_fee` (giảm phí giao) · `item_discount` (giảm một số sản phẩm) · `order_discount` (giảm theo đơn) · `buy_gift` (mua / đặt đơn tặng quà) · `other` |
| `is_freeship` | `True` nếu `type = delivery_fee` |
| `title` | nội dung khuyến mãi như Grab hiển thị |
| `discount_pct` / `discount_vnd` | % giảm hoặc số tiền giảm (một trong hai) |
| `min_order_vnd` / `max_discount_vnd` | đơn tối thiểu / mức giảm tối đa |
| `valid_from` / `valid_to` | thời hạn (rỗng nếu Grab không ghi) |
| `conditions` | điều kiện đi kèm, ngăn bằng ` \| ` |
| `is_expired` | `True` nếu `valid_to` trước ngày lấy dữ liệu (đã loại khỏi `has_voucher`) |

Grab áp ưu đãi tự động, **không có mã voucher gõ tay**. Không có phí giao thực tế (chỉ hiện ở giỏ hàng).

## Khoá và quan hệ

`restaurants.restaurant_id` 1—n `menu_items.restaurant_id` · 1—n `promotions.restaurant_id`.
`check_data.py` kiểm: không trùng khoá, không món mồ côi, giá gốc lớn hơn giá bán, mọi quán có menu và khuyến mãi.

## Bản đồ sang công cụ (`codebase/tools.py`)

| Công cụ | Đọc cột nào |
|---|---|
| `search_restaurants` | `distance_km`, `eta_min`, `price_level`, `cuisine`, `main_type`, `rating`, `has_freeship`, `has_voucher`, `open_status` + tên món |
| `get_menu` | `menu_items.*` + `promotions.*` của quán |
| `check_constraints` | `price_vnd`, `item_name`, `description`, `distance_km`, `eta_min`, `has_freeship`, `open_status` |
