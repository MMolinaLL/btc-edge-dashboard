"""
Backtest engine for BTC 5-minute up/down bets.

The bet: at the close of candle t, predict whether candle t+1 closes higher.
A strategy emits a signal in {+1 = bet up, -1 = bet down, 0 = no bet} using ONLY
information available through candle t (no look-ahead).

We report, per strategy:
  - number of bets
  - raw directional win rate  (is there ANY predictive edge?)
  - edge vs 50%
  - net P&L under a binary payout model (win -> +payout, loss -> -1.0)
  - whether it clears the breakeven win rate for that payout

A coin-flip and an always-up baseline are included as sanity checks: if the
harness is honest, coin-flip lands near 50% and always-up reveals BTC's drift.
"""

import argparse
import numpy as np
import pandas as pd


# ----------------------------- strategies ---------------------------------
# Each returns a signal array in {+1, -1, 0}, aligned to df.index, using only
# data up to and including each candle's close.

def s_always_up(df):
    return np.ones(len(df), dtype=int)


def s_coinflip(df):
    rng = np.random.default_rng(42)  # seeded => reproducible
    return rng.choice([-1, 1], size=len(df))


def s_momentum1(df):
    # bet next candle continues the last candle's direction
    r = df["close"].diff()
    return np.sign(r).fillna(0).astype(int).values


def s_meanrev1(df):
    r = df["close"].diff()
    return (-np.sign(r)).fillna(0).astype(int).values


def s_momentum_n(df, n):
    r = df["close"] - df["close"].shift(n)
    return np.sign(r).fillna(0).astype(int).values


def s_ema_trend(df, span):
    ema = df["close"].ewm(span=span, adjust=False).mean()
    return np.where(df["close"] > ema, 1, -1)


def s_rsi(df, period=14, low=30, high=70):
    # mean-reversion on RSI extremes; flat (no bet) in the middle
    delta = df["close"].diff()
    up = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = up / down.replace(0, np.nan)
    rsi = 100 - 100 / (1 + rs)
    sig = np.zeros(len(df), dtype=int)
    sig[rsi.values < low] = 1     # oversold -> bet up
    sig[rsi.values > high] = -1   # overbought -> bet down
    return sig


STRATEGIES = {
    "always_up":      s_always_up,
    "coinflip":       s_coinflip,
    "momentum_1":     s_momentum1,
    "meanrev_1":      s_meanrev1,
    "momentum_3":     lambda df: s_momentum_n(df, 3),
    "momentum_6":     lambda df: s_momentum_n(df, 6),
    "meanrev_3":      lambda df: -s_momentum_n(df, 3),
    "ema_12":         lambda df: s_ema_trend(df, 12),
    "ema_48":         lambda df: s_ema_trend(df, 48),
    "rsi_14":         s_rsi,
}


# ----------------------------- evaluation ---------------------------------

def evaluate(df, signal, payout):
    """Return metrics dict for a signal array against next-candle direction."""
    next_ret = df["close"].shift(-1) - df["close"]          # outcome of candle t+1
    next_up = next_ret > 0

    sig = pd.Series(signal, index=df.index)
    bet_mask = (sig != 0) & next_ret.notna() & (next_ret != 0)  # drop flats & last row

    s = sig[bet_mask]
    up = next_up[bet_mask]
    predicted_up = s > 0
    correct = predicted_up == up

    n = int(bet_mask.sum())
    if n == 0:
        return None
    win = correct.mean()
    # binary payout model: win -> +payout, loss -> -1
    pnl_per_bet = np.where(correct, payout, -1.0)
    roi = pnl_per_bet.mean()
    total = pnl_per_bet.sum()
    se = np.sqrt(win * (1 - win) / n)  # standard error of the win rate
    return {
        "bets": n,
        "win": win,
        "edge": win - 0.5,
        "se": se,
        "roi": roi,
        "total": total,
    }


def by_year(df, signal, payout):
    out = {}
    years = df.index.year
    for y in sorted(set(years)):
        m = years == y
        r = evaluate(df.iloc[m], np.asarray(signal)[m], payout)
        if r:
            out[y] = r["win"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/btc_5m.parquet")
    ap.add_argument("--payout", type=float, default=0.95,
                    help="binary win payout per 1 unit staked (default 0.95)")
    args = ap.parse_args()

    df = pd.read_parquet(args.data)
    breakeven = 1.0 / (1.0 + args.payout)

    print(f"\nData: {len(df):,} candles  "
          f"{df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d}")
    print(f"Payout model: win +{args.payout}, loss -1.0  "
          f"=> breakeven win rate = {breakeven:.4f} ({breakeven*100:.2f}%)\n")

    # base rate: how often does a 5m candle go up at all?
    nxt = df["close"].shift(-1) - df["close"]
    base_up = (nxt > 0).sum() / nxt.notna().sum()
    print(f"Base rate: {base_up*100:.2f}% of 5m candles close up "
          f"(flats excluded from bets)\n")

    hdr = f"{'strategy':<14}{'bets':>9}{'win%':>8}{'edge':>8}{'±2se':>8}{'ROI/bet':>9}{'total':>10}  result"
    print(hdr)
    print("-" * len(hdr))

    rows = []
    for name, fn in STRATEGIES.items():
        sig = np.asarray(fn(df))
        r = evaluate(df, sig, args.payout)
        if r is None:
            continue
        # 95% CI half-width on win rate, and verdict vs breakeven
        ci = 2 * r["se"]
        beats = r["win"] - ci > breakeven  # lower bound of CI clears breakeven
        verdict = "PROFITABLE" if beats else ("edge>0" if r["edge"] > 0 else "")
        rows.append((name, r, ci, verdict))
        print(f"{name:<14}{r['bets']:>9,}{r['win']*100:>7.2f}%"
              f"{r['edge']*100:>+7.2f}%{ci*100:>7.2f}%"
              f"{r['roi']:>+9.4f}{r['total']:>+10.1f}  {verdict}")

    # consistency check for the most interesting non-baseline strategies
    print("\nPer-year win% (consistency check — an edge should persist):")
    for name, r, ci, verdict in rows:
        if name in ("always_up", "coinflip"):
            continue
        yrs = by_year(df, np.asarray(STRATEGIES[name](df)), args.payout)
        cells = "  ".join(f"{y}:{w*100:5.2f}%" for y, w in yrs.items())
        print(f"  {name:<12} {cells}")

    print(f"\nNote: with {len(df):,} bets the win-rate standard error is tiny, so")
    print("even a 'statistically significant' 50.5% is economically worthless")
    print(f"once you need {breakeven*100:.2f}% just to break even.")


if __name__ == "__main__":
    main()
