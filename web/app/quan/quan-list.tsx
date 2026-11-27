"use client";

import QuanCover from "../quan-cover";
import { useEffect, useRef, useState } from "react";
import { READ, vnd } from "../lib";
import type { DuLieu, Mon, Quan } from "../types";


function Tags({ m }: { m: Mon }) {
  return (
    <span className="flex flex-wrap gap-1">
      {m.chay === true && <span className="rounded bg-ok/15 px-1.5 text-[11px] font-medium text-ok">🌱 chay</span>}
      {m.co_nhac.length > 0 && (
        <span className="rounded bg-soft px-1.5 text-[11px] text-muted">có {m.co_nhac.map((c) => READ[c] ?? c).join(", ")}</span>
      )}
      {!m.ghi_thanh_phan && <span className="rounded bg-warn/15 px-1.5 text-[11px] text-warn">không ghi mô tả</span>}
    </span>
  );
}

// Loại quán (để chọn biểu tượng khi quán chưa có ảnh). Ảnh quán: web/public/img/quan/<id>.webp (gpt-image-2)
// quán chay: không dùng ảnh (ảnh có sẵn đều có thịt) → biểu tượng
const COVER: [RegExp, string][] = [[/chay/i, ""], [/^bếp/i, "com"], [/phở/i, "pho"], [/bún/i, "bun"], [/cơm/i, "com"], [/bánh mì/i, "banh_mi"], [/lẩu/i, "lau"]];
const coverOf = (q: Quan) => COVER.find(([re]) => re.test(q.ten) || re.test(q.am_thuc))?.[1] || undefined;
const iconOf = (q: Quan) => (/chay/i.test(q.am_thuc) ? "🌱" : /mì|miến/i.test(q.am_thuc) ? "🍜" : "🍽️");

function QuanCard({ q, active, chosen, onClick }: { q: Quan; active: boolean; chosen: boolean; onClick: () => void }) {
  const veg = q.mon.filter((m) => m.chay === true).length;
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`group overflow-hidden rounded-xl border bg-panel text-left transition hover:-translate-y-0.5 hover:shadow-md ${
        active ? "border-accent ring-2 ring-accent/30" : "border-line hover:border-accent/60"
      }`}
    >
      <div className="relative h-32 overflow-hidden bg-soft">
        <QuanCover id={q.id} fallback={coverOf(q)} icon={iconOf(q)} sizes="(min-width: 1024px) 360px, 50vw" className="transition duration-300 group-hover:scale-105" />
        <span className="absolute inset-0 bg-gradient-to-t from-black/35 to-transparent" />
      </div>
      <div className="p-3">
      <div className="flex items-start justify-between gap-2">
        <p className="line-clamp-2 font-semibold leading-snug">{q.ten}</p>
        {chosen && <span className="shrink-0 rounded-full bg-ok px-2 py-0.5 text-[10px] font-semibold text-white">Đang gợi ý</span>}
      </div>
      <p className="mt-1 text-xs text-muted">
        {q.am_thuc} · {q.khoang_cach_km} km{q.danh_gia ? ` · ★ ${q.danh_gia} (${q.so_danh_gia ?? 0} đánh giá)` : ""} · {q.mon.length} món
      </p>
      <div className="mt-2 flex flex-wrap gap-1">
        {veg > 0 && <span className="rounded bg-ok/15 px-1.5 text-[11px] font-medium text-ok">🌱 {veg} món chay</span>}
        {q.freeship && <span className="rounded bg-accent/15 px-1.5 text-[11px] text-accent">freeship</span>}
        {q.gio_mo && <span className="rounded bg-soft px-1.5 text-[11px] text-muted">🕒 {q.gio_mo}</span>}
      </div>
      </div>
    </button>
  );
}

export default function QuanList() {
  const [data, setData] = useState<DuLieu | null>(null);
  const [open, setOpen] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [chosenId, setChosenId] = useState<string | undefined>(undefined);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch("/api/quan")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((d: DuLieu) => {
        setData(d);
        // quán vừa được gợi ý trong trang chat (hội thoại lưu ở sessionStorage)
        try {
          const msgs = JSON.parse(sessionStorage.getItem("malto-chat") || "[]");
          const last = [...msgs].reverse().find((m: { data?: { ket_qua?: { loai?: string; quan?: { id: string } } } }) => m.data?.ket_qua?.loai === "goi_y");
          setChosenId(last?.data?.ket_qua?.quan?.id);
        } catch {}
        // /quan?open=Q05 → mở sẵn menu quán đó (link "Xem menu quán" từ trang chat)
        const id = new URLSearchParams(window.location.search).get("open");
        if (id) {
          setOpen(id);
          setTimeout(() => menuRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
        }
      })
      .catch(() => setData({ _ghi_chu: "", quan: [] }));
  }, []);

  if (!data) return <p className="text-sm text-muted">Đang tải dữ liệu quán…</p>;
  const ql = query.trim().toLowerCase();
  const list = ql
    ? data.quan.filter((q) => q.ten.toLowerCase().includes(ql) || q.am_thuc.toLowerCase().includes(ql) || q.mon.some((m) => m.ten.toLowerCase().includes(ql)))
    : data.quan;
  const sel = data.quan.find((q) => q.id === open);
  return (
    <>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Tìm quán hoặc món (vd: bún, phở, chay)…"
        className="mb-3 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm outline-none focus:border-accent"
      />
      <p className="mb-3 text-xs text-muted">{list.length} quán</p>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {list.map((q) => (
          <QuanCard key={q.id} q={q} active={open === q.id} chosen={chosenId === q.id} onClick={() => setOpen(open === q.id ? null : q.id)} />
        ))}
      </div>
      {sel && (
        <div ref={menuRef} className="mt-4 scroll-mt-4 rounded-xl border border-line bg-bg/60 p-4">
          <div className="mb-3 flex items-baseline justify-between gap-2">
            <h3 className="text-lg font-semibold">Menu · {sel.ten}</h3>
            <button type="button" onClick={() => setOpen(null)} className="text-sm text-muted hover:text-ink">
              Đóng ✕
            </button>
          </div>
          {sel.khuyen_mai && <p className="mb-3 text-xs text-accent">🎁 {sel.khuyen_mai}</p>}
          <ul className="grid gap-x-6 sm:grid-cols-2">
            {sel.mon.map((m) => (
              <li key={m.id} className="border-t border-line py-2">
                <div className="flex items-baseline justify-between gap-2">
                  <p className="text-sm font-medium leading-snug">{m.ten}</p>
                  <p className="shrink-0 text-sm tabular-nums text-accent">{vnd(m.gia)}</p>
                </div>
                {m.mo_ta && <p className="mt-0.5 line-clamp-2 text-xs text-muted">{m.mo_ta}</p>}
                <div className="mt-1">
                  <Tags m={m} />
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}

