"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export default function NotFound() {
  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center bg-background px-6 text-center overflow-hidden">
      {/* Background ambient lighting */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[15%] top-[25%] h-80 w-80 rounded-full bg-primary/15 blur-[7rem]" />
        <div className="absolute right-[15%] bottom-[25%] h-96 w-96 rounded-full bg-secondary/10 blur-[8rem]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: "easeOut" }}
        className="relative z-10 max-w-md"
      >
        <span className="inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-3.5 py-1 text-xs font-semibold tracking-wider text-primary uppercase">
          Orbit Missing
        </span>

        <h1 className="mt-6 font-display text-8xl font-black tracking-tight bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          404
        </h1>

        <h2 className="mt-4 font-display text-2xl font-bold text-foreground">
          Lost in the Verse
        </h2>

        <p className="mt-3 text-sm text-muted-foreground leading-relaxed">
          The requested address is outside our mapped sectors. You can query the dashboard or return to orbit.
        </p>

        <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-lg transition-all hover:brightness-110 active:scale-[0.98] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            Dashboard
          </Link>
          <Link
            href="/"
            className="inline-flex items-center justify-center rounded-xl border border-border bg-surface px-6 py-3 text-sm font-semibold text-foreground transition-all hover:bg-accent active:scale-[0.98] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border"
          >
            Go Home
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
