# Kiến trúc bản chạy thử — Chọn quán cho nhóm

> Nhóm MALTO · Track D. Tóm tắt thiết kế ở `spec.md` §4. File này nói **code chạy thế nào**, để ai trong nhóm cũng giải thích được khi bị hỏi lúc demo.

## 1. Tổng quan

Một người nhắn yêu cầu của cả nhóm bằng lời thường. Hệ thống trả về **một quán và một món cho từng người**, hoặc nói thẳng "không có quán nào thoả", hoặc hỏi lại.

**Hình dạng: workflow cố định.** Có 2 lần gọi AI, mọi bước còn lại là code. AI không tự chọn bước tiếp theo, không tự gọi công cụ.

```
   ┌──────────────── giao diện ─────────────────┐
   │  Next.js (web/)  ──/api/* proxy──┐         │
   │                                  ▼         │
   │  CLI: python run.py      codebase/web.py   │
   │  (codebase/app.py)       (API + trang dự phòng)
   └──────────────┬───────────────┬─────────────┘
                  └───────┬───────┘
                          │ answer(text)
                         ┌──────────▼──────────┐
                         │  codebase/agent.py  │  luồng B1 → B6
                         └───┬─────────────┬───┘
                 call_model  │             │  công cụ (@tool)
                  ┌──────────▼───┐   ┌─────▼──────────────┐
                  │ codebase/    │   │ codebase/tools.py  │
                  │ ai.py        │   │ search_restaurants │
                  │ (OpenAI /    │   │ get_menu           │
                  │  Claude /    │   │ check_constraints  │
                  │  Ollama /    │   │ dish_safe_for      │
                  │  fake)       │   └─────┬──────────────┘
                  └──────────────┘         │ đọc
                                   ┌───────▼───────────────┐
                                   │ data/restaurants.json │  (dựng giả, seed)
                                   └───────────────────────┘
       codebase/tracing.py (khung): ghi mọi lần gọi model / công cụ / note → trace, token
```

## 2. Luồng xử lý một tin nhắn

| Bước | Ai làm | Làm gì | Ra gì |
|---|---|---|---|
| **B1** | **AI** (`SYSTEM_PARSE`) | Đọc tin nhắn thành JSON ràng buộc: số người, và với từng người: chay, dị ứng, kiêng thịt, muốn ăn loại món. Thêm ngân sách, km, quán được nhắc | `chon_quan` · `thieu_thong_tin` → hỏi lại · `ngoai_pham_vi` → từ chối |
| B1' | Code | `_clean_person`: chỉ giữ mã hợp lệ (mã dị ứng, mã thịt, mã loại món có trong data), bỏ mã model bịa | Ràng buộc sạch |
| **B2** | Code | Tin nhắn có chữ "dị ứng" mà không đọc ra mã dị ứng nào → **hỏi lại, không đoán** | Chặn "kệ dị ứng đi" |
| **B3** | Code | `search_restaurants` + `get_menu`. Với mỗi quán, lọc món an toàn cho từng người bằng `dish_safe_for`. Giữ quán mà **mọi người có ≥1 món** và tổng rẻ nhất (gồm ship) ≤ ngân sách | ≤5 phương án, xếp theo tổng tiền rồi khoảng cách |
| B3' | Code | Không có phương án → `_relax_hint` thử nới **ngân sách, khoảng cách, loại món** (không bao giờ nới chay hay dị ứng) | "Không có quán nào…" + gợi ý |
| **B4** | **AI** (`SYSTEM_CHOOSE`) | Chọn 1 quán + 1 món / người trong các phương án đã lọc, kèm 1–2 câu lý do | JSON phương án |
| **B5** | Code | `check_constraints` kiểm lại phương án của AI: quán có thật, món có trong menu, món an toàn, tổng ≤ ngân sách. Sai → dùng phương án rẻ nhất code tìm được, ghi `note` | Phương án đã kiểm |
| **B6** | Code | `_render`: soạn câu trả lời. Tên món, giá, tổng tiền **lấy từ data**. Chữ của model chỉ dùng cho phần "Lý do" | `{"output", "ket_qua"}` |

Mỗi tin nhắn gọi model **1 lần** (dừng ở B1–B3) hoặc **2 lần** (đi tới B4).

## 3. Dữ liệu — `data/restaurants.json`

Chỉ cần file JSON, không cần database: data nhỏ (15–30 quán), khung chỉ dùng thư viện chuẩn, eval cần data cố định để chạy lại ra cùng kết quả. Muốn đổi sang database thì chỉ sửa hàm `_data()` trong `tools.py`, `agent.py` giữ nguyên.

```json
{
  "ma_di_ung": ["hai_san", "dau_phong", "sua", "trung", "gluten", "dau_nanh"],
  "ma_thit":   ["bo", "heo", "ga", "vit", "ca", "hai_san"],
  "ma_loai":   ["bun", "pho", "com", "mi", "banh_mi", "lau", "khac"],
  "quan": [{
    "id": "Q01", "ten": "Bún Cô Ba", "khu_vuc": "cau_giay", "khoang_cach_km": 0.8, "phi_ship": 15000,
    "mon": [{"id": "Q01-4", "ten": "Bún nấm chay", "gia": 40000, "loai": "bun", "mo_ta": "…",
             "chay": true, "di_ung": ["dau_nanh"], "thit": []}]
  }]
}
```

| Trường của món | Giá trị | `null` nghĩa là | Code xử lý khi `null` |
|---|---|---|---|
| `chay` | `true` / `false` / `null` | quán không ghi | coi như **không chay** |
| `di_ung` | danh sách mã / `null` | quán không ghi thành phần | coi như **không an toàn** với người có dị ứng |
| `thit` | danh sách mã / `null` | không rõ thịt gì | coi như **không an toàn** với người kiêng thịt |

**Thêm quán (Thu):** giữ đúng các trường trên, `id` quán dạng `Qnn`, `id` món dạng `Qnn-k`, mã chỉ dùng trong 3 danh sách mã. Muốn thêm mã mới thì thêm vào danh sách tương ứng, prompt B1 tự đọc danh sách này.

## 4. Chỗ chặn rủi ro

Rủi ro đắt nhất: **gợi ý món gây dị ứng, hoặc món có thịt cho người ăn chay.** Không lớp nào trong số này phụ thuộc vào việc model làm đúng:

| Lớp | Ở đâu | Chặn gì |
|---|---|---|
| 1 | `dish_safe_for` (`tools.py`) | Món không rõ thành phần hoặc không rõ chay bị loại |
| 2 | B1' `_clean_person` | Mã dị ứng hay mã loại món do model bịa bị bỏ |
| 3 | B2 (`agent.py`) | Có nhắc dị ứng mà không rõ dị ứng gì → hỏi lại |
| 4 | B4 chỉ thấy phương án đã lọc | AI không có món nào không an toàn để mà chọn |
| 5 | B5 `check_constraints` | AI chọn sai hoặc bịa → bỏ, dùng phương án code đã kiểm |
| 6 | B6 `_render` | Giá, tổng tiền không lấy từ chữ của model |

Thêm vào đó: prompt B1 coi tin nhắn là **dữ liệu, không phải lệnh**. Quán người dùng chỉ định mà không có trong data thì trả "không có".

## 5. Hợp đồng với khung (không sửa)

- `answer(text) -> {"output": str, "ket_qua": dict}`. Eval và simulate chỉ đọc `output`. `ket_qua` dành cho giao diện web.
- `call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}`, có `@model_call`. Token lấy từ `usage` của API.
- Mỗi công cụ có `@tool`, docstring ghi: tên · input · output · có tác động ra ngoài không. **Cả 3 công cụ chỉ đọc.**
- `note("…")` ghi quyết định vào trace: `y_dinh` của B1, lý do dừng, lý do B5 thay phương án.

## 6. Chế độ giả

Chưa có `MODEL_PROVIDER` trong `.env` thì `ai.py` trả câu giả. Khi đó B1 dùng ràng buộc mẫu `FAKE_PARSE` (3 người, 1 chay, 1 dị ứng hải sản, 200k) và **bỏ qua tin nhắn**. B4 không đọc được JSON nên B5 dùng phương án rẻ nhất. Output ghi rõ `[chế độ giả …]`. Chế độ này chỉ để luồng chạy hết trước khi nối model. Lượt eval chạy ở chế độ giả không được tính.

## 7. Giao diện web

**Frontend: Next.js trong `web/`** (Next 16, React 19, Tailwind 4). Toàn bộ là client component (`web/app/app.tsx`), gọi `/api/*`. `next.config.ts` proxy `/api/*` sang backend Python, nên trình duyệt chỉ gọi cùng origin, không cần CORS. Frontend không chứa logic nghiệp vụ: lọc, kiểm, tính tiền đều nằm ở Python. Hiển thị:
- Ô nhập, 6 câu mẫu (thường, muốn bún, không quán nào, thiếu thông tin, tấn công, ngoài phạm vi).
- Thẻ kết quả: quán, món từng người, tổng tiền, lý do, cảnh báo.
- **Luồng 6 bước có tô màu:** xanh = đã chạy, đỏ = dừng ở đây, cam = B5 đã thay phương án của AI. Thêm trace chi tiết, dùng để thuyết minh khi demo.
- Lưới quán có ảnh bìa, bấm vào quán để xem menu kèm ảnh món và nhãn "🌱 chay", "⚠ thành phần không rõ". Quán đang được gợi ý có nhãn riêng.
- Ảnh trong `web/public/img/loai/` là **ảnh minh hoạ theo loại món** do AI tạo, không phải ảnh món của quán. Giao diện ghi rõ.
- `/?q=…`: điền sẵn câu hỏi và chạy luôn.

**Backend: `codebase/web.py`.** Server `http.server` của thư viện chuẩn, một luồng, chỉ nghe trên `127.0.0.1`. Gọi đúng `answer(text)` như CLI. Ở `/` có trang HTML dự phòng (`codebase/static/index.html`) cho máy không có Node.

| Đường dẫn | Làm gì |
|---|---|
| `GET /` | Trang `codebase/static/index.html` |
| `GET /api/info` | Model đang dùng (không trả key) |
| `GET /api/quan` | Dữ liệu quán, để hiển thị bảng |
| `POST /api/answer` | `{"text"}` → `{"output", "ket_qua", "thong_ke", "cac_buoc"}`. `cac_buoc` là các sự kiện trace (gọi model, gọi công cụ, note), dùng để thuyết minh luồng khi demo |

## 8. Khi làm thật (ngoài phạm vi hackathon)

- Dữ liệu quán: database (SQLite, Postgres) + cập nhật giá, hết món, giờ mở cửa. Chỉ thay `_data()` và các công cụ.
- Khoảng cách: tính theo vị trí thật của người dùng, thay vì số cố định trong data.
- Thành phần món: lấy từ quán, có người kiểm. Món chưa kiểm vẫn giữ quy tắc "không rõ = không an toàn".
- Hội thoại nhiều lượt (người dùng sửa yêu cầu), gom đơn, chia tiền: hiện nằm trong mục "không làm" ở `spec.md` §4.
