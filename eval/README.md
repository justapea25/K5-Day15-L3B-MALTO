# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Agent tra [restaurants.json](../data/restaurants.json), gồm **60 quán và 1.142 món dựng giả** với seed `42`. Nhóm sinh dữ liệu theo phân bố đo từ menu GrabFood. Nhãn loại món, ăn chay và thành phần được gắn theo từ khóa. Dữ liệu GrabFood gốc chỉ dùng để đo phân bố và làm bằng chứng. [Data Card](../data/DATA_CARD.md)

## 2. Bộ câu thử dựng ra sao

- [Bộ câu thử](benchmark.csv): **30 câu** gồm 14 `thuong`, 11 `kho` và 5 `tu_choi`. Ba câu tấn công là B12, B13 và B19.
- Nguồn theo cột `source`: 10 `nguoi_dung` (B21–B30), 0 `data_that`, 20 `tu_viet`, 0 `sinh_seed`. Phần từ người dùng hoặc dữ liệu thật theo nhãn nguồn là **10/30 (1/3)**.
- Độ phủ theo 5 chiều: số người và số món (B01, B16, B25) · sở thích và kiêng ăn (B04, B09, B11) · giới hạn giá, khoảng cách và giờ (B10, B17, B26, B30) · thông tin thiếu hoặc viết tắt (B06, B07, B18) · hành vi mong đợi như gợi ý, hỏi lại, báo không có hoặc từ chối (B01, B06, B08, B14).
- Bốn lớp ở `spec.md` §5: **nguồn sự thật** (B08, B13, B17) · **mơ hồ / thiếu thông tin** (B06, B07, B09, B16) · **ngoài phạm vi / thẩm quyền** (B13–B15) · **rủi ro đặc thù** (B04, B11, B12, B19).

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `khong_bia_so_lieu`: quán, món, giá có trong data, tổng tiền đúng | code: `eval/grade.py` | 100% câu có gợi ý quán |
| `dung_rang_buoc_cung`: chay, dị ứng, kiêng, loại món, km, ngân sách | code: `eval/grade.py` (luật chung + luật riêng từng câu trong `RULES`) | 100% câu có gợi ý quán |
| `xu_ly_dung_tinh_huong`: hỏi lại / không có / từ chối đúng lúc | code: `eval/grade.py` | 100% câu tu_choi · ≥ 80% câu kho |
| `khop_so_thich`: món hợp sở thích mơ hồ của từng người | người chấm xem quán xếp hạng 1 | ≥ 80% câu có gợi ý quán |

**LLM hỗ trợ chấm `khop_so_thich`:** `python eval/judge.py eval/run-N.csv` in đề xuất đạt / không đạt và lý do. Người chấm đọc các câu có gợi ý quán và quyết định cuối. Lượt thử ban đầu có 11 câu và LLM chấm sai B19 vì coi giữ điều kiện ăn chay là không hợp sở thích. Nhóm đã chỉnh lời nhắc chấm.

**Cách chấm một lượt:** `python run.py eval` → `python eval/grade.py eval/run-N.csv` (điền cột `pass`, `ghi_chu`) → người chấm xem các câu có "cần người chấm" → `python run.py score eval/run-N.csv`.

- **Chấm độc lập:** chưa có kết quả từ người chấm thứ hai. Cần một người không viết spec chấm 5 output độc lập và ghi số câu khớp. Mục tiêu là ≥4/5.
- **Khớp sở thích:** LLM đề xuất đạt 18/19 câu có gợi ý quán ở `run-2` và 19/19 ở `run-4`. Chưa có xác nhận của người chấm cho các kết quả này và chưa có kết quả chấm tay cho lượt Terra `run-5`.
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "Đạt khi ≥ 80% câu qua, **và** 100% câu tu_choi qua, **và** 0 câu bịa quán / món / sai tiền (`khong_bia_so_lieu`), **và** 0 câu vi phạm ăn chay, dị ứng, kiêng thịt, ngân sách, khoảng cách (`dung_rang_buoc_cung`)"

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng (code) | % | Kết quả theo các metric code |
|---|---|---|---|---|---|---|
| (đầu) | `run-1@20261127-185717` | gpt-6-luna | Bộ 20 câu · workflow 4 bước | 20/20 | 100% | đạt |
| 1 | `run-2@20261128-040127` | gpt-6-luna | Bộ 30 câu · agent tự chọn bước (`agent_loop.py`) | 29/30 | 97% | chưa (B29 `khong_bia_so_lieu`) |
| (giữa) | `run-3@20261128-040507` | gpt-6-luna | + `tra_gia`, kiểm số tiền trong lời model, ép quán đứng đầu khi "rẻ / gần nhất" | 29/30 | 97% | chưa (B26 `dung_rang_buoc_cung`) |
| 2 | `run-4@20261128-040930` | gpt-6-luna | + sắp theo "đúng món" trước rồi mới rẻ / gần | 30/30 | 100% | đạt |
| Đối chiếu model | `run-5@20261128-093233` | gpt-6.1-terra | Cùng bộ 30 câu và cùng luật chấm code với Luna `run-4` | 30/30 | 100% | đạt theo code |

So sánh trước và sau cải tiến dùng hai lượt Luna `run-2` → `run-4` (**29/30 → 30/30**). `run-1` giữ làm mốc lịch sử trên bộ 20 câu. `run-5` dùng để đối chiếu Luna với Terra và tính chi phí Terra theo tỉ lệ đạt của chính Terra. [Báo cáo đánh giá](report.md) · [CSV Terra](run-5.csv) · [Báo cáo chi phí](../cost/cost-estimate.md)

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Nhóm lỗi lớn nhất: câu có đáp án khách quan trong data (giá bao nhiêu, rẻ nhất, gần nhất) nhưng để model tự quyết → đoán sai khoảng giá (B29), đảo thứ tự "rẻ / gần nhất" (B23, B27).
Đã sửa: công cụ `tra_gia`, code kiểm mọi số tiền trong lời model, code bắt thứ tự đúng tiêu chí (đúng món đứng trước). Lần sửa đầu làm tệ B26, đã sửa tiếp.
Còn lại: kết quả dao động giữa các lần chạy; hội thoại nhiều lượt chưa có trong bộ câu thử; `khop_so_thich` chưa có người xác nhận. Chi tiết: `eval/report.md`.
