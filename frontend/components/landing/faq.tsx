"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

const FAQS = [
  {
    question: "Is InterviewVerse free?",
    answer: "Yes! InterviewVerse AI offers a generous free tier that gives you access to a selection of default personas and 3 practice sessions per month. Premium tiers unlock unlimited sessions, advanced technical leads, and team progress metrics.",
  },
  {
    question: "Which AI powers the interviews?",
    answer: "Our engine relies on advanced large language models tailored specifically for tech interviews. They are trained to assess technical vocabulary, structural responses, code complexity, and behavioral alignment.",
  },
  {
    question: "Can I practice coding interviews?",
    answer: "Yes! You can choose algorithm-heavy personas that walk you through algorithms, code implementations, logic structures, and complex system architectures.",
  },
  {
    question: "Are reports saved?",
    answer: "Absolutely. Every session generates a detailed scorecard, complete transcript logs, and actionable advice that remain saved securely in your personal history dashboard.",
  },
];

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggle = (idx: number) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  return (
    <section id="faq" className="relative bg-background py-24 px-6 overflow-hidden border-t border-border/30">
      <div className="pointer-events-none absolute left-[-5%] top-[10%] h-80 w-80 rounded-full bg-secondary/5 blur-[8rem]" />

      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="text-center mb-16">
          <span className="text-[10px] font-semibold uppercase tracking-[0.25em] text-primary">
            Help Center
          </span>
          <h2 className="mt-3 font-display text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
            Frequently Asked Questions
          </h2>
          <p className="mt-4 text-sm sm:text-base text-muted-foreground leading-relaxed">
            Quick responses to common questions about InterviewVerse AI workspace functions.
          </p>
        </div>

        {/* Accordions */}
        <div className="space-y-4">
          {FAQS.map((faq, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div
                key={faq.question}
                className="rounded-2xl border border-border/60 bg-surface/40 overflow-hidden transition-all duration-300 hover:border-border/80"
              >
                <button
                  onClick={() => toggle(idx)}
                  className="flex w-full items-center justify-between p-6 text-left font-semibold text-sm sm:text-base text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:ring-inset"
                  aria-expanded={isOpen}
                  aria-controls={`faq-answer-${idx}`}
                >
                  <span>{faq.question}</span>
                  <svg
                    className={cn(
                      "h-4 w-4 text-muted-foreground transition-transform duration-300 shrink-0 ml-4",
                      isOpen && "rotate-180 text-primary"
                    )}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      id={`faq-answer-${idx}`}
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.24, ease: "easeInOut" }}
                    >
                      <div className="px-6 pb-6 pt-0 text-sm leading-relaxed text-muted-foreground border-t border-border/10">
                        {faq.answer}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
