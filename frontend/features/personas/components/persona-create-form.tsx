"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { PersonaFormField } from "@/features/personas/components/persona-form-field";
import {
  personaCreateSchema,
  toPersonaCreateRequest,
  type PersonaCreateSchema,
} from "@/features/personas/schemas/persona-schema";
import { useCreatePersonaMutation } from "@/features/personas/hooks/use-create-persona";
import { getApiErrorMessage } from "@/lib/api-error";

export function PersonaCreateForm() {
  const router = useRouter();
  const createPersonaMutation = useCreatePersonaMutation();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<PersonaCreateSchema>({
    resolver: zodResolver(personaCreateSchema),
    defaultValues: {
      id: "",
      name: "",
      role: "",
      description: "",
      interview_style: "",
      supported_difficulty_levels: "",
      focus_areas: "",
      system_context: "",
    },
  });

  const onSubmit = handleSubmit(async (values) => {
    setServerError(null);

    try {
      await createPersonaMutation.mutateAsync(toPersonaCreateRequest(values));
      toast.success("Persona created successfully.");
      router.replace("/dashboard/personas");
    } catch (error) {
      const message = getApiErrorMessage(error);

      if (message.toLowerCase().includes("id") && message.toLowerCase().includes("exists")) {
        setError("id", {
          type: "server",
          message,
        });
      } else {
        setServerError(message);
      }

      toast.error(message);
    }
  });

  return (
    <form className="space-y-5" onSubmit={onSubmit} noValidate>
      {serverError ? (
        <div className="rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {serverError}
        </div>
      ) : null}

      <div className="grid gap-5 md:grid-cols-2">
        <PersonaFormField
          id="id"
          label="Persona ID"
          helperText="Use lowercase letters, numbers, underscores, or hyphens."
          error={errors.id?.message}
        >
          <Input
            id="id"
            autoComplete="off"
            placeholder="custom_interviewer"
            aria-invalid={Boolean(errors.id)}
            aria-describedby={errors.id?.message ? "id-error" : undefined}
            {...register("id")}
          />
        </PersonaFormField>

        <PersonaFormField
          id="name"
          label="Persona Name"
          error={errors.name?.message}
        >
          <Input
            id="name"
            autoComplete="off"
            placeholder="Jordan Blake"
            aria-invalid={Boolean(errors.name)}
            aria-describedby={errors.name?.message ? "name-error" : undefined}
            {...register("name")}
          />
        </PersonaFormField>

        <PersonaFormField
          id="role"
          label="Role"
          error={errors.role?.message}
        >
          <Input
            id="role"
            autoComplete="off"
            placeholder="Senior Product Manager"
            aria-invalid={Boolean(errors.role)}
            aria-describedby={errors.role?.message ? "role-error" : undefined}
            {...register("role")}
          />
        </PersonaFormField>

        <PersonaFormField
          id="interview_style"
          label="Interview Style"
          error={errors.interview_style?.message}
        >
          <Input
            id="interview_style"
            autoComplete="off"
            placeholder="Direct, structured, and thoughtful"
            aria-invalid={Boolean(errors.interview_style)}
            aria-describedby={
              errors.interview_style?.message ? "interview_style-error" : undefined
            }
            {...register("interview_style")}
          />
        </PersonaFormField>
      </div>

      <PersonaFormField
        id="description"
        label="Description"
        error={errors.description?.message}
      >
        <Textarea
          id="description"
          placeholder="Describe the interviewer persona in a sentence or two."
          aria-invalid={Boolean(errors.description)}
          aria-describedby={errors.description?.message ? "description-error" : undefined}
          {...register("description")}
        />
      </PersonaFormField>

      <div className="grid gap-5 md:grid-cols-2">
        <PersonaFormField
          id="supported_difficulty_levels"
          label="Difficulty Levels"
          helperText="Comma-separated. Example: junior, mid, senior"
          error={errors.supported_difficulty_levels?.message}
        >
          <Textarea
            id="supported_difficulty_levels"
            placeholder="junior, mid, senior"
            aria-invalid={Boolean(errors.supported_difficulty_levels)}
            aria-describedby={
              errors.supported_difficulty_levels?.message
                ? "supported_difficulty_levels-error"
                : undefined
            }
            {...register("supported_difficulty_levels")}
          />
        </PersonaFormField>

        <PersonaFormField
          id="focus_areas"
          label="Focus Areas"
          helperText="Comma-separated. Example: systems design, product thinking"
          error={errors.focus_areas?.message}
        >
          <Textarea
            id="focus_areas"
            placeholder="systems design, product thinking"
            aria-invalid={Boolean(errors.focus_areas)}
            aria-describedby={errors.focus_areas?.message ? "focus_areas-error" : undefined}
            {...register("focus_areas")}
          />
        </PersonaFormField>
      </div>

      <PersonaFormField
        id="system_context"
        label="System Context"
        helperText="Prompt context for the model. Required by the backend."
        error={errors.system_context?.message}
      >
        <Textarea
          id="system_context"
          placeholder="You are a calm and rigorous interviewer..."
          aria-invalid={Boolean(errors.system_context)}
          aria-describedby={errors.system_context?.message ? "system_context-error" : undefined}
          {...register("system_context")}
        />
      </PersonaFormField>

      <div className="flex flex-wrap items-center gap-3">
        <Button type="submit" disabled={createPersonaMutation.isPending}>
          {createPersonaMutation.isPending ? "Creating Persona..." : "Create Persona"}
        </Button>
        <Button type="button" variant="outline" onClick={() => router.push("/dashboard/personas")}>
          Cancel
        </Button>
      </div>
    </form>
  );
}
