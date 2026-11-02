"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-11-02 17:44 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def kyle_lambda_regime(df):
    # Use Amihud illiquidity (|return|/volume) as a rolling price-impact estimate. When impact is LOW (deep book absorbing flow), informed order flow should trend-continue; when impact is HIGH (thin, moves 
    r = df['close'].pct_change()
    vol = df['volume'].replace(0, np.nan)
    amihud = (r.abs() / vol)
    med = amihud.rolling(120, min_periods=30).median()
    illiq = amihud > med
    mom = np.sign(r).fillna(0)
    sig = np.where(illiq, -mom, mom)
    valid = med.notna() & amihud.notna()
    sig = np.where(valid, sig, 0)
    sig = pd.Series(sig, index=df.index).fillna(0)
    return sig.astype(int).values

def jump_reversion_bipower(df):
    # Decompose realized variation into continuous (diffusion) and jump components using bipower variation, which is robust to jumps. When the current bar's return exceeds a multiple of the jump-robust loca
    r = df['close'].pct_change()
    bpv = (r.abs() * r.abs().shift(1)).rolling(30, min_periods=10).mean() * (np.pi/2.0)
    sig_vol = np.sqrt(bpv)
    jump = r.abs() > 3.0 * sig_vol
    sig = np.where(jump, -np.sign(r), 0)
    sig = pd.Series(sig, index=df.index).fillna(0)
    return sig.astype(int).values

def round_number_magnet(df):
    # Behavioral round-number gravitation: when price sits just off a psychologically salient $100 level, order clustering tends to pull it toward the level. Signal fades the small deviation back toward the
    c = df['close']
    step = 100.0
    nearest = (c / step).round() * step
    d = (c - nearest) / c
    near = d.abs() < 0.0008
    sig = np.where(near, -np.sign(d), 0)
    sig = pd.Series(sig, index=df.index).fillna(0)
    return sig.astype(int).values

def vol_accel_return_corr(df):
    # Interaction between volume ACCELERATION (diff of volume) and returns. When rising volume is correlated with up-moves over a short window, flow is genuinely demand-driven and should continue; negative 
    r = df['close'].pct_change()
    dv = df['volume'].diff()
    corr = r.rolling(30, min_periods=15).corr(dv)
    base = np.sign(corr) * np.sign(r)
    sig = np.where(corr.abs() > 0.2, base, 0)
    sig = pd.Series(sig, index=df.index).fillna(0)
    return sig.astype(int).values

def semivariance_skew_fade(df):
    # Realized semivariance asymmetry: split recent squared returns into upside vs downside halves. Strong downside dominance signals fear/overshoot (contrarian buy), strong upside dominance signals greedy 
    r = df['close'].pct_change()
    up = (r.clip(lower=0)**2).rolling(24, min_periods=12).sum()
    dn = (r.clip(upper=0)**2).rolling(24, min_periods=12).sum()
    denom = (up + dn).replace(0, np.nan)
    asym = (up - dn) / denom
    sig = np.where(asym.abs() > 0.4, -np.sign(asym), 0)
    sig = pd.Series(sig, index=df.index).fillna(0)
    return sig.astype(int).values

def absorption_breakout(df):
    # Detect absorption bars: abnormally high volume packed into an unusually narrow range implies a large passive order soaking up flow. The side on which the close settles reveals who won; trade in that d
    rng = (df['high'] - df['low'])
    v_mean = df['volume'].rolling(50, min_periods=20).mean()
    v_std = df['volume'].rolling(50, min_periods=20).std()
    v_z = (df['volume'] - v_mean) / v_std
    rng_med = rng.rolling(50, min_periods=20).median()
    absorb = (v_z > 1.0) & (rng < rng_med)
    pos = (df['close'] - df['low']) / rng.replace(0, np.nan)
    sig = np.where(absorb, np.sign(pos - 0.5), 0)
    sig = pd.Series(sig, index=df.index).fillna(0)
    return sig.astype(int).values

STRATEGIES = {
    "kyle_lambda_regime": kyle_lambda_regime,
    "jump_reversion_bipower": jump_reversion_bipower,
    "round_number_magnet": round_number_magnet,
    "vol_accel_return_corr": vol_accel_return_corr,
    "semivariance_skew_fade": semivariance_skew_fade,
    "absorption_breakout": absorption_breakout,
}
