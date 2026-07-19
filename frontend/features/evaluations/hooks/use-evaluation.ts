"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/query-keys";
import { fetchEvaluation, generateEvaluation } from "@/features/evaluations/services/evaluations";

export function useEvaluationQuery(interviewId: string) {
  return useQuery({
    queryKey: queryKeys.evaluations.detail(interviewId),
    queryFn: () => fetchEvaluation(interviewId),
    staleTime: Infinity,
    retry: false,
    refetchOnWindowFocus: false,
  });
}

export function useGenerateEvaluationMutation() {
  return useMutation({
    mutationFn: (interviewId: string) => generateEvaluation(interviewId),
  });
}
