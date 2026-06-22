from __future__ import annotations

from typing import Any

import pandas as pd
import yfinance as yf


def fetch_price_history(symbol: str, start: str, end: str, source: str = "yahoo") -> pd.DataFrame:
    """Fetch historical price data for a ticker symbol."""
    if source.lower() != "yahoo":
        raise ValueError("Only the 'yahoo' source is supported in Phase 1.")

    data = yf.download(symbol, start=start, end=end, progress=False)
    if data is None or data.empty:
        raise RuntimeError(f"No historical price data available for {symbol}.")

    return data


def fetch_company_fundamentals(symbol: str, source: str = "yahoo") -> dict[str, Any]:
    """Fetch company fundamentals for a ticker symbol."""
    if source.lower() != "yahoo":
        raise ValueError("Only the 'yahoo' source is supported in Phase 1.")

    ticker = yf.Ticker(symbol)
    info = ticker.info or {}
    if not info:
        raise RuntimeError(f"No fundamentals available for {symbol}.")

    return {
        "symbol": symbol,
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "dividendYield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "fullTimeEmployees": info.get("fullTimeEmployees"),
    }
