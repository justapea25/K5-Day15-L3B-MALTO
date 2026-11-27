"use client";

import Image from "next/image";
import { useState } from "react";

// Tăng số này mỗi khi sinh lại ảnh (scripts/gen_images.py), để trình duyệt không dùng ảnh cũ trong bộ nhớ tạm.
// Nhớ sửa cả `search` trong images.localPatterns ở next.config.ts cho khớp.
export const IMG_VERSION = "2";

const EMOJI: Record<string, string> = {
  bun: "🍜", pho: "🍜", mi: "🍜", com: "🍚", banh_mi: "🥖", lau: "🍲", khac: "🥢", quan: "🏪",
};

/** Ảnh minh hoạ (do AI tạo, ở web/public/img). Chưa có ảnh thì hiện emoji theo loại món. */
export function Photo({
  kind, id, loai, alt, sizes, className = "",
}: { kind: "quan" | "mon"; id: string; loai?: string; alt: string; sizes: string; className?: string }) {
  const [failed, setFailed] = useState(false);
  return (
    <div className={`relative overflow-hidden bg-soft ${className}`}>
      {failed ? (
        <div className="flex h-full w-full items-center justify-center text-3xl" aria-label={alt}>
          {EMOJI[kind === "quan" ? "quan" : loai ?? "khac"] ?? "🥢"}
        </div>
      ) : (
        <Image src={`/img/${kind}/${id}.webp?v=${IMG_VERSION}`} alt={alt} fill sizes={sizes} className="object-cover" onError={() => setFailed(true)} />
      )}
    </div>
  );
}
