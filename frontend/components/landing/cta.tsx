"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

export function CTA() {
  return (
    <section className="relative bg-background py-24 px-6 overflow-hidden border-t border-border/30">
      {/* Background glow */}
      <div className="pointer-events-none absolute left-1/2 top-1/2 h-[30rem] w-[30rem] -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary/10 blur-[8rem]" />

      <div className="relative z-10 mx-auto max-w-4xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="rounded-3xl border border-border bg-surface/40 p-12 backdrop-blur-xl shadow-2xl space-y-6"
        >
          <h2 className="font-display text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
            Ready to Ace Your Next Interview?
          </h2>
          <p className="mx-auto max-w-xl text-sm sm:text-base leading-relaxed text-muted-foreground">
            Join thousands of developers using autonomous AI simulation models to target weaknesses, grow confidence, and secure high-compensation offers.
          </p>
          <div className="pt-4 flex justify-center">
            <Button size="lg" className="w-full sm:w-auto px-10 animate-pulse hover:animate-none" asChild>
              <Link href="/register">Start Practicing</Link>
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
