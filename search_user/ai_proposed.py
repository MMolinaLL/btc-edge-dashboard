"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-08-31 15:48 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def liquidity_backed_momentum(df):
    # Amihud illiquidity conditioning: a move made on LOW price-impact (high volume relative to the move) is genuine order flow and tends to continue; a big move on thin volume is a spasm and is ignored. Tr
    ret = df['close'].pct_change()
    vol = df['volume'].replace(0, np.nan)
    impact = ret.abs() / vol
    med = impact.rolling(60, min_periods=30).median()
    low_impact = impact < med
    s = np.where(low_impact & (ret > 0), 1,
        np.where(low_impact & (ret < 0), -1, 0))
    sig = np.asarray(s).astype(int)
    return sig

def realized_skew_reversal(df):
    # Rolling realized skewness of 5-min returns captures asymmetric crash/melt-up pressure. Strong negative skew means downside tails just realized (over-shot fear) -> fade up; strong positive skew -> fade
    ret = df['close'].pct_change()
    skew = ret.rolling(36, min_periods=24).skew()
    s = np.where(skew < -0.7, 1, np.where(skew > 0.7, -1, 0))
    sig = np.asarray(s).astype(int)
    return sig

def volofvol_gated_drift(df):
    # Vol-of-vol as a stability gate (not a plain vol switch): when the volatility of volatility is calm (below its rolling median), short-horizon drift is more likely to be information-driven and persist; 
    ret = df['close'].pct_change()
    rv = ret.rolling(6, min_periods=6).std()
    vov = rv.rolling(24, min_periods=12).std()
    med = vov.rolling(120, min_periods=60).median()
    mom = df['close'].pct_change(6)
    calm = vov < med
    s = np.where(calm & (mom > 0), 1, np.where(calm & (mom < 0), -1, 0))
    sig = np.asarray(s).astype(int)
    return sig

def impact_efficiency_asymmetry(df):
    # Directional price-impact asymmetry: measure average return-per-unit-volume separately on up bars vs down bars. If it costs LESS volume to push price up than down (buyers more efficient), the book is s
    ret = df['close'].pct_change()
    vol = df['volume'].replace(0, np.nan)
    upimp = (ret.where(ret > 0) / vol).rolling(30, min_periods=10).mean()
    dnimp = (ret.where(ret < 0).abs() / vol).rolling(30, min_periods=10).mean()
    diff = upimp - dnimp
    sd = diff.rolling(60, min_periods=30).std()
    s = np.where(diff > 0.5 * sd, 1, np.where(diff < -0.5 * sd, -1, 0))
    sig = np.asarray(pd.Series(s, index=df.index).fillna(0)).astype(int)
    return sig

def flow_elasticity_regression(df):
    # Rolling regression of returns on signed volume gives a local price-impact elasticity (Kyle's lambda). Predicted move = elasticity * current signed flow; trade its sign. This is a conditional flow mode
    ret = df['close'].pct_change()
    sv = np.sign(ret) * df['volume']
    w = 30
    cov = ret.rolling(w, min_periods=15).cov(sv)
    var = sv.rolling(w, min_periods=15).var()
    beta = cov / var.replace(0, np.nan)
    pred = beta * sv
    s = np.where(pred > 0, 1, np.where(pred < 0, -1, 0))
    sig = np.asarray(pd.Series(s, index=df.index).fillna(0)).astype(int)
    return sig

def range_efficiency_trend(df):
    # Path efficiency interaction: compare net displacement over N bars to the total intrabar path (sum of true ranges). High efficiency = clean directional travel with little chop -> genuine trend likely t
    n = 10
    disp = (df['close'] - df['close'].shift(n)).abs()
    tr = (df['high'] - df['low'])
    path = tr.rolling(n, min_periods=n).sum()
    eff = disp / path.replace(0, np.nan)
    direction = np.sign(df['close'] - df['close'].shift(n))
    trending = eff > 0.45
    s = np.where(trending & (direction > 0), 1,
        np.where(trending & (direction < 0), -1, 0))
    sig = np.asarray(pd.Series(s, index=df.index).fillna(0)).astype(int)
    return sig

STRATEGIES = {
    "liquidity_backed_momentum": liquidity_backed_momentum,
    "realized_skew_reversal": realized_skew_reversal,
    "volofvol_gated_drift": volofvol_gated_drift,
    "impact_efficiency_asymmetry": impact_efficiency_asymmetry,
    "flow_elasticity_regression": flow_elasticity_regression,
    "range_efficiency_trend": range_efficiency_trend,
}
