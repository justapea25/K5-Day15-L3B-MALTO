import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chọn quán cho nhóm · MALTO",
  description: "Bản chạy thử: AI chọn một quán và một món cho từng người trong nhóm, theo ăn chay, dị ứng, ngân sách.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="vi" className="h-full antialiased">
      <body className="min-h-full">{children}</body>
    </html>
  );
}
