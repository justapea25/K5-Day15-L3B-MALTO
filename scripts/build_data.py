"""Dựng data/restaurants.json từ dữ liệu menu GrabFood nhóm crawl (restaurants.csv, menu_items.csv).

Chạy:  python scripts/build_data.py <thư mục chứa CSV crawl> [--max-quan 60] [--max-km 3]

Làm gì (ghi vào data/DATA_CARD.md):
  - Chỉ giữ quán đồ ăn (main_type = food), có menu, cách ≤ max_km, ≥ 8 món chính. Lấy max_quan quán gần nhất.
  - Bỏ link, bỏ cột nội bộ. Mã quán đánh lại Q01, Q02… theo khoảng cách.
  - Chỉ giữ MÓN CHÍNH: bỏ đồ uống, topping, món thêm, món < 20.000đ.
  - Gắn nhãn bằng TỪ KHOÁ trên tên + nhóm + mô tả món (heuristic, có thể sót / nhầm):
      loai     bun / pho / com / mi / banh_mi / lau / khac
      chay     true nếu tên hoặc nhóm món có chữ "chay"; ngược lại null (không rõ)
      co_nhac  chất gây dị ứng ĐƯỢC NHẮC trong tên / mô tả (hai_san, dau_phong, sua, trung, dau_nanh)
      thit     loại thịt được nhắc (bo, heo, ga, vit, ca, hai_san)
      ghi_thanh_phan  món có mô tả hay không
File CSV gốc KHÔNG commit (dữ liệu crawl của quán thật).
"""
import argparse
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP = re.compile(r"đồ uống|nước|trà|cà phê|cafe|coffee|sinh tố|soda|coca|pepsi|7up|sting|lavie|dasani|bia|"
                  r"topping|thêm|add|gói|ly |cốc|kem|sữa chua|tráng miệng|bánh ngọt|kim chi|canh\b|rau thêm", re.I)
LOAI = [("banh_mi", r"bánh mì|bánh mỳ|burger|sandwich"), ("bun", r"\bbún\b"), ("pho", r"\bphở\b"),
        ("com", r"\bcơm\b|\bxôi\b"), ("mi", r"\bmì\b|\bmỳ\b|miến|hủ tiếu|bánh canh|udon|ramen|spaghetti|mỳ ý"),
        ("lau", r"\blẩu\b")]
ALLERGEN = {"hai_san": r"tôm|\bcua\b|mực|hải sản|ghẹ|nghêu|ngao|\bsò\b|hến|riêu|bạch tuộc|tép|ruốc|\bốc\b|sushi|sashimi",
            "dau_phong": r"lạc|đậu phộng|bơ đậu",
            "sua": r"sữa|phô mai|phomai|cheese|bơ\b|kem\b|mayonnaise|mayo",
            "trung": r"trứng|ốp la|chả trứng",
            "dau_nanh": r"đậu phụ|đậu hũ|tàu hũ|đậu nành|tương|tofu"}
THIT = {"bo": r"\bbò\b|beef", "heo": r"heo|lợn|sườn|xá xíu|ba chỉ|giò|chả\b|thịt nướng|nem|pork|bacon|xúc xích",
        "ga": r"\bgà\b|chicken", "vit": r"vịt|ngan", "ca": r"\bcá\b|fish|cá hồi|cá ngừ", "hai_san": ALLERGEN["hai_san"]}


def tags(text, table):
    return [k for k, p in table.items() if re.search(p, text, re.I)]


def dish(m, qid, k):
    name, cat, desc = m["item_name"].strip(), m["category"].strip(), m["description"].strip()
    text = " ".join([name, desc]).lower()   # nhãn theo tên + mô tả món, KHÔNG theo tên nhóm (nhóm hay ghi chung chung)
    loai = next((code for code, p in LOAI if re.search(p, name, re.I)), "khac")
    chay = True if re.search(r"\bchay\b", name + " " + cat, re.I) else None
    return {"id": "%s-%d" % (qid, k), "ten": name, "gia": int(float(m["price_vnd"])), "loai": loai,
            "nhom": cat, "mo_ta": desc[:200], "chay": chay,
            "co_nhac": tags(text, ALLERGEN), "thit": [] if chay else tags(text, THIT),
            "ghi_thanh_phan": bool(desc)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="thư mục chứa restaurants.csv, menu_items.csv")
    ap.add_argument("--max-quan", type=int, default=60)
    ap.add_argument("--max-km", type=float, default=3.0)
    a = ap.parse_args()
    R = list(csv.DictReader(open(os.path.join(a.src, "restaurants.csv"), encoding="utf-8-sig")))
    M = list(csv.DictReader(open(os.path.join(a.src, "menu_items.csv"), encoding="utf-8-sig")))
    by_rest = {}
    for m in M:
        if m["price_flag"] or not m["price_vnd"] or m["only_in_promo_section"] == "True":
            continue
        if int(float(m["price_vnd"])) < 20000 or SKIP.search(m["item_name"] + " " + m["category"]):
            continue
        by_rest.setdefault(m["restaurant_id"], []).append(m)

    cands = [r for r in R if r["main_type"] == "food" and r["distance_km"]
             and float(r["distance_km"]) <= a.max_km and len(by_rest.get(r["restaurant_id"], [])) >= 8]
    cands.sort(key=lambda r: (float(r["distance_km"]), r["name"]))
    # luôn giữ quán có món chay (ít, nhưng cần cho ca ăn chay), rồi lấp bằng quán gần nhất
    has_veg = lambda r: any(re.search(r"\bchay\b", m["item_name"] + " " + m["category"], re.I) for m in by_rest[r["restaurant_id"]])
    keep = [r for r in cands if has_veg(r)]
    keep += [r for r in cands if r not in keep][:max(0, a.max_quan - len(keep))]
    keep.sort(key=lambda r: (float(r["distance_km"]), r["name"]))
    out = []
    for i, r in enumerate(keep, 1):
        qid = "Q%02d" % i
        seen, mons = set(), []
        for m in by_rest[r["restaurant_id"]]:
            key = m["item_name"].strip().lower()
            if key in seen:
                continue
            seen.add(key)
            mons.append(dish(m, qid, len(mons) + 1))
        out.append({"id": qid, "ten": r["name"].strip(), "khu_vuc": r["area"] or None, "am_thuc": r["cuisine"],
                    "khoang_cach_km": float(r["distance_km"]),
                    "danh_gia": float(r["rating"]) if r["rating"] else None,
                    "gio_mo": r["open_hours"] or None,
                    "freeship": r["has_freeship"] == "True",
                    "khuyen_mai": (r["promo_summary"] or "").split(" ; ")[0][:120] or None,
                    "mon": mons})
    data = {
        "_ghi_chu": ("Dữ liệu menu thật của quán trên GrabFood quanh Vinhomes Ocean Park (Hà Nội), nhóm crawl. "
                     "Đã bỏ link, chỉ giữ món chính. Nhãn chay / co_nhac / thit / loai gắn bằng TỪ KHOÁ (heuristic), "
                     "có thể sót hoặc nhầm. Không có phí ship. Giá và giờ mở cửa tại thời điểm crawl. Xem data/DATA_CARD.md."),
        "ma_di_ung": list(ALLERGEN), "ma_thit": list(THIT), "ma_loai": [c for c, _ in LOAI] + ["khac"],
        "quan": out,
    }
    path = os.path.join(ROOT, "data", "restaurants.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    n_mon = sum(len(q["mon"]) for q in out)
    print("Ghi %s: %d quán, %d món chính" % (os.path.relpath(path, ROOT), len(out), n_mon))
    print("  món ghi chay: %d · món có mô tả: %d · quán có giờ mở cửa: %d"
          % (sum(1 for q in out for m in q["mon"] if m["chay"]), sum(1 for q in out for m in q["mon"] if m["ghi_thanh_phan"]),
             sum(1 for q in out if q["gio_mo"])))


if __name__ == "__main__":
    main()
