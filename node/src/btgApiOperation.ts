import { buildHeaders, handleResponse } from './btgApiUtils.js';
import { buildBtgUrl } from './btgUrl.js';

const DEFAULT_TIMEOUT = 30_000;

export interface OperationHistoryPartnerRequest {
  monthRef: string;
}

function buildOperationHeaders(
  fetchCurrentAccount: boolean
): Promise<Record<string, string>> {
  return fetchCurrentAccount
    ? buildHeaders({ fetch_current_account: 'no_value' })
    : buildHeaders();
}

export async function getMovementsByAccountFull(
  accountNumber: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-operation/api/v1/operation-history/full/${accountNumber}`
    ),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getMovementsByAccountMonthly(
  accountNumber: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-operation/api/v1/operation-history/monthly/${accountNumber}`
    ),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getMovementsByAccountWeekly(
  accountNumber: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-operation/api/v1/operation-history/weekly/${accountNumber}`
    ),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getMovementsByPartnerAndPeriod(
  monthRef: string,
  options?: { fetchCurrentAccount?: boolean; timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const headers = await buildOperationHeaders(fetchCA);
  const body: OperationHistoryPartnerRequest = { monthRef };

  const response = await fetch(
    buildBtgUrl('/iaas-api-operation/api/v1/operation-history/period'),
    {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeout),
    }
  );
  await handleResponse(response);
}

export async function getMovementsByPartnerMonthly(options?: {
  fetchCurrentAccount?: boolean;
  timeout?: number;
}): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(
    buildBtgUrl('/iaas-api-operation/api/v1/operation-history/monthly'),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getMovementsByPartnerWeekly(options?: {
  fetchCurrentAccount?: boolean;
  timeout?: number;
}): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const fetchCA = options?.fetchCurrentAccount ?? true;
  const headers = await buildOperationHeaders(fetchCA);

  const response = await fetch(
    buildBtgUrl('/iaas-api-operation/api/v1/operation-history/weekly'),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}
