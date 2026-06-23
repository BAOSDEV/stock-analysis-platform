import pandas as pd
import pytest

from main import main, fetch_and_report


def test_main_with_symbol(monkeypatch, capsys):
    def fake_fetch_company_fundamentals(symbol):
        return {
            "symbol": symbol,
            "longName": "Test Corp",
            "sector": "Technology",
            "industry": "Software",
            "marketCap": 1000000000,
            "trailingPE": 15.0,
            "forwardPE": 13.5,
            "dividendYield": 0.02,
            "beta": 1.1,
            "fullTimeEmployees": 5000,
        }

    def fake_fetch_price_history(symbol, start, end):
        return pd.DataFrame({"Close": [100.0, 101.0]}, index=pd.date_range(start, periods=2))

    monkeypatch.setattr("main.fetch_company_fundamentals", fake_fetch_company_fundamentals)
    monkeypatch.setattr("main.fetch_price_history", fake_fetch_price_history)

    main(["--symbol", "RELIANCE.NS"])
    captured = capsys.readouterr()
    assert "SYMBOL: RELIANCE.NS" in captured.out


def test_fetch_and_report_success(monkeypatch):
    def fake_fetch_company_fundamentals(symbol):
        return {
            "symbol": symbol,
            "longName": "Test",
            "sector": "Tech",
            "industry": "Software",
            "marketCap": 1000000,
            "trailingPE": 20.0,
            "forwardPE": 18.0,
            "dividendYield": 0.01,
            "beta": 1.0,
            "fullTimeEmployees": 1000,
        }

    def fake_fetch_price_history(symbol, start, end):
        return pd.DataFrame({"Close": [100.0, 101.0]}, index=pd.date_range(start, periods=2))

    monkeypatch.setattr("main.fetch_company_fundamentals", fake_fetch_company_fundamentals)
    monkeypatch.setattr("main.fetch_price_history", fake_fetch_price_history)

    result = fetch_and_report("MSFT", "2024-01-01", "2024-12-31")
    assert result is True


def test_fetch_and_report_invalid_symbol(monkeypatch):
    def fake_fetch_company_fundamentals(symbol):
        raise RuntimeError(f"No fundamentals available for {symbol}")

    monkeypatch.setattr("main.fetch_company_fundamentals", fake_fetch_company_fundamentals)

    result = fetch_and_report("INVALID123456", "2024-01-01", "2024-12-31")
    assert result is False
