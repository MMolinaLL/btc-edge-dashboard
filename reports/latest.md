# 🟢 25 resolved trades, mean -1.5 bps net (-38.6 bps total); sample too thin to judge. Signal flat, BTC ~$79k.

_Updated 2026-09-07 18:37 UTC · model claude-opus-4-8_

**Regime:** BTC near $79k, far above the $63-66k band where most ledger trades were struck; the recent short signals into the late-Aug/early-Sep run-up mostly worked, and the live signal is currently flat (0).

**How it's doing:** Over 25 resolved live bets the strategy has averaged **-1.5 bps per trade** (-38.6 bps cumulative) after an assumed 3 bps cost, with a 40% win rate. That's negative, but it's exactly the kind of result you'd expect from a signal whose *gross* edge is only ~4 bps against a ~3.9 bps breakeven cost — the margin is razor-thin, so noise easily swamps it.

**What changed vs last time:** Essentially nothing. Same 25-trade ledger, same -1.5 bps mean. The most recent trades (late Aug into Sep) were mostly **winning shorts** into the run-up toward $79-81k — e.g. +48.7, +25.9, +16.2 bps — which is encouraging but is a handful of bets. The tiny 3-bet rolling window shows +4.2 bps net; that's noise, not evidence.

**What the numbers do and don't tell us:** They confirm the strategy is *selective* (only 25 bets accumulated over ~6 weeks) and *marginal by design*. A few dozen trades cannot distinguish 'no edge' from 'small edge minus costs' — the confidence bands are far wider than the signal. Individual trades range from -61 to +49 bps, so a couple of outliers dominate the total.

**Honest bottom line:** Too thin to conclude anything, and consistent with the prior finding that this is likely **not net-profitable after realistic costs**. No degradation alert is warranted, but no evidence of a live money-making edge either. Keep collecting data; don't deploy real size on this.
