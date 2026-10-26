"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-10-26 14:48 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def semivar_asymmetry_reversal(df):
    # Split recent realized variance into downside and upside halves; a heavy imbalance toward downside variance marks capitulation that tends to bounce (and vice versa). This is distinct from vol-regime sw
    close = df['close']
    ret = close.pct_change()
    n = 24
    up = ret.clip(lower=0.0)**2
    dn = ret.clip(upper=0.0)**2
    rsv_up = up.rolling(n).sum()
    rsv_dn = dn.rolling(n).sum()
    asym = (rsv_dn - rsv_up) / (rsv_dn + rsv_up + 1e-12)
    # strong downside variance -> expect mean-reversion up
    thr = 0.35
    sig = np.where(asym > thr, 1, np.where(asym < -thr, -1, 0))
    return np.nan_to_num(sig).astype(int)

def amihud_gated_momentum(df):
    # Use Amihud illiquidity (|ret|/volume) as a gate: only follow short-term momentum when illiquidity is unusually LOW relative to its own recent norm, meaning the market absorbed flow cheaply and the mov
    close = df['close']
    vol = df['volume']
    ret = close.pct_change()
    illiq = ret.abs() / (vol + 1e-9)
    illiq_avg = illiq.rolling(48).mean()
    illiq_low = illiq < (illiq_avg * 0.7)
    mom = np.sign(ret.rolling(6).sum())
    sig = np.where(illiq_low.values, mom.values, 0)
    return np.nan_to_num(sig).astype(int)

def kyle_lambda_residual_fade(df):
    # Estimate a rolling price-impact coefficient (beta of return on signed volume), compute the part of the latest return NOT explained by signed order flow, and fade it: price that moved without commensur
    close = df['close']
    vol = df['volume']
    ret = close.pct_change()
    sv = np.sign(ret) * vol
    n = 48
    cov = (ret*sv).rolling(n).mean() - ret.rolling(n).mean()*sv.rolling(n).mean()
    var = sv.rolling(n).var()
    beta = cov / (var + 1e-12)
    expected = beta * sv
    resid = ret - expected
    rstd = resid.rolling(n).std()
    sig = np.where(resid > 0.5*rstd, -1, np.where(resid < -0.5*rstd, 1, 0))
    return np.nan_to_num(sig).astype(int)

def volofvol_regime_flip(df):
    # Measure volatility-of-volatility. When vol-of-vol is high the tape is erratic and short moves mean-revert; when vol-of-vol is calm, short moves persist. Same momentum input, opposite sign depending on
    close = df['close']
    ret = close.pct_change()
    vest = ret.rolling(12).std()
    vov = vest.rolling(12).std()
    vov_ref = vov.rolling(96).mean()
    mom = np.sign(ret.rolling(3).sum())
    high_vov = (vov > vov_ref).values
    sig = np.where(high_vov, -mom.values, mom.values)
    return np.nan_to_num(sig).astype(int)

def compression_volflow_breakout(df):
    # Detect intrabar range compression (recent true range far below its longer norm), and pick breakout direction from the volume-weighted intrabar close-location tilt. Direction comes from where trades cl
    close = df['close']; high = df['high']; low = df['low']; vol = df['volume']
    tr = (high - low)
    tr_short = tr.rolling(6).mean()
    tr_long = tr.rolling(48).mean()
    compressed = (tr_short < tr_long * 0.7).values
    clv = ((close - low) - (high - close)) / ((high - low) + 1e-12)
    tilt = (clv * vol).rolling(12).sum()
    t = tilt.values
    sig = np.where(compressed & (t > 0), 1, np.where(compressed & (t < 0), -1, 0))
    return np.nan_to_num(sig).astype(int)

def flow_acceleration(df):
    # Track the acceleration (second difference) of smoothed cumulative signed volume. Steady flow is already priced; an accelerating imbalance signals fresh directional demand not yet fully absorbed. Gated
    close = df['close']; vol = df['volume']
    ret = close.pct_change()
    sv = np.sign(ret) * vol
    flow = sv.ewm(span=10, adjust=False).mean()
    accel = flow.diff()
    accel_s = accel.ewm(span=5, adjust=False).mean()
    astd = accel_s.rolling(48).std()
    agree = np.sign(flow) == np.sign(accel_s)
    strong = (accel_s.abs() > 0.5*astd).values
    base = np.sign(accel_s).values
    sig = np.where(agree.values & strong, base, 0)
    return np.nan_to_num(sig).astype(int)

STRATEGIES = {
    "semivar_asymmetry_reversal": semivar_asymmetry_reversal,
    "amihud_gated_momentum": amihud_gated_momentum,
    "kyle_lambda_residual_fade": kyle_lambda_residual_fade,
    "volofvol_regime_flip": volofvol_regime_flip,
    "compression_volflow_breakout": compression_volflow_breakout,
    "flow_acceleration": flow_acceleration,
}
