"""
BTG Pactual API Utilities

Shared utilities for BTG Pactual API clients.
"""

from __future__ import annotations

import uuid
from typing import Any, TypedDict, NotRequired

import httpx

from btg_api_auth import get_access_token


# =============================================================================
# Type Definitions - Error Types
# =============================================================================

class Error(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]


class ErrorMetadata(TypedDict):
    globalErrors: NotRequired[list[Error]]
    fieldErrors: NotRequired[dict]


class ResponseError(TypedDict):
    status: NotRequired[int]
    title: NotRequired[str]
    meta: NotRequired[ErrorMetadata]


# =============================================================================
# Exceptions
# =============================================================================

class BTGAPIError(Exception):
    """Exception raised when BTG API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict | None = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


# =============================================================================
# Header Utilities
# =============================================================================

def build_headers(**extra_headers: str) -> dict[str, str]:
    """
    Build required headers for API requests.

    Args:
        **extra_headers: Additional headers to include in the request

    Returns:
        Dictionary of headers including access_token, x-id-partner-request,
        Content-Type, and any extra headers provided
    """
    headers = {
        "access_token": get_access_token(),
        "x-id-partner-request": str(uuid.uuid4()),
        "Content-Type": "application/json",
    }
    headers.update(extra_headers)
    return headers


# =============================================================================
# Response Handling
# =============================================================================

def handle_response(response: httpx.Response) -> Any:
    """
    Handle API response and raise appropriate errors.

    Args:
        response: The httpx Response object

    Returns:
        Parsed JSON response for successful requests, empty dict for 202

    Raises:
        BTGAPIError: If the API returns an error status code
    """
    if response.status_code in (200, 202):
        if response.status_code == 202:
            return {}
        try:
            return response.json()
        except Exception:
            return {}

    try:
        error_body: dict[str, Any] = response.json()
    except Exception:
        error_body = {"message": response.text}

    error_message = f"BTG API Error (HTTP {response.status_code})"

    if "errors" in error_body and error_body["errors"]:
        error_message = error_body["errors"][0].get("message", error_message)
    elif "meta" in error_body and "globalErrors" in error_body.get("meta", {}):
        global_errors = error_body["meta"]["globalErrors"]
        if global_errors:
            error_message = global_errors[0].get("message", error_message)
    elif "message" in error_body:
        error_message = error_body["message"]

    raise BTGAPIError(
        message=error_message,
        status_code=response.status_code,
        response_body=error_body
    )


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Error Types
    "Error",
    "ErrorMetadata",
    "ResponseError",
    # Exceptions
    "BTGAPIError",
    # Functions
    "build_headers",
    "handle_response",
]
