import type { Metadata } from "next";
import { Be_Vietnam_Pro } from "next/font/google";
import "./globals.css";
import Nav from "./nav";

const font = Be_Vietnam_Pro({ subsets: ["vietnamese", "latin"], weight: ["400", "500", "600", "700"], variable: "--font-bvp", display: "swap" });

export const metadata: Metadata = {
  title: "Chọn quán cho nhóm · MALTO",
  description: "Bản chạy thử: AI chọn một quán và một món cho từng người trong nhóm, theo ăn chay, dị ứng, ngân sách.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="vi" className={`${font.variable} h-full antialiased`}>
      <body className="min-h-full">
        <Nav />
        <main className="mx-auto max-w-6xl px-4 pb-16 pt-5">{children}</main>
      </body>
    </html>
  );
}
