"use client";

import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import { Button } from "@/components/ui/button";

type InterviewConfirmDialogProps = {
  open: boolean;
  title: string;
  description: string;
  confirmLabel?: string;
  cancelLabel?: string;
  pending?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
};

export function InterviewConfirmDialog({
  open,
  title,
  description,
  confirmLabel = "End Interview",
  cancelLabel = "Cancel",
  pending = false,
  onConfirm,
  onCancel,
}: InterviewConfirmDialogProps) {
  const confirmButtonRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    if (!open) {
      return;
    }

    confirmButtonRef.current?.focus();

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onCancel();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onCancel]);

  if (!open || typeof document === "undefined") {
    return null;
  }

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 px-4 backdrop-blur-sm"
      role="presentation"
      onMouseDown={onCancel}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="end-interview-title"
        aria-describedby="end-interview-description"
        className="w-full max-w-lg rounded-3xl border border-border/80 bg-surface p-6 shadow-2xl"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="space-y-3">
          <h2 id="end-interview-title" className="text-xl font-semibold tracking-tight">
            {title}
          </h2>
          <p id="end-interview-description" className="text-sm leading-6 text-muted-foreground">
            {description}
          </p>
        </div>

        <div className="mt-6 flex flex-wrap justify-end gap-3">
          <Button type="button" variant="outline" onClick={onCancel} disabled={pending}>
            {cancelLabel}
          </Button>
          <Button type="button" onClick={onConfirm} disabled={pending} ref={confirmButtonRef}>
            {pending ? "Ending..." : confirmLabel}
          </Button>
        </div>
      </div>
    </div>,
    document.body
  );
}
