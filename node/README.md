# btg-api-client

TypeScript client for the BTG Pactual Auth, Position, and Operation APIs.

## Requirements

- Node.js >= 20
- Environment variables: `BTG_CLIENT_ID`, `BTG_CLIENT_SECRET`

You must load `.env` yourself — the package does not include `dotenv`.

## Install

```bash
cd node && npm install
```

## Usage

```ts
import { getPositionByAccountAndDate } from "./src/index.js";

const position = await getPositionByAccountAndDate("004209281", "2025-11-28");
console.log(position);
```

## Run the demo script

```bash
npx tsx node/test.ts
```

## Build

```bash
npm run build
```

## Typecheck

```bash
npm run typecheck
```
