# 🟢 Signal flat (0); tiny sample (5-7 trades) running negative but far too thin to judge — BTC ~$65.2k

_Updated 2026-07-27 09:53 UTC · model claude-opus-4-8_

**Regime:** Signal is currently inactive (signal=0). The live sample is tiny and sparse, so early-negative results are indistinguishable from ordinary noise.

**Status:** No trade signal right now (`signal=0`), BTC ~$65,232 on Coinbase. Nothing has meaningfully changed since last check — the strategy is still barely active and the live sample is still far too small to draw conclusions.

**The numbers:** The rolling window shows 7 bets, 43% win rate, and −3.7 bps net (−0.7 bps gross, before 3 bps cost). The resolved ledger shows 5 trades, 20% win rate, averaging −8.2 bps net (−41 bps total). All negative — but with only 5-7 resolved trades, this is noise-level, not signal. One trade alone (2026-07-17, −22.8 bps) drives much of the loss; another (2026-07-24, +3.1 bps) was a small win. A single bad fill swings these averages wildly.

**What this does and doesn't tell us:** It does NOT tell us the edge is broken. Remember the strategy's validated edge is only ~4 bps/bet gross against a ~3.9 bps breakeven cost — it was always marginal and likely not net-profitable after realistic costs. A handful of losing trades is exactly what you'd expect from ordinary variance around a near-zero edge. To actually judge degradation we need dozens of resolved trades, and this selective signal (~1-2% of candles) grows that sample slowly.

**Also worth noting:** the broader edge search currently has 0 survivors clearing the stricter 5 bps two-venue bar — a reminder that a robust net-profitable edge has not been demonstrated.

**Bottom line:** Too thin to judge. Keep collecting data; don't act on 5-7 trades either way.
