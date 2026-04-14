import { randomUUID } from "node:crypto";
import { getAccessToken } from "./btgApiAuth.js";

export interface BtgError {
  code?: string;
  message?: string;
}

export interface ErrorMetadata {
  globalErrors?: BtgError[];
  fieldErrors?: Record<string, unknown>;
}

export interface ResponseError {
  status?: number;
  title?: string;
  meta?: ErrorMetadata;
}

export class BtgApiError extends Error {
  statusCode: number | undefined;
  responseBody: Record<string, unknown> | undefined;

  constructor(
    message: string,
    statusCode?: number,
    responseBody?: Record<string, unknown>,
  ) {
    super(message);
    this.name = "BtgApiError";
    this.statusCode = statusCode;
    this.responseBody = responseBody;
  }
}

export async function buildHeaders(
  extra?: Record<string, string>,
): Promise<Record<string, string>> {
  const headers: Record<string, string> = {
    access_token: await getAccessToken(),
    "x-id-partner-request": randomUUID(),
    "Content-Type": "application/json",
  };
  if (extra) {
    Object.assign(headers, extra);
  }
  return headers;
}

export async function handleResponse<T>(response: Response): Promise<T> {
  if (response.status === 200 || response.status === 202) {
    if (response.status === 202) {
      return {} as T;
    }
    try {
      return (await response.json()) as T;
    } catch {
      return {} as T;
    }
  }

  let errorBody: Record<string, unknown>;
  try {
    errorBody = (await response.json()) as Record<string, unknown>;
  } catch {
    errorBody = { message: await response.text() };
  }

  let errorMessage = `BTG API Error (HTTP ${response.status})`;

  const errors = errorBody.errors;
  if (Array.isArray(errors) && errors.length > 0) {
    const msg = (errors[0] as Record<string, unknown>).message;
    if (typeof msg === "string") errorMessage = msg;
  } else if (
    errorBody.meta &&
    typeof errorBody.meta === "object" &&
    "globalErrors" in (errorBody.meta as Record<string, unknown>)
  ) {
    const globalErrors = (errorBody.meta as Record<string, unknown>)
      .globalErrors;
    if (Array.isArray(globalErrors) && globalErrors.length > 0) {
      const msg = (globalErrors[0] as Record<string, unknown>).message;
      if (typeof msg === "string") errorMessage = msg;
    }
  } else if (typeof errorBody.message === "string") {
    errorMessage = errorBody.message;
  }

  throw new BtgApiError(errorMessage, response.status, errorBody);
}
