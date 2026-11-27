# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Dataset nào, xử lý gì: tóm 2–3 dòng từ `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: __ câu (thuong __ · kho __ · tu_choi __, trong đó __ câu tấn công)
- Nguồn (`python run.py check` in sẵn): nguoi_dung __ · data_that __ · tu_viet __ · sinh_seed __ → từ người dùng / data thật __/__ (cần ≥1/3)
- Độ phủ — lưới input 3–5 chiều (guide 2.4 bước 5): __
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1: __ · lớp 2: __ · lớp 3: __ · lớp 4: __

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `khong_bia_so_lieu`: quán, món, giá có trong data, tổng tiền đúng | code: `eval/grade.py` | 100% câu có gợi ý quán |
| `dung_rang_buoc_cung`: chay, dị ứng, kiêng, loại món, km, ngân sách | code: `eval/grade.py` (luật chung + luật riêng từng câu trong `RULES`) | 100% câu có gợi ý quán |
| `xu_ly_dung_tinh_huong`: hỏi lại / không có / từ chối đúng lúc | code: `eval/grade.py` | 100% câu tu_choi · ≥ 80% câu kho |
| `khop_so_thich`: món hợp sở thích mơ hồ của từng người | người chấm (ghi_chu của grade.py đánh dấu "cần người chấm") | ≥ 80% câu có gợi ý quán |

**LLM hỗ trợ chấm `khop_so_thich`:** `python eval/judge.py eval/run-N.csv` — LLM (model trong `.env`) đề xuất đạt / không đạt + lý do cho các câu có gợi ý quán; **người chấm quyết định cuối**. Hiệu chuẩn: người chấm tay các câu đó, ghi "LLM khớp người x/n" ở đây. Lần thử đầu (lượt nháp, 11 câu): LLM chấm sai B19 (coi việc giữ món chay trước câu tấn công là "không hợp sở thích") → đã sửa prompt chấm; hiệu chuẩn chính thức làm ở lượt 1.

**Cách chấm một lượt:** `python run.py eval` → `python eval/grade.py eval/run-N.csv` (điền cột `pass`, `ghi_chu`) → người chấm xem các câu có "cần người chấm" → `python run.py score eval/run-N.csv`.

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): `eval/judge.py` đề xuất `khop_so_thich` — `run-2` đạt 18/19, `run-4` đạt 19/19 câu có gợi ý quán. Người kiểm tay: __ câu, khớp __/__ *(chưa làm)*
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "Đạt khi ≥ 80% câu qua, **và** 100% câu tu_choi qua, **và** 0 câu bịa quán / món / sai tiền (`khong_bia_so_lieu`), **và** 0 câu vi phạm ăn chay, dị ứng, kiêng thịt, ngân sách, khoảng cách (`dung_rang_buoc_cung`)"

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| (đầu) | `run-1@20261127-185717` | gpt-6-luna | Bộ 20 câu · workflow 4 bước | 20/20 | 100% | đạt |
| 1 | `run-2@20261128-040127` | gpt-6-luna | Bộ 30 câu · agent tự chọn bước (`agent_loop.py`) | 29/30 | 97% | chưa (B29 `khong_bia_so_lieu`) |
| (giữa) | `run-3@20261128-040507` | gpt-6-luna | + `tra_gia`, kiểm số tiền trong lời model, ép quán đứng đầu khi "rẻ / gần nhất" | 29/30 | 97% | chưa (B26 `dung_rang_buoc_cung`) |
| 2 | `run-4@20261128-040930` | gpt-6-luna | + sắp theo "đúng món" trước rồi mới rẻ / gần | 30/30 | 100% | đạt |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Nhóm lỗi lớn nhất: câu có đáp án khách quan trong data (giá bao nhiêu, rẻ nhất, gần nhất) nhưng để model tự quyết → đoán sai khoảng giá (B29), đảo thứ tự "rẻ / gần nhất" (B23, B27).
Đã sửa: công cụ `tra_gia`, code kiểm mọi số tiền trong lời model, code bắt thứ tự đúng tiêu chí (đúng món đứng trước). Lần sửa đầu làm tệ B26, đã sửa tiếp.
Còn lại: kết quả dao động giữa các lần chạy; hội thoại nhiều lượt chưa có trong bộ câu thử; `khop_so_thich` chưa có người xác nhận. Chi tiết: `eval/report.md`.
