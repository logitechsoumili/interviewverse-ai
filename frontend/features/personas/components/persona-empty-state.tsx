"use client";

import Link from "next/link";
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
    <Card className="border-border/80 bg-surface/90 shadow-sm">
      <CardHeader className="space-y-3">
        <div className="flex h-16 w-16 items-center justify-center rounded-3xl border border-border bg-background/40 text-2xl">
          *
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
  );
}
