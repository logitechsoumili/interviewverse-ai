import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().min(1, "Email is required.").email("Enter a valid email."),
  password: z.string().min(1, "Password is required."),
});

export const registerSchema = z
  .object({
    full_name: z
      .string()
      .min(2, "Full name must be at least 2 characters.")
      .max(255, "Full name is too long."),
    email: z.string().min(1, "Email is required.").email("Enter a valid email."),
    password: z
      .string()
      .min(8, "Password must be at least 8 characters.")
      .max(128, "Password is too long."),
    confirm_password: z.string().min(1, "Please confirm your password."),
  })
  .refine((values) => values.password === values.confirm_password, {
    message: "Passwords do not match.",
    path: ["confirm_password"],
  });

export type LoginFormValues = z.infer<typeof loginSchema>;
export type RegisterFormValues = z.infer<typeof registerSchema>;
