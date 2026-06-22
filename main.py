from __future__ import annotations

import argparse
from typing import Sequence

from stock_analysis.data import fetch_company_fundamentals, fetch_price_history
from stock_analysis.report.summary import generate_summary

DEFAULT_SYMBOLS = ["RELIANCE.NS", "500325.BO", "MSFT", "NVDA"]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="stock-analysis-platform Phase 1 data fetcher")
    parser.add_argument("--symbol", "-s", help="Ticker symbol to fetch")
    parser.add_argument("--start", default="2024-01-01", help="Historical start date in YYYY-MM-DD format")
    parser.add_argument("--end", default="2024-12-31", help="Historical end date in YYYY-MM-DD format")
    parser.add_argument("--show-defaults", action="store_true", help="Print supported default symbols and exit")
    return parser.parse_args(argv)


def choose_symbol(symbol: str | None) -> str:
    if symbol:
        return symbol

    print("No symbol provided. Choose a default symbol or enter a custom ticker:")
    for index, default_symbol in enumerate(DEFAULT_SYMBOLS, start=1):
        print(f"  {index}. {default_symbol}")

    choice = input("Enter ticker or number [1]: ").strip()
    if not choice:
        return DEFAULT_SYMBOLS[0]
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(DEFAULT_SYMBOLS):
            return DEFAULT_SYMBOLS[index]

    return choice


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    if args.show_defaults:
        print("Supported default symbols:")
        for symbol in DEFAULT_SYMBOLS:
            print(f" - {symbol}")
        return

    symbol = choose_symbol(args.symbol)
    print("stock-analysis-platform Phase 1: Data Fetcher")
    print(f"Fetching data for {symbol}")

    fundamentals = fetch_company_fundamentals(symbol)
    print("Fundamentals:")
    print(generate_summary(fundamentals))

    prices = fetch_price_history(symbol, start=args.start, end=args.end)
    print(f"Fetched {len(prices)} historical rows for {symbol}.")


if __name__ == "__main__":
    main()
