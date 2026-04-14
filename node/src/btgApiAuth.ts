import { randomUUID } from 'node:crypto';
import { buildBtgUrl } from './btgUrl.js';

const DEFAULT_TIMEOUT = 30_000;
const TOKEN_VALIDITY_SECONDS = 15 * 60;

let cachedToken: string | null = null;
let tokenExpiry = 0;

export class BtgAuthError extends Error {
  statusCode: number | undefined;
  responseBody: Record<string, unknown> | undefined;

  constructor(
    message: string,
    statusCode?: number,
    responseBody?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'BtgAuthError';
    this.statusCode = statusCode;
    this.responseBody = responseBody;
  }
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

function getCredentials(): [string, string] {
  const clientId = process.env.BTG_CLIENT_ID;
  const clientSecret = process.env.BTG_CLIENT_SECRET;
  if (!clientId) {
    throw new BtgAuthError(
      'Client ID is required. Set BTG_CLIENT_ID environment variable.'
    );
  }
  if (!clientSecret) {
    throw new BtgAuthError(
      'Client secret is required. Set BTG_CLIENT_SECRET environment variable.'
    );
  }
  return [clientId, clientSecret];
}

function buildBasicAuthHeader(): string {
  const [clientId, clientSecret] = getCredentials();
  const encoded = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
  return `Basic ${encoded}`;
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0;
}

function extractTokenFromBody(data: Record<string, unknown>): string | null {
  const value = data.access_token;
  return isNonEmptyString(value) ? value : null;
}

function buildHeaders(): Record<string, string> {
  return {
    Authorization: buildBasicAuthHeader(),
    'x-id-partner-request': randomUUID(),
    'Content-Type': 'application/x-www-form-urlencoded',
  };
}

export async function getAccessToken(options?: {
  timeout?: number;
  useCache?: boolean;
}): Promise<string> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const useCache = options?.useCache ?? true;

  if (useCache && cachedToken && Date.now() < tokenExpiry) {
    return cachedToken;
  }

  const headers = buildHeaders();
  const body = 'grant_type=client_credentials';

  const response = await fetch(
    buildBtgUrl('/iaas-auth/api/v1/authorization/oauth2/accesstoken'),
    { method: 'POST', headers, body, signal: AbortSignal.timeout(timeout) }
  );

  if (response.status === 200) {
    const token = response.headers.get('access_token');
    if (token) {
      cachedToken = token;
      tokenExpiry = Date.now() + (TOKEN_VALIDITY_SECONDS - 60) * 1000;
      return token;
    }

    try {
      const data = (await response.json()) as Record<string, unknown>;
      const bodyToken = extractTokenFromBody(data);
      if (bodyToken) {
        cachedToken = bodyToken;
        tokenExpiry = Date.now() + (TOKEN_VALIDITY_SECONDS - 60) * 1000;
        return bodyToken;
      }
    } catch {
      // fall through
    }

    throw new BtgAuthError(
      'Access token not found in response',
      response.status
    );
  }

  let errorBody: Record<string, unknown>;
  try {
    errorBody = (await response.json()) as Record<string, unknown>;
  } catch {
    errorBody = { message: await response.text() };
  }

  const errorMessage =
    typeof errorBody.message === 'string'
      ? errorBody.message
      : `BTG Auth API Error (HTTP ${response.status})`;

  throw new BtgAuthError(errorMessage, response.status, errorBody);
}

export function clearTokenCache(): void {
  cachedToken = null;
  tokenExpiry = 0;
}
