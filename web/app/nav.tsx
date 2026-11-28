"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Nav() {
  const [down, setDown] = useState(false);

  // Chỉ để biết backend có sống không (hiện thanh cảnh báo bên dưới); không còn hiển thị tên model
  useEffect(() => {
    fetch("/api/info")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .catch(() => setDown(true));
  }, []);

  return (
    <>
      <header className="anim-drop sticky top-0 z-20 border-b border-line/70 bg-bg/75 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center px-4 py-3">
          <Link href="/" className="flex items-center gap-3">
            <span aria-hidden className="logo-mark grid h-12 w-12 place-items-center border-2 border-ink bg-brand text-2xl font-black text-brand-ink">M</span>
            <span className="flex flex-col leading-tight">
              <span className="text-[10px] font-extrabold uppercase tracking-[0.12em] text-brand">MALTO · Track D</span>
              <span className="text-[15px] font-bold tracking-wide">MEALMATE</span>
              <span className="mt-0.5 text-[11px] text-muted">Chọn quán cho cả nhóm, mỗi người một món</span>
            </span>
          </Link>
        </div>
      </header>

      {down && (
        <p className="mx-auto mt-4 max-w-7xl border border-bad/40 bg-bad/10 px-4 py-3 text-sm text-bad">
          Không kết nối được backend. Chạy <code className="font-mono">python codebase/web.py</code> ở thư mục gốc repo rồi tải lại trang.
        </p>
      )}
    </>
  );
}
