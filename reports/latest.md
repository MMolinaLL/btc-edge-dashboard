# 🟢 Idle (signal=0); 13-bet window net -15.2 bps, gross -12.2 bps — negative but far too thin to judge; BTC ~$64.2k

_Updated 2026-07-06 23:09 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no live position) with BTC near $64,200. The rolling window holds just 13 bets — a tiny sample where a single trade dominates the average and noise, not edge decay, is the likely story.

**Status: quiet and inconclusive.** The strategy is currently flat (signal = 0), so no capital is at risk right now. BTC sits around $64,247, up slightly from ~$63,700 last check.

**What the numbers say.** The rolling window shows 13 bets, a 38.5% win rate, and a net result of **-15.2 bps** (gross -12.2 bps at 3.0 bps assumed cost). The live ledger records exactly **1 fully resolved trade**, which lost -13.0 bps — a short (signal -1) that got run over as price ticked up from $63,438 to $63,501. Nothing has meaningfully changed since the prior assessment; this is essentially the same snapshot.

**What this does and doesn't tell us.** It does *not* tell us the edge is broken. With only ~13 bets (and just 1 in the resolved ledger), a single trade swings the average by more than the entire ~4 bps/bet gross edge we're hunting for. This is pure small-sample noise territory — you'd expect stretches of red purely by chance even from a genuinely (marginally) profitable signal.

**Honest bottom line.** Remember the setup: this is the best candidate found, but its gross edge (~4 bps) barely clears the ~3.9 bps breakeven cost, so it is marginal and likely *not* net-profitable after realistic fees. The current data is negative but far too thin to conclude anything. No action warranted — just keep accumulating trades. I'd want dozens of resolved bets before drawing conclusions. No profit is implied or guaranteed here.
