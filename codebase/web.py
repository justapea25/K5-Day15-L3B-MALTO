"""Giao diện web mẫu cho bản chạy thử — chỉ dùng thư viện chuẩn (http.server). Phụ trách: Minh.

Chạy:  python codebase/web.py            → mở http://localhost:8010
       python codebase/web.py --port 8080

Gọi đúng answer(text) trong agent.py như `python run.py` (cùng luồng, cùng công cụ, cùng model trong .env).
API:
  GET  /             trang giao diện (codebase/static/index.html)
  GET  /api/info     model đang dùng (không trả API key)
  GET  /api/quan     dữ liệu quán (data/restaurants.json) để hiển thị
  POST /api/answer   {"text": "..."} → {"output", "ket_qua", "thong_ke", "cac_buoc"}
Server một luồng (tracing của khung dùng biến toàn cục), chỉ nghe trên 127.0.0.1. Không ghi trace ra file.
"""
import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ai  # noqa: E402
import tracing  # noqa: E402
from agent import answer  # noqa: E402
from tools import _data  # noqa: E402

STATIC = os.path.join(HERE, "static")
MAX_BODY = 20_000


def _steps(events):
    """Rút gọn sự kiện trace thành các bước để hiển thị."""
    out = []
    for e in events:
        step = {"loai": e["kind"], "t": e.get("t")}
        if e["kind"] == "model":
            step.update(ten="gọi model", chi_tiet="%s · vào %s / ra %s token" % (
                e.get("model") or "?", e.get("tokens_in"), e.get("tokens_out")))
        elif e["kind"] == "tool":
            step.update(ten=e.get("name"), chi_tiet=e.get("input"))
        else:
            step.update(ten="ghi chú", chi_tiet=e.get("text"))
        if e.get("error"):
            step["loi"] = e["error"]
        out.append(step)
    return out


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(STATIC, "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if self.path == "/api/info":
            return self._send(200, {"provider": ai.MODEL_PROVIDER, "model": ai.MODEL_NAME or ai.MODEL_PROVIDER})
        if self.path == "/api/quan":
            return self._send(200, _data())
        return self._send(404, {"loi": "không có đường dẫn này"})

    def do_POST(self):
        if self.path != "/api/answer":
            return self._send(404, {"loi": "không có đường dẫn này"})
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return self._send(400, {"loi": "nội dung rỗng hoặc quá dài"})
        try:
            text = str(json.loads(self.rfile.read(length).decode("utf-8")).get("text") or "").strip()
        except (ValueError, AttributeError):
            return self._send(400, {"loi": "body phải là JSON {\"text\": \"...\"}"})
        if not text:
            return self._send(400, {"loi": "chưa nhập yêu cầu"})
        tracing.begin("web")
        try:
            result = answer(text)
        except Exception as e:  # lỗi gọi model: báo lên giao diện, server vẫn chạy
            _, events = tracing.end()
            return self._send(500, {"loi": "%s: %s" % (type(e).__name__, e), "cac_buoc": _steps(events)})
        summary, events = tracing.end()
        return self._send(200, {"output": result.get("output", ""), "ket_qua": result.get("ket_qua"),
                                "thong_ke": summary, "cac_buoc": _steps(events)})

    def log_message(self, fmt, *args):
        sys.stderr.write("[web] %s\n" % (fmt % args))


def main():
    ap = argparse.ArgumentParser(description="Giao diện web mẫu — chọn quán cho nhóm")
    ap.add_argument("--port", type=int, default=8010)
    port = ap.parse_args().port
    server = HTTPServer(("127.0.0.1", port), Handler)
    print("Giao diện web: http://localhost:%d  (model: %s) · Thoát: Ctrl+C" % (port, ai.MODEL_NAME or ai.MODEL_PROVIDER))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
