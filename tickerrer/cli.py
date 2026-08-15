"""Command-line interface for tickerrer data downloader and repository upkeep."""

import argparse
import sys
import logging
from typing import List

from tickerrer.symbols import AssetClass, resolve_symbol
from tickerrer.downloader import TickerDownloader
from tickerrer.storage import save_ticker_data


def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args: List[str] = None):
    parser = argparse.ArgumentParser(
        description="tickerrer - Download & upkeep historical market ticker data across Indexes, CFD, Equity, Commodities, ETFs, Forex, and Crypto."
    )
    parser.add_argument(
        "symbols",
        nargs="+",
        help="One or more ticker symbols or aliases (e.g., ndx, aapl, gold, eurusd, btc, us30)."
    )
    parser.add_argument(
        "-s", "--start",
        help="Start date (YYYY-MM-DD)."
    )
    parser.add_argument(
        "-e", "--end",
        help="End date (YYYY-MM-DD)."
    )
    parser.add_argument(
        "-p", "--period",
        default="1y",
        help="Historical period if start/end not specified (e.g. 5d, 1mo, 1y, 5y, max). Default: 1y."
    )
    parser.add_argument(
        "-i", "--intervals",
        nargs="+",
        default=["1d"],
        help="Data intervals (e.g. 1m, 5m, 15m, 1h, 1d, 1wk). Default: 1d."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="./data",
        help="Repository root directory to store downloaded ticker data. Default: ./data."
    )
    parser.add_argument(
        "-f", "--format",
        choices=["csv", "json", "parquet"],
        default="csv",
        help="Output file format (csv, json, parquet). Default: csv."
    )
    parser.add_argument(
        "--asset-class",
        choices=[ac.value for ac in AssetClass],
        help="Override asset class categorization."
    )
    parser.add_argument(
        "--source",
        help="Preferred data source (e.g. yfinance, stooq, binance, frankfurter)."
    )
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Disable incremental merging/upkeep with existing repository files."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose log output."
    )

    parsed = parser.parse_args(args)
    setup_logging(parsed.verbose)

    override_ac = None
    if parsed.asset_class:
        override_ac = AssetClass(parsed.asset_class)

    downloader = TickerDownloader()
    refresh_enabled = not parsed.no_refresh

    print(f"🚀 tickerrer starting data download for symbols: {', '.join(parsed.symbols)}")
    print(f"📅 Range/Period: Start={parsed.start}, End={parsed.end}, Period={parsed.period}")
    print(f"⏱️ Intervals: {', '.join(parsed.intervals)}")
    print(f"📁 Output Directory: {parsed.output_dir} (Format: {parsed.format}, Upkeep/Refresh: {refresh_enabled})\n")

    summary = []

    for sym in parsed.symbols:
        sym_info = resolve_symbol(sym, override_asset_class=override_ac)
        print(f"Fetching '{sym}' -> {sym_info.name} [{sym_info.asset_class.value}]...")

        download_results = downloader.download_symbol(
            symbol=sym,
            start=parsed.start,
            end=parsed.end,
            period=parsed.period,
            intervals=parsed.intervals,
            override_asset_class=override_ac,
            preferred_source=parsed.source
        )

        saved_files = save_ticker_data(
            data_by_interval=download_results,
            symbol_info=sym_info,
            output_dir=parsed.output_dir,
            file_format=parsed.format,
            refresh=refresh_enabled
        )

        for interval, path in saved_files.items():
            df = download_results.get(interval)
            row_cnt = len(df) if df is not None else 0
            summary.append((sym, sym_info.asset_class.value, interval, row_cnt, path))
            print(f"  ✓ [{interval}] Saved {row_cnt} records to {path}")

    print("\n✅ Download and repository upkeep complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
