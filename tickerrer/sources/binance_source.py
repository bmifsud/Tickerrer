"""Binance data source driver (primary/fallback for Crypto)."""

from typing import Optional
import datetime
import pandas as pd
import requests
from tickerrer.symbols import SymbolInfo
from tickerrer.sources.base import BaseSource


class BinanceSource(BaseSource):
    """Data source using Binance public REST API."""

    INTERVAL_MAP = {
        "1m": "1m",
        "3m": "3m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "2h": "2h",
        "4h": "4h",
        "1d": "1d",
        "1wk": "1w",
        "1mth": "1M"
    }

    @property
    def name(self) -> str:
        return "binance"

    def fetch_data(
        self,
        symbol_info: SymbolInfo,
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        binance_sym = symbol_info.binance_ticker
        if not binance_sym:
            # Try constructing ticker if ends with -USD or USDT
            query = symbol_info.query_symbol.upper().replace("-USD", "USDT").replace("USD", "USDT")
            if not query.endswith("USDT"):
                query = f"{query}USDT"
            binance_sym = query

        binance_interval = self.INTERVAL_MAP.get(interval, "1d")

        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": binance_sym,
            "interval": binance_interval,
            "limit": 1000
        }

        if start:
            params["startTime"] = int(pd.to_datetime(start).timestamp() * 1000)
        if end:
            params["endTime"] = int(pd.to_datetime(end).timestamp() * 1000)

        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                return pd.DataFrame()

            data = resp.json()
            if not isinstance(data, list) or len(data) == 0:
                return pd.DataFrame()

            records = []
            for item in data:
                # kline structure: [open_time, open, high, low, close, volume, ...]
                open_time = pd.to_datetime(item[0], unit="ms")
                records.append({
                    "Datetime": open_time,
                    "Open": float(item[1]),
                    "High": float(item[2]),
                    "Low": float(item[3]),
                    "Close": float(item[4]),
                    "Volume": float(item[5])
                })

            df = pd.DataFrame(records).set_index("Datetime")
            return df
        except Exception:
            return pd.DataFrame()
