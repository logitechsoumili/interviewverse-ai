"use client";

import { motion } from "framer-motion";

export default function HomePage() {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-6">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[-6rem] top-[-6rem] h-72 w-72 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute right-[-7rem] top-1/3 h-80 w-80 rounded-full bg-secondary/10 blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.28, ease: "easeOut" }}
        className="relative z-10 max-w-xl text-center"
      >
        <div className="mb-6 inline-flex items-center rounded-full border border-border/70 bg-surface/80 px-4 py-2 text-xs font-medium uppercase tracking-[0.28em] text-muted-foreground shadow-sm backdrop-blur">
          InterviewVerse AI
        </div>
        <h1 className="font-display text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">
          Frontend foundation ready.
        </h1>
        <p className="mt-4 text-base leading-7 text-muted-foreground sm:text-lg">
          A polished workspace for personas, interviews, evaluations, and reports.
        </p>
      </motion.div>
    </main>
  );
}
