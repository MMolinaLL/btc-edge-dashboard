"""
paper_trader.py — forward, out-of-sample paper trading.

This is how we learn from REALITY instead of a curve-fit. Each run:
  1. resolves any pending trades whose 5-minute window has closed
  2. opens a new paper trade from the latest *closed* candle's signal (if any)
All trades append to data/paper_ledger.csv with realized P&L net of a cost model.

Modes:
  --replay-days N   seed the ledger by replaying the last N days of real candles
                    (out-of-sample forward simulation on recent data) -- gives the
                    dashboard immediate, honest content.
  (default)         "live" tick: resolve dues + open one new trade from fresh data.

Intended to run on a 5-minute schedule for genuine live forward testing.

Usage:
    python paper_trader.py --replay-days 5            # seed
    python paper_trader.py                            # one live tick
    python paper_trader.py --strategy meanrev_3 --cost-bps 3
"""
import argparse
import os
from datetime import timedelta, datetime, timezone

import numpy as np
import pandas as pd
import requests

import eval_engine as ee

BASE = os.path.dirname(os.path.abspath(__file__))
BINANCE = "https://api.binance.us/api/v3/klines"
LEDGER = os.path.join(BASE, "data", "paper_ledger.csv")
RUNLOG = os.path.join(BASE, "data", "paper_runs.log")
COLS = ["entry_time", "resolve_time", "strategy", "mode", "signal",
        "entry_price", "resolve_price", "gross_bps", "cost_bps", "pnl_bps"]


def fetch_klines(symbol="BTCUSDT", interval="5m", limit=500):
    r = requests.get(BINANCE, params={"symbol": symbol, "interval": interval,
                                      "limit": limit}, timeout=15)
    r.raise_for_status()
    rows = r.json()
    df = pd.DataFrame(rows, columns=["open_time", "open", "high", "low", "close",
                                     "volume", "close_time", *["_"] * 5])
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c])
    df["time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    return df.set_index("time")[["open", "high", "low", "close"]]


def load_ledger():
    if os.path.exists(LEDGER):
        return pd.read_csv(LEDGER, parse_dates=["entry_time", "resolve_time"])
    return pd.DataFrame(columns=COLS)


def signal_at(df, strategy, idx):
    sig = np.asarray(ee.ALL_STRATEGIES[strategy](df))
    return int(sig[idx])


def resolve_pending(led, df, cost_bps):
    """Fill in realized P&L for trades whose resolve candle now exists."""
    price_at = df["close"]
    for i, row in led[led["pnl_bps"].isna()].iterrows():
        rt = pd.Timestamp(row["resolve_time"])
        # the candle whose open_time == resolve_time holds the resolve close
        if rt in price_at.index:
            rp = float(price_at.loc[rt])
            gross = row["signal"] * (rp / row["entry_price"] - 1) * 1e4
            led.at[i, "resolve_price"] = rp
            led.at[i, "gross_bps"] = gross
            led.at[i, "pnl_bps"] = gross - row["cost_bps"]
    return led


def open_trade(led, df, strategy, cost_bps, mode, entry_idx):
    """Open a paper trade from a closed candle at position entry_idx."""
    entry_time = df.index[entry_idx]
    if ((led["entry_time"] == entry_time) & (led["strategy"] == strategy)).any():
        return led  # idempotent: already logged this candle
    sig = signal_at(df, strategy, entry_idx)
    if sig == 0:
        return led  # strategy chose not to bet this candle
    rec = {
        "entry_time": entry_time,
        "resolve_time": entry_time + timedelta(minutes=5),
        "strategy": strategy, "mode": mode, "signal": sig,
        "entry_price": float(df["close"].iloc[entry_idx]),
        "resolve_price": np.nan, "gross_bps": np.nan,
        "cost_bps": cost_bps, "pnl_bps": np.nan,
    }
    new = pd.DataFrame([rec])
    return new if led.empty else pd.concat([led, new], ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", default="meanrev_volfilter")
    ap.add_argument("--cost-bps", type=float, default=3.0,
                    help="realistic per-trade cost (spread+fee). Default 3 = maker-ish.")
    ap.add_argument("--replay-days", type=int, default=0)
    args = ap.parse_args()

    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    df = fetch_klines(limit=1000)
    led = load_ledger()

    if args.replay_days > 0:
        # forward-simulate over recent closed candles (need history for the signal)
        n = min(len(df) - 2, args.replay_days * 288)
        start = len(df) - 1 - n
        for idx in range(max(30, start), len(df) - 1):
            led = open_trade(led, df, args.strategy, args.cost_bps, "replay", idx)
        led = resolve_pending(led, df, args.cost_bps)
        print(f"Replay seeded {n} candles for {args.strategy}.")
    else:
        led = resolve_pending(led, df, args.cost_bps)
        led = open_trade(led, df, args.strategy, args.cost_bps, "live", len(df) - 2)
        print(f"Live tick: opened from candle {df.index[-2]} (if signal != 0).")

    led = led[COLS]
    led.to_csv(LEDGER, index=False)
    done = led.dropna(subset=["pnl_bps"])
    net = done["pnl_bps"].mean() if len(done) else float("nan")
    with open(RUNLOG, "a") as f:
        f.write(f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}Z  {args.strategy}  "
                f"trades={len(led)} resolved={len(done)} net={net:+.2f}bps\n")
    print(f"Ledger: {len(led)} trades, {len(done)} resolved.")
    if len(done):
        print(f"  win rate: {(done['pnl_bps']>0).mean()*100:.1f}%   "
              f"net: {done['pnl_bps'].mean():+.2f} bps/trade   "
              f"total: {done['pnl_bps'].sum():+.1f} bps")
        print(f"  (gross before cost: {done['gross_bps'].mean():+.2f} bps/trade "
              f"at cost {args.cost_bps} bps)")


if __name__ == "__main__":
    main()
