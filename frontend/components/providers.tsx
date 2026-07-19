"use client";

import type { ReactNode } from "react";
import { MotionConfig } from "framer-motion";
import { QueryProvider } from "@/components/query-provider";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/toaster";
import { AuthProvider } from "@/features/auth/auth-context";

type ProvidersProps = {
  children: ReactNode;
};

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider>
      <MotionConfig reducedMotion="user">
        <QueryProvider>
          <AuthProvider>
            {children}
            <Toaster />
          </AuthProvider>
        </QueryProvider>
      </MotionConfig>
    </ThemeProvider>
  );
}
