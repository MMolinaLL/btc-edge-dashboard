"""
Fetch historical hourly temperature observations from the Iowa Environmental
Mesonet (IEM) ASOS archive -- free, no auth.

Central Park (the NYC high-temp settlement station) is IEM id 'NYC' on the
NY_ASOS network. We pull air temperature (tmpf) in local time, which lets the
backtest compute the running daily high at any moment of the trading day.

Usage:
    python fetch_obs.py --station NYC --tz America/New_York \
        --start 2026-04-01 --end 2026-06-12
"""
import argparse
import io
import os

import pandas as pd
import requests

URL = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--station", default="NYC")
    ap.add_argument("--tz", default="America/New_York")
    ap.add_argument("--start", required=True)  # YYYY-MM-DD
    ap.add_argument("--end", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    y1, m1, d1 = args.start.split("-")
    y2, m2, d2 = args.end.split("-")
    params = {
        "station": args.station, "data": "tmpf", "tz": args.tz,
        "year1": y1, "month1": m1, "day1": d1,
        "year2": y2, "month2": m2, "day2": d2,
        "format": "onlycomma", "latlon": "no", "missing": "M", "trace": "T",
    }
    print(f"Requesting ASOS tmpf for {args.station} "
          f"{args.start}..{args.end} ({args.tz}) ...")
    r = requests.get(URL, params=params, timeout=120)
    r.raise_for_status()

    df = pd.read_csv(io.StringIO(r.text))
    # columns: station, valid (local time string), tmpf
    df = df[df["tmpf"] != "M"].copy()
    df["tmpf"] = pd.to_numeric(df["tmpf"], errors="coerce")
    df = df.dropna(subset=["tmpf"])
    df["valid"] = pd.to_datetime(df["valid"])  # local naive time
    df = df[["station", "valid", "tmpf"]].sort_values("valid").reset_index(drop=True)
    df["date"] = df["valid"].dt.date

    out = args.out or f"data/obs_{args.station.lower()}.parquet"
    os.makedirs("data", exist_ok=True)
    df.to_parquet(out)

    # quick daily-high summary as a sanity check
    daily = df.groupby("date")["tmpf"].max()
    print(f"Saved {len(df):,} obs across {df['date'].nunique()} days "
          f"({df['valid'].min()} .. {df['valid'].max()})")
    print(f"  daily-high range: {daily.min():.0f}F .. {daily.max():.0f}F, "
          f"mean {daily.mean():.1f}F")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
