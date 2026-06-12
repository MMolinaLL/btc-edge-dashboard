"""
search_runner.py — the honest evaluator for the edge search.

A strategy "survives" only if its out-of-sample (TEST) net edge is positive on
BOTH venues at the given cost:
  - Binance.US (thinner book)  AND  Coinbase (deep book)
Requiring both kills bid-ask-bounce mirages, which inflate on thin books and
vanish on deep ones. We also require the in-sample (TRAIN) net to agree in sign,
so we are not just curve-fitting the test window.

Two entry points:
  1. Built-in grid sweep:
       python search_runner.py --sweep --cost-bps 2
  2. Evaluate a user strategy file exposing a STRATEGIES dict {name: df->signal}:
       python search_runner.py --user search_user/myidea.py --cost-bps 2
     (prints JSON — this is what the workflow agents call.)
"""
import argparse
import importlib.util
import json
import os

import numpy as np
import pandas as pd

import eval_engine as ee

BASE = os.path.dirname(os.path.abspath(__file__))
VENUES = {"binanceus": os.path.join(BASE, "data", "btc_5m.parquet"),
          "coinbase": os.path.join(BASE, "data", "btc_5m_coinbase.parquet")}
_CACHE = {}


def venue_df(v):
    if v not in _CACHE:
        _CACHE[v] = pd.read_parquet(VENUES[v])
    return _CACHE[v]


def evaluate_fn(fn, cost_bps):
    """Evaluate one strategy across both venues. Returns a result dict."""
    out = {}
    for v in VENUES:
        df = venue_df(v)
        res = ee.evaluate_spot(df, np.asarray(fn(df)), cost_bps)
        out[v] = {
            "win_test": round(res["test"]["win"], 4),
            "net_bps_test": round(res["test"]["net_bps"], 3),
            "net_bps_train": round(res["train"]["net_bps"], 3),
            "gross_bps_test": round(res["test"]["gross_bps"], 3),
            "bets_test": res["test"]["bets"],
        }
    b, c = out["binanceus"], out["coinbase"]
    survives = (b["net_bps_test"] > 0 and c["net_bps_test"] > 0
                and b["net_bps_train"] > 0 and c["net_bps_train"] > 0
                and b["bets_test"] >= 200 and c["bets_test"] >= 200)
    out["survives"] = bool(survives)
    out["min_net_test"] = round(min(b["net_bps_test"], c["net_bps_test"]), 3)
    return out


# --------------------------- built-in strategy space ----------------------
def _ret(df):
    return df["close"].diff()


def make_space():
    sp = {}
    for k in (1, 2, 3, 6, 12, 24, 48):
        sp[f"momentum_{k}"] = (lambda k: lambda df:
                               np.sign(df["close"] - df["close"].shift(k)).fillna(0).astype(int).values)(k)
        sp[f"meanrev_{k}"] = (lambda k: lambda df:
                              (-np.sign(df["close"] - df["close"].shift(k))).fillna(0).astype(int).values)(k)
    for span in (12, 24, 48, 96):
        sp[f"ema_{span}"] = (lambda s: lambda df:
                             np.where(df["close"] > df["close"].ewm(span=s, adjust=False).mean(), 1, -1))(span)
    for span in (12, 24, 48):
        sp[f"breakout_{span}"] = (lambda s: lambda df: _breakout(df, s))(span)
    for span in (12, 24, 48):
        for mult in (1.0, 1.5, 2.0):
            sp[f"mrvf_{span}_{mult}"] = (lambda s, m: lambda df: _mrvf(df, s, m))(span, mult)
    for span in (20, 40):
        for z in (1.0, 1.5, 2.0):
            sp[f"boll_{span}_{z}"] = (lambda s, zz: lambda df: _boll(df, s, zz))(span, z)
    for k in (2, 3, 4):
        sp[f"streak_rev_{k}"] = (lambda kk: lambda df: _streak(df, kk))(k)
    sp["time_of_day"] = ee.s_time_of_day
    return sp


def _breakout(df, span):
    hi = df["high"].rolling(span).max().shift(1)
    lo = df["low"].rolling(span).min().shift(1)
    s = np.zeros(len(df), dtype=int)
    s[df["close"].values > hi.values] = 1
    s[df["close"].values < lo.values] = -1
    return s


def _mrvf(df, span, mult):
    r = _ret(df)
    vol = r.rolling(span).std()
    big = r.abs() > mult * vol
    return np.where(big, -np.sign(r).fillna(0), 0).astype(int)


def _boll(df, span, z):
    ma = df["close"].rolling(span).mean()
    sd = df["close"].rolling(span).std()
    upper = df["close"] > ma + z * sd
    lower = df["close"] < ma - z * sd
    s = np.zeros(len(df), dtype=int)
    s[upper.values] = -1   # revert from upper band
    s[lower.values] = 1
    return s


def _streak(df, k):
    d = np.sign(_ret(df)).fillna(0).values
    s = np.zeros(len(df), dtype=int)
    for i in range(k, len(df)):
        if all(d[i - j] == 1 for j in range(k)):
            s[i] = -1
        elif all(d[i - j] == -1 for j in range(k)):
            s[i] = 1
    return s


def load_user(path):
    spec = importlib.util.spec_from_file_location("user_strat", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.STRATEGIES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--user", default=None)
    ap.add_argument("--cost-bps", type=float, default=2.0)
    args = ap.parse_args()

    strategies = make_space() if args.sweep else load_user(args.user)
    results = []
    for name, fn in strategies.items():
        try:
            r = evaluate_fn(fn, args.cost_bps)
            r["strategy"] = name
            results.append(r)
        except Exception as e:
            results.append({"strategy": name, "error": str(e)})

    results.sort(key=lambda r: r.get("min_net_test", -1e9), reverse=True)
    if args.sweep:
        os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
        with open(os.path.join(BASE, "data", "sweep.json"), "w") as f:
            json.dump({"cost_bps": args.cost_bps, "results": results}, f, indent=2)
        print(f"Swept {len(results)} strategies at cost {args.cost_bps} bps. "
              f"Survivors (net>0 OOS on BOTH venues): "
              f"{sum(1 for r in results if r.get('survives'))}\n")
        print(f"{'strategy':<16}{'BUS net':>9}{'CB net':>9}{'min':>8}  survives")
        for r in results[:18]:
            if "error" in r:
                continue
            print(f"{r['strategy']:<16}{r['binanceus']['net_bps_test']:>9.2f}"
                  f"{r['coinbase']['net_bps_test']:>9.2f}{r['min_net_test']:>8.2f}"
                  f"  {'YES' if r['survives'] else ''}")
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
