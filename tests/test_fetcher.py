import pandas as pd

import pytest

from stock_analysis.data import fetcher


def test_fetch_price_history(monkeypatch):
    def fake_download(symbol, start, end, progress):
        return pd.DataFrame({"Close": [100.0, 101.0]}, index=pd.date_range(start, periods=2))

    monkeypatch.setattr(fetcher, "yf", type("FakeYF", (), {"download": staticmethod(fake_download)}))

    history = fetcher.fetch_price_history("RELIANCE.NS", "2024-01-01", "2024-01-03")

    assert isinstance(history, pd.DataFrame)
    assert history.shape == (2, 1)
    assert history["Close"].tolist() == [100.0, 101.0]


def test_fetch_company_fundamentals(monkeypatch):
    class FakeTicker:
        def __init__(self, symbol):
            self.symbol = symbol

        @property
        def info(self):
            return {
                "longName": "Test Company",
                "sector": "Technology",
                "industry": "Software",
                "marketCap": 1234567890,
                "trailingPE": 20.1,
                "forwardPE": 18.5,
                "dividendYield": 0.015,
                "beta": 1.2,
                "fullTimeEmployees": 5000,
            }

    monkeypatch.setattr(fetcher, "yf", type("FakeYF", (), {"Ticker": FakeTicker}))

    fundamentals = fetcher.fetch_company_fundamentals("RELIANCE.NS")

    assert fundamentals["symbol"] == "RELIANCE.NS"
    assert fundamentals["marketCap"] == 1234567890
    assert fundamentals["trailingPE"] == 20.1


def test_unsupported_source_raises():
    with pytest.raises(ValueError, match="Only the 'yahoo' source is supported"):
        fetcher.fetch_price_history("RELIANCE.NS", "2024-01-01", "2024-01-03", source="alpha")

    with pytest.raises(ValueError, match="Only the 'yahoo' source is supported"):
        fetcher.fetch_company_fundamentals("RELIANCE.NS", source="alpha")
