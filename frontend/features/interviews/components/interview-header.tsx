"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  formatElapsedTime,
  formatInterviewStatus,
  getInterviewStatusTone,
} from "@/features/interviews/utils";
import type { InterviewSession } from "@/features/interviews/types";

type InterviewHeaderProps = {
  session: InterviewSession;
  onEndInterview: () => void;
};

export function InterviewHeader({ session, onEndInterview }: InterviewHeaderProps) {
  const [, setTick] = useState(0);

  useEffect(() => {
    if (session.status === "completed") {
      return;
    }

    const interval = window.setInterval(() => {
      setTick((value) => value + 1);
    }, 1000);

    return () => window.clearInterval(interval);
  }, [session.status]);

  const elapsed = formatElapsedTime(session.startedAt, session.completedAt);

  return (
    <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
      <CardContent className="space-y-5 p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.32em] text-secondary">
              Live Interview
            </p>
            <h1 className="text-3xl font-semibold tracking-tight">{session.personaName}</h1>
            <p className="max-w-3xl text-sm leading-6 text-muted-foreground">
              {session.personaRole} | {session.title}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Badge variant={getInterviewStatusTone(session.status)}>
              {formatInterviewStatus(session.status)}
            </Badge>
            <div className="rounded-2xl border border-border/70 bg-background/50 px-4 py-3 text-sm">
              <div className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">
                Elapsed
              </div>
              <div className="mt-1 font-semibold tabular-nums">{elapsed}</div>
            </div>
            <Button
              type="button"
              variant="outline"
              onClick={onEndInterview}
              disabled={session.status === "completed"}
            >
              End Interview
            </Button>
          </div>
        </div>

        <div className="grid gap-3 text-sm text-muted-foreground sm:grid-cols-3">
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Persona</div>
            <div className="mt-1 text-foreground">{session.personaName}</div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Difficulty</div>
            <div className="mt-1 text-foreground">{session.difficulty}</div>
          </div>
          <div className="rounded-2xl border border-border/70 bg-background/40 px-4 py-3">
            <div className="text-[11px] uppercase tracking-[0.24em]">Topics</div>
            <div className="mt-1 text-foreground">{session.topics.join(", ")}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
