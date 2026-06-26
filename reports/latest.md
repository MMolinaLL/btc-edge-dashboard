# 🟡 Unchanged: 21-bet window still negative, gross -8.8 bps / net -11.8 bps after 3 bps cost; BTC ~$59.6k, flat

_Updated 2026-06-26 20:22 UTC · model claude-opus-4-8_

> **WATCH:** Rolling window negative gross and net over 21 bets — early degradation signal, sample still thin.

**Regime:** Strategy is flat (signal=0) with no open position and BTC near $59,600. The rolling window remains negative both gross and net — an early warning, not yet conclusive given the small sample.

## How it's doing
No change since last check — same data snapshot. The strategy is **flat** (signal=0, no position open) with BTC near **$59,639**.

The rolling window covers **21 bets**: win rate **42.9%**, gross **-8.76 bps**, net **-11.76 bps** after 3 bps cost. So over this stretch the signal has been losing money *before* costs, not just getting eaten by fees.

## What changed vs last time
Nothing material — identical numbers. Still no resolved trades in the live ledger (0 trades), so the official out-of-sample record hasn't grown.

## What the numbers do and don't tell us
- This is a **small sample**. 21 bets is far too few to conclude the edge is broken. With a strategy whose gross edge was only ~4 bps/bet, normal noise easily produces a stretch like this.
- That said, being negative *gross* (-8.8 bps) is a yellow flag worth watching — it's not just costs.
- Separately, the edge search found **0 survivors** at its 5-bps two-venue bar, consistent with this being a marginal, likely-not-net-profitable signal to begin with.

## Honest bottom line
This was always a marginal candidate (~4 bps gross edge vs ~3.9 bps breakeven cost). The live window leans negative but the sample is too thin to call it a true breakdown. **Watch**, don't pause yet. I'd want to see dozens more trades stay clearly negative before escalating. No expectation of guaranteed profit here.
