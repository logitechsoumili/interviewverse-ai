"use client";

import { Card, CardContent } from "@/components/ui/card";
import { LoadingSkeleton } from "@/features/dashboard/components/loading-skeleton";
import { getApiErrorMessage } from "@/lib/api-error";
import type { User } from "@/types/auth";
import { cn } from "@/lib/utils";

type UserProfileCardProps = {
  user: User | null;
  isLoading?: boolean;
  error?: unknown;
  compact?: boolean;
  className?: string;
};

function getInitials(name: string) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join("");
}

export function UserProfileCard({
  user,
  isLoading,
  error,
  compact = false,
  className,
}: UserProfileCardProps) {
  if (isLoading) {
    return <LoadingSkeleton variant="profile" className={className} />;
  }

  if (error) {
    return (
      <Card className={cn("border-border/80 bg-surface/90 shadow-sm", className)}>
        <CardContent className={cn(compact ? "p-3" : "p-4")}>
          <p className="text-sm font-medium">Profile unavailable</p>
          <p className="mt-1 text-sm text-muted-foreground">
            {getApiErrorMessage(error)}
          </p>
        </CardContent>
      </Card>
    );
  }

  const fullName = user?.full_name || "Account";
  const email = user?.email || "profile@interviewverse.ai";

  return (
    <Card className={cn("border-border/80 bg-surface/90 shadow-sm", className)}>
      <CardContent className={cn("flex items-center gap-3", compact ? "p-3" : "p-4")}>
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-border bg-gradient-to-br from-primary/40 to-secondary/30 text-sm font-semibold text-foreground">
          {getInitials(fullName) || "IV"}
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-foreground">{fullName}</p>
          <p className="truncate text-xs text-muted-foreground">{email}</p>
        </div>
      </CardContent>
    </Card>
  );
}
