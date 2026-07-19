"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type EmptyStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  actionHref?: string;
  onAction?: () => void;
  className?: string;
};

export function EmptyState({
  title,
  description,
  actionLabel,
  actionHref,
  onAction,
  className,
}: EmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.99 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
    >
      <Card className={cn("border-border/80 bg-surface/90 shadow-sm", className)}>
        <CardHeader className="space-y-3">
          <div
            aria-hidden="true"
            className="flex h-14 w-14 items-center justify-center rounded-2xl border border-border/70 bg-background/50 shadow-inner"
          >
            <span className="flex h-7 w-7 items-center justify-center rounded-full bg-primary/15 text-primary">
              <span className="h-3 w-3 rounded-full border border-current" />
            </span>
          </div>
          <CardTitle className="text-lg">{title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
            {description}
          </p>
          {actionLabel ? (
            actionHref ? (
              <Button asChild>
                <Link href={actionHref}>{actionLabel}</Link>
              </Button>
            ) : (
              <Button type="button" onClick={onAction} disabled={!onAction}>
                {actionLabel}
              </Button>
            )
          ) : null}
        </CardContent>
      </Card>
    </motion.div>
  );
}
