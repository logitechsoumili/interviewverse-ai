"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function EvaluationLoadingState() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="space-y-6"
      role="status"
      aria-live="polite"
      aria-label="Loading evaluation"
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <Skeleton className="h-4 w-36" />
          <Skeleton className="h-8 w-72" />
          <Skeleton className="h-4 w-full max-w-2xl" />
        </CardHeader>
      </Card>

      <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <Card className="border-border/80 bg-surface/90 shadow-sm">
          <CardContent className="space-y-4 p-6">
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-24 w-full rounded-2xl" />
            <Skeleton className="h-24 w-full rounded-2xl" />
          </CardContent>
        </Card>
        <Card className="border-border/80 bg-surface/90 shadow-sm">
          <CardContent className="space-y-3 p-6">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="h-3 w-full" />
            <Skeleton className="h-3 w-5/6" />
            <Skeleton className="h-3 w-4/6" />
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}
