# btg-api-clientes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./node/LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D20-brightgreen.svg)](./node)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](./python)

TypeScript and Python clients for the **BTG Pactual MFO APIs** (Auth, Position, Operation).

## Table of Contents

- 💡 [Overview](#-overview)
- 📦 [Packages](#-packages)
- 📌 [Requirements](#-requirements)
- 🔐 [Credentials](#-credentials)
- 🚀 [Quick Start](#-quick-start)
- 🗂️ [Repository Layout](#️-repository-layout)
- 🛡️ [Security](#️-security)
- 📄 [License](#-license)

## 💡 Overview

This repository hosts two thin, strongly-typed clients for BTG Pactual's MFO (Multi Family Office) platform:

- **Node.js / TypeScript** — distributed as the [`btg-mfo-api-client`](./node) npm package.
- **Python** — a set of scripts under [`python/`](./python) covering the same endpoints (auth, position, operation).

Both clients hit the same hardcoded host (`api.btgpactual.com`), authenticate via OAuth2 `client_credentials`, and return typed responses.

## 📦 Packages

| Language   | Path                 | Package                                                              | Status     |
|------------|----------------------|----------------------------------------------------------------------|------------|
| TypeScript | [`node/`](./node)    | [`btg-mfo-api-client`](https://www.npmjs.com/package/btg-mfo-api-client) | ✅ Published |
| Python     | [`python/`](./python)| scripts (not yet packaged)                                           | 🧪 Local use |

## 📌 Requirements

- **Node.js** ≥ 20 (for the TypeScript client)
- **Python** ≥ 3.10 (for the Python scripts)
- BTG Pactual API credentials

## 🔐 Credentials

Set the following environment variables before using either client:

```bash
export BTG_CLIENT_ID="your-client-id"
export BTG_CLIENT_SECRET="your-client-secret"
```

Neither client bundles a `.env` loader — use `dotenv` yourself if needed.

## 🚀 Quick Start

### Node.js

```bash
npm install btg-mfo-api-client
```

```ts
import { getPositionByAccountAndDate } from "btg-mfo-api-client";

const position = await getPositionByAccountAndDate("000123456", "2025-11-28");
console.log(position);
```

See [node/README.md](./node/README.md) for the full API reference.

### Python

```bash
cd python
pip install -r requirements.txt
python test.py
```

Modules of interest:
- `btg_api_auth.py` — token acquisition / caching
- `btg_api_position.py` — position endpoints
- `btg_api_operation.py` — movement / operation endpoints

## 🗂️ Repository Layout

```
.
├── node/        # TypeScript client (npm package)
├── python/      # Python scripts + OpenAPI specs in python/docs/
├── scripts/     # Internal tooling
├── SECURITY.md  # Security policy & threat model
└── README.md    # You are here
```

## 🛡️ Security

See [SECURITY.md](./SECURITY.md) for the threat model, covered CWEs, and how to report vulnerabilities privately.

## 📄 License

MIT © Bruno Lobo — see [node/LICENSE](./node/LICENSE).
