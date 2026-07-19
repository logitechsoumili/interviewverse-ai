"use client";

import { motion } from "framer-motion";

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex max-w-[76%] items-center gap-2 rounded-3xl border border-border/80 bg-surface/95 px-4 py-3 shadow-sm"
      aria-label="Interviewer is typing"
    >
      <span className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
        Thinking
      </span>
      <div className="flex items-center gap-1" aria-hidden="true">
        <span className="h-2 w-2 animate-bounce rounded-full bg-primary/70 [animation-delay:-0.24s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-primary/70 [animation-delay:-0.12s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-primary/70" />
      </div>
    </motion.div>
  );
}
