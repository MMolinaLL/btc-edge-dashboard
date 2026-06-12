"""
composite_reversion.py — family: composite_reversion

Idea: combine several classic mean-reversion oscillators (RSI, Bollinger %B,
Stochastic %K) and only take a (counter-trend) bet when MULTIPLE oscillators
AGREE that price is stretched, AND a volatility filter confirms the stretch is
large in absolute terms. The thesis: a 5m candle that pokes far outside its
recent range on several independent measures tends to snap back next candle.
Being selective (fewer, higher-conviction bets) is the whole point — we would
rather take 300 good bets than 30000 coin-flips.

NO LOOK-AHEAD: every indicator below is built from rolling/expanding windows or
.shift(+k). signal[i] uses only close/high/low/volume through row i. The outcome
(next candle) is never referenced. We deliberately do NOT fit any parameter on
the dataset; thresholds are fixed constants.

Each fn(df) -> np.ndarray[int] in {-1, 0, +1}, aligned to df.index:
    +1 bet next candle closes UP,  -1 DOWN,  0 no bet.
"""
import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# Causal oscillator building blocks (all use only past/current data)
# --------------------------------------------------------------------------
def _rsi(close, n=14):
    """Wilder-style RSI in [0,100], causal (EMA of gains/losses)."""
    delta = close.diff()
    up = delta.clip(lower=0.0)
    down = (-delta).clip(lower=0.0)
    # Wilder smoothing == EMA with alpha = 1/n; adjust=False is causal.
    roll_up = up.ewm(alpha=1.0 / n, adjust=False).mean()
    roll_down = down.ewm(alpha=1.0 / n, adjust=False).mean()
    rs = roll_up / roll_down.replace(0.0, np.nan)
    rsi = 100.0 - 100.0 / (1.0 + rs)
    return rsi.fillna(50.0)


def _bollinger_pctb(close, n=20):
    """Bollinger %B: (close - lower)/(upper - lower); 0.5 = at the mean.
    Returns a value typically in ~[0,1] but can exceed when far outside band."""
    ma = close.rolling(n).mean()
    sd = close.rolling(n).std()
    upper = ma + 2.0 * sd
    lower = ma - 2.0 * sd
    width = (upper - lower).replace(0.0, np.nan)
    return ((close - lower) / width)


def _bollinger_z(close, n=20):
    """Standardized distance of close from its rolling mean (z-score)."""
    ma = close.rolling(n).mean()
    sd = close.rolling(n).std().replace(0.0, np.nan)
    return (close - ma) / sd


def _stoch_k(high, low, close, n=14):
    """Stochastic %K in [0,100]: where close sits in the n-bar high/low range."""
    ll = low.rolling(n).min()
    hh = high.rolling(n).max()
    rng = (hh - ll).replace(0.0, np.nan)
    k = 100.0 * (close - ll) / rng
    return k.fillna(50.0)


def _ret(df):
    return df["close"].diff()


def _vol_filter(df, span=48, mult=1.0):
    """True when the latest 1-bar move is large vs recent realized vol.
    Uses only data through the current row."""
    r = _ret(df)
    vol = r.rolling(span).std()
    return (r.abs() > mult * vol)


# --------------------------------------------------------------------------
# Strategy 1: Triple-oscillator agreement (RSI + %B + Stoch), no vol filter.
#   Fade only when all three say "overbought" or all three say "oversold".
# --------------------------------------------------------------------------
def triple_agree(df):
    close = df["close"]
    rsi = _rsi(close, 14)
    pctb = _bollinger_pctb(close, 20)
    stoch = _stoch_k(df["high"], df["low"], close, 14)

    overbought = (rsi > 70) & (pctb > 0.95) & (stoch > 80)
    oversold = (rsi < 30) & (pctb < 0.05) & (stoch < 20)

    sig = np.zeros(len(df), dtype=int)
    sig[overbought.values] = -1   # fade the top -> bet down
    sig[oversold.values] = 1      # fade the bottom -> bet up
    return sig


# --------------------------------------------------------------------------
# Strategy 2: Triple agreement PLUS a volatility filter.
#   Same as above but the move must also be large in absolute terms.
# --------------------------------------------------------------------------
def triple_agree_volfilter(df):
    close = df["close"]
    rsi = _rsi(close, 14)
    pctb = _bollinger_pctb(close, 20)
    stoch = _stoch_k(df["high"], df["low"], close, 14)
    big = _vol_filter(df, span=48, mult=1.0)

    overbought = (rsi > 70) & (pctb > 0.95) & (stoch > 80) & big
    oversold = (rsi < 30) & (pctb < 0.05) & (stoch < 20) & big

    sig = np.zeros(len(df), dtype=int)
    sig[overbought.values] = -1
    sig[oversold.values] = 1
    return sig


# --------------------------------------------------------------------------
# Strategy 3: "2-of-3" agreement with a strong Bollinger z-score gate.
#   More permissive on which oscillators agree, but requires a genuinely
#   extreme z-score (>2.5 sigma) so we only fade real outliers.
# --------------------------------------------------------------------------
def two_of_three_z(df):
    close = df["close"]
    rsi = _rsi(close, 14)
    stoch = _stoch_k(df["high"], df["low"], close, 14)
    z = _bollinger_z(close, 20)

    ob_votes = ((rsi > 68).astype(int)
                + (stoch > 80).astype(int)
                + (z > 2.0).astype(int))
    os_votes = ((rsi < 32).astype(int)
                + (stoch < 20).astype(int)
                + (z < -2.0).astype(int))

    overbought = (ob_votes >= 2) & (z > 2.5)
    oversold = (os_votes >= 2) & (z < -2.5)

    sig = np.zeros(len(df), dtype=int)
    sig[overbought.values] = -1
    sig[oversold.values] = 1
    return sig


# --------------------------------------------------------------------------
# Strategy 4: RSI + Stochastic agreement, gated by an EXPANDING-window
#   percentile vol regime (only fade when current vol is in the high regime).
#   Uses expanding history (no future leakage) to define "high vol".
# --------------------------------------------------------------------------
def rsi_stoch_volregime(df):
    close = df["close"]
    rsi = _rsi(close, 14)
    stoch = _stoch_k(df["high"], df["low"], close, 14)

    r = _ret(df)
    vol = r.rolling(24).std()
    # Expanding median of vol, shifted by 1 so row i only sees vols < i.
    vol_med = vol.expanding(min_periods=200).median().shift(1)
    high_vol = vol > vol_med

    overbought = (rsi > 72) & (stoch > 82) & high_vol
    oversold = (rsi < 28) & (stoch < 18) & high_vol

    sig = np.zeros(len(df), dtype=int)
    sig[overbought.values] = -1
    sig[oversold.values] = 1
    return sig


# --------------------------------------------------------------------------
# Strategy 5: Composite oscillator score. Average three oscillators (each
#   centered/normalized to [-1,+1]) into a single conviction score, then fade
#   only the extreme tails AND require a vol-filtered large move.
# --------------------------------------------------------------------------
def composite_score(df):
    close = df["close"]
    rsi = _rsi(close, 14)
    stoch = _stoch_k(df["high"], df["low"], close, 14)
    pctb = _bollinger_pctb(close, 20)

    # Normalize each to roughly [-1, +1]: +1 = overbought, -1 = oversold.
    rsi_n = (rsi - 50.0) / 50.0
    stoch_n = (stoch - 50.0) / 50.0
    pctb_n = (pctb.clip(0.0, 1.0) - 0.5) * 2.0
    score = (rsi_n + stoch_n + pctb_n) / 3.0

    big = _vol_filter(df, span=48, mult=1.0)
    overbought = (score > 0.80) & big
    oversold = (score < -0.80) & big

    sig = np.zeros(len(df), dtype=int)
    sig[overbought.values] = -1
    sig[oversold.values] = 1
    return sig


# --------------------------------------------------------------------------
# Strategy 6: Slow-frame composite reversion. Use longer oscillator windows
#   (RSI-21, Stoch-21, Boll-30) so we only react to bigger, slower stretches,
#   and require all three to agree at moderately extreme levels.
# --------------------------------------------------------------------------
def slow_triple_agree(df):
    close = df["close"]
    rsi = _rsi(close, 21)
    stoch = _stoch_k(df["high"], df["low"], close, 21)
    pctb = _bollinger_pctb(close, 30)
    big = _vol_filter(df, span=96, mult=1.0)

    overbought = (rsi > 65) & (pctb > 0.90) & (stoch > 78) & big
    oversold = (rsi < 35) & (pctb < 0.10) & (stoch < 22) & big

    sig = np.zeros(len(df), dtype=int)
    sig[overbought.values] = -1
    sig[oversold.values] = 1
    return sig


STRATEGIES = {
    "triple_agree": triple_agree,
    "triple_agree_volfilter": triple_agree_volfilter,
    "two_of_three_z": two_of_three_z,
    "rsi_stoch_volregime": rsi_stoch_volregime,
    "composite_score": composite_score,
    "slow_triple_agree": slow_triple_agree,
}
