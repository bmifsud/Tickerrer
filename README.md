# Tickerrer 📈

**Tickerrer** is a Python tool and library designed to fetch, download, and organize historical market ticker data across multiple asset classes with automatic source fallback and repository data upkeep.

---

## 🌟 Supported Asset Classes

Tickerrer supports full coverage across:
- 📊 **Indexes** (e.g., `ndx` / `^NDX`, `spx` / `^GSPC`, `dji` / `^DJI`, `vix`, `dax`, `nikkei`)
- 📈 **Equity** (e.g., `aapl`, `msft`, `tsla`, `nvda`, `googl`)
- 🛢️ **Commodities** (e.g., `gold` / `GC=F`, `silver` / `SI=F`, `oil` / `CL=F`, `brent`, `ng`)
- 🏢 **ETFs** (e.g., `spy`, `qqq`, `iwm`, `gld`, `vti`)
- 💱 **Forex** (e.g., `eurusd` / `EURUSD=X`, `gbpusd`, `usdjpy`, `audusd`)
- 🪙 **Crypto** (e.g., `btc` / `BTC-USD`, `eth`, `sol`, `xrp`)
- 📉 **CFDs** (e.g., `us30`, `us500`, `nas100`, `ger40`, `xauusd`)

---

## 🚀 Data Sources & Multi-Source Fallback

Tickerrer connects to multiple data sources with automatic failover so downloads remain uninterrupted and complete:
1. **Yahoo Finance** (`yfinance`) - Primary source for multi-asset OHLCV market data.
2. **Binance API** - Secondary/Primary fallback source for cryptocurrency historical data.
3. **Stooq** - Fallback source for equities, global indexes, commodities, and currency pairs.
4. **Frankfurter (ECB)** - Fallback source for official Forex exchange rates.

---

## 📦 Installation

```bash
pip install -e .
```

Dependencies include `yfinance`, `pandas`, `requests`, and `pyarrow`.

---

## 💻 CLI Usage

```bash
# Download daily data for Nasdaq 100, Apple, Gold, EUR/USD, and Bitcoin
tickerrer ndx aapl gold eurusd btc --period 1y --intervals 1d

# Download specific date range with multiple intervals
tickerrer spy qqq gld -s 2023-01-01 -e 2023-12-31 -i 1d 1h -f csv -o ./my_data

# Run data refresh (merges new market data into existing files without duplicates)
tickerrer ndx aapl gold -p 5d
```

### CLI Arguments Summary
| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `symbols` | | Space-separated symbols or aliases (`ndx`, `aapl`, `gold`, `eurusd`, `btc`) | **Required** |
| `--start` | `-s` | Start date string (`YYYY-MM-DD`) | None |
| `--end` | `-e` | End date string (`YYYY-MM-DD`) | None |
| `--period` | `-p` | Period string if start/end omitted (`5d`, `1mo`, `1y`, `5y`) | `1y` |
| `--intervals` | `-i` | Interval list (`1m`, `5m`, `15m`, `1h`, `1d`, `1wk`) | `1d` |
| `--output-dir` | `-o` | Target repository directory | `./data` |
| `--format` | `-f` | Output file format (`csv`, `json`, `parquet`) | `csv` |
| `--no-refresh` | | Disable incremental merging with existing data files | False |
| `--verbose` | `-v` | Enable detailed logs | False |

---

## 🐍 Python API Usage

```python
from tickerrer import TickerDownloader, save_ticker_data, resolve_symbol

# 1. Resolve symbols & asset classes
info = resolve_symbol("gold")
print(info.name, info.ticker, info.asset_class)

# 2. Download ticker data
downloader = TickerDownloader()
data = downloader.download_symbol("gold", period="1y", intervals=["1d", "1h"])

# data is a dict: {'1d': DataFrame, '1h': DataFrame}
print(data["1d"].tail())

# 3. Save & refresh repository data
saved_paths = save_ticker_data(
    data_by_interval=data,
    symbol_info=info,
    output_dir="./data",
    file_format="csv",
    refresh=True # Merges new data with existing repository data seamlessly
)
print(saved_paths)
```

---

## 🔄 Repository Upkeep & Data Refreshing

When data refresh is executed, `tickerrer`:
1. Fetches the requested interval market data online.
2. Checks for existing data files in the target repository directory.
3. Automatically concatenates and deduplicates records by timestamp index.
4. Keeps the latest refreshed records and maintains sorted chronological order.

---

## 🧪 Running Tests

```bash
pytest --cov=tickerrer
```
