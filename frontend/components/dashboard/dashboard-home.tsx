"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/dashboard/empty-state";
import { ErrorState } from "@/components/dashboard/error-state";
import { HistoryList } from "@/components/dashboard/history-list";
import { LoadingSkeleton } from "@/components/dashboard/loading-skeleton";
import { StatCard } from "@/components/dashboard/stat-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getApiErrorMessage } from "@/lib/api-error";
import { getInterviewStats } from "@/lib/dashboard";
import { useInterviewHistoryQuery } from "@/hooks/use-interview-history";

export function DashboardHome() {
  const interviewsQuery = useInterviewHistoryQuery();

  if (interviewsQuery.isLoading) {
    return <LoadingSkeleton variant="dashboard" />;
  }

  if (interviewsQuery.isError) {
    return (
      <ErrorState
        title="Unable to load dashboard"
        description={getApiErrorMessage(interviewsQuery.error)}
        onAction={() => void interviewsQuery.refetch()}
      />
    );
  }

  const interviews = [...(interviewsQuery.data ?? [])].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
  const stats = getInterviewStats(interviews);
  const recentInterviews = interviews.slice(0, 3);
  const isEmpty = interviews.length === 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="space-y-6"
    >
      <section className="grid gap-6 xl:grid-cols-[minmax(0,1.55fr)_minmax(0,0.95fr)]">
        <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
          <CardHeader className="space-y-4">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
              Welcome
            </p>
            <CardTitle className="text-3xl tracking-tight sm:text-4xl">
              InterviewVerse AI dashboard is ready.
            </CardTitle>
            <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
              Review your latest sessions, keep an eye on completion progress, and
              jump back into the workflow without leaving the workspace.
            </p>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-3">
            <Button type="button" disabled>
              Start Interview
            </Button>
            <Button asChild variant="outline">
              <Link href="/dashboard/history">View History</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="border-border/80 bg-surface/90 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3">
            <div className="rounded-2xl border border-border/70 bg-background/40 p-4">
              <p className="font-medium text-foreground">Start Interview</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Placeholder action for the interview flow.
              </p>
            </div>
            <div className="rounded-2xl border border-border/70 bg-background/40 p-4">
              <p className="font-medium text-foreground">Review History</p>
              <p className="mt-1 text-sm text-muted-foreground">
                See interview progress and completion details.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <StatCard label="Total Interviews" value={stats.total} hint="All sessions" />
        <StatCard label="Completed" value={stats.completed} hint="Finished" />
        <StatCard label="Pending" value={stats.pending} hint="In progress" />
      </section>

      <section className="space-y-4">
        <div className="flex items-end justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold tracking-tight">Recent interviews</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              The latest sessions from your workspace.
            </p>
          </div>
          {!isEmpty ? (
            <Button asChild variant="outline" className="hidden sm:inline-flex">
              <Link href="/dashboard/history">Open full history</Link>
            </Button>
          ) : null}
        </div>

        {isEmpty ? (
          <EmptyState
            title="No interviews yet."
            description="Start your first interview to populate the dashboard and see session analytics here."
            actionLabel="Start Interview"
            className="border-border/80 bg-surface/90"
          />
        ) : (
          <HistoryList interviews={recentInterviews} limit={3} />
        )}
      </section>
    </motion.div>
  );
}
