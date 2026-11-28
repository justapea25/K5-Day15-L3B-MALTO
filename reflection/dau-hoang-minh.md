# Reflection — Đậu Hoàng Minh

> Đội trưởng nhóm MALTO · L3B · Track D. Hạn: 23:59 Thứ Bảy 28/11.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình là đội trưởng và lead code. Mình thiết kế giải pháp (`spec.md` §4–§6, §9) và viết luồng agent. Bản đầu là workflow 4 bước (`ab45b3a`). Sau lượt 1 mình đổi sang agent tự chọn bước có nhớ hội thoại (`codebase/agent_loop.py`, `787dfd2`). Mình nối model gpt-6-luna qua OpenAI Responses API (`codebase/ai.py`) và làm giao diện chat Next.js (`web/`). Mình viết `eval/grade.py` để chấm 3 metric bằng code, chạy các lượt `run-2` → `run-4`, rồi viết `eval/report.md` (`e9a568f`, `cbb0709`). Mình quay video demo, gộp nhánh của cả nhóm vào `main` và nộp form các checkpoint.
2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Mình dùng Claude Code để viết phần lớn code, script sinh data dựng giả, luật chấm và phần nháp tài liệu. Mình duyệt diff và chạy bộ câu thử trước mỗi lần commit. gpt-6-luna là model của bản chạy thử, gpt-image-2 sinh ảnh minh hoạ quán. Có mấy chỗ mình phải sửa lại output của AI:

   - Bản agent đầu "nhớ" hội thoại bằng cách ghép chuỗi, nên câu "không phải mình muốn hàu cơ mà" vẫn bị đọc thành hàu. Mình phải bắt đổi sang gửi lịch sử hội thoại thật.
   - Bot trả lời nghe như hardcode từng trường hợp, mình phải yêu cầu chuyển sang để model tự gọi công cụ.
3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   **B29** ("phở với bún bò ở đây thường giá khoảng bao nhiêu 1 tô") trượt ở `run-2`. Data có phở 65–95k, bún bò 51–85k. Bot lại trả lời "phở 65–80k, bún 60–85k", vì model tự suy ra khoảng giá từ 6 quán nó thấy, và còn coi bún chay là bún bò. Mình học được rằng câu hỏi có đáp án khách quan trong data (giá, rẻ nhất, gần nhất) thì phải để **code tính**, model chỉ diễn đạt lại. Mình thêm công cụ `tra_gia` và cho code kiểm mọi con số trong lời của model. Lần sửa đầu làm trượt câu khác: B26 ở `run-3`, khi code ép quán gần nhất lên đầu dù quán đó không có cơm tấm. Từ đó mình hiểu thêm: luật cứng nào cũng phải xếp sau "đúng món người dùng nói", và mỗi lần sửa phải chạy lại cả bộ câu thử, không chỉ thử riêng câu vừa sửa.
