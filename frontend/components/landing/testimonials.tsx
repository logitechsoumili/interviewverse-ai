"use client";

import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";

const TESTIMONIALS = [
  {
    name: "Alex Rivera",
    role: "Senior Software Engineer at Vercel",
    text: "The AI personas are incredibly realistic. Sarah's tech probes felt exactly like my real systems design loops. Landed my dream offer in record time.",
    avatar: "AR",
  },
  {
    name: "Samantha Chen",
    role: "Fullstack Engineer at Stripe",
    text: "I loved the communication score breakout. Practicing behavioral mocks with Marcus really lowered my interview day stress and anxiety levels.",
    avatar: "SC",
  },
  {
    name: "Daniel Mwangi",
    role: "Systems Architect at AWS",
    text: "The instant evaluation analysis is top tier. Getting granular code recommendations on edge-cases helped me optimize my backend design explanations.",
    avatar: "DM",
  },
];

export function Testimonials() {
  return (
    <section className="relative bg-background py-24 px-6 overflow-hidden border-t border-border/30">
      <div className="pointer-events-none absolute right-[10%] bottom-[10%] h-80 w-80 rounded-full bg-secondary/5 blur-[8rem]" />

      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="text-[10px] font-semibold uppercase tracking-[0.25em] text-primary">
            Testimonials
          </span>
          <h2 className="mt-3 font-display text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
            What Our Candidates Say
          </h2>
          <p className="mt-4 text-sm sm:text-base text-muted-foreground leading-relaxed">
            Read how developers use our platform to lock in high-quality technical offers.
          </p>
        </div>

        {/* Grid */}
        <div className="grid gap-6 md:grid-cols-3">
          {TESTIMONIALS.map((t, idx) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-10%" }}
              transition={{ duration: 0.35, delay: idx * 0.05, ease: "easeOut" }}
            >
              <Card className="h-full border-border/60 bg-surface/40 hover:bg-surface/75 transition-all duration-300 flex flex-col justify-between p-6">
                <CardContent className="p-0 flex-1 flex flex-col justify-between space-y-6">
                  {/* Quote Icon */}
                  <svg className="h-6 w-6 text-muted-foreground/30 shrink-0" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                  </svg>
                  {/* Text */}
                  <p className="text-sm leading-relaxed text-muted-foreground italic flex-1">
                    &ldquo;{t.text}&rdquo;
                  </p>
                  {/* Divider */}
                  <div className="border-t border-border/40 pt-4 flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center font-bold text-primary text-[10px]">
                      {t.avatar}
                    </div>
                    <div>
                      <p className="text-xs font-bold text-foreground">{t.name}</p>
                      <p className="text-[10px] text-muted-foreground mt-0.5">{t.role}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
