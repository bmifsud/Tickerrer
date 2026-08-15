import pytest
from tickerrer.symbols import resolve_symbol, AssetClass, KNOWN_SYMBOLS

def test_resolve_known_symbols():
    info_ndx = resolve_symbol("ndx")
    assert info_ndx.ticker == "^NDX"
    assert info_ndx.asset_class == AssetClass.INDEX

    info_gold = resolve_symbol("gold")
    assert info_gold.ticker == "GC=F"
    assert info_gold.asset_class == AssetClass.COMMODITY

    info_eurusd = resolve_symbol("eurusd")
    assert info_eurusd.ticker == "EURUSD=X"
    assert info_eurusd.asset_class == AssetClass.FOREX

    info_btc = resolve_symbol("btc")
    assert info_btc.ticker == "BTC-USD"
    assert info_btc.asset_class == AssetClass.CRYPTO
    assert info_btc.binance_ticker == "BTCUSDT"

    info_us30 = resolve_symbol("us30")
    assert info_us30.asset_class == AssetClass.CFD

def test_resolve_heuristics():
    info_forex = resolve_symbol("GBPUSD")
    assert info_forex.ticker == "GBPUSD=X"
    assert info_forex.asset_class == AssetClass.FOREX

    info_crypto = resolve_symbol("SOL-USD")
    assert info_crypto.ticker == "SOL-USD"
    assert info_crypto.asset_class == AssetClass.CRYPTO

    info_custom_equity = resolve_symbol("tsla", override_asset_class=AssetClass.EQUITY)
    assert info_custom_equity.asset_class == AssetClass.EQUITY
