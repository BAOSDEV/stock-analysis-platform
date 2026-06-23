from __future__ import annotations

import logging
from typing import Any

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)
SUPPORTED_SOURCE = "yahoo"


def _validate_source(source: str) -> None:
    """Validate that the source is supported."""
    if source.lower() != SUPPORTED_SOURCE:
        raise ValueError(f"Only the '{SUPPORTED_SOURCE}' source is supported in Phase 1.")


def fetch_price_history(symbol: str, start: str, end: str, source: str = "yahoo") -> pd.DataFrame:
    """Fetch historical price data for a ticker symbol.
    
    Args:
        symbol: Ticker symbol (e.g., 'RELIANCE.NS', 'MSFT')
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        source: Data source (only 'yahoo' supported in Phase 1)
        
    Returns:
        DataFrame with OHLCV data indexed by date
        
    Raises:
        ValueError: If source is not 'yahoo'
        RuntimeError: If no data is available
    """
    _validate_source(source)

    logger.debug(f"Downloading {symbol} from {start} to {end}")
    data = yf.download(symbol, start=start, end=end, progress=False)
    if data is None or data.empty:
        raise RuntimeError(f"No historical price data available for {symbol} ({start} to {end}).")

    logger.debug(f"Downloaded {len(data)} records for {symbol}")
    return data


def fetch_company_fundamentals(symbol: str, source: str = "yahoo") -> dict[str, Any]:
    """Fetch company fundamentals for a ticker symbol.
    
    Args:
        symbol: Ticker symbol (e.g., 'RELIANCE.NS', 'MSFT')
        source: Data source (only 'yahoo' supported in Phase 1)
        
    Returns:
        Dictionary with company fundamentals
        
    Raises:
        ValueError: If source is not 'yahoo'
        RuntimeError: If no fundamentals data is available
    """
    _validate_source(source)

    logger.debug(f"Fetching fundamentals for {symbol}")
    ticker = yf.Ticker(symbol)
    info = ticker.info or {}
    if not info:
        raise RuntimeError(f"No fundamentals available for {symbol}. Symbol may be invalid.")

    logger.debug(f"Retrieved {len(info)} fields for {symbol}")
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
