export interface InterviewListItem {
  id: string;
  persona: string;
  status: string;
  created_at: string;
  completed_at: string | null;
}

export interface DashboardStats {
  total: number;
  completed: number;
  pending: number;
}
