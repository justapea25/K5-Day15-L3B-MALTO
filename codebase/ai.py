"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

SHOW_RAW = False   # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY") or "").strip()


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER == "openai":
        r = call_openai(system, user)
    elif MODEL_PROVIDER == "anthropic":
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(
            "chưa viết phần gọi model cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md mục 2.4"
            % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}


def post_json(url, headers, body, timeout=40, retries=1):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib).
    Mạng / model chậm quá `timeout` giây → thử lại `retries` lần rồi mới báo lỗi."""
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt == retries:
                raise RuntimeError("Gọi model quá %ds (đã thử %d lần): %s" % (timeout, retries + 1, e))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


URL_OPENAI = "https://api.openai.com/v1/chat/completions"
URL_RESPONSES = "https://api.openai.com/v1/responses"
REASONING_EFFORT = (os.environ.get("REASONING_EFFORT") or "low").strip()  # agent tự chọn bước: low cho nhanh
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
URL_OLLAMA = "http://localhost:11434/api/chat"


def call_openai(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OPENAI, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages})
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"],
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


@model_call
def call_model_tools(system: str, items: list, tools: list, previous_id=None) -> dict:
    """Gọi model CÓ CÔNG CỤ (function calling) qua OpenAI Responses API — cho agent tự chọn bước (agent_loop.py).
    items: input của lượt này (tin nhắn, hoặc kết quả công cụ {"type": "function_call_output", ...}).
    previous_id: id phản hồi trước để nối hội thoại (model giữ cả phần suy luận). Model BẮT BUỘC gọi ≥1 công cụ.
    Trả 4 khoá như call_model + "id" (id phản hồi) + "calls" [{call_id, name, arguments}]. Chỉ có nhánh OpenAI."""
    if MODEL_PROVIDER != "openai":
        raise NotImplementedError("call_model_tools mới viết cho MODEL_PROVIDER=openai")
    body = {"model": MODEL_NAME, "instructions": system, "input": items, "tools": tools,
            "tool_choice": "required", "reasoning": {"effort": REASONING_EFFORT}}
    if previous_id:
        body["previous_response_id"] = previous_id
    data = post_json(URL_RESPONSES, {"Authorization": "Bearer " + API_KEY}, body, timeout=120)
    calls = [{"call_id": o["call_id"], "name": o["name"], "arguments": o.get("arguments") or "{}"}
             for o in data.get("output", []) if o.get("type") == "function_call"]
    text = "".join(c.get("text", "") for o in data.get("output", []) if o.get("type") == "message"
                   for c in o.get("content", []) if c.get("type") == "output_text")
    text = text or "; ".join("%s(%s)" % (c["name"], c["arguments"][:200]) for c in calls)
    u = data["usage"]
    return {"text": text, "model": MODEL_NAME, "tokens_in": int(u["input_tokens"]),
            "tokens_out": int(u["output_tokens"]), "id": data["id"], "calls": calls}


def call_claude(system, user):
    data = post_json(URL_CLAUDE,
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


def call_ollama(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OLLAMA, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300, retries=0)
    return {"text": data["message"]["content"],
            "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0)}
