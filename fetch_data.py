"""
Download historical BTC candles for backtesting.

Two sources:
  --source binanceus  (default) -> BTCUSDT 5m, fast 1000/req pagination
  --source coinbase             -> BTC-USD, deeper book, 300/req pagination

Each 5-minute candle is one potential "up/down" bet: open vs. close tells us
which way that window resolved. Saved to data/btc_<interval>_<source>.parquet.

Usage:
    python fetch_data.py --source binanceus --interval 5m --days 730
    python fetch_data.py --source coinbase  --interval 5m --days 365
"""

import argparse
import os
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests

# ------------------------------- Binance.US -------------------------------
BINANCE = "https://api.binance.us/api/v3/klines"
BINANCE_SYMBOLS = ["BTCUSDT", "BTCUSD"]
BINANCE_INTERVAL_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000}
KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume",
              "close_time", "qv", "trades", "tb", "tq", "ig"]


def fetch_binance(interval, start_ms, end_ms):
    for symbol in BINANCE_SYMBOLS:
        print(f"Trying {symbol} ...")
        out, cursor = [], start_ms
        while cursor < end_ms:
            r = requests.get(BINANCE, params={
                "symbol": symbol, "interval": interval,
                "startTime": cursor, "endTime": end_ms, "limit": 1000}, timeout=15)
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            out.extend(batch)
            cursor = batch[-1][6] + 1
            if len(batch) < 1000:
                break
            time.sleep(0.12)
            print(f"  {symbol}: {len(out):>7} candles", end="\r")
        print()
        if out:
            df = pd.DataFrame(out, columns=KLINE_COLS)
            df["time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
            return _clean(df), symbol
    return None, None


# -------------------------------- Coinbase --------------------------------
COINBASE = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
CB_GRAN = {"1m": 60, "5m": 300, "15m": 900}  # seconds


def fetch_coinbase(interval, start_dt, end_dt):
    gran = CB_GRAN[interval]
    span = gran * 300                      # 300 candles per request
    out, cursor = [], start_dt
    headers = {"User-Agent": "btc-backtest"}
    while cursor < end_dt:
        win_end = min(cursor + timedelta(seconds=span), end_dt)
        r = requests.get(COINBASE, params={
            "granularity": gran,
            "start": cursor.isoformat(),
            "end": win_end.isoformat()}, headers=headers, timeout=15)
        r.raise_for_status()
        batch = r.json()  # [time, low, high, open, close, volume], newest first
        if batch:
            out.extend(batch)
            print(f"  coinbase: {len(out):>7} candles "
                  f"(through {win_end:%Y-%m-%d})", end="\r")
        cursor = win_end
        time.sleep(0.18)  # stay under the 10 req/s public limit
    print()
    if not out:
        return None, None
    df = pd.DataFrame(out, columns=["t", "low", "high", "open", "close", "volume"])
    df["time"] = pd.to_datetime(df["t"], unit="s", utc=True)
    return _clean(df), "BTC-USD"


# --------------------------------- shared ---------------------------------
def _clean(df):
    cols = ["open", "high", "low", "close", "volume"]
    for c in cols:
        df[c] = pd.to_numeric(df[c])
    df = df[["time"] + cols].set_index("time").sort_index()
    return df[~df.index.duplicated(keep="first")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="binanceus", choices=["binanceus", "coinbase"])
    ap.add_argument("--interval", default="5m")
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=args.days)

    if args.source == "binanceus":
        df, label = fetch_binance(
            args.interval, int(start.timestamp() * 1000), int(end.timestamp() * 1000))
    else:
        df, label = fetch_coinbase(args.interval, start, end)

    if df is None or df.empty:
        raise SystemExit("No data returned. Check connectivity / params.")

    os.makedirs("data", exist_ok=True)
    out = args.out or f"data/btc_{args.interval}_{args.source}.parquet"
    df.to_parquet(out)
    print(f"\nSaved {len(df):,} {args.interval} candles ({label}) "
          f"{df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d}\n  -> {out}")


if __name__ == "__main__":
    main()
