import { buildHeaders, handleResponse } from "./btgApiUtils.js";

const BASE_URL = "https://api.btgpactual.com/iaas-api-operation";
const DEFAULT_TIMEOUT = 30_000;

export interface OperationHistoryPartnerRequest {
  monthRef: string;
}

function buildOperationHeaders(
  fetchCurrentAccount: boolean,
): Promise<Record<string, string>> {
  return fetchCurrentAccount
    ? buildHeaders({ fetch_current_account: "no_value" })
    : buildHeaders();
}

export async function getMovementsByAccountFull(
  accountNumber: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number },
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const url = `${BASE_URL}/api/v1/operation-history/full/${accountNumber}`;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(url, {
    method: "GET",
    headers,
    signal: AbortSignal.timeout(timeout),
  });
  await handleResponse(response);
}

export async function getMovementsByAccountMonthly(
  accountNumber: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number },
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const url = `${BASE_URL}/api/v1/operation-history/monthly/${accountNumber}`;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(url, {
    method: "GET",
    headers,
    signal: AbortSignal.timeout(timeout),
  });
  await handleResponse(response);
}

export async function getMovementsByAccountWeekly(
  accountNumber: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number },
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const url = `${BASE_URL}/api/v1/operation-history/weekly/${accountNumber}`;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(url, {
    method: "GET",
    headers,
    signal: AbortSignal.timeout(timeout),
  });
  await handleResponse(response);
}

export async function getMovementsByPartnerAndPeriod(
  monthRef: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number },
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const url = `${BASE_URL}/api/v1/operation-history/period`;
  const headers = await buildOperationHeaders(fetchCA);
  const body: OperationHistoryPartnerRequest = { monthRef };

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(timeout),
  });
  await handleResponse(response);
}

export async function getMovementsByPartnerMonthly(
  options?: { fetchCurrentAccount?: boolean; timeout?: number },
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const url = `${BASE_URL}/api/v1/operation-history/monthly`;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(url, {
    method: "GET",
    headers,
    signal: AbortSignal.timeout(timeout),
  });
  await handleResponse(response);
}

export async function getMovementsByPartnerWeekly(
  options?: { fetchCurrentAccount?: boolean; timeout?: number },
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const url = `${BASE_URL}/api/v1/operation-history/weekly`;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(url, {
    method: "GET",
    headers,
    signal: AbortSignal.timeout(timeout),
  });
  await handleResponse(response);
}
