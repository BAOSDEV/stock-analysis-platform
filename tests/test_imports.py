from stock_analysis.data import fetch_company_fundamentals, fetch_price_history


def test_imports_work():
    assert fetch_company_fundamentals
    assert fetch_price_history
