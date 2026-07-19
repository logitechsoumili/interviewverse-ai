export type EvaluationScore = {
  overall_score: number;
  communication_score: number;
  technical_score: number;
  confidence_score: number;
};

export type EvaluationSummary = {
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  learning_roadmap: string[];
};

export type EvaluationApiResponse = {
  scores: EvaluationScore;
  summary: EvaluationSummary;
  evaluated_at: string;
  persona_id: string;
};

export type ReportSection = {
  title: string;
  content: string;
};

export type ReportApiResponse = {
  report_id: string;
  interview_id: string;
  persona_id: string;
  generated_at: string;
  executive_summary: ReportSection;
  performance_overview: ReportSection;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  learning_roadmap: string[];
  markdown_report: string;
};
