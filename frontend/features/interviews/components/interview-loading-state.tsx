"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function InterviewLoadingState() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="space-y-6"
      role="status"
      aria-live="polite"
      aria-label="Loading interview"
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-full max-w-lg" />
        </CardHeader>
      </Card>

      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardContent className="space-y-4 p-6">
          <div className="space-y-3">
            <Skeleton className="h-20 w-3/4 rounded-2xl" />
            <div className="flex justify-end">
              <Skeleton className="h-20 w-2/3 rounded-2xl" />
            </div>
            <Skeleton className="h-20 w-5/6 rounded-2xl" />
          </div>
          <Skeleton className="h-24 w-full rounded-2xl" />
        </CardContent>
      </Card>
    </motion.div>
  );
}
