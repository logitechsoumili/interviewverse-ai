"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type LoadingSkeletonProps = {
  variant: "dashboard" | "history" | "profile" | "stats";
  className?: string;
};

function SkeletonLine({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-full bg-[length:200%_100%] bg-[linear-gradient(90deg,hsl(var(--muted)/0.7)_0%,hsl(var(--muted)/0.95)_50%,hsl(var(--muted)/0.7)_100%)] animate-shimmer motion-reduce:animate-none",
        className
      )}
    />
  );
}

export function LoadingSkeleton({ variant, className }: LoadingSkeletonProps) {
  if (variant === "profile") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        role="status"
        aria-live="polite"
        aria-label="Loading profile"
      >
        <Card className={cn("border-border/80 bg-surface/90 shadow-sm", className)}>
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
      </motion.div>
    );
  }

  if (variant === "stats") {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        role="status"
        aria-live="polite"
        aria-label="Loading dashboard statistics"
        className={cn("grid gap-4 md:grid-cols-3", className)}
      >
        {Array.from({ length: 3 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90 shadow-sm">
            <CardHeader className="space-y-3">
              <SkeletonLine className="h-3 w-24" />
              <SkeletonLine className="h-8 w-16" />
            </CardHeader>
          </Card>
        ))}
      </motion.div>
    );
  }

  if (variant === "history") {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        role="status"
        aria-live="polite"
        aria-label="Loading interview history"
        className={cn("grid gap-4", className)}
      >
        {Array.from({ length: 4 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90 shadow-sm">
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
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      role="status"
      aria-live="polite"
      aria-label="Loading dashboard content"
      className={cn("space-y-6", className)}
    >
      <div className="grid gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }).map((_, index) => (
          <Card key={index} className="border-border/80 bg-surface/90 shadow-sm">
            <CardHeader className="space-y-3">
              <SkeletonLine className="h-3 w-24" />
              <SkeletonLine className="h-8 w-16" />
            </CardHeader>
          </Card>
        ))}
      </div>
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <SkeletonLine className="h-4 w-36" />
          <SkeletonLine className="h-3 w-64" />
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          {Array.from({ length: 3 }).map((_, index) => (
            <Card key={index} className="border-border/80 bg-background/30 shadow-sm">
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
    </motion.div>
  );
}
