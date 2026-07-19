"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PersonaListView } from "@/features/personas/components/persona-list-view";

export function PersonasPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="space-y-6"
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
              Persona Management
            </p>
            <CardTitle className="text-2xl tracking-tight">
              Build and organize interviewer personas.
            </CardTitle>
          </div>
          <Button asChild>
            <Link href="/dashboard/personas/create">Create Persona</Link>
          </Button>
        </CardHeader>
        <CardContent>
          <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
            Browse built-in and custom personas, inspect their styles, and prepare
            new personas for the interview workflow.
          </p>
        </CardContent>
      </Card>

      <PersonaListView />
    </motion.div>
  );
}
