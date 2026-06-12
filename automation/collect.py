"""
automation/collect.py — serverless data collection (runs in GitHub Actions).

Replaces the local PC scheduled task. On each run it:
  1. fetches recent live BTC 5m candles (Coinbase primary, Binance.US fallback)
  2. resolves any pending paper trades whose 5-min window has closed
  3. opens a new paper trade from the latest closed candle (if composite_score fires)
  4. writes data/live_ledger.csv (persisted forward record, committed by the workflow)
     and data/live_results.json (a snapshot the dashboard + AI monitor read)

No PC required — GitHub Actions is the always-on engine.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval_engine as ee  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(BASE, "data", "live_ledger.csv")
RESULTS = os.path.join(BASE, "data", "live_results.json")
COST_BPS = 3.0
STRATEGY = "composite_score"
COLS = ["entry_time", "resolve_time", "signal", "entry_price",
        "resolve_price", "gross_bps", "pnl_bps", "source"]


def fetch_recent():
    """Coinbase primary (reliable from CI), Binance.US fallback. ~3 days of 5m."""
    try:
        end = datetime.now(timezone.utc); cur = end - timedelta(days=3); out = []
        while cur < end:
            we = min(cur + timedelta(seconds=300 * 300), end)
            r = requests.get("https://api.exchange.coinbase.com/products/BTC-USD/candles",
                             params={"granularity": 300, "start": cur.isoformat(),
                                     "end": we.isoformat()},
                             headers={"User-Agent": "btc-bot-ci"}, timeout=20)
            if r.ok:
                out += r.json()
            cur = we
        if out:
            df = pd.DataFrame(out, columns=["t", "low", "high", "open", "close", "volume"])
            df["time"] = pd.to_datetime(df["t"], unit="s", utc=True)
            for c in ["open", "high", "low", "close", "volume"]:
                df[c] = pd.to_numeric(df[c])
            return df.set_index("time").sort_index()[
                ["open", "high", "low", "close", "volume"]], "Coinbase"
    except Exception as e:
        print("coinbase failed:", e)
    r = requests.get("https://api.binance.us/api/v3/klines",
                     params={"symbol": "BTCUSDT", "interval": "5m", "limit": 1000}, timeout=20)
    r.raise_for_status()
    df = pd.DataFrame(r.json(), columns=["t", "open", "high", "low", "close",
                                         "volume", *[f"_{i}" for i in range(6)]])
    df["time"] = pd.to_datetime(df["t"], unit="ms", utc=True)
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c])
    return df.set_index("time")[["open", "high", "low", "close", "volume"]], "Binance.US"


def main():
    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    df, source = fetch_recent()
    sig = np.asarray(ee.ALL_STRATEGIES[STRATEGY](df))

    led = (pd.read_csv(LEDGER, parse_dates=["entry_time", "resolve_time"])
           if os.path.exists(LEDGER) else pd.DataFrame(columns=COLS))

    # 1) resolve pending trades whose resolve candle now exists
    close_at = df["close"]
    for i, row in led[led["pnl_bps"].isna()].iterrows():
        rt = pd.Timestamp(row["resolve_time"])
        if rt in close_at.index:
            rp = float(close_at.loc[rt])
            gross = row["signal"] * (rp / row["entry_price"] - 1) * 1e4
            led.at[i, "resolve_price"] = rp
            led.at[i, "gross_bps"] = gross
            led.at[i, "pnl_bps"] = gross - COST_BPS

    # 2) open a new trade from the latest CLOSED candle (idempotent on entry_time)
    entry_time = df.index[-2]
    s = int(sig[-2])
    if s != 0 and not (led["entry_time"] == entry_time).any():
        rec = {"entry_time": entry_time, "resolve_time": entry_time + timedelta(minutes=5),
               "signal": s, "entry_price": float(df["close"].iloc[-2]),
               "resolve_price": np.nan, "gross_bps": np.nan, "pnl_bps": np.nan,
               "source": source}
        led = pd.concat([led, pd.DataFrame([rec])], ignore_index=True) if len(led) else pd.DataFrame([rec])

    led = led[COLS]
    led.to_csv(LEDGER, index=False)

    # 3) snapshot for the dashboard + AI monitor
    res = ee.evaluate_spot(df, sig, COST_BPS)
    done = led.dropna(subset=["pnl_bps"])
    eq = done["pnl_bps"].cumsum() if len(done) else pd.Series(dtype=float)
    snapshot = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": source,
        "price": round(float(df["close"].iloc[-1]), 2),
        "signal": int(sig[-2]),
        "window": {"bets": res["all"]["bets"], "win": round(res["all"]["win"], 4),
                   "net_bps": round(res["all"]["net_bps"], 3),
                   "gross_bps": round(res["all"]["gross_bps"], 3), "cost_bps": COST_BPS},
        "ledger": {"trades": len(led), "resolved": len(done),
                   "win": round(float((done["pnl_bps"] > 0).mean()), 4) if len(done) else None,
                   "net_bps_mean": round(float(done["pnl_bps"].mean()), 3) if len(done) else None,
                   "total_bps": round(float(done["pnl_bps"].sum()), 1) if len(done) else 0.0},
        "recent_trades": done.tail(20).assign(
            entry_time=lambda d: d["entry_time"].astype(str),
            resolve_time=lambda d: d["resolve_time"].astype(str)).to_dict("records"),
    }
    with open(RESULTS, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"[{source}] price={snapshot['price']} signal={snapshot['signal']} "
          f"ledger={len(led)} resolved={len(done)} "
          f"net={snapshot['ledger']['net_bps_mean']} bps/trade")


if __name__ == "__main__":
    main()
