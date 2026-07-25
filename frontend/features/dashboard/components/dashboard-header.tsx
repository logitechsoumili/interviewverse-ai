"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function DashboardHeader() {
  return (
    <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
      <CardHeader className="space-y-4">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
          Welcome
        </p>
        <CardTitle className="text-3xl tracking-tight sm:text-4xl">
          InterviewVerse AI dashboard is ready.
        </CardTitle>
        <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
          Review your latest sessions, keep an eye on completion progress, and
          jump back into the workflow without leaving the workspace.
        </p>
      </CardHeader>
      <CardContent className="flex flex-wrap gap-3">
        <Button asChild>
          <Link href="/dashboard/personas">Start Interview</Link>
        </Button>
        <Button asChild variant="outline">
          <Link href="/dashboard/history">View History</Link>
        </Button>
      </CardContent>
    </Card>
  );
}
