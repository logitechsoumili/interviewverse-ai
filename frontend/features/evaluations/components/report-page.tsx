"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useInterviewSessionQuery } from "@/features/interviews/hooks/use-interview-session";
import { useReportQuery } from "@/features/evaluations/hooks/use-report";
import { ReportLoadingState } from "@/features/evaluations/components/report-loading-state";
import { ReportErrorState } from "@/features/evaluations/components/report-error-state";
import {
  extractEvaluationSummary,
  extractTranscriptSummary,
  formatEvaluationTimestamp,
  getReportApiErrorMessage,
} from "@/features/evaluations/utils";
import { formatElapsedTime } from "@/features/interviews/utils";
import { formatPersonaName } from "@/features/dashboard/utils";

type ReportPageProps = {
  interviewId: string;
};

function ReportListCard({
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

function ReportSectionCard({
  title,
  content,
}: {
  title: string;
  content: string;
}) {
  return (
    <Card className="border-border/80 bg-surface/90 shadow-sm">
      <CardHeader className="space-y-2">
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="whitespace-pre-wrap text-sm leading-6 text-muted-foreground">{content}</p>
      </CardContent>
    </Card>
  );
}

export function ReportPage({ interviewId }: ReportPageProps) {
  const sessionQuery = useInterviewSessionQuery(interviewId);
  const reportQuery = useReportQuery(interviewId);

  const report = reportQuery.data ?? null;
  const session = sessionQuery.data ?? null;
  const generatedAt = report ? formatEvaluationTimestamp(report.generated_at) : null;
  const duration = session ? formatElapsedTime(session.startedAt, session.completedAt) : null;
  const interviewerName = session?.personaName ?? (report ? formatPersonaName(report.persona_id) : "Interview");
  const interviewTitle = session?.title ?? "Interview report";
  const printableMarkdown = report?.markdown_report ?? "";

  if (reportQuery.isLoading) {
    return <ReportLoadingState />;
  }

  if (!report) {
    return (
      <ReportErrorState
        title="Unable to load report"
        description={getReportApiErrorMessage(reportQuery.error, "The report could not be found.")}
        onRetry={reportQuery.refetch}
        actionHref={`/dashboard/interview/${interviewId}/evaluation`}
        actionLabel="Back to Evaluation"
      />
    );
  }

  return (
    <div className="space-y-6">
      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader className="space-y-4">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
            Interview Report
          </p>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="space-y-2">
              <CardTitle className="text-3xl tracking-tight">{interviewerName}</CardTitle>
              <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
                {interviewTitle}
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button type="button" variant="outline" disabled>
                Download Report
              </Button>
              <Button
                type="button"
                onClick={() => window.print()}
              >
                Print Report
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="grid gap-3 text-sm text-muted-foreground sm:grid-cols-4">
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Persona</div>
            <div className="mt-2 text-foreground">{interviewerName}</div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Generated</div>
            <div className="mt-2 text-foreground">{generatedAt ?? "Unavailable"}</div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Duration</div>
            <div className="mt-2 text-foreground">{duration ?? "Unavailable"}</div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Interview ID</div>
            <div className="mt-2 break-all text-foreground">{report.interview_id}</div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <ReportSectionCard
          title="Transcript Summary"
          content={extractTranscriptSummary(report)}
        />
        <ReportSectionCard
          title="Evaluation Summary"
          content={extractEvaluationSummary(report)}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <ReportListCard
          title="Strengths"
          items={report.strengths}
          emptyText="No strengths were returned for this report."
        />
        <ReportListCard
          title="Areas for Improvement"
          items={report.weaknesses}
          emptyText="No improvement areas were returned for this report."
        />
        <ReportListCard
          title="Recommendations"
          items={report.recommendations}
          emptyText="No recommendations were returned for this report."
        />
        <ReportListCard
          title="Learning Roadmap"
          items={report.learning_roadmap}
          emptyText="No roadmap items were returned for this report."
        />
      </div>

      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <div className="flex items-center justify-between gap-3">
            <CardTitle className="text-lg">Printable Report Preview</CardTitle>
            <Badge variant="outline">Markdown</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <pre className="max-h-[480px] overflow-auto whitespace-pre-wrap rounded-2xl border border-border/70 bg-background/50 p-4 text-sm leading-6 text-muted-foreground">
            {printableMarkdown}
          </pre>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button asChild variant="outline">
          <Link href={`/dashboard/interview/${interviewId}/evaluation`}>Back to Evaluation</Link>
        </Button>
      </div>
    </div>
  );
}
