"use client";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type LoadingSkeletonProps = {
  variant: "dashboard" | "history" | "profile" | "stats";
  className?: string;
};

function SkeletonLine({ className }: { className?: string }) {
  return <div className={cn("rounded-full bg-muted/80 animate-pulse", className)} />;
}

export function LoadingSkeleton({ variant, className }: LoadingSkeletonProps) {
  if (variant === "profile") {
    return (
      <Card className={cn("border-border/80 bg-surface/90", className)}>
        <CardContent className="p-4">
          <div className="flex items-center gap-3">
            <SkeletonLine className="h-11 w-11 rounded-full" />
            <div className="min-w-0 flex-1 space-y-2">
              <SkeletonLine className="h-4 w-32" />
              <SkeletonLine className="h-3 w-44" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (variant === "stats") {
    return (
      <div className={cn("grid gap-4 md:grid-cols-3", className)}>
        {Array.from({ length: 3 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90">
            <CardHeader className="space-y-3">
              <SkeletonLine className="h-3 w-24" />
              <SkeletonLine className="h-8 w-16" />
            </CardHeader>
          </Card>
        ))}
      </div>
    );
  }

  if (variant === "history") {
    return (
      <div className={cn("grid gap-4", className)}>
        {Array.from({ length: 4 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90">
            <CardHeader className="space-y-3">
              <SkeletonLine className="h-5 w-2/5" />
              <SkeletonLine className="h-3 w-1/3" />
            </CardHeader>
            <CardContent className="space-y-3">
              <SkeletonLine className="h-3 w-2/3" />
              <SkeletonLine className="h-3 w-1/2" />
              <div className="flex items-center justify-between pt-2">
                <SkeletonLine className="h-9 w-28" />
                <SkeletonLine className="h-9 w-32" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className={cn("space-y-6", className)}>
      <div className="grid gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90">
            <CardHeader className="space-y-3">
              <SkeletonLine className="h-3 w-24" />
              <SkeletonLine className="h-8 w-16" />
            </CardHeader>
          </Card>
        ))}
      </div>
      <Card className="border-border/80 bg-surface/90">
        <CardHeader className="space-y-3">
          <SkeletonLine className="h-4 w-36" />
          <SkeletonLine className="h-3 w-64" />
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          {Array.from({ length: 3 }).map((_, index) => (
            <Card key={index} className="border-border/80 bg-background/30">
              <CardHeader className="space-y-3">
                <SkeletonLine className="h-4 w-1/2" />
                <SkeletonLine className="h-3 w-2/3" />
              </CardHeader>
              <CardContent className="space-y-3">
                <SkeletonLine className="h-3 w-full" />
                <SkeletonLine className="h-3 w-3/4" />
              </CardContent>
            </Card>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
