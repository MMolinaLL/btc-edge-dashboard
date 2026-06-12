"""
ensemble_vote.py — ensemble / consensus-voting strategies for BTC 5m up/down.

Family idea: build several weak, causal base signals (momentum, mean-reversion,
breakout, Bollinger, vol-gated fade) and only place a bet when enough of them
AGREE. The hope is that demanding consensus filters noise and concentrates bets
on the highest-conviction setups, lifting the per-bet edge above trading cost.

CONTRACT (see search_user/_template.py):
  - Each fn(df) -> numpy int array in {-1, 0, +1}, aligned to df.index.
  - +1 bet next 5m candle closes UP, -1 DOWN, 0 no bet.
  - df columns: open, high, low, close, volume (UTC index).

NO LOOK-AHEAD: every base signal at row i uses ONLY data through row i. We use
.diff(), .shift(+k), and rolling/ewm windows (which look backward only). The one
place a future value is touched (range-max/min) is explicitly .shift(1)'d so the
breakout reference excludes the current bar. No .shift(-k), no whole-series
statistics, no parameters fit on the full set.
"""
import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# Causal base signals. Each returns a float numpy array in {-1, 0, +1}.
# All use only backward-looking windows / shifts.
# --------------------------------------------------------------------------
def _ret(df):
    return df["close"].diff()


def _b_momentum(df, k):
    """Trend: +1 if price rose over the last k bars, -1 if it fell."""
    return np.sign(df["close"] - df["close"].shift(k)).fillna(0.0).values


def _b_meanrev(df, k):
    """Fade: opposite of the last k-bar move."""
    return (-np.sign(df["close"] - df["close"].shift(k))).fillna(0.0).values


def _b_ema_trend(df, span):
    """Regime: +1 above the trailing EMA, -1 below it."""
    ema = df["close"].ewm(span=span, adjust=False).mean()
    return np.where(df["close"].values > ema.values, 1.0, -1.0)


def _b_breakout(df, span):
    """Momentum on range expansion. Reference range is shifted(1) -> causal."""
    hi = df["high"].rolling(span).max().shift(1)
    lo = df["low"].rolling(span).min().shift(1)
    s = np.zeros(len(df), dtype=float)
    s[df["close"].values > hi.values] = 1.0
    s[df["close"].values < lo.values] = -1.0
    return s


def _b_boll(df, span, z):
    """Bollinger fade: short above upper band, long below lower band."""
    ma = df["close"].rolling(span).mean()
    sd = df["close"].rolling(span).std()
    s = np.zeros(len(df), dtype=float)
    s[(df["close"] > ma + z * sd).values] = -1.0
    s[(df["close"] < ma - z * sd).values] = 1.0
    return s


def _b_mrvf(df, span, mult):
    """Vol-filtered fade: revert only when the last move is large vs recent vol."""
    r = _ret(df)
    vol = r.rolling(span).std()
    big = (r.abs() > mult * vol).values
    return np.where(big, -np.sign(r).fillna(0.0).values, 0.0)


def _vote(voters, thr):
    """Sum signed votes; bet only when net agreement >= thr (consensus)."""
    V = np.vstack(voters)
    net = V.sum(axis=0)
    sig = np.where(net >= thr, 1, np.where(net <= -thr, -1, 0))
    return sig.astype(int)


# --------------------------------------------------------------------------
# Strategy 1: Mean-reversion consensus, simple majority (>=1 net agreement).
# Five fade-style voters; bet whenever they lean one way on net.
# --------------------------------------------------------------------------
def meanrev_majority(df):
    voters = [
        _b_meanrev(df, 1),
        _b_meanrev(df, 3),
        _b_mrvf(df, 24, 1.5),
        _b_mrvf(df, 48, 2.0),
        _b_boll(df, 20, 2.0),
    ]
    return _vote(voters, thr=1)


# --------------------------------------------------------------------------
# Strategy 2: Mean-reversion STRONG consensus (>=3 of 5 net agreement).
# Same voters as #1 but demand a clear majority -> fewer, higher-conviction bets.
# --------------------------------------------------------------------------
def meanrev_strong_consensus(df):
    voters = [
        _b_meanrev(df, 1),
        _b_meanrev(df, 3),
        _b_mrvf(df, 24, 1.5),
        _b_mrvf(df, 48, 2.0),
        _b_boll(df, 20, 2.0),
    ]
    return _vote(voters, thr=3)


# --------------------------------------------------------------------------
# Strategy 3: Trend consensus, strong agreement (>=3 of 5 momentum voters).
# Pure trend-following ensemble (the opposite regime bet from #1/#2).
# --------------------------------------------------------------------------
def trend_consensus(df):
    voters = [
        _b_momentum(df, 3),
        _b_momentum(df, 12),
        _b_ema_trend(df, 24),
        _b_ema_trend(df, 48),
        _b_breakout(df, 24),
    ]
    return _vote(voters, thr=3)


# --------------------------------------------------------------------------
# Strategy 4: Mixed ensemble — trend AND fade voters together; only act on
# UNANIMITY-ish agreement (>=4 net) so the two camps must strongly align.
# This demands the move be both extended (fade) and confirmed, a rare setup.
# --------------------------------------------------------------------------
def mixed_unanimous(df):
    voters = [
        _b_meanrev(df, 1),
        _b_meanrev(df, 6),
        _b_boll(df, 40, 2.0),
        _b_mrvf(df, 24, 1.5),
        _b_mrvf(df, 48, 2.0),
        _b_breakout(df, 48),
    ]
    return _vote(voters, thr=4)


# --------------------------------------------------------------------------
# Strategy 5: Vol-GATED mean-reversion consensus. Only vote in high-vol bars
# (current 12-bar realized vol above its own trailing 96-bar median), where
# overshoot/reversion is more pronounced; require >=2 net agreement.
# The gate is fully causal (rolling median of a rolling std).
# --------------------------------------------------------------------------
def volgated_meanrev_consensus(df):
    voters = [
        _b_meanrev(df, 1),
        _b_meanrev(df, 3),
        _b_mrvf(df, 24, 2.0),
        _b_boll(df, 20, 2.0),
    ]
    sig = _vote(voters, thr=2)
    r = _ret(df)
    vol = r.rolling(12).std()
    vol_med = vol.rolling(96).median()
    high_vol = (vol > vol_med).fillna(False).values
    return np.where(high_vol, sig, 0).astype(int)


STRATEGIES = {
    "meanrev_majority": meanrev_majority,
    "meanrev_strong_consensus": meanrev_strong_consensus,
    "trend_consensus": trend_consensus,
    "mixed_unanimous": mixed_unanimous,
    "volgated_meanrev_consensus": volgated_meanrev_consensus,
}
