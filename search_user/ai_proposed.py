"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-11-23 19:46 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def amihud_illiq_reversion(df):
    # Amihud illiquidity (|return| per unit volume) spikes when a move happened on thin participation; such moves are transient and tend to revert. Only fade moves that occurred under abnormally high price-
    ret = df['close'].pct_change()
    vol = df['volume'].replace(0, np.nan)
    illiq = (ret.abs() / vol).replace([np.inf, -np.inf], np.nan)
    med = illiq.rolling(120, min_periods=30).median()
    mad = (illiq - med).abs().rolling(120, min_periods=30).median()
    high_impact = illiq > (med + 2.0 * mad)
    sig = np.where(high_impact & (ret > 0), -1,
          np.where(high_impact & (ret < 0), 1, 0))
    return np.nan_to_num(sig).astype(int)

def kyle_lambda_momentum(df):
    # Estimate a rolling Kyle's lambda = cov(return, signed volume)/var(signed volume). When lambda is low (deep, resilient book), order flow does NOT easily reverse and short-horizon momentum persists; fol
    ret = df['close'].pct_change()
    sv = np.sign(ret) * df['volume']
    w = 60
    cov = ret.rolling(w, min_periods=20).cov(sv)
    var = sv.rolling(w, min_periods=20).var()
    lam = (cov / var).replace([np.inf, -np.inf], np.nan)
    lam_med = lam.rolling(240, min_periods=60).median()
    deep = lam < lam_med
    mom = np.sign(df['close'].pct_change(3))
    sig = np.where(deep, mom, 0)
    return np.nan_to_num(sig).astype(int)

def variance_ratio_regime(df):
    # The variance ratio VR(k)=Var(k-period ret)/(k*Var(1-period ret)) distinguishes trending (VR>1) from mean-reverting (VR<1) microstructure. Trade momentum when VR is clearly >1, fade when clearly <1, ot
    ret = df['close'].pct_change()
    w = 72
    k = 6
    v1 = ret.rolling(w, min_periods=25).var()
    vk = df['close'].pct_change(k).rolling(w, min_periods=25).var()
    vr = (vk / (k * v1)).replace([np.inf, -np.inf], np.nan)
    mom = np.sign(df['close'].pct_change(k))
    sig = np.where(vr > 1.15, mom,
          np.where(vr < 0.85, -mom, 0))
    return np.nan_to_num(sig).astype(int)

def jump_vs_diffusion(df):
    # Separate jumps from continuous diffusion: a single bar whose standardized return far exceeds recent diffusive vol is likely information-driven if accompanied by elevated volume (continuation) but liqu
    ret = df['close'].pct_change()
    dvol = ret.rolling(60, min_periods=20).std()
    z = (ret / dvol).replace([np.inf, -np.inf], np.nan)
    vm = df['volume'].rolling(60, min_periods=20).mean()
    vs = df['volume'].rolling(60, min_periods=20).std()
    vz = ((df['volume'] - vm) / vs).replace([np.inf, -np.inf], np.nan)
    jump = z.abs() > 2.5
    sig = np.where(jump & (vz > 0.5), np.sign(z),
          np.where(jump & (vz < -0.5), -np.sign(z), 0))
    return np.nan_to_num(sig).astype(int)

def absorption_reversal(df):
    # Absorption: large volume transacted while the bar's range stays compressed means aggressive flow is being met by resting liquidity and cannot move price. Such bars typically precede a reversal of the 
    rng = ((df['high'] - df['low']) / df['close']).replace([np.inf, -np.inf], np.nan)
    rng_m = rng.rolling(60, min_periods=20).mean()
    vm = df['volume'].rolling(60, min_periods=20).mean()
    vs = df['volume'].rolling(60, min_periods=20).std()
    vz = ((df['volume'] - vm) / vs).replace([np.inf, -np.inf], np.nan)
    absorb = (rng < 0.7 * rng_m) & (vz > 1.5)
    body = np.sign(df['close'] - df['open'])
    sig = np.where(absorb, -body, 0)
    return np.nan_to_num(sig).astype(int)

def impact_asymmetry(df):
    # Compare average price-impact-per-volume on up bars vs down bars over a rolling window. If up moves are achieved with more impact per unit volume than down moves, the ask side is thinner (resistance be
    ret = df['close'].pct_change()
    imp = (ret.abs() / df['volume']).replace([np.inf, -np.inf], np.nan)
    up_imp = imp.where(ret > 0)
    dn_imp = imp.where(ret < 0)
    w = 80
    iu = up_imp.rolling(w, min_periods=15).mean()
    idn = dn_imp.rolling(w, min_periods=15).mean()
    sig = np.where(iu > 1.2 * idn, 1,
          np.where(idn > 1.2 * iu, -1, 0))
    return np.nan_to_num(sig).astype(int)

STRATEGIES = {
    "amihud_illiq_reversion": amihud_illiq_reversion,
    "kyle_lambda_momentum": kyle_lambda_momentum,
    "variance_ratio_regime": variance_ratio_regime,
    "jump_vs_diffusion": jump_vs_diffusion,
    "absorption_reversal": absorption_reversal,
    "impact_asymmetry": impact_asymmetry,
}
