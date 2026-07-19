import type {
  PersonaDetail,
  PersonaDisplayPersona,
  PersonaListItem,
  PersonaSource,
} from "@/features/personas/types";

type PersonaPreset = Omit<
  PersonaDisplayPersona,
  "id" | "name" | "role" | "source"
>;

const BUILTIN_PERSONA_PRESETS: Record<string, PersonaPreset> = {
  hr_interviewer: {
    shortDescription:
      "A friendly, culture-focused HR representative who evaluates soft skills and communication.",
    description:
      "A friendly, culture-focused HR representative who evaluates soft skills and communication.",
    interviewStyle: "Warm, conversational, and empathetic",
    experienceLevel: "All levels",
    company: "InterviewVerse AI",
    industry: "People Operations",
    difficulty: "junior, mid, senior",
    expertise: ["Behavioral", "Culture Fit", "Communication", "Conflict Resolution"],
    tags: ["behavioral", "culture fit", "communication"],
  },
  swe_interviewer: {
    shortDescription:
      "A technical interviewer focused on software engineering fundamentals and problem solving.",
    description:
      "A technical interviewer focused on software engineering fundamentals and problem solving.",
    interviewStyle: "Analytical, structured, and technically rigorous",
    experienceLevel: "All levels",
    company: "InterviewVerse AI",
    industry: "Software Engineering",
    difficulty: "junior, mid, senior",
    expertise: ["Data Structures", "Algorithms", "Clean Code", "Design Patterns"],
    tags: ["engineering", "algorithms", "architecture"],
  },
  mle_interviewer: {
    shortDescription:
      "A machine learning specialist focused on statistics, model training, and productionization.",
    description:
      "A machine learning specialist focused on statistics, model training, and productionization.",
    interviewStyle: "Mathematically precise and engineering-driven",
    experienceLevel: "Mid to Senior",
    company: "InterviewVerse AI",
    industry: "Machine Learning",
    difficulty: "mid, senior",
    expertise: ["Statistics", "ML Algorithms", "Feature Engineering", "Model Deployment"],
    tags: ["ml", "statistics", "deployment"],
  },
  professor_interviewer: {
    shortDescription:
      "An academic interviewer who focuses on theory, first principles, and formal correctness.",
    description:
      "An academic interviewer who focuses on theory, first principles, and formal correctness.",
    interviewStyle: "Intellectual, theoretical, and conceptually demanding",
    experienceLevel: "All levels",
    company: "InterviewVerse AI",
    industry: "Computer Science",
    difficulty: "junior, mid, senior",
    expertise: ["Theoretical CS", "Math Foundations", "Complexity Theory", "Formal Proofs"],
    tags: ["theory", "math", "formal reasoning"],
  },
  investor_interviewer: {
    shortDescription:
      "A venture partner persona focused on product strategy, trade-offs, and scaling decisions.",
    description:
      "A venture partner persona focused on product strategy, trade-offs, and scaling decisions.",
    interviewStyle: "Strategic, pragmatic, and business-focused",
    experienceLevel: "Senior",
    company: "InterviewVerse AI",
    industry: "Startups",
    difficulty: "senior",
    expertise: ["Business Viability", "Technical Debt", "Product-Market Fit", "Scaling"],
    tags: ["strategy", "growth", "architecture"],
  },
};

const BUILTIN_PERSONA_IDS = new Set(Object.keys(BUILTIN_PERSONA_PRESETS));

function getFallbackPreset(persona: PersonaListItem): PersonaPreset {
  const shortDescription = `${persona.name} is a custom persona for ${persona.role.toLowerCase()}.`;
  return {
    shortDescription,
    description: shortDescription,
    interviewStyle: "Custom",
    experienceLevel: "Custom",
    company: "Your Workspace",
    industry: "Custom",
    difficulty: "custom",
    expertise: [persona.role],
    tags: [persona.role],
  };
}

export function getPersonaSource(id: string): PersonaSource {
  return BUILTIN_PERSONA_IDS.has(id) ? "built-in" : "custom";
}

export function summarizePersonaDescription(value: string) {
  const trimmed = value.trim();
  if (trimmed.length <= 120) {
    return trimmed;
  }

  return `${trimmed.slice(0, 117).trimEnd()}...`;
}

export function formatPersonaDifficulty(value: string[]) {
  return value.length > 0 ? value.join(", ") : "Custom";
}

export function enrichPersona(
  persona: PersonaListItem,
  cachedDetail?: PersonaDetail | null
): PersonaDisplayPersona {
  const source = getPersonaSource(persona.id);

  if (cachedDetail) {
    return {
      id: cachedDetail.id,
      name: cachedDetail.name,
      role: cachedDetail.role,
      source,
      shortDescription: summarizePersonaDescription(cachedDetail.description),
      description: cachedDetail.description,
      interviewStyle: cachedDetail.interview_style,
      experienceLevel: formatPersonaDifficulty(cachedDetail.supported_difficulty_levels),
      company: source === "built-in" ? "InterviewVerse AI" : "Custom Workspace",
      industry: source === "built-in" ? "Interviewing" : "Custom",
      difficulty: formatPersonaDifficulty(cachedDetail.supported_difficulty_levels),
      expertise: cachedDetail.focus_areas,
      tags: cachedDetail.focus_areas,
      systemContext: cachedDetail.system_context,
    };
  }

  const preset = BUILTIN_PERSONA_PRESETS[persona.id] ?? getFallbackPreset(persona);

  return {
    id: persona.id,
    name: persona.name,
    role: persona.role,
    source,
    ...preset,
  };
}

export function getPersonaRoleOptions(personas: PersonaListItem[]) {
  return Array.from(new Set(personas.map((persona) => persona.role))).sort((a, b) =>
    a.localeCompare(b)
  );
}
