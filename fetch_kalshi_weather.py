"""
Fetch settled Kalshi daily-high-temperature markets + their price history.

For a city series (default NYC = KXHIGHNY), pull every settled bucket market over
the last N days, parse its temperature range from the subtitle, grab hourly price
candlesticks across the market's life, and save a long-format table:

    date, event, ticker, lo, hi, kind, result, ts, bid, ask, mid, last, volume, oi

where `kind` is 'range' / 'above' / 'below' and (lo, hi) bound the bucket in °F
(open-ended sides use -inf / +inf). One row per (market, hourly candle).

Public API, no auth required.

Usage:
    python fetch_kalshi_weather.py --series KXHIGHNY --days 60
"""
import argparse
import re
import time
from datetime import datetime, timezone

import pandas as pd
import requests

BASE = "https://api.elections.kalshi.com/trade-api/v2"
H = {"User-Agent": "weather-backtest", "Accept": "application/json"}


def get(path, **params):
    for attempt in range(4):
        r = requests.get(BASE + path, params=params, headers=H, timeout=25)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429:
            time.sleep(1.0 + attempt)
            continue
        r.raise_for_status()
    r.raise_for_status()


def parse_range(sub: str):
    """'81° to 82°' -> (81,82,'range'); '83° or above' -> (83,inf,'above');
       '74° or below' -> (-inf,74,'below')."""
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", sub)]
    s = sub.lower()
    if "above" in s or "higher" in s or "greater" in s:
        return (nums[0], float("inf"), "above")
    if "below" in s or "lower" in s or "less" in s:
        return (float("-inf"), nums[0], "below")
    if len(nums) >= 2:
        return (nums[0], nums[1], "range")
    return (nums[0] if nums else float("nan"),
            nums[0] if nums else float("nan"), "point")


def list_settled_markets(series, days):
    """Paginate /markets for the series, keep settled markets in the window."""
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    out, cursor = [], None
    while True:
        page = get("/markets", series_ticker=series, status="settled",
                   limit=1000, cursor=cursor)
        ms = page.get("markets", [])
        for m in ms:
            ct = m.get("close_time")
            if not ct:
                continue
            cts = datetime.fromisoformat(ct.replace("Z", "+00:00")).timestamp()
            if cts >= cutoff:
                out.append(m)
        cursor = page.get("cursor")
        if not cursor or not ms:
            break
        # stop early if the whole page is older than the cutoff
        oldest = min(datetime.fromisoformat(
            m["close_time"].replace("Z", "+00:00")).timestamp()
            for m in ms if m.get("close_time"))
        if oldest < cutoff:
            break
    return out


def candles(series, ticker, start_ts, end_ts, period=60):
    j = get(f"/series/{series}/markets/{ticker}/candlesticks",
            start_ts=start_ts, end_ts=end_ts, period_interval=period)
    return j.get("candlesticks", [])


def fnum(d, k):
    v = d.get(k)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default="KXHIGHNY")
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--period", type=int, default=60, help="candle minutes: 1/60/1440")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    print(f"Listing settled {args.series} markets, last {args.days} days ...")
    markets = list_settled_markets(args.series, args.days)
    # date code from ticker, e.g. KXHIGHNY-26JUN10-B81.5 -> 26JUN10
    def datecode(t):
        parts = t.split("-")
        return parts[1] if len(parts) > 1 else "?"
    days = sorted(set(datecode(m["ticker"]) for m in markets))
    print(f"  {len(markets)} markets across {len(days)} days: "
          f"{days[0]} .. {days[-1]}")

    rows = []
    for i, m in enumerate(markets):
        ticker = m["ticker"]
        sub = m.get("yes_sub_title") or m.get("subtitle") or ""
        lo, hi, kind = parse_range(sub)
        close_ts = int(datetime.fromisoformat(
            m["close_time"].replace("Z", "+00:00")).timestamp())
        open_iso = m.get("open_time")
        open_ts = (int(datetime.fromisoformat(open_iso.replace("Z", "+00:00"))
                       .timestamp()) if open_iso else close_ts - 3 * 86400)
        result = m.get("result")
        try:
            cs = candles(args.series, ticker, open_ts, close_ts, args.period)
        except Exception as e:
            print(f"  ! {ticker}: candles failed ({e})")
            cs = []
        for c in cs:
            yb = c.get("yes_bid", {}) or {}
            ya = c.get("yes_ask", {}) or {}
            pr = c.get("price", {}) or {}
            bid = fnum(yb, "close_dollars")
            ask = fnum(ya, "close_dollars")
            mid = (bid + ask) / 2 if (bid is not None and ask is not None) else None
            rows.append({
                "date": datecode(ticker),
                "event": m.get("event_ticker"),
                "ticker": ticker,
                "lo": lo, "hi": hi, "kind": kind,
                "result": result,
                "ts": c.get("end_period_ts"),
                "bid": bid, "ask": ask, "mid": mid,
                "last": fnum(pr, "close_dollars"),
                "volume": fnum(c, "volume_fp"),
                "oi": fnum(c, "open_interest_fp"),
            })
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(markets)} markets, {len(rows)} candle-rows", end="\r")
        time.sleep(0.05)
    print()

    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No candle rows collected.")
    df["dt"] = pd.to_datetime(df["ts"], unit="s", utc=True)
    out = args.out or f"data/kalshi_{args.series.lower()}_{args.period}m.parquet"
    import os
    os.makedirs("data", exist_ok=True)
    df.to_parquet(out)
    print(f"Saved {len(df):,} candle-rows for {df['ticker'].nunique()} markets "
          f"({df['date'].nunique()} days)\n  -> {out}")


if __name__ == "__main__":
    main()
