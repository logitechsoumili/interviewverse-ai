import axios from "axios";

type FastApiValidationDetail = {
  loc?: Array<string | number>;
  msg?: string;
};

type ApiErrorPayload = {
  detail?: string | FastApiValidationDetail[];
  message?: string;
};

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return "Network error. Please check your connection and try again.";
    }

    const payload = error.response.data as ApiErrorPayload | undefined;

    if (typeof payload?.detail === "string") {
      return payload.detail;
    }

    if (Array.isArray(payload?.detail) && payload.detail.length > 0) {
      return payload.detail
        .map((item) => item.msg)
        .filter((message): message is string => Boolean(message))
        .join(" ");
    }

    if (typeof payload?.message === "string") {
      return payload.message;
    }

    return error.message || "Something went wrong. Please try again.";
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong. Please try again.";
}
