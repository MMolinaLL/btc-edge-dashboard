"""
eval_engine.py — the shared, honest evaluation core.

Used by both the Streamlit dashboard and the edge-search. Every strategy is
scored with:
  - a TRAIN / TEST split (last 30% is held out, out-of-sample)
  - an explicit per-bet cost in basis points (spread + fees)
  - gross AND net figures, plus an equity curve
  - controls (coinflip, always-up) so we can tell signal from noise

A strategy is a function: df -> signal array in {-1, 0, +1} (bet down/none/up),
using ONLY information available at each candle's close (no look-ahead).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Reuse the strategies already written + validated in backtest.py
from backtest import STRATEGIES as BASE_STRATEGIES


# --------------------------- extra candidates -----------------------------
def _ret(df):
    return df["close"].diff()


def s_streak_reversal(df, k=3):
    """After k candles in the same direction, fade the move."""
    d = np.sign(_ret(df)).fillna(0).values
    sig = np.zeros(len(df), dtype=int)
    for i in range(k, len(df)):
        if all(d[i - j] == 1 for j in range(k)):
            sig[i] = -1
        elif all(d[i - j] == -1 for j in range(k)):
            sig[i] = 1
    return sig


def s_meanrev_volfilter(df, span=24, mult=1.5):
    """Mean-revert only when the last move is large vs recent volatility."""
    r = _ret(df)
    vol = r.rolling(span).std()
    big = r.abs() > mult * vol
    return np.where(big, -np.sign(r).fillna(0), 0).astype(int)


def s_time_of_day(df):
    """Bet the historical mean direction for each UTC hour (trained in-sample)."""
    nxt = (df["close"].shift(-1) > df["close"]).astype(float)
    hour = df.index.hour
    n_train = int(len(df) * 0.7)
    bias = pd.Series(nxt.values[:n_train]).groupby(hour[:n_train]).mean()
    sig = np.array([1 if bias.get(h, 0.5) > 0.5 else -1 for h in hour])
    return sig


def s_vol_breakout(df, span=24):
    """Trade in the direction of a range breakout (momentum on expansion)."""
    hi = df["high"].rolling(span).max().shift(1)
    lo = df["low"].rolling(span).min().shift(1)
    sig = np.zeros(len(df), dtype=int)
    sig[df["close"].values > hi.values] = 1
    sig[df["close"].values < lo.values] = -1
    return sig


def s_composite_score(df):
    """Promoted from the edge search (composite_reversion family).

    Fade extreme readings only when RSI(14), Stochastic(14) and Bollinger %B(20)
    AGREE that price is stretched AND the latest move is large vs recent vol.
    Selective mean-reversion: the best, cleanest (cross-venue, no-look-ahead)
    signal the search found. ~4 bps gross/bet — real, but below most real costs.
    """
    close = df["close"]
    # RSI (causal Wilder/EMA)
    delta = close.diff()
    up = delta.clip(lower=0.0).ewm(alpha=1/14, adjust=False).mean()
    down = (-delta).clip(lower=0.0).ewm(alpha=1/14, adjust=False).mean()
    rsi = (100 - 100 / (1 + up / down.replace(0, np.nan))).fillna(50)
    # Stochastic %K
    ll = df["low"].rolling(14).min()
    hh = df["high"].rolling(14).max()
    stoch = (100 * (close - ll) / (hh - ll).replace(0, np.nan)).fillna(50)
    # Bollinger %B
    ma = close.rolling(20).mean()
    sd = close.rolling(20).std()
    pctb = (close - (ma - 2*sd)) / ((ma + 2*sd) - (ma - 2*sd)).replace(0, np.nan)
    # composite, normalized to ~[-1,+1]
    score = ((rsi - 50)/50 + (stoch - 50)/50 + (pctb.clip(0, 1) - 0.5)*2) / 3
    r = close.diff()
    big = r.abs() > r.rolling(48).std()
    sig = np.zeros(len(df), dtype=int)
    sig[((score > 0.80) & big).values] = -1
    sig[((score < -0.80) & big).values] = 1
    return sig


EXTRA_STRATEGIES = {
    "composite_score": s_composite_score,        # best edge-search find
    "streak_reversal_3": lambda df: s_streak_reversal(df, 3),
    "meanrev_volfilter": s_meanrev_volfilter,
    "time_of_day": s_time_of_day,
    "vol_breakout_24": lambda df: s_vol_breakout(df, 24),
}

ALL_STRATEGIES = {**BASE_STRATEGIES, **EXTRA_STRATEGIES}


# ------------------------------ evaluation --------------------------------
def evaluate_spot(df: pd.DataFrame, signal, cost_bps: float = 5.0,
                  train_frac: float = 0.70) -> dict:
    """Score a signal as a per-candle directional bet, net of cost_bps per bet."""
    next_ret = df["close"].shift(-1) / df["close"] - 1.0
    sig = pd.Series(np.asarray(signal), index=df.index).astype(float)
    active = (sig != 0) & next_ret.notna() & (next_ret != 0)

    gross_bps = sig * next_ret * 1e4
    net_bps = gross_bps - cost_bps
    net_bps = net_bps.where(active, 0.0)             # 0 P&L when not betting
    correct = ((sig > 0) == (next_ret > 0)) & active

    n = len(df)
    cut = int(n * train_frac)
    idx = np.arange(n)

    def slice_stats(mask_period):
        m = active.values & mask_period
        k = int(m.sum())
        if k == 0:
            return dict(bets=0, win=float("nan"), gross_bps=float("nan"),
                        net_bps=float("nan"), total=0.0)
        return dict(
            bets=k,
            win=float(correct.values[m].mean()),
            gross_bps=float(gross_bps.values[m].mean()),
            net_bps=float(net_bps.values[m].mean()),
            total=float(net_bps.values[m].sum()),
        )

    train = slice_stats(idx < cut)
    test = slice_stats(idx >= cut)
    allp = slice_stats(idx >= 0)

    equity = net_bps.cumsum()                        # bps, cumulative
    return {
        "train": train, "test": test, "all": allp,
        "cut_time": df.index[cut],
        "equity": equity,                            # pd.Series indexed by time
        "cost_bps": cost_bps,
    }


def run_all(df: pd.DataFrame, cost_bps: float = 5.0,
            strategies: dict | None = None) -> pd.DataFrame:
    """Evaluate every strategy; return a sortable leaderboard DataFrame."""
    strategies = strategies or ALL_STRATEGIES
    rows = []
    for name, fn in strategies.items():
        try:
            res = evaluate_spot(df, np.asarray(fn(df)), cost_bps)
        except Exception as e:
            rows.append({"strategy": name, "error": str(e)})
            continue
        rows.append({
            "strategy": name,
            "bets_total": res["all"]["bets"],
            "win_train": res["train"]["win"],
            "win_test": res["test"]["win"],
            "net_bps_train": res["train"]["net_bps"],
            "net_bps_test": res["test"]["net_bps"],     # the number that matters
            "total_test": res["test"]["total"],
            "gross_bps_test": res["test"]["gross_bps"],
        })
    out = pd.DataFrame(rows)
    if "net_bps_test" in out:
        out = out.sort_values("net_bps_test", ascending=False, na_position="last")
    return out.reset_index(drop=True)


if __name__ == "__main__":
    # quick smoke test from CLI
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "data/btc_5m.parquet"
    cost = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    df = pd.read_parquet(path)
    print(f"{path}  ({len(df):,} candles)  cost={cost} bps/bet\n")
    lb = run_all(df, cost)
    with pd.option_context("display.float_format", lambda v: f"{v:.3f}",
                           "display.width", 160):
        print(lb.to_string(index=False))
    print("\nKey column: net_bps_test (out-of-sample net edge per bet). "
          "Positive AND consistent with net_bps_train = worth a closer look.")
