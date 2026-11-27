"""Kiểm tra chất lượng dữ liệu GrabFood sau khi chuẩn hoá.

Dùng:  python data/grab/check_data.py            (chạy trong repo, đọc 3 CSV cạnh file này)
Thoát mã 1 nếu có lỗi nặng (để dùng trong CI / make check).
"""
import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent


def load(name):
    with open(HERE / name, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    rs, items, promos = load("restaurants.csv"), load("menu_items.csv"), load("promotions.csv")
    errors, warns = [], []

    ids = [r["restaurant_id"] for r in rs]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    if dup:
        errors.append(f"trùng restaurant_id: {dup[:5]}")

    no_menu = [r["name"] for r in rs if r["menu_crawled"] != "True"]
    if no_menu:
        errors.append(f"{len(no_menu)} quán chưa có menu: {no_menu[:5]}")
    empty_menu = [r["name"] for r in rs if r["menu_crawled"] == "True" and r["n_items"] == "0"]
    if empty_menu:
        warns.append(f"{len(empty_menu)} quán có menu rỗng (đóng cửa/lỗi tải?): {empty_menu[:5]}")
    no_promo = [r["name"] for r in rs if r["promo_crawled"] != "True"]
    if no_promo:
        errors.append(f"{len(no_promo)} quán chưa lấy voucher: {no_promo[:3]}")

    rid_set = set(ids)
    orphan = [i for i in items if i["restaurant_id"] not in rid_set]
    if orphan:
        errors.append(f"{len(orphan)} món trỏ tới quán không tồn tại")

    item_ids = [i["item_id"] for i in items]
    if len(item_ids) != len(set(item_ids)):
        errors.append("item_id bị trùng")

    no_price = [i for i in items if not num(i["price_vnd"])]
    if no_price:
        warns.append(f"{len(no_price)} món không có giá hoặc giá 0 (VD: {no_price[0]['item_name']})")
    prices = [num(i["price_vnd"]) for i in items if num(i["price_vnd"])]
    low = [i for i in items if num(i["price_vnd"]) and num(i["price_vnd"]) < 1000]
    high = [i for i in items if num(i["price_vnd"]) and num(i["price_vnd"]) > 2_000_000]
    if low:
        warns.append(f"{len(low)} món giá < 1.000đ (VD: {low[0]['item_name']} {low[0]['price_vnd']})")
    if high:
        warns.append(f"{len(high)} món giá > 2 triệu (VD: {high[0]['item_name']} {high[0]['price_vnd']})")
    bad_disc = [i for i in items if num(i["original_price_vnd"]) and num(i["price_vnd"])
                and num(i["original_price_vnd"]) < num(i["price_vnd"])]
    if bad_disc:
        errors.append(f"{len(bad_disc)} món có giá gốc < giá bán")

    far = [r["name"] for r in rs if num(r["distance_km"]) and num(r["distance_km"]) > 7]
    if far:
        warns.append(f"{len(far)} quán xa hơn 7 km")
    no_dist = [r["name"] for r in rs if num(r["distance_km"]) is None]
    if no_dist:
        warns.append(f"{len(no_dist)} quán thiếu khoảng cách: {no_dist[:3]}")

    desc = sum(1 for i in items if i["has_description"] == "True")
    print(f"quán: {len(rs)} | món: {len(items)} | khuyến mãi: {len(promos)}")
    print(f"món có mô tả: {desc}/{len(items)} ({100 * desc // max(1, len(items))}%)")
    if prices:
        prices.sort()
        print(f"giá món: min {prices[0]:,.0f} · trung vị {prices[len(prices) // 2]:,.0f} · max {prices[-1]:,.0f}")
    print("mức giá quán:", dict(Counter(r["price_level"] or "?" for r in rs)))
    print(f"giao nhanh (≤20p): {sum(r['is_fast'] == 'True' for r in rs)} · "
          f"có voucher: {sum(r['has_voucher'] == 'True' for r in rs)} · "
          f"có giảm phí giao: {sum(r['has_freeship'] == 'True' for r in rs)}")
    print("loại khuyến mãi:", dict(Counter(p["type"] for p in promos)))
    print("trạng thái quán:", dict(Counter(r["open_status"] for r in rs)),
          "· loại quán:", dict(Counter(r["main_type"] for r in rs)))
    expired = sum(1 for p in promos if p["is_expired"] == "True")
    if expired:
        warns.append(f"{expired} khuyến mãi đã hết hạn (đã loại khỏi has_voucher)")
    leftover = [p for p in promos if p["title"].strip().lower() == "tận hưởng ưu đãi"]
    if leftover:
        errors.append(f"{len(leftover)} khuyến mãi còn tiêu đề 'Tận hưởng ưu đãi' (chưa tách nội dung)")
    flagged = Counter(i["price_flag"] for i in items if i["price_flag"])
    if flagged:
        warns.append(f"món có cờ giá: {dict(flagged)}")
    for w in warns:
        print("⚠️ ", w)
    for e in errors:
        print("❌", e)
    if not errors:
        print("✅ không có lỗi nặng")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
