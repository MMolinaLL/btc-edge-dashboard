"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-09-07 13:55 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def kyle_lambda_gate(df):
    # Estimate recent price impact per unit volume (Kyle's lambda). A directional move on LOW impact means a deep book absorbed real informed flow -> continue; a move on HIGH impact was thin/noise -> fade. 
    n = 24
    ret = df['close'].pct_change()
    vol = df['volume'].replace(0, np.nan)
    impact = (ret.abs() / vol)
    med = impact.rolling(n).median()
    mom = ret.rolling(5).sum()
    cheap = (impact < med)
    up = mom > 0
    sig = np.where(cheap & up, 1,
          np.where(cheap & (~up), -1,
          np.where((~cheap) & up, -1,
          np.where((~cheap) & (~up), 1, 0))))
    sig = np.where(mom.isna().values | impact.isna().values, 0, sig)
    return np.nan_to_num(sig).astype(int)

def variance_ratio_regime(df):
    # Compare the squared NET return over a window to the SUM of squared bar returns. If net move dominates (path efficient, variance-ratio>1) the trend is real -> follow; if the path was choppy relative to
    n = 12
    ret = df['close'].pct_change()
    net = ret.rolling(n).sum()
    sq = (ret**2).rolling(n).sum()
    q = (net**2) / (sq + 1e-12)
    s = np.sign(net)
    sig = np.where(q > 1.3, s, np.where(q < 0.4, -s, 0))
    sig = np.where(net.isna().values, 0, sig)
    return np.nan_to_num(sig).astype(int)

def vw_ew_return_divergence(df):
    # Volume-weighted mean return vs equal-weighted mean return over a window. If VW>EW, the high-volume bars were more bullish than average -> informed accumulation -> lean long (and vice versa). Uses the 
    n = 20
    ret = df['close'].pct_change()
    v = df['volume']
    vw = (ret * v).rolling(n).sum() / (v.rolling(n).sum() + 1e-12)
    ew = ret.rolling(n).mean()
    diff = vw - ew
    scale = diff.abs().rolling(n).median()
    sig = np.where(diff > 0.5 * scale, 1, np.where(diff < -0.5 * scale, -1, 0))
    sig = np.where(diff.isna().values, 0, sig)
    return np.nan_to_num(sig).astype(int)

def range_exhaustion_reversal(df):
    # A bar with an unusually large true range AND a volume spike BUT a small body signals climax/exhaustion (buyers or sellers spent effort without net progress). Predict the next bar reverses the exhausti
    n = 24
    rng = (df['high'] - df['low'])
    body = (df['close'] - df['open'])
    tr_med = rng.rolling(n).median()
    vol_med = df['volume'].rolling(n).median()
    big = (rng > 1.6 * tr_med) & (df['volume'] > 1.6 * vol_med)
    small_body = body.abs() < 0.35 * (rng + 1e-12)
    bar_dir = np.sign(body)
    sig = np.where(big & small_body, -bar_dir, 0)
    sig = np.where(tr_med.isna().values, 0, sig)
    return np.nan_to_num(sig).astype(int)

def realized_skew_reversal(df):
    # Rolling realized skewness of short returns. Strong positive skew means recent upside spikes/jumps that tend to short-term revert; strong negative skew (downside spikes) tends to bounce. A higher-momen
    n = 30
    ret = df['close'].pct_change()
    sk = ret.rolling(n).skew()
    sig = np.where(sk > 0.6, -1, np.where(sk < -0.6, 1, 0))
    sig = np.where(sk.isna().values, 0, sig)
    return np.nan_to_num(sig).astype(int)

def vol_of_vol_momentum_gate(df):
    # Volatility-of-volatility as a regime switch for momentum. When vol-of-vol is calm, realized-vol is stable and short momentum tends to persist; when vol-of-vol spikes (regime instability), the same mom
    n = 20
    ret = df['close'].pct_change()
    rv = ret.rolling(6).std()
    vov = rv.rolling(n).std()
    vov_med = vov.rolling(n * 3).median()
    mom = ret.rolling(6).sum()
    calm = vov < vov_med
    s = np.sign(mom)
    sig = np.where(calm, s, -s)
    sig = np.where(vov_med.isna().values | mom.isna().values, 0, sig)
    return np.nan_to_num(sig).astype(int)

STRATEGIES = {
    "kyle_lambda_gate": kyle_lambda_gate,
    "variance_ratio_regime": variance_ratio_regime,
    "vw_ew_return_divergence": vw_ew_return_divergence,
    "range_exhaustion_reversal": range_exhaustion_reversal,
    "realized_skew_reversal": realized_skew_reversal,
    "vol_of_vol_momentum_gate": vol_of_vol_momentum_gate,
}
