# btg-mfo-api-client

[![npm version](https://img.shields.io/npm/v/btg-mfo-api-client.svg)](https://www.npmjs.com/package/btg-mfo-api-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D20-brightgreen.svg)](#requirements)
[![GitHub Issues](https://img.shields.io/github/issues/lobobruno/btg-mfo-api-client.svg)](https://github.com/lobobruno/btg-mfo-api-client/issues)
[![GitHub Stars](https://img.shields.io/github/stars/lobobruno/btg-mfo-api-client.svg)](https://github.com/lobobruno/btg-mfo-api-client/stargazers)

## Table of Contents

- 💡 [Description](#-description)
- ✨ [Features](#-features)
- 📌 [Requirements](#-requirements)
- 🚀 [Installation](#-installation)
- 🔐 [Authentication](#-authentication)
- 📚 [Usage & Examples](#-usage--examples)
- 🧱 [API](#-api)
- 📣 [Feedback & Contact](#-feedback--contact)

## 💡 Description

`btg-mfo-api-client` is a TypeScript client for the **BTG Pactual MFO (Multi Family Office) APIs**, covering Auth, Position, and Operation endpoints. It handles OAuth2 `client_credentials` authentication with token caching, typed requests, and strongly-typed responses so you can consume BTG data directly from Node.js without wrangling HTTP details.

## ✨ Features

- 🔑 OAuth2 authentication with automatic token caching
- 📊 Position endpoints (by account, by date, by partner, unit price history, V2 variants)
- 💸 Operation / movement endpoints (account and partner, full/monthly/weekly windows)
- 🧾 Full TypeScript types for every response payload
- 🪶 Zero runtime dependencies — uses the native `fetch` in Node 20+
- 🛑 Typed error classes (`BtgAuthError`, `BtgApiError`) with status code and body

## 📌 Requirements

- Node.js **20+**
- BTG Pactual API credentials (`BTG_CLIENT_ID`, `BTG_CLIENT_SECRET`)

## 🚀 Installation

```bash
npm install btg-mfo-api-client
```

```bash
yarn add btg-mfo-api-client
```

```bash
pnpm add btg-mfo-api-client
```

## 🔐 Authentication

Set your credentials as environment variables before calling any API:

```bash
export BTG_CLIENT_ID="your-client-id"
export BTG_CLIENT_SECRET="your-client-secret"
```

The package does not bundle `dotenv` — load `.env` yourself (e.g. `import "dotenv/config"`) if you use one.

Tokens are cached in-memory for ~14 minutes. Call `clearTokenCache()` to force a refresh.

## 📚 Usage & Examples

### Get a position for a specific date

```ts
import { getPositionByAccountAndDate } from "btg-mfo-api-client";

const position = await getPositionByAccountAndDate("000123456", "2025-11-28");
console.log(position);
```

### Get weekly movements for the partner

```ts
import { getMovementsByPartnerWeekly } from "btg-mfo-api-client";

const movements = await getMovementsByPartnerWeekly();
console.log(movements);
```

### Get full movement history for an account

```ts
import { getMovementsByAccountFull } from "btg-mfo-api-client";

const history = await getMovementsByAccountFull("000987654");
console.log(history);
```

### Handle typed errors

```ts
import { getPositionByAccountAndDate, BtgApiError, BtgAuthError } from "btg-mfo-api-client";

try {
  await getPositionByAccountAndDate("000123456", "2025-11-28");
} catch (err) {
  if (err instanceof BtgAuthError) {
    console.error("Auth failed", err.statusCode, err.responseBody);
  } else if (err instanceof BtgApiError) {
    console.error("API error", err.statusCode, err.responseBody);
  } else {
    throw err;
  }
}
```

## 🧱 API

### Auth

- `getAccessToken(options?)` — returns a cached or fresh access token
- `clearTokenCache()` — clears the cached token

### Position

- `getPositionByAccount(account)`
- `getPositionByAccountAndDate(account, date)`
- `getPositionUnitPriceByAccount(account)`
- `getPositionUnitPriceHistoryByAccount(account, filter)`
- `getPartnerPosition()`
- `getPositionRefresh(account)`
- `getPositionUnitPriceByAccountV2(account)`
- `getPositionUnitPriceHistoryByAccountV2(account, filter)`
- `getPositionUnitPriceHistoryByPartnerV2(filter)`
- `getPositionUnitPriceHistoryByAccountsV2(accounts, filter)`

### Operation

- `getMovementsByAccountFull(account)`
- `getMovementsByAccountMonthly(account)`
- `getMovementsByAccountWeekly(account)`
- `getMovementsByPartnerAndPeriod(request)`
- `getMovementsByPartnerMonthly()`
- `getMovementsByPartnerWeekly()`

Every response is fully typed — see the exported types in `btgApiPositionTypes` (e.g. `Position`, `PositionData`, `InvestmentFund`, `FixedIncome`, `Equities`, `Derivative`, `CryptoAsset`, and many more).

## 📣 Feedback & Contact

Bugs, feature requests, and contributions welcome at [github.com/lobobruno/btg-mfo-api-client](https://github.com/lobobruno/btg-mfo-api-client/issues).

Reach me on X/Twitter: [@brunowlf](https://twitter.com/brunowlf).

---

Licensed under the [MIT License](./LICENSE).
