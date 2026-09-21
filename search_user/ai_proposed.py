"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-09-21 14:48 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def variance_ratio_regime_switch(df):
    # Use a rolling Lo-MacKinlay variance ratio to decide whether recent drift should be followed (trending regime, VR>1) or faded (mean-reverting regime, VR<1), with a neutral dead-zone around VR=1. This i
    ret = df['close'].pct_change()
    k = 6
    var1 = ret.rolling(72).var()
    retk = df['close'].pct_change(k)
    vark = retk.rolling(72).var()
    vr = vark / (k * var1)
    mom = np.sign(ret.rolling(k).sum())
    v = vr.values
    m = np.nan_to_num(mom.values)
    sig = np.where(v > 1.15, m, np.where(v < 0.85, -m, 0.0))
    sig = np.nan_to_num(sig)
    return sig.astype(int)

def kyle_lambda_liquidity_momentum(df):
    # Estimate a rolling price-impact coefficient (abs return per unit volume, a Kyle-lambda proxy). When impact is low relative to its own recent history, price is moving efficiently on flow so short drift
    r = df['close'].pct_change()
    vol = df['volume'].replace(0, np.nan)
    lam = (r.abs() / vol).rolling(50).mean()
    lam_med = lam.rolling(240).median()
    mom = np.sign(r.rolling(3).sum())
    lo = (lam < 0.8 * lam_med).values
    hi = (lam > 1.2 * lam_med).values
    m = np.nan_to_num(mom.values)
    sig = np.where(lo, m, np.where(hi, -m, 0.0))
    sig = np.nan_to_num(sig)
    return sig.astype(int)

def absorption_close_location(df):
    # Detect absorption bars: unusually high volume paired with an unusually compressed range (big flow that failed to move price far). This signals hidden liquidity being consumed; the next move tends to r
    rng = (df['high'] - df['low']).replace(0, np.nan)
    clv = ((df['close'] - df['low']) - (df['high'] - df['close'])) / rng
    vmu = df['volume'].rolling(50).mean()
    vsd = df['volume'].rolling(50).std()
    volz = (df['volume'] - vmu) / vsd
    rmu = rng.rolling(50).mean()
    rsd = rng.rolling(50).std()
    rngz = (rng - rmu) / rsd
    mask = (volz > 1.2) & (rngz < -0.4)
    sig = np.where(mask.values, np.sign(np.nan_to_num(clv.values)), 0.0)
    sig = np.nan_to_num(sig)
    return sig.astype(int)

def efficiency_ratio_gated_trend(df):
    # Kaufman efficiency ratio (net move / summed absolute moves) measures how directional recent action is. Only take the drift direction when the path is efficient relative to its own recent norm (true tr
    c = df['close']
    n = 10
    net = (c - c.shift(n)).abs()
    path = c.diff().abs().rolling(n).sum().replace(0, np.nan)
    er = net / path
    er_med = er.rolling(120).median()
    mom = np.sign(c - c.shift(n))
    trade = (er > er_med).values
    m = np.nan_to_num(mom.values)
    sig = np.where(trade, m, 0.0)
    sig = np.nan_to_num(sig)
    return sig.astype(int)

def vol_of_vol_stability_filter(df):
    # Volatility-of-volatility as a stability meter: when realized-vol itself is calm (low vol-of-vol), microstructure noise is low and short drift carries; when vol-of-vol spikes, the tape is regime-unstab
    ret = df['close'].pct_change()
    rv = ret.rolling(12).std()
    vov = rv.rolling(48).std()
    vov_med = vov.rolling(240).median()
    mom = np.sign(ret.rolling(6).sum())
    calm = (vov < vov_med).values
    m = np.nan_to_num(mom.values)
    sig = np.where(calm, m, 0.0)
    sig = np.nan_to_num(sig)
    return sig.astype(int)

def volume_weighted_close_pressure(df):
    # Measure intrabar buying/selling pressure as close position relative to the typical price (H+L+C)/3, scaled by range, then weight by relative volume and smooth. Persistent volume-backed pressure toward
    rng = (df['high'] - df['low']).replace(0, np.nan)
    tp = (df['high'] + df['low'] + df['close']) / 3.0
    press = (df['close'] - tp) / rng
    w = df['volume'] / df['volume'].rolling(50).mean()
    score = (press * w).rolling(3).mean()
    thr = score.rolling(100).std()
    s = score.values
    t = np.nan_to_num(thr.values)
    sig = np.where(s > t, 1.0, np.where(s < -t, -1.0, 0.0))
    sig = np.nan_to_num(sig)
    return sig.astype(int)

STRATEGIES = {
    "variance_ratio_regime_switch": variance_ratio_regime_switch,
    "kyle_lambda_liquidity_momentum": kyle_lambda_liquidity_momentum,
    "absorption_close_location": absorption_close_location,
    "efficiency_ratio_gated_trend": efficiency_ratio_gated_trend,
    "vol_of_vol_stability_filter": vol_of_vol_stability_filter,
    "volume_weighted_close_pressure": volume_weighted_close_pressure,
}
