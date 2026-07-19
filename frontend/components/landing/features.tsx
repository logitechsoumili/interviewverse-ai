"use client";

import { motion } from "framer-motion";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const FEATURES = [
  {
    title: "AI Personas",
    description: "Choose from a roster of expert AI personas with distinct behaviors, difficulty levels, and organizational cultures.",
    icon: (
      <svg className="h-5 w-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
    ),
  },
  {
    title: "Real-time Interview Chat",
    description: "Engage in dynamic, low-latency mock interviews. Converse with autonomous AI agents that react naturally.",
    icon: (
      <svg className="h-5 w-5 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
    ),
  },
  {
    title: "Instant Evaluation",
    description: "Receive scorecard reviews measuring response structure, communication clarity, and technical competence.",
    icon: (
      <svg className="h-5 w-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    title: "Personalized Reports",
    description: "Access diagnostic analysis covering your strengths, weaknesses, and concrete recommendations for growth.",
    icon: (
      <svg className="h-5 w-5 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
  },
  {
    title: "Progress Tracking",
    description: "Monitor your preparation growth. Review historical trends of all previous interviews in your archive.",
    icon: (
      <svg className="h-5 w-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
      </svg>
    ),
  },
  {
    title: "Secure Cloud Platform",
    description: "Keep your interview history safe. Your personal workspace and details are securely hosted in our vault.",
    icon: (
      <svg className="h-5 w-5 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    ),
  },
];

export function Features() {
  return (
    <section id="features" className="relative bg-background py-24 px-6 overflow-hidden">
      {/* Glow ambient background decorator */}
      <div className="pointer-events-none absolute right-[5%] top-[10%] h-80 w-80 rounded-full bg-secondary/5 blur-[7rem]" />

      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="font-display text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
            A Complete Prep Suite in One Workspace
          </h2>
          <p className="mt-4 text-sm sm:text-base text-muted-foreground leading-relaxed">
            No scheduling delays. No expensive mock coaches. Explore features tailored to elevate your performance.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((feature, idx) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-10%" }}
              transition={{ duration: 0.35, delay: idx * 0.05, ease: "easeOut" }}
            >
              <Card className="h-full border-border/60 bg-surface/40 backdrop-blur-sm hover:bg-surface/75 hover:border-border/80 transition-all duration-300 flex flex-col group">
                <CardHeader className="space-y-4 flex-1">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-border bg-background/50 group-hover:scale-105 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg font-bold group-hover:text-primary transition-colors">
                    {feature.title}
                  </CardTitle>
                  <CardContent className="p-0 text-sm leading-relaxed text-muted-foreground">
                    {feature.description}
                  </CardContent>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
