"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchCurrentUser } from "@/services/auth";
import { queryKeys } from "@/lib/query-keys";

export function useCurrentUserQuery() {
  return useQuery({
    queryKey: queryKeys.currentUser,
    queryFn: fetchCurrentUser,
    staleTime: 5 * 60 * 1000,
    retry: 1,
    refetchOnWindowFocus: false,
  });
}
