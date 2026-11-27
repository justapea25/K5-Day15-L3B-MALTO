"""Đếm bằng chứng từ menu GrabFood nhóm crawl (đào data, guide bước 1.2).

Chạy:  python evidence/count_menu.py <thư mục chứa restaurants.csv, menu_items.csv>
Data crawl KHÔNG commit (quán thật) — script này để người khác có data chạy lại ra cùng số.
Cách đếm ghi trước ở evidence/data-mining.md mục 1.
"""
import csv
import os
import re
import sys


def main(src):
    R = list(csv.DictReader(open(os.path.join(src, "restaurants.csv"), encoding="utf-8-sig")))
    M = list(csv.DictReader(open(os.path.join(src, "menu_items.csv"), encoding="utf-8-sig")))
    n, nq = len(M), len(R)
    nodesc = [m for m in M if not m["description"].strip()]
    allergy_word = [m for m in M if "dị ứng" in m["description"].lower()]
    veg = {m["restaurant_id"] for m in M if re.search(r"\bchay\b", m["item_name"] + " " + m["category"], re.I)}
    print("Mẫu: %d quán, %d món (mọi món trong menu đã crawl)" % (nq, n))
    print("1. Món không có mô tả:            %d/%d (%.1f%%)" % (len(nodesc), n, 100 * len(nodesc) / n))
    print("2. Mô tả có chữ 'dị ứng':         %d/%d (%.1f%%)" % (len(allergy_word), n, 100 * len(allergy_word) / n))
    print("3. Quán có ≥1 món ghi chữ 'chay': %d/%d (%.1f%%)" % (len(veg), nq, 100 * len(veg) / nq))
    print("Ví dụ món không có mô tả (5 món đầu theo thứ tự file):")
    for m in nodesc[:5]:
        print("  -", m["item_name"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: python evidence/count_menu.py <thư mục CSV crawl>")
    main(sys.argv[1])
