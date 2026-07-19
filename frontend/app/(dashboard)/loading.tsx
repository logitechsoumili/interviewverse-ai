import { LoadingSkeleton } from "@/features/dashboard/components/loading-skeleton";

export default function DashboardLoading() {
  return (
    <div className="w-full p-6 animate-pulse">
      <LoadingSkeleton variant="dashboard" />
    </div>
  );
}
