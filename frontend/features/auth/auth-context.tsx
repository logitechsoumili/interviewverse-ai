"use client";

import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import axios from "axios";
import { fetchCurrentUser, loginUser, registerUser } from "@/services/auth";
import {
  clearAuthToken,
  dispatchAuthLogout,
  getAuthToken,
  setAuthToken,
} from "@/lib/auth-storage";
import type {
  AuthenticationState,
  LoginRequest,
  RegisterRequest,
  User,
} from "@/types/auth";

export type AuthContextValue = AuthenticationState & {
  login: (payload: LoginRequest) => Promise<User>;
  logout: () => void;
  register: (payload: RegisterRequest) => Promise<User>;
  refreshUser: () => Promise<User | null>;
};

export const AuthContext = createContext<AuthContextValue | null>(null);

type AuthProviderProps = {
  children: ReactNode;
};

function clearAuthState(setUser: (value: User | null) => void, setToken: (value: string | null) => void) {
  clearAuthToken();
  setToken(null);
  setUser(null);
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshUser = useCallback(async (): Promise<User | null> => {
    const storedToken = getAuthToken();

    if (!storedToken) {
      clearAuthState(setUser, setToken);
      setIsLoading(false);
      return null;
    }

    setToken(storedToken);
    setIsLoading(true);

    try {
      const currentUser = await fetchCurrentUser();
      setUser(currentUser);
      return currentUser;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        clearAuthState(setUser, setToken);
      }
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refreshUser();
  }, [refreshUser]);

  useEffect(() => {
    function handleLogout() {
      clearAuthState(setUser, setToken);
      setIsLoading(false);
    }

    window.addEventListener("auth:logout", handleLogout);
    return () => window.removeEventListener("auth:logout", handleLogout);
  }, []);

  const login = useCallback(
    async (payload: LoginRequest): Promise<User> => {
      const response = await loginUser(payload);
      setAuthToken(response.access_token);
      setToken(response.access_token);

      const currentUser = await refreshUser();
      if (!currentUser) {
        clearAuthState(setUser, setToken);
        throw new Error("Unable to restore the authenticated session.");
      }

      return currentUser;
    },
    [refreshUser]
  );

  const register = useCallback(async (payload: RegisterRequest): Promise<User> => {
    const createdUser = await registerUser(payload);
    return createdUser;
  }, []);

  const logout = useCallback(() => {
    clearAuthState(setUser, setToken);
    dispatchAuthLogout();
    window.location.replace("/login");
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(token),
      isLoading,
      login,
      logout,
      register,
      refreshUser,
    }),
    [isLoading, login, logout, refreshUser, register, token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
