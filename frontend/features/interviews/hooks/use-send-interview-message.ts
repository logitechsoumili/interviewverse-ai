"use client";

import { useMutation } from "@tanstack/react-query";
import { sendInterviewMessage } from "@/features/interviews/services/interviews";

export type SendInterviewMessageVariables = {
  interviewId: string;
  message: string;
};

export function useSendInterviewMessageMutation() {
  return useMutation({
    mutationFn: ({ interviewId, message }: SendInterviewMessageVariables) =>
      sendInterviewMessage(interviewId, { message }),
  });
}
