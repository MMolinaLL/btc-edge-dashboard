"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-10-12 17:17 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def kyle_lambda_deep_momentum(df):
    # Estimate rolling price impact (|return|/volume). When lambda is LOW the book is deep and moves reflect genuine absorbed flow, so momentum should persist; we only follow direction in the deep-book regi
    close = df['close']
    vol = df['volume'].replace(0, np.nan)
    ret = close.pct_change()
    lam = (ret.abs() / vol).rolling(50, min_periods=20).median()
    lam_ref = lam.rolling(200, min_periods=50).median().shift(1)
    deep = lam < lam_ref
    sig = np.where(deep.values & (ret.values > 0), 1,
          np.where(deep.values & (ret.values < 0), -1, 0))
    sig = np.nan_to_num(sig, nan=0.0)
    return sig.astype(int)

def jump_continuation_informed(df):
    # Decompose the last move into jump vs diffusion: a return many sigma beyond recent realized vol AND accompanied by a volume surge is informational and tends to continue one more bar, unlike ordinary no
    ret = df['close'].pct_change()
    rv = ret.rolling(48, min_periods=20).std().shift(1)
    z = ret / rv
    v = df['volume']
    volz = (v - v.rolling(48, min_periods=20).mean()) / v.rolling(48, min_periods=20).std()
    jump = (z.abs() > 2.5) & (volz > 1.0)
    sig = np.where(jump.values & (ret.values > 0), 1,
          np.where(jump.values & (ret.values < 0), -1, 0))
    sig = np.nan_to_num(sig, nan=0.0)
    return sig.astype(int)

def path_efficiency_switch(df):
    # Compute directional efficiency = net displacement / total path length over a window (a proxy for local fractal dimension). Clean, efficient moves trend; rough, choppy moves mean-revert. Use efficiency
    close = df['close']
    n = 12
    net = (close - close.shift(n)).abs()
    path = close.diff().abs().rolling(n, min_periods=n).sum()
    eff = net / path.replace(0, np.nan)
    drift = np.sign((close - close.shift(n)).values)
    sig = np.where(eff.values > 0.6, drift,
          np.where(eff.values < 0.3, -drift, 0))
    sig = np.nan_to_num(sig, nan=0.0)
    return sig.astype(int)

def semivariance_panic_reversion(df):
    # Measure asymmetry between downside and upside realized semivariance. Strong downside dominance reflects leverage/liquidation panic that typically over-shoots and bounces; strong upside dominance eupho
    ret = df['close'].pct_change()
    up = ret.clip(lower=0)
    dn = (-ret).clip(lower=0)
    usv = (up ** 2).rolling(24, min_periods=12).sum()
    dsv = (dn ** 2).rolling(24, min_periods=12).sum()
    asym = (dsv - usv) / (dsv + usv)
    sig = np.where(asym.values > 0.5, 1,
          np.where(asym.values < -0.5, -1, 0))
    sig = np.nan_to_num(sig, nan=0.0)
    return sig.astype(int)

def thin_move_fade(df):
    # Inverse of the deep-book case: when a sizable price move happens on unusually LOW volume (high per-unit impact), it is fragile overextension lacking real flow support and tends to retrace. Fade only t
    ret = df['close'].pct_change()
    vol = df['volume']
    impact = ret.abs() / (vol + 1e-9)
    imp_ref = impact.rolling(100, min_periods=40).median().shift(1)
    big = ret.abs() > ret.abs().rolling(48, min_periods=20).median().shift(1)
    thin = (impact > 2.0 * imp_ref) & big
    sig = np.where(thin.values & (ret.values > 0), -1,
          np.where(thin.values & (ret.values < 0), 1, 0))
    sig = np.nan_to_num(sig, nan=0.0)
    return sig.astype(int)

def variance_ratio_conditional(df):
    # Lo-MacKinlay variance ratio: var of k-bar returns divided by k times var of 1-bar returns. VR>1 signals trending micro-regime, VR<1 mean-reverting. Use the regime to conditionally follow or fade the m
    close = df['close']
    ret = close.pct_change()
    k = 6
    var1 = ret.rolling(60, min_periods=30).var()
    vark = close.pct_change(k).rolling(60, min_periods=30).var()
    vr = vark / (k * var1)
    drift = np.sign(ret.values)
    sig = np.where(vr.values > 1.1, drift,
          np.where(vr.values < 0.9, -drift, 0))
    sig = np.nan_to_num(sig, nan=0.0)
    return sig.astype(int)

STRATEGIES = {
    "kyle_lambda_deep_momentum": kyle_lambda_deep_momentum,
    "jump_continuation_informed": jump_continuation_informed,
    "path_efficiency_switch": path_efficiency_switch,
    "semivariance_panic_reversion": semivariance_panic_reversion,
    "thin_move_fade": thin_move_fade,
    "variance_ratio_conditional": variance_ratio_conditional,
}
