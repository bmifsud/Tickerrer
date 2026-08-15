"""Stooq data source driver (primary/fallback for stocks, indexes, ETFs, commodities, forex)."""

from typing import Optional
import datetime
import pandas as pd
import requests
from tickerrer.symbols import SymbolInfo
from tickerrer.sources.base import BaseSource


class StooqSource(BaseSource):
    """Data source using Stooq CSV endpoint."""

    @property
    def name(self) -> str:
        return "stooq"

    def fetch_data(
        self,
        symbol_info: SymbolInfo,
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        # Stooq supports daily data primarily
        if interval not in ["1d", "d", "daily"]:
            return pd.DataFrame()

        stooq_sym = symbol_info.stooq_ticker or symbol_info.query_symbol.lower()
        if not stooq_sym:
            return pd.DataFrame()

        # Stooq CSV format URL: https://stooq.com/q/d/l/?s=aapl.us&i=d
        url = f"https://stooq.com/q/d/l/?s={stooq_sym}&i=d"

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200 or "Date,Open,High,Low,Close" not in resp.text:
                return pd.DataFrame()

            from io import StringIO
            df = pd.read_csv(StringIO(resp.text))

            if df.empty or "Date" not in df.columns:
                return pd.DataFrame()

            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.dropna(subset=["Date"]).set_index("Date").sort_index()

            # Filter by start / end date if provided
            if start:
                start_dt = pd.to_datetime(start)
                df = df[df.index >= start_dt]
            if end:
                end_dt = pd.to_datetime(end)
                df = df[df.index <= end_dt]

            # Normalize column names
            col_map = {c: c.capitalize() for c in df.columns}
            df.rename(columns=col_map, inplace=True)

            for col in ["Open", "High", "Low", "Close"]:
                if col not in df.columns:
                    return pd.DataFrame()

            if "Volume" not in df.columns:
                df["Volume"] = 0

            return df[["Open", "High", "Low", "Close", "Volume"]].copy()
        except Exception:
            return pd.DataFrame()
