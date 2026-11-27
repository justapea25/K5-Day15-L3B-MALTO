# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/agent.py`, `agent_loop.py`, `tools.py` bản đầu, `web.py`, giao diện `web/` theo thiết kế nhóm chốt | Chạy thử từng thay đổi bằng bộ câu thử + 30 câu thực tế trong `playground/`, duyệt diff trước khi commit | Minh |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn prompt agent, mô tả công cụ, luật code chặn (kiểm phương án, kiểm số tiền) | Chỉnh theo câu trượt ở từng lượt (ghi ở `spec.md` §10, `eval/report.md`) | Minh |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | gpt-6-luna (`eval/judge.py`) | Chỉ đề xuất `khop_so_thich`; 3 metric còn lại chấm bằng code `eval/grade.py` | Kiểm tra thủ công __ câu thử, khớp __/__ *(chưa làm)* | Minh / Thế Anh |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
