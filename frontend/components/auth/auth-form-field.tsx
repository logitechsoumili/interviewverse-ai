import type { ReactNode } from "react";
import { Label } from "@/components/ui/label";

type AuthFormFieldProps = {
  id: string;
  label: string;
  error?: string;
  helperText?: string;
  children: ReactNode;
};

export function AuthFormField({
  id,
  label,
  error,
  helperText,
  children,
}: AuthFormFieldProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>
      {children}
      {helperText ? (
        <p className="text-xs text-muted-foreground">{helperText}</p>
      ) : null}
      {error ? (
        <p id={`${id}-error`} className="text-sm text-destructive">
          {error}
        </p>
      ) : null}
    </div>
  );
}
