"use client";

import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/query-keys";
import { fetchReport } from "@/features/evaluations/services/evaluations";

export function useReportQuery(interviewId: string) {
  return useQuery({
    queryKey: queryKeys.reports.detail(interviewId),
    queryFn: () => fetchReport(interviewId),
    staleTime: Infinity,
    retry: false,
    refetchOnWindowFocus: false,
  });
}
