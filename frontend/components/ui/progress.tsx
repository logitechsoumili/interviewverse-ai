import * as React from "react";
import { cn } from "@/lib/utils";

type ProgressProps = React.HTMLAttributes<HTMLDivElement> & {
  value: number;
  label?: string;
};

export function Progress({ className, value, label, ...props }: ProgressProps) {
  const safeValue = Math.max(0, Math.min(100, value));

  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={safeValue}
      className={cn(
        "relative h-2 w-full overflow-hidden rounded-full bg-muted/70",
        className
      )}
      {...props}
    >
      <div
        className="h-full rounded-full bg-gradient-to-r from-primary to-secondary transition-[width] duration-700 ease-out motion-reduce:transition-none"
        style={{ width: `${safeValue}%` }}
      />
    </div>
  );
}
