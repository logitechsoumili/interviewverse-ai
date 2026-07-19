"use client";

import Link from "next/link";

export function Footer() {
  const currentYear = new Date().getFullYear();

  const handleScrollTo = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault();
    const id = href.replace("#", "");
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <footer className="bg-background border-t border-border/30 px-6 py-12 text-xs text-muted-foreground">
      <div className="mx-auto max-w-7xl flex flex-col md:flex-row justify-between items-center gap-8">
        {/* Brand */}
        <div className="flex items-center gap-2">
          <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-secondary text-primary-foreground">
            <svg
              className="h-3.5 w-3.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          </div>
          <span className="font-display font-bold text-foreground text-sm">
            InterviewVerse AI
          </span>
        </div>

        {/* Links Directories */}
        <div className="flex flex-wrap justify-center gap-x-8 gap-y-4">
          <a href="#features" onClick={(e) => handleScrollTo(e, "#features")} className="hover:text-foreground transition-colors">
            Features
          </a>
          <a href="#how-it-works" onClick={(e) => handleScrollTo(e, "#how-it-works")} className="hover:text-foreground transition-colors">
            How it Works
          </a>
          <Link href="/login" className="hover:text-foreground transition-colors">
            Login
          </Link>
          <Link href="/register" className="hover:text-foreground transition-colors">
            Register
          </Link>
          <a href="#" className="hover:text-foreground transition-colors">
            GitHub
          </a>
          <a href="#" className="hover:text-foreground transition-colors">
            Privacy Policy
          </a>
          <a href="#" className="hover:text-foreground transition-colors">
            Terms of Service
          </a>
        </div>

        {/* Copyright */}
        <p className="text-muted-foreground/60 text-center md:text-right">
          &copy; {currentYear} InterviewVerse AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
