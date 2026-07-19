import { http } from "@/services/http";
import type {
  EvaluationApiResponse,
  ReportApiResponse,
} from "@/features/evaluations/types";

export async function generateEvaluation(interviewId: string): Promise<EvaluationApiResponse> {
  const { data } = await http.post<EvaluationApiResponse>(
    `/interviews/${interviewId}/evaluate`
  );
  return data;
}

export async function fetchEvaluation(interviewId: string): Promise<EvaluationApiResponse> {
  const { data } = await http.get<EvaluationApiResponse>(`/interviews/${interviewId}/evaluation`);
  return data;
}

export async function fetchReport(interviewId: string): Promise<ReportApiResponse> {
  const { data } = await http.get<ReportApiResponse>(`/interviews/${interviewId}/report`);
  return data;
}
