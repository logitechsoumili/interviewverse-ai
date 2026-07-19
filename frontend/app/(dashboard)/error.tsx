"use client";

import { useEffect } from "react";
import { ErrorState } from "@/features/dashboard/components/error-state";

type DashboardErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function DashboardError({ error, reset }: DashboardErrorProps) {
  useEffect(() => {
    console.error("❌ Dashboard page error:", error);
  }, [error]);

  return (
    <div className="w-full max-w-2xl p-6 mx-auto">
      <ErrorState
        title="Dashboard section error"
        description="The system could not load the requested dashboard panel. Let's retry the transition or query the database again."
        actionLabel="Retry Loading"
        onAction={reset}
      >
        {error.digest && (
          <div className="mt-2 font-mono text-[10px] text-muted-foreground select-all">
            Digest: {error.digest}
          </div>
        )}
      </ErrorState>
    </div>
  );
}
