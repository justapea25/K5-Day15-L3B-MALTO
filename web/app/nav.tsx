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
      <header className="sticky top-0 z-20 border-b border-line/70 bg-bg/75 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-4 gap-y-2 px-4 py-3">
          <Link href="/" className="flex items-center gap-2.5">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-accent to-accent/60 text-lg shadow-sm">🍜</span>
            <span className="leading-tight">
              <span className="block text-[15px] font-bold tracking-tight">Chọn quán cho nhóm</span>
              <span className="block text-[11px] font-semibold uppercase tracking-[0.16em] text-accent">MALTO · Track D</span>
            </span>
          </Link>

          <nav className="order-3 flex w-full gap-1 rounded-xl border border-line bg-panel p-1 sm:order-none sm:ml-auto sm:w-auto" aria-label="Chuyển trang">
            {TABS.map((t) => {
              const active = path === t.href;
              return (
                <Link
                  key={t.href}
                  href={t.href}
                  aria-current={active ? "page" : undefined}
                  className={`flex-1 whitespace-nowrap rounded-lg px-4 py-1.5 text-center text-sm font-semibold transition sm:flex-none ${
                    active ? "bg-accent text-accent-ink shadow-sm" : "text-muted hover:bg-soft hover:text-ink"
                  }`}
                >
                  {t.label}
                </Link>
              );
            })}
          </nav>

          <div className="ml-auto flex items-center gap-1.5 rounded-full border border-line bg-panel px-3 py-1 text-xs text-muted sm:ml-0">
            <span className={`h-2 w-2 rounded-full ${down ? "bg-bad" : model ? "bg-ok" : "bg-line"}`} aria-hidden />
            <b className="font-semibold text-ink">{model?.model ?? "…"}</b>
            {model?.provider === "fake" && <span className="text-warn">· chế độ giả</span>}
          </div>
        </div>
      </header>

      {down && (
        <p className="mx-auto mt-4 max-w-6xl rounded-lg border border-bad/40 bg-bad/10 px-4 py-3 text-sm text-bad">
          Không kết nối được backend. Chạy <code className="font-mono">python codebase/web.py</code> ở thư mục gốc repo rồi tải lại trang.
        </p>
      )}
    </>
  );
}
