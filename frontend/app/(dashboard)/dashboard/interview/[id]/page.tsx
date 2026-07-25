import { InterviewPage } from "@/features/interviews/components/interview-page";

type InterviewRoutePageProps = {
  params: Promise<{
    id: string;
  }>;
};

export async function generateStaticParams() {
  return [{ id: "placeholder" }];
}

export default async function InterviewRoutePage({ params }: InterviewRoutePageProps) {
  const { id } = await params;
  return <InterviewPage interviewId={id} />;
}
