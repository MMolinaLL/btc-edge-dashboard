"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-10-19 15:15 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def kyle_lambda_regime(df):
    # Estimate rolling price impact (|return| per unit volume, a Kyle's-lambda proxy). When impact is cheap relative to its own baseline the book is deep and directional pushes persist (momentum); when impa
    eps=1e-12
    r=np.log(df['close']).diff()
    lam=r.abs().rolling(20).sum()/(df['volume'].rolling(20).sum()+eps)
    base=lam.ewm(span=120).mean()
    mom=np.sign(df['close']-df['close'].shift(3))
    regime=pd.Series(np.where(lam<base,1.0,-1.0),index=df.index)
    sig=(regime*mom)
    sig=sig.replace([np.inf,-np.inf],0).fillna(0)
    return sig.round().astype(int).values

def variance_ratio_adaptive(df):
    # Compute a rolling variance ratio comparing k-bar return variance to k times 1-bar variance. VR>1 means returns compound (trending memory) so follow the k-bar move; VR<1 means over-differencing/reversi
    eps=1e-12
    k=6
    r1=np.log(df['close']).diff()
    rk=np.log(df['close']).diff(k)
    v1=r1.rolling(72).var()
    vk=rk.rolling(72).var()
    vr=vk/(k*v1+eps)
    mom=np.sign(df['close']-df['close'].shift(k))
    sig=pd.Series(np.where(vr>1.1,1.0,np.where(vr<0.9,-1.0,0.0)),index=df.index)*mom
    sig=sig.replace([np.inf,-np.inf],0).fillna(0)
    return sig.round().astype(int).values

def realized_skew_reversal(df):
    # Rolling realized skewness of 1-bar returns captures asymmetric tail pressure. A strongly positive skew means recent upside was driven by a few outsized jumps that tend to retrace; negative skew the re
    eps=1e-12
    r=np.log(df['close']).diff()
    sk=r.rolling(36).skew()
    scale=sk.abs().ewm(span=120).mean()+eps
    strong=(sk.abs()/scale)>1.0
    sig=pd.Series(np.where(strong,-np.sign(sk),0.0),index=df.index)
    sig=sig.replace([np.inf,-np.inf],0).fillna(0)
    return sig.round().astype(int).values

def absorption_continuation(df):
    # Detect liquidity absorption: bars where volume is abnormally high but the realized price move is abnormally small. That signature implies a large passive participant absorbing aggressive flow (accumul
    eps=1e-12
    r=np.log(df['close']).diff()
    vol=df['volume']
    volz=(vol-vol.rolling(50).mean())/(vol.rolling(50).std()+eps)
    absz=(r.abs()-r.abs().rolling(50).mean())/(r.abs().rolling(50).std()+eps)
    absorb=(volz>1.0)&(absz<-0.2)
    mom=np.sign(df['close']-df['close'].shift(2))
    sig=pd.Series(np.where(absorb,mom,0.0),index=df.index)
    sig=sig.replace([np.inf,-np.inf],0).fillna(0)
    return sig.round().astype(int).values

def vol_of_vol_reversion(df):
    # Instability of the volatility process (vol-of-vol) flags disorderly, emotionally-driven moves that overshoot. When short-run realized volatility is itself unusually volatile, recent directional extrem
    eps=1e-12
    r=np.log(df['close']).diff()
    rv=r.rolling(12).std()
    vov=rv.rolling(12).std()
    base=vov.ewm(span=120).mean()
    mom=np.sign(df['close']-df['close'].shift(3))
    hot=vov>(base*1.3)
    sig=pd.Series(np.where(hot,-mom,0.0),index=df.index)
    sig=sig.replace([np.inf,-np.inf],0).fillna(0)
    return sig.round().astype(int).values

def volume_accel_lead(df):
    # Volume often accelerates before price resolves direction. Combine positive volume acceleration (flow building) with the sign of accumulated intrabar body pressure (close-open over a few bars) to antic
    eps=1e-12
    vol=df['volume']
    accel=vol.diff().rolling(3).mean()
    accel_std=vol.diff().rolling(50).std()+eps
    elevated=(vol-vol.rolling(50).mean())/(vol.rolling(50).std()+eps)
    flow=np.sign((df['close']-df['open']).rolling(3).sum())
    trigger=(accel/accel_std>0.5)&(elevated>0.5)
    sig=pd.Series(np.where(trigger,flow,0.0),index=df.index)
    sig=sig.replace([np.inf,-np.inf],0).fillna(0)
    return sig.round().astype(int).values

STRATEGIES = {
    "kyle_lambda_regime": kyle_lambda_regime,
    "variance_ratio_adaptive": variance_ratio_adaptive,
    "realized_skew_reversal": realized_skew_reversal,
    "absorption_continuation": absorption_continuation,
    "vol_of_vol_reversion": vol_of_vol_reversion,
    "volume_accel_lead": volume_accel_lead,
}
