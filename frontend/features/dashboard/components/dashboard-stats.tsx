"use client";

import { StatCard } from "@/features/dashboard/components/stat-card";
import type { DashboardStats } from "@/features/dashboard/types";

type DashboardStatsProps = {
  stats: DashboardStats;
};

export function DashboardStats({ stats }: DashboardStatsProps) {
  return (
    <section className="grid gap-4 md:grid-cols-3">
      <StatCard label="Total Interviews" value={stats.total} hint="All sessions" />
      <StatCard label="Completed" value={stats.completed} hint="Finished" />
      <StatCard label="Pending" value={stats.pending} hint="In progress" />
    </section>
  );
}
