# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/agent.py`, `agent_loop.py`, `tools.py` bản đầu, `web.py`, giao diện `web/` theo thiết kế nhóm chốt | Chạy thử từng thay đổi bằng bộ câu thử + 30 câu thực tế trong `playground/`, duyệt diff trước khi commit | Minh |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn prompt agent, mô tả công cụ, luật code chặn (kiểm phương án, kiểm số tiền) | Chỉnh theo câu trượt ở từng lượt (ghi ở `spec.md` §10, `eval/report.md`) | Minh |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Viết script đếm `evidence/count.py`, `evidence/count_menu.py`, gợi ý từ khoá nhãn | Thu đọc và kiểm lại kết quả đếm trên 60 quán / 1.142 món, xác nhận khớp (28/11) | Thu |
| Rà câu hỏi phỏng vấn / khảo sát | ⚠️ CẦN ĐIỀN (Linh) | Chỉ rà câu dẫn dắt | ⚠️ CẦN ĐIỀN | Linh |
| Viết câu thử (benchmark) | Claude Code | Soạn B16–B20 (ghi `tu_viet`); viết luật chấm từng câu trong `eval/grade.py`; kiểm `expected` của B21–B30 với data (sửa B26 / B28 / B30 cho khớp data **trước** khi chạy) | Mỗi câu thử có `source`; B21–B30 là câu hỏi người dùng (`nguoi_dung`), không do AI viết | Thế Anh (bộ câu thử), Minh |
| Sinh data `synthetic` (nếu có) | Claude Code | Viết `scripts/gen_synthetic.py` sinh 60 quán / 1.142 món theo phân bố đo từ data GrabFood crawl (giá, khoảng cách, đánh giá, tỉ lệ món có mô tả) | Seed 42 · xem lại danh sách quán trên giao diện `/quan`, bỏ quán trùng kiểu | Minh (script), Thu (DATA_CARD) |
| Chấm cột `pass` bằng LLM (nếu có) | gpt-6-luna (`eval/judge.py`) | Chỉ đề xuất `khop_so_thich`; 3 metric còn lại chấm bằng code `eval/grade.py` Kiểm tra thủ công 5 câu, khớp 5/5 — phiếu chấm ở [eval/human-check.md](../eval/human-check.md) | Minh / Thế Anh |
| Slide, văn bản | ⚠️ CẦN ĐIỀN (Linh) — slide chính · Claude Code thêm trang "Chi phí" và "Kết luận" | Trang chi phí / kết luận: dựng từ số trong `cost/cost-estimate.md`, `eval/report.md` | Minh soát số khớp file nguồn | Linh, Minh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
