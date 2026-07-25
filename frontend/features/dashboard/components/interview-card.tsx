"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  formatInterviewDate,
  formatPersonaName,
  getInterviewStatusLabel,
  getInterviewStatusTone,
} from "@/features/dashboard/utils";
import type { InterviewListItem } from "@/features/dashboard/types";
import { cn } from "@/lib/utils";

type InterviewCardProps = {
  interview: InterviewListItem;
};

export function InterviewCard({ interview }: InterviewCardProps) {
  const personaName = formatPersonaName(interview.persona);
  const createdDate = formatInterviewDate(interview.created_at);
  const completedDate = interview.completed_at
    ? formatInterviewDate(interview.completed_at)
    : null;

  return (
    <motion.article
      whileHover={{ y: -2 }}
      transition={{ duration: 0.18, ease: "easeOut" }}
    >
      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader className="space-y-3">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div className="space-y-1">
              <CardTitle className="text-xl tracking-tight">
                Interview with {personaName}
              </CardTitle>
              <p className="text-sm text-muted-foreground">Persona: {personaName}</p>
            </div>
            <span
              className={cn(
                "inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium",
                getInterviewStatusTone(interview.status)
              )}
            >
              {getInterviewStatusLabel(interview.status)}
            </span>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid gap-2 text-sm text-muted-foreground sm:grid-cols-2">
            <p>
              <span className="text-foreground">Created:</span> {createdDate}
            </p>
            <p>
              <span className="text-foreground">Completion:</span>{" "}
              {completedDate || "Pending"}
            </p>
          </div>
        </CardContent>
        <CardFooter className="justify-end">
          <Button asChild variant="outline">
            <Link href={interview.status === "completed" ? `/dashboard/interview/${interview.id}/report` : `/dashboard/interview/${interview.id}`}>
              View Details
            </Link>
          </Button>
        </CardFooter>
      </Card>
    </motion.article>
  );
}
