"""Symbol resolution and asset classification for tickerrer."""

from enum import Enum
from typing import NamedTuple, Dict, Optional


class AssetClass(str, Enum):
    INDEX = "indexes"
    EQUITY = "equity"
    COMMODITY = "commodities"
    ETF = "etfs"
    FOREX = "forex"
    CRYPTO = "crypto"
    CFD = "cfd"


class SymbolInfo(NamedTuple):
    query_symbol: str        # The raw query or alias input (e.g. "ndx", "gold")
    ticker: str              # The mapped default yfinance/standard ticker (e.g. "^NDX", "GC=F")
    asset_class: AssetClass  # Categorization
    name: str                # Human friendly name
    stooq_ticker: Optional[str] = None     # Stooq ticker mapping
    binance_ticker: Optional[str] = None   # Binance ticker mapping
    forex_pair: Optional[tuple] = None     # Forex currency pair (base, quote)


KNOWN_SYMBOLS: Dict[str, SymbolInfo] = {
    # Indexes
    "ndx": SymbolInfo("ndx", "^NDX", AssetClass.INDEX, "Nasdaq 100 Index", stooq_ticker="^ndx"),
    "^ndx": SymbolInfo("^ndx", "^NDX", AssetClass.INDEX, "Nasdaq 100 Index", stooq_ticker="^ndx"),
    "spx": SymbolInfo("spx", "^GSPC", AssetClass.INDEX, "S&P 500 Index", stooq_ticker="^spx"),
    "gspc": SymbolInfo("gspc", "^GSPC", AssetClass.INDEX, "S&P 500 Index", stooq_ticker="^spx"),
    "^gspc": SymbolInfo("^gspc", "^GSPC", AssetClass.INDEX, "S&P 500 Index", stooq_ticker="^spx"),
    "dji": SymbolInfo("dji", "^DJI", AssetClass.INDEX, "Dow Jones Industrial Average", stooq_ticker="^dji"),
    "^dji": SymbolInfo("^dji", "^DJI", AssetClass.INDEX, "Dow Jones Industrial Average", stooq_ticker="^dji"),
    "rut": SymbolInfo("rut", "^RUT", AssetClass.INDEX, "Russell 2000 Index", stooq_ticker="^rut"),
    "^rut": SymbolInfo("^rut", "^RUT", AssetClass.INDEX, "Russell 2000 Index", stooq_ticker="^rut"),
    "vix": SymbolInfo("vix", "^VIX", AssetClass.INDEX, "CBOE Volatility Index", stooq_ticker="^vix"),
    "^vix": SymbolInfo("^vix", "^VIX", AssetClass.INDEX, "CBOE Volatility Index", stooq_ticker="^vix"),
    "ftse": SymbolInfo("ftse", "^FTSE", AssetClass.INDEX, "FTSE 100 Index", stooq_ticker="^ukx"),
    "^ftse": SymbolInfo("^ftse", "^FTSE", AssetClass.INDEX, "FTSE 100 Index", stooq_ticker="^ukx"),
    "dax": SymbolInfo("dax", "^GDAXI", AssetClass.INDEX, "DAX Performance Index", stooq_ticker="^dax"),
    "^gdaxi": SymbolInfo("^gdaxi", "^GDAXI", AssetClass.INDEX, "DAX Performance Index", stooq_ticker="^dax"),
    "nikkei": SymbolInfo("nikkei", "^N225", AssetClass.INDEX, "Nikkei 225", stooq_ticker="^nkx"),
    "^n225": SymbolInfo("^n225", "^N225", AssetClass.INDEX, "Nikkei 225", stooq_ticker="^nkx"),

    # Equities (popular examples)
    "aapl": SymbolInfo("aapl", "AAPL", AssetClass.EQUITY, "Apple Inc.", stooq_ticker="aapl.us"),
    "msft": SymbolInfo("msft", "MSFT", AssetClass.EQUITY, "Microsoft Corporation", stooq_ticker="msft.us"),
    "googl": SymbolInfo("googl", "GOOGL", AssetClass.EQUITY, "Alphabet Inc.", stooq_ticker="googl.us"),
    "amzn": SymbolInfo("amzn", "AMZN", AssetClass.EQUITY, "Amazon.com Inc.", stooq_ticker="amzn.us"),
    "nvda": SymbolInfo("nvda", "NVDA", AssetClass.EQUITY, "NVIDIA Corporation", stooq_ticker="nvda.us"),
    "tsla": SymbolInfo("tsla", "TSLA", AssetClass.EQUITY, "Tesla Inc.", stooq_ticker="tsla.us"),

    # Commodities (Futures / Spot)
    "gold": SymbolInfo("gold", "GC=F", AssetClass.COMMODITY, "Gold Futures", stooq_ticker="xauusd"),
    "gc=f": SymbolInfo("gc=f", "GC=F", AssetClass.COMMODITY, "Gold Futures", stooq_ticker="xauusd"),
    "silver": SymbolInfo("silver", "SI=F", AssetClass.COMMODITY, "Silver Futures", stooq_ticker="xagusd"),
    "si=f": SymbolInfo("si=f", "SI=F", AssetClass.COMMODITY, "Silver Futures", stooq_ticker="xagusd"),
    "oil": SymbolInfo("oil", "CL=F", AssetClass.COMMODITY, "Crude Oil Futures", stooq_ticker="cl.f"),
    "cl=f": SymbolInfo("cl=f", "CL=F", AssetClass.COMMODITY, "Crude Oil Futures", stooq_ticker="cl.f"),
    "brent": SymbolInfo("brent", "BZ=F", AssetClass.COMMODITY, "Brent Crude Oil Futures", stooq_ticker="cb.f"),
    "bz=f": SymbolInfo("bz=f", "BZ=F", AssetClass.COMMODITY, "Brent Crude Oil Futures", stooq_ticker="cb.f"),
    "ng": SymbolInfo("ng", "NG=F", AssetClass.COMMODITY, "Natural Gas Futures", stooq_ticker="ng.f"),
    "ng=f": SymbolInfo("ng=f", "NG=F", AssetClass.COMMODITY, "Natural Gas Futures", stooq_ticker="ng.f"),
    "copper": SymbolInfo("copper", "HG=F", AssetClass.COMMODITY, "Copper Futures", stooq_ticker="hg.f"),

    # ETFs
    "spy": SymbolInfo("spy", "SPY", AssetClass.ETF, "SPDR S&P 500 ETF Trust", stooq_ticker="spy.us"),
    "qqq": SymbolInfo("qqq", "QQQ", AssetClass.ETF, "Invesco QQQ Trust", stooq_ticker="qqq.us"),
    "iwm": SymbolInfo("iwm", "IWM", AssetClass.ETF, "iShares Russell 2000 ETF", stooq_ticker="iwm.us"),
    "dia": SymbolInfo("dia", "DIA", AssetClass.ETF, "SPDR Dow Jones Industrial Average ETF", stooq_ticker="dia.us"),
    "vti": SymbolInfo("vti", "VTI", AssetClass.ETF, "Vanguard Total Stock Market ETF", stooq_ticker="vti.us"),
    "gld": SymbolInfo("gld", "GLD", AssetClass.ETF, "SPDR Gold Shares", stooq_ticker="gld.us"),
    "slv": SymbolInfo("slv", "SLV", AssetClass.ETF, "iShares Silver Trust", stooq_ticker="slv.us"),

    # Forex
    "eurusd": SymbolInfo("eurusd", "EURUSD=X", AssetClass.FOREX, "EUR/USD", stooq_ticker="eurusd", forex_pair=("EUR", "USD")),
    "eurusd=x": SymbolInfo("eurusd=x", "EURUSD=X", AssetClass.FOREX, "EUR/USD", stooq_ticker="eurusd", forex_pair=("EUR", "USD")),
    "gbpusd": SymbolInfo("gbpusd", "GBPUSD=X", AssetClass.FOREX, "GBP/USD", stooq_ticker="gbpusd", forex_pair=("GBP", "USD")),
    "gbpusd=x": SymbolInfo("gbpusd=x", "GBPUSD=X", AssetClass.FOREX, "GBP/USD", stooq_ticker="gbpusd", forex_pair=("GBP", "USD")),
    "usdjpy": SymbolInfo("usdjpy", "USDJPY=X", AssetClass.FOREX, "USD/JPY", stooq_ticker="usdjpy", forex_pair=("USD", "JPY")),
    "usdjpy=x": SymbolInfo("usdjpy=x", "USDJPY=X", AssetClass.FOREX, "USD/JPY", stooq_ticker="usdjpy", forex_pair=("USD", "JPY")),
    "audusd": SymbolInfo("audusd", "AUDUSD=X", AssetClass.FOREX, "AUD/USD", stooq_ticker="audusd", forex_pair=("AUD", "USD")),
    "usdcad": SymbolInfo("usdcad", "USDCAD=X", AssetClass.FOREX, "USD/CAD", stooq_ticker="usdcad", forex_pair=("USD", "CAD")),
    "usdchf": SymbolInfo("usdchf", "USDCHF=X", AssetClass.FOREX, "USD/CHF", stooq_ticker="usdchf", forex_pair=("USD", "CHF")),
    "nzdusd": SymbolInfo("nzdusd", "NZDUSD=X", AssetClass.FOREX, "NZD/USD", stooq_ticker="nzdusd", forex_pair=("NZD", "USD")),

    # Crypto
    "btc": SymbolInfo("btc", "BTC-USD", AssetClass.CRYPTO, "Bitcoin USD", binance_ticker="BTCUSDT"),
    "btc-usd": SymbolInfo("btc-usd", "BTC-USD", AssetClass.CRYPTO, "Bitcoin USD", binance_ticker="BTCUSDT"),
    "btcusd": SymbolInfo("btcusd", "BTC-USD", AssetClass.CRYPTO, "Bitcoin USD", binance_ticker="BTCUSDT"),
    "eth": SymbolInfo("eth", "ETH-USD", AssetClass.CRYPTO, "Ethereum USD", binance_ticker="ETHUSDT"),
    "eth-usd": SymbolInfo("eth-usd", "ETH-USD", AssetClass.CRYPTO, "Ethereum USD", binance_ticker="ETHUSDT"),
    "ethusd": SymbolInfo("ethusd", "ETH-USD", AssetClass.CRYPTO, "Ethereum USD", binance_ticker="ETHUSDT"),
    "sol": SymbolInfo("sol", "SOL-USD", AssetClass.CRYPTO, "Solana USD", binance_ticker="SOLUSDT"),
    "sol-usd": SymbolInfo("sol-usd", "SOL-USD", AssetClass.CRYPTO, "Solana USD", binance_ticker="SOLUSDT"),
    "xrp": SymbolInfo("xrp", "XRP-USD", AssetClass.CRYPTO, "XRP USD", binance_ticker="XRPUSDT"),

    # Common CFDs / Synthetic instruments
    "us30": SymbolInfo("us30", "^DJI", AssetClass.CFD, "US 30 Index CFD", stooq_ticker="^dji"),
    "us500": SymbolInfo("us500", "^GSPC", AssetClass.CFD, "US 500 Index CFD", stooq_ticker="^spx"),
    "nas100": SymbolInfo("nas100", "^NDX", AssetClass.CFD, "US Tech 100 CFD", stooq_ticker="^ndx"),
    "uk100": SymbolInfo("uk100", "^FTSE", AssetClass.CFD, "UK 100 CFD", stooq_ticker="^ukx"),
    "ger40": SymbolInfo("ger40", "^GDAXI", AssetClass.CFD, "Germany 40 CFD", stooq_ticker="^dax"),
    "xauusd": SymbolInfo("xauusd", "GC=F", AssetClass.CFD, "Gold / USD CFD", stooq_ticker="xauusd"),
    "xagusd": SymbolInfo("xagusd", "SI=F", AssetClass.CFD, "Silver / USD CFD", stooq_ticker="xagusd"),
}


def resolve_symbol(raw_symbol: str, override_asset_class: Optional[AssetClass] = None) -> SymbolInfo:
    """
    Resolves a raw user input symbol (e.g. "ndx", "aapl", "gold", "eurusd") into a SymbolInfo instance.
    """
    cleaned = raw_symbol.strip().lower()

    if cleaned in KNOWN_SYMBOLS:
        info = KNOWN_SYMBOLS[cleaned]
        if override_asset_class is not None:
            return SymbolInfo(
                info.query_symbol, info.ticker, override_asset_class, info.name,
                stooq_ticker=info.stooq_ticker, binance_ticker=info.binance_ticker, forex_pair=info.forex_pair
            )
        return info

    ticker = raw_symbol.strip().upper()

    # Index heuristic
    if ticker.startswith("^"):
        ac = override_asset_class or AssetClass.INDEX
        return SymbolInfo(raw_symbol, ticker, ac, f"Index {ticker}", stooq_ticker=cleaned)

    # Forex heuristic: ending in =X or 6-letter currency pair
    if ticker.endswith("=X"):
        base, quote = ticker[:3], ticker[3:6]
        ac = override_asset_class or AssetClass.FOREX
        return SymbolInfo(raw_symbol, ticker, ac, f"Forex {ticker}", stooq_ticker=ticker.lower().replace("=x", ""), forex_pair=(base, quote))

    if len(ticker) == 6 and ticker.isalpha():
        currencies = {"USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "NZD", "CNY", "HKD", "XAU", "XAG"}
        c1, c2 = ticker[:3], ticker[3:]
        if c1 in currencies and c2 in currencies:
            ac = override_asset_class or AssetClass.FOREX
            return SymbolInfo(raw_symbol, f"{ticker}=X", ac, f"Forex {c1}/{c2}", stooq_ticker=ticker.lower(), forex_pair=(c1, c2))

    # Crypto heuristic: ends with -USD or -EUR
    if "-" in ticker and any(ticker.endswith(f"-{quote}") for quote in ["USD", "USDT", "EUR", "BTC"]):
        ac = override_asset_class or AssetClass.CRYPTO
        symbol_base = ticker.split("-")[0]
        binance = f"{symbol_base}USDT"
        return SymbolInfo(raw_symbol, ticker, ac, f"Crypto {ticker}", binance_ticker=binance)

    # Commodity / Futures heuristic
    if ticker.endswith("=F"):
        ac = override_asset_class or AssetClass.COMMODITY
        return SymbolInfo(raw_symbol, ticker, ac, f"Commodity Futures {ticker}")

    # Default fallback to Equity (or user specified)
    ac = override_asset_class or AssetClass.EQUITY
    stooq_t = f"{cleaned}.us" if "." not in cleaned else cleaned
    return SymbolInfo(raw_symbol, ticker, ac, f"Equity {ticker}", stooq_ticker=stooq_t)
