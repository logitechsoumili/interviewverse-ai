import { EvaluationPage } from "@/features/evaluations/components/evaluation-page";

export async function generateStaticParams() {
  return [{ id: "placeholder" }];
}

export default function InterviewEvaluationRoutePage() {
  return <EvaluationPage />;
}
