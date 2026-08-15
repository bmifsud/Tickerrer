import pytest
from fastapi.testclient import TestClient
import shutil
from pathlib import Path
import pandas as pd

from main import app, DATA_DIR
from tickerrer.symbols import resolve_symbol
from tickerrer.storage import save_ticker_data

client = TestClient(app)

def setup_function():
    # Clear test data directory before tests
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)

def test_get_data_404_when_missing():
    response = client.get("/api/data?symbol=nonexistent")
    assert response.status_code == 404

def test_fetch_and_get_data_flow():
    # Pre-populate sample data
    sym_info = resolve_symbol("aapl")
    dates = pd.date_range("2026-01-01", "2026-01-02", freq="D")
    df = pd.DataFrame(
        {"Open": [100.0, 101.0], "High": [105.0, 106.0], "Low": [95.0, 96.0], "Close": [102.0, 103.0], "Volume": [1000, 1100]},
        index=dates
    )
    save_ticker_data({"1d": df}, sym_info, output_dir=DATA_DIR, file_format="csv")

    response = client.get("/api/data?symbol=aapl&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["Close"] == 102.0

def test_chart_data_endpoint():
    sym_info = resolve_symbol("aapl")
    dates = pd.date_range("2026-01-01", "2026-01-02", freq="D")
    df = pd.DataFrame(
        {"Open": [100.0, 101.0], "High": [105.0, 106.0], "Low": [95.0, 96.0], "Close": [102.0, 103.0], "Volume": [1000, 1100]},
        index=dates
    )
    save_ticker_data({"1d": df}, sym_info, output_dir=DATA_DIR, file_format="csv")

    response = client.get("/api/chart?symbol=aapl&interval=1d")
    assert response.status_code == 200
    chart_json = response.json()
    assert chart_json["symbol"] == "aapl"
    assert "labels" in chart_json
    assert "series" in chart_json
    assert chart_json["series"]["Close"] == [102.0, 103.0]
