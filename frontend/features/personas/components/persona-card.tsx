"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { StartInterviewButton } from "@/features/interviews/components/start-interview-button";
import type { PersonaDisplayPersona } from "@/features/personas/types";

type PersonaCardProps = {
  persona: PersonaDisplayPersona;
};

export function PersonaCard({ persona }: PersonaCardProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.article
      whileHover={{ y: -2 }}
      transition={{ duration: 0.18, ease: "easeOut" }}
      className="h-full"
    >
      <Card className="flex h-full flex-col border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader className="space-y-4">
          <div className="flex items-start justify-between gap-3">
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <CardTitle className="text-xl tracking-tight">{persona.name}</CardTitle>
                <Badge variant={persona.source === "built-in" ? "default" : "outline"}>
                  {persona.source === "built-in" ? "Built-in" : "Custom"}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">{persona.role}</p>
            </div>
          </div>

          <div className="grid gap-2 text-sm text-muted-foreground sm:grid-cols-2">
            <p>
              <span className="text-foreground">Experience:</span>{" "}
              {persona.experienceLevel}
            </p>
            <p>
              <span className="text-foreground">Company:</span> {persona.company}
            </p>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          <p className="text-sm leading-6 text-muted-foreground">
            {persona.shortDescription}
          </p>

          <div className="flex flex-wrap gap-2">
            {persona.tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="secondary">
                {tag}
              </Badge>
            ))}
          </div>

          <AnimatePresence initial={false}>
            {isOpen ? (
              <motion.div
                key="persona-details"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2, ease: "easeOut" }}
                className="overflow-hidden"
              >
                <Separator className="my-4 bg-border/70" />
                <div className="space-y-4">
                  <div className="space-y-1">
                    <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                      Full Description
                    </p>
                    <p className="text-sm leading-6 text-foreground">
                      {persona.description}
                    </p>
                  </div>

                  <div className="grid gap-3 sm:grid-cols-2">
                    <div className="space-y-1 rounded-xl border border-border/70 bg-background/40 p-3">
                      <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                        Interview Style
                      </p>
                      <p className="text-sm text-foreground">{persona.interviewStyle}</p>
                    </div>
                    <div className="space-y-1 rounded-xl border border-border/70 bg-background/40 p-3">
                      <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                        Difficulty
                      </p>
                      <p className="text-sm text-foreground">{persona.difficulty}</p>
                    </div>
                    <div className="space-y-1 rounded-xl border border-border/70 bg-background/40 p-3">
                      <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                        Expertise
                      </p>
                      <p className="text-sm text-foreground">
                        {persona.expertise.join(", ")}
                      </p>
                    </div>
                    <div className="space-y-1 rounded-xl border border-border/70 bg-background/40 p-3">
                      <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                        Company
                      </p>
                      <p className="text-sm text-foreground">{persona.company}</p>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                      Industry
                    </p>
                    <p className="text-sm text-foreground">{persona.industry}</p>
                  </div>

                  {persona.tags.length > 0 ? (
                    <div className="space-y-2">
                      <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                        Tags
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {persona.tags.map((tag) => (
                          <Badge key={tag} variant="outline">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              </motion.div>
            ) : null}
          </AnimatePresence>
        </CardContent>

        <CardFooter className="mt-auto flex flex-wrap gap-3 pt-0">
          <Button type="button" variant="outline" onClick={() => setIsOpen((value) => !value)}>
            {isOpen ? "Hide Details" : "View Details"}
          </Button>
          <StartInterviewButton
            personaId={persona.id}
            personaName={persona.name}
            personaRole={persona.role}
          />
        </CardFooter>
      </Card>
    </motion.article>
  );
}
