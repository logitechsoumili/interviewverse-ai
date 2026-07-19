"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useInterviewSessionQuery } from "@/features/interviews/hooks/use-interview-session";

type InterviewEvaluationPlaceholderProps = {
  interviewId: string;
};

export function InterviewEvaluationPlaceholder({
  interviewId,
}: InterviewEvaluationPlaceholderProps) {
  const sessionQuery = useInterviewSessionQuery(interviewId);
  const session = sessionQuery.data ?? null;

  return (
    <Card className="border-border/80 bg-surface/90 shadow-sm">
      <CardHeader className="space-y-3">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
          Evaluation
        </p>
        <CardTitle className="text-2xl tracking-tight">Evaluation placeholder</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
          Evaluation is not implemented in this phase. The interview session has been
          completed, and the backend evaluation APIs remain untouched.
        </p>
        {session ? (
          <div className="rounded-2xl border border-border/70 bg-background/50 px-4 py-3 text-sm">
            <div className="font-medium text-foreground">{session.personaName}</div>
            <div className="mt-1 text-muted-foreground">{session.title}</div>
          </div>
        ) : null}
        <Button asChild variant="outline">
          <Link href="/dashboard/personas">Back to Personas</Link>
        </Button>
      </CardContent>
    </Card>
  );
}
