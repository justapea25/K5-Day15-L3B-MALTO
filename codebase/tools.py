"""Công cụ của bài toán — chọn quán cho nhóm có nhiều yêu cầu.

Phụ trách: Thu (data + công cụ). Bản đầu do Minh viết theo hợp đồng để agent chạy được.
Mỗi công cụ ghi đủ: tên · input · output · có tác động ra ngoài không. Khớp bảng ở spec.md §4.
Tất cả công cụ CHỈ ĐỌC, không tác động ra ngoài (không đặt đơn, không gửi tin).

Nguyên tắc an toàn cài trong code (không để model quyết):
  - Món không rõ thành phần (di_ung = null) → coi như KHÔNG an toàn với người có dị ứng.
  - Món không rõ chay hay không (chay = null) → coi như KHÔNG chay.
  - Món không rõ loại thịt (thit = null) → coi như KHÔNG an toàn với người kiêng thịt.
  - Tiền, khoảng cách tính bằng code, không để model nhẩm.
"""
import json
import os

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
    for q in _data()["quan"]:
        if q["id"] == rid:
            return q
    return None


def known_codes():
    """Các mã hợp lệ (dị ứng, thịt, loại món) — agent dùng để chuẩn hoá output của model. Không phải công cụ."""
    d = _data()
    return {"di_ung": d["ma_di_ung"], "thit": d["ma_thit"], "loai": d["ma_loai"]}


def dish_safe_for(dish, person):
    """True nếu món an toàn và hợp với một người. Code thuần, không gọi AI.
    person: {"chay": bool, "di_ung": [mã], "kieng": [mã thịt], "muon": [mã loại]}"""
    if person.get("chay") and dish.get("chay") is not True:
        return False
    allergies = set(person.get("di_ung") or [])
    if allergies:
        if dish.get("di_ung") is None or allergies & set(dish["di_ung"]):
            return False
    avoid = set(person.get("kieng") or [])
    if avoid:
        if dish.get("thit") is None or avoid & set(dish["thit"]):
            return False
    wants = set(person.get("muon") or [])
    if wants and dish.get("loai") not in wants:
        return False
    return True


@tool
def search_restaurants(max_distance_km=None, name=None) -> list:
    """search_restaurants — tìm quán trong dữ liệu.
    Input: max_distance_km (số km tối đa, None = không giới hạn) · name (tên quán người dùng nhắc, None = mọi quán).
    Output: danh sách {"id", "ten", "khoang_cach_km", "phi_ship"}; không có quán nào thì [].
    Tác động ra ngoài: không (chỉ đọc)."""
    out = []
    for q in _data()["quan"]:
        if max_distance_km is not None and q["khoang_cach_km"] > max_distance_km:
            continue
        if name and name.strip().lower() not in q["ten"].lower():
            continue
        out.append({k: q[k] for k in ("id", "ten", "khoang_cach_km", "phi_ship")})
    return out


@tool
def get_menu(restaurant_id: str) -> list:
    """get_menu — lấy menu một quán.
    Input: restaurant_id (str, vd "Q01").
    Output: danh sách món {"id", "ten", "gia", "loai", "mo_ta", "chay", "di_ung", "thit"}; quán không có thì [].
    Tác động ra ngoài: không (chỉ đọc)."""
    q = _restaurant(restaurant_id)
    return list(q["mon"]) if q else []


@tool
def check_constraints(plan: dict, people: list, budget_total=None, max_distance_km=None) -> dict:
    """check_constraints — kiểm một phương án bằng CODE (không phải AI).
    Input: plan {"quan_id", "chon": [{"nguoi": số thứ tự, "mon_id"}]} · people (danh sách ràng buộc từng người)
           · budget_total (VND, tổng cả phí ship; None = không giới hạn) · max_distance_km.
    Output: {"ok": bool, "vi_pham": [lý do], "tong_tien": int, "phi_ship": int}.
    Tác động ra ngoài: không (chỉ đọc, chỉ tính)."""
    errors = []
    q = _restaurant(plan.get("quan_id"))
    if not q:
        return {"ok": False, "vi_pham": ["quán %r không có trong dữ liệu" % plan.get("quan_id")], "tong_tien": 0, "phi_ship": 0}
    if max_distance_km is not None and q["khoang_cach_km"] > max_distance_km:
        errors.append("quán cách %.1f km, quá %.1f km" % (q["khoang_cach_km"], max_distance_km))
    menu = {m["id"]: m for m in q["mon"]}
    picks = {c.get("nguoi"): c.get("mon_id") for c in plan.get("chon", [])}
    total = 0
    for i, person in enumerate(people, 1):
        dish = menu.get(picks.get(i))
        if dish is None:
            errors.append("người %d chưa có món, hoặc món không có trong menu quán" % i)
            continue
        if not dish_safe_for(dish, person):
            errors.append("món %s không hợp với người %d" % (dish["ten"], i))
        total += dish["gia"]
    total += q["phi_ship"]
    if budget_total is not None and total > budget_total:
        errors.append("tổng %d vượt ngân sách %d" % (total, budget_total))
    return {"ok": not errors, "vi_pham": errors, "tong_tien": total, "phi_ship": q["phi_ship"]}
