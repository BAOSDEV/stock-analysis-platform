"""Table formatting utilities."""

from __future__ import annotations

from typing import Any

import pandas as pd


def format_fundamentals_table(fundamentals: dict[str, Any]) -> str:
    """Format fundamentals as a clean text table."""
    df = pd.Series(fundamentals).to_frame(name="Value")
    return df.to_string()


def format_prices_summary(prices: pd.DataFrame, symbol: str) -> str:
    """Format price summary statistics."""
    if prices.empty:
        return "No price data available."

    close_col = prices.get("Close")
    summary = {
        "Symbol": symbol,
        "Start Date": prices.index[0].strftime("%Y-%m-%d"),
        "End Date": prices.index[-1].strftime("%Y-%m-%d"),
        "Rows": len(prices),
    }

    if close_col is not None:
        summary.update({
            "Close (Latest)": close_col.iloc[-1],
            "Close (Min)": close_col.min(),
            "Close (Max)": close_col.max(),
            "Close (Mean)": float(close_col.mean()),
        })

    series = pd.Series(summary, name="")
    return series.to_string()
