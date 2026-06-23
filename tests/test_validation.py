import pytest

from stock_analysis.validation import validate_date, validate_symbol


def test_validate_symbol_valid():
    assert validate_symbol("RELIANCE.NS") == "RELIANCE.NS"
    assert validate_symbol("msft") == "MSFT"


def test_validate_symbol_invalid():
    with pytest.raises(ValueError, match="must be a non-empty string"):
        validate_symbol("")
    
    with pytest.raises(ValueError, match="12 characters or less"):
        validate_symbol("VERYLONGSYMBOL")


def test_validate_date_valid():
    result = validate_date("2024-01-01")
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 1


def test_validate_date_invalid():
    with pytest.raises(ValueError, match="Invalid date"):
        validate_date("2024/01/01")
    
    with pytest.raises(ValueError, match="Invalid date"):
        validate_date("invalid")
