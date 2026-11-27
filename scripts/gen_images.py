"""Sinh ẢNH MINH HOẠ cho quán và món trong data/restaurants.json bằng model sinh ảnh của OpenAI.

Ảnh do AI tạo, chỉ để giao diện dễ nhìn — KHÔNG phải ảnh quán / món thật (quán là dựng giả).
Giao diện ghi rõ "ảnh minh hoạ do AI tạo".

Chạy (ở thư mục gốc repo, cần OPENAI_API_KEY hoặc API_KEY trong .env):
    python scripts/gen_images.py            # sinh ảnh còn thiếu
    python scripts/gen_images.py --only Q01-4 --force
Ảnh lưu ở web/public/img/{quan,mon}/<id>.webp. Ảnh đã có thì bỏ qua (thêm quán / món mới thì chạy lại).
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "public", "img")
MODEL = "gpt-image-1-mini"
STYLE = ("Realistic food photo, 45-degree overhead angle, natural daylight, on a simple wooden table "
         "of a casual Hanoi street eatery, warm colors, sharp focus. No text, no logo, no people, no hands.")
SHAPE = {  # gợi ý hình dạng theo loại món để model vẽ đúng món
    "bun": "a bowl with thin round white rice vermicelli noodles clearly visible",
    "pho": "a bowl of pho with flat white rice noodles clearly visible in clear broth",
    "com": "a plate of steamed white rice with the main dish on top or beside it",
    "mi": "a bowl of yellow egg noodles",
    "banh_mi": "a Vietnamese baguette sandwich (banh mi) cut open showing the filling",
    "lau": "a small single-portion hot pot on a burner",
    "khac": "a Vietnamese dish served on a plate",
}


def env_key():
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8-sig"):
        k, _, v = line.strip().partition("=")
        if k in ("OPENAI_API_KEY", "API_KEY") and v.strip():
            return v.strip().strip('"').strip("'")
    sys.exit("Không thấy OPENAI_API_KEY / API_KEY trong .env")


def generate(key, prompt, path, model=MODEL, quality="low"):
    body = {"model": model, "prompt": prompt, "size": "1024x1024", "quality": quality,
            "output_format": "webp", "output_compression": 70, "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", method="POST",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    return data.get("usage", {})


def jobs(data):
    for q in data["quan"]:
        dishes = ", ".join(m["ten"] for m in q["mon"][:3])
        yield q["id"], "quan", ("Realistic daytime photo of the front of a small casual Vietnamese street eatery in Hanoi "
                                "(style of a place called \"%s\", serving %s), low plastic stools and tables on the sidewalk, "
                                "warm and inviting. Signboard without readable text. No people, no text, no logo."
                                % (q["ten"], dishes))
        for m in q["mon"]:
            yield m["id"], "mon", "Vietnamese dish \"%s\" (%s): %s. %s" % (
                m["ten"], m.get("mo_ta") or "", SHAPE.get(m.get("loai"), SHAPE["khac"]), STYLE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="chỉ sinh các id này (vd Q01 Q01-4)")
    ap.add_argument("--force", action="store_true", help="sinh lại kể cả khi đã có ảnh")
    ap.add_argument("--kind", choices=["quan", "mon"], help="chỉ sinh ảnh quán hoặc ảnh món")
    ap.add_argument("--model", default=MODEL, help="model sinh ảnh (mặc định %s)" % MODEL)
    ap.add_argument("--quality", default="low", choices=["low", "medium", "high"])
    a = ap.parse_args()
    key = env_key()
    with open(os.path.join(ROOT, "data", "restaurants.json"), encoding="utf-8") as f:
        data = json.load(f)
    done = 0
    for item_id, kind, prompt in jobs(data):
        if (a.only and item_id not in a.only) or (a.kind and kind != a.kind):
            continue
        path = os.path.join(OUT, kind, item_id + ".webp")
        if os.path.exists(path) and not a.force:
            continue
        try:
            usage = generate(key, prompt, path, a.model, a.quality)
            done += 1
            print("✓ %s/%s.webp  %s" % (kind, item_id, usage or ""))
        except Exception as e:  # một ảnh lỗi thì báo rồi làm tiếp
            print("✗ %s: %s" % (item_id, e))
    print("Xong: sinh %d ảnh mới (model %s, quality %s)." % (done, a.model, a.quality))


if __name__ == "__main__":
    main()
