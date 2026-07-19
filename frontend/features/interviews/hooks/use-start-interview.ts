"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { queryKeys } from "@/lib/query-keys";
import { startInterview } from "@/features/interviews/services/interviews";
import {
  createInterviewSession,
  saveInterviewSession,
} from "@/features/interviews/utils";
import type { InterviewStartContext } from "@/features/interviews/types";

export type StartInterviewVariables = InterviewStartContext;

export function useStartInterviewMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ personaId, topics, difficulty }: StartInterviewVariables) => {
      return startInterview({
        persona_id: personaId,
        topics,
        difficulty,
      });
    },
    onSuccess: (response, variables) => {
      const session = createInterviewSession(variables, response);
      saveInterviewSession(session);
      queryClient.setQueryData(queryKeys.interviewSessions.detail(session.interviewId), session);
      void queryClient.invalidateQueries({ queryKey: queryKeys.interviews });
    },
  });
}
