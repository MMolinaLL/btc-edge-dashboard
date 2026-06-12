"""
Fetch 1-minute ASOS temperature from the IEM 1-minute archive (free, no auth).

Hourly METARs miss the true daily peak (it happens between :51 obs), biasing our
running-max ~1F low. The 1-minute product captures the continuous trace, which
should track the official NWS Climate Report high far better.

Usage:
    python fetch_obs_1min.py --station NYC --start 2026-04-10 --end 2026-06-12
    python fetch_obs_1min.py --station NYC --start 2026-04-12 --end 2026-04-15 --test
"""
import argparse
import io
import os

import pandas as pd
import requests

URL = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos1min.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--station", default="NYC")
    ap.add_argument("--tz", default="America/New_York")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--test", action="store_true", help="print head & stop, no save")
    args = ap.parse_args()

    y1, m1, d1 = args.start.split("-")
    y2, m2, d2 = args.end.split("-")
    params = {
        "station": args.station,
        "vars": "tmpf",
        "sample": "1min",
        "what": "download",
        "delim": "comma",
        "gis": "no",
        "tz": args.tz,
        "year1": y1, "month1": m1, "day1": d1,
        "year2": y2, "month2": m2, "day2": d2,
    }
    print(f"Requesting 1-min tmpf for {args.station} {args.start}..{args.end} ...")
    r = requests.get(URL, params=params, timeout=300)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    print(f"  columns: {list(df.columns)}")
    print(f"  rows: {len(df):,}")
    if args.test:
        print(df.head(8).to_string())
        return

    # normalize: find the time column and temp column
    tcol = next((c for c in df.columns if c.lower().startswith("valid")), df.columns[1])
    tmp = "tmpf" if "tmpf" in df.columns else \
        next(c for c in df.columns if "tmpf" in c.lower())
    df = df.rename(columns={tcol: "valid", tmp: "tmpf"})
    df["tmpf"] = pd.to_numeric(df["tmpf"], errors="coerce")
    df = df.dropna(subset=["tmpf"])
    df["valid"] = pd.to_datetime(df["valid"])
    df = df[["station", "valid", "tmpf"]].sort_values("valid").reset_index(drop=True)
    df["date"] = df["valid"].dt.date

    out = args.out or f"data/obs_{args.station.lower()}_1min.parquet"
    os.makedirs("data", exist_ok=True)
    df.to_parquet(out)
    daily = df.groupby("date")["tmpf"].max()
    print(f"Saved {len(df):,} 1-min obs across {df['date'].nunique()} days")
    print(f"  daily-high range: {daily.min():.0f}F .. {daily.max():.0f}F, "
          f"mean {daily.mean():.1f}F\n  -> {out}")


if __name__ == "__main__":
    main()
