# 🟢 Too thin to judge: 6 bets in rolling window, net ~0 bps, BTC ~$64.3k, currently flat

_Updated 2026-06-21 10:55 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0) with BTC near $64,293 — quiet, range-bound conditions and no open position. The rolling window holds just 6 bets, far too few to draw any conclusion.

## How it's doing

The strategy is **idle right now** (signal = 0), holding no position with BTC around **$64,293**. Nothing is being risked at the moment.

## What changed vs last time

- Window bet count nudged from **5 → 6**.
- Rolling net edge slipped from **+4.5 bps to essentially break-even (-0.012 bps)** after costs, with a coin-flip win rate (50%).
- Gross edge in the window is **+2.99 bps**, almost exactly eaten by the **3.0 bps** assumed cost.
- The persistent ledger still shows **0 resolved trades** — these 6 are window/backtest-style bets, not banked live results.

## What the numbers do and don't tell us

They tell us the strategy is behaving roughly as designed: marginal, with gross edge sitting right on top of trading costs. They **do not** tell us whether the edge is holding or fading — 6 bets is statistical noise. A single trade can swing this figure by several bps. We need **dozens** of resolved trades before any read is meaningful, and the edge-search bar (positive net on both venues at 5 bps cost) still has **0 survivors**.

## Honest bottom line

No edge is proven and none is broken — there simply isn't enough data. This was always a marginal candidate (~4 bps gross vs ~3.9 bps breakeven) that is **likely not net-profitable after realistic costs**. The slip from +4.5 to ~0 bps is within noise, not a degradation signal. Keep watching; do not expect or claim profit.
