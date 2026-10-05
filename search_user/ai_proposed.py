"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated 2026-10-05 16:45 UTC. Reviewed via PR before merge. Each fn(df) -> {-1,0,1} signal.
"""
import numpy as np
import pandas as pd


def amihud_regime_flip(df):
    # Per-bar price impact |ret|/volume (Amihud) determines whether short-horizon returns trend or revert: high-impact (illiquid) bars persist, low-impact (absorbed) bars revert. Conditional sign-flip rathe
    eps=1e-9
    ret=df['close'].pct_change()
    illiq=ret.abs()/(df['volume']+eps)
    med=illiq.rolling(120).median()
    hi=illiq>med
    raw=np.where(hi,np.sign(ret),-np.sign(ret))
    sig=pd.Series(raw,index=df.index).shift(1).fillna(0)
    return sig.astype(int).values

def volume_absorption_reversal(df):
    # A bar with large volume but a small body relative to its range signals absorption (one side soaking up flow without moving price); the subsequent bar tends to move against the absorbed push. Distinct 
    eps=1e-9
    body=(df['close']-df['open']).abs()
    rng=(df['high']-df['low'])
    bratio=body/(rng+eps)
    volr=df['volume']/(df['volume'].rolling(50).mean()+eps)
    absorb=(volr>1.6)&(bratio<0.30)
    mom=np.sign(df['close']-df['open'])
    raw=np.where(absorb,-mom,0.0)
    sig=pd.Series(raw,index=df.index).shift(1).fillna(0)
    return sig.astype(int).values

def jump_vs_diffusion_fade(df):
    # Separate jumps from diffusion using a robust rolling median of |ret| (bipower-style). Only outsized single-bar jumps (poor execution, forced flow) are faded; ordinary diffusion is ignored, avoiding th
    eps=1e-9
    ret=df['close'].pct_change()
    diff_vol=ret.abs().rolling(60).median()
    z=ret/(diff_vol+eps)
    raw=np.where(z>4.0,-1.0,np.where(z<-4.0,1.0,0.0))
    sig=pd.Series(raw,index=df.index).shift(1).fillna(0)
    return sig.astype(int).values

def dispersion_gated_momentum(df):
    # Momentum only works when participation is broad; when one bar dominates window volume (high Herfindahl concentration) the move is a single-order artifact and fails. Gate a short momentum by low volume
    eps=1e-9
    v=df['volume']
    w=20
    sumv=v.rolling(w).sum()
    hhi=(v**2).rolling(w).sum()/(sumv**2+eps)
    disp=hhi<hhi.rolling(150).median()
    mom=np.sign(df['close']-df['close'].shift(w))
    raw=np.where(disp,mom,0.0)
    sig=pd.Series(raw,index=df.index).shift(1).fillna(0)
    return sig.astype(int).values

def wick_flow_rejection(df):
    # Wick imbalance (upper minus lower wick) only carries information when confirmed by above-average flow: a large upper wick on real volume = failed push up = next-bar down bias, and vice versa. Flow-con
    eps=1e-9
    body_hi=df[['close','open']].max(axis=1)
    body_lo=df[['close','open']].min(axis=1)
    upper=df['high']-body_hi
    lower=body_lo-df['low']
    rng=(df['high']-df['low'])
    imb=(upper-lower)/(rng+eps)
    volr=df['volume']/(df['volume'].rolling(50).mean()+eps)
    strong=volr>1.3
    raw=np.where(strong&(imb>0.45),-1.0,np.where(strong&(imb<-0.45),1.0,0.0))
    sig=pd.Series(raw,index=df.index).shift(1).fillna(0)
    return sig.astype(int).values

def compression_participation_break(df):
    # A bar whose range is compressed versus recent average but whose volume is elevated and whose close sits at an extreme signals a quiet build-up resolving directionally. Combines three interacting condi
    eps=1e-9
    rng=(df['high']-df['low'])
    rng_avg=rng.rolling(20).mean()
    compress=rng<(0.8*rng_avg)
    vol_up=df['volume']>df['volume'].rolling(20).mean()
    loc=(df['close']-df['low'])/(rng+eps)
    up=compress&vol_up&(loc>0.70)
    dn=compress&vol_up&(loc<0.30)
    raw=np.where(up,1.0,np.where(dn,-1.0,0.0))
    sig=pd.Series(raw,index=df.index).shift(1).fillna(0)
    return sig.astype(int).values

STRATEGIES = {
    "amihud_regime_flip": amihud_regime_flip,
    "volume_absorption_reversal": volume_absorption_reversal,
    "jump_vs_diffusion_fade": jump_vs_diffusion_fade,
    "dispersion_gated_momentum": dispersion_gated_momentum,
    "wick_flow_rejection": wick_flow_rejection,
    "compression_participation_break": compression_participation_break,
}
