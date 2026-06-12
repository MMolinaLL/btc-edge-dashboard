"""
build_search_results.py — authoritative aggregation for the Edge search tab.

Does NOT trust agent-reported numbers. Independently re-evaluates every strategy
(built-in grid + every search_user/*.py the workflow produced) through the same
honest cross-venue evaluator, at both an optimistic (2 bps) and realistic (5 bps)
cost, and runs a crude look-ahead smell test on each file. Writes
data/search_results.json for the dashboard.

Run after the edge-search workflow completes:
    python build_search_results.py
"""
import glob
import json
import os
import re
from datetime import datetime, timezone

import search_runner as sr

BASE = sr.BASE
USER_DIR = os.path.join(BASE, "search_user")
OUT = os.path.join(BASE, "data", "search_results.json")

# crude look-ahead patterns: negative shift, or whole-series reducers without rolling
LOOKAHEAD_PAT = re.compile(r"\.shift\(\s*-")
WHOLE_SERIES_PAT = re.compile(r'(?<!rolling\()(?<!expanding\()df\[[^\]]+\]\.(max|min|mean|quantile)\(')


def _strip_comments_and_strings(txt):
    """Remove triple-quoted blocks and # comments so we scan CODE only.
    (The template's docstring literally says 'do not use .shift(-1)', which
    would otherwise be a false positive.)"""
    txt = re.sub(r'"""[\s\S]*?"""', "", txt)
    txt = re.sub(r"'''[\s\S]*?'''", "", txt)
    txt = re.sub(r"#.*", "", txt)
    return txt


def smell_lookahead(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return False, ""
    code = _strip_comments_and_strings(txt)
    flags = []
    if LOOKAHEAD_PAT.search(code):
        flags.append("negative-shift")
    if WHOLE_SERIES_PAT.search(code):
        flags.append("whole-series-reducer")
    return (len(flags) > 0), ",".join(flags)


def eval_dict(fn, family, name, file=""):
    row = {"strategy": name, "family": family, "file": os.path.basename(file)}
    try:
        r2 = sr.evaluate_fn(fn, 2.0)
        r5 = sr.evaluate_fn(fn, 5.0)
        row.update({
            "bus_net_2bps": r2["binanceus"]["net_bps_test"],
            "cb_net_2bps": r2["coinbase"]["net_bps_test"],
            "min_net_2bps": r2["min_net_test"],
            "min_net_5bps": r5["min_net_test"],
            "win_test_bus": r2["binanceus"]["win_test"],
            "bets_test_bus": r2["binanceus"]["bets_test"],
            "survives_2bps": r2["survives"],
            "survives_5bps": r5["survives"],
        })
    except Exception as e:
        row["error"] = str(e)[:160]
    return row


def main():
    results = []

    # 1) built-in grid
    for name, fn in sr.make_space().items():
        results.append(eval_dict(fn, "builtin_grid", name))

    # 2) every agent-produced strategy file
    files = sorted(f for f in glob.glob(os.path.join(USER_DIR, "*.py"))
                   if not os.path.basename(f).startswith("_"))
    for path in files:
        family = os.path.splitext(os.path.basename(path))[0]
        la_flag, la_kind = smell_lookahead(path)
        try:
            strategies = sr.load_user(path)
        except Exception as e:
            results.append({"strategy": f"<{family} failed to import>",
                            "family": family, "error": str(e)[:160]})
            continue
        for name, fn in strategies.items():
            row = eval_dict(fn, family, name, path)
            row["lookahead_flag"] = la_flag
            if la_flag:
                row["lookahead_kind"] = la_kind
            results.append(row)

    # sort by realistic-cost out-of-sample edge, worst-case venue
    results.sort(key=lambda r: r.get("min_net_5bps", -1e9), reverse=True)

    # a strategy only "survives" honestly if it clears BOTH venues at 5 bps AND
    # has no look-ahead smell
    for r in results:
        r["survives"] = bool(r.get("survives_5bps") and not r.get("lookahead_flag"))

    survivors = [r for r in results if r["survives"]]
    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "n_tested": len(results),
        "n_survivors": len(survivors),
        "bar": "net_bps_test > 0 on BOTH venues at 5 bps cost, no look-ahead",
        "results": results,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Aggregated {len(results)} strategies -> {OUT}")
    print(f"Survivors (net>0 OOS both venues @5bps, no look-ahead): {len(survivors)}")
    print(f"\nTop 12 by worst-venue net @5bps:")
    print(f"{'strategy':<22}{'family':<18}{'min@2':>8}{'min@5':>8}  surv  flag")
    for r in results[:12]:
        if "error" in r:
            continue
        print(f"{r['strategy']:<22}{r['family']:<18}"
              f"{r.get('min_net_2bps', float('nan')):>8.2f}"
              f"{r.get('min_net_5bps', float('nan')):>8.2f}"
              f"  {'YES' if r['survives'] else '   '}  "
              f"{'LOOKAHEAD' if r.get('lookahead_flag') else ''}")


if __name__ == "__main__":
    main()
