"use client";

import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { InterviewComposer } from "@/features/interviews/components/interview-composer";
import { InterviewConfirmDialog } from "@/features/interviews/components/interview-confirm-dialog";
import { InterviewErrorState } from "@/features/interviews/components/interview-error-state";
import { InterviewHeader } from "@/features/interviews/components/interview-header";
import { InterviewLoadingState } from "@/features/interviews/components/interview-loading-state";
import { InterviewMessageList } from "@/features/interviews/components/interview-message-list";
import { useCompleteInterviewMutation } from "@/features/interviews/hooks/use-complete-interview";
import { useInterviewSessionQuery } from "@/features/interviews/hooks/use-interview-session";
import { useSendInterviewMessageMutation } from "@/features/interviews/hooks/use-send-interview-message";
import type { InterviewMessage, InterviewSession } from "@/features/interviews/types";
import {
  createAssistantMessage,
  createId,
  createUserMessage,
  getInterviewApiErrorMessage,
  saveInterviewSession,
  getPathnameInterviewId,
} from "@/features/interviews/utils";
import { queryKeys } from "@/lib/query-keys";
import { toast } from "sonner";

export function InterviewPage() {
  const router = useRouter();
  const [interviewId, setInterviewId] = useState<string | null>(null);

  useEffect(() => {
    const id = getPathnameInterviewId();
    if (id) {
      setInterviewId(id);
    }
  }, []);

  const queryClient = useQueryClient();
  const sessionQuery = useInterviewSessionQuery(interviewId || "");
  const sendMessageMutation = useSendInterviewMessageMutation();
  const completeInterviewMutation = useCompleteInterviewMutation();
  const [endDialogOpen, setEndDialogOpen] = useState(false);

  const session = sessionQuery.data ?? null;
  const isLoading = !interviewId || sessionQuery.isLoading || sessionQuery.isFetching;

  const commitSession = (updater: (current: InterviewSession) => InterviewSession) => {
    queryClient.setQueryData<InterviewSession | null>(
      queryKeys.interviewSessions.detail(interviewId || ""),
      (current) => {
        if (!current) {
          return current;
        }

        const nextSession = updater(current);
        saveInterviewSession(nextSession);
        return nextSession;
      }
    );
  };

  if (isLoading) {
    return <InterviewLoadingState />;
  }

  if (!session) {
    return (
      <InterviewErrorState
        title="Interview session unavailable"
        description="This interview session is not available in the current browser context. Start a new interview from the Personas page."
      />
    );
  }

  const sendMessage = async (content: string, retryMessageId?: string) => {
    const timestamp = new Date().toISOString();
    const messageId = retryMessageId ?? createId();
    const userMessage: InterviewMessage = retryMessageId
      ? {
          id: messageId,
          role: "user",
          content,
          timestamp,
          status: "sending",
          errorMessage: null,
        }
      : createUserMessage(content, timestamp, messageId);
    const markMessage = (
      message: InterviewMessage,
      status: InterviewMessage["status"],
      errorMessage: string | null = null
    ): InterviewMessage => ({
      ...message,
      status,
      errorMessage,
    });

    commitSession((current) => ({
      ...current,
      messages: retryMessageId
        ? current.messages.map((message) =>
            message.id === messageId
              ? markMessage(
                  {
                    ...message,
                    content,
                    timestamp,
                  },
                  "sending"
                )
              : message
          )
        : [...current.messages, userMessage],
      latestError: null,
    }));

    try {
      const response = await sendMessageMutation.mutateAsync({
        interviewId,
        message: content,
      });

      const assistantMessage = createAssistantMessage(
        response.question,
        new Date().toISOString()
      );

      commitSession((current) => ({
        ...current,
        messages: current.messages
          .map((message) =>
            message.id === messageId ? markMessage(message, "sent") : message
          )
          .concat(assistantMessage),
        latestError: null,
      }));
    } catch (error) {
      const errorMessage = getInterviewApiErrorMessage(error);
      commitSession((current) => ({
        ...current,
        messages: current.messages.map((message) =>
          message.id === messageId ? markMessage(message, "error", errorMessage) : message
        ),
        latestError: errorMessage,
      }));
      toast.error(errorMessage);
    }
  };

  const retryMessage = (message: InterviewMessage) => {
    void sendMessage(message.content, message.id);
  };

  const handleEndInterview = async () => {
    try {
      await completeInterviewMutation.mutateAsync({ interviewId });
      router.replace(`/dashboard/interview/${interviewId}/evaluation`);
    } catch (error) {
      const errorMessage = getInterviewApiErrorMessage(error);
      commitSession((current) => ({ ...current, latestError: errorMessage }));
      toast.error(errorMessage);
    } finally {
      setEndDialogOpen(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
      className="space-y-6"
    >
      <InterviewHeader session={session} onEndInterview={() => setEndDialogOpen(true)} />

      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardContent className="flex min-h-[68vh] flex-col gap-4 p-4 sm:p-6">
          {session.latestError ? (
            <div
              className="rounded-2xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive"
              role="alert"
            >
              {session.latestError}
            </div>
          ) : null}

          <div className="min-h-0 flex-1">
            <InterviewMessageList
              messages={session.messages}
              isSending={sendMessageMutation.isPending}
              onRetryMessage={retryMessage}
            />
          </div>

          <div className="rounded-3xl border border-border/70 bg-background/50 p-4 shadow-sm">
            <InterviewComposer
              session={session}
              isSending={sendMessageMutation.isPending}
              onSendMessage={sendMessage}
            />
          </div>
        </CardContent>
      </Card>

      <InterviewConfirmDialog
        open={endDialogOpen}
        title="End this interview?"
        description="This will finalize the session and redirect you to the evaluation placeholder."
        onConfirm={() => void handleEndInterview()}
        onCancel={() => setEndDialogOpen(false)}
        pending={completeInterviewMutation.isPending}
      />
    </motion.div>
  );
}
