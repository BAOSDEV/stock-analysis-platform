import pandas as pd

from main import main


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
    assert "Fetching data for RELIANCE.NS" in captured.out
    assert "Fetched 2 historical rows for RELIANCE.NS." in captured.out
