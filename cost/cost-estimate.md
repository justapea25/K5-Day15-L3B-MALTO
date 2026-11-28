# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Token lấy từ lượt chạy `python run.py simulate`. Chi phí được tính từ CSV của lượt chạy và bảng giá trong `cost/personas.yaml`.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona:** nhóm ít dùng (58,97%, 0,5 phiên/tháng, 1 lượt hỏi/phiên), dùng vừa (30,77%, 2 phiên/tháng, 2 lượt hỏi/phiên) và dùng nhiều (10,26%, 4 phiên/tháng, 3 lượt hỏi/phiên). Đây là giả định thử nghiệm, tham chiếu khảo sát và phỏng vấn P1 trong [tổng hợp bằng chứng](../evidence/summary.md). Chi tiết nguồn ghi trong [personas.yaml](personas.yaml).
- **Quy mô thử nghiệm (tự ước tính):** thấp 100 · cơ sở 300 · cao 500 người dùng/tháng.
- **Giá OpenAI Standard** (USD / 1 triệu token, xem 28/11/2026): `gpt-6-luna` **$0,10 vào / $0,50 ra**, `gpt-6.1-terra` **$1,00 vào / $5,00 ra**. Mỗi model được tính giá trên token đo từ lần chạy của chính model đó. [Giá Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) · [Giá Terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra)
- **Tỉ lệ đạt dùng để tính:** Luna **30/30** ở lượt 2 `run-4@20261128-040930` và Terra **30/30** ở lượt đối chiếu `run-5@20261128-093233`. Cả hai dùng cùng 30 câu và cùng 3 metric chấm bằng code. Metric `khop_so_thich` còn chờ người chấm xác nhận. [CSV Luna](../eval/run-4.csv) · [CSV Terra](../eval/run-5.csv)

## 2. Kết quả mô phỏng

Hai lượt dùng cùng seed `42`, cùng **50 phiên và 71 lượt hỏi**. Mỗi lượt có 31 phiên nhóm ít dùng, 17 phiên nhóm dùng vừa và 2 phiên nhóm dùng nhiều. Chi phí bình quân của nhóm dùng nhiều dựa trên mẫu nhỏ.

| Model chạy qua API | Run ID | Token vào | Token ra | Lần gọi model | Phiên báo lỗi | Bằng chứng |
|---|---|---:|---:|---:|---:|---|
| `gpt-6-luna` | `simulate-1@20261128-084547` | 665.901 | 32.900 | 156 | 0/50 | [CSV](simulate-1.csv) · [Trace](../traces/simulate-1.jsonl) · [Tóm tắt](simulate-1-summary.md) |
| `gpt-6.1-terra` | `simulate-2@20261128-091535` | 577.714 | 27.965 | 139 | 0/50 | [CSV](simulate-2.csv) · [Trace](../traces/simulate-2.jsonl) · [Tóm tắt](simulate-2-summary.md) |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `gpt-6-luna` | $0.0017 | $0.0017 | $0.3184 (100 người) | $0.9552 (300 người) | $1.59 (500 người) | $0.0032 |
| `gpt-6.1-terra` | $0.0144 | $0.0144 | $2.80 (100 người) | $8.39 (300 người) | $13.99 (500 người) | $0.0280 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt đã chấm của cùng model. Tỉ lệ 30/30 của Terra được bổ sung sau khi chấm `run-5`. Mô phỏng chi phí không chấm lại 71 lượt hỏi. Chi phí tính theo giá token tiêu chuẩn và chưa áp giá cache riêng.

Mỗi bản tóm tắt có thể áp nhiều mức giá lên cùng token của một lượt. Bảng so sánh lấy chi phí theo giá Luna từ `simulate-1-summary.md` và giá Terra từ `simulate-2-summary.md`. Hai bản tóm tắt lưu trạng thái tại thời điểm chạy. Chi phí mỗi task thành công của Terra tính thêm từ `run-5` đã chấm. Terra dùng ít token hơn trong lần chạy này, nhưng chi phí tháng ở kịch bản cơ sở cao khoảng 8,8 lần do đơn giá cao hơn.

## 3. So với impact

- **Impact:** P1 dành khoảng 60 phút/tháng cho toàn bộ quy trình đặt đồ ăn nhóm. Nhóm chưa đo được MALTO tiết kiệm bao nhiêu trong số đó. [spec.md §2](../spec.md)
- **Chi phí model / người / tháng ở kịch bản cơ sở:** khoảng **$0.0032** với Luna và **$0.0280** với Terra, tính từ token đo riêng của từng model.
- **Kết luận:** Chọn Luna cho thử nghiệm quy mô nhỏ vì chi phí thấp hơn và cùng đạt 30/30 theo 3 metric chấm bằng code. Cần chấm `khop_so_thich` và đo thời gian chọn quán trước và sau khi dùng MALTO để đánh giá lợi ích.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
