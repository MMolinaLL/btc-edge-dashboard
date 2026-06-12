"""
volume_flow.py — edge search in the VOLUME-FLOW family.

The base grid ignored volume entirely; this file probes whether volume carries a
real, capturable directional edge for the NEXT 5-minute BTC candle.

All features are strictly causal: signal[i] uses only rows 0..i (rolling /
expanding / .shift(+k) only). No .shift(-1), no full-series .max()/.mean(), no
parameters fit on the whole sample. Because the two venues report volume on
totally different scales (Binance.US ~0.09 BTC/candle, Coinbase ~28 BTC/candle),
every volume feature is NORMALIZED with a trailing rolling window (z-score or
share-of-window) so nothing depends on an absolute volume threshold.

Signals returned: numpy int array in {-1, 0, +1} aligned to df.index
    +1 bet next candle UP, -1 bet next candle DOWN, 0 no bet.

Family members (deliberately distinct mechanisms):
  1. vol_spike_fade      — fade a large move that came on a volume spike
                           (exhaustion / liquidity-grab reversion).
  2. vol_imbalance_rev   — fade extreme up- vs down-volume imbalance over a
                           window (one side got crowded -> revert).
  3. vol_weighted_mom    — volume-weighted directional momentum (continuation
                           when recent volume-heavy candles agree on direction).
  4. obv_trend           — sign of the slope of an EMA of on-balance-volume
                           (cumulative signed volume) -> trend-follow.
  5. low_vol_drift       — in quiet (below-trailing-average volume) regimes,
                           follow the last candle's direction (drift persists
                           when there is no volume to push it back).
  6. vol_confirm_breakout— range breakout that ONLY fires when accompanied by a
                           volume spike (volume-confirmed breakout momentum).
"""
import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# helpers (all causal)
# --------------------------------------------------------------------------
def _ret(df):
    return df["close"].diff()


def _volz(df, span):
    """Trailing z-score of volume over the last `span` candles (causal)."""
    v = df["volume"].astype(float)
    mu = v.rolling(span).mean()
    sd = v.rolling(span).std()
    return (v - mu) / (sd + 1e-12)


# --------------------------------------------------------------------------
# 1. Volume-spike fade
#    A big return (vs trailing return-vol) that arrives on a volume spike often
#    overshoots; fade it. Uses only trailing windows.
# --------------------------------------------------------------------------
def vol_spike_fade(df, span=48, ret_z=1.5, vol_z=1.0):
    r = _ret(df)
    rstd = r.rolling(span).std()
    volz = _volz(df, span)
    trigger = (r.abs() > ret_z * rstd) & (volz > vol_z)
    sig = np.where(trigger.values, -np.sign(r.fillna(0).values), 0)
    return sig.astype(int)


# --------------------------------------------------------------------------
# 2. Up/down volume-imbalance reversion
#    Over a trailing window, split volume into up-candle vs down-candle volume.
#    When one side dominates strongly, fade it (mean reversion of order flow).
# --------------------------------------------------------------------------
def vol_imbalance_rev(df, span=12, thresh=0.7):
    r = _ret(df)
    v = df["volume"].astype(float)
    up = pd.Series(np.where(r.values > 0, v.values, 0.0), index=df.index).rolling(span).sum()
    dn = pd.Series(np.where(r.values < 0, v.values, 0.0), index=df.index).rolling(span).sum()
    imb = (up - dn) / (up + dn + 1e-12)
    sig = np.zeros(len(df), dtype=int)
    sig[imb.values > thresh] = -1   # too much buy volume -> fade down
    sig[imb.values < -thresh] = 1   # too much sell volume -> fade up
    return sig


# --------------------------------------------------------------------------
# 3. Volume-weighted momentum
#    Weight each recent candle's direction by its share of the window's volume,
#    then follow the net (volume-heavy candles dominate the vote). Continuation.
# --------------------------------------------------------------------------
def vol_weighted_mom(df, span=12):
    r = _ret(df)
    v = df["volume"].astype(float)
    w = v / (v.rolling(span).sum() + 1e-12)
    contrib = pd.Series(np.sign(r.fillna(0).values) * w.values, index=df.index)
    score = contrib.rolling(span).sum()
    return np.sign(score.fillna(0).values).astype(int)


# --------------------------------------------------------------------------
# 4. On-balance-volume trend
#    OBV = cumulative signed volume (expanding, causal). Trend-follow the sign of
#    the slope of its EMA.
# --------------------------------------------------------------------------
def obv_trend(df, span=24):
    r = _ret(df)
    v = df["volume"].astype(float)
    obv = (np.sign(r.fillna(0).values) * v.values).cumsum()
    obv = pd.Series(obv, index=df.index)
    ema = obv.ewm(span=span, adjust=False).mean()
    return np.sign(ema.diff().fillna(0).values).astype(int)


# --------------------------------------------------------------------------
# 5. Low-volume drift
#    When current volume is below its trailing average (quiet regime), follow the
#    last candle's direction; otherwise stand aside.
# --------------------------------------------------------------------------
def low_vol_drift(df, span=48, vol_z=-0.3):
    r = _ret(df)
    volz = _volz(df, span)
    quiet = volz < vol_z
    sig = np.where(quiet.values, np.sign(r.fillna(0).values), 0)
    return sig.astype(int)


# --------------------------------------------------------------------------
# 6. Volume-confirmed breakout
#    Break of the trailing high/low range, but ONLY when accompanied by a volume
#    spike (trailing z-score). Momentum in the breakout direction.
# --------------------------------------------------------------------------
def vol_confirm_breakout(df, span=24, vol_z=1.0):
    hi = df["high"].rolling(span).max().shift(1)
    lo = df["low"].rolling(span).min().shift(1)
    volz = _volz(df, span)
    confirmed = volz.values > vol_z
    sig = np.zeros(len(df), dtype=int)
    sig[(df["close"].values > hi.values) & confirmed] = 1
    sig[(df["close"].values < lo.values) & confirmed] = -1
    return sig


STRATEGIES = {
    "vol_spike_fade": vol_spike_fade,
    "vol_imbalance_rev": vol_imbalance_rev,
    "vol_weighted_mom": vol_weighted_mom,
    "obv_trend": obv_trend,
    "low_vol_drift": low_vol_drift,
    "vol_confirm_breakout": vol_confirm_breakout,
}
