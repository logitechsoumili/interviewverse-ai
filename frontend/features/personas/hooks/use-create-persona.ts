"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createPersona } from "@/features/personas/services/personas";
import { queryKeys } from "@/lib/query-keys";

export function useCreatePersonaMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPersona,
    onSuccess: (createdPersona) => {
      queryClient.setQueryData(
        queryKeys.personas.detail(createdPersona.id),
        createdPersona
      );
      void queryClient.invalidateQueries({ queryKey: queryKeys.personas.list });
    },
  });
}
