"""
BTG Pactual Operation API Client

A typed Python client for the BTG Pactual Operation API.
Each endpoint is exposed as an individual function that can be imported separately.

Configuration via environment variables:
    BTG_CLIENT_ID: OAuth2 client ID (required)
    BTG_CLIENT_SECRET: OAuth2 client secret (required)

Usage:
    from btg_api_operation import get_movements_by_account_full
    get_movements_by_account_full("001234567")
"""

from __future__ import annotations

from typing import TypedDict

import httpx

from btg_api_utils import build_headers, handle_response

# =============================================================================
# Configuration
# =============================================================================

BASE_URL = "https://api.btgpactual.com/iaas-api-operation"
DEFAULT_TIMEOUT = 30.0


# =============================================================================
# Type Definitions - Request Types
# =============================================================================

class OperationHistoryPartnerRequest(TypedDict):
    """Request body for movements by partner and period query."""
    monthRef: str  # Format: "yyyy-MM"


# =============================================================================
# API Functions - By Account
# =============================================================================

def get_movements_by_account_full(
    account_number: str,
    fetch_current_account: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Get all movements for an account since inception.

    This is an asynchronous call. Response will be delivered via webhook
    (operations-by-account). Data is cached for 12 hours.

    Args:
        account_number: Account number to query (e.g., "001234567")
        fetch_current_account: Whether to include current account info (default: True)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/operation-history/full/{account_number}"
    headers = build_headers(fetch_current_account="no_value") if fetch_current_account else build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


def get_movements_by_account_monthly(
    account_number: str,
    fetch_current_account: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Get movements for an account for the last month plus current month.

    This report can bring up to D-60, depending on the day of the request.
    This is an asynchronous call. Response will be delivered via webhook
    (operations-by-account). Data is cached for 12 hours.

    Args:
        account_number: Account number to query (e.g., "001234567")
        fetch_current_account: Whether to include current account info (default: True)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/operation-history/monthly/{account_number}"
    headers = build_headers(fetch_current_account="no_value") if fetch_current_account else build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


def get_movements_by_account_weekly(
    account_number: str,
    fetch_current_account: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Get movements for an account for the last 7 days.

    This is an asynchronous call. Response will be delivered via webhook
    (operations-by-account). Data is cached for 12 hours.

    Args:
        account_number: Account number to query (e.g., "001234567")
        fetch_current_account: Whether to include current account info (default: True)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/operation-history/weekly/{account_number}"
    headers = build_headers(fetch_current_account="no_value") if fetch_current_account else build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


# =============================================================================
# API Functions - By Partner
# =============================================================================

def get_movements_by_partner_and_period(
    month_ref: str,
    fetch_current_account: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Get movements for all partner accounts for a specific month.

    The period must be before the first day of the previous month.
    This is an asynchronous call. Response will be delivered via webhook
    (operations-by-partner). Data is cached for 12 hours.

    Note: Does not include Fund-type accounts, only Investment-type accounts.

    Args:
        month_ref: Reference month in format "yyyy-MM" (e.g., "2024-12")
        fetch_current_account: Whether to include current account info (default: True)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/operation-history/period"
    headers = build_headers(fetch_current_account="no_value") if fetch_current_account else build_headers()
    body: OperationHistoryPartnerRequest = {"monthRef": month_ref}

    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, headers=headers, json=body)
        handle_response(response)


def get_movements_by_partner_monthly(
    fetch_current_account: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Get movements for all partner accounts for the last month plus current month.

    This report can bring up to D-60, depending on the day of the request.
    This is an asynchronous call. Response will be delivered via webhook
    (operations-by-partner). Data is cached for 12 hours.

    Args:
        fetch_current_account: Whether to include current account info (default: True)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/operation-history/monthly"
    headers = build_headers(fetch_current_account="no_value") if fetch_current_account else build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


def get_movements_by_partner_weekly(
    fetch_current_account: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    """
    Get movements for all partner accounts for the last 7 days.

    This is an asynchronous call. Response will be delivered via webhook
    (operations-by-partner). Data is cached for 12 hours.

    Args:
        fetch_current_account: Whether to include current account info (default: True)
        timeout: Request timeout in seconds

    Raises:
        BTGAPIError: If the API returns an error
    """
    url = f"{BASE_URL}/api/v1/operation-history/weekly"
    headers = build_headers(fetch_current_account="no_value") if fetch_current_account else build_headers()

    with httpx.Client(timeout=timeout) as client:
        response = client.get(url, headers=headers)
        handle_response(response)


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Configuration
    "BASE_URL",
    # Request Types
    "OperationHistoryPartnerRequest",
    # API Functions - By Account
    "get_movements_by_account_full",
    "get_movements_by_account_monthly",
    "get_movements_by_account_weekly",
    # API Functions - By Partner
    "get_movements_by_partner_and_period",
    "get_movements_by_partner_monthly",
    "get_movements_by_partner_weekly",
]
