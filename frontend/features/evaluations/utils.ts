import axios from "axios";
import { getApiErrorMessage } from "@/lib/api-error";
import type { EvaluationApiResponse, ReportApiResponse } from "@/features/evaluations/types";

export function formatEvaluationTimestamp(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function getScoreLabel(score: number) {
  if (score >= 90) {
    return "Exceptional";
  }
  if (score >= 75) {
    return "Strong";
  }
  if (score >= 60) {
    return "Developing";
  }
  return "Needs focus";
}

export function getScoreTone(score: number) {
  if (score >= 90) {
    return "bg-emerald-500";
  }
  if (score >= 75) {
    return "bg-sky-500";
  }
  if (score >= 60) {
    return "bg-amber-500";
  }
  return "bg-rose-500";
}

export function buildEvaluationSummary(evaluation: EvaluationApiResponse) {
  const topStrengths = evaluation.summary.strengths.slice(0, 2).join(", ");
  const topWeaknesses = evaluation.summary.weaknesses.slice(0, 2).join(", ");

  return [
    `Overall score: ${evaluation.scores.overall_score}/100.`,
    topStrengths ? `Strengths: ${topStrengths}.` : "Strengths are not listed.",
    topWeaknesses ? `Areas for improvement: ${topWeaknesses}.` : "No improvement areas were listed.",
  ].join(" ");
}

export function getEvaluationApiErrorMessage(error: unknown, missingMessage = "Evaluation not found.") {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return "Network error. Please check your connection and try again.";
    }

    if (error.response.status === 401) {
      return "Your session expired. Please sign in again.";
    }

    if (error.response.status === 404) {
      return missingMessage;
    }
  }

  return getApiErrorMessage(error);
}

export function getReportApiErrorMessage(error: unknown, missingMessage = "Report not found.") {
  return getEvaluationApiErrorMessage(error, missingMessage);
}

export function isEvaluationNotFoundError(error: unknown) {
  return axios.isAxiosError(error) && error.response?.status === 404;
}

export function toBulletLines(items: string[]) {
  return items.filter(Boolean);
}

export function extractTranscriptSummary(report: ReportApiResponse) {
  return report.executive_summary.content;
}

export function extractEvaluationSummary(report: ReportApiResponse) {
  return report.performance_overview.content;
}
