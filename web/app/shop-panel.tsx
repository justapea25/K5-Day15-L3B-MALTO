"use client";

import { useEffect, useRef, useState } from "react";
import { vnd } from "./lib";
import QuanCover from "./quan-cover";
import { Tags, coverOf, iconOf } from "./quan/quan-list";
import type { DuLieu, Quan } from "./types";

/** Danh sách quán dạng thanh bên, nằm ngay cạnh khung chat: xem menu, hỏi trợ lý về một quán mà không phải chuyển trang.
 *  - `chosenId`: quán trợ lý vừa gợi ý (hiện nhãn "Đang gợi ý")
 *  - `focus`: mỗi lần `n` đổi thì mở menu quán `id` và cuộn tới đó (bấm "Xem menu quán" trong kết quả chat)
 *  - `onAsk`: bấm "Hỏi trợ lý về quán này" → cha điền câu hỏi vào ô chat */
export default function ShopPanel({ chosenId, focus, onAsk, onClose }: {
  chosenId?: string;
  focus: { id: string; n: number } | null;
  onAsk: (q: Quan) => void;
  onClose?: () => void;
}) {
  const [data, setData] = useState<DuLieu | null>(null);
  const [open, setOpen] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const rows = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    fetch("/api/quan")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(setData)
      .catch(() => setData({ _ghi_chu: "", quan: [] }));
  }, []);

  // Điều chỉnh state ngay khi render (không dùng effect): mỗi lần `focus.n` đổi thì xoá tìm kiếm và mở quán đó
  const [seen, setSeen] = useState(0);
  if (focus && focus.n !== seen) {
    setSeen(focus.n);
    setQuery("");
    setOpen(focus.id);
  }

  useEffect(() => {
    if (!focus) return;
    const t = setTimeout(() => rows.current[focus.id]?.scrollIntoView({ behavior: "smooth", block: "nearest" }), 80);
    return () => clearTimeout(t);
  }, [focus]);

  const ql = query.trim().toLowerCase();
  const list = !data
    ? []
    : ql
      ? data.quan.filter((q) => q.ten.toLowerCase().includes(ql) || q.am_thuc.toLowerCase().includes(ql) || q.mon.some((m) => m.ten.toLowerCase().includes(ql)))
      : data.quan;

  return (
    <aside className="flex h-full min-h-0 flex-col overflow-hidden border-2 border-ink bg-panel shadow-[6px_6px_0_#242434]">
      <div className="flex items-center justify-between gap-2 border-b-2 border-ink bg-sun px-4 py-3">
        <div>
          <p className="text-sm font-bold uppercase leading-tight tracking-[0.08em]">Danh sách quán</p>
          <p className="text-xs text-ink/75">{data ? `${list.length} / ${data.quan.length} quán` : "Đang tải…"} · bấm một quán để xem menu</p>
        </div>
        {onClose && (
          <button type="button" onClick={onClose} className=" border-2 border-ink bg-panel px-3 py-1 text-xs font-bold lg:hidden">
            Đóng
          </button>
        )}
      </div>

      <div className="border-b border-line p-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Tìm quán hoặc món (vd: bún, phở, chay)…"
          className="w-full border-2 border-ink bg-panel px-3 py-2 text-sm outline-none focus:border-brand focus:ring-2 focus:ring-brand/25"
        />
      </div>

      <div className="paper-purple min-h-0 flex-1 space-y-2 overflow-y-auto p-3">
        {data && list.length === 0 && <p className="py-6 text-center text-sm text-muted">Không có quán nào khớp.</p>}
        {list.map((q, idx) => {
          const active = open === q.id;
          const veg = q.mon.filter((m) => m.chay === true).length;
          return (
            <div
              key={q.id}
              ref={(el) => {
                rows.current[q.id] = el;
              }}
              style={{ animationDelay: `${Math.min(idx, 10) * 0.04}s` }}
              className={`anim-pop press overflow-hidden border-2 bg-panel shadow-[3px_3px_0_#242434] ${active ? "border-brand ring-2 ring-brand/25" : "border-ink"}`}
            >
              <button type="button" onClick={() => setOpen(active ? null : q.id)} aria-expanded={active} className="flex w-full items-center gap-3 p-2 text-left hover:bg-sun/20">
                <div className="relative h-14 w-14 shrink-0 overflow-hidden bg-soft">
                  <QuanCover id={q.id} fallback={coverOf(q)} icon={iconOf(q)} sizes="56px" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-2">
                    <p className="line-clamp-1 text-sm font-semibold leading-snug">{q.ten}</p>
                    {chosenId === q.id && <span className="shrink-0 border border-ink bg-ok px-2 py-0.5 text-[10px] font-semibold text-white">Đang gợi ý</span>}
                  </div>
                  <p className="line-clamp-1 text-xs text-muted">
                    {q.am_thuc} · {q.khoang_cach_km} km{q.danh_gia ? ` · ★ ${q.danh_gia}` : ""} · {q.mon.length} món
                  </p>
                  <div className="mt-0.5 flex flex-wrap gap-1">
                    {veg > 0 && <span className=" bg-ok/15 px-1.5 text-[10px] font-medium text-ok">🌱 {veg} món chay</span>}
                    {q.freeship && <span className=" bg-accent/15 px-1.5 text-[10px] text-accent">freeship</span>}
                  </div>
                </div>
              </button>

              {active && (
                <div className="anim-unfold border-t-2 border-ink bg-[#faf8fd] p-3">
                  {q.gio_mo && <p className="mb-1 text-xs text-muted">🕒 {q.gio_mo}</p>}
                  {q.khuyen_mai && <p className="mb-2 text-xs text-accent">🎁 {q.khuyen_mai}</p>}
                  <ul className="max-h-64 divide-y divide-line overflow-y-auto pr-1">
                    {q.mon.map((m) => (
                      <li key={m.id} className="py-1.5">
                        <div className="flex items-baseline justify-between gap-2">
                          <p className="text-sm font-medium leading-snug">{m.ten}</p>
                          <p className="shrink-0 text-sm tabular-nums text-accent">{vnd(m.gia)}</p>
                        </div>
                        {m.mo_ta && <p className="mt-0.5 line-clamp-2 text-xs text-muted">{m.mo_ta}</p>}
                        <div className="mt-0.5">
                          <Tags m={m} />
                        </div>
                      </li>
                    ))}
                  </ul>
                  <button
                    type="button"
                    onClick={() => onAsk(q)}
                    className="mt-3 w-full border-2 border-ink bg-accent px-3 py-2 text-sm font-bold text-accent-ink shadow-[3px_3px_0_#242434] hover:brightness-110 active:translate-x-[2px] active:translate-y-[2px] active:shadow-none"
                  >
                    Hỏi trợ lý về quán này
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
      <p className="border-t border-line px-3 py-2 text-[11px] text-muted">Quán dựng giả · ảnh minh hoạ do AI tạo · nhãn chay / thành phần gắn theo tên và mô tả món, có thể thiếu.</p>
    </aside>
  );
}
