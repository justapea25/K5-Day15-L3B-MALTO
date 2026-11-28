# Người dùng thử *(bonus)*

> Điền ở guide bước 4.3 — 2–3 người ngoài nhóm, ~10 phút / người, theo 5 nhịp: làm quen · bối cảnh · giao việc · quan sát · hỏi sau. Ôn lại: ngày 5, ngày 13. Chấm ở rubric Bonus.
> Không ghi tên: ghi vai. Hành vi quan sát được nặng hơn lời nói; toàn lời khen = phiên chưa đạt, giao việc khó hơn.
> Người dùng thử **không thay được** bằng chứng pain ở `evidence/`.


| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| Người ngoài nhóm, người đặt đồ ăn · tình huống: nhóm bạn ở lại làm bài lúc 7h tối | Chọn quán và món cho 3 người: 1 chay, 1 bún/phở, 1 cơm; ~60k/người, trong 1 km; hỏi giờ mở | **Tin 1:** đúng. Ông Ngoại 0,4 km, mở đến 21:30, 3 món × 60k = 180k, món chay `chay=true`, bún đậu mắm tôm (loại bún), cơm gà xối mỡ; khớp data. **Tin 2:** giờ mở đúng (21:30) nhưng **thẻ kết quả tự đổi**: suất của người bún/phở từ *Bún đậu mắm tôm đặc biệt* thành *Bún chay nấm đặc biệt* dù không ai yêu cầu đổi; nhãn người đổi thành "Bún hoặc phở", "Cơm", và người chay bị gắn thêm "muốn cơm" chưa ai nói. Chưa thử tin 3 (xem quán khác) · Bot trả lời: "Suất bún là bún chay nấm, gần với yêu cầu bún/phở." *(bot, tin 2)* | "Trong nhóm học, có người ăn chay, người thì thèm phở, đứa thì thích ăn cơm, muốn đặt chung quán cho đỡ phí ship." | **Thấp** (món mới vẫn đúng loại bún, giá 60k, các ràng buộc vẫn được giữ; điểm có thể làm mượt thêm là giữ nguyên đơn đã gợi ý và không thêm nhãn người dùng chưa nói); tin 1 đạt |
| Người ngoài nhóm, người đặt đồ ăn · tình huống: người ăn tối một mình, thèm bún chả | Chọn quán bún chả dưới 70k, gần; hỏi quán rẻ hơn | **Tin 1:** quán và giá đúng data: Ông Ngoại 0,4 km Bún chả đặc biệt 65k, Bếp Cô Thu 60k; nêu đúng Mẹ Mít gần nhất nhưng bún chả 75k vượt ngân sách. Lời mở đầu rối vì nhắc "bún đậu mắm tôm" khi người dùng chỉ hỏi bún chả. **Tin 2 ("rẻ hơn"):** đưa quán bánh cuốn Bếp Nhà Bông 53k (đúng data), nhưng **cách 4,8 km** trong khi người dùng nói "gần gần"; bot có nói "xa hơn", đồng thời liệt kê Bếp Cô Thu 60k (0,4 km) và Chú Hải 60k (1,2 km), cả hai đều rẻ hơn 65k · Bot trả lời: "Gần nhất là Món Nhà Làm Mẹ Mít, nhưng bún chả ở đó vượt ngân sách; món hợp mức bạn đặt là bún đậu mắm tôm." *(bot, tin 1)* | "Thích ăn bún chả, muốn tìm quán bún quanh đây, oke." | **Thấp** (quán 4,8 km đúng giá và đúng loại, bot đã báo "xa hơn" và liệt kê quán gần ở dưới; có thể ưu tiên quán gần hơn khi người dùng nói "gần gần"); **thấp** (có thể bỏ câu mở đầu nhắc món chưa được hỏi cho gọn hơn) |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → __ / __ / __ *(chưa hỏi người thử câu này)*

## Tổng hợp

*(Từ 2 phiên ghi ở trên.)*

- Chủ đề lặp nhiều nhất: **tin đầu đúng, từ tin thứ hai bot dựng lại đơn hơi khác.** Phiên 1: món của một người tự đổi và nhãn gắn thêm sở thích chưa ai nói. Phiên 2: xếp quán xa lên hạng 1 khi hỏi "rẻ hơn".
- Đề xuất sửa (chưa làm, ghi ở `spec.md` §10 / `eval/report.md` §4): (1) giữ nguyên món đã gợi ý khi người dùng chỉ hỏi thêm giờ mở; (2) không gắn sở thích người dùng chưa nói ("muốn cơm"); (3) khi người dùng nói "gần", ưu tiên quán gần khi so giá; (4) bỏ câu mở đầu nhắc món không liên quan.
- Giữ gì và vì sao: tin 1 cả hai phiên đúng tên quán, món, giá, km và tổng tiền theo data; bot nói rõ khi bún chả Mẹ Mít vượt ngân sách và khi chọn quán "xa hơn".
- Để dành sau: tin 3 "xem thêm quán khác" ở tình huống 1 chưa thử; nhãn món nước.
