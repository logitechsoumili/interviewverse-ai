"use client";

import type { InterviewListItem } from "@/features/dashboard/types";
import { InterviewHistoryList } from "@/features/dashboard/components/interview-history-list";

type RecentInterviewListProps = {
  interviews: InterviewListItem[];
  limit?: number;
};

export function RecentInterviewList({
  interviews,
  limit = 3,
}: RecentInterviewListProps) {
  return <InterviewHistoryList interviews={interviews.slice(0, limit)} />;
}
