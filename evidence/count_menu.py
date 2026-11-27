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
    # --- Pain chính: quán nhiều, menu dài → tự lục tìm quán đủ món cho cả đơn rất tốn công
    import statistics
    food = {r["restaurant_id"] for r in R if r["main_type"] == "food"}
    per = {}
    for m in M:
        if m["restaurant_id"] in food:
            per[m["restaurant_id"]] = per.get(m["restaurant_id"], 0) + 1
    L = [per.get(r, 0) for r in food]
    nf = len(food)
    print("PAIN CHÍNH — quán đồ ăn (main_type = food): %d quán, %d món" % (nf, sum(L)))
    print("A. Số món / menu: trung vị %g · trung bình %.0f · nhiều nhất %d" % (statistics.median(L), sum(L) / nf, max(L)))
    print("B. Quán có ≥ 30 món: %d/%d (%.0f%%)" % (sum(x >= 30 for x in L), nf, 100 * sum(x >= 30 for x in L) / nf))
    print("C. Quán có ≥ 50 món: %d/%d (%.0f%%)" % (sum(x >= 50 for x in L), nf, 100 * sum(x >= 50 for x in L) / nf))
    print()
    print("PHẦN PHỤ — mẫu: %d quán, %d món (mọi món trong menu đã crawl)" % (nq, n))
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
