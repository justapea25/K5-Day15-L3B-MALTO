# Tóm tắt mô phỏng simulate-1@20261128-084547

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 31 | 1 | 9226 | 478 | 2.2 | 112.0 |
| dung_vua | 17 | 2 | 19141 | 911 | 4.4 | 165.3 |
| dung_nhieu | 2 | 3 | 27240 | 1293 | 6.5 | 310.5 |

Tỉ lệ đạt dùng để tính: 30/30 (100%) — lượt run-4@20261128-040930

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-4.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (300 người) | Chi phí / tháng — cao (500 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.0017 | $0.0017 | $0.0012 | $0.3184 | $0.9552 | $1.59 | $0.0032 |
| gpt-6-sol (vào 2.0 · ra 10.0 $/1M) | $0.0332 | $0.0332 | $0.0234 | $6.37 | $19.10 | $31.84 | $0.0637 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
