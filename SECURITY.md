# Security Policy

## Threat Model

This package is a thin API client for BTG Pactual's platform APIs.
It is designed to run in server-side environments (Node.js / Python) where
credentials are supplied via environment variables.

### Key assumptions

- **Hosts are hardcoded, not user-supplied.**
  All HTTP requests are routed through a URL builder (`buildBtgUrl` in Node,
  direct `httpx` calls in Python) that enforces a hostname allowlist.
  Only `api.btgpactual.com` is permitted.

- **Credentials come from environment variables.**
  Client ID, client secret, and other auth inputs are read from the
  caller's environment. They are never hardcoded in source.

- **Hostname allowlist is enforced at runtime.**
  Any attempt to construct a URL targeting a host outside the allowlist
  throws an error before the request is sent.

## Covered CWEs

| CWE | Name | Mitigation |
|-----|------|------------|
| [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | Server-Side Request Forgery (SSRF) | Hostname allowlist in `buildBtgUrl` rejects non-BTG hosts |
| [CWE-208](https://cwe.mitre.org/data/definitions/208.html) | Observable Timing Discrepancy | Token type-guards use generic helpers to avoid leaking timing info |
| [CWE-862](https://cwe.mitre.org/data/definitions/862.html) | Missing Authorization | Response validators ensure API responses are checked before use |

## Reporting a Vulnerability

If you discover a security issue in this package, please report it
**privately** so we can address it before public disclosure.

1. **Email:** Send a description to the repository maintainers
   (see the `author` field in `package.json` or `setup.py`).
2. **Include:** A clear description of the issue, steps to reproduce,
   and the potential impact.
3. **Do not** open a public GitHub issue for security vulnerabilities.

We aim to acknowledge reports within 48 hours and provide a fix or
mitigation plan within 7 business days.

## Scope

This policy covers the `btg-api-clientes` Node and Python packages.
Third-party dependencies are outside the scope of this document; refer
to their own security policies.
