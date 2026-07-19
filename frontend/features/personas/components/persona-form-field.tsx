"use client";

import type { ReactNode } from "react";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

type PersonaFormFieldProps = {
  id: string;
  label: string;
  error?: string;
  helperText?: string;
  className?: string;
  children: ReactNode;
};

export function PersonaFormField({
  id,
  label,
  error,
  helperText,
  className,
  children,
}: PersonaFormFieldProps) {
  return (
    <div className={cn("space-y-2", className)}>
      <Label htmlFor={id}>{label}</Label>
      {children}
      {helperText ? (
        <p className="text-xs text-muted-foreground">{helperText}</p>
      ) : null}
      {error ? (
        <p className="text-xs text-destructive" id={`${id}-error`}>
          {error}
        </p>
      ) : null}
    </div>
  );
}
