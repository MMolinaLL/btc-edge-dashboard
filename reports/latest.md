# 🟢 Idle (signal=0); 9-bet window net -9.1 bps, sample far too thin to judge; BTC ~$62.9k

_Updated 2026-07-09 09:41 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $62,926, up roughly $660 (~1.1%) since the last check around $62,264. The rolling window is just 9 bets — nowhere near enough to separate real edge from random noise.

## How it's doing

The strategy is currently **idle** — signal is 0, so there's no live position. BTC sits at about **$62,926**, up roughly 1% since the last check.

## What changed vs last time

The rolling window shrank from 12 bets to **9 bets** and net moved from -13.5 bps to **-9.1 bps** (gross -6.1, cost 3.0). The formal ledger now shows **1 resolved trade**: a short entered 2026-07-06 that lost -13.0 bps net when price ticked up against it. Win rate on the window is 33% (3 of 9).

## What the numbers do and don't tell us

They tell us essentially **nothing statistically**. With 9 window bets and only 1 ledger trade, a string of losses is fully consistent with pure noise around a marginal edge. Recall the validated backtest: gross edge is only ~4 bps/bet against a ~3.9 bps breakeven cost — this signal was **never expected to be reliably net-profitable** after realistic costs. So negative live prints are not surprising and are not evidence of a 'breakdown' yet.

Also worth noting: the broader edge search currently has **0 survivors** meeting the strict bar (positive net on both venues at 5 bps cost, no look-ahead) — a reminder that a durable, cost-proof edge has not been demonstrated.

## Bottom line

Too thin to judge. No action warranted — keeping alert level **none**. This is not a green light: the strategy remains marginal and likely not net-profitable after costs. We need dozens of trades before any live conclusion is meaningful.
