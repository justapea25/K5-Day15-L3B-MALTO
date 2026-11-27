# Tổng hợp bằng chứng pain

> Nguồn: Đào dữ liệu công khai GrabFood, khảo sát Google Forms, phỏng vấn người dùng và audit trực tiếp ứng dụng.
> Tổng hợp bằng chứng ban đầu cho MALTO – Track D.

## 1. Nguồn đã dùng

| Nguồn | Trạng thái | File |
|---|---|---|
| Đào data | Đã thực hiện: 258 nhà hàng, 11.322 món; có cách đếm, script và ví dụ cụ thể. Dữ liệu gốc lưu ngoài repo nên cần cung cấp nếu muốn chạy lại độc lập. | `evidence/data-mining.md` |
| Phỏng vấn | Đã thực hiện 3 cuộc. P1 đúng vai người đặt đồ ăn nhóm; P2 là người đặt cá nhân; P3 thường đi ăn ngoài cùng bạn bè. Chưa đủ 3 người đúng persona chính. | `evidence/interviews/P1.md`… |
| Khảo sát | 39 người ngoài nhóm, trong đó 36 người xác nhận sử dụng ứng dụng giao đồ ăn trong 30 ngày gần đây. Chưa sàng lọc trực tiếp vai trò người đứng ra chọn quán cho nhóm. | `evidence/survey/` |
| Audit sản phẩm | Đã audit trực tiếp GrabFood qua các luồng tìm kiếm nhà hàng, voucher, giỏ hàng và tính tổng thanh toán. | Ghi chép audit của nhóm |

**Lưu ý:** Audit sản phẩm là nguồn đối chiếu về chức năng hiện tại của ứng dụng, không thay thế bằng chứng về trải nghiệm thực tế của người dùng.

## 2. Số chính

### 2.1. Đào dữ liệu GrabFood

Nguồn: Các trang nhà hàng và thực đơn công khai trên GrabFood, khu vực Vinhomes Ocean Park, Gia Lâm, Hà Nội. Thời điểm crawl: 27/11/2026, khoảng 08:40.

| Chỉ số | Kết quả | Ý nghĩa |
|---|---:|---|
| Nhà hàng được thu thập | 258 | Quy mô dữ liệu |
| Món ăn được thu thập | 11.322 | Khối lượng dữ liệu thực đơn |
| Nhà hàng thuộc nhóm đồ ăn | 184 | Phạm vi phân tích pain chính |
| Số món tại các quán đồ ăn | 7.608 | Khối lượng thông tin cần xem xét |
| Số món trung vị mỗi menu | 33 | Thực đơn tương đối dài |
| Số món trung bình mỗi menu | 41 | Khối lượng lựa chọn trung bình |
| Menu dài nhất | 200 món | Trường hợp có nhiều lựa chọn |
| Quán có từ 30 món trở lên | 101/184 (55%) | Hơn một nửa số quán có menu dài |
| Quán có từ 50 món trở lên | 58/184 (32%) | Gần một phần ba số quán có menu rất dài |

**Phần phụ – thông tin thực đơn:**

| Chỉ số | Kết quả |
|---|---:|
| Món không có mô tả | 4.589/11.322 (40,5%) |
| Mô tả có chứa từ khóa "dị ứng" | 0/11.322 (0%) |
| Quán có ít nhất một món ghi chữ "chay" | 19/258 (7,4%) |

Các số liệu trên cho thấy thực đơn có lượng thông tin tương đối lớn và một phần món ăn thiếu mô tả. Tuy nhiên, chúng chỉ phản ánh đặc điểm dữ liệu công khai, chưa trực tiếp chứng minh người dùng gặp khó khăn khi chọn quán.

Chi tiết phương pháp, script và ví dụ: `evidence/data-mining.md`.

### 2.2. Khảo sát người dùng

- Tổng số phản hồi: 39.
- Số người ngoài nhóm dự án: 39.
- Số người sử dụng ít nhất một ứng dụng giao đồ ăn trong 30 ngày gần đây: 36.
- Số người đặt đồ ăn cho nhóm từ 3 người trở lên ít nhất 1–3 lần/tháng: 16/39.
- Số người chọn tần suất đặt nhóm ít hơn 1 lần/tháng: 23/39.

**Demographics:**

- 37/39 người (94,9%) thuộc nhóm tuổi 18–27.
- 35/39 người (89,7%) là nam.
- 30/39 người (76,9%) là học sinh/sinh viên.
- 31/39 người (79,5%) sinh sống tại Hà Nội.

**Ứng dụng được sử dụng trong 30 ngày gần đây:**

- ShopeeFood: 27/39 (69,2%).
- GrabFood: 17/39 (43,6%).
- beFood: 6/39 (15,4%).
- Green SM: 5/39 (12,8%).

*Câu hỏi cho phép chọn nhiều ứng dụng nên tổng tỷ lệ có thể vượt 100%.*

**Các phát hiện Likert nổi bật:**

Tỷ lệ đồng ý được tính bằng số người chọn mức 4 hoặc 5 trên thang Likert 5 mức. Mẫu số là 39 người cho từng phát biểu.

**A. Tìm kiếm và so sánh nhà hàng**

| Phát biểu | Điểm trung bình | Đồng ý |
|---|---:|---:|
| Mất nhiều thời gian chọn nhà hàng phù hợp | 3,82 | 25/39 (64,1%) |
| Phải mở nhiều nhà hàng để so sánh | 3,69 | 23/39 (59,0%) |
| Khó so sánh tổng chi phí giữa các nhà hàng | 3,59 | 22/39 (56,4%) |
| Khó đánh giá chất lượng giữa các quán có mức giá khác nhau | 3,77 | 25/39 (64,1%) |
| Khó tìm một nhà hàng có đủ các món mong muốn | 3,59 | 21/39 (53,8%) |

**B. Chất lượng nhà hàng**

| Phát biểu | Điểm trung bình | Đồng ý |
|---|---:|---:|
| Thường xem đánh giá trước khi đặt món | 3,95 | 25/39 (64,1%) |
| Khó so sánh chất lượng giữa nhiều nhà hàng | 3,69 | 24/39 (61,5%) |
| Quan tâm chất lượng hơn mức giảm giá | 3,21 | 12/39 (30,8%) |
| Sẵn sàng trả thêm cho chất lượng tốt hơn | 3,49 | 22/39 (56,4%) |
| Muốn nhà hàng có ưu đãi tốt và chất lượng đáng tin cậy | 4,28 | 31/39 (79,5%) |

**C. Voucher và khuyến mãi**

| Phát biểu | Điểm trung bình | Đồng ý |
|---|---:|---:|
| Thường sử dụng voucher | 4,41 | 32/39 (82,1%) |
| Mất thời gian chọn voucher có lợi nhất | 3,54 | 21/39 (53,8%) |
| Khó biết voucher nào có thể kết hợp | 3,36 | 17/39 (43,6%) |
| Từng bỏ lỡ ưu đãi tốt hơn do không biết cách kết hợp | 3,67 | 20/39 (51,3%) |
| Muốn ứng dụng tự tìm tổ hợp voucher tốt nhất | 3,72 | 25/39 (64,1%) |

**D. Tối ưu giỏ hàng**

| Phát biểu | Điểm trung bình | Đồng ý |
|---|---:|---:|
| Từng thêm món để đạt ngưỡng voucher | 3,69 | 24/39 (61,5%) |
| Khó xác định có nên thêm món để nhận ưu đãi | 3,54 | 19/39 (48,7%) |
| Muốn biết còn thiếu bao nhiêu tiền để đạt ngưỡng voucher | 3,79 | 22/39 (56,4%) |
| Muốn được gợi ý món phù hợp để tận dụng ưu đãi | 3,90 | 26/39 (66,7%) |

**Insight từ khảo sát:**

- Người dùng có dấu hiệu mất thời gian trong quá trình tìm kiếm và so sánh nhà hàng.
- Người dùng quan tâm đến cả chất lượng và ưu đãi, thay vì chỉ ưu tiên giá rẻ nhất.
- Hành vi sử dụng voucher khá phổ biến.
- Có nhu cầu được hỗ trợ tìm tổ hợp voucher và gợi ý món bổ sung để tận dụng ngưỡng ưu đãi.

**Giới hạn:** Khảo sát chưa hỏi trực tiếp người trả lời có phải người đứng ra chọn quán cho nhóm hay không. Vì vậy, không thể coi toàn bộ 39 người là persona chính của MALTO. Ngoài ra, câu hỏi tần suất đặt nhóm không có lựa chọn "chưa từng".

### 2.3. Phỏng vấn người dùng

Nhóm đã thực hiện 3 cuộc phỏng vấn.

| | Vai | Gặp pain? | Số lần/tháng | Thời gian lần gần nhất | Cách xoay xở |
|---|---|---|---:|---:|---|
| P1 | Người trực tiếp đặt đồ ăn cho nhóm | Một phần | Khoảng 4 | 15 phút | Trao đổi trong nhóm và dùng ShopeeFood |
| P2 | Người đặt đồ ăn cá nhân | Có, về so sánh nhà hàng | Chưa hỏi | 15 phút | Mở 4 quán, so sánh menu, khoảng cách và voucher |
| P3 | Người thường đi ăn ngoài cùng bạn bè | Chưa xác nhận pain đặt online | Không đặt online trong 6 tháng gần nhất | Chưa ghi nhận | Chọn quán quen, tìm TikTok và trao đổi nhóm chat |

**Phát hiện từ P1:**

- Lần gần nhất đứng ra đặt đồ ăn cho các thành viên trước buổi họp mentor duty.
- Mất khoảng 15 phút từ lúc chốt món, tìm quán đến thao tác đặt hàng.
- Các thành viên trao đổi và thống nhất khá nhanh.
- Không có ai phải nhường món hoặc ăn tạm.
- Tần suất đặt khoảng 4 lần/tháng.

P1 xác nhận có công sức trong quá trình đặt đồ ăn nhóm, nhưng chưa xác nhận sự khác biệt sở thích là pain nghiêm trọng.

**Phát hiện từ P2:**

- Lần gần nhất mất khoảng 15 phút để lựa chọn nhà hàng.
- Phải mở 4 quán để kiểm tra menu, giá, khoảng cách và voucher.
- Phải quay lại các nhà hàng nhiều lần và đôi khi quên giá đã xem.
- Khó xác định tổng bill sau ưu đãi, phí giao hàng và thời gian giao.
- Từng thêm topping trị giá 8.000đ để đạt ngưỡng voucher. Tổng tiền giảm từ 63.000đ xuống 61.000đ sau khi đổi voucher.

P2 cung cấp ví dụ cụ thể về khó khăn khi so sánh nhà hàng và tự tối ưu giỏ hàng, nhưng thuộc phân khúc đặt đồ ăn cá nhân.

**Phát hiện từ P3:**

- Ít sử dụng ứng dụng giao đồ ăn, lần gần nhất khoảng 6 tháng trước.
- Thường chọn quán quen.
- Khi ở khu vực lạ, tìm quán trên TikTok rồi gửi vào nhóm chat để mọi người cùng xem.
- Đôi khi có khác biệt về sở thích món ăn nhưng không xảy ra mâu thuẫn nghiêm trọng.
- Nếu quán không đáp ứng kỳ vọng, nhóm thường không quay lại.

P3 là nguồn tham khảo về hành vi lựa chọn quán khi đi ăn ngoài cùng bạn bè, không phải người dùng đặt đồ ăn online thường xuyên.

**Kết luận phỏng vấn:** Chưa đủ cơ sở để kết luận người đứng ra chọn quán cho nhóm thường xuyên gặp khó khăn vì mỗi thành viên có sở thích khác nhau. Cần phỏng vấn thêm người đúng persona chính.

### 2.4. Audit ứng dụng GrabFood

Các phát hiện chính từ quá trình audit:

- Người dùng phải mở từng nhà hàng để xem chi tiết menu, giá và ưu đãi.
- Không có chức năng so sánh trực tiếp tổng chi phí cuối cùng giữa nhiều nhà hàng.
- Ứng dụng không tự xếp hạng nhà hàng tiết kiệm nhất sau voucher và phí.
- Không phải voucher nào cũng có thể kết hợp; voucher không tương thích bị làm mờ/khóa mà không giải thích lý do.
- Khi tăng giá trị giỏ hàng, voucher chưa đủ điều kiện có thể tự mở khóa, nhưng ứng dụng không thông báo số tiền còn thiếu.
- Không tự gợi ý món nên thêm để tận dụng ưu đãi.
- Rating và review có thể xem ở từng nhà hàng nhưng chưa thuận tiện khi so sánh nhiều quán cùng lúc.

Đây là kết quả quan sát các luồng đã được nhóm kiểm tra, không khẳng định mọi tình huống sử dụng GrabFood đều giống nhau.

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Nhiều khi lướt Grab search quán mà mất tận 30 phút-1 tiếng vì đau đầu không chốt được quán ăn" — Phiếu khảo sát R004. Chủ đề: mất thời gian lựa chọn nhà hàng.

2. "mất khá nhiều thời gian từ chốt món ăn đến tìm quán rồi thao tác đặt online có thể là mất 15 phút" — Phỏng vấn P1. Chủ đề: thời gian lựa chọn và đặt đồ ăn nhóm. Người tham gia đã đồng ý cho trích dẫn ẩn danh.

3. "Chủ yếu là voucher nhiều khi show như thật nhưng mà đến lúc áp vào thì lại không áp được lại thông báo là không đủ điều kiện" — Phiếu khảo sát R002. Chủ đề: điều kiện sử dụng voucher chưa rõ ràng.

4. "Nhà hàng đóng cửa trước nhưng trên shopee food vẫn hiện voucher và tôi đã mua nhưng không dùng được" — Phiếu khảo sát R018. Chủ đề: thông tin khả dụng của nhà hàng và ưu đãi.

5. "Tôi đề nghị thà tự đi mua về ăn còn hơn" — Phiếu khảo sát R033. Chủ đề: trải nghiệm đặt đồ ăn không đáp ứng kỳ vọng; chưa rõ nguyên nhân cụ thể.

6. "cập nhật giá món / giá ship theo các mốc thời gian nhưng tôi không biết cụ thể. Suggest các bạn có thêm mục alert là từ mấy giờ thì giá ship có thể tăng/giảm để thêm tính tỉ mỉ cho sản phẩm (thể hiện sự quan tâm đến khách hàng)" — Phiếu khảo sát R035. Chủ đề: minh bạch thông tin giá và phí giao hàng.

Các phản hồi R002, R004, R018, R033 và R035 được giữ nguyên nội dung từ câu hỏi mở trong Google Forms, đã loại bỏ thông tin nhận dạng cá nhân. Không sử dụng lời nói nguyên văn của P2 và P3 khi chưa xác nhận quyền trích dẫn.

## 4. Các nguồn có khớp nhau không?

**Data nói:** Trong 184 nhà hàng đồ ăn được crawl trên GrabFood, số món trung vị mỗi menu là 33; 101/184 nhà hàng (55%) có từ 30 món trở lên. Ngoài ra, 40,5% món trong toàn bộ dữ liệu không có mô tả. Điều này cho thấy người dùng phải đối mặt với lượng thông tin thực đơn tương đối lớn và một số món thiếu thông tin để đánh giá.

**Khảo sát nói:** 64,1% người tham gia mất nhiều thời gian chọn nhà hàng; 59% thường phải mở nhiều nhà hàng để so sánh; 56,4% gặp khó khăn khi so sánh tổng chi phí. Có 53,8% đồng ý rằng họ khó tìm một nhà hàng có đủ các món mình muốn ăn trong cùng một đơn hàng. Tuy nhiên, phát biểu này không xác định rõ bối cảnh đặt nhóm.

**Phỏng vấn nói:** P2 mất khoảng 15 phút, mở 4 nhà hàng để so sánh menu, khoảng cách và voucher. Điều này phù hợp với khó khăn tìm kiếm và so sánh được ghi nhận trong khảo sát. P1 cũng mất khoảng 15 phút cho toàn bộ quá trình đặt đồ ăn nhóm, nhưng các thành viên thống nhất khá nhanh và lần đặt gần nhất diễn ra suôn sẻ. P3 thường chọn quán quen hoặc tìm trên TikTok và trao đổi trong nhóm chat, chưa ghi nhận khó khăn nghiêm trọng.

**Audit GrabFood ghi nhận:** Người dùng phải mở từng nhà hàng để kiểm tra thông tin chi tiết, không thể so sánh trực tiếp tổng chi phí cuối cùng giữa nhiều quán. Ứng dụng cũng chưa tự lựa chọn tổ hợp voucher tiết kiệm nhất hoặc gợi ý món nên thêm để đạt ngưỡng ưu đãi.

**Mức độ đối chiếu:**

- **Restaurant Discovery:** Khớp một phần. Dữ liệu cho thấy menu có nhiều món; khảo sát và P2 ghi nhận khó khăn khi tìm kiếm, mở nhiều quán và so sánh thông tin.
- **Group Preference Matching:** Chưa được xác nhận rõ. P1 cho biết các thành viên thống nhất khá nhanh; P3 cũng không gặp mâu thuẫn nghiêm trọng khi đi ăn cùng bạn bè.
- **Information Completeness:** Khớp một phần. 40,5% món không có mô tả cho thấy hạn chế của dữ liệu menu, nhưng chưa chứng minh người dùng đã gặp vấn đề cụ thể vì thiếu mô tả.
- **Price and Promotion Comparison:** Khớp rõ ở bối cảnh đặt đồ ăn nói chung. Khảo sát ghi nhận khó so sánh tổng chi phí; P2 phải tự so sánh giá và voucher; audit cũng cho thấy người dùng phải tự tổng hợp thông tin giữa các nhà hàng.
- **Smart Cart:** Có tín hiệu hỗ trợ từ khảo sát và trải nghiệm P2. Tuy nhiên, đây là pain liên quan đến tối ưu voucher khi đặt cá nhân, chưa phải bằng chứng trực tiếp cho bài toán phối hợp nhu cầu nhóm.

**Kết luận đối chiếu:** Các nguồn cùng chỉ ra rằng quá trình tìm kiếm và so sánh thông tin nhà hàng có thể đòi hỏi nhiều thao tác thủ công. Tuy nhiên, bằng chứng hiện tại chưa đủ mạnh để khẳng định việc mỗi thành viên có sở thích khác nhau là nguyên nhân chính khiến người tổ chức đặt đồ ăn nhóm gặp khó khăn.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **Phải điều chỉnh và tiếp tục kiểm chứng.**

**Những nội dung được ủng hộ:**

- Người dùng có dấu hiệu mất thời gian khi tìm kiếm và so sánh nhiều nhà hàng.
- Thực đơn của nhiều nhà hàng có số lượng món lớn, trong khi một phần món ăn thiếu mô tả.
- Người dùng phải tự mở nhiều nhà hàng để kiểm tra menu, giá cả, khoảng cách và ưu đãi.
- P2 cung cấp ví dụ cụ thể về việc phải so sánh 4 nhà hàng và tự tính toán khi thêm món để tận dụng voucher.
- Audit GrabFood xác nhận một số bước so sánh và tính toán vẫn phải do người dùng tự thực hiện.

**Những nội dung chưa được xác nhận:**

- Việc mỗi thành viên có sở thích khác nhau có thường xuyên khiến người tổ chức không tìm được nhà hàng phù hợp hay không.
- Người đặt đồ ăn nhóm có thực sự mất nhiều thời gian hơn người đặt cá nhân hay không.
- Có thành viên nào thường phải nhường hoặc ăn món không phù hợp vì không tìm được nhà hàng đáp ứng cả nhóm hay không.
- Việc chọn một nhà hàng duy nhất cho cả nhóm có thực sự là cách giải quyết phù hợp nhất trong mọi tình huống hay không.

P1 và P3 cho thấy việc thống nhất lựa chọn trong nhóm có thể diễn ra khá dễ dàng trong một số tình huống. Vì vậy, không nên mặc định mọi đơn hàng nhóm đều gặp vấn đề về sở thích khác nhau.

**Điều vẫn chưa biết:**

- Tần suất thực tế của các tình huống mỗi thành viên muốn ăn một món khác nhau.
- Người trực tiếp tổ chức đặt đồ ăn nhóm thường xử lý các yêu cầu khác nhau như thế nào.
- Mức thời gian và công sức họ phải bỏ ra để tìm một nhà hàng phù hợp với cả nhóm.
- Việc đề xuất một nhà hàng và một món cho từng thành viên có thực sự giúp họ ra quyết định nhanh hơn hay không.

**Hướng kiểm chứng tiếp theo:**

Nhóm cần phỏng vấn thêm ít nhất hai người thường xuyên đứng ra chọn quán hoặc đặt đồ ăn cho nhóm từ 3 người trở lên. Tập trung vào một tình huống cụ thể trong tháng gần nhất, cách họ tổng hợp yêu cầu của các thành viên, số nhà hàng đã xem, thời gian ra quyết định và những khó khăn thực tế phát sinh.

## Lịch hẹn (dùng cho CP2 – chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Người trực tiếp đặt đồ ăn cho nhóm từ 3 người trở lên (P1) | 17h30 27/11 | Có |
| Người đặt đồ ăn cá nhân qua ứng dụng (P2) | 17h45 27/11 | Có |
| Người thường đi ăn ngoài cùng bạn bè (P3) | 18h 27/11 | Có |