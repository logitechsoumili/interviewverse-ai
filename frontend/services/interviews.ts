import { http } from "@/services/http";
import type { InterviewListItem } from "@/types/dashboard";

export async function fetchInterviews(): Promise<InterviewListItem[]> {
  const { data } = await http.get<InterviewListItem[]>("/interviews");
  return data;
}
