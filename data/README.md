# Thư mục data

| File | Là gì | Trong repo? |
|---|---|---|
| `restaurants.json` | **Dữ liệu agent dùng**: 60 quán + 1.142 món dựng giả (synthetic, seed 42) | Có |
| `DATA_CARD.md` | Nguồn, cách sinh, seed, số dòng, giới hạn | Có |
| `SCHEMA.md` | Ý nghĩa từng trường của `restaurants.json` | Có |
| `grab/*.csv`, `grab/*.json` | Dữ liệu crawl GrabFood (258 quán, 11.322 món) — chỉ để đo số liệu và làm bằng chứng, **agent không đọc** | Không (`.gitignore`) |
| `grab/normalize_grab.py`, `grab/check_data.py` | Script chuẩn hoá và kiểm dữ liệu crawl | Có |

Chạy lại dữ liệu agent dùng (ra đúng file đang commit):

    python scripts/gen_synthetic.py --seed 42

Kiểm đã đủ dữ liệu chưa (ở thư mục gốc repo):

    python -c "import sys; sys.path.insert(0,'codebase'); import tools; print(len(tools.search_restaurants()))"

In ra `60` là dùng được. Ý nghĩa trường: `SCHEMA.md`. Nguồn và giới hạn: `DATA_CARD.md`.
