"""
Probe the Kalshi public API (no auth) to confirm we can:
  1. reach the API
  2. list settled NYC daily-high-temperature markets
  3. pull historical price candlesticks for one of them

If all three work, the weather strategy is backtestable end-to-end for free.
"""
import json
import requests

HOSTS = [
    "https://api.kalshi.com/trade-api/v2",
    "https://api.elections.kalshi.com/trade-api/v2",
]
SERIES = "KXHIGHNY"  # daily high temperature, New York City
H = {"User-Agent": "btc-backtest-probe", "Accept": "application/json"}


def get(base, path, **params):
    r = requests.get(base + path, params=params, headers=H, timeout=20)
    return r


def main():
    base = None
    for b in HOSTS:
        try:
            r = get(b, "/exchange/status")
            print(f"{b}/exchange/status -> {r.status_code}  {r.text[:120]}")
            if r.status_code == 200:
                base = b
                break
        except Exception as e:
            print(f"{b} -> ERROR {e}")
    if not base:
        raise SystemExit("Could not reach any Kalshi host.")

    print(f"\nUsing base: {base}\n")

    # 1) list settled markets in the NYC high-temp series
    r = get(base, "/markets", series_ticker=SERIES, status="settled", limit=20)
    print(f"GET /markets?series_ticker={SERIES}&status=settled -> {r.status_code}")
    if r.status_code != 200:
        print(r.text[:400]); return
    markets = r.json().get("markets", [])
    print(f"  got {len(markets)} settled markets")
    if not markets:
        # try without status filter to see what's there
        r2 = get(base, "/markets", series_ticker=SERIES, limit=20)
        print(f"  retry no-status -> {r2.status_code}; "
              f"{len(r2.json().get('markets', []))} markets")
        markets = r2.json().get("markets", [])
    for m in markets[:8]:
        print(f"    {m['ticker']:<28} result={m.get('result','?'):<4} "
              f"close={m.get('close_time','?')[:10]}  "
              f"yes_bid={m.get('yes_bid')} yes_ask={m.get('yes_ask')} "
              f"sub='{m.get('yes_sub_title', m.get('subtitle',''))}'")

    if not markets:
        return

    print("\nAll keys on a market object:")
    print(" ", sorted(markets[0].keys()))

    # 2) pull candlesticks for one settled market that actually traded.
    # Pick the bucket that settled 'yes' (the winning range) for a real series.
    from datetime import datetime, timezone
    m = next((x for x in markets if x.get("result") == "yes"), markets[0])
    ticker = m["ticker"]
    close_iso = m.get("close_time")
    close_ts = int(datetime.fromisoformat(
        close_iso.replace("Z", "+00:00")).timestamp())
    start_ts = close_ts - 3 * 24 * 3600  # 3 days of history before settlement
    path = f"/series/{SERIES}/markets/{ticker}/candlesticks"
    print(f"\nPulling candlesticks for {ticker} "
          f"(settled {m.get('result')}, '{m.get('yes_sub_title','')}')")
    r = get(base, path, start_ts=start_ts, end_ts=close_ts, period_interval=60)
    print(f"\nGET {path} (1h) -> {r.status_code}")
    if r.status_code == 200:
        cs = r.json().get("candlesticks", [])
        print(f"  {len(cs)} hourly candlesticks for {ticker}")
        if cs:
            print("  first:", json.dumps(cs[0])[:300])
            print("  last: ", json.dumps(cs[-1])[:300])
    else:
        print("  body:", r.text[:400])


if __name__ == "__main__":
    main()
