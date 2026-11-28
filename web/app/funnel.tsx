"use client";

import { useEffect, useMemo, useState } from "react";
import { vnd } from "./lib";
import type { DuLieu, PhanTich } from "./types";

// Danh sách quán dùng chung cho mọi lần vẽ (chỉ tải một lần)
let quanPromise: Promise<DuLieu["quan"]> | null = null;
function loadQuan() {
  quanPromise ??= fetch("/api/quan")
    .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
    .then((d: DuLieu) => d.quan)
    .catch(() => {
      quanPromise = null;
      return [];
    });
  return quanPromise;
}

const SIZE = 300;
const C = SIZE / 2;
const R = 132;

/** "MealMate đã lọc thế nào": radar khoảng cách + phễu các bước lọc, phát lại từng bước sau khi có đáp án.
 *  Số liệu (số quán còn lại ở mỗi bước, quán nào bị loại ở bước nào) do backend ghi lại khi lọc thật.
 *  Dữ liệu không có toạ độ: khoảng cách từ tâm là thật, hướng của chấm chỉ để minh hoạ. */
export default function Funnel({ pt, chosenId, altIds }: { pt: PhanTich; chosenId?: string; altIds: string[] }) {
  const [quan, setQuan] = useState<DuLieu["quan"]>([]);
  const [step, setStep] = useState(0);
  const [run, setRun] = useState(0);

  useEffect(() => {
    let live = true;
    loadQuan().then((q) => live && setQuan(q));
    return () => {
      live = false;
    };
  }, []);

  const ready = quan.length > 0;
  useEffect(() => {
    if (!ready) return;
    let n = 0;
    let iv: ReturnType<typeof setInterval> | undefined;
    const t = setTimeout(() => {
      iv = setInterval(() => {
        n += 1;
        setStep(n);
        if (n >= 4 && iv) clearInterval(iv);
      }, 1100);
    }, 700);
    return () => {
      clearTimeout(t);
      if (iv) clearInterval(iv);
    };
  }, [ready, run]);

  const maxKm = Math.max(5, Math.ceil(Math.max(0, ...quan.map((q) => q.khoang_cach_km))));
  const dots = useMemo(() => {
    const sorted = [...quan].sort((a, b) => a.id.localeCompare(b.id));
    return sorted.map((q, i) => {
      const ang = (i * 137.508 * Math.PI) / 180;
      const rr = R * Math.sqrt(Math.min(q.khoang_cach_km, maxKm) / maxKm);
      return { id: q.id, ten: q.ten, x: C + rr * Math.cos(ang), y: C + rr * Math.sin(ang) };
    });
  }, [quan, maxKm]);

  const rings = [1, 2, 5, maxKm].filter((v, i, a) => v <= maxKm && a.indexOf(v) === i);
  const radius = (km: number) => R * Math.sqrt(km / maxKm);
  const steps = [
    { ten: "Tất cả quán trong dữ liệu", n: pt.buoc[0] },
    { ten: pt.max_km != null ? `Trong ${pt.max_km} km và đang mở cửa` : "Còn mở cửa / đúng tên quán", n: pt.buoc[1] },
    { ten: pt.so_nguoi > 1 ? `Ai trong ${pt.so_nguoi} người cũng có món ăn được` : "Có món hợp yêu cầu", n: pt.buoc[2] },
    { ten: pt.ngan_sach ? `Vừa ngân sách ${vnd(pt.ngan_sach)}` : "Không giới hạn ngân sách", n: pt.buoc[3] },
    { ten: chosenId ? "Xếp hạng và chọn 1 quán" : "Không còn quán nào để chọn", n: chosenId ? 1 : 0 },
  ];
  const alive = (id: string) => {
    const b = pt.quan[id] ?? 0;
    return step <= 0 ? true : step >= 4 ? b >= 3 : b >= step;
  };
  const chosen = dots.find((d) => d.id === chosenId);
  const label = chosen && step >= 4 ? chosen.ten : "";

  return (
    <div className="anim-pop mt-3 border-2 border-ink bg-panel shadow-[3px_3px_0_#242434]">
      <div className="flex items-center justify-between gap-2 border-b-2 border-ink bg-sun px-3 py-2">
        <p className="text-xs font-extrabold uppercase tracking-[0.08em]">MealMate đã lọc thế nào</p>
        <button
          type="button"
          onClick={() => {
            setStep(0);
            setRun((r) => r + 1);
          }}
          className="press border-2 border-ink bg-panel px-2 py-0.5 text-[11px] font-bold shadow-[2px_2px_0_#242434]"
        >
          ▶ Phát lại
        </button>
      </div>

      <div className="grid gap-4 p-3 sm:grid-cols-[minmax(0,300px)_1fr]">
        <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="mx-auto w-full max-w-[300px]" role="img" aria-label="Bản đồ khoảng cách của các quán quanh bạn">
          <rect x="1" y="1" width={SIZE - 2} height={SIZE - 2} fill="#f1ebfa" stroke="#242434" strokeWidth="2" />
          {rings.map((km) => (
            <g key={km}>
              <circle cx={C} cy={C} r={radius(km)} fill="none" stroke="#cfc5dc" strokeWidth="1" strokeDasharray="3 4" />
              <text x={C + 3} y={C - radius(km) + 10} fontSize="9" fill="#615a6b">{km} km</text>
            </g>
          ))}
          {pt.max_km != null && (
            <circle cx={C} cy={C} r={radius(Math.min(pt.max_km, maxKm))} fill="rgba(217,61,36,0.07)" stroke="#d93d24" strokeWidth="2" strokeDasharray="6 4" />
          )}
          {dots.map((d) => {
            const on = alive(d.id);
            const isChosen = d.id === chosenId && step >= 4;
            const isAlt = altIds.includes(d.id) && step >= 4;
            return (
              <circle
                key={d.id}
                cx={d.x}
                cy={d.y}
                r={isChosen ? 0 : isAlt ? 5 : on ? 4 : 2.5}
                fill={isAlt ? "#ff9b3d" : on ? "#674795" : "#b9afc6"}
                stroke={isAlt ? "#242434" : "none"}
                strokeWidth="1.5"
                opacity={on ? 1 : 0.35}
                style={{ transition: "all .6s ease" }}
              />
            );
          })}
          {chosen && step >= 4 && (
            <g>
              <circle cx={chosen.x} cy={chosen.y} r="16" fill="none" stroke="#d93d24" strokeWidth="2" className="anim-ring-svg" />
              <circle cx={chosen.x} cy={chosen.y} r="9" fill="#ffd23f" stroke="#242434" strokeWidth="2.5" className="anim-pop-svg" />
              <text x={chosen.x} y={chosen.y + 3.5} textAnchor="middle" fontSize="10" fontWeight="800" fill="#242434">★</text>
            </g>
          )}
          <g>
            <circle cx={C} cy={C} r="7" fill="#d93d24" stroke="#242434" strokeWidth="2.5" />
            <text x={C} y={C + 20} textAnchor="middle" fontSize="10" fontWeight="800" fill="#242434">Bạn</text>
          </g>
        </svg>

        <div className="min-w-0">
          <ol className="space-y-2">
            {steps.map((s, i) => {
              const shown = step >= i;
              const current = step === i;
              const pct = pt.tong ? Math.max(s.n > 0 ? 4 : 0, Math.round((s.n / pt.tong) * 100)) : 0;
              return (
                <li key={s.ten} className={`transition-opacity duration-500 ${shown ? "opacity-100" : "opacity-25"}`}>
                  <div className="flex items-baseline justify-between gap-2 text-sm">
                    <span className={`min-w-0 ${current ? "font-bold" : "font-medium"}`}>
                      <span className="mr-1.5 inline-block w-4 text-center text-xs text-muted">{i + 1}</span>
                      {s.ten}
                    </span>
                    <span className={`shrink-0 tabular-nums ${i === 4 && s.n === 0 ? "text-bad" : "text-accent"} font-bold`}>{shown ? s.n : "…"}</span>
                  </div>
                  <div className="ml-5 mt-1 h-2.5 border border-ink bg-soft">
                    <div
                      className={`h-full ${i === 4 ? "bg-sun" : i === 3 ? "bg-ok" : "bg-brand"}`}
                      style={{ width: shown ? `${pct}%` : "0%", transition: "width .8s cubic-bezier(.22,1,.36,1)" }}
                    />
                  </div>
                </li>
              );
            })}
          </ol>
          {label && <p className="anim-pop mt-3 border-2 border-ink bg-sun/50 px-2 py-1 text-xs font-bold">★ {label}</p>}
          <p className="mt-3 text-[11px] leading-snug text-muted">
            Số liệu lấy từ bước lọc thật của hệ thống. Khoảng cách từ tâm là thật; hướng của chấm chỉ để minh hoạ vì dữ liệu không có toạ độ.
          </p>
        </div>
      </div>
    </div>
  );
}
