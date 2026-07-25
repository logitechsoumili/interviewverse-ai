import { z } from "zod";

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z
    .string()
    .refine(
      (val) => val.startsWith("/") || z.string().url().safeParse(val).success,
      {
        message: "NEXT_PUBLIC_API_URL must be a valid URL or a relative path starting with '/'",
      }
    )
    .default("/api/v1"),
});

function validateEnv() {
  const result = envSchema.safeParse({
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || undefined,
  });

  if (!result.success) {
    // In production, throw an error to fail fast and prevent deploying misconfigured builds.
    console.error("❌ Invalid environment variables:", result.error.format());
    if (process.env.NODE_ENV === "production") {
      throw new Error(
        "Invalid environment variables. Build/Runtime aborted to prevent production misconfiguration."
      );
    }
    return {
      NEXT_PUBLIC_API_URL: "/api/v1",
    };
  }

  return result.data;
}

export const env = validateEnv();
