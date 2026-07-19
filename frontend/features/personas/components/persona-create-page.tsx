"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PersonaCreateForm } from "@/features/personas/components/persona-create-form";

export function PersonaCreatePage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="space-y-6"
    >
      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardHeader className="space-y-3">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
            Create Persona
          </p>
          <CardTitle className="text-2xl tracking-tight">
            Define a new interviewer persona.
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button asChild variant="outline">
            <Link href="/dashboard/personas">Back to Personas</Link>
          </Button>
        </CardContent>
      </Card>

      <Card className="border-border/80 bg-surface/90 shadow-sm">
        <CardContent className="p-6">
          <PersonaCreateForm />
        </CardContent>
      </Card>
    </motion.div>
  );
}
