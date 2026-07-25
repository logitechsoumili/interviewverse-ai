export const queryKeys = {
  currentUser: ["auth", "current-user"] as const,
  interviews: ["dashboard", "interviews"] as const,
  interviewSessions: {
    detail: (id: string) => ["interviews", "session", id] as const,
  },
  evaluations: {
    detail: (id: string) => ["evaluations", "detail", id] as const,
  },
  reports: {
    detail: (id: string) => ["reports", "detail", id] as const,
  },
  personas: {
    all: ["personas"] as const,
    list: ["personas", "list"] as const,
    detail: (id: string) => ["personas", "detail", id] as const,
  },
};
