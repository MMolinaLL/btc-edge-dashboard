"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-09-28 16:24 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def kyle_lambda_absorption(df):
    # Compute per-bar price impact |ret|/volume (a Kyle-lambda proxy). When a move happens with LOW impact it was absorbed by real liquidity -> continue; when it happens with HIGH impact it was a thin overs
    ret = df['close'].pct_change()
    vol = df['volume']
    impact = ret.abs() / (vol + 1e-9)
    lo = impact.rolling(120).quantile(0.30)
    hi = impact.rolling(120).quantile(0.75)
    r = np.sign(ret.values)
    low_imp = (impact < lo).values
    high_imp = (impact > hi).values
    sig = np.where(low_imp, r, np.where(high_imp, -r, 0))
    return np.nan_to_num(sig).astype(int)

def realized_semivariance_skew(df):
    # Split recent squared returns into upside vs downside realized semivariance. Persistent dominance of one side (volatility asymmetry) predicts short-run directional drift, independent of the simple mean
    ret = df['close'].pct_change()
    up = ret.clip(lower=0) ** 2
    dn = ret.clip(upper=0) ** 2
    w = 24
    su = up.rolling(w).sum()
    sd = dn.rolling(w).sum()
    skew = (su - sd) / (su + sd + 1e-12)
    thr = 0.25
    sig = np.where(skew > thr, 1, np.where(skew < -thr, -1, 0))
    return np.nan_to_num(sig).astype(int)

def variance_ratio_regime(df):
    # Use a rolling variance ratio (var of k-bar returns / k*var of 1-bar returns) to decide the sign convention: VR>1 means microstructure is trending (follow last move), VR<1 means mean-reverting (fade la
    ret = df['close'].pct_change()
    k = 5
    w = 72
    retk = df['close'].pct_change(k)
    v1 = ret.rolling(w).var()
    vk = retk.rolling(w).var()
    vr = vk / (k * v1 + 1e-12)
    last = np.sign(ret.values)
    sig = np.where(vr.values > 1.10, last, np.where(vr.values < 0.90, -last, 0))
    return np.nan_to_num(sig).astype(int)

def liquidation_cascade_reversion(df):
    # Asymmetric overshoot: on deep venues sharp down-moves with volume spikes are often forced-liquidation overshoots that bounce, while up-spikes are less reverting. Encode asymmetric z-score thresholds g
    ret = df['close'].pct_change()
    z = ret / (ret.rolling(72).std() + 1e-12)
    vexp = df['volume'] / (df['volume'].rolling(72).mean() + 1e-9)
    down = (z < -1.5) & (vexp > 1.3)
    up = (z > 2.2) & (vexp > 1.6)
    sig = np.where(down.values, 1, np.where(up.values, -1, 0))
    return np.nan_to_num(sig).astype(int)

def compression_expansion_break(df):
    # Volatility compression (short-window true range far below its longer baseline) followed by a volume-backed expansion tends to resolve directionally. Trade the direction of the expanding bar only under
    tr = (df['high'] - df['low'])
    comp = tr.rolling(6).mean() / (tr.rolling(60).mean() + 1e-9)
    vexp = df['volume'] / (df['volume'].rolling(60).mean() + 1e-9)
    ret = df['close'].pct_change()
    cond = (comp < 0.75) & (vexp > 1.5)
    sig = np.where(cond.values, np.sign(ret.values), 0)
    return np.nan_to_num(sig).astype(int)

def depth_withdrawal_flow(df):
    # Effective depth = dollar-volume / range. When depth is steadily FALLING (liquidity being withdrawn) while price trends the same way over a few bars, an informed participant is pushing a thinning book 
    dvol = df['close'] * df['volume']
    depth = dvol / ((df['high'] - df['low']) + 1e-9)
    depth_tr = depth.pct_change().rolling(3).mean()
    ret3 = df['close'].pct_change(3)
    dn_depth = (depth_tr < 0).values
    sig = np.where(dn_depth & (ret3.values > 0), 1,
                   np.where(dn_depth & (ret3.values < 0), -1, 0))
    return np.nan_to_num(sig).astype(int)

STRATEGIES = {
    "kyle_lambda_absorption": kyle_lambda_absorption,
    "realized_semivariance_skew": realized_semivariance_skew,
    "variance_ratio_regime": variance_ratio_regime,
    "liquidation_cascade_reversion": liquidation_cascade_reversion,
    "compression_expansion_break": compression_expansion_break,
    "depth_withdrawal_flow": depth_withdrawal_flow,
}
