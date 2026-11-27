"""Kiểm 3 công cụ + hàm ràng buộc trên data/restaurants.json. Chạy: python -m unittest discover -s tests -v
Chỉ dùng thư viện chuẩn. Không gọi model, không cần mạng."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "codebase"))
import tools  # noqa: E402


def find_dish(pred):
    for q in tools._data()["quan"]:
        for m in q["mon"]:
            if pred(m):
                return q, m
    raise AssertionError("không có món phù hợp")


class SearchTests(unittest.TestCase):
    def test_all(self):
        self.assertEqual(len(tools.search_restaurants()), 60)

    def test_distance(self):
        r = tools.search_restaurants(max_distance_km=1.5)
        self.assertTrue(0 < len(r) < 60)
        self.assertTrue(all(x["khoang_cach_km"] <= 1.5 for x in r))

    def test_unknown_name_is_empty(self):
        self.assertEqual(tools.search_restaurants(name="xyzabc"), [])

    def test_closed_shop_removed(self):
        q = next(x for x in tools._data()["quan"] if x.get("gio_mo"))
        for hhmm in ("03:00", "12:00", "23:30"):
            ids = {x["id"] for x in tools.search_restaurants(at_time=hhmm)}
            self.assertEqual(q["id"] in ids, tools.open_at(q, hhmm) is not False)


class MenuTests(unittest.TestCase):
    def test_menu_and_missing(self):
        self.assertGreater(len(tools.get_menu("Q01")), 0)
        self.assertEqual(tools.get_menu("Q999"), [])


class CheckTests(unittest.TestCase):
    def plan(self, q, dish_ids):
        return {"quan_id": q["id"], "chon": [{"nguoi": i, "mon_id": d} for i, d in enumerate(dish_ids, 1)]}

    def test_ok_plan(self):
        q, m = find_dish(lambda d: d["gia"] > 0)
        r = tools.check_constraints(self.plan(q, [m["id"]]), [{}])
        self.assertTrue(r["ok"])
        self.assertEqual(r["tong_tien"], m["gia"])

    def test_vegetarian_blocks_non_veg_and_unknown(self):
        q, m = find_dish(lambda d: d.get("chay") is not True)  # None (không rõ) cũng bị chặn
        r = tools.check_constraints(self.plan(q, [m["id"]]), [{"chay": True}])
        self.assertFalse(r["ok"])
        q2, m2 = find_dish(lambda d: d.get("chay") is True)
        self.assertTrue(tools.check_constraints(self.plan(q2, [m2["id"]]), [{"chay": True}])["ok"])

    def test_allergy_blocks_mentioned(self):
        q, m = find_dish(lambda d: d.get("co_nhac"))
        code = m["co_nhac"][0]
        self.assertFalse(tools.check_constraints(self.plan(q, [m["id"]]), [{"di_ung": [code]}])["ok"])

    def test_meat_avoid_and_wanted_type(self):
        q, m = find_dish(lambda d: d.get("thit") and d.get("loai") != "khac")
        self.assertFalse(tools.check_constraints(self.plan(q, [m["id"]]), [{"kieng": [m["thit"][0]]}])["ok"])
        self.assertTrue(tools.check_constraints(self.plan(q, [m["id"]]), [{"muon_loai": [m["loai"]]}])["ok"])
        other = next(c for c in tools.known_codes()["loai"] if c != m["loai"])
        self.assertFalse(tools.check_constraints(self.plan(q, [m["id"]]), [{"muon_loai": [other]}])["ok"])

    def test_budget_distance_and_missing_pick(self):
        q, m = find_dish(lambda d: d["gia"] > 0)
        p = self.plan(q, [m["id"]])
        self.assertFalse(tools.check_constraints(p, [{}], budget_total=m["gia"] - 1)["ok"])
        self.assertTrue(tools.check_constraints(p, [{}], budget_total=m["gia"])["ok"])
        self.assertFalse(tools.check_constraints(p, [{}], max_distance_km=q["khoang_cach_km"] - 0.01)["ok"])
        self.assertFalse(tools.check_constraints(p, [{}, {}])["ok"])  # người 2 chưa có món

    def test_unknown_restaurant_and_dish(self):
        self.assertFalse(tools.check_constraints({"quan_id": "Q999", "chon": []}, [{}])["ok"])
        q, _ = find_dish(lambda d: True)
        self.assertFalse(tools.check_constraints(self.plan(q, ["nope"]), [{}])["ok"])


if __name__ == "__main__":
    unittest.main()
