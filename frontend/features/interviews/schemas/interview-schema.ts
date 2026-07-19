import { z } from "zod";
import type {
  InterviewComposerValues,
  InterviewMessage,
  InterviewSession,
} from "@/features/interviews/types";

const timestampSchema = z.string().datetime({ offset: true });

const interviewMessageSchema = z.object({
  id: z.string().min(1),
  role: z.enum(["user", "assistant"]),
  content: z.string().min(1),
  timestamp: timestampSchema,
  status: z.enum(["sending", "sent", "error"]),
  errorMessage: z.string().nullable().optional(),
}) satisfies z.ZodType<InterviewMessage>;

export const interviewComposerSchema = z.object({
  message: z.string().trim().min(1, "Message cannot be empty."),
}) satisfies z.ZodType<InterviewComposerValues>;

export const interviewSessionSchema = z.object({
  interviewId: z.string().min(1),
  personaId: z.string().min(1),
  personaName: z.string().min(1),
  personaRole: z.string().min(1),
  title: z.string().min(1),
  status: z.enum(["starting", "in_progress", "completed"]),
  startedAt: timestampSchema,
  completedAt: timestampSchema.nullable(),
  topics: z.array(z.string()),
  difficulty: z.string().min(1),
  messages: z.array(interviewMessageSchema),
  latestError: z.string().nullable(),
}) satisfies z.ZodType<InterviewSession>;

export type InterviewComposerSchema = z.infer<typeof interviewComposerSchema>;

export function isInterviewMessage(value: unknown): value is InterviewMessage {
  return interviewMessageSchema.safeParse(value).success;
}

export function isInterviewSession(value: unknown): value is InterviewSession {
  return interviewSessionSchema.safeParse(value).success;
}
