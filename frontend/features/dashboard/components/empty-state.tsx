"use client";

import Link from "next/link";
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
    <Card className={cn("border-border/80 bg-surface/90 shadow-sm", className)}>
      <CardHeader className="space-y-3">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-border bg-background/40 text-xl">
          ✦
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
  );
}
