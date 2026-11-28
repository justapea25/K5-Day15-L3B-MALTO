"use client";

import { useState, type CSSProperties } from "react";

// Ảnh nhân vật nằm ở web/public/characters/ và KHÔNG được commit (đã loại trừ qua .git/info/exclude):
// đây là tranh có bản quyền, chỉ dùng cục bộ cho học nhóm. Thiếu file → tự quay về `fallback`,
// nên ai clone repo vẫn chạy bình thường, chỉ không có tranh.
const FILES = {
  think: "thinking.webp", // đang suy nghĩ: ảnh đại diện bot + lúc chờ
  point: "pointing.webp", // chỉ vào kết quả
  happy: "happy.webp",    // phản hồi khi người dùng hài lòng
  user: "user.webp",      // ảnh đại diện người dùng
  duo: "duo.webp",        // nhắc khi chờ quá lâu
} as const;

export type CastKey = keyof typeof FILES;

export function CastImg({ k, alt = "", className = "", style, fallback = null }: {
  k: CastKey; alt?: string; className?: string; style?: CSSProperties; fallback?: React.ReactNode;
}) {
  const [bad, setBad] = useState(false);
  if (bad) return <>{fallback}</>;
  // Ảnh nhỏ (vài chục KB) và có cơ chế quay về fallback khi 404, nên dùng <img> thường thay vì next/image.
  // eslint-disable-next-line @next/next/no-img-element
  return <img src={`/characters/${FILES[k]}`} alt={alt} className={className} style={style} onError={() => setBad(true)} />;
}
