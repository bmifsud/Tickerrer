"""Frankfurter (ECB rates) data source driver for Forex pairs."""

from typing import Optional
import pandas as pd
import requests
from tickerrer.symbols import SymbolInfo
from tickerrer.sources.base import BaseSource


class FrankfurterSource(BaseSource):
    """Data source using Frankfurter API for Forex currency rates."""

    @property
    def name(self) -> str:
        return "frankfurter"

    def fetch_data(
        self,
        symbol_info: SymbolInfo,
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        if interval not in ["1d", "d", "daily"]:
            return pd.DataFrame()

        pair = symbol_info.forex_pair
        if not pair:
            return pd.DataFrame()

        base, quote = pair

        start_date = start if start else "2020-01-01"
        end_date = end if end else ""

        url = f"https://api.frankfurter.app/{start_date}..{end_date}"
        params = {"from": base, "to": quote}

        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                return pd.DataFrame()

            data = resp.json()
            rates = data.get("rates", {})
            if not rates:
                return pd.DataFrame()

            records = []
            for date_str, rate_dict in rates.items():
                if quote in rate_dict:
                    val = float(rate_dict[quote])
                    records.append({
                        "Date": pd.to_datetime(date_str),
                        "Open": val,
                        "High": val,
                        "Low": val,
                        "Close": val,
                        "Volume": 0.0
                    })

            if not records:
                return pd.DataFrame()

            df = pd.DataFrame(records).set_index("Date").sort_index()
            return df
        except Exception:
            return pd.DataFrame()
