import axios, { AxiosHeaders, type AxiosError } from "axios";
import {
  clearAuthToken,
  getAuthToken,
  dispatchAuthLogout,
} from "@/lib/auth-storage";

import { env } from "@/lib/env";

export const API_BASE_URL = env.NEXT_PUBLIC_API_URL;

export const http = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

http.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = getAuthToken();

    if (token) {
      const headers = AxiosHeaders.from(config.headers);
      headers.set("Authorization", `Bearer ${token}`);
      config.headers = headers;
    }
  }

  return config;
});

http.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (typeof window !== "undefined" && error.response?.status === 401) {
      clearAuthToken();
      dispatchAuthLogout();
    }

    return Promise.reject(error);
  }
);
