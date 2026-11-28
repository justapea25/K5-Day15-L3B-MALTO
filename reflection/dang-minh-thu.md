# Reflection — Đặng Minh Thu

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):

   Mình phụ trách dữ liệu quán và công cụ tra cứu. Cụ thể: `codebase/tools.py` (công cụ tìm quán, lấy menu, kiểm ràng buộc; commit `2ba4963`), `data/DATA_CARD.md`, `data/SCHEMA.md`, `data/README.md` (`2ba4963`, `fdb2a50`), crawl GrabFood và script chuẩn hoá `data/grab/normalize_grab.py`, `data/grab/check_data.py`. Phần đào data cho bằng chứng pain là `evidence/data-mining.md` và `evidence/count.py` (`c85d4a5`). Sau CP3 mình viết lại SCHEMA và README theo đúng `restaurants.json` đang dùng, sửa docstring `tools.py` và viết lại `tests/test_tools.py` (11 test, chạy qua) cho khớp API hiện tại (`fdb2a50`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

   Mình dùng Claude Code để viết và sửa `tools.py`, script đếm (`evidence/count.py`), script chuẩn hoá data crawl, và `tests/test_tools.py`. Output AI mình đọc lại và chỉnh cho khớp data thật và API hiện tại (docstring `tools.py`, SCHEMA, test viết lại ở `fdb2a50`). `data/restaurants.json` sinh bằng `scripts/gen_synthetic.py` seed 42 (60 quán, 1.142 món); mình đã kiểm hết 60 quán và 1.142 món, khớp. Data crawl GrabFood (258 quán, 11.322 món) chỉ dùng để đo số liệu, không commit, không đưa cho agent.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

   Câu **B26** ("có quán nào bán cơm tấm trong vòng 500m không") trượt `dung_rang_buoc_cung` ở `run-3` (`eval/report.md` §3). Model chỉ điền loại "cơm" khi gọi `tim_quan`, không điền đúng món "cơm tấm", nên luật mới "gần nhất" đẩy Bé Na (chỉ có cơm chiên dứa) lên đầu. Minh sửa ở `run-4` bằng cách xếp quán có đúng món lên trước. Với phần dữ liệu và công cụ của mình, bài học là: nhãn `loai` thô ("cơm") gộp cả cơm tấm lẫn cơm chiên, nên mọi bước xếp hạng phía sau đều dễ chọn nhầm. Khi sinh và gắn nhãn data, mình cần kiểm xem nhãn có đủ mịn cho những món người dùng hay hỏi cụ thể không.
