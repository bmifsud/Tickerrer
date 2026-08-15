"""Core downloader module with multi-source fallback for tickerrer."""

from typing import List, Dict, Union, Optional
import logging
import pandas as pd

from tickerrer.symbols import resolve_symbol, AssetClass, SymbolInfo
from tickerrer.sources.base import BaseSource
from tickerrer.sources.yfinance_source import YFinanceSource
from tickerrer.sources.stooq_source import StooqSource
from tickerrer.sources.binance_source import BinanceSource
from tickerrer.sources.frankfurter_source import FrankfurterSource

logger = logging.getLogger("tickerrer.downloader")


class TickerDownloader:
    """
    Downloads historical market ticker data using primary and fallback data sources.
    """

    def __init__(self, sources: Optional[List[BaseSource]] = None):
        if sources is not None:
            self.sources = sources
        else:
            # Default order of sources
            self.sources = [
                YFinanceSource(),
                BinanceSource(),
                StooqSource(),
                FrankfurterSource()
            ]

    def download_symbol(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        intervals: Union[str, List[str]] = "1d",
        override_asset_class: Optional[AssetClass] = None,
        preferred_source: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Downloads market data for a given symbol across one or multiple intervals.

        Args:
            symbol: Ticker or alias (e.g., 'ndx', 'aapl', 'gold', 'eurusd', 'btc').
            start: Start date string (YYYY-MM-DD).
            end: End date string (YYYY-MM-DD).
            period: Historical period if start/end not provided (e.g. '1y', '5d', '1mo').
            intervals: Single interval string ('1d') or list of intervals (['1d', '1h']).
            override_asset_class: Explicitly classify asset class.
            preferred_source: Name of preferred data source (e.g. 'yfinance', 'stooq').

        Returns:
            Dict mapping interval string to pandas DataFrame with market data.
        """
        symbol_info = resolve_symbol(symbol, override_asset_class=override_asset_class)

        if isinstance(intervals, str):
            interval_list = [intervals]
        else:
            interval_list = list(intervals)

        results = {}

        # Prepare source ordering
        source_order = list(self.sources)
        if preferred_source:
            pref = preferred_source.lower().strip()
            source_order.sort(key=lambda s: 0 if s.name.lower() == pref else 1)

        for interval in interval_list:
            df = pd.DataFrame()
            for src in source_order:
                try:
                    fetched_df = src.fetch_data(
                        symbol_info=symbol_info,
                        start=start,
                        end=end,
                        period=period,
                        interval=interval
                    )
                    if fetched_df is not None and not fetched_df.empty:
                        df = fetched_df
                        logger.info(
                            f"Successfully downloaded {symbol_info.query_symbol} ({interval}) using {src.name}"
                        )
                        break
                except Exception as e:
                    logger.debug(f"Source {src.name} failed for {symbol}: {e}")

            results[interval] = df

        return results

    def download_batch(
        self,
        symbols: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        period: Optional[str] = None,
        intervals: Union[str, List[str]] = "1d",
        override_asset_class: Optional[AssetClass] = None,
        preferred_source: Optional[str] = None
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Downloads market data for multiple symbols.

        Returns:
            Dict mapping symbol name -> { interval -> DataFrame }.
        """
        batch_results = {}
        for sym in symbols:
            batch_results[sym] = self.download_symbol(
                symbol=sym,
                start=start,
                end=end,
                period=period,
                intervals=intervals,
                override_asset_class=override_asset_class,
                preferred_source=preferred_source
            )
        return batch_results
