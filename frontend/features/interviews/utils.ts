import axios from "axios";
import { getApiErrorMessage } from "@/lib/api-error";
import { interviewSessionSchema } from "@/features/interviews/schemas/interview-schema";
import type {
  InterviewMessage,
  InterviewSession,
  InterviewStartContext,
  InterviewApiStartResponse,
} from "@/features/interviews/types";

const STORAGE_PREFIX = "interviewverse:interview-session:";

function getStorageKey(interviewId: string) {
  return `${STORAGE_PREFIX}${interviewId}`;
}

function nowIso() {
  return new Date().toISOString();
}

export function createId() {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }

  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function formatInterviewTimestamp(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}

export function formatElapsedTime(startedAt: string, completedAt?: string | null) {
  const start = new Date(startedAt).getTime();
  const end = completedAt ? new Date(completedAt).getTime() : Date.now();
  const elapsedSeconds = Math.max(0, Math.floor((end - start) / 1000));
  const hours = Math.floor(elapsedSeconds / 3600);
  const minutes = Math.floor((elapsedSeconds % 3600) / 60);
  const seconds = elapsedSeconds % 60;

  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
  }

  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

export function formatInterviewStatus(status: InterviewSession["status"]) {
  switch (status) {
    case "starting":
      return "Starting";
    case "in_progress":
      return "In progress";
    case "completed":
      return "Completed";
  }
}

export function getInterviewStatusTone(status: InterviewSession["status"]) {
  switch (status) {
    case "starting":
      return "outline" as const;
    case "in_progress":
      return "default" as const;
    case "completed":
      return "secondary" as const;
  }
}

export function getInterviewApiErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return "Network error. Please check your connection and try again.";
    }

    if (error.response.status === 401) {
      return "Your session expired. Please sign in again.";
    }

    return getApiErrorMessage(error);
  }

  return getApiErrorMessage(error);
}

export function createInterviewSession(
  context: InterviewStartContext,
  response: InterviewApiStartResponse,
  startedAt = nowIso()
): InterviewSession {
  return {
    interviewId: response.interview_id,
    personaId: context.personaId,
    personaName: context.personaName,
    personaRole: context.personaRole,
    title: context.title ?? "Interview Session",
    status: "in_progress",
    startedAt,
    completedAt: null,
    topics: context.topics ?? ["Python"],
    difficulty: context.difficulty ?? "mid",
    messages: [
      {
        id: createId(),
        role: "assistant",
        content: response.question,
        timestamp: nowIso(),
        status: "sent",
      },
    ],
    latestError: null,
  };
}

export function createUserMessage(
  content: string,
  timestamp = nowIso(),
  id = createId()
): InterviewMessage {
  return {
    id,
    role: "user",
    content,
    timestamp,
    status: "sending",
  };
}

export function createAssistantMessage(
  content: string,
  timestamp = nowIso()
): InterviewMessage {
  return {
    id: createId(),
    role: "assistant",
    content,
    timestamp,
    status: "sent",
  };
}

export function loadInterviewSession(interviewId: string): InterviewSession | null {
  if (typeof window === "undefined") {
    return null;
  }

  const rawValue = window.localStorage.getItem(getStorageKey(interviewId));
  if (!rawValue) {
    return null;
  }

  try {
    const parsed = JSON.parse(rawValue) as unknown;
    const result = interviewSessionSchema.safeParse(parsed);
    return result.success ? result.data : null;
  } catch {
    return null;
  }
}

export function saveInterviewSession(session: InterviewSession) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(getStorageKey(session.interviewId), JSON.stringify(session));
}

export function getPathnameInterviewId(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  const pathname = window.location.pathname;
  const segments = pathname.split("/");
  const idx = segments.indexOf("interview");
  if (idx !== -1 && segments[idx + 1] && segments[idx + 1] !== "placeholder") {
    return segments[idx + 1];
  }
  return null;
}
