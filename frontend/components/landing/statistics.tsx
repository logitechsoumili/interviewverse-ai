"use client";

import { motion } from "framer-motion";

const STATS = [
  { value: "500+", label: "AI Personas" },
  { value: "10k+", label: "Practice Mocks" },
  { value: "95%", label: "Success Rate" },
  { value: "24/7", label: "Availability" },
];

export function Statistics() {
  return (
    <section className="relative bg-background py-20 px-6 overflow-hidden border-t border-border/30">
      <div className="mx-auto max-w-7xl">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          {STATS.map((stat, idx) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true, margin: "-10%" }}
              transition={{ duration: 0.3, delay: idx * 0.05, ease: "easeOut" }}
              className="text-center space-y-2 group"
            >
              <div className="font-display text-4xl font-extrabold tracking-tight bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent sm:text-5xl transition-transform duration-300 group-hover:scale-105">
                {stat.value}
              </div>
              <div className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
