import pytest
import shutil
import tempfile
from pathlib import Path
import pandas as pd
from tickerrer.cli import main
from tickerrer.sources.base import BaseSource

class MockSuccessSource(BaseSource):
    @property
    def name(self) -> str:
        return "mock_success"

    def fetch_data(self, symbol_info, start=None, end=None, period=None, interval="1d"):
        index = pd.date_range("2023-01-01", periods=3, freq="D")
        return pd.DataFrame({
            "Open": [100.0] * 3,
            "High": [105.0] * 3,
            "Low": [95.0] * 3,
            "Close": [102.0] * 3,
            "Volume": [1000] * 3
        }, index=index)

def test_cli_execution(monkeypatch, tmp_path):
    # Monkeypatch TickerDownloader to use MockSuccessSource
    from tickerrer.downloader import TickerDownloader
    monkeypatch.setattr(TickerDownloader, "__init__", lambda self, sources=None: setattr(self, "sources", [MockSuccessSource()]))

    out_dir = str(tmp_path / "data")
    ret = main(["aapl", "gold", "-p", "5d", "-i", "1d", "-o", out_dir, "-f", "csv"])
    assert ret == 0

    # Check files were created in output directory
    created_files = list(Path(out_dir).rglob("*.csv"))
    assert len(created_files) >= 2
