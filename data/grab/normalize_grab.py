"""Chuẩn hoá dữ liệu GrabFood thô -> CSV/JSON sạch cho chatbot chọn quán.

Dùng:  python data/grab/normalize_grab.py data/grab/grab_raw.json

Đầu vào (grab_raw.json):
  {"crawled_at", "origin", "list": [quán...], "menus": {id: {hours, promos, categories}},
   "promos": {id: {has_link, blocks: [{title, rules[]}]}}}

Đầu ra (cùng thư mục):
  restaurants.csv      1 dòng / quán: tên, khu vực, khoảng cách, ETA, rating, mức giá, cờ giao nhanh/freeship/voucher
  menu_items.csv       1 dòng / món: giá, giá gốc, % giảm, kcal, mô tả món (đầy đủ nhất có thể)
  promotions.csv       1 dòng / khuyến mãi: loại, % hoặc số tiền giảm, đơn tối thiểu, giảm tối đa, hạn dùng
  dataset.json         bản lồng nhau (quán -> khuyến mãi + menu) để nạp thẳng cho công cụ
  DATA_CARD_grab.md    bản nháp mục "Dataset" cho data/DATA_CARD.md, số liệu điền sẵn từ dữ liệu
"""
import csv
import json
import re
import sys
from pathlib import Path

PROMO_CATS = {"ưu đãi hôm nay", "dành cho bạn", "quyền lợi dành riêng hội viên grabunlimited"}
FAST_ETA_MIN = 20          # <= 20 phút coi là giao nhanh
CHEAP_MEDIAN = 40_000      # median giá món < 40k -> rẻ
MID_MEDIAN = 80_000        # 40k-80k -> vừa, > 80k -> cao

# Khu vực đoán từ tên quán (heuristic, có thể rỗng). Thứ tự: cụ thể trước, chung sau.
AREAS = [
    ("Vinhomes Ocean Park", r"ocean\s*park|oceanpark|vinhomes?\s*op|\bvin\s?1\b|\bvin1\b|s[1-3]\.\d{2}"),
    ("Trâu Quỳ", r"tr[âa]u\s*qu[ỳy]"),
    ("Đa Tốn", r"đa\s*tốn"),
    ("Kiêu Kỵ", r"kiêu\s*kỵ"),
    ("Cổ Bi", r"cổ\s*bi"),
    ("Dương Xá", r"dương\s*xá"),
    ("Yên Viên", r"yên\s*viên"),
    ("Phú Thị", r"phú\s*thị"),
    ("Gia Lâm", r"gia\s*lâm"),
    ("Long Biên", r"long\s*biên"),
]


def guess_area(name):
    for label, pat in AREAS:
        if re.search(pat, name, re.I):
            return label
    return ""


def money(text):
    m = re.search(r"(\d[\d.]*)\s*₫", text or "")
    return int(m.group(1).replace(".", "")) if m else None


def classify(title):
    t = title.lower()
    if "phí giao" in t or "freeship" in t or "miễn phí giao" in t or "miễn phí vận chuyển" in t:
        return "delivery_fee"
    if re.search(r"mua .* tặng", t) or t.startswith("tặng"):
        return "buy_gift"
    if "sản phẩm" in t or "món" in t:
        return "item_discount"
    if "giảm" in t:
        return "order_discount"
    return "other"


def expand_blocks(title, rules):
    """Khối "Tận hưởng ưu đãi" chứa nội dung thật ở dòng điều kiện (VD "Giảm 30% cho một số sản phẩm"):
    tách mỗi dòng thành một khuyến mãi riêng, tiêu đề là chính nội dung đó."""
    if title.strip().lower() == "tận hưởng ưu đãi" and rules:
        return [(r, []) for r in rules]
    return [(title, rules)]


def parse_block(title, rules):
    text = " | ".join([title] + rules)
    pct = re.search(r"(\d+)\s*%", title)
    frm = re.search(r"Hạn sử dụng\s+(\S+ \S+)\s+đến\s+(\S+ \S+)", text)
    min_order = re.search(r"tối thiểu\s*([\d.]+)\s*₫", text)
    max_disc = re.search(r"Giảm tối đa\s*([\d.]+)\s*₫", text)
    kind = classify(title)
    return {
        "type": kind,
        "is_freeship": kind == "delivery_fee",
        "title": title,
        "discount_pct": int(pct.group(1)) if pct else None,
        "discount_vnd": money(title) if not pct else None,
        "min_order_vnd": int(min_order.group(1).replace(".", "")) if min_order else None,
        "max_discount_vnd": int(max_disc.group(1).replace(".", "")) if max_disc else None,
        "valid_from": frm.group(1) if frm else None,
        "valid_to": frm.group(2) if frm else None,
        "conditions": " | ".join(rules),
    }


def promos_for(raw, rid):
    """Ưu tiên khối 'promos' (đủ điều kiện); không có thì dùng chuỗi khuyến mãi từ menu."""
    out = []
    p = (raw.get("promos") or {}).get(rid)
    if p and p.get("blocks"):
        for b in p["blocks"]:
            for t, rl in expand_blocks(b["title"], b.get("rules", [])):
                out.append(parse_block(t, rl))
    else:
        for s in ((raw["menus"].get(rid) or {}).get("promos") or []):
            out.append(parse_block(s, []))
    return out


DRINK_PAT = re.compile(r"trà|cà phê|cafe|coffee|nước ép|sinh tố|sữa chua|đồ uống|smoothie|matcha|boba", re.I)


def split_tags(cuisine):
    return [t.strip() for t in re.split(r"\s*[,\-–]\s*", cuisine or "") if t.strip()]


def merge_menu(categories):
    """Gộp món: ưu tiên nhóm thật; nhóm "Ưu đãi hôm nay / Dành cho bạn" chỉ bổ sung thông tin giảm giá
    hoặc thêm món chưa có. Trả về list món (đã khử trùng theo tên)."""
    real = [c for c in categories if c["cat"].strip().lower() not in PROMO_CATS]
    meta = [c for c in categories if c["cat"].strip().lower() in PROMO_CATS]
    by_name, order = {}, []
    for cat in real + meta:
        is_meta = cat["cat"].strip().lower() in PROMO_CATS
        for it in cat["items"]:
            key = it["n"].strip().lower()
            if key not in by_name:
                by_name[key] = {**it, "_cat": cat["cat"], "_meta_only": is_meta}
                order.append(key)
            elif is_meta and it.get("o") and not by_name[key].get("o"):
                cur = by_name[key]       # món có ở nhóm thật nhưng giá giảm chỉ hiện ở nhóm ưu đãi
                cur["p"], cur["o"], cur["s"] = it["p"], it["o"], it["s"]
    return [by_name[k] for k in order]


def clean_desc(d):
    d = re.sub(r"\[\d+ kcal\]\s*-?\s*", "", d or "")
    return re.sub(r"\s+", " ", d).strip(" -")


def main(path):
    src = Path(path)
    raw = json.loads(src.read_text(encoding="utf-8"))
    out = src.parent
    restaurants, items, promos, nested = [], [], [], []

    for r in raw["list"]:
        rid = r["id"]
        m = raw["menus"].get(rid)
        menu = []
        if m:
            for it in merge_menu(m["categories"]):
                desc = it["d"] or ""
                kcal = re.search(r"\[(\d+) kcal\]", desc)
                price, orig = it["p"], it["o"]
                flag = ""
                if not price:
                    flag = "missing"                 # Grab không hiện giá (VD món chọn size mới có giá)
                elif price < 1000:
                    flag, price = "invalid_lt_1000", None   # dòng ghi chú bị đọc nhầm thành giá
                if orig is not None and (price is None or orig <= price):
                    orig = None
                d = clean_desc(desc)
                menu.append({
                    "item_id": f"{rid}#{len(menu) + 1:03d}",
                    "restaurant_id": rid,
                    "category": it["_cat"],
                    "item_name": it["n"],
                    "price_vnd": price,
                    "price_flag": flag,
                    "original_price_vnd": orig,
                    "discount_vnd": it["s"] if orig else None,
                    "discount_pct": round(100 * (orig - price) / orig) if orig and price else None,
                    "kcal": int(kcal.group(1)) if kcal else None,
                    "description": d,
                    "has_description": bool(d),
                    "only_in_promo_section": it["_meta_only"],
                })
        items.extend(menu)

        pr = promos_for(raw, rid)
        crawl_date = (raw.get("crawled_at") or "")[:10]
        for p in pr:
            p["is_expired"] = bool(p["valid_to"] and crawl_date and p["valid_to"][:10] < crawl_date)
        pr_live = [p for p in pr if not p["is_expired"]]
        for p in pr:
            promos.append({"restaurant_id": rid, **p})

        prices = sorted(i["price_vnd"] for i in menu if i["price_vnd"])
        dist = r.get("distance_km")
        if dist is None and re.search(r"đại học vinuni", r["name"], re.I):
            dist = 0.0                      # quán nằm ngay trong trường (điểm giao hàng)
        hours = (m or {}).get("hours", "")
        if not m or not menu:
            open_status = "no_menu"
        elif hours:
            open_status = "has_hours"
        else:
            open_status = "closed_at_crawl"  # Grab hiện "Closed" lúc lấy, không có lịch mở cửa
        cuisine = r.get("cuisine", "")
        main_type = "drink" if DRINK_PAT.search(cuisine) and not re.search(r"cơm|bún|phở|mì|bánh mì|xôi|lẩu|nướng", cuisine, re.I) else "food"
        median = prices[len(prices) // 2] if prices else None
        if median is None:
            level = ""
        elif median < CHEAP_MEDIAN:
            level = "cheap"
        elif median <= MID_MEDIAN:
            level = "mid"
        else:
            level = "high"
        disc_items = [i for i in menu if i["discount_pct"]]

        row = {
            "restaurant_id": rid,
            "name": r["name"],
            "area": guess_area(r["name"]),
            "cuisine": cuisine,
            "cuisine_tags": "|".join(split_tags(cuisine)),
            "main_type": main_type,
            "distance_km": dist,
            "eta_min": r.get("eta_min"),
            "is_fast": bool(r.get("eta_min") and r["eta_min"] <= FAST_ETA_MIN),
            "rating": r.get("rating"),
            "open_hours": hours,
            "open_status": open_status,
            "n_items": len(menu),
            "min_price_vnd": prices[0] if prices else None,
            "median_price_vnd": median,
            "max_price_vnd": prices[-1] if prices else None,
            "price_level": level,
            "has_voucher": bool(pr_live),
            "has_freeship": any(p["is_freeship"] for p in pr_live),
            "n_discounted_items": len(disc_items),
            "max_item_discount_pct": max((i["discount_pct"] for i in disc_items), default=None),
            "promo_summary": " ; ".join(p["title"] for p in pr_live)[:300],
            "url": r["url"],
            "menu_crawled": bool(m),
            "promo_crawled": rid in (raw.get("promos") or {}),
        }
        restaurants.append(row)
        nested.append({**row, "promotions": pr, "menu": menu})

    def write_csv(name, rows):
        if not rows:
            return
        with open(out / name, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write_csv("restaurants.csv", restaurants)
    write_csv("menu_items.csv", items)
    write_csv("promotions.csv", promos)
    (out / "dataset.json").write_text(
        json.dumps({"crawled_at": raw.get("crawled_at"), "origin": raw.get("origin"), "restaurants": nested},
                   ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    n_menu = sum(r["menu_crawled"] for r in restaurants)
    n_vou = sum(r["has_voucher"] for r in restaurants)
    n_free = sum(r["has_freeship"] for r in restaurants)
    n_desc = sum(i["has_description"] for i in items)
    n_area = sum(1 for r in restaurants if r["area"])
    n_closed = sum(r["open_status"] == "closed_at_crawl" for r in restaurants)
    n_nomenu = sum(r["open_status"] == "no_menu" for r in restaurants)
    n_noprice = sum(1 for i in items if i["price_flag"])
    n_expired = sum(1 for p in promos if p["is_expired"])
    n_promo_only = sum(1 for i in items if i["only_in_promo_section"])
    dists = [r["distance_km"] for r in restaurants if r["distance_km"] is not None]
    print(f"restaurants={len(restaurants)} menu_crawled={n_menu} items={len(items)} "
          f"promos={len(promos)} quán_có_voucher={n_vou} quán_có_freeship={n_free}")

    date = (raw.get("crawled_at") or "")[:10]
    card = f"""## Dataset · Quán ăn GrabFood quanh VinUni (dữ liệu thật)

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `search_restaurants`, `get_menu`, `check_constraints` · làm kho quán thật, không dùng dữ liệu giả |
| Từ đâu | trang công khai GrabFood VN (`food.grab.com/vn/vi/restaurants`), vị trí giao hàng đặt tại VinUni (Sảnh Thư Viện, Gia Lâm, Hà Nội). Đọc từ nội dung hiển thị trên trang, từng quán một, có nghỉ giữa các lần. Không dùng API nội bộ. |
| Xử lý những bước gì | lọc trùng quán · khử trùng món lặp ở nhóm "Ưu đãi hôm nay / Dành cho bạn" · tách giá gốc / giá giảm · tách voucher thành loại, % hoặc số tiền, đơn tối thiểu, giảm tối đa, hạn dùng · gắn mức giá (cheap < {CHEAP_MEDIAN // 1000}k ≤ mid ≤ {MID_MEDIAN // 1000}k < high theo giá món trung vị) · cờ giao nhanh (ETA ≤ {FAST_ETA_MIN} phút) · đoán khu vực từ tên quán · phân loại quán ăn / quán đồ uống (`main_type`) · bỏ giá < 1.000đ (dòng ghi chú bị đọc nhầm thành giá) · gắn cờ voucher hết hạn (script: `data/grab/normalize_grab.py`, kiểm tra: `data/grab/check_data.py`) |
| Số dòng / số đoạn | {len(restaurants)} quán ({n_menu} có menu) · {len(items)} món ({n_desc} món có mô tả) · {len(promos)} khuyến mãi ({n_vou} quán có voucher, {n_free} quán có giảm phí giao) |
| Phiên bản / ngày lấy | {date} (một lần lấy, giá và khuyến mãi đổi theo ngày) |
| Nhãn | thật (dữ liệu công khai của quán; không có dữ liệu cá nhân) |
| Giới hạn | chỉ quán Grab giao tới VinUni (xa nhất {max(dists) if dists else '?'} km, nên không phủ quán ngoài bán kính giao) · lệch về khu Vinhomes Ocean Park · menu và giá là ảnh chụp một thời điểm · {len(items) - n_desc} món không có mô tả nên không biết thành phần (xử lý như không an toàn khi lọc ăn chay / dị ứng) · không có phí giao thực tế và không có mã voucher gõ tay (Grab áp ưu đãi tự động) · `area` đoán từ tên quán, {len(restaurants) - n_area} quán để trống · ETA là ước tính của Grab lúc lấy · {n_closed} quán hiện "Closed" lúc lấy nên không có lịch mở cửa (`open_status=closed_at_crawl`) · {n_nomenu} quán không có menu (`no_menu`, bỏ khỏi tìm kiếm) · {n_noprice} món không có giá dùng được (thường là món chọn size mới biết giá) · {n_expired} khuyến mãi đã hết hạn (cờ `is_expired`; chỉ khuyến mãi còn hạn tính vào `has_voucher`) · {n_promo_only} món chỉ xuất hiện ở mục "Ưu đãi / Dành cho bạn" nên nhóm món có thể không chính xác |

**Lưu ý dùng lại:** dữ liệu lấy từ trang của bên thứ ba. File thô `grab_raw*.json` không commit (đã thêm vào `.gitignore`). Trong slide và báo cáo, ghi nguồn và ngày lấy; số trong slide truy về `restaurants.csv`, `menu_items.csv`, `promotions.csv`.
"""
    (out / "DATA_CARD_grab.md").write_text(card, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "grab_raw.json")
