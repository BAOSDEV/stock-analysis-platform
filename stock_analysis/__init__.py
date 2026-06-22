"""Stock analysis platform package."""

from .data import fetch_company_fundamentals, fetch_price_history

__all__ = ["fetch_company_fundamentals", "fetch_price_history"]
