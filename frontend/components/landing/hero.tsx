"use client";

import Link from "next/link";
import { motion, type Variants } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Hero() {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.05,
      },
    },
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.45, ease: "easeOut" },
    },
  };

  return (
    <section className="relative flex min-h-[95vh] items-center justify-center overflow-hidden bg-background px-6 pt-32 pb-20">
      {/* Background gradients */}
      <div className="pointer-events-none absolute inset-0 z-0">
        <div className="absolute left-[15%] top-[10%] h-96 w-96 rounded-full bg-primary/10 blur-[8rem]" />
        <div className="absolute right-[15%] bottom-[10%] h-[30rem] w-[30rem] rounded-full bg-secondary/10 blur-[9rem]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#0f172a_1px,transparent_1px),linear-gradient(to_bottom,#0f172a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-30" />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 w-full max-w-4xl text-center"
      >
        {/* Badge */}
        <motion.div variants={itemVariants} className="mb-6 inline-flex">
          <Badge variant="default" className="gap-1.5 px-3.5 py-1 text-[10px] font-semibold uppercase tracking-[0.25em] bg-primary/10 border-primary/20 text-primary">
            <span className="flex h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
            Autonomous Platform v2.0
          </Badge>
        </motion.div>

        {/* Title */}
        <motion.h1
          variants={itemVariants}
          className="font-display text-4xl font-extrabold tracking-tight text-foreground sm:text-6xl lg:text-7xl"
        >
          Master Every Interview with{" "}
          <span className="block mt-2 bg-gradient-to-r from-primary via-primary-foreground to-secondary bg-clip-text text-transparent pb-1">
            Autonomous AI
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={itemVariants}
          className="mx-auto mt-6 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg sm:leading-8"
        >
          Practice mock interviews in real-time with hyper-realistic AI personas. Get instant scorecard evaluation, transcript breakdown, and actionable feedback.
        </motion.p>

        {/* Buttons */}
        <motion.div
          variants={itemVariants}
          className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
        >
          <Button size="lg" className="w-full sm:w-auto" asChild>
            <Link href="/register">
              Start Practicing Free
            </Link>
          </Button>
          <Button size="lg" variant="outline" className="w-full sm:w-auto border-border/80 bg-surface/40 backdrop-blur-sm" asChild>
            <Link href="/login">
              Sign In to Workspace
            </Link>
          </Button>
        </motion.div>

        {/* Floating shapes */}
        <div className="absolute top-1/2 left-[-8%] -translate-y-1/2 select-none pointer-events-none opacity-20">
          <motion.div
            animate={{ y: [0, -15, 0], rotate: [0, 10, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
            className="h-12 w-12 rounded-2xl border border-primary/30 bg-primary/5"
          />
        </div>
        <div className="absolute top-1/3 right-[-8%] select-none pointer-events-none opacity-20">
          <motion.div
            animate={{ y: [0, 15, 0], rotate: [0, -10, 0] }}
            transition={{ duration: 7, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            className="h-14 w-14 rounded-full border border-secondary/30 bg-secondary/5"
          />
        </div>
      </motion.div>
    </section>
  );
}
