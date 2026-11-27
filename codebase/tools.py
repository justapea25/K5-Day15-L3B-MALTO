"""Công cụ của bài toán — chọn quán và món hợp với cả nhóm. Phụ trách: Thu (data + công cụ), Minh (bản đầu).

Dữ liệu: data/restaurants.json — quán dựng giả (synthetic, seed 42) theo phân bố đo từ menu GrabFood; xem data/DATA_CARD.md.
Mỗi công cụ ghi đủ: tên · input · output · có tác động ra ngoài không. Khớp bảng ở spec.md §4.
Tất cả công cụ CHỈ ĐỌC, không tác động ra ngoài (không đặt đơn, không gửi tin).

Quy tắc trong code (không để model quyết):
  - Ăn chay: chỉ món có chay = true (tên / nhóm món ghi "chay"). Không rõ = không chay.
  - Dị ứng (phần phụ): loại món có NHẮC chất đó trong tên / mô tả. Món không ghi mô tả vẫn có thể gợi ý
    nhưng phải kèm cảnh báo "chưa rõ thành phần, hỏi quán" — data không có thành phần đầy đủ.
  - Kiêng thịt: loại món có nhắc loại thịt đó.
  - Muốn ăn loại món (bún, phở, cơm…): món phải đúng loại.
  - Giờ mở cửa: chỉ lọc khi người dùng nói giờ VÀ quán có ghi giờ; quán không ghi giờ → giữ, kèm cảnh báo.
  - Tiền, khoảng cách tính bằng code. Data không có phí ship → tổng là tiền món, chưa gồm ship.
"""
import json
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "restaurants.json")
_DATA = None


def _data():
    global _DATA
    if _DATA is None:
        with open(DATA_PATH, encoding="utf-8") as f:
            _DATA = json.load(f)
    return _DATA


def _restaurant(rid):
    return next((q for q in _data()["quan"] if q["id"] == rid), None)


def known_codes():
    """Các mã hợp lệ (dị ứng, thịt, loại món) — agent dùng để chuẩn hoá output của model. Không phải công cụ."""
    d = _data()
    return {"di_ung": d["ma_di_ung"], "thit": d["ma_thit"], "loai": d["ma_loai"]}


def _minutes(hhmm):
    m = re.match(r"^(\d{1,2}):(\d{2})$", (hhmm or "").strip())
    return int(m.group(1)) * 60 + int(m.group(2)) if m else None


def open_at(q, hhmm):
    """True / False nếu biết; None nếu quán không ghi giờ hoặc không có giờ để so."""
    t = _minutes(hhmm)
    if t is None or not q.get("gio_mo"):
        return None
    for span in q["gio_mo"].split():
        a, _, b = span.partition("-")
        lo, hi = _minutes(a), _minutes(b)
        if lo is not None and hi is not None and lo <= t <= hi:
            return True
    return False


def norm(text):
    """Chữ thường, bỏ dấu, bỏ ký tự lạ — để "bun cha" khớp "Bún chả". Không phải công cụ."""
    t = unicodedata.normalize("NFD", (text or "").lower()).replace("đ", "d")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()


def match_level(dish, want):
    """Mức khớp món với món cụ thể người dùng nói: 2 = đúng món (mọi chữ của "want" có trong tên món), 0 = không.
    Không phải công cụ — code dùng để gắn nhãn "đúng món" / "gần giống"."""
    w = norm(want)
    return 2 if w and all(x in norm(dish["ten"]) for x in w) else 0


def dish_ok_for(dish, person):
    """True nếu món hợp với ràng buộc CỨNG của một người. Code thuần, không gọi AI.
    person: {"chay": bool, "di_ung": [mã], "kieng": [mã thịt], "muon_loai": [mã loại], "ngan_sach_rieng": VND, "mon": tên}"""
    if person.get("chay") and dish.get("chay") is not True:
        return False
    if set(person.get("di_ung") or []) & set(dish.get("co_nhac") or []):
        return False
    if set(person.get("kieng") or []) & set(dish.get("thit") or []):
        return False
    wants = set(person.get("muon_loai") or [])
    if wants and dish.get("loai") not in wants:
        return False
    cap = person.get("ngan_sach_rieng")
    if cap and dish["gia"] > cap:           # ngân sách riêng của suất này
        return False
    if person.get("mon") and not wants and match_level(dish, person["mon"]) < 2:
        return False                         # nói món cụ thể mà không rõ loại → chỉ nhận đúng món
    return True


@tool
def search_restaurants(max_distance_km=None, name=None, at_time=None) -> list:
    """search_restaurants — tìm quán trong dữ liệu.
    Input: max_distance_km (km tối đa, None = không giới hạn) · name (tên quán người dùng nhắc, None = mọi quán)
           · at_time ("HH:MM", None = không lọc giờ).
    Output: danh sách {"id", "ten", "khoang_cach_km", "danh_gia", "so_danh_gia", "gio_mo", "mo_cua"} — mo_cua True/False/None (không rõ).
            Quán chắc chắn đóng cửa lúc at_time bị loại. Không có quán nào thì [].
    Tác động ra ngoài: không (chỉ đọc)."""
    out = []
    for q in _data()["quan"]:
        if max_distance_km is not None and q["khoang_cach_km"] > max_distance_km:
            continue
        if name and name.strip().lower() not in q["ten"].lower():
            continue
        is_open = open_at(q, at_time)
        if is_open is False:
            continue
        out.append({"id": q["id"], "ten": q["ten"], "khoang_cach_km": q["khoang_cach_km"],
                    "danh_gia": q.get("danh_gia"), "so_danh_gia": q.get("so_danh_gia"), "muc_gia": q.get("muc_gia"),
                    "gio_mo": q.get("gio_mo"), "mo_cua": is_open})
    return out


@tool
def get_menu(restaurant_id: str) -> list:
    """get_menu — lấy menu món chính của một quán.
    Input: restaurant_id (str, vd "Q01").
    Output: danh sách món {"id", "ten", "gia", "loai", "nhom", "mo_ta", "chay", "co_nhac", "thit", "ghi_thanh_phan"};
            quán không có thì [].
    Tác động ra ngoài: không (chỉ đọc)."""
    q = _restaurant(restaurant_id)
    return list(q["mon"]) if q else []


@tool
def check_constraints(plan: dict, people: list, budget_total=None, max_distance_km=None, at_time=None) -> dict:
    """check_constraints — kiểm một phương án bằng CODE (không phải AI).
    Input: plan {"quan_id", "chon": [{"nguoi": số thứ tự, "mon_id"}]} · people (ràng buộc từng người)
           · budget_total (VND, None = không giới hạn) · max_distance_km · at_time ("HH:MM" hoặc None).
    Output: {"ok": bool, "vi_pham": [lý do], "tong_tien": int}.
    Tác động ra ngoài: không (chỉ đọc, chỉ tính)."""
    errors = []
    q = _restaurant((plan or {}).get("quan_id"))
    if not q:
        return {"ok": False, "vi_pham": ["quán %r không có trong dữ liệu" % (plan or {}).get("quan_id")], "tong_tien": 0}
    if max_distance_km is not None and q["khoang_cach_km"] > max_distance_km:
        errors.append("quán cách %.1f km, quá %.1f km" % (q["khoang_cach_km"], max_distance_km))
    if open_at(q, at_time) is False:
        errors.append("quán đóng cửa lúc %s" % at_time)
    menu = {m["id"]: m for m in q["mon"]}
    picks = {c.get("nguoi"): c.get("mon_id") for c in plan.get("chon", [])}
    total = 0
    for i, person in enumerate(people, 1):
        dish = menu.get(picks.get(i))
        if dish is None:
            errors.append("người %d chưa có món, hoặc món không có trong menu quán" % i)
            continue
        if not dish_ok_for(dish, person):
            errors.append("món %s không hợp với người %d" % (dish["ten"], i))
        total += dish["gia"]
    if budget_total is not None and total > budget_total:
        errors.append("tổng %d vượt ngân sách %d" % (total, budget_total))
    return {"ok": not errors, "vi_pham": errors, "tong_tien": total}
