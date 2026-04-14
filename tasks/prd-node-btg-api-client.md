# PRD: TypeScript npm Package for BTG Pactual API

## Introduction

Create a TypeScript npm package, located at `./node`, that provides strongly-typed Node.js (>=20) access to the BTG Pactual Auth, Position, and Operation APIs. The package mirrors the existing Python clients in `./python` (`btg_api_auth.py`, `btg_api_position.py`, `btg_api_operation.py`) 1:1 as individual exported functions, but is a pure TypeScript reimplementation using the native `fetch` API — it does **not** call the Python code. A typed consumer script equivalent to `python/test.py` demonstrates usage.

## Goals

- Expose every function in the three Python modules as an individually-importable, camelCase TypeScript function with identical behavior and semantics.
- Provide complete TypeScript types for every request payload and every response payload (port all `TypedDict` classes).
- Zero runtime dependencies — use Node 20+ built-in `fetch`.
- OAuth2 token caching with the same 15-minute validity + 1-minute safety buffer as the Python client.
- Read credentials from `BTG_CLIENT_ID` / `BTG_CLIENT_SECRET` env vars (same as Python).
- Ship a working `test.ts` that reproduces `python/test.py` against the same endpoints.

## User Stories

### US-001: Initialize npm package scaffold
**Description:** As a developer, I want a properly configured TypeScript npm package at `./node` so consumers can install and import it.

**Acceptance Criteria:**
- [ ] `node/package.json` created with `"type": "module"`, `"engines": { "node": ">=20" }`, entry points for ESM, and a `build` script
- [ ] `node/tsconfig.json` with `strict: true`, `target: ES2022`, `module: NodeNext`, `moduleResolution: NodeNext`, `declaration: true`, `outDir: dist`
- [ ] `node/.gitignore` excludes `dist/` and `node_modules/`
- [ ] `node/src/` directory created
- [ ] No runtime dependencies in `package.json` (only `typescript` and `tsx` as devDependencies; `@types/node` as devDependency for Node built-ins)
- [ ] `npx tsc --noEmit` passes on an empty project

### US-002: Port auth module (`btgApiAuth`)
**Description:** As a developer, I want `getAccessToken()` and `clearTokenCache()` to obtain and cache OAuth2 tokens exactly like the Python client.

**Acceptance Criteria:**
- [ ] `node/src/btgApiAuth.ts` exports `getAccessToken(options?: { timeout?: number; useCache?: boolean }): Promise<string>`
- [ ] `node/src/btgApiAuth.ts` exports `clearTokenCache(): void`
- [ ] `node/src/btgApiAuth.ts` exports `BtgAuthError` class with `statusCode` and `responseBody` properties
- [ ] `node/src/btgApiAuth.ts` exports `TokenResponse` interface
- [ ] Token cached in module-level state for `TOKEN_VALIDITY_SECONDS - 60` seconds
- [ ] Reads `BTG_CLIENT_ID` / `BTG_CLIENT_SECRET` from `process.env`; throws `BtgAuthError` if missing
- [ ] Sends `POST` to `https://api.btgpactual.com/iaas-auth/api/v1/authorization/oauth2/accesstoken` with Basic auth header, `x-id-partner-request` UUID, `Content-Type: application/x-www-form-urlencoded`, body `grant_type=client_credentials`
- [ ] Reads token from `access_token` response header first, falls back to response JSON body
- [ ] `tsc --noEmit` passes

### US-003: Port shared utilities (`btgApiUtils`)
**Description:** As a developer, I need shared header-building, response-handling, and error utilities that mirror `btg_api_utils.py`.

**Acceptance Criteria:**
- [ ] `node/src/btgApiUtils.ts` exports `buildHeaders(extra?: Record<string, string>): Promise<Record<string, string>>` — injects `access_token` (from `getAccessToken`), `x-id-partner-request` UUID, `Content-Type: application/json`
- [ ] `node/src/btgApiUtils.ts` exports `handleResponse<T>(response: Response): Promise<T>` — returns parsed JSON for 200, `{}` for 202, throws `BtgApiError` otherwise with message extracted from `errors[0].message`, `meta.globalErrors[0].message`, or `message` field
- [ ] `node/src/btgApiUtils.ts` exports `BtgApiError` class with `statusCode` and `responseBody`
- [ ] Exports `Error`, `ErrorMetadata`, `ResponseError` interfaces (ported from `TypedDict`s; rename `Error` → `BtgError` to avoid clashing with global `Error`)
- [ ] Uses `crypto.randomUUID()` for the partner-request ID
- [ ] `tsc --noEmit` passes

### US-004: Port position request types and all nested response types
**Description:** As a developer, I want every `TypedDict` from `btg_api_position.py` ported to a TypeScript interface so responses are fully typed. Use `python/docs/API-POSITION.yml` as the authoritative schema source.

**Acceptance Criteria:**
- [ ] `node/src/btgApiPositionTypes.ts` contains TypeScript interfaces for every `TypedDict` in `btg_api_position.py` (≈70 types including `Position`, `PositionData`, `PositionDownloadData`, `Positions`, `Acquisition`, `ACCACE`, `AccountingGroup`, `Prices`, `Acquisitions`, `ValuesPerCurrency`, `ValuesPerCurrencySBCLC`, `ValuesPerCurrencyACC`, `ACCs`, `AveragePrice`, `BMFFuturePosition`, `BMFOptionPosition`, `CashCollateral`, `CashInvestedName`, `CashInvested`, `CetipOptionPosition`, `CollateralPositions`, `Commitments`, `Credit`, `CryptoAsset`, `CryptoAcquisition`, `CurrentAccount`, `DebtEarlyTerminationPeriod`, `DebtEarlyTerminationSchedules`, `Derivative1`, `Equities1`, `FixedIncome1`, `ReferenceAsset`, `ForwardPositions`, `Fund`, `InvestmentFund1`, `IrAliquots`, `Loan`, `NDFPosition`, `TickerInfo`, `OptionPositions`, `Others`, `Pension`, `PrecatoryAsset`, `PrecatoryAcquisition`, `PrecatoryScenario`, `PortfolioInvestments`, `RealEstate`, `Receivables`, `SBCLC`, `StockLendingPositions`, `StockPositions`, `StructuredProducts`, `SwapPosition`, `SummaryAccount`, `InvestmentFund`, `InvestmentFundCotaCetipada`, `FixedIncome`, `Credits`, `PensionInformations`, `Commodity`, `Equities`, `Derivative`, `FixedIncomeStructuredNote`, `PayableReceivables`, `PendingSettlements`, `CryptoCoins`, `Cash`, `CashCollateralRoot`, `Precatories`, `PrecatoriesCR`, and request types `PositionDateRequest`, `PositionPURequest`, `PositionPeriodFilter`, `FixedIncomeHistoryRequest`)
- [ ] `NotRequired[X]` in Python maps to `X | undefined` optional (`field?: X`) in TypeScript
- [ ] `list[X]` maps to `X[]`, `dict` maps to `Record<string, unknown>`
- [ ] No `any` types used
- [ ] `tsc --noEmit` passes

### US-005: Port position API functions
**Description:** As a developer, I want every position endpoint available as a typed async TS function.

**Acceptance Criteria:**
- [ ] `node/src/btgApiPosition.ts` exports the following async functions with signatures matching the Python versions (camelCased, params optional where Python used defaults):
  - `getPositionByAccount(accountNumber: string, options?: { timeout?: number }): Promise<Position>`
  - `getPositionByAccountAndDate(accountNumber: string, date: string, options?: { timeout?: number }): Promise<PositionData>`
  - `getPositionUnitPriceByAccount(accountNumber: string, options?: { startDate?: string; endDate?: string; timeout?: number }): Promise<void>`
  - `getPositionUnitPriceHistoryByAccount(accountNumber: string, options?: { timeout?: number }): Promise<void>`
  - `getPartnerPosition(options?: { timeout?: number }): Promise<PositionDownloadData>`
  - `getPositionRefresh(options?: { timeout?: number }): Promise<void>`
  - `getPositionUnitPriceByAccountV2(accountNumber: string, startDate: string, endDate: string, options?: { timeout?: number }): Promise<void>`
  - `getPositionUnitPriceHistoryByAccountV2(accountNumber: string, options?: { timeout?: number }): Promise<void>`
  - `getPositionUnitPriceHistoryByPartnerV2(options?: { timeout?: number }): Promise<void>`
  - `getPositionUnitPriceHistoryByAccountsV2(accounts: string[], options?: { timeout?: number }): Promise<void>`
- [ ] All URLs use `BASE_URL = "https://api.btgpactual.com/iaas-api-position"` and match the Python paths exactly
- [ ] HTTP methods and bodies match the Python client (e.g. `getPositionByAccountAndDate` POSTs `{ date }`)
- [ ] Timeouts implemented via `AbortController` / `AbortSignal.timeout(ms)` (default 30000 ms)
- [ ] `tsc --noEmit` passes

### US-006: Port operation module (`btgApiOperation`)
**Description:** As a developer, I want every operation endpoint as a typed async TS function.

**Acceptance Criteria:**
- [ ] `node/src/btgApiOperation.ts` exports:
  - `OperationHistoryPartnerRequest` interface (`{ monthRef: string }`)
  - `getMovementsByAccountFull(accountNumber: string, options?: { fetchCurrentAccount?: boolean; timeout?: number }): Promise<void>`
  - `getMovementsByAccountMonthly(accountNumber: string, options?: { fetchCurrentAccount?: boolean; timeout?: number }): Promise<void>`
  - `getMovementsByAccountWeekly(accountNumber: string, options?: { fetchCurrentAccount?: boolean; timeout?: number }): Promise<void>`
  - `getMovementsByPartnerAndPeriod(monthRef: string, options?: { fetchCurrentAccount?: boolean; timeout?: number }): Promise<void>`
  - `getMovementsByPartnerMonthly(options?: { fetchCurrentAccount?: boolean; timeout?: number }): Promise<void>`
  - `getMovementsByPartnerWeekly(options?: { fetchCurrentAccount?: boolean; timeout?: number }): Promise<void>`
- [ ] `fetchCurrentAccount` defaults to `true`; when `true`, adds `fetch_current_account: "no_value"` header (mirrors Python)
- [ ] URLs use `BASE_URL = "https://api.btgpactual.com/iaas-api-operation"` and match the Python paths exactly
- [ ] `tsc --noEmit` passes

### US-007: Package barrel export
**Description:** As a consumer, I want a single `index.ts` that re-exports everything so I can import from the package root.

**Acceptance Criteria:**
- [ ] `node/src/index.ts` re-exports all public functions, types, and errors from the 4 modules
- [ ] `package.json` points `main`, `module`, and `types` at the compiled `dist/index.js` / `dist/index.d.ts`
- [ ] `npm run build` produces `dist/` with `.js` and `.d.ts` files
- [ ] `tsc --noEmit` passes

### US-008: Port `test.py` to `test.ts`
**Description:** As a developer, I want a `node/test.ts` that demonstrates the package and mirrors `python/test.py`.

**Acceptance Criteria:**
- [ ] `node/test.ts` imports `getPositionByAccountAndDate`, `getMovementsByAccountFull`, `getMovementsByPartnerWeekly` from the local package
- [ ] Mirrors the three branches in `python/test.py` (two behind `if (false)` gates, one active calling `getMovementsByPartnerWeekly` and writing the response to `get_movements_by_partner_weekly.json`)
- [ ] Uses `node:fs/promises` `writeFile` with `JSON.stringify`
- [ ] Runnable via `npx tsx node/test.ts` (add `tsx` as a devDependency); document the command in `node/README.md`
- [ ] Type-checks strictly (no `any`) against the package types
- [ ] `tsc --noEmit` passes

## Functional Requirements

- FR-1: The package MUST be located at `./node` relative to the repo root.
- FR-2: The package MUST target Node.js >=20 and use native `fetch` — no `axios`, `undici`, `node-fetch`, or other HTTP libraries.
- FR-3: The package MUST have zero runtime dependencies (`dependencies: {}`).
- FR-4: All source files MUST live under `node/src/` and be authored in TypeScript with `strict: true`.
- FR-5: Every function from `btg_api_auth.py`, `btg_api_position.py`, and `btg_api_operation.py` MUST have a 1:1 TypeScript equivalent (camelCase naming).
- FR-6: Every `TypedDict` from those three modules MUST be ported to a TypeScript `interface` (camelCase on fields is NOT applied — preserve the original API field names from the wire format, e.g., `monthRef`, `startDate`, `globalErrors`).
- FR-7: Function parameter names MUST be camelCased (e.g., `accountNumber`, `monthRef`) even though Python uses snake_case.
- FR-8: Optional Python parameters (those with defaults) MUST be grouped into a trailing `options?` object in TypeScript.
- FR-9: Errors from the API MUST be thrown as `BtgApiError` (or `BtgAuthError` for auth endpoints) with the same message-extraction precedence as the Python `handle_response`.
- FR-10: Token caching MUST be process-global (module-level state), matching Python behavior.
- FR-11: Credential env vars MUST be `BTG_CLIENT_ID` and `BTG_CLIENT_SECRET` (same as Python). No `dotenv` dependency — consumers are responsible for loading `.env` themselves (document this).
- FR-12: The default request timeout MUST be 30 seconds and MUST be implementable per-call via an `options.timeout` number (milliseconds in TS; the Python value is seconds — convert and document clearly).
- FR-13: The package MUST NOT shell out to Python.

## Non-Goals

- No webhook server implementation (the Python `webhook_server.py` is out of scope).
- No wallet-related scripts (`create_quantum_wallet.py`, `recreate_wallet.py`) — these are not API clients.
- No class-based client API (`new BtgClient()`). Only individual functions, per the user's explicit choice.
- No automated unit/integration test suite — only the manual `test.ts` script demonstrating usage.
- No publishing to the public npm registry in this iteration; the package is local-only.
- No retry/backoff logic beyond what the Python client already does (which is none).
- No `.env` auto-loading — consumers load env vars themselves.
- No support for Node <20, Bun, or Deno.
- No Python–TypeScript cross-validation harness.

## Technical Considerations

- **Timeout units:** Python uses seconds (float), TypeScript convention is milliseconds. Convert: Python `30.0` → TS `30_000`. Document this in the function JSDoc.
- **UUIDs:** Use `crypto.randomUUID()` (built into Node 20+) — no `uuid` dependency.
- **Basic auth encoding:** Use `Buffer.from(`${id}:${secret}`).toString("base64")`.
- **Abort on timeout:** `AbortSignal.timeout(ms)` is the simplest approach (Node 20+).
- **Field-name casing:** Wire payloads use BTG's existing casing (`monthRef`, `startDate`, `globalErrors`, `access_token` header, `x-id-partner-request` header). Function **parameters** are camelCased, but request/response **interface fields** mirror the wire format. Do not rename.
- **`Error` type clash:** Python's `Error` TypedDict should be renamed in TS (e.g., `BtgError`) to avoid shadowing the global `Error`.
- **Module layout:**
  ```
  node/
    package.json
    tsconfig.json
    .gitignore
    src/
      index.ts
      btgApiAuth.ts
      btgApiUtils.ts
      btgApiPosition.ts
      btgApiPositionTypes.ts
      btgApiOperation.ts
    test.ts
  ```
- **No bundler required** — just `tsc`.

## Success Metrics

- `npx tsc --noEmit` passes with zero errors on the full `node/` project.
- `node/test.ts` type-checks strictly against the package's own types (no `any`).
- Every public symbol from the Python modules has a TypeScript counterpart (verified by manual checklist against `__all__` in each Python file).
- A developer reading `node/test.ts` can see that it is a direct translation of `python/test.py`.

### US-009: Add minimal README
**Description:** As a consumer of the package, I want a short `node/README.md` documenting setup and usage.

**Acceptance Criteria:**
- [ ] `node/README.md` explains required env vars: `BTG_CLIENT_ID`, `BTG_CLIENT_SECRET`
- [ ] Notes that consumers must load `.env` themselves (no built-in `dotenv`)
- [ ] Shows install command and the `npx tsx test.ts` run command
- [ ] Shows one minimal import + call example (e.g., `getPositionByAccountAndDate`)
- [ ] Kept short — under ~40 lines

## Reference Documentation

Authoritative OpenAPI specs for the three APIs live in `python/docs/`:
- `python/docs/auth-token.yml` — auth/token endpoint
- `python/docs/API-POSITION.yml` — position endpoints (including the full `PositionDownloadData` shape and every nested schema)
- `python/docs/api-operation.yml` — operation endpoints

When porting a `TypedDict`, consult these specs as the source of truth. If the Python `TypedDict` and the OpenAPI schema disagree, **trust the OpenAPI spec** and flag the discrepancy in a code comment.

## Open Questions

None — all previously-open questions resolved.
