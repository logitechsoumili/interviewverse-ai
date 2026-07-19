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
import { loginSchema, type LoginFormValues } from "@/features/auth/auth-schema";

export function LoginForm() {
  const router = useRouter();
  const auth = useAuth();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const loginMutation = useMutation({
    mutationFn: auth.login,
    onSuccess: () => {
      setServerError(null);
      router.replace("/dashboard");
    },
    onError: (error) => {
      const message = getApiErrorMessage(error);

      if (message.toLowerCase().includes("incorrect email or password")) {
        setError("password", {
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
    await loginMutation.mutateAsync(values);
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
        id="email"
        label="Email"
        error={errors.email?.message}
      >
        <Input
          id="email"
          type="email"
          autoComplete="email"
          autoFocus
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
          autoComplete="current-password"
          placeholder="Enter your password"
          aria-invalid={Boolean(errors.password)}
          aria-describedby={errors.password?.message ? "password-error" : undefined}
          {...register("password")}
        />
      </AuthFormField>

      <Button type="submit" className="w-full" disabled={loginMutation.isPending}>
        {loginMutation.isPending ? "Signing in..." : "Sign in"}
      </Button>
    </form>
  );
}
