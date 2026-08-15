import pytest
import pandas as pd
from tickerrer.symbols import resolve_symbol, AssetClass
from tickerrer.downloader import TickerDownloader
from tickerrer.sources.base import BaseSource

class MockSuccessSource(BaseSource):
    @property
    def name(self) -> str:
        return "mock_success"

    def fetch_data(self, symbol_info, start=None, end=None, period=None, interval="1d"):
        index = pd.date_range("2023-01-01", periods=5, freq="D")
        return pd.DataFrame({
            "Open": [100.0] * 5,
            "High": [105.0] * 5,
            "Low": [95.0] * 5,
            "Close": [102.0] * 5,
            "Volume": [1000] * 5
        }, index=index)

class MockFailingSource(BaseSource):
    @property
    def name(self) -> str:
        return "mock_fail"

    def fetch_data(self, symbol_info, start=None, end=None, period=None, interval="1d"):
        return pd.DataFrame()

def test_downloader_fallback():
    downloader = TickerDownloader(sources=[MockFailingSource(), MockSuccessSource()])
    res = downloader.download_symbol("aapl", period="5d", intervals="1d")
    assert "1d" in res
    df = res["1d"]
    assert not df.empty
    assert len(df) == 5

def test_downloader_batch():
    downloader = TickerDownloader(sources=[MockSuccessSource()])
    res = downloader.download_batch(["aapl", "gold"], period="5d", intervals=["1d", "1h"])
    assert "aapl" in res
    assert "gold" in res
    assert "1d" in res["aapl"]
    assert "1h" in res["aapl"]
