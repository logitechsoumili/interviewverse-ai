"use client";

import { useEffect, useRef } from "react";
import { InterviewMessageItem } from "@/features/interviews/components/interview-message-item";
import { TypingIndicator } from "@/features/interviews/components/typing-indicator";
import type { InterviewMessage } from "@/features/interviews/types";

type InterviewMessageListProps = {
  messages: InterviewMessage[];
  isSending: boolean;
  onRetryMessage: (message: InterviewMessage) => void;
};

export function InterviewMessageList({
  messages,
  isSending,
  onRetryMessage,
}: InterviewMessageListProps) {
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, isSending]);

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="flex-1 space-y-4 overflow-y-auto px-1 py-1 pr-2">
        {messages.map((message) => (
          <InterviewMessageItem key={message.id} message={message} onRetry={onRetryMessage} />
        ))}

        {isSending ? (
          <div className="flex justify-start">
            <TypingIndicator />
          </div>
        ) : null}
        <div ref={endRef} />
      </div>
    </div>
  );
}
