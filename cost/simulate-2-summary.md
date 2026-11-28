# Tóm tắt mô phỏng simulate-2@20261128-091535

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 31 | 1 | 8442 | 431 | 2.0 | 111.4 |
| dung_vua | 17 | 2 | 15532 | 720 | 3.8 | 163.5 |
| dung_nhieu | 2 | 3 | 25993 | 1178 | 6.0 | 310.5 |

Tỉ lệ đạt dùng để tính: **chưa có** lượt eval chấm xong chạy bằng gpt-6.1-terra. Lượt chấm gần nhất (run-4@20261128-040930) chạy bằng gpt-6-luna — model khác, nên KHÔNG dùng tỉ lệ đạt đó → chưa tính chi phí / task thành công. Chạy `python run.py eval` bằng đúng model này, chấm xong (`python run.py score …`) rồi chạy lại simulate.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (300 người) | Chi phí / tháng — cao (500 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.0014 | — | — | $0.2798 | $0.8395 | $1.40 | $0.0028 |
| gpt-6.1-terra (vào 1.0 · ra 5.0 $/1M) | $0.0144 | — | — | $2.80 | $8.39 | $13.99 | $0.0280 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-6.1-terra. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
