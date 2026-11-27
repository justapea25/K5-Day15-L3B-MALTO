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

## Ảnh

`public/img/loai/<loại món>.webp` là **ảnh minh hoạ theo loại món** (bún, phở, cơm, bánh mì, lẩu) do AI tạo, không phải ảnh món của quán nào. Loại chưa có ảnh thì hiện emoji. Giao diện ghi rõ "ảnh minh hoạ".

## File

| File | Làm gì |
|---|---|
| `app/app.tsx` | Toàn bộ giao diện (client component): ô nhập, câu mẫu, khung chat, thẻ gợi ý (ảnh minh hoạ theo loại món, thanh ngân sách), luồng 6 bước, trace, danh sách quán có tìm kiếm và menu |
| `app/types.ts` | Kiểu dữ liệu khớp với `codebase/web.py` và `ket_qua` trong `codebase/agent.py` |
| `app/globals.css` | Màu sáng / tối (Tailwind v4) |
| `next.config.ts` | Rewrites `/api/*` → backend Python |

Next.js 16.4 · React 19 · Tailwind 4.
