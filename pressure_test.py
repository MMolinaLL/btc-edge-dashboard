"""
Pressure-test the mean-reversion "edge" against realistic execution costs, and
cross-check it across venues of different liquidity.

The earlier backtest used a binary payout haircut. Here we measure the edge the
honest way: the GROSS profit per bet in basis points (1 bp = 0.01%), computed as
signal * next-candle fractional return. That gross figure IS the breakeven
round-trip cost -- the trading cost at which the strategy nets exactly zero.

If the gross edge is ~1 bp but the cheapest realistic round-trip cost is tens of
bps, the "edge" is an artifact of the bid-ask bounce, not money you can capture.

Cross-venue check: if the edge is microstructure noise, it should SHRINK on a
deeper-liquidity venue (Coinbase) versus a thinner one (Binance.US).
"""

import sys
import numpy as np
import pandas as pd

from backtest import STRATEGIES

FOCUS = ["meanrev_1", "meanrev_3", "rsi_14"]

# Representative round-trip costs (bps) for putting on AND taking off a position.
# Sources: published retail taker fees + typical top-of-book BTC spread.
COST_BENCHMARKS = {
    "Top-of-book spread only (maker, both sides)": 4,
    "Coinbase Advanced taker (retail ~0.6%/side)": 120,
    "Binance.US taker (~0.4%/side)": 80,
    "Kraken Pro taker (~0.26%/side)": 52,
    "Kalshi binary fee (~1.75%/side at 50c)": 350,
}


def spot_eval(df, signal):
    """Gross P&L per bet in bps, win rate, and bet count (no look-ahead)."""
    next_ret = df["close"].shift(-1) / df["close"] - 1.0
    sig = pd.Series(np.asarray(signal), index=df.index)
    mask = (sig != 0) & next_ret.notna() & (next_ret != 0)
    s, r = sig[mask], next_ret[mask]
    if len(s) == 0:
        return None
    gross = (s * r)                       # fractional P&L per bet
    win = ((s > 0) == (r > 0)).mean()
    return {
        "bets": int(mask.sum()),
        "win": float(win),
        "gross_bps": float(gross.mean() * 1e4),
        "gross_se_bps": float(gross.std(ddof=1) / np.sqrt(len(gross)) * 1e4),
        "abs_ret_bps": float(r.abs().mean() * 1e4),
    }


def load(path):
    df = pd.read_parquet(path)
    return df


def common_window(dfs):
    lo = max(d.index[0] for d in dfs)
    hi = min(d.index[-1] for d in dfs)
    return [d.loc[lo:hi] for d in dfs], lo, hi


def main():
    paths = sys.argv[1:] or ["data/btc_5m.parquet", "data/btc_5m_coinbase.parquet"]
    labels = [p.split("btc_5m")[-1].replace(".parquet", "").strip("_") or "binanceus"
              for p in paths]

    dfs = [load(p) for p in paths]
    dfs, lo, hi = common_window(dfs)
    print(f"\nCommon window: {lo:%Y-%m-%d} -> {hi:%Y-%m-%d}  "
          f"({len(dfs[0]):,} candles)\n")

    # typical 5-minute move, for scale
    for lbl, df in zip(labels, dfs):
        ar = (df['close'].shift(-1) / df['close'] - 1).abs().mean() * 1e4
        print(f"  [{lbl}] avg |5m move| = {ar:.1f} bps")
    print()

    hdr = (f"{'strategy':<11}{'venue':<11}{'bets':>8}{'win%':>8}"
           f"{'gross bps':>11}{'(±2se)':>9}  breakeven cost")
    print(hdr); print("-" * len(hdr))
    for name in FOCUS:
        for lbl, df in zip(labels, dfs):
            r = spot_eval(df, STRATEGIES[name](df))
            if r is None:
                continue
            print(f"{name:<11}{lbl:<11}{r['bets']:>8,}{r['win']*100:>7.2f}%"
                  f"{r['gross_bps']:>+11.3f}{2*r['gross_se_bps']:>8.3f}  "
                  f"= {r['gross_bps']:.2f} bps/round-trip")
        print()

    print("Realistic round-trip costs you'd actually pay (bps):")
    for k, v in COST_BENCHMARKS.items():
        print(f"  {v:>4} bps   {k}")

    print("\nReality check: the gross edge above is the MOST you could net per bet")
    print("at zero cost. Compare it to the cost table. If the cheapest realistic")
    print("cost exceeds the gross edge, the strategy loses money in practice.")


if __name__ == "__main__":
    main()
