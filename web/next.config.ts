import type { NextConfig } from "next";

// Backend Python (codebase/web.py) chạy ở cổng 8010. Next proxy /api/* sang đó, nên trình duyệt
// chỉ gọi cùng origin, không cần CORS. Đổi cổng backend: BACKEND_URL=http://127.0.0.1:8020 npm run dev
const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:8010";

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  rewrites() {
    return [{ source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` }];
  },
};

export default nextConfig;
