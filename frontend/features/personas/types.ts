export type PersonaListItem = {
  id: string;
  name: string;
  role: string;
};

export type PersonaDetail = {
  id: string;
  name: string;
  role: string;
  description: string;
  interview_style: string;
  supported_difficulty_levels: string[];
  focus_areas: string[];
  system_context: string;
};

export type PersonaCreateRequest = PersonaDetail;

export type PersonaSource = "built-in" | "custom";

export type PersonaDisplayPersona = {
  id: string;
  name: string;
  role: string;
  source: PersonaSource;
  shortDescription: string;
  description: string;
  interviewStyle: string;
  experienceLevel: string;
  company: string;
  industry: string;
  difficulty: string;
  expertise: string[];
  tags: string[];
  systemContext?: string;
};

export type PersonaCreateFormValues = {
  id: string;
  name: string;
  role: string;
  description: string;
  interview_style: string;
  supported_difficulty_levels: string;
  focus_areas: string;
  system_context: string;
};
