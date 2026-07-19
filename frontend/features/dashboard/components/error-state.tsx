"use client";

import type { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type ErrorStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
  children?: ReactNode;
};

export function ErrorState({
  title,
  description,
  actionLabel = "Try Again",
  onAction,
  className,
  children,
}: ErrorStateProps) {
  return (
    <Card className={cn("border-border/80 bg-surface/90 shadow-sm", className)}>
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
          {description}
        </p>
        {children}
        {onAction ? (
          <Button type="button" onClick={onAction}>
            {actionLabel}
          </Button>
        ) : null}
      </CardContent>
    </Card>
  );
}
