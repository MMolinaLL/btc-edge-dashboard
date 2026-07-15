# 🟢 Idle (signal=0); window 12 bets net +8.0 bps, 1 ledger trade -13 bps; sample far too thin; BTC ~$65.3k

_Updated 2026-07-15 15:27 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $65,306, up roughly $770 from the prior check (~$64,533). No meaningful regime shift; the live traded sample remains far too small to draw conclusions.

## How it's doing

The strategy is currently **idle** (signal=0), meaning no position is open. BTC sits around **$65,306**, up modestly (~$770) from last check.

## What changed vs last time

- The rolling **window** ticked up to **12 bets** (from 11), still showing a positive **+8.0 bps net** (91.7% win rate). 
- The **live ledger** is unchanged: still just **1 resolved trade**, a loss of **-13.0 bps**.
- **Edge-search survivors remain at 0** — no candidate currently clears the strict bar (net-positive on both venues at 5 bps cost).

## What the numbers do and don't tell us

Honestly: **almost nothing conclusive yet.** The ledger has exactly **one** resolved trade — that single -13 bps loss is pure noise, not evidence of failure. The window's +8 bps looks nice but is measured at an assumed **3 bps cost**, below the ~3.9 bps breakeven, and rests on only 12 bets. A dozen samples cannot separate a real ~4 bps/bet edge from luck.

## Bottom line

No action needed. The strategy is behaving as expected for a **marginal, highly selective** signal that trades ~1-2% of candles. It was never established as reliably net-profitable after realistic costs, and the live data is **far too thin** to confirm or reject an edge. Keep collecting trades; don't read into single results.
