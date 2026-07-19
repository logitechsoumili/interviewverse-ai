import type { ReactNode } from "react";
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
    <main className="flex min-h-screen items-center justify-center px-6 py-12">
      <section className="w-full max-w-md">
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

        <Card className="border-border/80 shadow-lg shadow-black/20">
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
      </section>
    </main>
  );
}
