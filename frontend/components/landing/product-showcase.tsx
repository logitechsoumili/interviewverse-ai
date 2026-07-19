"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

const TABS = [
  { id: "dashboard", label: "Dashboard" },
  { id: "personas", label: "Personas" },
  { id: "chat", label: "Interview Chat" },
  { id: "evaluation", label: "Evaluation" },
  { id: "report", label: "Feedback Report" },
];

export function ProductShowcase() {
  const [activeTab, setActiveTab] = useState("dashboard");

  return (
    <section className="relative bg-background py-24 px-6 overflow-hidden border-t border-border/30">
      <div className="pointer-events-none absolute right-[-10%] top-[20%] h-[32rem] w-[32rem] rounded-full bg-secondary/5 blur-[8rem]" />
      <div className="pointer-events-none absolute left-[-10%] bottom-[20%] h-[32rem] w-[32rem] rounded-full bg-primary/5 blur-[8rem]" />

      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="text-[10px] font-semibold uppercase tracking-[0.25em] text-primary">
            Workspace Preview
          </span>
          <h2 className="mt-3 font-display text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
            Explore the Interface
          </h2>
          <p className="mt-4 text-sm sm:text-base text-muted-foreground leading-relaxed">
            Gain a visual preview of the InterviewVerse application. Click the tabs below to switch views.
          </p>
        </div>

        {/* Switcher Tabs */}
        <div className="flex flex-wrap justify-center gap-2 mb-10">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={cn(
                "rounded-xl px-5 py-2.5 text-sm font-medium transition-all duration-300 border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40",
                activeTab === tab.id
                  ? "bg-primary/10 border-primary text-primary shadow-sm"
                  : "bg-surface/50 border-border/60 text-muted-foreground hover:text-foreground hover:bg-surface/90"
              )}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Browser Mockup Window */}
        <div className="mx-auto max-w-5xl rounded-2xl border border-border/75 bg-surface/40 p-1.5 backdrop-blur-xl shadow-2xl shadow-black/40">
          <div className="rounded-xl border border-border bg-background overflow-hidden min-h-[480px] flex flex-col md:flex-row text-xs">
            {/* Sidebar Mock */}
            <aside className="w-full md:w-56 border-b md:border-b-0 md:border-r border-border bg-surface/50 p-4 space-y-4 shrink-0 flex flex-row md:flex-col justify-between md:justify-start gap-4">
              <div className="space-y-4 w-full">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-secondary">
                    InterviewVerse AI
                  </p>
                  <p className="font-semibold text-foreground mt-0.5">Workspace</p>
                </div>
                <nav className="hidden md:block space-y-1">
                  <div className={cn("px-3 py-2.5 rounded-lg font-medium transition-colors", activeTab === "dashboard" ? "bg-primary/15 text-primary" : "text-muted-foreground")}>Dashboard</div>
                  <div className={cn("px-3 py-2.5 rounded-lg font-medium transition-colors", activeTab === "personas" ? "bg-primary/15 text-primary" : "text-muted-foreground")}>Personas</div>
                  <div className={cn("px-3 py-2.5 rounded-lg font-medium transition-colors", activeTab === "chat" ? "bg-primary/15 text-primary" : "text-muted-foreground")}>Interview Chat</div>
                  <div className={cn("px-3 py-2.5 rounded-lg font-medium transition-colors", activeTab === "evaluation" || activeTab === "report" ? "bg-primary/15 text-primary" : "text-muted-foreground")}>History</div>
                </nav>
              </div>
              <div className="shrink-0 flex items-center gap-2">
                <div className="h-7 w-7 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center font-bold text-primary">U</div>
                <span className="font-medium text-foreground hidden md:inline">User Profile</span>
              </div>
            </aside>

            {/* Content Mock */}
            <main className="flex-1 p-6 relative overflow-hidden bg-background/50 flex flex-col justify-center min-h-[360px]">
              <AnimatePresence mode="wait">
                {activeTab === "dashboard" && (
                  <motion.div
                    key="dashboard-mock"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.25 }}
                    className="space-y-6 w-full"
                  >
                    <div className="flex justify-between items-center">
                      <h3 className="text-sm font-bold text-foreground">Dashboard Analytics</h3>
                      <span className="rounded-full bg-emerald-500/10 text-emerald-400 px-2 py-0.5 font-medium border border-emerald-500/20 text-[10px]">Connected</span>
                    </div>
                    {/* Stats */}
                    <div className="grid grid-cols-3 gap-4">
                      <div className="rounded-xl border border-border bg-surface p-4 text-center">
                        <p className="text-[10px] text-muted-foreground">Sessions</p>
                        <p className="text-lg font-bold text-foreground mt-1">12</p>
                      </div>
                      <div className="rounded-xl border border-border bg-surface p-4 text-center">
                        <p className="text-[10px] text-muted-foreground">Avg Score</p>
                        <p className="text-lg font-bold text-primary mt-1">84%</p>
                      </div>
                      <div className="rounded-xl border border-border bg-surface p-4 text-center">
                        <p className="text-[10px] text-muted-foreground">Personas</p>
                        <p className="text-lg font-bold text-secondary mt-1">3</p>
                      </div>
                    </div>
                    {/* Recent Sessions */}
                    <div className="rounded-xl border border-border bg-surface overflow-hidden">
                      <div className="border-b border-border bg-muted/30 px-4 py-2 font-semibold">Recent Evaluations</div>
                      <div className="divide-y divide-border">
                        <div className="px-4 py-3 flex justify-between items-center">
                          <span>Senior Frontend Lead</span>
                          <span className="font-bold text-emerald-400">88%</span>
                        </div>
                        <div className="px-4 py-3 flex justify-between items-center">
                          <span>Algorithm Coach</span>
                          <span className="font-bold text-amber-400">72%</span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}

                {activeTab === "personas" && (
                  <motion.div
                    key="personas-mock"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.25 }}
                    className="space-y-4 w-full"
                  >
                    <h3 className="text-sm font-bold text-foreground">Available Personas</h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                      <div className="rounded-xl border border-border bg-surface p-4 space-y-2 hover:border-primary/40 transition-colors">
                        <div className="flex justify-between items-center">
                          <span className="font-bold text-foreground">Sarah (Tech Lead)</span>
                          <span className="rounded bg-primary/10 border border-primary/20 text-primary px-1.5 py-0.5 text-[9px]">Hard</span>
                        </div>
                        <p className="text-muted-foreground leading-normal">Deep technical probes, core logic, architecture audits, and JS details.</p>
                      </div>
                      <div className="rounded-xl border border-border bg-surface p-4 space-y-2 hover:border-secondary/40 transition-colors">
                        <div className="flex justify-between items-center">
                          <span className="font-bold text-foreground">Marcus (Manager)</span>
                          <span className="rounded bg-secondary/10 border border-secondary/20 text-secondary px-1.5 py-0.5 text-[9px]">Medium</span>
                        </div>
                        <p className="text-muted-foreground leading-normal">Behavioral metrics, conflicts resolution, scaling, and leadership.</p>
                      </div>
                    </div>
                  </motion.div>
                )}

                {activeTab === "chat" && (
                  <motion.div
                    key="chat-mock"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.25 }}
                    className="space-y-4 w-full flex flex-col h-[320px]"
                  >
                    <div className="border-b border-border pb-2 flex justify-between items-center shrink-0">
                      <span className="font-bold text-foreground">Interview Session with Sarah</span>
                      <span className="flex h-2 w-2 rounded-full bg-rose-500 animate-pulse" />
                    </div>
                    {/* Chat Messages */}
                    <div className="flex-1 space-y-4 overflow-y-auto py-2">
                      <div className="flex items-start gap-2.5 max-w-[85%]">
                        <div className="h-6 w-6 rounded-full bg-primary/20 flex items-center justify-center font-bold text-primary text-[10px]">S</div>
                        <div className="rounded-2xl border border-border bg-surface p-3 leading-normal text-muted-foreground">
                          Can you explain how the microtask queue operates relative to the event loop macrotasks in Node.js?
                        </div>
                      </div>
                      <div className="flex items-start gap-2.5 max-w-[85%] ml-auto flex-row-reverse">
                        <div className="h-6 w-6 rounded-full bg-secondary/20 flex items-center justify-center font-bold text-secondary text-[10px]">U</div>
                        <div className="rounded-2xl border border-primary/20 bg-primary/5 p-3 leading-normal text-foreground">
                          Microtasks (like Promise callbacks and process.nextTick) resolve immediately after the current operation finishes, before yielding control back to the event loop phase transitions.
                        </div>
                      </div>
                    </div>
                    <div className="shrink-0 flex items-center gap-2 pt-2 border-t border-border">
                      <span className="flex h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
                      <span className="text-[10px] text-muted-foreground font-semibold">Sarah is evaluating your response...</span>
                    </div>
                  </motion.div>
                )}

                {activeTab === "evaluation" && (
                  <motion.div
                    key="evaluation-mock"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.25 }}
                    className="space-y-4 w-full"
                  >
                    <h3 className="text-sm font-bold text-foreground">Instant Evaluation</h3>
                    <div className="flex items-center gap-6">
                      <div className="h-24 w-24 rounded-full border-4 border-primary/30 border-t-primary flex items-center justify-center shrink-0">
                        <span className="text-2xl font-black text-foreground">88%</span>
                      </div>
                      <div className="space-y-2 flex-1">
                        <div className="space-y-1">
                          <div className="flex justify-between font-semibold">
                            <span>Technical Competence</span>
                            <span>90/100</span>
                          </div>
                          <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                            <div className="h-full bg-primary rounded-full" style={{ width: "90%" }} />
                          </div>
                        </div>
                        <div className="space-y-1">
                          <div className="flex justify-between font-semibold">
                            <span>Communication Clarity</span>
                            <span>85/100</span>
                          </div>
                          <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                            <div className="h-full bg-secondary rounded-full" style={{ width: "85%" }} />
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}

                {activeTab === "report" && (
                  <motion.div
                    key="report-mock"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.25 }}
                    className="space-y-4 w-full"
                  >
                    <h3 className="text-sm font-bold text-foreground">Feedback Report</h3>
                    <div className="rounded-xl border border-border bg-surface p-4 space-y-3 leading-normal">
                      <div>
                        <h4 className="font-bold text-primary mb-1">Summary of Strengths</h4>
                        <p className="text-muted-foreground">The candidate explained event loops, microtask queues, and process.nextTick with high technical accuracy and structural clarity.</p>
                      </div>
                      <div>
                        <h4 className="font-bold text-secondary mb-1">Key Advice</h4>
                        <p className="text-muted-foreground">Practice describing heap memory allocation paradigms under event load spikes for next level responses.</p>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </main>
          </div>
        </div>
      </div>
    </section>
  );
}
