# Giao diện web (Next.js) — Chọn quán cho nhóm

Frontend cho bản chạy thử. Logic nằm hết ở backend Python (`codebase/`). Trang này chỉ gọi API và hiển thị kết quả.

## Chạy

Mở **2 cửa sổ lệnh**:

```bash
# 1. Backend — ở thư mục gốc repo
python codebase/web.py                # API ở http://127.0.0.1:8010

# 2. Frontend — trong thư mục web/
cd web
npm install                           # lần đầu
npm run dev                           # mở http://localhost:3010
```

- Next proxy `/api/*` sang backend (cấu hình trong `next.config.ts`). Backend chạy cổng khác thì đặt `BACKEND_URL=http://127.0.0.1:8020 npm run dev`.
- `http://localhost:3010/?q=<câu hỏi>`: điền sẵn câu hỏi và chạy luôn, tiện khi demo.
- Không có Node thì vẫn dùng được giao diện dự phòng: chỉ cần chạy `python codebase/web.py` rồi mở http://localhost:8010.

## Ảnh quán và món

Ảnh trong `public/img/{quan,mon}/<id>.webp` là **ảnh minh hoạ do AI tạo**, không phải ảnh quán hay món thật, vì quán trong data là dựng giả. Ảnh món dùng `gpt-image-1-mini` (low). Ảnh quán dùng `gpt-image-2` (medium), khoảng $0.05 mỗi ảnh. Thêm quán hoặc món mới vào `data/restaurants.json` thì chạy ở thư mục gốc repo:

```bash
python scripts/gen_images.py --kind mon                                        # ảnh món còn thiếu
python scripts/gen_images.py --kind quan --model gpt-image-2 --quality medium  # ảnh quán còn thiếu
``` Món chưa có ảnh thì giao diện hiện emoji thay thế.

## File

| File | Làm gì |
|---|---|
| `app/app.tsx` | Toàn bộ giao diện (client component): ô nhập, câu mẫu, kết quả có ảnh, thanh ngân sách, luồng 6 bước, trace, lưới quán và menu có ảnh |
| `app/photo.tsx` | Ảnh quán / món (`next/image`), chưa có ảnh thì hiện emoji |
| `app/types.ts` | Kiểu dữ liệu khớp với `codebase/web.py` và `ket_qua` trong `codebase/agent.py` |
| `app/globals.css` | Màu sáng / tối (Tailwind v4) |
| `next.config.ts` | Rewrites `/api/*` → backend Python |

Next.js 16.4 · React 19 · Tailwind 4.
