"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const TABS = [
  { href: "/", label: "💬 Trợ lý chọn quán" },
  { href: "/quan", label: "🔎 Danh sách quán" },
];

export default function Nav() {
  const path = usePathname();
  const [model, setModel] = useState<{ provider: string; model: string } | null>(null);
  const [down, setDown] = useState(false);

  useEffect(() => {
    fetch("/api/info")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(setModel)
      .catch(() => setDown(true));
  }, []);

  return (
    <>
      <header className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-accent">MALTO · Track D</p>
          <h1 className="text-3xl font-semibold tracking-tight">🍜 Chọn quán cho nhóm</h1>
        </div>
        <div className="rounded-full border border-line bg-panel px-3 py-1 text-xs text-muted">
          model: <b className="font-semibold text-ink">{model?.model ?? "…"}</b>
          {model?.provider === "fake" && <span className="text-warn"> · chế độ giả</span>}
        </div>
      </header>

      <nav className="mb-5 flex gap-1 rounded-xl border border-line bg-panel p-1" aria-label="Chuyển trang">
        {TABS.map((t) => {
          const active = path === t.href;
          return (
            <Link
              key={t.href}
              href={t.href}
              aria-current={active ? "page" : undefined}
              className={`flex-1 rounded-lg px-4 py-2 text-center text-sm font-semibold transition ${
                active ? "bg-accent text-accent-ink" : "text-muted hover:bg-soft hover:text-ink"
              }`}
            >
              {t.label}
            </Link>
          );
        })}
      </nav>

      {down && (
        <p className="mb-4 rounded-lg border border-bad/40 bg-bad/10 px-4 py-3 text-sm text-bad">
          Không kết nối được backend. Chạy <code className="font-mono">python codebase/web.py</code> ở thư mục gốc repo rồi tải lại trang.
        </p>
      )}
    </>
  );
}
