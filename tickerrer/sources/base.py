"""Base data source interface for tickerrer."""

from abc import ABC, abstractmethod
from typing import Optional, Dict
import pandas as pd
from tickerrer.symbols import SymbolInfo


class BaseSource(ABC):
    """Abstract base class for ticker data sources."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Source identifier name (e.g. 'yfinance', 'stooq', 'binance', 'frankfurter')."""
        pass

    @abstractmethod
    def fetch_data(
        self,
        symbol_info: SymbolInfo,
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical ticker OHLCV data.

        Returns a standardized DataFrame with index as Datetime or Date, and columns:
        ['Open', 'High', 'Low', 'Close', 'Volume'].
        Returns an empty DataFrame if no data found or request failed.
        """
        pass
