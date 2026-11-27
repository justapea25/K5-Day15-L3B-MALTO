"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { vnd } from "./lib";
import QuanCover from "./quan-cover";
import type { AnswerResponse, KetQua, Loai, LuaChon } from "./types";

const EXAMPLES: [string, string][] = [
  ["Nhóm mỗi người một ý", "Nhóm 4 người: Lan muốn ăn gì có nước, Hùng thèm cơm, Mai không ăn đồ chiên, Nam ăn chay. Mỗi người tầm 70k, dưới 2km"],
  ["Một mình, nhiều món", "Mình đặt về văn phòng: 1 bún, 1 phở, 1 cơm chay, tổng 250k, dưới 2km"],
  ["Đồ Nhật cho 2 người", "2 người muốn ăn đồ Nhật, 1 người thích sushi, tổng 400k, đi xa được 5km"],
  ["Ăn vặt buổi tối", "Tối nay 8h, 3 đứa muốn ăn vặt, tokbokki hoặc nem chua rán, mỗi đứa 50k"],
]

const LABEL: Record<Loai, string> = { goi_y: "Gợi ý", hoi_lai: "Hỏi lại", khong_co: "Không có", tu_choi: "Từ chối" };
const BADGE: Record<Loai, string> = {
  goi_y: "bg-ok/15 text-ok",
  hoi_lai: "bg-warn/15 text-warn",
  khong_co: "bg-bad/15 text-bad",
  tu_choi: "bg-bad/15 text-bad",
};
// ---------- Kết quả ----------

function BudgetBar({ total, budget }: { total: number; budget: number }) {
  const pct = Math.min(100, Math.round((total / budget) * 100));
  return (
    <div className="mt-2">
      <div className="h-2 overflow-hidden rounded-full bg-soft">
        <div className={`h-full rounded-full ${pct > 90 ? "bg-warn" : "bg-ok"}`} style={{ width: `${pct}%` }} />
      </div>
      <p className="mt-1 text-xs text-muted">
        Dùng {pct}% ngân sách {vnd(budget)} · còn {vnd(budget - total)}
      </p>
    </div>
  );
}

function Suggestion({ k }: { k: KetQua }) {
  if (!k.quan || !k.mon) return null;
  return (
    <>
      <div className="flex gap-3 rounded-xl bg-gradient-to-br from-accent to-accent/70 p-3 text-accent-ink">
        <div className="relative h-24 w-24 shrink-0 overflow-hidden rounded-lg bg-black/10 sm:h-28 sm:w-28">
          <QuanCover id={k.quan.id} icon="🍜" sizes="112px" />
        </div>
        <div className="min-w-0 py-1">
        <p className="text-xs font-medium uppercase tracking-wider opacity-80">⭐ Quán hợp nhất với đơn của bạn</p>
        <h3 className="text-xl font-semibold leading-snug tracking-tight">{k.quan.ten}</h3>
        <div className="mt-2 flex flex-wrap gap-1.5 text-xs">
          <span className="rounded-full bg-black/15 px-2 py-0.5">📍 {k.quan.khoang_cach_km} km</span>
          {k.quan.muc_gia ? <span className="rounded-full bg-black/15 px-2 py-0.5">{k.quan.muc_gia}</span> : null}
          {k.quan.danh_gia ? <span className="rounded-full bg-black/15 px-2 py-0.5">★ {k.quan.danh_gia}{k.quan.so_danh_gia ? ` (${k.quan.so_danh_gia})` : ""}</span> : null}
          <span className="rounded-full bg-black/15 px-2 py-0.5">🕒 {k.quan.gio_mo ?? "chưa rõ giờ mở"}</span>
          <Link href={`/quan?open=${k.quan.id}`} className="rounded-full bg-white/90 px-2.5 py-0.5 font-semibold text-accent hover:bg-white">
            Xem menu quán →
          </Link>
        </div>
        </div>
      </div>

      <div className="mt-3 rounded-xl border border-line bg-panel">
        <p className="flex items-center justify-between border-b border-line px-3 py-2 text-xs font-semibold text-muted">
          <span>Yêu cầu trong đơn → món quán đáp ứng</span>
          <span className="rounded-full bg-ok/15 px-2 py-0.5 text-ok">✓ đủ {k.mon.length}/{k.mon.length}</span>
        </p>
        <ul className="divide-y divide-line">
          {k.mon.map((m, i) => (
            <li key={i} className="flex items-center gap-3 px-3 py-2">
              <span className="text-ok">✓</span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-xs text-muted">{m.nguoi}</span>
                <span className="block truncate font-medium" title={m.mon}>{m.mon}</span>
              </span>
              <span className="shrink-0 text-sm font-semibold tabular-nums text-accent">{vnd(m.gia)}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-3 rounded-xl bg-soft px-4 py-3">
        <div className="flex items-baseline justify-between">
          <span className="text-sm text-muted">Tổng đơn (chưa gồm ship)</span>
          <span className="text-xl font-semibold tabular-nums">{vnd(k.tong_tien)}</span>
        </div>
        {k.ngan_sach ? <BudgetBar total={k.tong_tien ?? 0} budget={k.ngan_sach} /> : null}
      </div>

      <p className="mt-1.5 text-[11px] text-muted">Ảnh quán là ảnh minh hoạ do AI tạo (quán dựng giả).</p>
      {k.ly_do && <p className="mt-3 text-sm leading-relaxed">💬 {k.ly_do}</p>}
      {k.ai_bi_thay && (
        <p className="mt-2 rounded-lg border-l-[3px] border-warn bg-soft px-3 py-2 text-sm">
          Lựa chọn của AI không qua bước kiểm tra, đây là phương án code đã kiểm.
        </p>
      )}
      <Alternatives options={(k.lua_chon ?? []).slice(1)} budget={k.ngan_sach} />
      {(k.canh_bao ?? []).map((w, i) => (
        <p key={i} className="mt-2 rounded-lg border-l-[3px] border-warn bg-soft px-3 py-2 text-sm">
          {w}
        </p>
      ))}
    </>
  );
}

function Alternatives({ options, budget }: { options: LuaChon[]; budget?: number | null }) {
  if (options.length === 0) return null;
  return (
    <div className="mt-4">
      <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">Quán khác cũng đáp ứng đơn</p>
      <div className="grid gap-2">
        {options.map((o, i) => (
          <details key={o.quan.id} className="group rounded-xl border border-line bg-panel">
            <summary className="flex cursor-pointer list-none items-start gap-3 p-3">
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-soft text-sm font-bold text-muted">{i + 2}</span>
              <span className="min-w-0 flex-1">
                <span className="flex flex-wrap items-baseline justify-between gap-x-3">
                  <span className="font-semibold">{o.quan.ten}</span>
                  <span className="text-sm font-semibold tabular-nums">
                    {vnd(o.tong_tien)}
                    {budget ? <span className="font-normal text-muted"> / {vnd(budget)}</span> : null}
                  </span>
                </span>
                <span className="block text-xs text-muted">
                  ✓ đủ {o.mon.length}/{o.mon.length} yêu cầu · 📍 {o.quan.khoang_cach_km} km{o.quan.muc_gia ? ` · ${o.quan.muc_gia}` : ""}{o.quan.danh_gia ? ` · ★ ${o.quan.danh_gia} (${o.quan.so_danh_gia ?? 0})` : ""} · {o.mon.map((m) => m.mon).join(", ")}
                </span>
                {o.danh_doi && <span className="mt-1 block text-xs text-warn">↔ {o.danh_doi}</span>}
              </span>
              <span className="text-muted transition group-open:rotate-180">▾</span>
            </summary>
            <div className="border-t border-line px-3 pb-3 pt-2">
              <ul className="grid gap-1 text-sm">
                {o.mon.map((m, j) => (
                  <li key={j} className="flex justify-between gap-2">
                    <span className="min-w-0 truncate">
                      <span className="text-muted">{m.nguoi}:</span> {m.mon}
                    </span>
                    <span className="shrink-0 tabular-nums text-accent">{vnd(m.gia)}</span>
                  </li>
                ))}
              </ul>
              {o.ly_do && <p className="mt-2 text-xs leading-relaxed text-muted">💬 {o.ly_do}</p>}
              <Link href={`/quan?open=${o.quan.id}`} className="mt-2 inline-block text-xs font-semibold text-accent hover:underline">
                Xem menu quán →
              </Link>
            </div>
          </details>
        ))}
      </div>
    </div>
  );
}

const ICON: Record<Loai, string> = { goi_y: "✅", hoi_lai: "🤔", khong_co: "🚫", tu_choi: "⛔" };

// ---------- Chat ----------

type Msg = {
  id: string;
  role: "user" | "bot";
  text: string;
  sent?: string;          // bot: câu thực sự đã gửi backend (có thể đã ghép với yêu cầu trước)
  merged?: boolean;       // bot: câu gửi đi là bản ghép
  data?: AnswerResponse;  // bot: phản hồi backend
  error?: string;
};

const newId = () => Math.random().toString(36).slice(2);

function Avatar() {
  return (
    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-accent/15 text-lg" aria-hidden>
      🍜
    </div>
  );
}

function Typing() {
  return (
    <div className="flex items-end gap-2">
      <Avatar />
      <div className="rounded-2xl rounded-bl-md border border-line bg-panel px-4 py-3">
        <span className="flex gap-1" aria-label="Đang trả lời">
          {[0, 150, 300].map((d) => (
            <span key={d} className="h-2 w-2 animate-bounce rounded-full bg-muted" style={{ animationDelay: `${d}ms` }} />
          ))}
        </span>
      </div>
    </div>
  );
}

function BotBubble({ m }: { m: Msg }) {
  const k = m.data?.ket_qua;
  const loai: Loai = k?.loai ?? "hoi_lai";
  const rich = k?.loai === "goi_y";
  return (
    <div className="flex items-start gap-2">
      <Avatar />
      <div className={`min-w-0 ${rich ? "w-full max-w-[880px]" : "max-w-[75%]"}`}>
        <div className={`rounded-2xl rounded-tl-md border bg-panel ${rich ? "p-3" : "px-4 py-3"} ${m.error ? "border-bad/40" : "border-line"}`}>
          {m.error ? (
            <p className="text-sm text-bad">Lỗi: {m.error}</p>
          ) : (
            <>
              {k?.che_do_gia && <p className="mb-2 text-xs font-medium text-warn">Chế độ giả: chưa nối model, đang dùng yêu cầu mẫu cố định.</p>}
              {rich && k ? (
                <Suggestion k={k} />
              ) : (
                <p className="whitespace-pre-wrap text-[15px] leading-relaxed">
                  <span className="mr-1.5">{ICON[loai]}</span>
                  {m.data?.output ?? m.text}
                </p>
              )}
            </>
          )}
        </div>
        {m.data && (
          <div className="mt-1 flex flex-wrap items-center gap-2 pl-1 text-[11px] text-muted">
            <span className={`rounded-full px-2 py-0.5 font-semibold ${BADGE[loai]}`}>{LABEL[loai]}</span>
            {m.merged && <span title={m.sent}>· đã ghép với yêu cầu trước</span>}
          </div>
        )}
      </div>
    </div>
  );
}

function UserBubble({ m }: { m: Msg }) {
  return (
    <div className="flex justify-end">
      <p className="max-w-[80%] whitespace-pre-wrap rounded-2xl rounded-br-md bg-accent px-4 py-2.5 text-[15px] leading-relaxed text-accent-ink">
        {m.text}
      </p>
    </div>
  );
}

const EX_ICON = ["👥", "🧾", "🍣", "🌙"];

function Welcome({ onPick, disabled, empty }: { onPick: (t: string) => void; disabled: boolean; empty: boolean }) {
  if (!empty) {
    return (
      <div className="flex items-start gap-2">
        <Avatar />
        <p className="rounded-2xl rounded-tl-md border border-line bg-panel px-4 py-3 text-[15px]">
          Chào bạn 👋 Kể yêu cầu của cả nhóm, mình chọn một quán hợp tất cả.
        </p>
      </div>
    );
  }
  return (
    <div className="mx-auto flex max-w-3xl flex-col items-center py-8 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-accent to-accent/60 text-3xl shadow-lg shadow-accent/20">
        🍜
      </div>
      <h2 className="mt-4 text-2xl font-bold tracking-tight">Hôm nay ăn gì đây?</h2>
      <p className="mt-2 max-w-md text-[15px] leading-relaxed text-muted">
        Cứ kể như đang nhắn cho bạn: ai muốn ăn gì, ai kiêng gì, tầm bao nhiêu tiền, đi xa được không. Mình lọc ra vài quán{" "}
        <b className="text-ink">chiều được cả đơn</b>, kèm món gợi ý cho từng yêu cầu.
      </p>
      <div className="mt-6 grid w-full gap-2.5 text-left sm:grid-cols-2">
        {EXAMPLES.map(([name, t], i) => (
          <button
            key={name}
            type="button"
            disabled={disabled}
            onClick={() => onPick(t)}
            className="group flex gap-3 rounded-xl border border-line bg-panel p-3 text-left transition hover:-translate-y-0.5 hover:border-accent/60 hover:shadow-md disabled:opacity-50"
          >
            <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-soft text-lg group-hover:bg-accent/15">{EX_ICON[i]}</span>
            <span className="min-w-0">
              <span className="block text-sm font-semibold">{name}</span>
              <span className="line-clamp-2 text-xs leading-snug text-muted">{t}</span>
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

// ---------- Trang ----------

const CHAT_KEY = "malto-chat";

export default function App() {
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const autoRan = useRef(false);

  const bots = msgs.filter((m) => m.role === "bot");
  const lastBot = bots[bots.length - 1];
  const waitingAnswer = lastBot?.data?.ket_qua?.loai === "hoi_lai";

  async function send(raw: string) {
    const t = raw.trim();
    if (!t || loading) return;
    // Bot vừa hỏi lại → ghép câu bổ sung với yêu cầu trước (backend xử lý mỗi tin độc lập)
    const prev = lastBot?.data?.ket_qua?.loai === "hoi_lai" ? lastBot.sent : undefined;
    const sent = prev ? `${prev}\nBổ sung: ${t}` : t;
    const userMsg: Msg = { id: newId(), role: "user", text: t };
    setMsgs((ms) => [...ms, userMsg]);
    setInput("");
    setLoading(true);
    const bot: Msg = { id: newId(), role: "bot", text: "", sent, merged: Boolean(prev) };
    try {
      const r = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: sent }),
      });
      const body = await r.json().catch(() => ({}));
      if (r.ok) bot.data = body as AnswerResponse;
      else bot.error = body.loi ?? `Lỗi ${r.status}`;
    } catch (e) {
      bot.error = `Không gọi được backend: ${e}`;
    } finally {
      setMsgs((ms) => [...ms, bot]);
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function reset() {
    try {
      sessionStorage.removeItem(CHAT_KEY);
    } catch {}
    setMsgs([]);
    setInput("");
    inputRef.current?.focus();
  }

  useEffect(() => {
    // khôi phục hội thoại khi quay lại từ tab "Danh sách quán"
    try {
      const saved = sessionStorage.getItem(CHAT_KEY);
      if (saved) setTimeout(() => setMsgs(JSON.parse(saved)), 0);
    } catch {}
    // ?q=... → gửi luôn câu đó (tiện khi demo: gửi link có sẵn câu hỏi)
    const q = new URLSearchParams(window.location.search).get("q");
    // React dev chạy effect 2 lần → chặn gửi trùng bằng cờ
    if (q && !autoRan.current) {
      autoRan.current = true;
      setTimeout(() => send(q), 0);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    try {
      sessionStorage.setItem(CHAT_KEY, JSON.stringify(msgs));
    } catch {}
  }, [msgs]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [msgs.length, loading]);

  // ô nhập tự giãn theo nội dung (tối đa ~5 dòng)
  useEffect(() => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 140)}px`;
  }, [input]);

  return (
    <>
      <div>
        {/* Khung chat */}
        <section className="flex h-[calc(100vh-7rem)] min-h-[560px] flex-col overflow-hidden rounded-2xl border border-line bg-panel">
          <div className="flex items-center justify-between gap-2 border-b border-line px-4 py-3">
            <div className="flex items-center gap-2">
              <Avatar />
              <div>
                <p className="text-sm font-semibold leading-tight">Trợ lý chọn quán</p>
                <p className="text-xs text-muted">{loading ? "đang trả lời…" : "Chỉ gợi ý từ danh sách quán có sẵn"}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={reset}
              disabled={loading || msgs.length === 0}
              className="rounded-lg border border-line px-3 py-1.5 text-xs hover:border-accent disabled:opacity-40"
            >
              ＋ Cuộc trò chuyện mới
            </button>
          </div>

          <div className="flex-1 space-y-4 overflow-y-auto bg-bg/40 px-4 py-5">
            <Welcome onPick={send} disabled={loading} empty={msgs.length === 0} />
            {msgs.map((m) =>
              m.role === "user" ? (
                <UserBubble key={m.id} m={m} />
              ) : (
                <BotBubble key={m.id} m={m} />
              ),
            )}
            {loading && <Typing />}
            <div ref={endRef} />
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              send(input);
            }}
            className="border-t border-line p-3"
          >
            {waitingAnswer && !loading && (
              <p className="mb-2 text-xs text-muted">↩ Trả lời câu hỏi của trợ lý, mình sẽ ghép với yêu cầu trước.</p>
            )}
            <div className="flex items-end gap-2 rounded-xl border border-line bg-bg px-3 py-2 focus-within:border-accent focus-within:ring-2 focus-within:ring-accent/25">
              <textarea
                ref={inputRef}
                value={input}
                rows={1}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
                    e.preventDefault();
                    send(input);
                  }
                }}
                placeholder={waitingAnswer ? "Trả lời trợ lý…" : "Nhắn yêu cầu của nhóm… (Enter để gửi, Shift+Enter xuống dòng)"}
                className="max-h-[140px] flex-1 resize-none bg-transparent py-1 text-[15px] outline-none placeholder:text-muted"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                aria-label="Gửi"
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent text-accent-ink disabled:opacity-40"
              >
                ➤
              </button>
            </div>
          </form>
        </section>

      </div>

    </>
  );
}
