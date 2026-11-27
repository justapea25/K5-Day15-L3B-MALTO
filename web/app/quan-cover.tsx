"use client";

import Image from "next/image";
import { useState } from "react";

/** Ảnh minh hoạ mặt tiền quán (AI tạo, web/public/img/quan/<id>.webp — quán dựng giả).
 *  Mọi quán trong data đều có ảnh; thiếu ảnh (khi thêm quán mới) → biểu tượng. */
export default function QuanCover({ id, fallback, icon, sizes, className = "" }: {
  id: string; fallback?: string; icon: string; sizes: string; className?: string;
}) {
  const [step, setStep] = useState(0);
  void fallback; // giữ tham số cho tương thích, không còn ảnh theo loại món
  const src = step === 0 ? `/img/quan/${id}.webp` : null;
  return src ? (
    <Image src={src} alt="" fill sizes={sizes} className={`object-cover ${className}`} onError={() => setStep(1)} />
  ) : (
    <span className="flex h-full items-center justify-center bg-gradient-to-br from-ok/20 to-soft text-4xl">{icon}</span>
  );
}
