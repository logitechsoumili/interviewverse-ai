"use client";

import type { ReactNode } from "react";
import { motion } from "framer-motion";
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
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
    >
      <Card
        className={cn("border-border/80 bg-surface/90 shadow-sm", className)}
        role="alert"
      >
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
    </motion.div>
  );
}
