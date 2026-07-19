"use client";

import { useEffect } from "react";

type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function RootError({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log the error to console in a styled format
    console.error("❌ Root error boundary caught:", error);
  }, [error]);

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center bg-background px-6 text-center overflow-hidden">
      {/* Background Radial Glow */}
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div className="h-[24rem] w-[24rem] rounded-full bg-destructive/10 blur-[6rem]" />
      </div>

      <div className="relative z-10 w-full max-w-md rounded-2xl border border-destructive/20 bg-surface/40 p-8 backdrop-blur-xl shadow-2xl">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-destructive/10 text-destructive">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="h-6 w-6"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
            />
          </svg>
        </div>

        <h1 className="mt-6 text-2xl font-bold tracking-tight text-foreground font-display">
          System Exception
        </h1>
        <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
          An error occurred in the workspace application shell. The system has logged the exception.
        </p>

        {error.digest && (
          <div className="mt-4 rounded border border-border/40 bg-muted/30 p-2.5 font-mono text-[10px] text-muted-foreground select-all">
            Reference ID: {error.digest}
          </div>
        )}

        <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
          <button
            onClick={() => reset()}
            className="inline-flex items-center justify-center rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground shadow-lg transition-all hover:brightness-110 active:scale-[0.98] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            Attempt Recovery
          </button>
          <button
            onClick={() => window.location.replace("/")}
            className="inline-flex items-center justify-center rounded-xl border border-border bg-surface px-5 py-2.5 text-sm font-semibold text-foreground transition-all hover:bg-accent focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border active:scale-[0.98]"
          >
            Return Home
          </button>
        </div>
      </div>
    </div>
  );
}
