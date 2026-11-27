import type { Metadata } from "next";
import "./globals.css";
import Nav from "./nav";

export const metadata: Metadata = {
  title: "Chọn quán cho nhóm · MALTO",
  description: "Bản chạy thử: AI chọn một quán và một món cho từng người trong nhóm, theo ăn chay, dị ứng, ngân sách.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="vi" className="h-full antialiased">
      <body className="min-h-full">
        <main className="mx-auto max-w-6xl px-4 pb-16 pt-6">
          <Nav />
          {children}
        </main>
      </body>
    </html>
  );
}
