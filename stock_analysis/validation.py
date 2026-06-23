"""Input validation utilities."""

from __future__ import annotations

from datetime import datetime


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> datetime:
    """Validate and parse a date string."""
    try:
        return datetime.strptime(date_str, format)
    except ValueError as e:
        raise ValueError(f"Invalid date '{date_str}'. Expected format: {format}") from e


def validate_symbol(symbol: str) -> str:
    """Validate a ticker symbol.

    Allows reasonably long tickers including exchange suffixes (e.g. RELIANCE.NS).
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")
    if len(symbol) > 12:
        raise ValueError("Symbol must be 12 characters or less.")
    return symbol.strip().upper()
