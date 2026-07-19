import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import "../styles/globals.css";
import { Providers } from "@/components/providers";

const baseUrl =
  process.env.NEXT_PUBLIC_APP_URL?.trim() || "https://interviewverse-ai.example.com";

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: "InterviewVerse AI - Standardized Interviewing Platform",
    template: "%s | InterviewVerse AI",
  },
  description: "An AI-powered dashboard workspace to manage interview personas, conduct live mock interviews, evaluate transcripts, and review performance reports.",
  applicationName: "InterviewVerse AI",
  keywords: ["AI Interview", "Tech Interview Prep", "Persona Builder", "Automated Evaluations", "Mock Interviews"],
  authors: [{ name: "InterviewVerse AI Team" }],
  creator: "InterviewVerse AI Team",
  publisher: "InterviewVerse AI Team",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: baseUrl,
    siteName: "InterviewVerse AI",
    title: "InterviewVerse AI - Standardized Interviewing Platform",
    description: "An AI-powered dashboard workspace to manage interview personas, conduct live mock interviews, evaluate transcripts, and review performance reports.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "InterviewVerse AI Dashboard Preview",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "InterviewVerse AI - Standardized Interviewing Platform",
    description: "An AI-powered dashboard workspace to manage interview personas, conduct live mock interviews, evaluate transcripts, and review performance reports.",
    images: ["/og-image.png"],
    creator: "@interviewverse",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#090d16" },
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
  ],
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
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
