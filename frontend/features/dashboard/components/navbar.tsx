"use client";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import type { User } from "@/types/auth";

type NavbarProps = {
  user: User | null;
  isLoading?: boolean;
  onMenuClick: () => void;
  onLogout: () => void;
};

function UserChip({ user, isLoading }: { user: User | null; isLoading?: boolean }) {
  if (isLoading) {
    return (
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 animate-pulse rounded-full bg-muted/80" />
        <div className="space-y-2">
          <div className="h-3 w-28 animate-pulse rounded-full bg-muted/80" />
          <div className="h-3 w-36 animate-pulse rounded-full bg-muted/80" />
        </div>
      </div>
    );
  }

  const initials =
    user?.full_name
      ?.split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part.charAt(0).toUpperCase())
      .join("") || "IV";

  return (
    <div className="flex items-center gap-3">
      <div className="flex h-10 w-10 items-center justify-center rounded-full border border-border bg-gradient-to-br from-primary/40 to-secondary/30 text-sm font-semibold text-foreground">
        {initials}
      </div>
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-foreground">
          {user?.full_name || "Account"}
        </p>
        <p className="truncate text-xs text-muted-foreground">
          {user?.email || "profile@interviewverse.ai"}
        </p>
      </div>
    </div>
  );
}

export function Navbar({ user, isLoading, onMenuClick, onLogout }: NavbarProps) {
  return (
    <header className="sticky top-0 z-30 border-b border-border/70 bg-background/85 backdrop-blur-xl">
      <div className="flex items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex min-w-0 items-center gap-3">
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="lg:hidden"
            onClick={onMenuClick}
            aria-label="Open navigation"
          >
            <span className="flex flex-col gap-1">
              <span className="h-0.5 w-4 rounded-full bg-current" />
              <span className="h-0.5 w-4 rounded-full bg-current" />
              <span className="h-0.5 w-4 rounded-full bg-current" />
            </span>
          </Button>
          <div className="min-w-0">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">
              Dashboard
            </p>
            <p className="truncate text-base font-medium text-foreground">
              InterviewVerse AI
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <UserChip user={user} isLoading={isLoading} />
          <Separator className="hidden h-8 w-px bg-border/70 md:block" />
          <Button type="button" variant="outline" onClick={onLogout}>
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
}
