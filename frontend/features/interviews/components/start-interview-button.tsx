"use client";

import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { useStartInterviewMutation } from "@/features/interviews/hooks/use-start-interview";
import { getInterviewApiErrorMessage } from "@/features/interviews/utils";

type StartInterviewButtonProps = {
  personaId: string;
  personaName: string;
  personaRole: string;
  personaTitle?: string;
  className?: string;
};

export function StartInterviewButton({
  personaId,
  personaName,
  personaRole,
  personaTitle,
  className,
}: StartInterviewButtonProps) {
  const router = useRouter();
  const startInterviewMutation = useStartInterviewMutation();

  const handleStartInterview = async () => {
    try {
      const response = await startInterviewMutation.mutateAsync({
        personaId,
        personaName,
        personaRole,
        title: personaTitle ?? "Interview Session",
      });

      router.push(`/dashboard/interview/${response.interview_id}`);
    } catch (error) {
      toast.error(getInterviewApiErrorMessage(error));
    }
  };

  return (
    <Button
      type="button"
      className={className}
      onClick={() => void handleStartInterview()}
      disabled={startInterviewMutation.isPending}
      aria-label={`Start interview with ${personaName}`}
    >
      {startInterviewMutation.isPending ? "Starting..." : "Use Persona"}
    </Button>
  );
}
