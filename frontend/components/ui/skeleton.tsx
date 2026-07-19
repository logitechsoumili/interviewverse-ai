import { cn } from "@/lib/utils";

type SkeletonProps = {
  className?: string;
};

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn(
        "rounded-md bg-[length:200%_100%] bg-[linear-gradient(90deg,hsl(var(--muted)/0.7)_0%,hsl(var(--muted)/0.95)_50%,hsl(var(--muted)/0.7)_100%)] animate-shimmer motion-reduce:animate-none",
        className
      )}
    />
  );
}
