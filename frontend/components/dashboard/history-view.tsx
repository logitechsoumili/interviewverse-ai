"use client";

import { motion } from "framer-motion";
import { EmptyState } from "@/components/dashboard/empty-state";
import { ErrorState } from "@/components/dashboard/error-state";
import { HistoryList } from "@/components/dashboard/history-list";
import { LoadingSkeleton } from "@/components/dashboard/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getApiErrorMessage } from "@/lib/api-error";
import { useInterviewHistoryQuery } from "@/hooks/use-interview-history";

export function HistoryView() {
  const interviewsQuery = useInterviewHistoryQuery();

  if (interviewsQuery.isLoading) {
    return <LoadingSkeleton variant="history" />;
  }

  if (interviewsQuery.isError) {
    return (
      <ErrorState
        title="Unable to load history"
        description={getApiErrorMessage(interviewsQuery.error)}
        onAction={() => void interviewsQuery.refetch()}
      />
    );
  }

  const interviews = [...(interviewsQuery.data ?? [])].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="space-y-6"
    >
      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader>
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
            Interview History
          </p>
          <CardTitle className="text-2xl tracking-tight">
            All interview sessions in one place.
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
            Review each session card for persona, creation date, and completion
            status. Details are intentionally placeholder-only for Phase 3.
          </p>
        </CardContent>
      </Card>

      {interviews.length === 0 ? (
        <EmptyState
          title="No interviews yet."
          description="There are no completed or pending interviews to show right now. Start a session to populate this list."
          actionLabel="Start Interview"
          className="border-border/80 bg-surface/90"
        />
      ) : (
        <HistoryList interviews={interviews} />
      )}
    </motion.div>
  );
}
