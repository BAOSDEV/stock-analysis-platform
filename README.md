# stock-analysis-platform

A minimal stock analysis platform with Phase 1 support for historical prices and company fundamentals via Yahoo Finance.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run with default prompt:

```bash
python main.py
```

Run with a specific symbol:

```bash
python main.py --symbol RELIANCE.NS
python main.py --symbol MSFT --start 2024-01-01 --end 2024-12-31
```

Show supported default symbols:

```bash
python main.py --show-defaults
```

## Phase 1 supported symbols

- `RELIANCE.NS` (NSE)
- `500325.BO` (BSE)
- `MSFT`, `NVDA` (US)

## Project structure

- `stock_analysis/data/fetcher.py` — Yahoo Finance data fetcher
- `stock_analysis/report/summary.py` — output formatting helper
- `main.py` — Phase 1 CLI entrypoint
- `tests/` — unit tests
