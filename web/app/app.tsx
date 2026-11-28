"use client";

import { useEffect, useRef, useState } from "react";
import { CastImg } from "./cast";
import { vnd } from "./lib";
import QuanCover from "./quan-cover";
import ShopPanel from "./shop-panel";
import type { Quan } from "./types";
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
      <div className="h-2 overflow-hidden bg-soft">
        <div className={`anim-bar h-full ${pct > 90 ? "bg-warn" : "bg-ok"}`} style={{ width: `${pct}%` }} />
      </div>
      <p className="mt-1 text-xs text-muted">
        Dùng {pct}% ngân sách {vnd(budget)} · còn {vnd(budget - total)}
      </p>
    </div>
  );
}

function Suggestion({ k, feedbackDone, onFeedback, onOpenShop }: { k: KetQua; feedbackDone?: boolean; onFeedback?: () => void; onOpenShop: (id: string) => void }) {
  if (!k.quan || !k.mon) return null;
  return (
    <>
      <div className="mb-2 flex items-start gap-3">
        <div className="min-w-0 flex-1">
          <p className="anim-stamp mb-2 text-[11px] font-extrabold uppercase tracking-[0.1em] text-brand">Kết luận điều tra</p>
          {onFeedback && (
            <button
              type="button"
              onClick={onFeedback}
              disabled={feedbackDone}
              className="press border-2 border-ink bg-sun/60 px-2.5 py-1 shadow-[2px_2px_0_#242434] text-xs font-bold disabled:opacity-60"
            >
              {feedbackDone ? "Đã gửi phản hồi" : "★ Tôi hài lòng"}
            </button>
          )}
        </div>
        <CastImg k="point" alt="Thám tử chỉ vào kết quả" className="anim-mascot h-[88px] w-[100px] shrink-0 object-contain" />
      </div>
      {k.loi_nhan && <p className="mb-3 whitespace-pre-line text-[15px] leading-relaxed">{k.loi_nhan}</p>}
      {(k.cau_hoi ?? []).map((q, i) => (
        <p key={i} className="mb-3 border border-accent/40 bg-accent/10 px-3 py-2 text-[15px] leading-relaxed">
          ❓ {q}
        </p>
      ))}
      <div className="anim-pop flex gap-3 bg-gradient-to-br from-accent to-accent/70 p-3 text-accent-ink">
        <div className="relative h-24 w-24 shrink-0 overflow-hidden bg-black/10 sm:h-28 sm:w-28">
          <QuanCover id={k.quan.id} icon="🍜" sizes="112px" />
        </div>
        <div className="min-w-0 py-1">
        <p className="text-xs font-medium uppercase tracking-wider opacity-80">⭐ Quán hợp nhất với đơn của bạn</p>
        <h3 className="text-xl font-semibold leading-snug tracking-tight">{k.quan.ten}</h3>
        <div className="mt-2 flex flex-wrap gap-1.5 text-xs">
          <span className="border border-ink/40 bg-black/15 px-2 py-0.5">📍 {k.quan.khoang_cach_km} km</span>
          {k.quan.muc_gia ? <span className="border border-ink/40 bg-black/15 px-2 py-0.5">{k.quan.muc_gia}</span> : null}
          {k.quan.danh_gia ? <span className="border border-ink/40 bg-black/15 px-2 py-0.5">★ {k.quan.danh_gia}{k.quan.so_danh_gia ? ` (${k.quan.so_danh_gia})` : ""}</span> : null}
          <span className="border border-ink/40 bg-black/15 px-2 py-0.5">🕒 {k.quan.gio_mo ?? "chưa rõ giờ mở"}</span>
          <button type="button" onClick={() => onOpenShop(k.quan!.id)} className="border border-ink/40 bg-white/90 px-2.5 py-0.5 font-semibold text-accent hover:bg-white">
            Xem menu quán →
          </button>
        </div>
        </div>
      </div>

      <div className="mt-3 border border-line bg-panel">
        <p className="flex items-center justify-between border-b border-line px-3 py-2 text-xs font-semibold text-muted">
          <span>Yêu cầu trong đơn → món quán đáp ứng</span>
          <span className="border border-ink bg-ok/15 px-2 py-0.5 text-ok">✓ đủ {k.mon.length}/{k.mon.length}</span>
        </p>
        <ul className="divide-y divide-line">
          {k.mon.map((m, i) => (
            <li key={i} className="anim-pop flex items-center gap-3 px-3 py-2" style={{ animationDelay: `${0.35 + i * 0.08}s` }}>
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

      <div className="mt-3 bg-soft px-4 py-3">
        <div className="flex items-baseline justify-between">
          <span className="text-sm text-muted">Tổng đơn (chưa gồm ship)</span>
          <span className="text-xl font-semibold tabular-nums">{vnd(k.tong_tien)}</span>
        </div>
        {k.ngan_sach ? <BudgetBar total={k.tong_tien ?? 0} budget={k.ngan_sach} /> : null}
      </div>

      <p className="mt-1.5 text-[11px] text-muted">Ảnh quán là ảnh minh hoạ do AI tạo (quán dựng giả).</p>
      {k.ly_do && <p className="mt-3 text-sm leading-relaxed">💬 {k.ly_do}</p>}
      {k.ai_bi_thay && (
        <p className="mt-2 border-l-[3px] border-warn bg-soft px-3 py-2 text-sm">
          Lựa chọn của AI không qua bước kiểm tra, đây là phương án code đã kiểm.
        </p>
      )}
      <Alternatives options={(k.lua_chon ?? []).slice(1)} budget={k.ngan_sach} onOpenShop={onOpenShop} />
      {k.hoi_them && <p className="mt-3 text-sm text-muted">💬 {k.hoi_them}</p>}
      {(k.canh_bao ?? []).map((w, i) => (
        <p key={i} className="mt-2 border-l-[3px] border-warn bg-soft px-3 py-2 text-sm">
          {w}
        </p>
      ))}
    </>
  );
}

function Alternatives({ options, budget, onOpenShop }: { options: LuaChon[]; budget?: number | null; onOpenShop: (id: string) => void }) {
  if (options.length === 0) return null;
  return (
    <div className="mt-4">
      <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted">Quán khác cũng đáp ứng đơn</p>
      <div className="grid gap-2">
        {options.map((o, i) => (
          <details key={o.quan.id} className="group border border-line bg-panel">
            <summary className="flex cursor-pointer list-none items-start gap-3 p-3">
              <span className="flex h-7 w-7 shrink-0 items-center justify-center bg-soft text-sm font-bold text-muted">{i + 2}</span>
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
              <button type="button" onClick={() => onOpenShop(o.quan.id)} className="mt-2 inline-block text-xs font-semibold text-accent hover:underline">
                Xem menu quán →
              </button>
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
  kind?: "feedback";      // bot: lời cảm ơn khi người dùng bấm "Tôi hài lòng" (chỉ ở giao diện, không gửi đi đâu)
  feedback?: boolean;     // bot: người dùng đã bấm "Tôi hài lòng" cho kết quả này
};

const newId = () => Math.random().toString(36).slice(2);

function Avatar() {
  return (
    <div className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-full border-2 border-ink bg-sun text-lg" aria-hidden>
      <CastImg k="think" className="h-full w-full object-cover" style={{ objectPosition: "50% 12%" }} fallback="🕵️" />
    </div>
  );
}

function UserAvatar() {
  return (
    <div className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-full border-2 border-ink bg-[#e8e2f5] text-lg" aria-hidden>
      <CastImg k="user" className="h-full w-full object-cover" style={{ objectPosition: "center 35%" }} fallback="🙂" />
    </div>
  );
}

function Typing() {
  // Chờ quá 10 giây thì nhắc nhẹ một câu, để người dùng biết hệ thống vẫn đang chạy chứ không treo
  const [slow, setSlow] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setSlow(true), 10000);
    return () => clearTimeout(t);
  }, []);
  return (
    <div className="flex items-end gap-2">
      <Avatar />
      <div className="anim-pop border-2 border-ink bg-panel px-4 py-3 shadow-[3px_3px_0_#242434]">
        <div className="flex items-center gap-3">
          <CastImg k="think" alt="" className="anim-wobble h-16 w-16 shrink-0 object-contain" />
          <div>
            <p className="text-sm font-semibold">Thám tử đang điều tra…</p>
            <span className="mt-1 flex gap-1" aria-label="Đang trả lời">
              {[0, 150, 300].map((d) => (
                <span key={d} className="h-2 w-2 animate-bounce rounded-full bg-accent" style={{ animationDelay: `${d}ms` }} />
              ))}
            </span>
          </div>
        </div>
        {slow && (
          <div className="mt-2 flex items-center gap-2 text-xs font-semibold text-brand">
            <CastImg k="duo" alt="" className="h-[60px] w-[72px] shrink-0 object-contain" />
            <span>Có người đang làm phiền, chờ thám tử một chút nhé!</span>
          </div>
        )}
      </div>
    </div>
  );
}

function BotBubble({ m, onFeedback, onOpenShop }: { m: Msg; onFeedback?: () => void; onOpenShop: (id: string) => void }) {
  if (m.kind === "feedback") {
    return (
      <div className="anim-pop flex items-start gap-2">
        <Avatar />
        <div className="flex max-w-[75%] items-center gap-3 border-2 border-ink bg-panel px-4 py-3 shadow-[3px_3px_0_#242434]">
          <CastImg k="happy" alt="" className="anim-cheer h-[72px] w-[80px] shrink-0 object-contain" fallback={<span className="text-3xl">😄</span>} />
          <p className="text-[15px] font-semibold leading-relaxed">Cảm ơn bạn! Mừng vì gợi ý hợp ý bạn!</p>
        </div>
      </div>
    );
  }
  const k = m.data?.ket_qua;
  const loai: Loai = k?.loai ?? "hoi_lai";
  const rich = k?.loai === "goi_y";
  return (
    <div className="anim-pop flex items-start gap-2">
      <Avatar />
      <div className={`min-w-0 ${rich ? "w-full max-w-[880px]" : "max-w-[75%]"}`}>
        <div className={` border-2 bg-panel ${rich ? "p-3" : "px-4 py-3"} ${m.error ? "border-bad/60" : "border-ink"}`}>
          {m.error ? (
            <p className="text-sm text-bad">Lỗi: {m.error}</p>
          ) : (
            <>
              {k?.che_do_gia && <p className="mb-2 text-xs font-medium text-warn">Chế độ giả: chưa nối model, đang dùng yêu cầu mẫu cố định.</p>}
              {rich && k ? (
                <Suggestion k={k} feedbackDone={m.feedback} onFeedback={onFeedback} onOpenShop={onOpenShop} />
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
            <span className={`border border-ink px-2 py-0.5 font-semibold ${BADGE[loai]}`}>{LABEL[loai]}</span>
            {m.merged && <span title={m.sent}>· có nhớ ngữ cảnh trước</span>}
          </div>
        )}
      </div>
    </div>
  );
}

function UserBubble({ m }: { m: Msg }) {
  return (
    <div className="anim-pop flex items-start justify-end gap-2">
      <p className="max-w-[80%] whitespace-pre-wrap border-2 border-ink bg-sun px-4 py-2.5 shadow-[3px_3px_0_#242434] text-[15px] font-semibold leading-relaxed text-ink">
        {m.text}
      </p>
      <UserAvatar />
    </div>
  );
}

const EX_ICON = ["👥", "🧾", "🍣", "🌙"];

function Welcome({ onPick, disabled, empty }: { onPick: (t: string) => void; disabled: boolean; empty: boolean }) {
  if (!empty) {
    return (
      <div className="anim-pop flex items-start gap-2">
        <Avatar />
        <p className="anim-pop border-2 border-ink bg-panel px-4 py-3 shadow-[3px_3px_0_#242434] text-[15px]">
          Chào bạn 👋 Kể yêu cầu của cả nhóm, mình chọn một quán hợp tất cả.
        </p>
      </div>
    );
  }
  return (
    <div className="mx-auto flex max-w-3xl flex-col items-center pb-8 pt-10 text-center">
      <CastImg
        k="point"
        alt=""
        className="anim-float h-28 w-auto object-contain"
        fallback={<div className="flex h-16 w-16 items-center justify-center border-2 border-ink bg-brand text-3xl">🕵️</div>}
      />
      <p className="mt-4 text-[11px] font-extrabold uppercase tracking-[0.1em] text-brand">Hồ sơ mới · Thám tử ẩm thực</p>
      <h2 className="anim-drop mt-1 text-2xl font-bold tracking-tight">Vụ án ăn gì hôm nay?</h2>
      <p className="mt-2 max-w-md text-[15px] leading-relaxed text-muted">
        Cứ kể như đang nhắn cho bạn: ai muốn ăn gì, ai kiêng gì, tầm bao nhiêu tiền, đi xa được không. Mình lọc ra vài quán{" "}
        <b className="text-ink">chiều được cả đơn</b>, kèm món gợi ý cho từng yêu cầu.
      </p>
      <p className="mt-6 w-full text-left text-[11px] font-extrabold uppercase tracking-[0.1em] text-brand">Chọn một vụ án mẫu</p>
      <div className="mt-2 grid w-full gap-2.5 text-left sm:grid-cols-2">
        {EXAMPLES.map(([name, t], i) => (
          <button
            key={name}
            type="button"
            disabled={disabled}
            onClick={() => onPick(t)}
            className="anim-pop press group flex gap-3 border-2 border-l-[6px] border-ink border-l-sun bg-panel p-3 text-left shadow-[3px_3px_0_#242434] hover:bg-sun/25 disabled:opacity-50" style={{ animationDelay: `${0.15 + i * 0.09}s` }}
          >
            <span className="flex h-9 w-9 shrink-0 items-center justify-center bg-soft text-lg group-hover:bg-sun/50">{EX_ICON[i]}</span>
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
  const [panelOpen, setPanelOpen] = useState(false); // chỉ dùng trên màn hình hẹp; màn rộng luôn hiện bên phải
  const [focusShop, setFocusShop] = useState<{ id: string; n: number } | null>(null);

  const bots = msgs.filter((m) => m.role === "bot" && m.kind !== "feedback");
  const lastBot = bots[bots.length - 1];
  const lkw = lastBot?.data?.ket_qua;
  const waitingAnswer = Boolean(lkw && (lkw.loai === "hoi_lai" || lkw.loai === "khong_co" || (lkw.cau_hoi?.length ?? 0) > 0 || lkw.hoi_them));

  const chosenId = [...bots].reverse().find((m) => m.data?.ket_qua?.loai === "goi_y")?.data?.ket_qua?.quan?.id;

  function openShop(id: string) {
    setPanelOpen(true);
    setFocusShop((f) => ({ id, n: (f?.n ?? 0) + 1 }));
  }

  function askAbout(q: Quan) {
    setInput(`Mình muốn ăn ở ${q.ten}, 2 người, tổng 150k`);
    setPanelOpen(false);
    inputRef.current?.focus();
  }

  async function send(raw: string) {
    const t = raw.trim();
    if (!t || loading) return;
    // Gửi kèm lịch sử hội thoại thật (vài lượt gần nhất) để bot hiểu bổ sung / sửa đơn ("không phải hàu", "ốc thì sao")
    const history = msgs.filter((m) => m.kind !== "feedback").slice(-8).map((m) =>
      m.role === "user" ? { role: "user", text: m.text } : { role: "bot", text: (m.data?.output ?? m.error ?? "").slice(0, 400) },
    );
    const sent = t;
    const userMsg: Msg = { id: newId(), role: "user", text: t };
    setMsgs((ms) => [...ms, userMsg]);
    setInput("");
    setLoading(true);
    const bot: Msg = { id: newId(), role: "bot", text: "", sent, merged: history.length > 0 };
    try {
      const r = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: sent, history }),
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

  // "Tôi hài lòng": chỉ là phản hồi ở giao diện (hiện lời cảm ơn), không gửi dữ liệu đi đâu
  function giveFeedback(id: string) {
    setMsgs((ms) => [...ms.map((x) => (x.id === id ? { ...x, feedback: true } : x)), { id: newId(), role: "bot", kind: "feedback", text: "" }]);
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
      <div className="mx-auto grid max-w-7xl gap-5 lg:grid-cols-[minmax(0,1fr)_380px]">
        {/* Khung chat */}
        <section className="anim-left flex h-[calc(100vh-8rem)] min-h-[560px] min-w-0 flex-col overflow-hidden border-2 border-ink bg-panel shadow-[6px_6px_0_#242434]">
          <div className="flex items-center justify-between gap-2 border-b-2 border-ink bg-brand px-5 py-3 text-brand-ink">
            <div className="flex items-center gap-3">
              <Avatar />
              <div>
                <p className="text-sm font-bold uppercase leading-tight tracking-[0.08em]">Hồ sơ vụ án ẩm thực</p>
                <p className="text-xs opacity-85">{loading ? "đang điều tra…" : "Chỉ gợi ý từ danh sách quán có sẵn"}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setPanelOpen(true)}
                className=" border-2 border-white/70 px-3 py-1.5 text-xs font-semibold hover:bg-white/15 lg:hidden"
              >
                Danh sách quán
              </button>
              <button
                type="button"
                onClick={reset}
                disabled={loading || msgs.length === 0}
                className=" border-2 border-white/70 px-3 py-1.5 text-xs font-semibold hover:bg-white/15 disabled:opacity-40"
              >
                ＋ Cuộc trò chuyện mới
              </button>
            </div>
          </div>

          <div className="flex-1 space-y-4 overflow-y-auto paper px-4 py-5">
            <Welcome onPick={send} disabled={loading} empty={msgs.length === 0} />
            {msgs.map((m) =>
              m.role === "user" ? (
                <UserBubble key={m.id} m={m} />
              ) : (
                <BotBubble key={m.id} m={m} onFeedback={() => giveFeedback(m.id)} onOpenShop={openShop} />
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
            className="border-t-2 border-ink bg-[#faf8fd] p-3"
          >
            {waitingAnswer && !loading && (
              <p className="mb-2 text-xs text-muted">↩ Trả lời / sửa đơn thoải mái (vd “không phải hàu”, “thêm 1 người”) — mình nhớ ngữ cảnh. Hỏi chuyện khác thì bấm “Cuộc trò chuyện mới”.</p>
            )}
            <div className="flex items-end gap-2 border-2 border-ink bg-panel px-3 py-2 focus-within:border-brand focus-within:ring-2 focus-within:ring-brand/25">
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
                className={`press flex h-9 w-9 shrink-0 items-center justify-center border-2 border-ink bg-accent text-accent-ink shadow-[2px_2px_0_#242434] disabled:opacity-40 ${input.trim() && !loading ? "anim-ring" : ""}`}
              >
                ➤
              </button>
            </div>
          </form>
        </section>

        {/* Danh sách quán: cột bên phải (màn rộng) hoặc lớp phủ (màn hẹp) */}
        <div className={`anim-right ${panelOpen ? "fixed inset-3 z-30" : "hidden"} lg:static lg:z-auto lg:block lg:h-[calc(100vh-8rem)] lg:min-h-[560px]`}>
          <ShopPanel chosenId={chosenId} focus={focusShop} onAsk={askAbout} onClose={() => setPanelOpen(false)} />
        </div>
      </div>
    </>
  );
}
