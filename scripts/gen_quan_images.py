"""Sinh ẢNH MINH HOẠ mặt tiền cho từng quán DỰNG GIẢ trong data/restaurants.json (OpenAI image API).

Quán là quán giả (tên dựng) → ảnh do AI tạo, giao diện ghi rõ "ảnh minh hoạ". Không dùng cho quán thật.
Chạy (thư mục gốc repo, cần OPENAI_API_KEY hoặc API_KEY trong .env):
    python scripts/gen_quan_images.py                       # sinh ảnh còn thiếu
    python scripts/gen_quan_images.py --only Q01 Q02 --force
Ảnh lưu ở web/public/img/quan/<id>.webp. Model mặc định gpt-image-2, quality medium (~$0.05 / ảnh).
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "public", "img", "quan")


def env_key():
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8-sig"):
        k, _, v = line.strip().partition("=")
        if k in ("OPENAI_API_KEY", "API_KEY") and v.strip():
            return v.strip().strip('"').strip("'")
    sys.exit("Không thấy OPENAI_API_KEY / API_KEY trong .env")


def prompt_for(q):
    dishes = ", ".join(dict.fromkeys(m["ten"].split(" (")[0] for m in q["mon"]))
    dishes = ", ".join(dishes.split(", ")[:4])
    return ("Realistic daytime photo of the front of a small casual Vietnamese street eatery in Hanoi, %s style "
            "(serving %s). Low plastic stools and small tables on the sidewalk, warm and inviting, natural light. "
            "Signboard without readable text. No people, no text, no logo." % (q["am_thuc"], dishes))


def generate(key, prompt, path, model, quality):
    body = {"model": model, "prompt": prompt, "size": "1024x1024", "quality": quality,
            "output_format": "webp", "output_compression": 70, "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", method="POST",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    return data.get("usage", {}).get("output_tokens")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--model", default="gpt-image-2")
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    a = ap.parse_args()
    key = env_key()
    quan = json.load(open(os.path.join(ROOT, "data", "restaurants.json"), encoding="utf-8"))["quan"]
    done = 0
    for q in quan:
        if a.only and q["id"] not in a.only:
            continue
        path = os.path.join(OUT, q["id"] + ".webp")
        if os.path.exists(path) and not a.force:
            continue
        try:
            tok = generate(key, prompt_for(q), path, a.model, a.quality)
            done += 1
            print("✓ %s %s (%s token)" % (q["id"], q["ten"], tok), flush=True)
        except Exception as e:  # một ảnh lỗi thì báo rồi làm tiếp
            print("✗ %s: %s" % (q["id"], e), flush=True)
    print("Xong: sinh %d ảnh (model %s, quality %s)." % (done, a.model, a.quality), flush=True)


if __name__ == "__main__":
    main()
