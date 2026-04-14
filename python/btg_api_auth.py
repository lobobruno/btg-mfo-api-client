"""
BTG Pactual Auth API Client

A typed Python client for the BTG Pactual Authorization API.
Generates OAuth2 access tokens using client credentials.

Configuration via environment variables:
    BTG_CLIENT_ID: OAuth2 client ID (required)
    BTG_CLIENT_SECRET: OAuth2 client secret (required)

Usage:
    from btg_api_auth import get_access_token
    token = get_access_token()
"""

from __future__ import annotations

import base64
import os
import uuid
from typing import TypedDict

import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# Configuration
# =============================================================================

BASE_URL = "https://api.btgpactual.com/iaas-auth"
DEFAULT_TIMEOUT = 30.0
TOKEN_VALIDITY_SECONDS = 15 * 60  # 15 minutes

# Environment variables
BTG_CLIENT_ID = os.getenv("BTG_CLIENT_ID")
BTG_CLIENT_SECRET = os.getenv("BTG_CLIENT_SECRET")

# Token cache
_cached_token: str | None = None
_token_expiry: float = 0


# =============================================================================
# Exceptions
# =============================================================================

class BTGAuthError(Exception):
    """Exception raised when BTG Auth API returns an error."""

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
# Type Definitions
# =============================================================================

class TokenResponse(TypedDict):
    """Response from the token endpoint."""
    access_token: str
    token_type: str
    expires_in: int


# =============================================================================
# Internal Utilities
# =============================================================================

def _get_credentials() -> tuple[str, str]:
    """Get client credentials from environment variables."""
    if not BTG_CLIENT_ID:
        raise BTGAuthError(
            "Client ID is required. Set BTG_CLIENT_ID environment variable."
        )
    if not BTG_CLIENT_SECRET:
        raise BTGAuthError(
            "Client secret is required. Set BTG_CLIENT_SECRET environment variable."
        )
    return BTG_CLIENT_ID, BTG_CLIENT_SECRET


def _build_basic_auth_header() -> str:
    """Build Basic Authorization header from client credentials."""
    client_id, client_secret = _get_credentials()
    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def _build_headers() -> dict[str, str]:
    """Build required headers for auth API requests."""
    return {
        "Authorization": _build_basic_auth_header(),
        "x-id-partner-request": str(uuid.uuid4()),
        "Content-Type": "application/x-www-form-urlencoded",
    }


# =============================================================================
# API Functions
# =============================================================================

def get_access_token(
    timeout: float = DEFAULT_TIMEOUT,
    use_cache: bool = True,
) -> str:
    """
    Generate an OAuth2 access token using client credentials.

    The token is valid for 15 minutes and is cached by default.

    Args:
        timeout: Request timeout in seconds
        use_cache: Whether to use cached token if available (default: True)

    Returns:
        Access token string

    Raises:
        BTGAuthError: If the API returns an error
    """
    import time

    global _cached_token, _token_expiry

    # Return cached token if still valid
    if use_cache and _cached_token and time.time() < _token_expiry:
        return _cached_token

    url = f"{BASE_URL}/api/v1/authorization/oauth2/accesstoken"
    headers = _build_headers()
    body = "grant_type=client_credentials"

    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, headers=headers, content=body)

        if response.status_code == 200:
            # Token is in the response header
            token = response.headers.get("access_token")
            if token:
                # Cache the token
                _cached_token = token
                _token_expiry = time.time() + TOKEN_VALIDITY_SECONDS - 60  # 1 min buffer
                return token

            # Try response body as fallback
            try:
                data = response.json()
                if "access_token" in data:
                    token = data["access_token"]
                    _cached_token = token
                    _token_expiry = time.time() + TOKEN_VALIDITY_SECONDS - 60
                    return token
            except Exception:
                pass

            raise BTGAuthError(
                "Access token not found in response",
                status_code=response.status_code
            )

        # Handle errors
        try:
            error_body = response.json()
        except Exception:
            error_body = {"message": response.text}

        error_message = f"BTG Auth API Error (HTTP {response.status_code})"
        if "message" in error_body:
            error_message = error_body["message"]

        raise BTGAuthError(
            message=error_message,
            status_code=response.status_code,
            response_body=error_body
        )


def clear_token_cache() -> None:
    """Clear the cached access token."""
    global _cached_token, _token_expiry
    _cached_token = None
    _token_expiry = 0


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Exceptions
    "BTGAuthError",
    # Types
    "TokenResponse",
    # Functions
    "get_access_token",
    "clear_token_cache",
]
