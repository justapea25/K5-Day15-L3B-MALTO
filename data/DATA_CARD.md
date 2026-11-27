# Data card — dữ liệu bản chạy thử dùng

> Nhóm MALTO · Track D · bài "chọn quán cho nhóm có nhiều yêu cầu khác nhau". Một trang, mỗi dataset một mục.
> Cột và quan hệ giữa các bảng: `data/SCHEMA.md`. Dữ liệu nằm ở `data/grab/`.

## Dataset 1 · Quán ăn GrabFood quanh VinUni (dữ liệu thật)

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `search_restaurants`, `get_menu`, `check_constraints` · làm kho quán thật, không dùng dữ liệu giả |
| Từ đâu | trang công khai GrabFood VN (`food.grab.com/vn/vi/restaurants`), vị trí giao hàng đặt tại VinUni (Sảnh Thư Viện, Gia Lâm, Hà Nội). Đọc từ nội dung hiển thị trên trang, từng quán một, có nghỉ giữa các lần. Không dùng API nội bộ. |
| Xử lý những bước gì | lọc trùng quán · khử trùng món lặp ở nhóm "Ưu đãi hôm nay / Dành cho bạn" · tách giá gốc / giá giảm · tách voucher thành loại, % hoặc số tiền, đơn tối thiểu, giảm tối đa, hạn dùng · gắn mức giá (cheap < 40k ≤ mid ≤ 80k < high theo giá món trung vị) · cờ giao nhanh (ETA ≤ 20 phút) · đoán khu vực từ tên quán · phân loại quán ăn / quán đồ uống (`main_type`) · bỏ giá < 1.000đ (dòng ghi chú bị đọc nhầm thành giá) · gắn cờ voucher hết hạn (script: `data/grab/normalize_grab.py`, kiểm tra: `data/grab/check_data.py`) |
| Số dòng / số đoạn | 258 quán (258 có menu) · 11322 món (6733 món có mô tả) · 100 khuyến mãi (88 quán có voucher, 16 quán có giảm phí giao) |
| Phiên bản / ngày lấy | 2026-11-27 (một lần lấy, giá và khuyến mãi đổi theo ngày) |
| Nhãn | thật (dữ liệu công khai của quán; không có dữ liệu cá nhân) |
| Giới hạn | chỉ quán Grab giao tới VinUni (xa nhất 4.6 km, nên không phủ quán ngoài bán kính giao) · lệch về khu Vinhomes Ocean Park · menu và giá là ảnh chụp một thời điểm · 4589 món không có mô tả nên không biết thành phần (xử lý như không an toàn khi lọc ăn chay / dị ứng) · không có phí giao thực tế và không có mã voucher gõ tay (Grab áp ưu đãi tự động) · `area` đoán từ tên quán, 121 quán để trống · ETA là ước tính của Grab lúc lấy · 136 quán hiện "Closed" lúc lấy nên không có lịch mở cửa (`open_status=closed_at_crawl`) · 12 quán không có menu (`no_menu`, bỏ khỏi tìm kiếm) · 21 món không có giá dùng được (thường là món chọn size mới biết giá) · 0 khuyến mãi đã hết hạn (cờ `is_expired`; chỉ khuyến mãi còn hạn tính vào `has_voucher`) · 3 món chỉ xuất hiện ở mục "Ưu đãi / Dành cho bạn" nên nhóm món có thể không chính xác |

**Lưu ý dùng lại:** dữ liệu lấy từ trang của bên thứ ba. File thô `grab_raw*.json` không commit (đã thêm vào `.gitignore`). Trong slide và báo cáo, ghi nguồn và ngày lấy; số trong slide truy về `restaurants.csv`, `menu_items.csv`, `promotions.csv`.

**Phạm vi lọc ăn chay / dị ứng (đo bằng `MEAT_KEYWORDS` trong `codebase/tools.py` trên `menu_items.csv`):** khoảng 37% món có
từ khoá thịt / cá / hải sản trong tên hoặc mô tả, khoảng 29% món không có mô tả (công cụ coi là "không rõ thành phần", không an toàn),
khoảng 33% món qua được bộ lọc chay. Code chỉ bắt được thành phần được nêu trong tên và mô tả; món có mô tả nhưng không liệt kê
thành phần vẫn có thể chứa thứ cần tránh, nên `check_constraints` luôn kèm cảnh báo "chưa xác nhận với quán".

## Dataset 2 · Dữ liệu `synthetic`

Không có. Nhóm dùng thẳng dữ liệu thật ở trên, không tự sinh quán hay menu giả, nên không có mục `synthetic` cần kiểm tay.

**Không phải bằng chứng pain:** dữ liệu này chỉ là kho quán và menu cho công cụ. Bằng chứng pain nằm ở `evidence/`.
