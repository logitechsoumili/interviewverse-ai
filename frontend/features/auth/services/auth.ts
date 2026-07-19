import { http } from "@/services/http";
import type {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  User,
} from "@/types/auth";

export async function loginUser(payload: LoginRequest): Promise<AuthResponse> {
  const { data } = await http.post<AuthResponse>("/auth/login", payload);
  return data;
}

export async function registerUser(
  payload: RegisterRequest
): Promise<void> {
  await http.post("/auth/register", payload);
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await http.get<User>("/users/me");
  return data;
}
