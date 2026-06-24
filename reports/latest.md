# 🟢 Still too thin: 15 bets, gross ~4.1 bps, net +1.1 bps after 3 bps cost; BTC ~$60.7k, flat

_Updated 2026-06-24 20:22 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0) with no open position and BTC near $60,700. The rolling window holds just 15 bets — far too small to draw conclusions.

## How it's doing

The strategy is currently **flat** (signal = 0, no open position) with BTC around **$60,688**. The rolling window now shows **15 bets** (up from 13 last time), winning **73.3%**, with a gross edge of **~4.1 bps** and **~+1.1 bps net** after a 3 bps cost assumption.

## What changed vs last time

Very little. Two more bets resolved (13 → 15), and the rolling net slipped slightly from +1.8 to **+1.1 bps**. The gross edge eased from ~4.8 to ~4.1 bps — basically noise at this sample size. BTC drifted down from ~$62.5k to ~$60.7k.

## What the numbers do and don't tell us

- **Do:** the rolling window is still marginally positive net, and roughly in line with the ~4 bps gross edge expected.
- **Don't:** 15 bets is **far too few** to confirm anything. A 73% win rate on 15 trades can flip easily. Note also the cost here is modeled at 3 bps, but the validated breakeven is ~3.9 bps — at realistic costs this edge may be **net-zero or negative**. The separate ledger shows **0 resolved trades**, and the edge re-search found **0 survivors** meeting the strict two-venue bar.

## Bottom line

No red flags, but no validation either. This remains a **marginal, likely-not-net-profitable** candidate, and the live sample is too thin to judge. No action needed — keep collecting data.
