"""Table formatting utilities."""

from __future__ import annotations

from typing import Any

import pandas as pd


def format_fundamentals_table(fundamentals: dict[str, Any]) -> str:
    """Format fundamentals as a clean text table."""
    df = pd.DataFrame([fundamentals]).T
    df.columns = ["Value"]
    return df.to_string()


def format_prices_summary(prices: pd.DataFrame, symbol: str) -> str:
    """Format price summary statistics."""
    if prices.empty:
        return "No price data available."

    summary = {
        "Symbol": symbol,
        "Start Date": prices.index[0].strftime("%Y-%m-%d"),
        "End Date": prices.index[-1].strftime("%Y-%m-%d"),
        "Rows": len(prices),
    }

    if "Close" in prices.columns:
        summary.update({
            "Close (Latest)": prices["Close"].iloc[-1],
            "Close (Min)": prices["Close"].min(),
            "Close (Max)": prices["Close"].max(),
            "Close (Mean)": float(prices["Close"].mean()),
        })

    df = pd.DataFrame(summary, index=[0]).T
    df.columns = [""]
    return df.to_string()
