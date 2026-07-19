import Link from "next/link";
import { AuthShell } from "@/components/auth/auth-shell";
import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <AuthShell
      title="Sign in"
      description="Access your InterviewVerse AI workspace."
      footer={
        <p className="text-sm text-muted-foreground">
          New here?{" "}
          <Link className="font-medium text-primary hover:underline" href="/register">
            Create an account
          </Link>
        </p>
      }
    >
      <LoginForm />
    </AuthShell>
  );
}
