import pytest
import shutil
import tempfile
from pathlib import Path
import pandas as pd
from tickerrer.symbols import resolve_symbol, AssetClass
from tickerrer.storage import save_ticker_data

@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield Path(d)
    shutil.rmtree(d)

def test_save_and_incremental_refresh(temp_dir):
    sym_info = resolve_symbol("aapl")

    # Initial batch: 3 days
    dates1 = pd.date_range("2023-01-01", "2023-01-03", freq="D")
    df1 = pd.DataFrame({
        "Open": [100.0, 101.0, 102.0],
        "High": [105.0, 106.0, 107.0],
        "Low": [95.0, 96.0, 97.0],
        "Close": [102.0, 103.0, 104.0],
        "Volume": [1000, 1100, 1200]
    }, index=dates1)

    saved = save_ticker_data({"1d": df1}, sym_info, output_dir=temp_dir, file_format="csv")
    csv_path = Path(saved["1d"])
    assert csv_path.exists()

    df_read1 = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    assert len(df_read1) == 3

    # Refresh batch: overlapping date + new dates
    dates2 = pd.date_range("2023-01-03", "2023-01-05", freq="D")
    df2 = pd.DataFrame({
        "Open": [102.5, 103.0, 104.0],  # Updated 2023-01-03
        "High": [107.5, 108.0, 109.0],
        "Low": [97.5, 98.0, 99.0],
        "Close": [104.5, 105.0, 106.0],
        "Volume": [1250, 1300, 1400]
    }, index=dates2)

    save_ticker_data({"1d": df2}, sym_info, output_dir=temp_dir, file_format="csv", refresh=True)

    df_read2 = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    # Total merged rows should be 5 (2023-01-01 to 2023-01-05)
    assert len(df_read2) == 5
    # The 2023-01-03 record should be updated with the latest refreshed data (Open: 102.5)
    assert df_read2.loc["2023-01-03"]["Open"] == 102.5

def test_save_json_and_parquet(temp_dir):
    sym_info = resolve_symbol("aapl")
    dates = pd.date_range("2023-01-01", "2023-01-02", freq="D")
    df = pd.DataFrame({"Open": [100.0, 101.0], "High": [105.0, 106.0], "Low": [95.0, 96.0], "Close": [102.0, 103.0], "Volume": [1000, 1100]}, index=dates)

    saved_json = save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="json")
    assert Path(saved_json["1d"]).exists()

    saved_parquet = save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="parquet")
    assert Path(saved_parquet["1d"]).exists()

    # Re-read json with refresh
    save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="json", refresh=True)

def test_load_existing_json(temp_dir):
    sym_info = resolve_symbol("aapl")
    dates = pd.date_range("2023-01-01", "2023-01-02", freq="D")
    df = pd.DataFrame({"Open": [100.0, 101.0], "High": [105.0, 106.0], "Low": [95.0, 96.0], "Close": [102.0, 103.0], "Volume": [1000, 1100]}, index=dates)

    save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="json")
    save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="json", refresh=True)

def test_load_existing_parquet(temp_dir):
    sym_info = resolve_symbol("aapl")
    dates = pd.date_range("2023-01-01", "2023-01-02", freq="D")
    df = pd.DataFrame({"Open": [100.0, 101.0], "High": [105.0, 106.0], "Low": [95.0, 96.0], "Close": [102.0, 103.0], "Volume": [1000, 1100]}, index=dates)

    save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="parquet")
    save_ticker_data({"1d": df}, sym_info, output_dir=temp_dir, file_format="parquet", refresh=True)
