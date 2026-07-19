export type InterviewApiStartRequest = {
  persona_id: string;
  topics?: string[];
  difficulty?: string;
};

export type InterviewApiStartResponse = {
  interview_id: string;
  question: string;
  question_number: number;
};

export type InterviewApiMessageRequest = {
  message: string;
};

export type InterviewApiMessageResponse = {
  question: string;
  question_number: number;
};

export type InterviewApiCompleteResponse = {
  status: string;
};

export type InterviewStatus = "starting" | "in_progress" | "completed";

export type InterviewMessageRole = "user" | "assistant";

export type InterviewMessageStatus = "sending" | "sent" | "error";

export type InterviewMessage = {
  id: string;
  role: InterviewMessageRole;
  content: string;
  timestamp: string;
  status: InterviewMessageStatus;
  errorMessage?: string | null;
};

export type InterviewSession = {
  interviewId: string;
  personaId: string;
  personaName: string;
  personaRole: string;
  title: string;
  status: InterviewStatus;
  startedAt: string;
  completedAt: string | null;
  topics: string[];
  difficulty: string;
  messages: InterviewMessage[];
  latestError: string | null;
};

export type InterviewStartContext = {
  personaId: string;
  personaName: string;
  personaRole: string;
  title?: string;
  topics?: string[];
  difficulty?: string;
};

export type InterviewComposerValues = {
  message: string;
};
