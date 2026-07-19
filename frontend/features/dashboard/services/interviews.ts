import { http } from "@/services/http";
import type { InterviewListItem } from "@/features/dashboard/types";

export async function fetchInterviews(): Promise<InterviewListItem[]> {
  const { data } = await http.get<InterviewListItem[]>("/interviews");
  return data;
}
