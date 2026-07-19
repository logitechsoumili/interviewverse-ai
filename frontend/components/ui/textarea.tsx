import * as React from "react";
import { cn } from "@/lib/utils";

const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn(
      "flex min-h-[120px] w-full rounded-md border border-border/80 bg-background/70 px-3 py-2 text-sm text-foreground shadow-sm transition-all duration-200 ease-out placeholder:text-muted-foreground focus-visible:outline-none focus-visible:border-primary/60 focus-visible:bg-background focus-visible:ring-2 focus-visible:ring-ring/30 disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
      className
    )}
    {...props}
  />
));
Textarea.displayName = "Textarea";

export { Textarea };
