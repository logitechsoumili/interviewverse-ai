"use client";

import type { ReactNode } from "react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";

type ProtectedRouteProps = {
  children: ReactNode;
};

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();
  const auth = useAuth();

  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      router.replace("/login");
    }
  }, [auth.isAuthenticated, auth.isLoading, router]);

  if (auth.isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="rounded-2xl border border-border bg-surface px-6 py-5 text-sm text-muted-foreground">
          Restoring your session...
        </div>
      </main>
    );
  }

  if (!auth.isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
