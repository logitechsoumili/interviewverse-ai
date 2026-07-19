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
import { useQueryClient } from "@tanstack/react-query";
import {
  fetchCurrentUser,
  loginUser,
  registerUser,
} from "@/features/auth/services/auth";
import {
  clearAuthToken,
  dispatchAuthLogout,
  getAuthToken,
  setAuthToken,
} from "@/lib/auth-storage";
import { queryKeys } from "@/lib/query-keys";
import type {
  AuthenticationState,
  LoginRequest,
  RegisterRequest,
  User,
} from "@/types/auth";

export type AuthContextValue = AuthenticationState & {
  login: (payload: LoginRequest) => Promise<User>;
  logout: () => void;
  register: (payload: RegisterRequest) => Promise<void>;
  refreshUser: () => Promise<User | null>;
};

export const AuthContext = createContext<AuthContextValue | null>(null);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const queryClient = useQueryClient();

  const clearSession = useCallback(() => {
    clearAuthToken();
    setToken(null);
    setUser(null);
    queryClient.removeQueries({ queryKey: queryKeys.currentUser });
    queryClient.removeQueries({ queryKey: queryKeys.interviews });
  }, [queryClient]);

  const refreshUser = useCallback(async (): Promise<User | null> => {
    const storedToken = getAuthToken();

    if (!storedToken) {
      clearSession();
      setIsLoading(false);
      return null;
    }

    setToken(storedToken);
    setIsLoading(true);

    try {
      const currentUser = await queryClient.fetchQuery({
        queryKey: queryKeys.currentUser,
        queryFn: fetchCurrentUser,
        staleTime: 5 * 60 * 1000,
      });
      setUser(currentUser);
      return currentUser;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        clearSession();
      }
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [clearSession, queryClient]);

  useEffect(() => {
    void refreshUser();
  }, [refreshUser]);

  useEffect(() => {
    function handleLogout() {
      clearSession();
      setIsLoading(false);
    }

    window.addEventListener("auth:logout", handleLogout);
    return () => window.removeEventListener("auth:logout", handleLogout);
  }, [clearSession]);

  const login = useCallback(
    async (payload: LoginRequest): Promise<User> => {
      const response = await loginUser(payload);
      setAuthToken(response.access_token);
      setToken(response.access_token);

      const currentUser = await refreshUser();
      if (!currentUser) {
        clearSession();
        throw new Error("Unable to restore the authenticated session.");
      }

      return currentUser;
    },
    [clearSession, refreshUser]
  );

  const register = useCallback(async (payload: RegisterRequest): Promise<void> => {
    await registerUser(payload);
  }, []);

  const logout = useCallback(() => {
    clearSession();
    dispatchAuthLogout();
    window.location.replace("/login");
  }, [clearSession]);

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
