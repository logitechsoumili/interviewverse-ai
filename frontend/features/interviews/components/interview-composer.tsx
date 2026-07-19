"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { interviewComposerSchema, type InterviewComposerSchema } from "@/features/interviews/schemas/interview-schema";
import { type InterviewSession } from "@/features/interviews/types";

type InterviewComposerProps = {
  session: InterviewSession;
  isSending: boolean;
  onSendMessage: (message: string) => Promise<void>;
};

export function InterviewComposer({ session, isSending, onSendMessage }: InterviewComposerProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<InterviewComposerSchema>({
    resolver: zodResolver(interviewComposerSchema),
    defaultValues: { message: "" },
  });

  useEffect(() => {
    reset({ message: "" });
  }, [session.interviewId, reset]);

  const submitMessage = handleSubmit(async ({ message }) => {
    await onSendMessage(message);
    reset({ message: "" });
  });

  return (
    <form className="space-y-3" onSubmit={submitMessage}>
      <div className="space-y-2">
        <Textarea
          rows={4}
          placeholder="Write your response..."
          aria-label="Message input"
          aria-invalid={Boolean(errors.message)}
          aria-describedby={errors.message ? "message-error" : undefined}
          disabled={isSending || session.status === "completed"}
          {...register("message")}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              if (!isSending && session.status !== "completed") {
                void submitMessage();
              }
            }
          }}
        />
        {errors.message ? (
          <p id="message-error" className="text-xs text-destructive">
            {errors.message.message}
          </p>
        ) : null}
      </div>

      <div className="flex items-center justify-between gap-3">
        <p className="text-xs text-muted-foreground">
          Press Enter to send, Shift+Enter for a new line.
        </p>
        <Button type="submit" disabled={isSending || session.status === "completed"}>
          {isSending ? "Sending..." : "Send"}
        </Button>
      </div>
    </form>
  );
}
