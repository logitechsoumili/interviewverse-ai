export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  full_name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface AuthenticationState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface RegisterFormValues extends RegisterRequest {
  confirm_password: string;
}
