"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type EvaluationErrorStateProps = {
  title?: string;
  description: string;
  onRetry?: () => void;
  retryLabel?: string;
  actionLabel?: string;
  actionHref?: string;
};

export function EvaluationErrorState({
  title = "Unable to load evaluation",
  description,
  onRetry,
  retryLabel = "Try Again",
  actionLabel = "Back to Interview",
  actionHref,
}: EvaluationErrorStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm" role="alert">
        <CardHeader className="space-y-3">
          <div
            aria-hidden="true"
            className="flex h-14 w-14 items-center justify-center rounded-2xl border border-destructive/20 bg-destructive/10 text-destructive shadow-inner"
          >
            !
          </div>
          <CardTitle className="text-lg">{title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="max-w-2xl text-sm leading-6 text-muted-foreground">{description}</p>
          <div className="flex flex-wrap gap-3">
            {onRetry ? (
              <Button type="button" onClick={onRetry}>
                {retryLabel}
              </Button>
            ) : null}
            {actionHref ? (
              <Button asChild variant="outline">
                <Link href={actionHref}>{actionLabel}</Link>
              </Button>
            ) : null}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
