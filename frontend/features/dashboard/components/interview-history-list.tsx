"use client";

import { motion } from "framer-motion";
import { InterviewCard } from "@/features/dashboard/components/interview-card";
import type { InterviewListItem } from "@/features/dashboard/types";

type InterviewHistoryListProps = {
  interviews: InterviewListItem[];
};

export function InterviewHistoryList({ interviews }: InterviewHistoryListProps) {
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
      {interviews.map((interview) => (
        <InterviewCard key={interview.id} interview={interview} />
      ))}
    </motion.div>
  );
}
