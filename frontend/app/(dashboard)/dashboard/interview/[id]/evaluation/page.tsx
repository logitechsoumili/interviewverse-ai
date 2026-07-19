import { InterviewEvaluationPlaceholder } from "@/features/interviews/components/interview-evaluation-placeholder";

type InterviewEvaluationRoutePageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function InterviewEvaluationRoutePage({
  params,
}: InterviewEvaluationRoutePageProps) {
  const { id } = await params;
  return <InterviewEvaluationPlaceholder interviewId={id} />;
}
