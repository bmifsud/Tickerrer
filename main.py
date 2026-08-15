from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd

from tickerrer.downloader import TickerDownloader
from tickerrer.symbols import resolve_symbol
from tickerrer.storage import save_ticker_data, _load_existing_file

app = FastAPI(title="Tickerrer API")
downloader = TickerDownloader()
DATA_DIR = Path("./data")

def _get_stored_filepath(symbol: str, interval: str = "1d", file_format: str = "csv") -> Optional[Path]:
    sym_info = resolve_symbol(symbol)
    safe_symbol_name = sym_info.query_symbol.lower().replace("^", "").replace("=", "_").replace("/", "_")
    base_dir = DATA_DIR / sym_info.asset_class.value / interval
    file_path = base_dir / f"{safe_symbol_name}_{interval}.{file_format}"
    if file_path.exists():
        return file_path
    return None

@app.get("/api/data")
def get_stored_data(
    symbol: str = Query(..., description="Ticker symbol e.g. aapl, ndx"),
    interval: str = Query("1d", description="Interval e.g. 1d, 1h"),
    file_format: str = Query("csv", description="File format e.g. csv, json, parquet")
) -> List[Dict[str, Any]]:
    """Retrieve stored ticker data."""
    file_path = _get_stored_filepath(symbol, interval, file_format)
    if not file_path:
        raise HTTPException(status_code=404, detail=f"No stored data found for symbol '{symbol}' with interval '{interval}'")

    df = _load_existing_file(file_path, file_format)
    if df.empty:
        return []

    reset_df = df.reset_index()
    # Convert dates/datetimes to string for JSON output
    for col in reset_df.columns:
        if pd.api.types.is_datetime64_any_dtype(reset_df[col]):
            reset_df[col] = reset_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    return reset_df.to_dict(orient="records")

@app.post("/api/fetch")
def fetch_and_store_data(
    symbol: str = Query(..., description="Ticker symbol e.g. aapl, ndx"),
    period: Optional[str] = Query("1y", description="Historical period e.g. 1y, 1mo, 5d"),
    start: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    interval: str = Query("1d", description="Interval e.g. 1d, 1h"),
    file_format: str = Query("csv", description="Storage format csv, json, parquet")
) -> Dict[str, Any]:
    """Instruct downloader to fetch symbol data and store/refresh repository data."""
    data_by_interval = downloader.download_symbol(
        symbol=symbol,
        start=start,
        end=end,
        period=period,
        intervals=[interval]
    )

    sym_info = resolve_symbol(symbol)
    saved_files = save_ticker_data(
        data_by_interval=data_by_interval,
        symbol_info=sym_info,
        output_dir=DATA_DIR,
        file_format=file_format,
        refresh=True
    )

    if not saved_files:
        raise HTTPException(status_code=400, detail="Failed to download data for the specified symbol")

    return {
        "message": f"Successfully fetched and stored data for {symbol}",
        "saved_files": saved_files
    }

@app.get("/api/chart")
def get_chart_data(
    symbol: str = Query(..., description="Ticker symbol e.g. aapl, ndx"),
    interval: str = Query("1d", description="Interval e.g. 1d, 1h"),
    file_format: str = Query("csv", description="File format e.g. csv, json, parquet")
) -> Dict[str, Any]:
    """Package stored ticker data into UI chart presentation format."""
    file_path = _get_stored_filepath(symbol, interval, file_format)
    if not file_path:
        # Attempt to auto-fetch if not stored yet
        try:
            data_by_interval = downloader.download_symbol(symbol=symbol, period="1y", intervals=[interval])
            sym_info = resolve_symbol(symbol)
            save_ticker_data(data_by_interval, sym_info, output_dir=DATA_DIR, file_format=file_format)
            file_path = _get_stored_filepath(symbol, interval, file_format)
        except Exception:
            pass

    if not file_path:
        raise HTTPException(status_code=404, detail=f"No data available for symbol '{symbol}'")

    df = _load_existing_file(file_path, file_format)
    if df.empty:
        raise HTTPException(status_code=404, detail="Stored data is empty")

    reset_df = df.reset_index()
    time_col = reset_df.columns[0]
    labels = reset_df[time_col].astype(str).tolist()

    series = {}
    for col in ["Close", "Open", "High", "Low", "Volume"]:
        if col in reset_df.columns:
            series[col] = reset_df[col].fillna(0).tolist()

    return {
        "symbol": symbol,
        "interval": interval,
        "labels": labels,
        "series": series
    }
