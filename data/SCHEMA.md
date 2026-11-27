# Schema dữ liệu quán và menu (`data/restaurants.json`)

Quán **dựng giả**, sinh bằng `python scripts/gen_synthetic.py --seed 42` (xem `DATA_CARD.md`). Tiền là VND (số nguyên) · khoảng cách là km · `null` = không có thông tin (không phải 0).

## Cấp file

| Trường | Ý nghĩa |
|---|---|
| `_ghi_chu` | ghi chú nguồn: synthetic, không phải quán thật |
| `seed` | seed sinh dữ liệu (42) |
| `ma_di_ung` | mã chất gây dị ứng hợp lệ: `hai_san` `dau_phong` `sua` `trung` `dau_nanh` |
| `ma_thit` | mã loại thịt hợp lệ: `bo` `heo` `ga` `vit` `ca` `hai_san` |
| `ma_loai` | mã loại món hợp lệ: `banh_mi` `bun` `pho` `com` `mi` `lau` `chao` `xoi` `sushi` `ga_ran` `pizza` `nuong` `an_vat` `khac` |
| `quan` | danh sách 60 quán |

## Một quán (`quan[]`)

| Trường | Ý nghĩa |
|---|---|
| `id` | khoá, dạng `Q01` |
| `ten` | tên quán (tên dựng, viết hoa thường lộn xộn như ngoài đời) |
| `khu_vuc`, `am_thuc` | khu vực / kiểu ẩm thực |
| `khoang_cach_km` | khoảng cách (số sinh, không theo vị trí người dùng) |
| `danh_gia`, `so_danh_gia` | sao và số lượt đánh giá |
| `muc_gia` | mức giá chung của quán |
| `gio_mo` | giờ mở cửa, vd `"07:00-14:00 17:00-21:00"` |
| `freeship`, `khuyen_mai` | ưu đãi (data giả; **không có phí ship thật**) |
| `mon` | danh sách món |

## Một món (`mon[]`)

| Trường | Ý nghĩa |
|---|---|
| `id` | khoá, dạng `Q01-1` |
| `ten`, `gia`, `nhom` | tên món, giá, nhóm món |
| `mo_ta` | mô tả của quán; rỗng = quán không ghi thành phần |
| `loai` | loại món (một mã trong `ma_loai`) |
| `chay` | `true` nếu tên / nhóm ghi chay; `null` = không rõ, **coi như không chay** |
| `co_nhac` | chất gây dị ứng **được nhắc** trong tên / mô tả. Không có trong danh sách **không** có nghĩa là món không chứa |
| `thit` | loại thịt được nhắc |
| `ghi_thanh_phan` | `true` nếu có mô tả. `false` → coi như thành phần không rõ → kèm cảnh báo, không khẳng định an toàn |

## Bản đồ sang công cụ (`codebase/tools.py`)

| Công cụ | Đọc trường nào |
|---|---|
| `search_restaurants` | `khoang_cach_km`, `ten`, `gio_mo`, `danh_gia`, `so_danh_gia`, `muc_gia` |
| `get_menu` | toàn bộ `mon` của một quán |
| `check_constraints` | `gia`, `chay`, `co_nhac`, `thit`, `loai`, `khoang_cach_km`, `gio_mo` (code thuần, không gọi AI) |
