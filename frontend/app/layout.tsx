import type { Metadata } from "next";
import type { ReactNode } from "react";
import "../styles/globals.css";
import { Providers } from "@/components/providers";

export const metadata: Metadata = {
  title: "InterviewVerse AI",
  description: "InterviewVerse AI frontend foundation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen overflow-x-hidden bg-background font-sans text-foreground antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
