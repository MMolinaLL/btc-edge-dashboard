"""
Quantify the core barrier: how accurately can free ASOS data reproduce the
official settlement high, measured against the 1-2F-wide bet buckets?

For each settled day we know the winning bucket [lo,hi]. We compute how far the
observed daily max sits from that bucket (0 if inside, else degrees to the
nearest edge). If that error is routinely >= the bucket width, you literally
cannot resolve which bucket wins -- your ruler is coarser than the bet.
"""
import numpy as np
import pandas as pd
from weather_backtest import parse_datecode

mkt = pd.read_parquet("data/kalshi_kxhighny_60m.parquet")
mkt = mkt.dropna(subset=["result"]).copy()
mkt["mdate"] = mkt["date"].map(parse_datecode)


def bucket_error(mx, lo, hi, kind):
    if kind == "above":
        return 0.0 if mx >= lo else lo - mx
    if kind == "below":
        return 0.0 if mx <= hi else mx - hi
    if lo - 0.5 <= mx <= hi + 0.5:
        return 0.0
    return (lo - 0.5 - mx) if mx < lo else (mx - hi - 0.5)


def assess(obs_path, label):
    obs = pd.read_parquet(obs_path)
    obs["valid"] = pd.to_datetime(obs["valid"])
    obs["d"] = obs["valid"].dt.date
    errs = []
    for d, g in mkt.groupby("mdate"):
        yes = g[g["result"] == "yes"]
        od = obs[obs["d"] == d]
        if yes.empty or od.empty:
            continue
        yb = yes.iloc[0]
        mx = od["tmpf"].max()
        errs.append(bucket_error(mx, yb["lo"], yb["hi"], yb["kind"]))
    errs = np.array(errs)
    print(f"\n{label}  (n={len(errs)} days)")
    print(f"  exact bucket hit:   {(errs == 0).mean()*100:5.1f}%")
    print(f"  within 1F of bucket:{(errs <= 1).mean()*100:5.1f}%")
    print(f"  within 2F of bucket:{(errs <= 2).mean()*100:5.1f}%")
    print(f"  mean miss (deg F):  {errs.mean():5.2f}")
    print(f"  worst miss (deg F): {errs.max():5.1f}")
    return errs


print("How well does free ASOS data reproduce the official settlement bucket?")
print("Bet buckets are only 1-2F wide, so even a ~1.5F error crosses bucket lines.")
assess("data/obs_nyc.parquet", "Hourly METAR")
assess("data/obs_nyc_1min.parquet", "1-minute ASOS")
print("\nBottom line: if you cannot place the official high inside its own 1-2F")
print("bucket on a large fraction of days, you cannot price these buckets better")
print("than the market -- the bet is finer than your measurement.")
