import Link from "next/link";
import { AuthShell } from "@/components/auth/auth-shell";
import { RegisterForm } from "@/components/auth/register-form";

export default function RegisterPage() {
  return (
    <AuthShell
      title="Create account"
      description="Start your InterviewVerse AI journey."
      footer={
        <p className="text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link className="font-medium text-primary hover:underline" href="/login">
            Sign in
          </Link>
        </p>
      }
    >
      <RegisterForm />
    </AuthShell>
  );
}
