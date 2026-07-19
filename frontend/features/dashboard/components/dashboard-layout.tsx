"use client";

import type { ReactNode } from "react";
import { useState } from "react";
import { motion } from "framer-motion";
import { ProtectedRoute } from "@/components/auth/protected-route";
import { Navbar } from "@/features/dashboard/components/navbar";
import { Sidebar } from "@/features/dashboard/components/sidebar";
import { useAuth } from "@/hooks/use-auth";
import { useCurrentUserQuery } from "@/features/auth/hooks/use-current-user";

type DashboardLayoutProps = {
  children: ReactNode;
};

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { logout } = useAuth();
  const currentUserQuery = useCurrentUserQuery();
  const isUserLoading =
    currentUserQuery.isLoading ||
    (!currentUserQuery.data && currentUserQuery.isFetching);

  return (
    <ProtectedRoute>
      <div className="relative min-h-screen overflow-hidden bg-background">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute left-[-8rem] top-[-6rem] h-72 w-72 rounded-full bg-primary/10 blur-3xl" />
          <div className="absolute right-[-7rem] top-40 h-80 w-80 rounded-full bg-secondary/10 blur-3xl" />
          <div className="absolute bottom-[-8rem] left-1/2 h-72 w-72 -translate-x-1/2 rounded-full bg-primary/5 blur-3xl" />
        </div>

        <div className="relative z-10 flex min-h-screen">
          <Sidebar
            user={currentUserQuery.data ?? null}
            isLoading={isUserLoading}
            error={currentUserQuery.error}
            open={isSidebarOpen}
            onClose={() => setIsSidebarOpen(false)}
          />

          <div className="flex min-w-0 flex-1 flex-col">
            <Navbar
              user={currentUserQuery.data ?? null}
              isLoading={isUserLoading}
              onMenuClick={() => setIsSidebarOpen(true)}
              onLogout={logout}
            />

            <motion.main
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="flex-1 px-4 py-6 sm:px-6 lg:px-8 lg:py-8"
            >
              {children}
            </motion.main>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
