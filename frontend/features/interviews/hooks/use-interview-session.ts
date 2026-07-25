"use client";

import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/query-keys";
import { loadInterviewSession } from "@/features/interviews/utils";

export function useInterviewSessionQuery(interviewId: string) {
  return useQuery({
    queryKey: queryKeys.interviewSessions.detail(interviewId),
    queryFn: () => {
      if (!interviewId) return null;
      return loadInterviewSession(interviewId);
    },
    enabled: !!interviewId,
    staleTime: Infinity,
    gcTime: Infinity,
    retry: false,
    refetchOnWindowFocus: false,
  });
}
