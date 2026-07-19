import type { ReactNode } from "react";
import { DashboardLayout as DashboardShell } from "@/components/dashboard/dashboard-layout";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return <DashboardShell>{children}</DashboardShell>;
}
