import { ReportPage } from "@/features/evaluations/components/report-page";

type InterviewReportRoutePageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function InterviewReportRoutePage({
  params,
}: InterviewReportRoutePageProps) {
  const { id } = await params;
  return <ReportPage interviewId={id} />;
}
