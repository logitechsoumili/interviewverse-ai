"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/features/dashboard/components/empty-state";
import { ErrorState } from "@/features/dashboard/components/error-state";
import { LoadingSkeleton } from "@/features/dashboard/components/loading-skeleton";
import { DashboardHeader } from "@/features/dashboard/components/dashboard-header";
import { DashboardStats } from "@/features/dashboard/components/dashboard-stats";
import { RecentInterviewList } from "@/features/dashboard/components/recent-interview-list";
import { getApiErrorMessage } from "@/lib/api-error";
import { getInterviewStats } from "@/features/dashboard/utils";
import { useInterviewHistoryQuery } from "@/features/dashboard/hooks/use-interview-history";

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
  const isEmpty = interviews.length === 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="space-y-6"
    >
      <section className="grid gap-6 xl:grid-cols-[minmax(0,1.55fr)_minmax(0,0.95fr)]">
        <DashboardHeader />

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

      <DashboardStats stats={stats} />

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
          <RecentInterviewList interviews={interviews} limit={3} />
        )}
      </section>
    </motion.div>
  );
}
