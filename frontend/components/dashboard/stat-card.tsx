"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type StatCardProps = {
  label: string;
  value: string | number;
  hint?: string;
  className?: string;
};

export function StatCard({ label, value, hint, className }: StatCardProps) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ duration: 0.18, ease: "easeOut" }}
      className={className}
    >
      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader className="pb-2">
          <p className="text-sm text-muted-foreground">{label}</p>
          <CardTitle className="text-3xl tracking-tight">{value}</CardTitle>
        </CardHeader>
        {hint ? (
          <CardContent className="pt-0">
            <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
              {hint}
            </p>
          </CardContent>
        ) : null}
      </Card>
    </motion.div>
  );
}
