"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-11-16 17:51 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def kyle_lambda_residual(df):
    # Rolling-regress returns on signed volume to estimate price impact (Kyle's lambda). The component of the current move explained by impact tends to persist; the UNEXPLAINED residual move is noise/overre
    ret = df['close'].pct_change()
    sv = np.sign(df['close'] - df['open']) * df['volume']
    w = 50
    mr = ret.rolling(w).mean(); ms = sv.rolling(w).mean()
    cov = (ret*sv).rolling(w).mean() - mr*ms
    var = (sv*sv).rolling(w).mean() - ms*ms
    lam = cov/(var+1e-12)
    expected = lam*sv
    resid = ret - expected
    rstd = resid.rolling(w).std()
    sig = np.where(resid >  0.8*rstd, -1,
          np.where(resid < -0.8*rstd,  1, 0))
    return np.nan_to_num(sig).astype(int)

def absorption_reversal(df):
    # High volume delivered into a SMALL range means a large passive player is absorbing the aggressor flow. The side that absorbs (inferred from where the bar closes inside its range) is the side with hidd
    rng = (df['high'] - df['low'])
    volma = df['volume'].rolling(50).mean()
    rngma = rng.rolling(50).mean()
    volz = df['volume']/(volma+1e-12)
    rz = rng/(rngma+1e-12)
    loc = (df['close'] - df['low'])/(rng+1e-12)
    absorb = (volz > 1.5) & (rz < 0.85)
    sig = np.where(absorb & (loc < 0.35),  1,
          np.where(absorb & (loc > 0.65), -1, 0))
    return np.nan_to_num(sig).astype(int)

def variance_ratio_regime(df):
    # Instead of pre-committing to momentum or mean-reversion, let the variance ratio (k-step var / k*1-step var) decide the regime bar-by-bar. VR>1 => diffusive/trending so follow the last move; VR<1 => me
    ret = df['close'].pct_change()
    k = 6
    var1 = ret.rolling(40).var()
    retk = df['close'].pct_change(k)
    vark = retk.rolling(40).var()
    vr = vark/(k*var1 + 1e-12)
    mom = np.sign(ret)
    sig = np.where(vr > 1.15,  mom,
          np.where(vr < 0.85, -mom, 0))
    return np.nan_to_num(sig).astype(int)

def realized_skew_reversal(df):
    # Realized return skewness over a recent window is a documented contrarian signal: a burst of large positive (right-skewed) returns tends to precede weakness and vice-versa, independent of simple moment
    ret = df['close'].pct_change()
    w = 48
    skew = ret.rolling(w).skew()
    sig = np.where(skew >  0.6, -1,
          np.where(skew < -0.6,  1, 0))
    return np.nan_to_num(sig).astype(int)

def jump_overshoot_fade(df):
    # Use bipower-variation as a jump-robust local variance estimate. A bar whose return far exceeds the smooth local volatility is an isolated liquidity-gap jump (not a trend), which typically overshoots a
    ret = df['close'].pct_change()
    absr = ret.abs()
    bv = (absr*absr.shift(1)).rolling(20).mean()
    sigma = np.sqrt(bv + 1e-18)
    trend = np.sign(ret.rolling(5).sum())
    jump = (absr > 3.0*sigma) & (np.sign(ret) != trend)
    sig = np.where(jump, -np.sign(ret), 0)
    return np.nan_to_num(sig).astype(int)

def flow_price_divergence(df):
    # Build an intrabar signed-flow proxy (close location within range times volume) and accumulate it. When price has risen but accumulated flow is net selling (or vice-versa), the move is unsupported by r
    rng = (df['high'] - df['low'])
    loc = ((df['close']-df['low']) - (df['high']-df['close']))/(rng+1e-12)
    flow = loc*df['volume']
    cf = flow.rolling(12).sum()
    cvol = df['volume'].rolling(12).sum()
    fz = cf/(cvol+1e-12)
    pchg = df['close'] - df['close'].shift(12)
    sig = np.where((pchg > 0) & (fz < -0.15), -1,
          np.where((pchg < 0) & (fz >  0.15),  1, 0))
    return np.nan_to_num(sig).astype(int)

STRATEGIES = {
    "kyle_lambda_residual": kyle_lambda_residual,
    "absorption_reversal": absorption_reversal,
    "variance_ratio_regime": variance_ratio_regime,
    "realized_skew_reversal": realized_skew_reversal,
    "jump_overshoot_fade": jump_overshoot_fade,
    "flow_price_divergence": flow_price_divergence,
}
