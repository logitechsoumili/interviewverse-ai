import { ReportPage } from "@/features/evaluations/components/report-page";

type InterviewReportRoutePageProps = {
  params: Promise<{
    id: string;
  }>;
};

export async function generateStaticParams() {
  return [{ id: "placeholder" }];
}

export default async function InterviewReportRoutePage({
  params,
}: InterviewReportRoutePageProps) {
  const { id } = await params;
  return <ReportPage interviewId={id} />;
}
