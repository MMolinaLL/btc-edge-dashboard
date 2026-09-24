# 🟢 29 trades net -1.5 bps/bet (total -44.9); last-8 window +9.5 net but tiny. Marginal as expected. Flat now.

_Updated 2026-09-24 11:15 UTC · model claude-opus-4-8_

**Regime:** BTC ~$83.5k, still in an elevated/trending regime that is generally hostile to a mean-reversion fade. Signal is flat (0), so there is no live position right now.

**How it's doing.** Over the full live ledger of 29 resolved trades, the strategy is net **-1.5 bps per bet** (total -44.9 bps), winning just **38%** of the time. Strip out the assumed ~3 bps cost and gross edge is only ~**+1.4 bps/bet** — below the ~4 bps we hoped for and consistent with the pre-registered warning that this signal is marginal and likely *not* net-profitable after realistic costs.

**What changed.** The most recent 8-bet window is actually **positive**: +9.5 bps net (12.5 gross), 62% wins, helped by a few large fades (+49, +26, +18 bps). So there's no sign of *fresh* degradation — if anything the last stretch was fine. The overall negative total is dominated by earlier losers, not a new breakdown.

**What the numbers do and don't tell us.** With only ~29 lifetime trades and ~8 in the recent window, both readings are dominated by a handful of outliers. A single +49 or -28 bps trade swings the average hard. This is **too thin to conclude** the edge is broken *or* alive. Separately, note `edge_search_survivors = 0`: nothing clears the stricter bar (net-positive on both venues at 5 bps cost).

**Bottom line.** Performing roughly as the marginal-edge thesis predicted — small gross edge, likely unprofitable after costs, no acute breakdown. Keep collecting data before drawing conclusions, and don't expect reliable profit. No action needed while the signal is flat.
