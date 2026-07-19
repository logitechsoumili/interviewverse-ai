"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useInterviewSessionQuery } from "@/features/interviews/hooks/use-interview-session";
import { useEvaluationQuery, useGenerateEvaluationMutation } from "@/features/evaluations/hooks/use-evaluation";
import { EvaluationLoadingState } from "@/features/evaluations/components/evaluation-loading-state";
import { EvaluationGeneratingState } from "@/features/evaluations/components/evaluation-generating-state";
import { EvaluationErrorState } from "@/features/evaluations/components/evaluation-error-state";
import type { EvaluationApiResponse } from "@/features/evaluations/types";
import {
  buildEvaluationSummary,
  formatEvaluationTimestamp,
  getEvaluationApiErrorMessage,
  getScoreLabel,
  isEvaluationNotFoundError,
} from "@/features/evaluations/utils";
import { queryKeys } from "@/lib/query-keys";
import { formatElapsedTime } from "@/features/interviews/utils";
import { formatPersonaName } from "@/features/dashboard/utils";
import { toast } from "sonner";

type EvaluationPageProps = {
  interviewId: string;
};

function ListCard({
  title,
  items,
  emptyText,
}: {
  title: string;
  items: string[];
  emptyText: string;
}) {
  return (
    <Card className="border-border/80 bg-surface/90 shadow-sm">
      <CardHeader className="space-y-2">
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {items.length > 0 ? (
          <ul className="space-y-2 text-sm leading-6 text-muted-foreground">
            {items.map((item) => (
              <li key={item} className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
                {item}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm leading-6 text-muted-foreground">{emptyText}</p>
        )}
      </CardContent>
    </Card>
  );
}

function ScoreMetricCard({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="space-y-3 rounded-2xl border border-border/70 bg-background/50 p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-medium">{label}</p>
          <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
            {getScoreLabel(value)}
          </p>
        </div>
        <Badge variant="outline">{value}/100</Badge>
      </div>
      <Progress value={value} label={label} className="h-2.5" />
    </div>
  );
}

export function EvaluationPage({ interviewId }: EvaluationPageProps) {
  const queryClient = useQueryClient();
  const sessionQuery = useInterviewSessionQuery(interviewId);
  const evaluationQuery = useEvaluationQuery(interviewId);
  const generateEvaluationMutation = useGenerateEvaluationMutation();
  const [generatedEvaluation, setGeneratedEvaluation] = useState<EvaluationApiResponse | null>(null);
  const [generationError, setGenerationError] = useState<string | null>(null);
  const [hasRequestedGeneration, setHasRequestedGeneration] = useState(false);

  const session = sessionQuery.data ?? null;
  const evaluation = generatedEvaluation ?? evaluationQuery.data ?? null;
  const queryError = evaluationQuery.error;
  const shouldGenerate = evaluationQuery.isError && isEvaluationNotFoundError(queryError) && !evaluation && !generationError;

  const startGeneration = useCallback(async () => {
    setHasRequestedGeneration(true);
    setGenerationError(null);

    try {
      const result = await generateEvaluationMutation.mutateAsync(interviewId);
      setGeneratedEvaluation(result);
      queryClient.setQueryData(queryKeys.evaluations.detail(interviewId), result);
    } catch (error) {
      const message = getEvaluationApiErrorMessage(error, "Unable to generate evaluation.");
      setGenerationError(message);
      toast.error(message);
    }
  }, [generateEvaluationMutation, interviewId, queryClient]);

  useEffect(() => {
    if (shouldGenerate && !hasRequestedGeneration && !generateEvaluationMutation.isPending) {
      void startGeneration();
    }
  }, [generateEvaluationMutation.isPending, hasRequestedGeneration, shouldGenerate, startGeneration]);

  const isLoading = evaluationQuery.isLoading;
  const isGenerating = generateEvaluationMutation.isPending || (hasRequestedGeneration && !evaluation);
  const hasUnauthorizedError =
    Boolean(queryError) &&
    !evaluation &&
    "response" in (queryError as object) &&
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (queryError as any)?.response?.status === 401;
  const non404ErrorMessage = queryError
    ? getEvaluationApiErrorMessage(queryError, "Evaluation not found.")
    : null;

  const overallScore = evaluation?.scores.overall_score ?? 0;
  const interviewerName = session?.personaName ?? (evaluation ? formatPersonaName(evaluation.persona_id) : "Interview");
  const interviewTitle = session?.title ?? "Interview evaluation";
  const interviewDuration = session
    ? formatElapsedTime(session.startedAt, session.completedAt)
    : null;

  if (isLoading) {
    return <EvaluationLoadingState />;
  }

  if (isGenerating) {
    return <EvaluationGeneratingState />;
  }

  if (generationError) {
    return (
      <EvaluationErrorState
        title="Evaluation generation failed"
        description={generationError}
        onRetry={() => void startGeneration()}
        retryLabel="Generate Again"
        actionHref="/dashboard/personas"
        actionLabel="Back to Personas"
      />
    );
  }

  if (!evaluation) {
    return (
      <EvaluationErrorState
        title={hasUnauthorizedError ? "Unauthorized" : "Unable to load evaluation"}
        description={non404ErrorMessage ?? "The evaluation could not be loaded."}
        onRetry={evaluationQuery.refetch}
        actionHref={`/dashboard/interview/${interviewId}/report`}
        actionLabel="View Report"
      />
    );
  }

  return (
    <div className="space-y-6">
      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader className="space-y-4">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
            Interview Evaluation
          </p>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="space-y-2">
              <CardTitle className="text-3xl tracking-tight">{interviewerName}</CardTitle>
              <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
                {interviewTitle}
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button asChild variant="outline">
                <Link href={`/dashboard/interview/${interviewId}/report`}>View Report</Link>
              </Button>
              <Button asChild>
                <Link href="/dashboard/personas">Back to Personas</Link>
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="grid gap-3 text-sm text-muted-foreground sm:grid-cols-3">
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Overall Score</div>
            <div className="mt-2 flex items-end justify-between gap-3">
              <div className="text-4xl font-semibold tracking-tight">{overallScore}</div>
              <Badge variant="secondary">{getScoreLabel(overallScore)}</Badge>
            </div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Evaluated At</div>
            <div className="mt-2 text-foreground">
              {formatEvaluationTimestamp(evaluation.evaluated_at)}
            </div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Duration</div>
            <div className="mt-2 text-foreground">{interviewDuration ?? "Unavailable"}</div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 lg:grid-cols-[1.25fr_1fr]">
        <Card className="border-border/80 bg-surface/90 shadow-sm">
          <CardHeader className="space-y-3">
            <CardTitle className="text-lg">Category Scores</CardTitle>
            <p className="text-sm text-muted-foreground">
              The structured score breakdown from the evaluation engine.
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            <ScoreMetricCard label="Communication" value={evaluation.scores.communication_score} />
            <ScoreMetricCard label="Technical" value={evaluation.scores.technical_score} />
            <ScoreMetricCard label="Confidence" value={evaluation.scores.confidence_score} />
          </CardContent>
        </Card>

        <Card className="border-border/80 bg-surface/90 shadow-sm">
          <CardHeader className="space-y-3">
            <CardTitle className="text-lg">Summary</CardTitle>
            <p className="text-sm text-muted-foreground">
              A concise synthesis of the evaluation data.
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm leading-6 text-muted-foreground">
              {buildEvaluationSummary(evaluation)}
            </p>
            <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">
                Overall Score
              </div>
              <div className="mt-2 text-3xl font-semibold tracking-tight">{overallScore}/100</div>
              <Progress value={overallScore} label="Overall score" className="mt-3 h-2.5" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <ListCard
          title="Strengths"
          items={evaluation.summary.strengths}
          emptyText="No strengths were returned for this evaluation."
        />
        <ListCard
          title="Areas for Improvement"
          items={evaluation.summary.weaknesses}
          emptyText="No improvement areas were returned for this evaluation."
        />
        <ListCard
          title="Recommendations"
          items={evaluation.summary.recommendations}
          emptyText="No recommendations were returned for this evaluation."
        />
        <ListCard
          title="Learning Roadmap"
          items={evaluation.summary.learning_roadmap}
          emptyText="No learning roadmap was returned for this evaluation."
        />
      </div>
    </div>
  );
}
