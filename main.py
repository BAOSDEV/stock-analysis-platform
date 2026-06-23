from __future__ import annotations

import argparse
import sys
from typing import Sequence

from stock_analysis.data import fetch_company_fundamentals, fetch_price_history
from stock_analysis.formatter import format_fundamentals_table, format_prices_summary
from stock_analysis.logging_config import get_logger, setup_logging
from stock_analysis.validation import validate_date, validate_symbol

logger = get_logger(__name__)
DEFAULT_SYMBOLS = ["RELIANCE.NS", "500325.BO", "MSFT", "NVDA"]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="stock-analysis-platform Phase 1 data fetcher")
    parser.add_argument("--symbol", "-s", help="Ticker symbol to fetch (comma-separated for batch)")
    parser.add_argument("--start", default="2024-01-01", help="Historical start date in YYYY-MM-DD format")
    parser.add_argument("--end", default="2024-12-31", help="Historical end date in YYYY-MM-DD format")
    parser.add_argument("--show-defaults", action="store_true", help="Print supported default symbols and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
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


def fetch_and_report(symbol: str, start: str, end: str) -> bool:
    """Fetch and display data for a single symbol. Returns success status."""
    try:
        symbol = validate_symbol(symbol)
        validate_date(start)
        validate_date(end)
        
        logger.info(f"Fetching fundamentals for {symbol}")
        fundamentals = fetch_company_fundamentals(symbol)
        logger.debug(f"Received fundamentals: {fundamentals}")
        
        logger.info(f"Fetching price history for {symbol}")
        prices = fetch_price_history(symbol, start=start, end=end)
        logger.debug(f"Received {len(prices)} price records")
        
        print(f"\n{'='*60}")
        print(f"SYMBOL: {symbol}")
        print(f"{'='*60}")
        print("\nFundamentals:")
        print(format_fundamentals_table(fundamentals))
        print("\nPrice Summary:")
        print(format_prices_summary(prices, symbol))
        print()
        return True
    except Exception as e:
        logger.error(f"Error processing {symbol}: {e}")
        return False


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    setup_logging(verbose=args.verbose)
    
    logger.info("stock-analysis-platform Phase 1: Data Fetcher")

    if args.show_defaults:
        print("Supported default symbols:")
        for symbol in DEFAULT_SYMBOLS:
            print(f" - {symbol}")
        return

    symbol_input = choose_symbol(args.symbol)
    symbols = [s.strip() for s in symbol_input.split(",")]
    
    success_count = 0
    for symbol in symbols:
        if fetch_and_report(symbol, args.start, args.end):
            success_count += 1
    
    logger.info(f"Successfully processed {success_count}/{len(symbols)} symbols")
    if success_count < len(symbols):
        sys.exit(1)


if __name__ == "__main__":
    main()
