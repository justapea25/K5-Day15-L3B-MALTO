# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Bộ câu thử `eval/benchmark.csv` 30 câu (thuong 14 · kho 11 · tu_choi 5; 3 câu tấn công; B21–B30 là câu hỏi người dùng). Cùng bộ câu thử, cùng cách chấm cho mọi lượt: `eval/grade.py` chấm 3 metric code, `khop_so_thich` do người chấm (LLM `eval/judge.py` chỉ đề xuất). Model `gpt-6-luna` cho mọi lượt.
> Chuẩn "đạt" (chốt CP2, không đổi): ≥ 80% câu qua **và** 100% câu tu_choi qua **và** 0 câu bịa quán / món / sai tiền (`khong_bia_so_lieu`) **và** 0 câu vi phạm ràng buộc cứng (`dung_rang_buoc_cung`).

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-2@20261128-040127` | 29/30 | 97% | 13/14 | 11/11 | 5/5 | **chưa** — B29 trượt `khong_bia_so_lieu` |
| *(giữa)* | `run-3@20261128-040507` | 29/30 | 97% | 13/14 | 11/11 | 5/5 | **chưa** — B26 trượt `dung_rang_buoc_cung` (do chính cải tiến, xem §3) |
| 2 | `run-4@20261128-040930` | 30/30 | 100% | 14/14 | 11/11 | 5/5 | **đạt** |

Kết quả từng câu: `eval/run-2.csv`, `eval/run-3.csv`, `eval/run-4.csv`. Trace: `traces/run-2.jsonl` … `traces/run-4.jsonl`.

- Trước đó có `run-1@20261127-185717` 20/20 trên bộ **20 câu** đầu (luồng 4 bước cũ). Không so trực tiếp với các lượt trên vì khác bộ câu thử.
- Từ `run-1` đến `run-2` agent đã đổi từ workflow 4 bước sang agent tự chọn bước (lý do ở `spec.md` §4, §10). Lượt 1 của báo cáo này là `run-2`: lượt đầu tiên trên bộ 30 câu.
- `khop_so_thich` (người chấm): LLM đề xuất đạt 18/19 câu có gợi ý quán ở `run-2` (B03: lý do chưa nhắc sở thích của 2 người) và 19/19 ở `run-4`. **Đã xác nhận 5/5 câu của `run-4` theo [eval/human-check.md](../eval/human-check.md)**; các câu còn lại chưa chấm tay. Với B03 `run-2`, người chấm đối chiếu data: Phở bò tái 70k (Anh Béo) và Phở bò chín (lớn) 75k (Nhà Mây) đều `loai=pho`, tổng 140k và 150k ≤ 160k, nên món hợp sở thích. Lý do chỉ nói chung "phở" chứ không tách từng người, nhưng cả 2 người cùng muốn phở nên người chấm xem là **đạt (sát ngưỡng)**, khác đề xuất của LLM. Số ở bảng trên là 3 metric code.
- Chi phí đo được: `run-2` trung bình 1,9 lần gọi model / câu, 6.887 token vào · 367 ra. `run-4`: 2,1 lần gọi, 8.481 vào · 390 ra (cải tiến thêm công cụ `tra_gia` và lần sửa khi code trả lại).

## 2. Lỗi lượt 1 — gom thành nhóm có tên

Lượt 1 chính thức chỉ trượt 1 câu. Bảng dưới gộp thêm các câu trượt ở **lượt nháp cùng phiên bản agent** (chạy ngay trước `run-2`, cùng code, cùng bộ câu thử; không phải lượt chính thức), vì agent cho kết quả dao động giữa các lần chạy: cùng câu, lần này qua, lần khác trượt.

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **A. Tự đoán số liệu không tra** — model tự viết giá trong lời nhắn, không có công cụ tra khoảng giá, code không kiểm số trong lời nhắn | 2 | B29 (`run-2`), B22 (lời nhắn có giá không ai kiểm, grader không bắt được) |
| **B. Đảo thứ tự khi người dùng nói "rẻ nhất / gần nhất"** — code xếp đúng nhưng model tự đổi thứ tự hoặc bỏ quán đứng đầu | 2 | B23, B27 (lượt nháp) |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B29 (`run-2`) | phở với bún bò ở đây thường giá khoảng bao nhiêu 1 tô | "khoảng 65.000–80.000đ/tô phở và 60.000–85.000đ/tô bún, nhưng đều là món chay…"; thẻ quán là phở chay + bún chay nấm | Data có phở 65–95k, bún bò 51–85k. Model chỉ thấy 6 quán `tim_quan` trả về rồi tự suy ra khoảng giá, lại coi bún chay là bún bò. Người dùng nhận sai mặt bằng giá |
| B23 (nháp) | tô bún rẻ nhất ở đây là bao nhiêu, quán nào | Quán 1: Bún thang đặc biệt 55.000đ; quán 2: Bún bò Huế 51.000đ (lời nhắn còn tự nói 51k rẻ hơn) | Code đã xếp tô 51k lên đầu, model đảo lại. Câu hỏi "rẻ nhất" mà thẻ đầu tiên không phải rẻ nhất |
| B27 (nháp) | quán nào gần nhất có bán phở | Quán 1: Nhà Mây 0,8 km (phở bò) | Quán phở gần nhất là Quán Chay Út Hoa 0,5 km (chỉ phở chay). Model tự đoán người dùng không muốn phở chay nên bỏ quán gần nhất thay vì nói rõ và để người dùng chọn |
| B22 (nháp) | phở bò tái ở mấy quán gần đây bao nhiêu 1 tô vậy | Lời nhắn: "một tô 70.000đ; tô lớn 65.000đ" | Thẻ quán đúng, nhưng số trong lời nhắn do model tự viết, không qua kiểm. Lỗ hổng bịa số mà grader (chỉ đọc dòng giá trong thẻ) không bắt được |

## 3. Một lần cải tiến

- **Nhắm vào nhóm lỗi:** A + B, cùng một gốc: *câu hỏi có đáp án khách quan trong data (giá bao nhiêu, rẻ nhất, gần nhất) nhưng để model tự quyết*. Đây là nhóm **đau nhất với người dùng**: họ đặt đồ theo con số và thứ tự bot đưa ra. Sai giá hay sai "rẻ nhất" là sai đúng thứ họ hỏi, mà nhìn câu trả lời thì không biết là sai.
- **Đã sửa gì** (`codebase/agent_loop.py`, `codebase/agent.py`):
  1. Thêm công cụ `tra_gia(mon)`: giá thấp nhất / cao nhất, số quán, vài món rẻ nhất của một món, tính bằng code trên toàn bộ data.
  2. Code kiểm **mọi số tiền** trong lời nhắn / câu hỏi của model: số không có trong kết quả công cụ (hoặc tin nhắn người dùng, hiệu số với ngân sách) → trả lại cho model viết lại; lần hai vẫn sai thì bỏ lời nhắn, chỉ giữ thẻ quán do code in.
  3. Người dùng nói "rẻ nhất / gần nhất / đánh giá cao nhất" → quán đứng đầu theo code phải có trong đề xuất, thẻ quán được code sắp đúng tiêu chí đó, so đúng giá trị (trước đây chênh < 20k / < 0,3 km coi như ngang).
- **Kết quả:** nhóm lỗi A + B (B22, B23, B27, B29) `run-2` 3/4 → `run-4` 4/4 · tổng 97% → 100% · từ **chưa đạt** chuẩn → **đạt** chuẩn.
- **Câu nào tệ đi sau khi sửa:** **B26** ở `run-3` ("có quán nào bán cơm tấm trong vòng 500m không"). Model quên điền món "cơm tấm" khi gọi `tim_quan`, chỉ điền loại "cơm"; luật mới thấy "gần nhất" nên ép quán gần nhất (Bé Na, chỉ có cơm chiên dứa) lên đầu → trượt `dung_rang_buoc_cung`. Sửa tiếp: khi sắp theo rẻ / gần, quán có nhiều suất **đúng món** vẫn đứng trước; lời nhắc model có ngoại lệ "quán đứng đầu không có món cụ thể → tìm lại với đúng món". `run-4`: B26 qua. Bài học: luật cứng "đứng đầu theo tiêu chí" phải xếp sau "đúng món người dùng nói".

## 4. Còn lại

- **Kết quả dao động giữa các lần chạy:** B23, B27 trượt ở lượt nháp nhưng qua ở `run-2` cùng phiên bản. 30/30 của `run-4` là một lần chạy, không phải bảo đảm. Nguy hiểm: demo có thể ra câu trả lời khác lúc chạy thử. Chỗ an toàn (giá, tổng, chay, dị ứng, ngân sách) vẫn do code chặn nên dao động chủ yếu ở thứ tự và câu chữ.
- **Hội thoại nhiều lượt chưa có trong bộ câu thử:** eval gọi `answer(text)` từng câu độc lập; phần "nhớ ngữ cảnh" (sửa đơn, "không phải hàu", "ốc thì sao") mới thử tay. Nguy hiểm: hiểu sai câu sửa đơn → gợi ý món người dùng vừa bỏ.
- **Grader dò chuỗi:** `must_not` không hiểu câu phủ định (bot viết "mình không gợi ý bỏ yêu cầu ăn chay" vẫn bị coi là vi phạm ở lượt nháp). Đang tránh bằng prompt, chưa sửa grader.
- **`khop_so_thich` chưa có người xác nhận**; người thứ hai chấm thử 5 output chưa làm.
- **Data dựng giả** (60 quán); số câu từ người dùng thật mới 10/30.
- **Góp ý ở buổi demo (28/11), chưa làm:**
  - *Ý mơ hồ cần hỏi lại kỹ hơn:* "muốn ăn gì mát mát" — hiện bot tự hiểu thành sở thích rồi gợi ý luôn (kèm 1 câu hỏi), có thể đoán sai ý (món lạnh? món thanh nhẹ? đồ uống?). Hướng sửa: khi sở thích là từ cảm tính mà data không có nhãn tương ứng, bot hỏi 1 câu có 2–3 lựa chọn cụ thể trước khi tìm; thêm câu thử cho kiểu này (`kho`).
  - *Cá nhân hoá:* gợi ý theo món người dùng hay gọi / không thích. Cần lưu hồ sơ sở thích có đồng ý của người dùng (hiện không lưu gì giữa các phiên, xem `spec.md` §9) và đo lại xem có chọn nhanh hơn không.
- **Từ người dùng thử (`validation/log.md`, 2 phiên), chưa làm:** tin đầu đúng nhưng từ tin thứ hai bot dựng lại đơn hơi khác — (1) hỏi thêm giờ mở thì giữ nguyên món đã gợi ý; (2) không gắn sở thích người dùng chưa nói ("muốn cơm"); (3) người dùng nói "gần" thì ưu tiên quán gần khi so giá (quán 4,8 km lên hạng 1 khi hỏi "rẻ hơn"); (4) bỏ câu mở đầu nhắc món không được hỏi.
- **Nếu có thêm 1 tuần:** chạy mỗi lượt 3 lần và báo % qua trung bình + độ lệch; thêm 10 câu hội thoại nhiều lượt (eval truyền `history`); sửa grader hiểu phủ định; thử với data quán thật và người đặt nhóm thật.
