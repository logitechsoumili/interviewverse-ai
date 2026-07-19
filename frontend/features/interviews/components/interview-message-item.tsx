"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { type InterviewMessage } from "@/features/interviews/types";
import { formatInterviewTimestamp } from "@/features/interviews/utils";

type InterviewMessageItemProps = {
  message: InterviewMessage;
  onRetry?: (message: InterviewMessage) => void;
};

export function InterviewMessageItem({ message, onRetry }: InterviewMessageItemProps) {
  const isAssistant = message.role === "assistant";
  const bubbleTone =
    message.status === "error"
      ? "border-destructive/40 bg-destructive/10 text-foreground"
      : isAssistant
        ? "border-border/80 bg-surface/95 text-foreground"
        : "border-primary/20 bg-primary/10 text-foreground";

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.18, ease: "easeOut" }}
      className={cn("flex w-full", isAssistant ? "justify-start" : "justify-end")}
    >
      <div
        className={cn(
          "max-w-[88%] rounded-3xl border px-4 py-3 shadow-sm sm:max-w-[76%]",
          bubbleTone
        )}
      >
        <div className="space-y-2">
          <p className="whitespace-pre-wrap text-sm leading-6">{message.content}</p>
          <div className="flex items-center justify-between gap-3 text-[11px] uppercase tracking-[0.22em] text-muted-foreground">
            <span>{isAssistant ? "Interviewer" : "You"}</span>
            <span>{formatInterviewTimestamp(message.timestamp)}</span>
          </div>
          {message.status === "error" && onRetry ? (
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="mt-2"
              onClick={() => onRetry(message)}
            >
              Retry
            </Button>
          ) : null}
        </div>
      </div>
    </motion.article>
  );
}
