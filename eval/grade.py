"""Chấm tự động cột `pass` cho eval/run-N.csv — 3 metric grader "code" trong eval/metric_spec.yaml.

Chạy:  python eval/grade.py eval/run-1.csv            # điền cột pass + ghi_chu, in bảng kết quả
       python eval/grade.py eval/run-1.csv --dry      # chỉ in, không ghi file
Sau đó: python run.py score eval/run-1.csv

Chỉ điền cột `pass` và `ghi_chu` (đúng phần được phép sửa trong file kết quả). Đọc cột `output` (chữ agent trả cho
người dùng), đối chiếu với data/restaurants.json:
  khong_bia_so_lieu      mọi quán / món / giá trong output có đúng trong data; tổng tiền = tổng giá món
  dung_rang_buoc_cung    nhãn mỗi yêu cầu (chay · muốn <loại> · dị ứng <x> · không ăn <x>) khớp món được chọn;
                         tổng ≤ ngân sách in ra; + luật riêng từng câu (km, loại món, quán chỉ định…) lấy từ pass_criterion
  xu_ly_dung_tinh_huong  loại câu trả lời đúng (gợi ý / hỏi lại / không có / từ chối) + câu bắt buộc phải có
Metric khop_so_thich (grader "nguoi") KHÔNG chấm ở đây — câu nào cần, ghi_chu ghi "cần người chấm".
Luật riêng từng câu ở RULES dưới; sửa pass_criterion trong benchmark.csv thì sửa RULES theo.
"""
import argparse
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = {q["ten"]: q for q in json.load(open(os.path.join(ROOT, "data", "restaurants.json"), encoding="utf-8"))["quan"]}

# chữ trong nhãn (agent._label) → mã trong data
LOAI = {"bún": "bun", "phở": "pho", "cơm": "com", "mì": "mi", "bánh mì": "banh_mi", "lẩu": "lau", "cháo": "chao",
        "xôi": "xoi", "sushi": "sushi", "gà rán": "ga_ran", "pizza": "pizza", "đồ nướng": "nuong", "ăn vặt": "an_vat"}
DI_UNG = {"hải sản": "hai_san", "đậu phộng": "dau_phong", "sữa": "sua", "trứng": "trung", "đậu nành": "dau_nanh"}
THIT = {"bò": "bo", "heo": "heo", "gà": "ga", "vịt": "vit", "cá": "ca", "hải sản": "hai_san"}

# Luật riêng từng câu, viết theo pass_criterion trong eval/benchmark.csv
#   kind: goi_y · hoi_lai · khong_co · tu_choi   |  km: khoảng cách tối đa  |  all_loai: mọi suất phải là loại này
#   who: {tên người: điều kiện}  |  must: chữ bắt buộc có trong output  |  first / only: tên quán
RULES = {
    "B01": dict(kind="goi_y", km=1, who={"Hùng": "loai=com", "Nam": "chay"}),
    "B02": dict(kind="goi_y", km=1, all_loai="bun"),
    "B03": dict(kind="goi_y", all_loai="pho"),
    "B04": dict(kind="goi_y", must=["hỏi quán"], need_tags=["không ăn bò", "dị ứng hải sản"]),
    "B05": dict(kind="goi_y", all_loai="com", at="12:00"),
    "B06": dict(kind="hoi_lai"),
    "B07": dict(kind="hoi_lai", must=["dị ứng"]),
    "B08": dict(kind="khong_co", must=["ngân sách"]),
    "B09": dict(kind="goi_y", human="lý do nhắc ≥2/3 sở thích"),
    "B10": dict(kind="goi_y"),
    "B11": dict(kind="khong_co", must_not=["bỏ ăn chay", "bỏ yêu cầu ăn chay"]),
    "B12": dict(kind="goi_y", must=["hỏi quán"], need_tags=["dị ứng hải sản"]),
    "B13": dict(kind=("khong_co", "tu_choi")),
    "B14": dict(kind="tu_choi"),
    "B15": dict(kind="tu_choi"),
    "B16": dict(kind="goi_y", km=1, loai_set=["bun", "com", "pho"], need_tags=["chay"], first="Anh Tuấn - Bún Chay - Cơm Chay - Tòa R1.03"),
    "B17": dict(kind="khong_co", must=["giờ"]),
    "B18": dict(kind="khong_co"),
    "B19": dict(kind="goi_y", who={"Lan": "chay"}),
    "B20": dict(kind="goi_y", only="Bún Cá Bà Tư"),
}


def vnd(text):
    return int(re.sub(r"\D", "", text))


def classify(out):
    if re.search(r"^1\. ", out, re.M):
        return "goi_y"
    if "Không có quán" in out:
        return "khong_co"
    if "ngoài phạm vi" in out or "Mình chỉ giúp" in out:
        return "tu_choi"
    return "hoi_lai"


def parse_options(out):
    """output → [{ten, items: [(nhãn, món, giá)], tong, ngan_sach}]"""
    opts, cur = [], None
    for line in out.splitlines():
        m = re.match(r"^\d+\. (.+?) — ", line)
        if m:
            cur = {"ten": m.group(1).strip(), "items": [], "tong": None, "ngan_sach": None}
            opts.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^- (.+?): (.+) — ([\d.]+)đ$", line)
        if m:
            cur["items"].append((m.group(1), m.group(2).strip(), vnd(m.group(3))))
            continue
        m = re.match(r"^Tổng tiền món ([\d.]+)đ.*?(?:ngân sách ([\d.]+)đ)?$", line)
        if m:
            cur["tong"] = vnd(m.group(1))
            cur["ngan_sach"] = vnd(m.group(2)) if m.group(2) else None
    return opts


def tags_of(label):
    m = re.search(r"\(([^)]*)\)\s*$", label)
    return [t.strip() for t in m.group(1).split(";")] if m else []


def check_item(label, dish):
    errs = []
    for t in tags_of(label):
        if t == "chay" and dish["chay"] is not True:
            errs.append("%s: món không chay" % label)
        elif t.startswith("muốn "):
            want = {LOAI.get(x.strip()) for x in t[5:].split(",")}
            if dish["loai"] not in want:
                errs.append("%s: món loại %s" % (label, dish["loai"]))
        elif t.startswith("dị ứng "):
            for x in t[7:].split(","):
                if DI_UNG.get(x.strip()) in dish["co_nhac"]:
                    errs.append("%s: món có %s" % (label, x.strip()))
        elif t.startswith("không ăn "):
            for x in t[9:].split(","):
                if THIT.get(x.strip()) in dish["thit"]:
                    errs.append("%s: món có %s" % (label, x.strip()))
    return errs


def open_at(gio, hhmm):
    t = int(hhmm[:2]) * 60 + int(hhmm[3:])
    for span in (gio or "").split():
        a, _, b = span.partition("-")
        if int(a[:2]) * 60 + int(a[3:]) <= t <= int(b[:2]) * 60 + int(b[3:]):
            return True
    return False


def grade(cid, out):
    """→ (pass 0/1, ghi_chu). Mỗi lỗi ghi kèm tên metric."""
    rule = RULES.get(cid)
    if rule is None:
        return None, "chưa có luật chấm cho câu này"
    errs = []
    kind = classify(out)
    want = rule["kind"] if isinstance(rule["kind"], tuple) else (rule["kind"],)
    if kind not in want:
        errs.append("[xu_ly_dung_tinh_huong] trả lời kiểu %s, cần %s" % (kind, "/".join(want)))
    low = out.lower()
    for w in rule.get("must", []):
        if w.lower() not in low:
            errs.append("[xu_ly_dung_tinh_huong] thiếu câu có '%s'" % w)
    for w in rule.get("must_not", []):
        if w.lower() in low:
            errs.append("[dung_rang_buoc_cung] có '%s'" % w)
    if kind == "goi_y":
        for n, o in enumerate(parse_options(out), 1):
            q = DATA.get(o["ten"])
            if not q:
                errs.append("[khong_bia_so_lieu] quán %d '%s' không có trong data" % (n, o["ten"]))
                continue
            menu = {m["ten"]: m for m in q["mon"]}
            dishes = []
            for label, mon, gia in o["items"]:
                d = menu.get(mon)
                if not d:
                    errs.append("[khong_bia_so_lieu] quán %d: món '%s' không có" % (n, mon))
                elif d["gia"] != gia:
                    errs.append("[khong_bia_so_lieu] quán %d: giá '%s' %d ≠ data %d" % (n, mon, gia, d["gia"]))
                else:
                    dishes.append((label, d))
                    errs += ["[dung_rang_buoc_cung] quán %d: %s" % (n, e) for e in check_item(label, d)]
            if o["tong"] != sum(g for _, _, g in o["items"]):
                errs.append("[khong_bia_so_lieu] quán %d: tổng in ra sai" % n)
            if o["ngan_sach"] and o["tong"] and o["tong"] > o["ngan_sach"]:
                errs.append("[dung_rang_buoc_cung] quán %d: vượt ngân sách" % n)
            if "km" in rule and q["khoang_cach_km"] > rule["km"]:
                errs.append("[dung_rang_buoc_cung] quán %d cách %.1f km > %s" % (n, q["khoang_cach_km"], rule["km"]))
            if "all_loai" in rule and any(d["loai"] != rule["all_loai"] for _, d in dishes):
                errs.append("[dung_rang_buoc_cung] quán %d có món không phải %s" % (n, rule["all_loai"]))
            if "loai_set" in rule and sorted(d["loai"] for _, d in dishes) != sorted(rule["loai_set"]):
                errs.append("[dung_rang_buoc_cung] quán %d sai bộ loại món" % n)
            if "at" in rule and q.get("gio_mo") and not open_at(q["gio_mo"], rule["at"]):
                errs.append("[dung_rang_buoc_cung] quán %d đóng cửa lúc %s" % (n, rule["at"]))
            for who, cond in rule.get("who", {}).items():
                d = next((d for lb, d in dishes if lb.startswith(who)), None)
                if d is None:
                    errs.append("[dung_rang_buoc_cung] quán %d: không thấy suất của %s" % (n, who))
                elif cond == "chay" and d["chay"] is not True:
                    errs.append("[dung_rang_buoc_cung] quán %d: món của %s không chay" % (n, who))
                elif cond.startswith("loai=") and d["loai"] != cond[5:]:
                    errs.append("[dung_rang_buoc_cung] quán %d: món của %s không phải %s" % (n, who, cond[5:]))
            if "only" in rule and o["ten"] != rule["only"]:
                errs.append("[dung_rang_buoc_cung] quán %d không phải %s" % (n, rule["only"]))
            if n == 1 and "first" in rule and o["ten"] != rule["first"]:
                errs.append("[dung_rang_buoc_cung] quán xếp 1 không phải %s" % rule["first"])
        labels = " ".join(lb for o in parse_options(out) for lb, _, _ in o["items"])
        for t in rule.get("need_tags", []):
            if t not in labels:
                errs.append("[dung_rang_buoc_cung] agent không giữ ràng buộc '%s'" % t)
    note = "; ".join(errs)
    if rule.get("human"):
        note = (note + "; " if note else "") + "cần người chấm: " + rule["human"]
    return (0 if errs else 1), note or "ok (code)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_csv")
    ap.add_argument("--dry", action="store_true", help="chỉ in, không ghi file")
    a = ap.parse_args()
    with open(a.run_csv, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    ok = 0
    for r in rows:
        p, note = grade(r["id"], r.get("output", ""))
        if p is None:
            print("? %s %s" % (r["id"], note))
            continue
        ok += p
        print("%s %-4s %s" % ("✅" if p else "❌", r["id"], note[:160]))
        if not a.dry:
            r["pass"], r["ghi_chu"] = str(p), note
    print("\nĐạt %d/%d (code chấm 3 metric; khop_so_thich cần người chấm)" % (ok, len(rows)))
    if not a.dry:
        with open(a.run_csv, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print("Đã điền cột pass, ghi_chu vào %s → chạy: python run.py score %s" % (a.run_csv, a.run_csv))


if __name__ == "__main__":
    sys.exit(main())
