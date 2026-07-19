"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { queryKeys } from "@/lib/query-keys";
import { completeInterview } from "@/features/interviews/services/interviews";
import { loadInterviewSession, saveInterviewSession } from "@/features/interviews/utils";

export type CompleteInterviewVariables = {
  interviewId: string;
};

export function useCompleteInterviewMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ interviewId }: CompleteInterviewVariables) => completeInterview(interviewId),
    onSuccess: (_response, variables) => {
      const existing = loadInterviewSession(variables.interviewId);
      if (existing) {
        const updated = {
          ...existing,
          status: "completed" as const,
          completedAt: new Date().toISOString(),
          latestError: null,
        };

        saveInterviewSession(updated);
        queryClient.setQueryData(
          queryKeys.interviewSessions.detail(variables.interviewId),
          updated
        );
      }

      void queryClient.invalidateQueries({ queryKey: queryKeys.interviews });
    },
  });
}
