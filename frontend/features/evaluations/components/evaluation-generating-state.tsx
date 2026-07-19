"use client";

import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";

export function EvaluationGeneratingState() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
    >
      <Card
        className="border-border/80 bg-surface/90 shadow-sm"
        role="status"
        aria-live="polite"
        aria-label="Generating evaluation"
      >
        <CardContent className="flex min-h-[320px] flex-col items-center justify-center gap-4 p-8 text-center">
          <div
            className="h-12 w-12 animate-spin rounded-full border-2 border-primary border-t-transparent"
            aria-hidden="true"
          />
          <div className="space-y-2">
            <p className="text-lg font-semibold tracking-tight">Generating evaluation</p>
            <p className="max-w-md text-sm leading-6 text-muted-foreground">
              The interview has been completed. We are generating the evaluation now and will
              render the results as soon as they are ready.
            </p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
