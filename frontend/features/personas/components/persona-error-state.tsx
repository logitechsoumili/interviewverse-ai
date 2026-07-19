"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type PersonaErrorStateProps = {
  message: string;
  onRetry: () => void;
};

export function PersonaErrorState({ message, onRetry }: PersonaErrorStateProps) {
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
          <CardTitle className="text-lg">Unable to load personas</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="max-w-2xl text-sm leading-6 text-muted-foreground">{message}</p>
          <Button type="button" onClick={onRetry}>
            Try Again
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );
}
