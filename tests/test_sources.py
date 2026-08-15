import pytest
import pandas as pd
from tickerrer.symbols import resolve_symbol
from tickerrer.sources.stooq_source import StooqSource
from tickerrer.sources.binance_source import BinanceSource
from tickerrer.sources.frankfurter_source import FrankfurterSource
from tickerrer.sources.yfinance_source import YFinanceSource

def test_stooq_source_invalid():
    src = StooqSource()
    assert src.name == "stooq"
    sym_info = resolve_symbol("aapl")
    # For non-1d interval, it should return empty
    df = src.fetch_data(sym_info, interval="1h")
    assert df.empty

def test_binance_source_invalid():
    src = BinanceSource()
    assert src.name == "binance"
    sym_info = resolve_symbol("aapl") # equity not crypto
    # Query for AAPL on binance will return empty dataframe safely
    df = src.fetch_data(sym_info, interval="1d")
    assert isinstance(df, pd.DataFrame)

def test_frankfurter_source_invalid():
    src = FrankfurterSource()
    assert src.name == "frankfurter"
    sym_info = resolve_symbol("aapl") # equity not forex
    df = src.fetch_data(sym_info, interval="1d")
    assert df.empty

def test_yfinance_source_name():
    src = YFinanceSource()
    assert src.name == "yfinance"
