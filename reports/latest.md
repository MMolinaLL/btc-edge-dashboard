# 🟢 Idle (signal=0); only 1 resolved trade (-13 bps), 4-bet window net -2.7 bps; far too thin to judge; BTC ~$64.0k

_Updated 2026-07-12 08:20 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $63,969, roughly unchanged from the prior check (~$64,123). With just one resolved trade and a 4-bet rolling window, nothing here is statistically meaningful.

## How it's doing
The strategy is currently idle — `signal=0`, so there's no open position. That's expected: this is a selective signal that only trades ~1-2% of candles, so live data accumulates slowly.

## What changed vs last time
Essentially nothing. Price is ~$63,969 vs ~$64,123 last check (a small dip). The resolved-trade ledger still shows a single trade (entered/resolved July 6), a short (`signal=-1`) that lost -13.0 bps: BTC ticked up ~10 bps against the position, plus 3 bps cost. The 4-bet rolling window shows 50% wins, gross +0.33 bps, net -2.67 bps after 3 bps cost.

## What the numbers do and don't tell us
They tell us almost nothing yet. One resolved trade and a 4-bet window are pure noise — you cannot distinguish a working edge from a broken one at this size. For context, the validated gross edge was only ~4 bps/bet against a ~3.9 bps breakeven cost, so even with hundreds of trades this was expected to be marginal and likely not net-profitable after realistic costs. Separately, the edge search currently has 0 survivors clearing the 'net-positive on both venues at 5 bps' bar — a reminder the underlying edge is fragile.

## Bottom line
No cause for alarm and no evidence of an edge either — the sample is far too thin to judge. Keep collecting data. No guarantee of profit here; treat this as monitoring, not a green light.
