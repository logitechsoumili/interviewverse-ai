"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AuthFormField } from "@/components/auth/auth-form-field";
import { getApiErrorMessage } from "@/lib/api-error";
import { useAuth } from "@/hooks/use-auth";
import {
  registerSchema,
  type RegisterFormValues,
} from "@/features/auth/auth-schema";

export function RegisterForm() {
  const router = useRouter();
  const auth = useAuth();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      full_name: "",
      email: "",
      password: "",
      confirm_password: "",
    },
  });

  const registerMutation = useMutation({
    mutationFn: auth.register,
    onSuccess: () => {
      setServerError(null);
      toast.success("Account created. Please sign in.");
      router.replace("/login");
    },
    onError: (error) => {
      const message = getApiErrorMessage(error);

      if (message.toLowerCase().includes("email already exists")) {
        setError("email", {
          type: "server",
          message,
        });
      } else {
        setServerError(message);
      }

      toast.error(message);
    },
  });

  const onSubmit = handleSubmit(async (values) => {
    setServerError(null);
    await registerMutation.mutateAsync({
      email: values.email,
      full_name: values.full_name,
      password: values.password,
    });
  });

  return (
    <form className="space-y-4" onSubmit={onSubmit} noValidate>
      {serverError ? (
        <p
          className="rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
          role="alert"
        >
          {serverError}
        </p>
      ) : null}

      <AuthFormField
        id="full_name"
        label="Full Name"
        error={errors.full_name?.message}
      >
        <Input
          id="full_name"
          autoComplete="name"
          autoFocus
          placeholder="Your name"
          aria-invalid={Boolean(errors.full_name)}
          aria-describedby={
            errors.full_name?.message ? "full_name-error" : undefined
          }
          {...register("full_name")}
        />
      </AuthFormField>

      <AuthFormField
        id="email"
        label="Email"
        error={errors.email?.message}
      >
        <Input
          id="email"
          type="email"
          autoComplete="email"
          placeholder="you@example.com"
          aria-invalid={Boolean(errors.email)}
          aria-describedby={errors.email?.message ? "email-error" : undefined}
          {...register("email")}
        />
      </AuthFormField>

      <AuthFormField
        id="password"
        label="Password"
        error={errors.password?.message}
      >
        <Input
          id="password"
          type="password"
          autoComplete="new-password"
          placeholder="Create a password"
          aria-invalid={Boolean(errors.password)}
          aria-describedby={errors.password?.message ? "password-error" : undefined}
          {...register("password")}
        />
      </AuthFormField>

      <AuthFormField
        id="confirm_password"
        label="Confirm Password"
        error={errors.confirm_password?.message}
      >
        <Input
          id="confirm_password"
          type="password"
          autoComplete="new-password"
          placeholder="Repeat your password"
          aria-invalid={Boolean(errors.confirm_password)}
          aria-describedby={
            errors.confirm_password?.message
              ? "confirm_password-error"
              : undefined
          }
          {...register("confirm_password")}
        />
      </AuthFormField>

      <Button
        type="submit"
        className="w-full"
        disabled={registerMutation.isPending}
      >
        {registerMutation.isPending ? "Creating account..." : "Create account"}
      </Button>
    </form>
  );
}
