"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchPersonas } from "@/features/personas/services/personas";
import { queryKeys } from "@/lib/query-keys";

export function usePersonasQuery() {
  return useQuery({
    queryKey: queryKeys.personas.list,
    queryFn: fetchPersonas,
    staleTime: 5 * 60 * 1000,
    retry: 1,
    refetchOnWindowFocus: false,
  });
}
