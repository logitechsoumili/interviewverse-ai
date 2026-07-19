import type { ReactNode } from "react";
import { DashboardLayout as DashboardShell } from "@/features/dashboard/components/dashboard-layout";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return <DashboardShell>{children}</DashboardShell>;
}
