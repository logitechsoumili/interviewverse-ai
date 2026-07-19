"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function PersonaLoadingSkeleton() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      role="status"
      aria-live="polite"
      aria-label="Loading personas"
      className="space-y-6"
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <Skeleton className="h-4 w-36" />
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-full max-w-xl" />
        </CardHeader>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90 shadow-sm">
            <CardHeader className="space-y-3">
              <Skeleton className="h-4 w-1/2" />
              <Skeleton className="h-3 w-3/5" />
            </CardHeader>
            <CardContent className="space-y-3">
              <Skeleton className="h-3 w-full" />
              <Skeleton className="h-3 w-4/5" />
              <Skeleton className="h-3 w-2/3" />
            </CardContent>
          </Card>
        ))}
      </div>
    </motion.div>
  );
}
