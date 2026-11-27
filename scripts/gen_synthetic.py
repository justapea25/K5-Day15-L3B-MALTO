"""Sinh data/restaurants.json GIẢ (synthetic, có seed) theo SỐ LIỆU đo từ menu GrabFood nhóm crawl.

Chạy:  python scripts/gen_synthetic.py [--seed 42] [--quan 40]

Dữ liệu crawl (quán thật) chỉ dùng làm BẰNG CHỨNG và để đo số liệu, KHÔNG commit, KHÔNG đưa cho agent.
Data cho agent là quán dựng: tên dựng, món ghép từ mẫu tên món phổ biến, giá / khoảng cách / đánh giá / tỉ lệ
có mô tả / tỉ lệ món chay lấy theo phân bố đo được (bảng STATS dưới, đo ngày 27/11/2026 trên 60 quán, 2.389 món
chính của bản crawl — xem data/DATA_CARD.md).
Nhãn chay / co_nhac / thit / loai gắn bằng cùng bộ từ khoá với scripts/build_data.py.
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_data import ALLERGEN, THIT, LOAI, tags  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Số liệu đo từ bản crawl (60 quán, 2.389 món chính)
STATS = {
    "mon_moi_quan": (20, 30, 40),          # thấp · trung vị · cao (trung vị đo được 29,5)
    "km": (0.1, 0.5, 2.5),                 # trung vị 0,5 km
    "danh_gia": (4.0, 4.3, 4.8),           # trung vị 4,3 (25/60 quán có đánh giá)
    "ti_le_co_danh_gia": 25 / 60,
    "ti_le_co_gio_mo": 7 / 60,
    "ti_le_co_mo_ta": 0.65,                # 65% món có mô tả
    "gia": {"bun": (60000, 68000, 80000), "pho": (68000, 74000, 87000), "com": (55000, 72000, 95000),
            "mi": (45000, 70000, 115000), "banh_mi": (25000, 38000, 55000), "lau": (350000, 450000, 580000),
            "khac": (45000, 79000, 155000)},
}

# Mẫu quán: (loại chính, tên dựng, mẫu món chính, mẫu món phụ "khác")
DISHES = {
    "bun": [("Bún bò Huế", "bò bắp, giò heo, chả cua"), ("Bún chả", "chả nướng, thịt ba chỉ nướng, nước mắm chua ngọt"),
            ("Bún riêu cua", "riêu cua, đậu phụ, cà chua"), ("Bún cá", "cá rô chiên, cần, cà chua"),
            ("Bún thang", "gà xé, trứng tráng, giò lụa"), ("Bún ốc", "ốc, đậu phụ, cà chua"),
            ("Bún trộn Nam Bộ", "thịt bò xào, lạc rang, rau thơm"), ("Bún mọc", "mọc heo, sườn"),
            ("Bún chay nấm", "nấm, đậu phụ, rau củ"), ("Bún đậu mắm tôm", "đậu phụ rán, chả cốm, mắm tôm")],
    "pho": [("Phở bò tái", "bò tái, hành"), ("Phở bò chín", "bò chín, hành"), ("Phở gà", "gà ta xé"),
            ("Phở bò sốt vang", "bò sốt vang"), ("Phở cuốn", "bò xào, rau thơm"), ("Phở trộn", "thịt bò, lạc rang"),
            ("Phở chay", "nước dùng rau củ, nấm")],
    "com": [("Cơm rang dưa bò", "thịt bò, dưa cải"), ("Cơm gà xối mỡ", "gà chiên giòn"), ("Cơm sườn nướng", "sườn heo nướng, trứng ốp"),
            ("Cơm rang hải sản", "tôm, mực"), ("Cơm văn phòng thịt kho", "thịt heo kho, trứng"), ("Cơm cá kho", "cá kho tộ"),
            ("Cơm chay thập cẩm", "đậu phụ, nấm, rau củ"), ("Cơm tấm bì chả", "sườn, bì, chả trứng"), ("Xôi xéo", "đỗ xanh, hành phi")],
    "mi": [("Mì xào bò", "thịt bò, rau cải"), ("Miến lươn", "lươn chiên"), ("Mì vằn thắn", "vằn thắn tôm thịt"),
           ("Hủ tiếu Nam Vang", "tôm, thịt heo, gan"), ("Miến gà", "gà xé, nấm"), ("Mì xào chay", "rau củ, nấm, đậu phụ"),
           ("Bánh canh cua", "cua, chả")],
    "banh_mi": [("Bánh mì pate", "pate, chả, thịt nguội"), ("Bánh mì trứng", "trứng ốp, dưa góp"), ("Bánh mì xíu mại", "xíu mại heo"),
                ("Bánh mì chay", "đậu phụ, nấm"), ("Burger bò", "bò, phô mai")],
    "lau": [("Lẩu thái hải sản", "tôm, mực, nghêu"), ("Lẩu riêu cua bắp bò", "riêu cua, bắp bò"), ("Lẩu gà lá é", "gà ta"),
            ("Lẩu nấm chay", "nấm các loại")],
    "khac": [("Gỏi cuốn", "tôm, thịt, bún, rau"), ("Nem rán", "thịt heo, mộc nhĩ"), ("Gà rán", "gà tẩm bột chiên"),
             ("Salad ức gà", "ức gà, rau xanh"), ("Há cảo hấp", "tôm, thịt"), ("Chả cá lã vọng", "cá lăng, thì là"),
             ("Bò lúc lắc", "bò, ớt chuông"), ("Đậu phụ sốt cà chua", "đậu phụ, cà chua"), ("Nộm đu đủ", "đu đủ, lạc rang"),
             ("Khoai tây chiên", "khoai tây"), ("Cháo sườn", "sườn heo, quẩy"), ("Pizza hải sản", "tôm, mực, phô mai")],
}
SHOPS = [("bun", "Bún"), ("pho", "Phở"), ("com", "Cơm"), ("mi", "Mì Miến"), ("banh_mi", "Bánh Mì"), ("lau", "Lẩu"),
         ("chay", "Quán Chay"), ("da_mon", "Bếp")]
SHOP_WEIGHTS = [0.18, 0.12, 0.22, 0.12, 0.08, 0.06, 0.06, 0.16]
OWNERS = ["Cô Lan", "Bà Tư", "Chú Hải", "Anh Béo", "Chị Mai", "Ông Bảy", "Cô Hằng", "Bác Thành", "Nhà Gạo", "Góc Phố",
          "Ngõ Nhỏ", "Phố Cũ", "Bếp Mẹ", "Sân Đình", "Hồ Tây", "Gia Lâm", "Ven Hồ", "Cây Bàng", "Hàng Xóm", "Chợ Sớm"]
SIZES = ["", " (nhỏ)", " (lớn)", " đặc biệt", " thập cẩm"]
HOURS = ["06:00-14:00 17:00-21:30", "07:00-21:00", "10:00-14:00 17:00-22:00", "09:00-22:00"]


def tri(rng, lo, mid, hi):
    return rng.triangular(lo, hi, mid)


def price(rng, loai):
    lo, mid, hi = STATS["gia"][loai]
    return int(round(tri(rng, lo * 0.85, mid, hi * 1.1) / 5000) * 5000)


def make_dish(rng, qid, k, name, desc, loai, force_veg=False):
    text = (name + " " + desc).lower()
    chay = True if "chay" in name.lower() or force_veg else None
    has_desc = rng.random() < STATS["ti_le_co_mo_ta"]
    return {"id": "%s-%d" % (qid, k), "ten": name, "gia": price(rng, loai), "loai": loai, "nhom": "Món chính",
            "mo_ta": desc if has_desc else "", "chay": chay,
            # nhãn chỉ dựa trên phần quán GHI (tên + mô tả hiện ra), như với data thật
            "co_nhac": tags(name + " " + (desc if has_desc else ""), ALLERGEN),
            "thit": [] if chay else tags(name + " " + (desc if has_desc else ""), THIT),
            "ghi_thanh_phan": has_desc}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--quan", type=int, default=40)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    used, out = set(), []
    for i in range(1, a.quan + 1):
        kind, label = rng.choices(SHOPS, SHOP_WEIGHTS)[0]
        while True:
            name = "%s %s" % (label, rng.choice(OWNERS))
            if name not in used:
                used.add(name)
                break
        qid = "Q%02d" % i
        n = int(tri(rng, *STATS["mon_moi_quan"]))
        if kind == "chay":
            pool = [(nm, ds, lo) for lo in ("bun", "pho", "com", "mi", "banh_mi", "lau") for nm, ds in DISHES[lo] if "chay" in nm.lower()]
            pool += [("Đậu phụ sốt cà chua chay", "đậu phụ, cà chua", "khac"), ("Nộm chay", "rau củ, lạc rang", "khac")]
        elif kind == "da_mon":
            pool = [(nm, ds, lo) for lo in ("com", "bun", "mi", "khac") for nm, ds in DISHES[lo]]
        else:
            pool = [(nm, ds, kind) for nm, ds in DISHES[kind]] + [(nm, ds, "khac") for nm, ds in DISHES["khac"]]
        mons, seen = [], set()
        for _ in range(n * 3):
            if len(mons) >= n:
                break
            nm, ds, lo = rng.choice(pool)
            full = nm + rng.choice(SIZES)
            if full in seen:
                continue
            seen.add(full)
            mons.append(make_dish(rng, qid, len(mons) + 1, full, ds, lo, force_veg=(kind == "chay")))
        out.append({"id": qid, "ten": name, "khu_vuc": None,
                    "am_thuc": {"chay": "Món chay", "da_mon": "Cơm, Bún, Món Việt"}.get(kind, label),
                    "khoang_cach_km": round(tri(rng, *STATS["km"]), 1),
                    "danh_gia": round(tri(rng, *STATS["danh_gia"]), 1) if rng.random() < STATS["ti_le_co_danh_gia"] else None,
                    "gio_mo": rng.choice(HOURS) if rng.random() < STATS["ti_le_co_gio_mo"] * 2 else None,
                    "freeship": rng.random() < 0.1, "khuyen_mai": None, "mon": mons})
    # Bổ sung đánh giá + giờ mở cửa cho MỌI quán (data thật chỉ 25/60 quán có sao, 7/60 ghi giờ) — dùng RNG riêng để không đổi các trường khác
    rng2 = random.Random(a.seed + 1)
    for q in out:
        if q["danh_gia"] is None:
            q["danh_gia"] = round(tri(rng2, *STATS["danh_gia"]), 1)
        q["so_danh_gia"] = int(tri(rng2, 15, 120, 900))
        if q["gio_mo"] is None:  # data thật chỉ ~12% quán ghi giờ; bổ sung cho mọi quán, có quán chỉ bán tối
            q["gio_mo"] = rng2.choices(HOURS + ["16:30-23:00", "17:00-22:30"], [3, 3, 3, 3, 1, 1])[0]
    out.sort(key=lambda q: q["khoang_cach_km"])
    for i, q in enumerate(out, 1):  # đánh lại mã theo khoảng cách
        old = q["id"]
        q["id"] = "Q%02d" % i
        for m in q["mon"]:
            m["id"] = m["id"].replace(old + "-", q["id"] + "-", 1)
    data = {"_ghi_chu": ("synthetic — quán DỰNG GIẢ, tên dựng, sinh bằng scripts/gen_synthetic.py (seed %d) theo phân bố "
                         "giá, khoảng cách, đánh giá, tỉ lệ có mô tả, tỉ lệ món chay đo từ menu GrabFood nhóm crawl. "
                         "Không phải quán thật. Không có phí ship. Xem data/DATA_CARD.md." % a.seed),
            "seed": a.seed, "ma_di_ung": list(ALLERGEN), "ma_thit": list(THIT), "ma_loai": [c for c, _ in LOAI] + ["khac"],
            "quan": out}
    path = os.path.join(ROOT, "data", "restaurants.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    M = [m for q in out for m in q["mon"]]
    print("Ghi data/restaurants.json: %d quán, %d món (seed %d) · có mô tả %.0f%% · món chay %d · quán có giờ mở %d"
          % (len(out), len(M), a.seed, 100 * sum(m["ghi_thanh_phan"] for m in M) / len(M),
             sum(1 for m in M if m["chay"]), sum(1 for q in out if q["gio_mo"])))


if __name__ == "__main__":
    main()
