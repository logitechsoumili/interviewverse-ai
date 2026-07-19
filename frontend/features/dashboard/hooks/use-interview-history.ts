"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchInterviews } from "@/features/dashboard/services/interviews";
import { queryKeys } from "@/lib/query-keys";

export function useInterviewHistoryQuery() {
  return useQuery({
    queryKey: queryKeys.interviews,
    queryFn: fetchInterviews,
    staleTime: 5 * 60 * 1000,
    retry: 1,
    refetchOnWindowFocus: false,
  });
}
