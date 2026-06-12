# AI monitoring engine — setup

The repo includes a serverless GitHub Actions engine that runs **without your PC**:

| Workflow | Schedule | What it does |
|---|---|---|
| `.github/workflows/collect.yml` | every 15 min | Fetches live BTC, updates the forward paper-trading ledger (`data/live_ledger.csv`). Commits only when a trade opens/resolves. |
| `.github/workflows/monitor.yml` | 3×/day | **Claude** reads the results and writes an honest assessment + degradation alert + regime note to `reports/`. |
| `.github/workflows/research.yml` | weekly + manual | **Claude** invents new strategies, the harness scores them against the strict cross-venue bar, and opens a **PR** with the survivors. |

The dashboard's **Paper trading** tab shows the AI assessment, the persisted forward
ledger + equity curve, and the live recompute — all auto-updating.

## One-time setup (after pushing the repo to GitHub)

### 1. Add your Anthropic API key as a repo secret
This is what lets the Actions "be Claude". The `collect` workflow needs no key; the
`monitor` and `research` workflows skip gracefully until you add it.

1. Get a key at <https://console.anthropic.com> → **API Keys**.
2. In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**.
3. Name: `ANTHROPIC_API_KEY` · Value: your key. Save.

### 2. Allow Actions to write + open PRs
**Settings → Actions → General → Workflow permissions**:
- Select **Read and write permissions**.
- Check **Allow GitHub Actions to create and approve pull requests** (needed for the research PR).

### 3. (First run) trigger them manually to test
**Actions** tab → pick a workflow → **Run workflow**. Start with `collect`
(no key needed), then `monitor` (needs the key). Check the run logs.

## Cost (you control it via cadence)

- `collect` — **free** (no AI; GitHub Actions minutes are free on public repos).
- `monitor` — one Claude call per run × 3/day. A small report run is ~10–40k tokens →
  **pennies per run**, roughly a few cents to ~$0.30/day.
- `research` — one larger Claude call/week → **~$0.50–$2 per run**.

To spend less: widen the `cron` schedules (e.g. monitor 1×/day). To spend more for
faster learning: tighten them. Model is `claude-opus-4-8` (set in the `automation/*.py`
files) — switch to `claude-sonnet-4-6` there to cut cost ~40% if you prefer.

## How the data flows (no PC anywhere)

```
GitHub Actions (cron) → fetch live BTC + run composite_score + Claude analysis
        ↓ commits data/live_ledger.csv + data/live_results.json + reports/
GitHub repo → Streamlit Cloud auto-redeploys → dashboard shows it
```

Safety note: `research.py` has Claude write small strategy functions that run **in CI
only** and land in a **PR you review** — nothing auto-merges, and the code is
constrained to `df → signal` with no I/O.
