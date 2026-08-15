"""Storage and incremental data repository upkeep management for tickerrer."""

import os
from pathlib import Path
from typing import Dict, Union, Optional
import pandas as pd
from tickerrer.symbols import SymbolInfo


def _load_existing_file(file_path: Path, file_format: str) -> pd.DataFrame:
    """Helper to load existing data file into pandas DataFrame."""
    if not file_path.exists():
        return pd.DataFrame()

    try:
        if file_format == "csv":
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            return df
        elif file_format == "json":
            df = pd.read_json(file_path, orient="records")
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
                df.set_index("Date", inplace=True)
            elif "Datetime" in df.columns:
                df["Datetime"] = pd.to_datetime(df["Datetime"])
                df.set_index("Datetime", inplace=True)
            return df
        elif file_format == "parquet":
            df = pd.read_parquet(file_path)
            return df
    except Exception:
        return pd.DataFrame()

    return pd.DataFrame()


def save_ticker_data(
    data_by_interval: Dict[str, pd.DataFrame],
    symbol_info: SymbolInfo,
    output_dir: Union[str, Path] = "./data",
    file_format: str = "csv",
    organize_by_asset_class: bool = True,
    refresh: bool = True
) -> Dict[str, str]:
    """
    Saves ticker data frames organized by interval and asset class.
    Performs incremental data merging/refresh upkeep if existing data is present.

    Args:
        data_by_interval: Dict mapping interval string (e.g. '1d') to pandas DataFrame.
        symbol_info: SymbolInfo metadata.
        output_dir: Root repository output directory.
        file_format: 'csv', 'json', or 'parquet'.
        organize_by_asset_class: If True, subfolders per asset class are created.
        refresh: If True, merges new fetched data with existing data, keeping repository up-to-date.

    Returns:
        Dict mapping interval string to the saved file path.
    """
    base_dir = Path(output_dir)
    if organize_by_asset_class:
        base_dir = base_dir / symbol_info.asset_class.value

    saved_files = {}
    file_format = file_format.lower().strip()

    safe_symbol_name = symbol_info.query_symbol.lower().replace("^", "").replace("=", "_").replace("/", "_")

    for interval, df in data_by_interval.items():
        if df is None or df.empty:
            continue

        interval_dir = base_dir / interval
        interval_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{safe_symbol_name}_{interval}.{file_format}"
        file_path = interval_dir / filename

        df_to_save = df.copy()

        # Incremental repository upkeep (merge with existing file)
        if refresh and file_path.exists():
            existing_df = _load_existing_file(file_path, file_format)
            if not existing_df.empty:
                try:
                    # Combine existing and new data
                    combined = pd.concat([existing_df, df_to_save])

                    # Deduplicate by index timestamp (keeping latest refreshed record)
                    combined = combined[~combined.index.duplicated(keep="last")]
                    combined.sort_index(inplace=True)
                    df_to_save = combined
                except Exception:
                    # Fallback to saving new df directly if concat/index fails
                    pass

        if file_format == "csv":
            df_to_save.to_csv(file_path, index=True)
        elif file_format == "json":
            # Convert index to column for json export
            reset_df = df_to_save.reset_index()
            reset_df.to_json(file_path, orient="records", date_format="iso")
        elif file_format == "parquet":
            df_to_save.to_parquet(file_path, index=True)
        else:
            raise ValueError(f"Unsupported file format: {file_format}. Use 'csv', 'json', or 'parquet'.")

        saved_files[interval] = str(file_path)

    return saved_files
