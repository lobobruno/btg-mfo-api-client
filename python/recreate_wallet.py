"""
Wallet Position Reconstruction

Reconstructs a client's portfolio position from BTG Position API response
into a unified Pandas DataFrame with all asset classes.

Usage:
    from recreate_wallet import recreate_wallet, get_wallet_summary

    # Get position data
    response = get_position_by_account_and_date("004209281", "2025-12-31")

    # Recreate wallet as DataFrame
    wallet_df = recreate_wallet(response)

    # Get summary by asset class
    summary_df = get_wallet_summary(wallet_df)
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

import pandas as pd

from btg_api_position import get_position_by_account_and_date


# =============================================================================
# Constants
# =============================================================================

MARKET_MAPPING = {
    "InvestmentFund": "FN",  # Fundos de Investimento
    "FixedIncome": "RF",      # Renda Fixa
    "Pension": "PREV",        # Previdência
    "Equities": "RV",         # Renda Variável
    "Cash": "CC",             # Conta Corrente
}

COLUMNS = [
    "asset_name",
    "asset_type",
    "market_class",
    "ticker",
    "cnpj",
    "quantity",
    "avg_price",
    "current_price",
    "cost_value",
    "gross_value",
    "net_value",
    "income_tax",
    "iof_tax",
    "portfolio_pct",
    "first_acquisition",
    "last_acquisition",
    "maturity_date",
    "indexador",
    "yield_rate",
    "benchmark",
    "liquidity_days",
    "issuer",
    "position_date",
]


# =============================================================================
# Parsing Functions
# =============================================================================

def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _safe_date(value: Any) -> str | None:
    """Safely parse a date string to YYYY-MM-DD format."""
    if not value:
        return None
    try:
        # Handle various date formats
        date_str = str(value)
        if "T" in date_str:
            date_str = date_str.split("T")[0]
        return date_str
    except Exception:
        return None


def _parse_investment_funds(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse InvestmentFund positions."""
    funds = data.get("InvestmentFund", []) or []
    rows = []

    for fund in funds:
        fund_info = fund.get("Fund", {})
        acquisitions = fund.get("Acquisition", []) or []

        # Calculate totals from acquisitions
        total_shares = sum(_safe_float(a.get("NumberOfShares")) for a in acquisitions)
        total_gross = sum(_safe_float(a.get("GrossAssetValue")) for a in acquisitions)
        total_net = sum(_safe_float(a.get("NetAssetValue")) for a in acquisitions)
        total_cost = sum(_safe_float(a.get("CostValue")) for a in acquisitions)
        total_tax = sum(_safe_float(a.get("IncomeTax")) for a in acquisitions)
        total_iof = sum(_safe_float(a.get("VirtualIOF")) for a in acquisitions)

        # Get acquisition dates
        acq_dates = [_safe_date(a.get("AcquisitionDate")) for a in acquisitions]
        acq_dates = [d for d in acq_dates if d]

        # Calculate weighted average cost price
        avg_price = total_cost / total_shares if total_shares > 0 else 0.0

        rows.append({
            "asset_name": fund_info.get("FundName", ""),
            "asset_type": "InvestmentFund",
            "market_class": "FN",
            "ticker": None,
            "cnpj": fund_info.get("FundCNPJCode"),
            "quantity": total_shares,
            "avg_price": avg_price,
            "current_price": _safe_float(fund.get("ShareValue")),
            "cost_value": total_cost,
            "gross_value": total_gross,
            "net_value": total_net,
            "income_tax": total_tax,
            "iof_tax": total_iof,
            "portfolio_pct": 0.0,  # Will be calculated later
            "first_acquisition": min(acq_dates) if acq_dates else None,
            "last_acquisition": max(acq_dates) if acq_dates else None,
            "maturity_date": None,
            "indexador": None,
            "yield_rate": None,
            "benchmark": fund_info.get("BenchMark"),
            "liquidity_days": _safe_float(fund_info.get("FundLiquidity")),
            "issuer": fund_info.get("ManagerName"),
            "position_date": _safe_date(fund.get("PositionDate")),
        })

    return rows


def _parse_fixed_income(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse FixedIncome positions."""
    fixed_income = data.get("FixedIncome", []) or []
    rows = []

    for asset in fixed_income:
        acquisitions = asset.get("Acquisitions", []) or []

        # Get acquisition dates
        acq_dates = [_safe_date(a.get("AcquisitionDate")) for a in acquisitions]
        acq_dates = [d for d in acq_dates if d]

        # Calculate weighted average cost price
        total_qty = _safe_float(asset.get("Quantity"))
        total_cost = sum(_safe_float(a.get("InitialInvestmentValue")) for a in acquisitions)
        avg_price = total_cost / total_qty if total_qty > 0 else 0.0

        rows.append({
            "asset_name": asset.get("Ticker", "") + " - " + (asset.get("Issuer", "") or ""),
            "asset_type": "FixedIncome",
            "market_class": "RF",
            "ticker": asset.get("Ticker"),
            "cnpj": None,
            "quantity": total_qty,
            "avg_price": avg_price,
            "current_price": _safe_float(asset.get("Price")),
            "cost_value": total_cost,
            "gross_value": _safe_float(asset.get("GrossValue")),
            "net_value": _safe_float(asset.get("NetValue")),
            "income_tax": _safe_float(asset.get("IncomeTax")),
            "iof_tax": _safe_float(asset.get("IOFTax")),
            "portfolio_pct": 0.0,
            "first_acquisition": min(acq_dates) if acq_dates else None,
            "last_acquisition": max(acq_dates) if acq_dates else None,
            "maturity_date": _safe_date(asset.get("MaturityDate")),
            "indexador": asset.get("ReferenceIndexName"),
            "yield_rate": asset.get("IndexYieldRate"),
            "benchmark": None,
            "liquidity_days": None,
            "issuer": asset.get("Issuer"),
            "position_date": None,
        })

    return rows


def _parse_pension(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse PensionInformations positions."""
    pensions = data.get("PensionInformations", []) or []
    rows = []

    for pension in pensions:
        positions = pension.get("Positions", []) or []

        for pos in positions:
            rows.append({
                "asset_name": pos.get("FundName", ""),
                "asset_type": "Pension",
                "market_class": "PREV",
                "ticker": None,
                "cnpj": pos.get("PensionCnpjCode"),
                "quantity": _safe_float(pos.get("NumberOfShares")),
                "avg_price": _safe_float(pos.get("AssetCostPrice")) / _safe_float(pos.get("NumberOfShares")) if _safe_float(pos.get("NumberOfShares")) > 0 else 0.0,
                "current_price": _safe_float(pos.get("ShareValue")),
                "cost_value": _safe_float(pos.get("AssetCostPrice")),
                "gross_value": _safe_float(pos.get("GrossAssetValue")),
                "net_value": _safe_float(pos.get("NetAssetValue")),
                "income_tax": sum(_safe_float(ir.get("IR")) for ir in pos.get("IrAliquots", []) or []),
                "iof_tax": 0.0,
                "portfolio_pct": 0.0,
                "first_acquisition": _safe_date(pension.get("FirstContributionDate")),
                "last_acquisition": _safe_date(pension.get("StartDate")),
                "maturity_date": None,
                "indexador": None,
                "yield_rate": None,
                "benchmark": None,
                "liquidity_days": None,
                "issuer": pension.get("FundType"),  # VGBL, PGBL
                "position_date": _safe_date(pos.get("PositionDate")),
            })

    return rows


def _parse_equities(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse Equities positions (stocks and FIIs)."""
    equities = data.get("Equities", []) or []
    rows = []

    for equity in equities:
        stocks = equity.get("StockPositions", []) or []

        for stock in stocks:
            avg_price_info = stock.get("AveragePrice", {}) or {}

            rows.append({
                "asset_name": stock.get("Description", ""),
                "asset_type": "FII" if stock.get("IsFII") == "true" else "Equity",
                "market_class": "RV",
                "ticker": stock.get("Ticker"),
                "cnpj": None,
                "quantity": _safe_float(stock.get("Quantity")),
                "avg_price": _safe_float(avg_price_info.get("Price")),
                "current_price": _safe_float(stock.get("MarketPrice")),
                "cost_value": _safe_float(stock.get("InitialInvestimentValue")),
                "gross_value": _safe_float(stock.get("GrossValue")),
                "net_value": _safe_float(stock.get("GrossValue")) - _safe_float(stock.get("IncomeTax")),
                "income_tax": _safe_float(stock.get("IncomeTax")),
                "iof_tax": 0.0,
                "portfolio_pct": 0.0,
                "first_acquisition": _safe_date(stock.get("FirstDealingDate")),
                "last_acquisition": None,
                "maturity_date": None,
                "indexador": None,
                "yield_rate": None,
                "benchmark": None,
                "liquidity_days": None,
                "issuer": stock.get("SectorDescription"),
                "position_date": _safe_date(stock.get("InterfaceDate")),
            })

    return rows


def _parse_cash(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse Cash positions (current account and invested cash)."""
    cash_data = data.get("Cash", []) or []
    rows = []

    for cash in cash_data:
        # Current Account
        current_account = cash.get("CurrentAccount", {}) or {}
        if _safe_float(current_account.get("Value")) > 0:
            rows.append({
                "asset_name": "Conta Corrente",
                "asset_type": "Cash",
                "market_class": "CC",
                "ticker": None,
                "cnpj": None,
                "quantity": 1.0,
                "avg_price": _safe_float(current_account.get("Value")),
                "current_price": _safe_float(current_account.get("Value")),
                "cost_value": _safe_float(current_account.get("Value")),
                "gross_value": _safe_float(current_account.get("Value")),
                "net_value": _safe_float(current_account.get("Value")),
                "income_tax": 0.0,
                "iof_tax": 0.0,
                "portfolio_pct": 0.0,
                "first_acquisition": None,
                "last_acquisition": None,
                "maturity_date": None,
                "indexador": None,
                "yield_rate": None,
                "benchmark": None,
                "liquidity_days": 0,
                "issuer": "BTG Pactual",
                "position_date": _safe_date(current_account.get("PositionDate")),
            })

        # Invested Cash (CDIE)
        cash_invested = cash.get("CashInvested", []) or []
        for inv in cash_invested:
            name_info = inv.get("Name", {}) or {}

            rows.append({
                "asset_name": f"Caixa Investido - {name_info.get('Nome', 'CDIE')}",
                "asset_type": "CashInvested",
                "market_class": "CC",
                "ticker": name_info.get("CodAtivo"),
                "cnpj": None,
                "quantity": _safe_float(inv.get("Quantity")),
                "avg_price": _safe_float(inv.get("CostPrice")),
                "current_price": _safe_float(inv.get("GrossValue")) / _safe_float(inv.get("Quantity")) if _safe_float(inv.get("Quantity")) > 0 else 0.0,
                "cost_value": _safe_float(inv.get("Quantity")) * _safe_float(inv.get("CostPrice")),
                "gross_value": _safe_float(inv.get("GrossValue")),
                "net_value": _safe_float(inv.get("NetValue")),
                "income_tax": _safe_float(inv.get("IncomeTax")),
                "iof_tax": _safe_float(inv.get("IofTax")),
                "portfolio_pct": 0.0,
                "first_acquisition": _safe_date(inv.get("AcquisitionDate")),
                "last_acquisition": _safe_date(inv.get("AcquisitionDate")),
                "maturity_date": _safe_date(inv.get("MaturityDate")),
                "indexador": name_info.get("Indexador"),
                "yield_rate": None,
                "benchmark": None,
                "liquidity_days": 0,
                "issuer": "BTG Pactual",
                "position_date": None,
            })

    return rows


# =============================================================================
# Main Functions
# =============================================================================

def recreate_wallet(response: dict[str, Any]) -> pd.DataFrame:
    """
    Recreate the client's wallet position as a Pandas DataFrame.

    Args:
        response: The response from get_position_by_account_and_date()

    Returns:
        DataFrame with unified portfolio positions
    """
    all_rows = []

    # Parse each asset type
    all_rows.extend(_parse_investment_funds(response))
    all_rows.extend(_parse_fixed_income(response))
    all_rows.extend(_parse_pension(response))
    all_rows.extend(_parse_equities(response))
    all_rows.extend(_parse_cash(response))

    # Create DataFrame
    df = pd.DataFrame(all_rows)
    # Ensure all columns exist
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[COLUMNS]

    # Calculate portfolio percentages
    total_gross = df["gross_value"].sum()
    if total_gross > 0:
        df["portfolio_pct"] = (df["gross_value"] / total_gross * 100).round(4)

    # Sort by gross value descending
    df = df.sort_values("gross_value", ascending=False).reset_index(drop=True)

    return df


def get_wallet_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a summary of the wallet by market class.

    Args:
        df: The wallet DataFrame from recreate_wallet()

    Returns:
        Summary DataFrame grouped by market class
    """
    summary = df.groupby("market_class").agg({
        "gross_value": "sum",
        "net_value": "sum",
        "cost_value": "sum",
        "income_tax": "sum",
        "asset_name": "count",
    })
    summary = summary.rename(columns={"asset_name": "num_assets"})

    # Calculate percentages
    total = summary["gross_value"].sum()
    summary["portfolio_pct"] = (summary["gross_value"] / total * 100).round(2)

    # Calculate P&L
    summary["pnl"] = summary["gross_value"] - summary["cost_value"]
    summary["pnl_pct"] = ((summary["gross_value"] / summary["cost_value"] - 1) * 100).round(2)

    # Rename market classes for readability
    market_names = {
        "CC": "Conta Corrente",
        "RF": "Renda Fixa",
        "RV": "Renda Variável",
        "FN": "Fundos de Investimento",
        "PREV": "Previdência",
    }
    summary.index = summary.index.map(lambda x: market_names.get(x, x))

    return summary.sort_values("gross_value", ascending=False)


def get_wallet_by_asset_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a summary of the wallet by asset type.

    Args:
        df: The wallet DataFrame from recreate_wallet()

    Returns:
        Summary DataFrame grouped by asset type
    """
    summary = df.groupby("asset_type").agg({
        "gross_value": "sum",
        "net_value": "sum",
        "cost_value": "sum",
        "income_tax": "sum",
        "asset_name": "count",
    })
    summary = summary.rename(columns={"asset_name": "num_assets"})

    # Calculate percentages
    total = summary["gross_value"].sum()
    summary["portfolio_pct"] = (summary["gross_value"] / total * 100).round(2)

    return summary.sort_values("gross_value", ascending=False)


def format_wallet_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the wallet DataFrame for display with formatted numbers.

    Args:
        df: The wallet DataFrame from recreate_wallet()

    Returns:
        Formatted DataFrame for display
    """
    display_df = df.copy()

    # Format currency columns
    currency_cols = ["avg_price", "current_price", "cost_value", "gross_value", "net_value", "income_tax"]
    for col in currency_cols:
        display_df[col] = display_df[col].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) else "-")

    # Format percentage
    display_df["portfolio_pct"] = display_df["portfolio_pct"].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")

    # Format quantity
    display_df["quantity"] = display_df["quantity"].apply(lambda x: f"{x:,.6f}" if pd.notna(x) else "-")

    return display_df


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    import json

    # Option 1: Load from JSON file (for testing)
    response: dict[str, Any]
    try:
        with open("get_position_by_account_and_date.json", "r") as f:
            response = json.load(f)
        print("Loaded from JSON file")
    except FileNotFoundError:
        # Option 2: Fetch from API
        print("Fetching from API...")
        response = dict(get_position_by_account_and_date("004209281", "2025-12-31"))

    # Recreate wallet
    wallet_df = recreate_wallet(response)

    # Display results
    print("\n" + "=" * 80)
    print("PORTFOLIO SUMMARY BY MARKET CLASS")
    print("=" * 80)
    summary = get_wallet_summary(wallet_df)
    print(summary.to_string())

    print("\n" + "=" * 80)
    print("PORTFOLIO SUMMARY BY ASSET TYPE")
    print("=" * 80)
    by_type = get_wallet_by_asset_type(wallet_df)
    print(by_type.to_string())

    print("\n" + "=" * 80)
    print("TOP 10 POSITIONS BY VALUE")
    print("=" * 80)
    top_10 = wallet_df.head(10)[["asset_name", "market_class", "gross_value", "portfolio_pct"]]
    print(top_10.to_string())

    print("\n" + "=" * 80)
    print(f"TOTAL PORTFOLIO VALUE: R$ {wallet_df['gross_value'].sum():,.2f}")
    print(f"TOTAL POSITIONS: {len(wallet_df)}")
    print("=" * 80)

    # Export to CSV
    wallet_df.to_csv("wallet_positions.csv", index=False)
    print("\nExported to wallet_positions.csv")
