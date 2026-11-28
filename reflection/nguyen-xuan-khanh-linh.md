## Reflection — Nguyễn Xuân Khánh Linh

### Thành viên nhóm MALTO · L3B · Track D.

1. Vai trò + phần mình làm (trỏ tới file / commit):

Mình phụ trách Product Research và Product Planning của nhóm. Công việc chính gồm xây dựng Google Form, rà soát câu hỏi khảo sát, tổng hợp kết quả của 39 người tham gia và các phát hiện từ phỏng vấn vào evidence/summary.md. Mình cũng tham gia phân tích pain, lựa chọn persona, so sánh các hướng sản phẩm và xây dựng Impact trong spec.md §1–§2. Ngoài ra, mình phụ trách nội dung thuyết trình, slide và chuẩn bị hoạt động kiểm thử người dùng trong validation/. Qua quá trình làm việc, mình hiểu rõ hơn vai trò Product không chỉ là nghĩ ra tính năng, mà còn phải đảm bảo mỗi quyết định sản phẩm có bằng chứng và lý do rõ ràng.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

Mình sử dụng ChatGPT để hỗ trợ xây dựng và diễn đạt câu hỏi khảo sát, câu hỏi Likert, câu hỏi phỏng vấn sâu, tổng hợp insight và xây dựng kịch bản thuyết trình. AI giúp tiết kiệm thời gian soạn thảo và hệ thống hóa thông tin, nhưng mình vẫn phải kiểm tra lại để đảm bảo câu hỏi không dẫn dắt người trả lời và nội dung phản ánh đúng dữ liệu thực tế. Một điểm mình phải điều chỉnh là cách diễn giải kết quả 21/39 người gặp khó khăn khi tìm nhà hàng có đủ món: đây là tín hiệu chung, chưa đủ để kết luận riêng về persona đặt cá nhân nhiều món vì khảo sát chưa phân biệt hai nhóm. Mình cũng không sử dụng AI để tạo câu trả lời khảo sát, người phỏng vấn hoặc trích dẫn giả.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

Mình chọn B29 trong eval/run-2.csv. Người dùng hỏi giá trung bình của phở và bún bò, nhưng bot tự đưa ra khoảng giá không chính xác và còn nhầm món bún chay với bún bò. Trong dữ liệu, phở có giá từ 65.000–95.000đ và bún bò từ 51.000–85.000đ. Sau đó, nhóm bổ sung công cụ tra_gia và cơ chế kiểm tra các con số do AI đưa ra bằng code; B29 đã vượt qua ở run-4. Từ trường hợp này, mình học được rằng một câu trả lời nghe hợp lý chưa chắc đã đúng. Với vai trò Product, mình cần xác định rõ thông tin nào phải có căn cứ từ dữ liệu, đặc biệt là giá cả và tên món, đồng thời đưa những yêu cầu đó thành tiêu chí đánh giá cụ thể thay vì chỉ tập trung vào trải nghiệm hội thoại.