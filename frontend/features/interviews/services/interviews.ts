import { http } from "@/services/http";
import type {
  InterviewApiCompleteResponse,
  InterviewApiMessageRequest,
  InterviewApiMessageResponse,
  InterviewApiStartRequest,
  InterviewApiStartResponse,
} from "@/features/interviews/types";

export async function startInterview(
  payload: InterviewApiStartRequest
): Promise<InterviewApiStartResponse> {
  const { data } = await http.post<InterviewApiStartResponse>("/interviews/start", payload);
  return data;
}

export async function sendInterviewMessage(
  interviewId: string,
  payload: InterviewApiMessageRequest
): Promise<InterviewApiMessageResponse> {
  const { data } = await http.post<InterviewApiMessageResponse>(
    `/interviews/${interviewId}/message`,
    payload
  );
  return data;
}

export async function completeInterview(
  interviewId: string
): Promise<InterviewApiCompleteResponse> {
  const { data } = await http.post<InterviewApiCompleteResponse>(
    `/interviews/${interviewId}/complete`
  );
  return data;
}
