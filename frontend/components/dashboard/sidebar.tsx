"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { UserProfileCard } from "@/components/dashboard/user-profile-card";
import type { User } from "@/types/auth";
import { cn } from "@/lib/utils";

type SidebarProps = {
  user: User | null;
  isLoading?: boolean;
  error?: unknown;
  open: boolean;
  onClose: () => void;
};

const NAV_ITEMS = [
  { label: "Dashboard", href: "/dashboard", disabled: false },
  { label: "History", href: "/dashboard/history", disabled: false },
  { label: "Personas", href: "#", disabled: true },
  { label: "Settings", href: "#", disabled: true },
] as const;

export function Sidebar({ user, isLoading, error, open, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      <div
        className={cn(
          "fixed inset-0 z-30 bg-background/70 backdrop-blur-sm transition-opacity lg:hidden",
          open ? "opacity-100" : "pointer-events-none opacity-0"
        )}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-80 max-w-[85vw] flex-col border-r border-border/70 bg-surface/95 backdrop-blur-xl transition-transform duration-200 lg:static lg:z-auto lg:w-72 lg:translate-x-0",
          open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        <div className="flex items-center justify-between gap-3 p-5 lg:p-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
              InterviewVerse AI
            </p>
            <p className="mt-1 text-lg font-semibold text-foreground">Workspace</p>
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="lg:hidden"
            onClick={onClose}
          >
            Close
          </Button>
        </div>

        <div className="px-5 lg:px-6">
          <UserProfileCard
            user={user}
            isLoading={isLoading}
            error={error}
            className="shadow-none"
          />
        </div>

        <Separator className="my-5 bg-border/70" />

        <nav className="flex-1 px-3 lg:px-4">
          <div className="space-y-1">
            {NAV_ITEMS.map((item) => {
              const isActive =
                !item.disabled &&
                (item.href === "/dashboard"
                  ? pathname === item.href
                  : pathname === item.href || pathname.startsWith(`${item.href}/`));

              if (item.disabled) {
                return (
                  <div
                    key={item.label}
                    aria-disabled="true"
                    className="flex items-center rounded-xl px-4 py-3 text-sm text-muted-foreground/80 opacity-60"
                  >
                    {item.label}
                    <span className="ml-auto rounded-full border border-border px-2 py-0.5 text-[11px] uppercase tracking-[0.24em]">
                      Soon
                    </span>
                  </div>
                );
              }

              return (
                <Link
                  key={item.label}
                  href={item.href}
                  onClick={onClose}
                  className={cn(
                    "flex items-center rounded-xl px-4 py-3 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary/15 text-primary shadow-sm"
                      : "text-muted-foreground hover:bg-accent hover:text-foreground"
                  )}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>
        </nav>

        <div className="p-5 lg:p-6">
          <div className="rounded-2xl border border-border/70 bg-background/40 p-4 text-sm text-muted-foreground">
            Subtle analytics and workspace controls live here.
          </div>
        </div>
      </aside>
    </>
  );
}
