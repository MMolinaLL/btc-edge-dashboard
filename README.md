# btc-bot — an honest edge-hunting harness + dashboard

A backtest-first research project for automated trading/betting, with a live web
dashboard. The goal was a high-win-rate bot placing many small bets. The **real**
deliverable is a disciplined harness that tells you the truth about a strategy
*before* you risk money — plus an automated edge search and a forward
paper-trading loop so we learn from reality, not from a curve-fit.

## Run the dashboard

```bash
pip install -r requirements.txt
streamlit run app.py        # opens http://localhost:8501
```

To host it **always-on at a public URL** (free, no PC required — the cloud fetches
live BTC data itself), see [`DEPLOY.md`](DEPLOY.md) (Streamlit Community Cloud).
The *Paper trading* tab recomputes `composite_score` from live data on every
refresh; the other tabs render the bundled historical data.

Five tabs: **Overview** (data inventory + findings), **BTC strategies** (live
leaderboard, cost slider, price + equity charts with a train/test split),
**Weather markets** (bucket-price convergence vs. the running-high temperature),
**Edge search** (the automated hunt leaderboard), **Paper trading** (forward,
out-of-sample ledger + equity curve).

## TL;DR findings

| Thread | Verdict | Why |
|---|---|---|
| BTC 5-min up/down (momentum / mean-reversion / RSI) | not viable | **Cost barrier.** The ~3% mean-reversion "edge" is bid-ask bounce: it collapses 54%→51% from Binance.US to deep-book Coinbase, and the gross edge is 30–200× smaller than fees. |
| Kalshi weather intraday-convergence | not viable on free data | **Data-resolution barrier.** 1–2°F buckets are finer than the ±1.5°F daily-high we can reconstruct from free ASOS data (wrong bucket 28–37% of days). |
| **Automated edge search (86 strategies, 8 novel families)** | **best candidate: `composite_score`** | A *clean, no-look-ahead, cross-venue* selective mean-reversion signal worth **~4 bps gross/bet** — real (survives on the deep book, unlike bounce) but still **below realistic ~10–40 bps retail costs**, so not net-profitable yet. |

The search also surfaced genuine sub-1-bp signals (volume-imbalance reversion,
vol-regime) that are real but far below cost. Net: there *is* faint structure in
5m BTC; capturing it is a **cost** problem, not a signal problem.

## What's here

| File | Purpose |
|---|---|
| `app.py` | Streamlit + Plotly dashboard over everything below. |
| `eval_engine.py` | Honest scoring core: train/test split, exact per-bet cost, equity curves, controls. Hosts the promoted `composite_score`. |
| `fetch_data.py` | BTC candles (Binance.US / Coinbase). Binance global is geo-blocked (451) in the US. |
| `backtest.py` / `pressure_test.py` | BTC up/down engine + the cross-venue bps cost analysis. |
| `fetch_kalshi_weather.py` | Settled Kalshi temp markets + hourly price candlesticks (public API, no auth). |
| `fetch_obs.py` / `fetch_obs_1min.py` | Central Park temps from IEM ASOS (hourly / 1-minute). |
| `weather_backtest.py` / `diag_*.py` | Weather convergence model + calibration/resolution diagnostics. |
| `search_runner.py` | Strict cross-venue evaluator. A strategy "survives" only if net-positive OOS on **both** venues. Agent-facing `--user` interface. |
| `search_user/*.py` | Strategy families invented by the edge-search workflow. |
| `build_search_results.py` | Authoritatively re-evaluates every strategy (no trust in self-reports) + look-ahead smell test → `data/search_results.json`. |
| `paper_trader.py` | Forward, out-of-sample paper-trading ledger, net of cost. Run on a 5-min schedule for live forward testing. |

## The honesty machinery (why the numbers are trustworthy)

- **Controls that must fail.** Coinflip lands at 50.0%; a no-info bettor places 0
  +EV bets. If these misbehave, the harness is lying.
- **Cross-venue bar.** Any edge must survive on *both* the thin (Binance.US) and
  deep (Coinbase) book. This is what kills bid-ask-bounce mirages — and it killed
  every naive technical signal.
- **Train/test split + no look-ahead** on every strategy; survivors get an
  adversarial code audit for data leakage.
- **Authoritative re-evaluation.** The search-result leaderboard is computed by
  `build_search_results.py`, not copied from what agents claimed.

## Forward testing — learn as we go

```bash
python paper_trader.py --replay-days 3 --strategy composite_score   # seed
python paper_trader.py                                              # one live tick
```

A Windows scheduled task **`BTC-PaperTrader`** is registered to run the live tick
every 5 minutes (via `pythonw`, no popup) using live Binance.US data. It only
fires while the PC is on and awake; gaps are harmless (pending trades still
resolve on the next run). Each run appends a heartbeat to `data/paper_runs.log`.

```powershell
Get-ScheduledTaskInfo -TaskName BTC-PaperTrader      # status / last + next run
Disable-ScheduledTask  -TaskName BTC-PaperTrader      # pause
Enable-ScheduledTask   -TaskName BTC-PaperTrader      # resume
Unregister-ScheduledTask -TaskName BTC-PaperTrader -Confirm:$false   # remove
```

Forward testing accumulates slowly — `composite_score` is selective (~1–2% of
candles), so expect only a few new trades per day. Give it a few hundred forward
trades before trusting the result. This is the only way to know whether the
in-sample edge is real on data the model has never seen.

## Honest bottom line

We found real but faint structure in 5m BTC. The frontier to "profitable" is
**driving transaction cost below ~4 bps** (maker rebates, fee tiers, a near-zero-fee
venue), not finding more signal. Durable retail edges live in providing liquidity
or in genuinely less-efficient niches — not in predicting BTC direction. The win
is having the tool that tells you the truth.
