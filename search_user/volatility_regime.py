"""
volatility_regime.py — edge-search strategies conditioned on the volatility regime.

Family thesis: BTC 5m direction is not stationary. The SAME raw signal (last
candle's move, a band break, a breakout) carries different information depending
on whether we are in a quiet, contracting tape or a loud, expanding one. Each
strategy below first measures a *regime* using only past data, then picks
momentum vs. mean-reversion (or stands aside) accordingly.

CONTRACT (see _template.py):
    fn(df) -> np.ndarray[int] in {-1, 0, +1}, aligned to df.index.
    +1 bet next 5m candle closes UP, -1 DOWN, 0 no bet.

NO LOOK-AHEAD: every feature uses rolling/expanding windows and .shift(+k) only.
The regime label for row i is computed from a window that ENDS at row i-1
(we shift regime features by +1 so the threshold and the trigger never share
the bar we are about to act on). Outcomes (next candle) are never referenced.
"""
import numpy as np
import pandas as pd


def _ret(df):
    return df["close"].diff()


def _atr(df, span):
    """Causal average true range over `span` bars (Wilder-style via rolling mean)."""
    h, l, c = df["high"], df["low"], df["close"]
    prev_c = c.shift(1)
    tr = pd.concat([(h - l).abs(),
                    (h - prev_c).abs(),
                    (l - prev_c).abs()], axis=1).max(axis=1)
    return tr.rolling(span).mean()


# --------------------------------------------------------------------------
# 1. ATR-percentile regime switch.
#    Rank current ATR against its own trailing history (expanding-ish via a long
#    rolling window). In the LOW-vol regime, fade the last move (mean-revert);
#    in the HIGH-vol regime, ride it (momentum). Mid regime: stand aside.
# --------------------------------------------------------------------------
def atr_pct_switch(df, atr_span=14, rank_win=288, lo=0.30, hi=0.70):
    atr = _atr(df, atr_span)
    # percentile rank of the most recent *completed* atr within trailing window
    rank = atr.shift(1).rolling(rank_win).apply(
        lambda w: (w[-1] >= w[:-1]).mean() if len(w) > 1 else np.nan, raw=True)
    r = _ret(df)
    last_dir = np.sign(r).fillna(0).values
    rk = rank.values
    sig = np.zeros(len(df), dtype=int)
    low_reg = rk <= lo
    high_reg = rk >= hi
    sig[low_reg] = (-last_dir[low_reg]).astype(int)   # quiet -> mean revert
    sig[high_reg] = (last_dir[high_reg]).astype(int)  # loud  -> momentum
    return sig


# --------------------------------------------------------------------------
# 2. Volatility contraction -> breakout.
#    When realized vol has been compressing (current short-window std well below
#    its longer-window baseline), a range break tends to extend. Trade the break
#    direction ONLY while the tape is coiled; ignore breaks in normal vol.
# --------------------------------------------------------------------------
def contraction_breakout(df, vol_short=12, vol_long=96, brk=12, squeeze=0.7):
    r = _ret(df)
    vs = r.rolling(vol_short).std()
    vl = r.rolling(vol_long).std()
    coiled = (vs / vl).shift(1) < squeeze          # regime measured pre-bar
    hi = df["high"].rolling(brk).max().shift(1)
    lo = df["low"].rolling(brk).min().shift(1)
    c = df["close"].values
    up = c > hi.values
    dn = c < lo.values
    sig = np.zeros(len(df), dtype=int)
    mask = coiled.values
    sig[mask & up] = 1
    sig[mask & dn] = -1
    return sig


# --------------------------------------------------------------------------
# 3. Vol-of-vol gate on mean reversion.
#    Mean reversion of an outsized candle works best when volatility itself is
#    STABLE (low vol-of-vol): the spike is idiosyncratic noise, not the start of
#    a vol expansion. When vol-of-vol is high, an outsized candle more often
#    begets follow-through, so we don't fade it.
# --------------------------------------------------------------------------
def volofvol_meanrev(df, span=24, vov_win=96, mult=1.3, vov_lo=0.45):
    r = _ret(df)
    vol = r.rolling(span).std()
    vov = vol.pct_change().abs().rolling(vov_win).std()       # how jumpy vol is
    vov_rank = vov.shift(1).rolling(vov_win).apply(
        lambda w: (w[-1] >= w[:-1]).mean() if len(w) > 1 else np.nan, raw=True)
    big = (r.abs() > mult * vol.shift(1))                     # outsized vs prior vol
    stable = vov_rank <= vov_lo
    fade = big & stable
    return np.where(fade.values, -np.sign(r).fillna(0).values, 0).astype(int)


# --------------------------------------------------------------------------
# 4. Regime-dependent EMA trend.
#    Trend-following (price vs EMA) only pays when there is enough vol to make a
#    real trend; in dead-quiet tape the EMA cross is whipsaw. Gate a classic
#    fast/slow EMA trend filter on the ATR percentile being elevated.
# --------------------------------------------------------------------------
def trend_when_volatile(df, fast=12, slow=48, atr_span=14, rank_win=288, hi=0.55):
    ema_f = df["close"].ewm(span=fast, adjust=False).mean()
    ema_s = df["close"].ewm(span=slow, adjust=False).mean()
    trend = np.sign((ema_f - ema_s)).fillna(0)
    atr = _atr(df, atr_span)
    rank = atr.shift(1).rolling(rank_win).apply(
        lambda w: (w[-1] >= w[:-1]).mean() if len(w) > 1 else np.nan, raw=True)
    active = (rank >= hi).values
    sig = np.where(active, trend.values, 0).astype(int)
    return sig


# --------------------------------------------------------------------------
# 5. Dual-regime momentum/mean-reversion on a z-score.
#    Build a causal z-score of price vs a rolling mean. The SIGN of what to do
#    flips with the volatility regime: in high vol, extreme z extends (momentum
#    on the z); in low vol, extreme z reverts (classic Bollinger fade).
# --------------------------------------------------------------------------
def zscore_regime_flip(df, span=24, rank_win=288, z_thr=1.0, lo=0.35, hi=0.65):
    ma = df["close"].rolling(span).mean()
    sd = df["close"].rolling(span).std()
    z = (df["close"] - ma) / sd
    vol = _ret(df).rolling(span).std()
    rank = vol.shift(1).rolling(rank_win).apply(
        lambda w: (w[-1] >= w[:-1]).mean() if len(w) > 1 else np.nan, raw=True)
    zv = z.values
    rk = rank.values
    sig = np.zeros(len(df), dtype=int)
    hot = rk >= hi
    cold = rk <= lo
    up_ext = zv > z_thr
    dn_ext = zv < -z_thr
    # high vol -> momentum: extended up keeps going up
    sig[hot & up_ext] = 1
    sig[hot & dn_ext] = -1
    # low vol -> reversion: extended up snaps back down
    sig[cold & up_ext] = -1
    sig[cold & dn_ext] = 1
    return sig


# --------------------------------------------------------------------------
# 6. Range-expansion follow-through.
#    Compare the current bar's true range to recent ATR. A bar that is much
#    bigger than normal (range EXPANSION) in a rising-vol regime tends to keep
#    going in its own direction the next bar; we ride that. We require the bar
#    to close in the top/bottom of its own range (conviction close).
# --------------------------------------------------------------------------
def expansion_follow(df, atr_span=24, exp_mult=1.6, clop=0.6):
    h, l, c, o = df["high"], df["low"], df["close"], df["open"]
    prev_c = c.shift(1)
    tr = pd.concat([(h - l).abs(), (h - prev_c).abs(), (l - prev_c).abs()],
                   axis=1).max(axis=1)
    atr_prev = tr.rolling(atr_span).mean().shift(1)
    rng = (h - l).replace(0, np.nan)
    clpos = (c - l) / rng                       # 1 = closed at high, 0 = at low
    expansion = tr > exp_mult * atr_prev
    bull = expansion & (clpos >= clop)
    bear = expansion & (clpos <= (1 - clop))
    sig = np.zeros(len(df), dtype=int)
    sig[bull.values] = 1
    sig[bear.values] = -1
    return sig


STRATEGIES = {
    "atr_pct_switch": atr_pct_switch,
    "contraction_breakout": contraction_breakout,
    "volofvol_meanrev": volofvol_meanrev,
    "trend_when_volatile": trend_when_volatile,
    "zscore_regime_flip": zscore_regime_flip,
    "expansion_follow": expansion_follow,
}
