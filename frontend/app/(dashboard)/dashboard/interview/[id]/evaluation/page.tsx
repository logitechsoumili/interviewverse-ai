import { EvaluationPage } from "@/features/evaluations/components/evaluation-page";

type InterviewEvaluationRoutePageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function InterviewEvaluationRoutePage({
  params,
}: InterviewEvaluationRoutePageProps) {
  const { id } = await params;
  return <EvaluationPage interviewId={id} />;
}
