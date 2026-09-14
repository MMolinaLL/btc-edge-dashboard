"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-09-14 14:41 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def illiquidity_regime_split(df):
    # Amihud illiquidity (|ret| per dollar volume) separates two very different momentum regimes: when recent moves are CHEAP to make (low illiquidity, efficient/informed flow) momentum continues; when move
    close = df['close']
    ret = close.pct_change()
    dvol = (df['volume'] * close).replace(0, np.nan)
    amihud = (ret.abs() / (dvol + 1e-12))
    a_base = amihud.rolling(120).median().shift(1)
    a_cur = amihud.rolling(6).mean().shift(1)
    mom = ret.rolling(6).sum().shift(1)
    low_il = (a_cur <= a_base).values
    high_il = (a_cur > a_base).values
    up = (mom > 0).values
    dn = (mom < 0).values
    sig = np.zeros(len(df), dtype=int)
    sig[low_il & up] = 1
    sig[low_il & dn] = -1
    sig[high_il & up] = -1
    sig[high_il & dn] = 1
    return sig

def realized_skew_reversal(df):
    # Rolling realized skewness of 5-min returns as a standalone directional predictor. Documented cross-sectional/time-series result: positive realized skew (lottery-like upside spikes) tends to precede ne
    ret = df['close'].pct_change()
    sk = ret.rolling(36).skew().shift(1)
    sig = np.where(sk > 0.6, -1, np.where(sk < -0.6, 1, 0)).astype(int)
    return sig

def vol_of_vol_gated_trend(df):
    # Trend signals are only reliable when the volatility process itself is stable. Compute volatility-of-volatility; only take a modest momentum position when vol-of-vol is below its own median (stable reg
    ret = df['close'].pct_change()
    rv = ret.rolling(12).std()
    vov = rv.rolling(12).std()
    vov_med = vov.rolling(120).median().shift(1)
    vov_l = vov.shift(1)
    mom = ret.rolling(12).mean().shift(1)
    stable = (vov_l < vov_med).values
    up = (mom > 0).values
    dn = (mom < 0).values
    sig = np.zeros(len(df), dtype=int)
    sig[stable & up] = 1
    sig[stable & dn] = -1
    return sig

def signed_flow_persistence(df):
    # Order-flow proxy = sign(return)*volume. Instead of using its level (imbalance, already tried), detect ACCELERATION: same-signed cumulative flow in the recent window that is strictly larger in magnitud
    ret = df['close'].pct_change()
    sv = np.sign(ret) * df['volume']
    flow = sv.rolling(6).sum().shift(1)
    flow_prev = sv.rolling(6).sum().shift(7)
    up = ((flow > 0) & (flow_prev > 0) & (flow > flow_prev)).values
    dn = ((flow < 0) & (flow_prev < 0) & (flow < flow_prev)).values
    sig = np.zeros(len(df), dtype=int)
    sig[up] = 1
    sig[dn] = -1
    return sig

def clv_drift(df):
    # Close-location value ((close-low)-(high-close))/range measures intrabar buying vs selling pressure. Rather than reading a single candle (candle-shape, tried), track the DRIFT of smoothed buying pressu
    high = df['high']; low = df['low']; close = df['close']
    rng = (high - low).replace(0, np.nan)
    clv = ((close - low) - (high - close)) / (rng + 1e-12)
    clv_ma = clv.rolling(10).mean()
    lvl = clv_ma.shift(1)
    slope = (clv_ma - clv_ma.shift(5)).shift(1)
    up = ((lvl > 0.1) & (slope > 0)).values
    dn = ((lvl < -0.1) & (slope < 0)).values
    sig = np.zeros(len(df), dtype=int)
    sig[up] = 1
    sig[dn] = -1
    return sig

def compression_impact_break(df):
    # Combines range compression with price-impact context. When true range has contracted sharply relative to its baseline (coiled) AND recent moves are low-impact (efficient), a directional bias from clos
    high = df['high']; low = df['low']; close = df['close']
    tr = (high - low)
    atr = tr.rolling(24).mean().shift(1)
    tr_recent = tr.rolling(5).mean().shift(1)
    compressed = (tr_recent < 0.65 * atr)
    ret = close.pct_change()
    dvol = (df['volume'] * close).replace(0, np.nan)
    amihud = (ret.abs() / (dvol + 1e-12))
    eff = (amihud.rolling(5).mean().shift(1) <= amihud.rolling(120).median().shift(1))
    rmin = close.rolling(12).min()
    rmax = close.rolling(12).max()
    cl = ((close - rmin) / (rmax - rmin + 1e-12)).shift(1)
    cond = (compressed & eff).values
    up = cond & (cl > 0.6).values
    dn = cond & (cl < 0.4).values
    sig = np.zeros(len(df), dtype=int)
    sig[up] = 1
    sig[dn] = -1
    return sig

STRATEGIES = {
    "illiquidity_regime_split": illiquidity_regime_split,
    "realized_skew_reversal": realized_skew_reversal,
    "vol_of_vol_gated_trend": vol_of_vol_gated_trend,
    "signed_flow_persistence": signed_flow_persistence,
    "clv_drift": clv_drift,
    "compression_impact_break": compression_impact_break,
}
