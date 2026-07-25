import { InterviewPage } from "@/features/interviews/components/interview-page";

export async function generateStaticParams() {
  return [{ id: "placeholder" }];
}

export default function InterviewRoutePage() {
  return <InterviewPage />;
}
