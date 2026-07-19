"use client";

import { motion } from "framer-motion";
import { InterviewCard } from "@/components/dashboard/interview-card";
import type { InterviewListItem } from "@/types/dashboard";

type HistoryListProps = {
  interviews: InterviewListItem[];
  limit?: number;
};

export function HistoryList({ interviews, limit }: HistoryListProps) {
  const visibleInterviews =
    typeof limit === "number" ? interviews.slice(0, limit) : interviews;

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: {
          transition: {
            staggerChildren: 0.05,
          },
        },
      }}
      className="grid gap-4"
    >
      {visibleInterviews.map((interview) => (
        <InterviewCard key={interview.id} interview={interview} />
      ))}
    </motion.div>
  );
}
