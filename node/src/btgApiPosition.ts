import type {
  FixedIncomeHistoryRequest,
  Position,
  PositionData,
  PositionDateRequest,
  PositionDownloadData,
  PositionPeriodFilter,
  PositionPURequest,
} from './btgApiPositionTypes.js';
import { buildHeaders, handleResponse } from './btgApiUtils.js';
import { buildBtgUrl } from './btgUrl.js';

const DEFAULT_TIMEOUT = 30_000;

export async function getPositionByAccount(
  accountNumber: string,
  options?: { timeout?: number }
): Promise<Position> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();

  const response = await fetch(
    buildBtgUrl(`/iaas-api-position/api/v1/position/${accountNumber}`),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  return handleResponse<Position>(response);
}

export async function getPositionByAccountAndDate(
  accountNumber: string,
  date: string,
  options?: { timeout?: number }
): Promise<PositionData> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();
  const body: PositionDateRequest = { date };

  const response = await fetch(
    buildBtgUrl(`/iaas-api-position/api/v1/position/${accountNumber}`),
    {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeout),
    }
  );
  return handleResponse<PositionData>(response);
}

export async function getPositionUnitPriceByAccount(
  accountNumber: string,
  options?: { startDate?: string; endDate?: string; timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();
  const body: PositionPURequest = {};
  if (options?.startDate) body.startDate = options.startDate;
  if (options?.endDate) body.endDate = options.endDate;

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-position/api/v1/position/unit-price/${accountNumber}`
    ),
    {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeout),
    }
  );
  await handleResponse(response);
}

export async function getPositionUnitPriceHistoryByAccount(
  accountNumber: string,
  options?: { timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-position/api/v1/position/unit-price/history/${accountNumber}`
    ),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getPartnerPosition(options?: {
  timeout?: number;
}): Promise<PositionDownloadData> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();

  const response = await fetch(
    buildBtgUrl('/iaas-api-position/api/v1/position/partner'),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  return handleResponse<PositionDownloadData>(response);
}

export async function getPositionRefresh(options?: {
  timeout?: number;
}): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();

  const response = await fetch(
    buildBtgUrl('/iaas-api-position/api/v1/position/refresh'),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getPositionUnitPriceByAccountV2(
  accountNumber: string,
  startDate: string,
  endDate: string,
  options?: { timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();
  const body: PositionPeriodFilter = { startDate, endDate };

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-position/api/v2/position/unit-price/${accountNumber}`
    ),
    {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeout),
    }
  );
  await handleResponse(response);
}

export async function getPositionUnitPriceHistoryByAccountV2(
  accountNumber: string,
  options?: { timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();

  const response = await fetch(
    buildBtgUrl(
      `/iaas-api-position/api/v2/position/unit-price/history/${accountNumber}`
    ),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getPositionUnitPriceHistoryByPartnerV2(options?: {
  timeout?: number;
}): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();

  const response = await fetch(
    buildBtgUrl(
      '/iaas-api-position/api/v2/position/unit-price/history/partner'
    ),
    { method: 'GET', headers, signal: AbortSignal.timeout(timeout) }
  );
  await handleResponse(response);
}

export async function getPositionUnitPriceHistoryByAccountsV2(
  accounts: string[],
  options?: { timeout?: number }
): Promise<void> {
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const headers = await buildHeaders();
  const body: FixedIncomeHistoryRequest = { accounts };

  const response = await fetch(
    buildBtgUrl(
      '/iaas-api-position/api/v2/position/unit-price/history/accounts'
    ),
    {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(timeout),
    }
  );
  await handleResponse(response);
}
