"""Yahoo Finance data source driver."""

from typing import Optional
import pandas as pd
import yfinance as yf
from tickerrer.symbols import SymbolInfo
from tickerrer.sources.base import BaseSource


class YFinanceSource(BaseSource):
    """Data source using yfinance library."""

    @property
    def name(self) -> str:
        return "yfinance"

    def fetch_data(
        self,
        symbol_info: SymbolInfo,
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        ticker_str = symbol_info.ticker
        try:
            ticker = yf.Ticker(ticker_str)
            if start or end:
                df = ticker.history(start=start, end=end, interval=interval)
            else:
                p = period or "1y"
                df = ticker.history(period=p, interval=interval)

            if df is None or df.empty:
                # Try download fallback call
                df = yf.download(
                    ticker_str,
                    start=start,
                    end=end,
                    period=period if not (start or end) else None,
                    interval=interval,
                    progress=False
                )

            if df is None or df.empty:
                return pd.DataFrame()

            # Flatten MultiIndex columns if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c[0] for c in df.columns]

            # Ensure standard required columns exist
            for col in ["Open", "High", "Low", "Close", "Volume"]:
                if col not in df.columns:
                    df[col] = float("nan")

            cols = ["Open", "High", "Low", "Close", "Volume"]
            if "Adj Close" in df.columns:
                cols.append("Adj Close")

            res_df = df[cols].copy()
            res_df.dropna(how="all", subset=["Open", "High", "Low", "Close"], inplace=True)
            return res_df
        except Exception:
            return pd.DataFrame()
