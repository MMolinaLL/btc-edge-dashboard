"""
automation/research.py — Claude proposes new candidate strategies, the existing
harness scores them against the strict cross-venue bar, and the workflow opens a
PR with the survivors (runs weekly / on-demand in GitHub Actions).

Claude returns small df->signal Python functions (constrained: no imports beyond
numpy/pandas, no I/O, no look-ahead). We write them to search_user/ai_proposed.py,
then run build_search_results.py to evaluate EVERYTHING authoritatively. The
workflow diffs the result and opens a PR for human review — nothing auto-merges.

Needs ANTHROPIC_API_KEY. Run with --dry-run to skip the API call.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(BASE, "search_user", "ai_proposed.py")
REPORT = os.path.join(BASE, "reports", "research_latest.md")
MODEL = "claude-opus-4-8"

SCHEMA = {
    "type": "object",
    "properties": {
        "rationale": {"type": "string", "description": "what angle you're exploring and why"},
        "strategies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "snake_case identifier"},
                    "idea": {"type": "string"},
                    "code": {"type": "string", "description":
                             "a Python function body for `def NAME(df):` returning a "
                             "numpy int array in {-1,0,1} aligned to df.index. Use only "
                             "df['open'/'high'/'low'/'close'/'volume'], numpy as np, "
                             "pandas as pd. NO look-ahead (no .shift(-k), no whole-series "
                             "max/mean). Indentation: the body only, 4 spaces."},
                },
                "required": ["name", "idea", "code"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["rationale", "strategies"],
    "additionalProperties": False,
}

PROMPT = """You are a quantitative researcher hunting for a REAL, capturable edge in \
BTC 5-minute up/down prediction, for a project that has already rigorously rejected \
the obvious ideas. Propose 4-6 NOVEL candidate strategies as small functions.

## What's already been tried and FAILED the bar (don't just repeat these)
- Plain momentum / mean-reversion / EMA / RSI / Bollinger / breakout / streak.
- Volume z-score, volume-imbalance, OBV, vol-weighted momentum.
- Volatility-regime switching, multi-timeframe trend, session/time-of-day, candle \
  shape, lagged autocorrelation, oscillator-agreement composites.
Every one either lost out-of-sample or was a thin-book bid-ask-bounce artifact that \
died on the deep (Coinbase) order book. The best survivor nets only ~4 bps gross.

## The bar your ideas will be scored against (be honest with yourself)
Each strategy must be net-positive OUT-OF-SAMPLE on BOTH Binance.US AND Coinbase, \
at realistic cost. Bid-ask-bounce mirages are auto-rejected by the cross-venue test. \
It is FINE if your ideas don't clear the bar — propose genuinely new angles (feature \
interactions, conditional combinations, novel signals) rather than relabeled classics.

## Hard rules for `code`
- It is the body of `def NAME(df):`. Return `sig` as a numpy int array in {-1,0,1}.
- df columns: open, high, low, close, volume (UTC index). numpy as np, pandas as pd \
  are already imported. No other imports, no file/network I/O.
- NO LOOK-AHEAD: only use data through each row. Never `.shift(-k)`, never a \
  whole-series `.max()/.mean()/.quantile()`. Use rolling/ewm/expanding and `.shift(+k)`.
- Keep each function short and self-contained.

Return your rationale and the strategy list."""

HEADER = '''"""
ai_proposed.py — strategies proposed by the automated research loop (Claude).
Generated {now}. Reviewed via PR before merge. Each fn(df) -> {{-1,0,1}} signal.
"""
import numpy as np
import pandas as pd


'''


def build_file(strategies):
    parts = [HEADER.format(now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))]
    names = []
    for s in strategies:
        name = "".join(c if (c.isalnum() or c == "_") else "_" for c in s["name"])[:40]
        body = s["code"].rstrip("\n")
        if "return" not in body:
            continue
        parts.append(f"def {name}(df):\n    # {s['idea'][:200]}\n{body}\n\n")
        names.append(name)
    parts.append("STRATEGIES = {\n" +
                 "".join(f'    "{n}": {n},\n' for n in names) + "}\n")
    return "".join(parts), names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    os.makedirs(os.path.join(BASE, "reports"), exist_ok=True)

    if args.dry_run:
        print("=== DRY RUN — research prompt ===\n")
        print(PROMPT[:3500])
        return

    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL, max_tokens=16000, thinking={"type": "adaptive"},
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": PROMPT}],
    )
    data = json.loads(next(b.text for b in resp.content if b.type == "text"))
    code, names = build_file(data["strategies"])
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(code)

    # authoritative evaluation of EVERYTHING (incl. the new proposals)
    proc = subprocess.run([sys.executable, os.path.join(BASE, "build_search_results.py")],
                          capture_output=True, text=True, cwd=BASE)
    print(proc.stdout[-2000:])

    sr = json.load(open(os.path.join(BASE, "data", "search_results.json")))
    proposed = [r for r in sr["results"] if r.get("file") == "ai_proposed.py"]
    survivors = [r for r in proposed if r.get("survives")]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(f"# Automated research run — {now}\n\n")
        f.write(f"**Rationale:** {data['rationale']}\n\n")
        f.write(f"Proposed {len(proposed)} strategies; **{len(survivors)} cleared the "
                f"strict cross-venue bar.**\n\n| strategy | min net @5bps | survives |\n"
                f"|---|---|---|\n")
        for r in sorted(proposed, key=lambda x: x.get("min_net_5bps", -1e9), reverse=True):
            f.write(f"| {r['strategy']} | {r.get('min_net_5bps','?')} | "
                    f"{'✅' if r.get('survives') else ''} |\n")
    print(f"Proposed {len(proposed)}, survivors {len(survivors)}. Report -> {REPORT}")


if __name__ == "__main__":
    main()
