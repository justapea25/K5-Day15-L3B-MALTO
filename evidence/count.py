"""Đếm số liệu cho evidence/data-mining.md.

Chạy:  python evidence/count.py   (ở thư mục gốc repo; cần 3 CSV trong data/grab/)
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent.parent / "data" / "grab"


def load(name):
    with open(D / name, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def line(label, x, n, note=""):
    print(f"{label} | {x}/{n} ({100 * x / n:.0f}%) | {note}")


rs, items, promos = load("restaurants.csv"), load("menu_items.csv"), load("promotions.csv")
searchable = [r for r in rs if r["open_status"] != "no_menu"]
n = len(searchable)
print(f"quán={len(rs)} tìm được={n} món={len(items)} khuyến mãi={len(promos)}")

line("quán đang Closed lúc lấy", sum(r["open_status"] == "closed_at_crawl" for r in searchable), n, "mẫu số: quán có menu")
line("quán không có khu vực (area rỗng)", sum(not r["area"] for r in searchable), n)
line("quán đồ uống (drink)", sum(r["main_type"] == "drink" for r in searchable), n)
line("quán có voucher còn hạn", sum(r["has_voucher"] == "True" for r in searchable), n)
line("quán có giảm phí giao", sum(r["has_freeship"] == "True" for r in searchable), n)
line("quán giao nhanh (ETA ≤ 20p)", sum(r["is_fast"] == "True" for r in searchable), n)
for lv in ("cheap", "mid", "high"):
    line(f"quán mức giá {lv}", sum(r["price_level"] == lv for r in searchable), n)

m = len(items)
line("món không có mô tả", sum(i["has_description"] != "True" for i in items), m, "không biết thành phần")
line("món không có giá dùng được", sum(not i["price_vnd"] for i in items), m)
line("món đang giảm giá", sum(bool(i["discount_pct"]) for i in items), m)

# Quán đủ "lọc chay": tối thiểu 1 món có mô tả và không có từ khoá thịt/cá (xấp xỉ, xem MEAT_KEYWORDS trong codebase/tools.py)
try:
    sys.path.insert(0, str(D.parent.parent / "codebase"))
    from tools import MEAT_KEYWORDS
    def veg_ok(i):
        t = (i["item_name"] + " " + i["description"]).lower()
        return i["has_description"] == "True" and not any(k in t for k in MEAT_KEYWORDS)
    line("món qua được bộ lọc chay", sum(veg_ok(i) for i in items), m, "MEAT_KEYWORDS trong tools.py")
    by = {}
    for i in items:
        by.setdefault(i["restaurant_id"], []).append(veg_ok(i))
    ok = sum(1 for r in searchable if any(by.get(r["restaurant_id"], [])))
    line("quán có ≥1 món qua bộ lọc chay", ok, n)
except Exception as e:
    print("bỏ qua phần lọc chay:", e)
