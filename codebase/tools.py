"""Công cụ của bài toán "chọn quán cho nhóm có nhiều yêu cầu khác nhau" — phần của Thu (Data & công cụ).

Dữ liệu: data/grab/*.csv (quán thật quanh VinUni lấy từ GrabFood, mô tả ở data/DATA_CARD.md,
cột ở data/SCHEMA.md). Chỉ dùng thư viện chuẩn.

Ba công cụ (khớp bảng công cụ ở spec.md §4). Cả ba chỉ ĐỌC dữ liệu, KHÔNG có tác động ra ngoài
(không đặt đơn, không thanh toán, không gửi tin):

  search_restaurants  AI dùng để thu hẹp ~250 quán xuống vài ứng viên
  get_menu            AI dùng để đọc menu của từng ứng viên rồi tự quyết quán nào, món nào cho ai
  check_constraints   CODE THUẦN (không gọi AI): kiểm lại đề xuất của AI theo ràng buộc của từng người

Nguyên tắc an toàn đã cài trong code:
  * Món không rõ thành phần (không có mô tả) mà người đó có yêu cầu ăn chay / dị ứng → bị tính là vi phạm.
  * Code chỉ bắt được thành phần được NÊU trong tên món và mô tả. Món có mô tả nhưng không liệt kê thành phần
    vẫn có thể chứa thứ cần tránh → check_constraints luôn kèm cảnh báo "chưa xác nhận với quán".
  * Giá không rõ (món chọn size mới biết giá) không được tính là rẻ → vi phạm.
  * Không tính dinh dưỡng, không tư vấn sức khoẻ.
"""
import csv
import re
import unicodedata
from pathlib import Path

from tracing import tool, TOOLS  # noqa: F401

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "grab"
DESC_MAX = 300  # cắt mô tả món trả cho AI, đủ để đọc thành phần mà không tốn token

# Từ khoá thịt / cá / hải sản dùng cho "ăn chay" (trứng, sữa vẫn được coi là chay; nước mắm không xét).
# So khớp CÓ DẤU: "cá" khác "cà" (cà phê). Thêm từ khoá ở đây nếu gặp món lọt.
MEAT_KEYWORDS = [
    "thịt", "bò", "gà", "heo", "lợn", "vịt", "ngan", "dê", "cừu", "sườn", "ba chỉ", "ba rọi", "nạc", "giò", "chả",
    "nem", "xúc xích", "lạp xưởng", "jambon", "patê", "gan", "lòng", "tiết", "dồi", "thăn", "bắp bò", "gầu",
    "cá", "tôm", "mực", "cua", "ghẹ", "ốc", "hến", "nghêu", "sò", "hàu", "hải sản", "tép", "ruốc", "bạch tuộc",
    "bít tết", "steak", "bacon", "ham", "pepperoni", "salami", "chicken", "beef", "pork", "shrimp", "sausage",
    "salmon", "tuna", "sashimi", "kebab", "gyros", "nuggets", "nugget",
]
# Tên món có các từ này (và không dính từ khoá thịt) thì tạm tin là món chay dù không có mô tả.
VEG_MARKERS = ["chay", "vegan", "vegetarian"]

_DB = {}


# ---------- tiện ích văn bản ----------

def _nfc(s):
    return unicodedata.normalize("NFC", s or "")


def _strip_accents(s):
    s = unicodedata.normalize("NFD", (s or "").lower().replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _has_accent(s):
    return _strip_accents(s) != _nfc(s).lower().replace("đ", "d")


def _contains(text, kw, accent_sensitive=None):
    """Khớp nguyên từ (ranh giới theo âm tiết). Từ khoá có dấu → khớp có dấu ("cá" ≠ "cà phê").
    Từ khoá không dấu → khớp không phân biệt dấu (bảo thủ: chặn dư còn hơn lọt)."""
    kw = _nfc(kw).lower().strip()
    if not kw:
        return False
    if accent_sensitive is None:
        accent_sensitive = _has_accent(kw)
    if accent_sensitive:
        hay, needle = _nfc(text).lower(), kw
    else:
        hay, needle = _strip_accents(text), _strip_accents(kw)
    return re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", hay) is not None


def _loose(text, kw):
    """Khớp để TÌM KIẾM theo nguyên từ: gõ có dấu thì khớp có dấu ("phở" không dính "phô mai"),
    gõ không dấu thì khớp mọi dấu ("pho"). Không khớp chuỗi con ("com" không dính "combo")."""
    return _contains(text, kw)


def _num(x, cast=float):
    try:
        return cast(x) if x not in ("", None) else None
    except ValueError:
        return None


def _bool(x):
    return str(x).strip().lower() == "true"


# ---------- nạp dữ liệu ----------

def _read(name):
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            "Thiếu %s. Chạy: python data/grab/normalize_grab.py data/grab/grab_raw_final.json" % path)
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _db():
    if _DB:
        return _DB
    restaurants, items, promos = {}, {}, {}
    for r in _read("restaurants.csv"):
        restaurants[r["restaurant_id"]] = {
            "restaurant_id": r["restaurant_id"], "name": r["name"], "area": r["area"], "cuisine": r["cuisine"],
            "main_type": r["main_type"], "distance_km": _num(r["distance_km"]), "eta_min": _num(r["eta_min"], int),
            "rating": _num(r["rating"]), "price_level": r["price_level"],
            "median_price_vnd": _num(r["median_price_vnd"], int), "has_voucher": _bool(r["has_voucher"]),
            "has_freeship": _bool(r["has_freeship"]), "open_status": r["open_status"],
            "open_hours": r["open_hours"], "n_items": _num(r["n_items"], int) or 0, "url": r["url"],
        }
    for i in _read("menu_items.csv"):
        items.setdefault(i["restaurant_id"], []).append({
            "item_id": i["item_id"], "name": i["item_name"], "category": i["category"],
            "price_vnd": _num(i["price_vnd"], int), "original_price_vnd": _num(i["original_price_vnd"], int),
            "discount_pct": _num(i["discount_pct"], int), "description": i["description"],
        })
    for p in _read("promotions.csv"):
        if _bool(p["is_expired"]):
            continue
        promos.setdefault(p["restaurant_id"], []).append({
            "type": p["type"], "title": p["title"], "discount_pct": _num(p["discount_pct"], int),
            "discount_vnd": _num(p["discount_vnd"], int), "min_order_vnd": _num(p["min_order_vnd"], int),
            "max_discount_vnd": _num(p["max_discount_vnd"], int), "valid_to": p["valid_to"],
        })
    _DB.update(restaurants=restaurants, items=items, promos=promos)
    return _DB


def _summary(r):
    keys = ("restaurant_id", "name", "area", "cuisine", "distance_km", "eta_min", "rating", "price_level",
            "median_price_vnd", "has_voucher", "has_freeship", "open_status", "open_hours")
    return {k: r[k] for k in keys}


# ---------- công cụ 1 ----------

@tool
def search_restaurants(max_distance_km: float = None, max_eta_min: int = None, price_level: str = None,
                       cuisine_keywords: list = None, dish_keywords: list = None, min_rating: float = None,
                       need_freeship: bool = False, need_voucher: bool = False, kind: str = "food",
                       limit: int = 10) -> dict:
    """search_restaurants — thu hẹp danh sách quán theo điều kiện của cả nhóm.
    Input: max_distance_km (km từ VinUni) · max_eta_min (phút giao tối đa) · price_level ("cheap"|"mid"|"high",
    theo giá món trung vị) · cuisine_keywords (loại quán, vd ["bún","cơm"]) · dish_keywords (món muốn ăn, quán
    phải có ít nhất 1 món khớp tên, vd ["phở","pizza"]) · min_rating · need_freeship / need_voucher ·
    kind ("food"|"drink"|"any", mặc định "food") · limit (≤30).
    Output: {"total_matches": số quán khớp, "results": [{restaurant_id, name, area, cuisine, distance_km, eta_min,
    rating, price_level, median_price_vnd, has_voucher, has_freeship, open_status, open_hours,
    matched_keywords, n_matched_items}]} — xếp quán khớp nhiều từ khoá món nhất, rồi gần nhất.
    Quán không có menu bị loại. open_status="closed_at_crawl" nghĩa là Grab hiện "Closed" lúc lấy dữ liệu,
    không có lịch mở cửa. Không khớp quán nào → results rỗng (AI phải nói "không có", không bịa).
    Tác động ra ngoài: không."""
    db = _db()
    limit = max(1, min(int(limit or 10), 30))
    kws = [k for k in (dish_keywords or []) if k and k.strip()]
    out = []
    for rid, r in db["restaurants"].items():
        if r["open_status"] == "no_menu" or not db["items"].get(rid):
            continue
        if kind in ("food", "drink") and r["main_type"] != kind:
            continue
        if max_distance_km is not None and (r["distance_km"] is None or r["distance_km"] > max_distance_km):
            continue
        if max_eta_min is not None and (r["eta_min"] is None or r["eta_min"] > max_eta_min):
            continue
        if price_level and r["price_level"] != price_level:
            continue
        if min_rating is not None and (r["rating"] is None or r["rating"] < min_rating):
            continue
        if need_freeship and not r["has_freeship"]:
            continue
        if need_voucher and not r["has_voucher"]:
            continue
        if cuisine_keywords and not any(_loose(r["cuisine"] + " " + r["name"], k) for k in cuisine_keywords if k):
            continue
        matched, n_items = [], 0
        if kws:
            for k in kws:
                hits = sum(1 for it in db["items"][rid] if _loose(it["name"], k))
                if hits:
                    matched.append(k)
                    n_items += hits
            if not matched:
                continue
        out.append({**_summary(r), "matched_keywords": matched, "n_matched_items": n_items})
    out.sort(key=lambda x: (-len(x["matched_keywords"]), x["distance_km"] if x["distance_km"] is not None else 99,
                            -(x["rating"] or 0)))
    return {"total_matches": len(out), "results": out[:limit]}


# ---------- công cụ 2 ----------

@tool
def get_menu(restaurant_id: str, query: str = None, max_price_vnd: int = None, limit: int = 80) -> dict:
    """get_menu — đọc menu và khuyến mãi của MỘT quán để AI tự chọn món cho từng người.
    Input: restaurant_id (lấy từ search_restaurants) · query (lọc theo tên/nhóm/mô tả món, nhiều từ cách nhau
    bằng dấu phẩy = hoặc) · max_price_vnd · limit (≤150).
    Output: {"restaurant": {... + promotions: [{type, title, min_order_vnd, max_discount_vnd, valid_to}]},
    "n_items_total", "n_items_returned", "items": [{item_id, name, category, price_vnd, original_price_vnd,
    discount_pct, description}]}. price_vnd=None nghĩa là giá không rõ. description rỗng nghĩa là quán không
    ghi thành phần. restaurant_id không tồn tại → {"error": ...} (AI phải nói không có, không đoán).
    Tác động ra ngoài: không."""
    db = _db()
    r = db["restaurants"].get(restaurant_id)
    if not r:
        return {"error": "Không có quán '%s' trong dữ liệu." % restaurant_id}
    limit = max(1, min(int(limit or 80), 150))
    qs = [q.strip() for q in (query or "").split(",") if q.strip()]
    items = db["items"].get(restaurant_id, [])
    sel = []
    for it in items:
        if max_price_vnd is not None and (it["price_vnd"] is None or it["price_vnd"] > max_price_vnd):
            continue
        if qs and not any(_loose(it["name"] + " " + it["category"] + " " + it["description"], q) for q in qs):
            continue
        sel.append({**it, "description": it["description"][:DESC_MAX]})
    promos = [{k: p[k] for k in ("type", "title", "min_order_vnd", "max_discount_vnd", "valid_to")}
              for p in db["promos"].get(restaurant_id, [])]
    return {"restaurant": {**_summary(r), "promotions": promos}, "n_items_total": len(items),
            "n_items_returned": len(sel[:limit]), "items": sel[:limit]}


# ---------- công cụ 3 ----------

def _person_text(it):
    return "%s %s" % (it["name"], it["description"])


def _check_item_for_person(it, p, violations, name):
    """Kiểm 1 món với yêu cầu ăn uống của 1 người. Trả True nếu phát hiện vi phạm."""
    text = _person_text(it)
    bad = False
    for kw in p.get("avoid") or []:
        if _contains(text, kw):
            violations.append({"person": name, "rule": "avoided_ingredient", "item_id": it["item_id"],
                               "detail": "'%s' có '%s' (nêu trong tên/mô tả)" % (it["name"], kw)})
            bad = True
    if p.get("vegetarian"):
        hit = next((m for m in MEAT_KEYWORDS if _contains(text, m, accent_sensitive=True)), None)
        if hit:
            violations.append({"person": name, "rule": "not_vegetarian", "item_id": it["item_id"],
                               "detail": "'%s' có '%s' (nêu trong tên/mô tả)" % (it["name"], hit)})
            bad = True
    needs_known = bool(p.get("avoid")) or bool(p.get("vegetarian"))
    if needs_known and not (it["description"] or "").strip():
        veg_ok = p.get("vegetarian") and not p.get("avoid") and any(_contains(it["name"], m) for m in VEG_MARKERS)
        if not veg_ok and not bad:
            violations.append({"person": name, "rule": "unknown_ingredients", "item_id": it["item_id"],
                               "detail": "'%s' không có mô tả thành phần → coi như không an toàn" % it["name"]})
            bad = True
    return bad


@tool
def check_constraints(restaurant_id: str, assignments: list, people: list, group: dict = None) -> dict:
    """check_constraints — CODE THUẦN, không gọi AI: kiểm lại đề xuất "quán này, món này cho người này".
    Input:
      restaurant_id: quán AI đề xuất.
      assignments: [{"person": "An", "item_ids": ["<item_id>", ...]}] (cũng nhận "item_id": "...").
      people: [{"name": "An", "budget_vnd": 80000 (tổng tiền món của riêng người đó), "avoid": ["tôm","đậu phộng"]
                (dị ứng/kiêng), "vegetarian": true/false, "wants": ["bún"] (món muốn ăn; ít nhất 1 món gán
                cho người đó phải khớp)}].
      group: {"max_distance_km", "max_eta_min", "max_total_vnd", "need_freeship"} (tuỳ chọn).
    Output: {"ok": bool (True khi không có vi phạm), "restaurant": {name, distance_km, eta_min},
      "total_vnd", "per_person": {tên: {"items": [tên món], "total_vnd"}},
      "violations": [{person, rule, item_id, detail}], "warnings": [str]}.
      rule ∈ unknown_restaurant · unknown_person · no_item · unknown_item · unknown_price · over_budget ·
      avoided_ingredient · not_vegetarian · unknown_ingredients · not_wanted · too_far · too_slow ·
      over_total · no_freeship. Có dấu hiệu lọt thành phần thì luôn có warning "chưa xác nhận với quán".
    Tác động ra ngoài: không (chỉ tính toán, không đặt đơn)."""
    db = _db()
    r = db["restaurants"].get(restaurant_id)
    if not r:
        return {"ok": False, "violations": [{"person": None, "rule": "unknown_restaurant", "item_id": None,
                                             "detail": "Không có quán '%s' trong dữ liệu." % restaurant_id}],
                "warnings": [], "total_vnd": 0, "per_person": {}}
    menu = {it["item_id"]: it for it in db["items"].get(restaurant_id, [])}
    ppl = {p["name"]: p for p in (people or []) if p.get("name")}
    violations, warnings, per_person = [], [], {}

    given = {}
    for a in assignments or []:
        name = a.get("person")
        ids = list(a.get("item_ids") or ([a["item_id"]] if a.get("item_id") else []))
        given.setdefault(name, []).extend(ids)

    for name in given:
        if name not in ppl:
            violations.append({"person": name, "rule": "unknown_person", "item_id": None,
                               "detail": "'%s' không có trong danh sách người của nhóm" % name})

    total = 0
    for name, p in ppl.items():
        ids = given.get(name, [])
        if not ids:
            violations.append({"person": name, "rule": "no_item", "item_id": None,
                               "detail": "chưa gán món nào cho %s" % name})
            continue
        subtotal, names, unpriced, dietary = 0, [], False, bool(p.get("avoid")) or bool(p.get("vegetarian"))
        for iid in ids:
            it = menu.get(iid)
            if not it:
                violations.append({"person": name, "rule": "unknown_item", "item_id": iid,
                                   "detail": "món '%s' không có trong menu của quán này" % iid})
                continue
            names.append(it["name"])
            if it["price_vnd"] is None:
                unpriced = True
                violations.append({"person": name, "rule": "unknown_price", "item_id": iid,
                                   "detail": "'%s' không có giá rõ (chọn size/tuỳ chọn mới biết giá)" % it["name"]})
            else:
                subtotal += it["price_vnd"]
            _check_item_for_person(it, p, violations, name)
        per_person[name] = {"items": names, "total_vnd": subtotal}
        total += subtotal
        budget = p.get("budget_vnd")
        if budget is not None and subtotal > budget and not unpriced:
            violations.append({"person": name, "rule": "over_budget", "item_id": None,
                               "detail": "%s: %d đ > ngân sách %d đ" % (name, subtotal, budget)})
        wants = [w for w in (p.get("wants") or []) if w]
        if wants and not any(_contains(menu[i]["name"], w) for i in ids if i in menu for w in wants):
            violations.append({"person": name, "rule": "not_wanted", "item_id": None,
                               "detail": "món gán cho %s không khớp món muốn ăn: %s" % (name, ", ".join(wants))})
        if dietary:
            warnings.append("%s: thành phần chỉ suy từ tên món và mô tả của quán, chưa xác nhận với quán — "
                            "nên hỏi quán trước khi đặt." % name)

    g = group or {}
    if g.get("max_distance_km") is not None and (r["distance_km"] is None or r["distance_km"] > g["max_distance_km"]):
        violations.append({"person": None, "rule": "too_far", "item_id": None,
                           "detail": "quán cách %s km > %s km" % (r["distance_km"], g["max_distance_km"])})
    if g.get("max_eta_min") is not None and (r["eta_min"] is None or r["eta_min"] > g["max_eta_min"]):
        violations.append({"person": None, "rule": "too_slow", "item_id": None,
                           "detail": "giao ~%s phút > %s phút" % (r["eta_min"], g["max_eta_min"])})
    if g.get("max_total_vnd") is not None and total > g["max_total_vnd"]:
        violations.append({"person": None, "rule": "over_total", "item_id": None,
                           "detail": "tổng %d đ > %d đ" % (total, g["max_total_vnd"])})
    if g.get("need_freeship") and not r["has_freeship"]:
        violations.append({"person": None, "rule": "no_freeship", "item_id": None,
                           "detail": "quán không có ưu đãi giảm phí giao còn hạn"})
    if r["open_status"] == "closed_at_crawl":
        warnings.append("Quán hiện 'Closed' lúc lấy dữ liệu và không có lịch mở cửa — nên kiểm tra quán còn mở không.")

    return {"ok": not violations, "restaurant": {"name": r["name"], "distance_km": r["distance_km"],
                                                  "eta_min": r["eta_min"]},
            "total_vnd": total, "per_person": per_person, "violations": violations, "warnings": warnings}


# ---------- tương thích với agent.py mẫu của khung ----------

@tool
def search_example(query: str) -> list:
    """(tạm — chỉ để agent.py mẫu của khung còn chạy tới khi Minh viết luồng thật; xoá khi không còn dùng)
    Input: câu hỏi (str). Output: danh sách {"code", "text"} từ search_restaurants. Tác động ra ngoài: không."""
    res = search_restaurants(dish_keywords=[w for w in re.split(r"\W+", query or "") if len(w) > 2][:3], limit=5)
    return [{"code": x["restaurant_id"], "text": "%s · %s · %s km" % (x["name"], x["cuisine"], x["distance_km"])}
            for x in res["results"]]
