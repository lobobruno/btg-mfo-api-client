"""Response validation helper for BTG API clients."""
from __future__ import annotations
from typing import Any

import httpx
from btg_api_utils import BTGAPIError


def validate_response(
    response: httpx.Response, required_keys: list[str]
) -> dict[str, Any]:
    if response.status_code not in (200, 202):
        try:
            body = response.json()
        except Exception:
            body = {"message": response.text}
        raise BTGAPIError(
            message=f"BTG API Error (HTTP {response.status_code})",
            status_code=response.status_code,
            response_body=body,
        )
    if response.status_code == 202:
        return {}
    try:
        data: dict[str, Any] = response.json()
    except Exception as exc:
        raise BTGAPIError(
            message="Invalid JSON in response body",
            status_code=response.status_code,
        ) from exc
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise BTGAPIError(
            message=f"Response missing required keys: {', '.join(missing)}",
            status_code=response.status_code,
            response_body=data,
        )
    return data
