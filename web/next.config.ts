import type { NextConfig } from "next";

// Backend Python (codebase/web.py) chạy ở cổng 8010. Next proxy /api/* sang đó, nên trình duyệt
// chỉ gọi cùng origin, không cần CORS. Đổi cổng backend: BACKEND_URL=http://127.0.0.1:8020 npm run dev
const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:8010";

const nextConfig: NextConfig = {
  cacheComponents: true,
  // Agent gọi model 2 lần, có lúc chậm → cho proxy /api chờ tối đa 180 giây (mặc định 30 giây → lỗi 500)
  experimental: { proxyTimeout: 180000 },
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  // Ảnh quán web/public/img/quan; search khớp IMG_VERSION trong app/quan-cover.tsx
  images: { localPatterns: [{ pathname: "/img/**", search: "?v=2" }] },
  rewrites() {
    return [{ source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` }];
  },
};

export default nextConfig;
