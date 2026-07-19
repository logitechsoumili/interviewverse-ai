"use client";

import { motion } from "framer-motion";

const STEPS = [
  {
    step: "01",
    title: "Create Account",
    description: "Register your developer profile to initiate your personal workspace and save progress.",
  },
  {
    step: "02",
    title: "Choose Persona",
    description: "Select an AI interviewer persona styled after tech leads, managers, or strict evaluators.",
  },
  {
    step: "03",
    title: "Start Interview",
    description: "Enter the mock interface. Conduct a live audio-capable session responding to questions.",
  },
  {
    step: "04",
    title: "Receive AI Evaluation",
    description: "Review detailed scores, parsed transcripts, highlights, and growth recommendations.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="relative bg-background py-24 px-6 overflow-hidden">
      <div className="pointer-events-none absolute left-[5%] bottom-[10%] h-80 w-80 rounded-full bg-primary/5 blur-[8rem]" />

      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-20">
          <h2 className="font-display text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
            A Simplified Journey to Mastery
          </h2>
          <p className="mt-4 text-sm sm:text-base text-muted-foreground leading-relaxed">
            Follow our four-step pipeline designed to take you from initial sign-up to in-depth analysis reports.
          </p>
        </div>

        {/* Timeline Grid */}
        <div className="relative">
          {/* Connecting line (Desktop) */}
          <div className="absolute top-[40px] left-[12%] right-[12%] hidden h-[2px] bg-gradient-to-r from-primary/30 via-secondary/30 to-primary/30 md:block" />

          <div className="grid gap-8 sm:grid-cols-2 md:grid-cols-4">
            {STEPS.map((step, idx) => (
              <motion.div
                key={step.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-10%" }}
                transition={{ duration: 0.4, delay: idx * 0.1, ease: "easeOut" }}
                className="relative flex flex-col items-center md:items-start text-center md:text-left group"
              >
                {/* Step Circle Bubble */}
                <div className="relative z-10 flex h-20 w-20 items-center justify-center rounded-2xl border border-border bg-surface shadow-lg group-hover:border-primary/50 transition-all duration-300">
                  <span className="font-display text-xl font-bold bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent">
                    {step.step}
                  </span>
                </div>

                {/* Content */}
                <h3 className="mt-6 text-lg font-bold text-foreground group-hover:text-primary transition-colors">
                  {step.title}
                </h3>
                <p className="mt-3 text-sm text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
