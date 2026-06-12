"""
automation/ai_monitor.py — Claude reads the live results and writes an honest
assessment + degradation alert + regime note (runs in GitHub Actions on a slow
cadence to keep cost trivial).

Outputs (committed by the workflow, shown in the dashboard):
  reports/latest.md      human-readable assessment
  reports/state.json     machine state (alert level, headline) + continuity
  reports/history.jsonl  append-only log of every run

Uses the official Anthropic SDK, model claude-opus-4-8, adaptive thinking, and a
structured JSON output schema. Needs ANTHROPIC_API_KEY in the environment.
Run with --dry-run to build the prompt and skip the API call (no key needed).
"""
import argparse
import json
import os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(BASE, "data", "live_results.json")
SEARCH = os.path.join(BASE, "data", "search_results.json")
REPORTS = os.path.join(BASE, "reports")
STATE = os.path.join(REPORTS, "state.json")
HISTORY = os.path.join(REPORTS, "history.jsonl")
LATEST = os.path.join(REPORTS, "latest.md")

MODEL = "claude-opus-4-8"

SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string", "description": "one-line status, <=120 chars"},
        "alert_level": {"type": "string", "enum": ["none", "watch", "alert"]},
        "alert_message": {"type": "string", "description": "short; empty if level=none"},
        "regime_note": {"type": "string", "description": "1-2 sentences on market regime"},
        "assessment_md": {"type": "string", "description": "markdown, ~150-300 words"},
    },
    "required": ["headline", "alert_level", "alert_message", "regime_note", "assessment_md"],
    "additionalProperties": False,
}

PROMPT = """You are an honest, calibrated quantitative monitor for an automated BTC \
trading research project. Your job is to assess whether the strategy's edge is \
holding on live, out-of-sample data — and to flag degradation early WITHOUT crying \
wolf on small-sample noise.

## What you're monitoring
Strategy `composite_score`: a selective mean-reversion signal (fade extreme \
RSI+Stochastic+Bollinger agreement on large moves). Validated facts you must respect:
- It is the BEST candidate found, but its gross edge is only ~4 bps/bet, and the \
  breakeven trading cost is ~3.9 bps — i.e. it is marginal and likely NOT \
  net-profitable after realistic costs. Do not hype it.
- It is selective: only ~1-2% of candles trade, so the live sample grows slowly. \
  A few dozen trades is NOT enough to conclude anything. Say so when sample is tiny.
- Honest framing is the point. If the data is too thin to judge, say it's too thin.

## Decision guide for alert_level
- "none": edge roughly as expected, or sample too small to judge.
- "watch": early signs of degradation (rolling net clearly negative over a \
  non-trivial sample), or an unusual regime worth noting.
- "alert": sustained, clear breakdown over a meaningful sample (e.g. dozens of \
  trades net materially negative beyond cost), warranting pausing the strategy.

## Live data (JSON)
{results}

## Prior assessment (for continuity; may be empty)
{prior}

Write `assessment_md` for a non-expert: how it's doing, what changed vs last time, \
what the numbers do and don't tell us, and the honest bottom line. Be specific with \
numbers. Never imply guaranteed profit."""


def load(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def build_prompt():
    results = load(RESULTS, {})
    search = load(SEARCH, {})
    if search:
        results = {**results, "edge_search_survivors": search.get("n_survivors"),
                   "edge_search_bar": search.get("bar")}
    prior = load(STATE, {})
    return PROMPT.format(results=json.dumps(results, indent=2),
                         prior=json.dumps({k: prior.get(k) for k in
                                           ("headline", "alert_level", "regime_note")}, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    os.makedirs(REPORTS, exist_ok=True)
    prompt = build_prompt()

    if args.dry_run:
        print("=== DRY RUN — prompt that would be sent ===\n")
        print(prompt[:4000])
        print("\n=== (no API call made) ===")
        return

    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": prompt}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    data = json.loads(text)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with open(LATEST, "w", encoding="utf-8") as f:
        badge = {"none": "🟢", "watch": "🟡", "alert": "🔴"}[data["alert_level"]]
        f.write(f"# {badge} {data['headline']}\n\n_Updated {now} · model {MODEL}_\n\n")
        if data["alert_level"] != "none" and data["alert_message"]:
            f.write(f"> **{data['alert_level'].upper()}:** {data['alert_message']}\n\n")
        f.write(f"**Regime:** {data['regime_note']}\n\n")
        f.write(data["assessment_md"] + "\n")

    state = {"updated": now, "model": MODEL, **data}
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now, "headline": data["headline"],
                            "alert_level": data["alert_level"]}) + "\n")

    print(f"{data['alert_level'].upper()}: {data['headline']}")
    print(f"  tokens in/out: {resp.usage.input_tokens}/{resp.usage.output_tokens}")


if __name__ == "__main__":
    main()
