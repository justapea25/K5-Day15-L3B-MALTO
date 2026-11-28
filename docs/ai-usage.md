# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/agent.py`, `agent_loop.py`, `tools.py` bản đầu, `web.py`, giao diện `web/` theo thiết kế nhóm chốt | Chạy thử từng thay đổi bằng bộ câu thử + 30 câu thực tế trong `playground/`, duyệt diff trước khi commit | Minh |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn prompt agent, mô tả công cụ, luật code chặn (kiểm phương án, kiểm số tiền) | Chỉnh theo câu trượt ở từng lượt (ghi ở `spec.md` §10, `eval/report.md`) | Minh |
| Rà câu hỏi phỏng vấn / khảo sát | ChatGPT | Hỗ trợ xây dựng cấu trúc Google Form; gợi ý và diễn đạt lại câu hỏi demographic, hành vi đặt đồ ăn, các phát biểu Likert 1–5, câu hỏi mở và câu hỏi phỏng vấn sâu | Linh lựa chọn, chỉnh sửa và duyệt câu hỏi theo mục tiêu nghiên cứu; kiểm tra câu chữ trung lập, dễ hiểu và đối chiếu với Google Form cuối cùng. AI không tạo người tham gia, câu trả lời khảo sát hay trích dẫn phỏng vấn | Linh |
| Đào data (viết script đếm, gợi ý nhãn) | ⚠️ CẦN ĐIỀN (Thu) | ⚠️ CẦN ĐIỀN | Kiểm tay ⚠️ __ dòng, khớp ⚠️ __ | Thu |
| Viết câu thử (benchmark) | Claude Code | Soạn B16–B20 (ghi `tu_viet`); viết luật chấm từng câu trong `eval/grade.py`; kiểm `expected` của B21–B30 với data (sửa B26 / B28 / B30 cho khớp data **trước** khi chạy) | Mỗi câu thử có `source`; B21–B30 là câu hỏi người dùng (`nguoi_dung`), không do AI viết | Thế Anh (bộ câu thử), Minh |
| Sinh data `synthetic` (nếu có) | Claude Code | Viết `scripts/gen_synthetic.py` sinh 60 quán / 1.142 món theo phân bố đo từ data GrabFood crawl (giá, khoảng cách, đánh giá, tỉ lệ món có mô tả) | Seed 42 · xem lại danh sách quán trên giao diện `/quan`, bỏ quán trùng kiểu | Minh (script), Thu (DATA_CARD) |
| Chấm cột `pass` bằng LLM (nếu có) | gpt-6-luna (`eval/judge.py`) | Chỉ đề xuất `khop_so_thich`; 3 metric còn lại chấm bằng code `eval/grade.py` | Kiểm tra thủ công ⚠️ CẦN ĐIỀN — phiếu chấm ở [eval/human-check.md](../eval/human-check.md) | Minh / Thế Anh |
| Slide, văn bản | ChatGPT hỗ trợ script và slideboard; Claude Code hỗ trợ trang Chi phí và Kết luận | ChatGPT hỗ trợ xây dựng cấu trúc slideboard, viết và chỉnh sửa kịch bản pitching 5 phút, câu chuyển giữa các phần và mô tả cách showcase tính năng MealMate. Claude Code dựng trang Chi phí / Kết luận từ số trong `cost/cost-estimate.md`, `eval/report.md` | Linh lựa chọn, chỉnh sửa nội dung và kiểm tra tính năng được mô tả có đúng với sản phẩm thực tế; đối chiếu số liệu với các file bằng chứng và evaluation. Minh kiểm tra số liệu chi phí và kết quả kỹ thuật, soát số khớp file nguồn | Linh, Minh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
