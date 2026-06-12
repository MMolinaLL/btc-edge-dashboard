"""
Diagnose WHY the convergence model is miscalibrated. Two checks:

1. Settlement mismatch: does the ASOS hourly daily-max land in the SAME bucket
   that Kalshi actually settled 'yes'? If not, our "I can see the temperature"
   certainty is built on the wrong number (NWS Climate Report != raw ASOS max).

2. Calibration: bin the model's probability and compare to the actual hit rate.
   A trustworthy model is on the diagonal (P=0.8 wins ~80% of the time).
"""
import numpy as np
import pandas as pd
from weather_backtest import (parse_datecode, in_bucket, build_residual_climatology,
                              rmax_at, model_prob)

import sys
obs_path = sys.argv[1] if len(sys.argv) > 1 else "data/obs_nyc.parquet"
print(f"(using obs: {obs_path})\n")
mkt = pd.read_parquet("data/kalshi_kxhighny_60m.parquet")
mkt = mkt.dropna(subset=["result"]).copy()
mkt["mdate"] = mkt["date"].map(parse_datecode)
obs = pd.read_parquet(obs_path)
obs["local"] = pd.to_datetime(obs["valid"]); obs["d"] = obs["local"].dt.date
obs["h"] = obs["local"].dt.hour

# ---- check 1: ASOS daily-max bucket vs the bucket Kalshi settled yes ----
print("Check 1: does the ASOS daily high land in the bucket that settled YES?\n")
rows = []
for d, g in mkt.groupby("mdate"):
    yes = g[g["result"] == "yes"]
    if yes.empty:
        continue
    yb = yes.iloc[0]
    od = obs[obs["d"] == d]
    if od.empty:
        continue
    asos_max = od["tmpf"].max()
    hit = in_bucket(asos_max, yb["lo"], yb["hi"], yb["kind"])
    rows.append((d, asos_max, yb["lo"], yb["hi"], yb["kind"], hit))
ck = pd.DataFrame(rows, columns=["date", "asos_max", "lo", "hi", "kind", "in_yes_bucket"])
agree = ck["in_yes_bucket"].mean()
print(f"  Days checked: {len(ck)}")
print(f"  ASOS max falls in the settled-yes bucket: {agree*100:.1f}% of days")
print(f"  -> {100-agree*100:.1f}% of days, raw ASOS disagrees with official settlement\n")
print("  Sample disagreements:")
for _, r in ck[~ck["in_yes_bucket"]].head(8).iterrows():
    print(f"    {r['date']}  ASOS max={r['asos_max']:.1f}F  "
          f"yes bucket=[{r['lo']}, {r['hi']}] ({r['kind']})")

# ---- check 2: model calibration ----
print("\nCheck 2: model probability vs. realized hit rate (calibration)\n")
hours = [10, 12, 13, 14, 15, 16, 17, 18]
resid = build_residual_climatology(obs, None, hours)
recs = []
for d, g in mkt.groupby("mdate"):
    od = obs[obs["d"] == d]
    if od.empty:
        continue
    for h in hours:
        if h not in resid:
            continue
        rmax = rmax_at(od, h)
        if rmax is None:
            continue
        for _, row in g.iterrows():
            p = model_prob(rmax, resid[h], row["lo"], row["hi"], row["kind"])
            won = 1.0 if row["result"] == "yes" else 0.0
            recs.append((p, won))
cal = pd.DataFrame(recs, columns=["p", "won"])
cal["bin"] = (cal["p"] * 10).clip(0, 9).astype(int)
print(f"  {'model P':>10}  {'n':>6}  {'actual win%':>12}")
for b, gg in cal.groupby("bin"):
    print(f"   {b/10:.1f}-{b/10+0.1:.1f}   {len(gg):>6}   {gg['won'].mean()*100:>10.1f}%")
print(f"\n  Overall: model mean P={cal['p'].mean():.3f}, actual win rate={cal['won'].mean():.3f}")
print("  (If the model were honest these would track; a big gap = overconfidence.)")
