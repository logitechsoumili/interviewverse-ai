import { z } from "zod";
import type {
  PersonaCreateFormValues,
  PersonaCreateRequest,
} from "@/features/personas/types";

const listField = z
  .string()
  .trim()
  .min(1, "At least one value is required.")
  .refine((value) => value.split(",").some((item) => item.trim().length > 0), {
    message: "At least one value is required.",
  });

export const personaCreateSchema = z.object({
  id: z
    .string()
    .trim()
    .min(3, "Persona ID must be at least 3 characters.")
    .max(64, "Persona ID must be 64 characters or fewer.")
    .regex(/^[a-zA-Z0-9_-]+$/, "Use letters, numbers, underscores, or hyphens."),
  name: z.string().trim().min(1, "Name is required."),
  role: z.string().trim().min(1, "Role is required."),
  description: z.string().trim().min(1, "Description is required."),
  interview_style: z.string().trim().min(1, "Interview style is required."),
  supported_difficulty_levels: listField,
  focus_areas: listField,
  system_context: z.string().trim().min(1, "System context is required."),
}) satisfies z.ZodType<PersonaCreateFormValues>;

export type PersonaCreateSchema = z.infer<typeof personaCreateSchema>;

function splitCsv(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function toPersonaCreateRequest(
  values: PersonaCreateSchema
): PersonaCreateRequest {
  return {
    id: values.id.trim(),
    name: values.name.trim(),
    role: values.role.trim(),
    description: values.description.trim(),
    interview_style: values.interview_style.trim(),
    supported_difficulty_levels: splitCsv(values.supported_difficulty_levels),
    focus_areas: splitCsv(values.focus_areas),
    system_context: values.system_context.trim(),
  };
}
