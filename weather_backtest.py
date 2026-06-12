"""
Backtest: intraday-convergence edge on Kalshi NYC daily-high-temp markets.

Idea: as the day progresses, observed temperatures pin down the eventual daily
high. A model that knows the running max + the climatological distribution of
"how much higher it still gets by this hour" can price each temperature bucket.
We bet only when our probability beats the market quote by more than the cost to
trade (exact taker fee 0.07*p*(1-p) + crossing the spread).

No look-ahead: at decision time we use ONLY observations at/before that instant,
and the market quote at/before that instant. Settlement uses the real outcome.

Controls:
  - "no_info" mode sets model P = market mid (zero edge). It should LOSE roughly
    the fee+spread on every bet, proving the harness charges costs honestly.

Usage:
    python weather_backtest.py
    python weather_backtest.py --edge 0.05 --hours 12,14,16,18
"""
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

UTC = ZoneInfo("UTC")
MONTHS = dict(JAN=1, FEB=2, MAR=3, APR=4, MAY=5, JUN=6,
              JUL=7, AUG=8, SEP=9, OCT=10, NOV=11, DEC=12)


def parse_datecode(code):
    # '26MAY31' -> date(2026,5,31)
    yy = 2000 + int(code[:2])
    mm = MONTHS[code[2:5]]
    dd = int(code[5:])
    return datetime(yy, mm, dd).date()


def in_bucket(high, lo, hi, kind):
    if kind == "above":
        return high >= lo
    if kind == "below":
        return high <= hi
    # range buckets are integer-degree ranges like 81..82 -> high in {81,82}
    return lo - 0.5 <= high <= hi + 0.5


def build_residual_climatology(obs, tz, hours):
    """For each decision hour, the empirical distribution of (final_high - rmax_so_far)."""
    obs = obs.copy()
    obs["local"] = pd.to_datetime(obs["valid"])  # already local naive
    obs["d"] = obs["local"].dt.date
    obs["h"] = obs["local"].dt.hour
    resid = {h: [] for h in hours}
    for d, g in obs.groupby("d"):
        g = g.sort_values("local")
        final_high = g["tmpf"].max()
        for h in hours:
            upto = g[g["h"] <= h]
            if upto.empty:
                continue
            rmax = upto["tmpf"].max()
            resid[h].append(final_high - rmax)
    return {h: np.array(v) for h, v in resid.items() if len(v) >= 10}


def rmax_at(obs_day, h):
    upto = obs_day[obs_day["h"] <= h]
    return upto["tmpf"].max() if not upto.empty else None


def model_prob(rmax, residual_samples, lo, hi, kind):
    highs = rmax + residual_samples            # possible final highs
    if kind == "above":
        return float(np.mean(highs >= lo))
    if kind == "below":
        return float(np.mean(highs <= hi))
    return float(np.mean((highs >= lo - 0.5) & (highs <= hi + 0.5)))


def taker_fee(price):
    return 0.07 * price * (1.0 - price)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", default="data/kalshi_kxhighny_60m.parquet")
    ap.add_argument("--obs", default="data/obs_nyc.parquet")
    ap.add_argument("--tz", default="America/New_York")
    ap.add_argument("--hours", default="10,12,13,14,15,16,17,18")
    ap.add_argument("--edge", type=float, default=0.04,
                    help="min model_EV (after fees) to place a bet")
    ap.add_argument("--no_info", action="store_true",
                    help="control: set model P = market mid (should lose ~costs)")
    args = ap.parse_args()

    tz = ZoneInfo(args.tz)
    hours = [int(x) for x in args.hours.split(",")]

    mkt = pd.read_parquet(args.market)
    mkt = mkt.dropna(subset=["bid", "ask", "result"]).copy()
    mkt["dt"] = pd.to_datetime(mkt["ts"], unit="s", utc=True)
    mkt["mdate"] = mkt["date"].map(parse_datecode)

    obs = pd.read_parquet(args.obs)
    obs["local"] = pd.to_datetime(obs["valid"])
    obs["d"] = obs["local"].dt.date
    obs["h"] = obs["local"].dt.hour

    resid = build_residual_climatology(obs, tz, hours)
    print(f"Residual climatology built for hours: {sorted(resid)}")
    for h in sorted(resid):
        s = resid[h]
        print(f"  {h:02d}:00  n={len(s):3d}  mean +{s.mean():.1f}F  "
              f"p90 +{np.percentile(s,90):.1f}F  (still-to-rise from running max)")

    common_days = sorted(set(mkt["mdate"]) & set(obs["d"]))
    print(f"\nDays usable (market & obs overlap): {len(common_days)} "
          f"({common_days[0]} .. {common_days[-1]})\n")

    bets = []
    for d in common_days:
        obs_day = obs[obs["d"] == d]
        if obs_day.empty:
            continue
        day_mkt = mkt[mkt["mdate"] == d]
        if day_mkt.empty:
            continue
        for h in hours:
            if h not in resid:
                continue
            rmax = rmax_at(obs_day, h)
            if rmax is None:
                continue
            # decision instant in UTC
            target = datetime(d.year, d.month, d.day, h, 0, tzinfo=tz).astimezone(UTC)
            target = pd.Timestamp(target)
            # best +EV trade across buckets at this instant
            best = None
            for tk, gb in day_mkt.groupby("ticker"):
                gb = gb[gb["dt"] <= target]
                if gb.empty:
                    continue
                row = gb.iloc[-1]                      # latest quote at/before target
                bid, ask = row["bid"], row["ask"]
                if not (0 < bid <= ask < 1):
                    continue
                lo, hi, kind, res = row["lo"], row["hi"], row["kind"], row["result"]
                mid = (bid + ask) / 2
                p = mid if args.no_info else model_prob(rmax, resid[h], lo, hi, kind)
                won_yes = 1.0 if res == "yes" else 0.0
                # buy YES at ask
                ev_yes = p - ask - taker_fee(ask)
                # buy NO at (1-bid)
                no_px = 1 - bid
                ev_no = (1 - p) - no_px - taker_fee(no_px)
                if ev_yes >= ev_no:
                    side, px, ev, won = "YES", ask, ev_yes, won_yes
                    pnl = (won - px) - taker_fee(px)
                else:
                    side, px, ev, won = "NO", no_px, ev_no, (1 - won_yes)
                    pnl = (won - px) - taker_fee(px)
                if best is None or ev > best["ev"]:
                    best = dict(day=d, h=h, ticker=tk, side=side, px=px,
                                ev=ev, pnl=pnl, model_p=p, rmax=rmax)
            if best and best["ev"] >= args.edge:
                bets.append(best)

    if not bets:
        print("No bets cleared the edge threshold.")
        return
    bdf = pd.DataFrame(bets)
    n = len(bdf)
    wins = (bdf["pnl"] > 0).sum()
    print(f"{'='*60}")
    print(f"{'CONTROL (no_info)' if args.no_info else 'MODEL'}  "
          f"edge>={args.edge}  hours={hours}")
    print(f"{'='*60}")
    print(f"Bets placed:     {n}  (over {bdf['day'].nunique()} days)")
    print(f"Win rate:        {wins/n*100:.2f}%  ({wins}/{n})")
    print(f"Avg model EV:    {bdf['ev'].mean():+.4f} per $1 (pre-settlement estimate)")
    print(f"Realized P&L:    {bdf['pnl'].sum():+.2f} units  "
          f"({bdf['pnl'].mean():+.4f}/bet)")
    print(f"ROI per bet:     {bdf['pnl'].mean()*100:+.2f}%")
    print(f"\nBy decision hour:")
    for h, g in bdf.groupby("h"):
        print(f"  {h:02d}:00  bets={len(g):3d}  win={(g['pnl']>0).mean()*100:5.1f}%  "
              f"pnl/bet={g['pnl'].mean():+.4f}")
    print(f"\nBy side: " + ", ".join(
        f"{s}={len(g)} ({g['pnl'].mean():+.4f}/bet)" for s, g in bdf.groupby("side")))


if __name__ == "__main__":
    main()
