# 🟢 Flat (signal 0); 13-trade ledger nets -8.9 bps/bet, gross ~flat. Sample still too thin to judge.

_Updated 2026-08-14 14:52 UTC · model claude-opus-4-8_

**Regime:** BTC is chopping in the low-$60k range and no signal is active right now. With an expected gross edge of only ~4 bps, a single outlier trade can swamp the entire live sample.

**Status:** No position open (signal 0), price ~$62,585. Nothing to act on right now.

**The numbers.** The full ledger has just **13 resolved trades**, netting **-8.9 bps/bet** (total -115 bps), with a 31% win rate. A rolling window of the last 12 bets shows gross **-0.05 bps** and net **-3.0 bps** after ~3 bps costs. So even before costs, live results are roughly flat-to-slightly-negative versus the ~4 bps gross edge we hoped to see.

**What changed vs last time.** Essentially nothing — one more trade added, same picture. Still flat, still tiny sample.

**What this does and doesn't tell us.** It does *not* tell us the edge is broken. The ledger is dominated by outliers: a single **-60.9 bps** loss (2026-07-31) and a **-22.8 bps** loss account for the bulk of the deficit. Strip those and the rest is a noisy mix of small wins and losses — exactly what you'd expect from a marginal signal at this sample size. A few dozen trades minimum are needed before the average means anything.

**Honest bottom line.** This was always a marginal candidate (gross ~4 bps vs ~3.9 bps breakeven cost), likely not net-profitable after realistic fees, and the separate edge search currently has **0 survivors**. Live data so far is consistent with 'weak or no net edge,' but the sample is genuinely too thin to conclude degradation. No alert — keep collecting data. No profit is implied or guaranteed.
