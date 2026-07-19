"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type PersonaEmptyStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  actionHref?: string;
};

export function PersonaEmptyState({
  title,
  description,
  actionLabel = "Create Persona",
  actionHref = "/dashboard/personas/create",
}: PersonaEmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.99 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <div
            aria-hidden="true"
            className="flex h-16 w-16 items-center justify-center rounded-3xl border border-border/70 bg-background/50 shadow-inner"
          >
            <span className="grid h-8 w-8 place-items-center rounded-2xl bg-primary/15 text-primary">
              <span className="h-3 w-3 rounded-sm border border-current" />
            </span>
          </div>
          <CardTitle className="text-lg">{title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="max-w-2xl text-sm leading-6 text-muted-foreground">{description}</p>
          <Button asChild>
            <Link href={actionHref}>{actionLabel}</Link>
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );
}
