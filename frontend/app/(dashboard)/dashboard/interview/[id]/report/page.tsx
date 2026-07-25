import { ReportPage } from "@/features/evaluations/components/report-page";

export async function generateStaticParams() {
  return [{ id: "placeholder" }];
}

export default function InterviewReportRoutePage() {
  return <ReportPage />;
}
