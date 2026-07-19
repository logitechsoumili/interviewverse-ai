import type { DashboardStats, InterviewListItem } from "@/features/dashboard/types";

const DEFAULT_PERSONA_NAMES: Record<string, string> = {
  hr_interviewer: "Sarah Jenkins",
  swe_interviewer: "Alex Rivera",
  mle_interviewer: "Dr. Elena Rostova",
  professor_interviewer: "Prof. Arthur Pendelton",
  investor_interviewer: "Marcus Vance",
};

function titleCase(value: string) {
  return value
    .split(/[_-]/g)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function formatPersonaName(personaId: string) {
  if (DEFAULT_PERSONA_NAMES[personaId]) {
    return DEFAULT_PERSONA_NAMES[personaId];
  }

  if (/^[0-9a-f-]{8,}$/i.test(personaId)) {
    return "Custom Persona";
  }

  return titleCase(personaId);
}

export function formatInterviewDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(value));
}

export function getInterviewStatusLabel(status: string) {
  switch (status) {
    case "completed":
      return "Completed";
    case "in_progress":
      return "In Progress";
    case "starting":
      return "Starting";
    default:
      return titleCase(status);
  }
}

export function getInterviewStatusTone(status: string) {
  switch (status) {
    case "completed":
      return "bg-emerald-500/15 text-emerald-300 border-emerald-500/20";
    case "in_progress":
      return "bg-primary/15 text-primary border-primary/20";
    case "starting":
      return "bg-secondary/15 text-secondary border-secondary/20";
    default:
      return "bg-muted/40 text-muted-foreground border-border";
  }
}

export function getInterviewStats(interviews: InterviewListItem[]): DashboardStats {
  const total = interviews.length;
  const completed = interviews.filter((item) => item.status === "completed").length;
  const pending = interviews.filter((item) => item.status !== "completed").length;

  return { total, completed, pending };
}
