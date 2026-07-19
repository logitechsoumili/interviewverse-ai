"use client";

import type { ReactNode } from "react";
import { motion } from "framer-motion";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { BrandMark } from "@/components/auth/brand-mark";

type AuthShellProps = {
  title: string;
  description: string;
  children: ReactNode;
  footer: ReactNode;
};

export function AuthShell({
  title,
  description,
  children,
  footer,
}: AuthShellProps) {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-6 py-12">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[-5rem] top-[-5rem] h-72 w-72 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute bottom-[-7rem] right-[-4rem] h-72 w-72 rounded-full bg-secondary/10 blur-3xl" />
      </div>

      <motion.section
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.28, ease: "easeOut" }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="mb-6 flex items-center gap-3">
          <BrandMark />
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.24em] text-muted-foreground">
              InterviewVerse AI
            </p>
            <p className="font-display text-lg font-semibold text-foreground">
              Authentication
            </p>
          </div>
        </div>

        <Card className="border-border/80 bg-surface/90 shadow-lg shadow-black/20 backdrop-blur-xl">
          <CardHeader className="space-y-2">
            <CardTitle className="font-display text-2xl">{title}</CardTitle>
            <CardDescription className="text-sm leading-6">
              {description}
            </CardDescription>
          </CardHeader>
          <Separator className="mb-6" />
          <CardContent>{children}</CardContent>
          <div className="px-6 pb-6">{footer}</div>
        </Card>
      </motion.section>
    </main>
  );
}
