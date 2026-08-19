# 🟡 No live signal; 18-trade ledger at -6.0 bps/trade net (~-3 bps gross) — weak vs +4 bps hope, but tail-driven and thin.

_Updated 2026-08-19 06:43 UTC · model claude-opus-4-8_

> **WATCH:** Live gross (~-3 bps) is running below the ~+4 bps expected edge, but the sample is only 18 trades and one -61 bps loss dominates. Keep monitoring; not yet a clear breakdown.

**Regime:** BTC chopping near $64k with no position currently open. In a selective mean-reversion strategy, a single trend-day loss can swamp dozens of tiny wins.

**How it's doing:** No trade is open right now (`signal = 0`). Across all 18 resolved trades the strategy is down **-108.8 bps total, or -6.0 bps per trade**, winning just 27.8% of the time. Stripping out the modeled 3 bps cost, the *gross* result is roughly **-3 bps per trade** — versus the ~+4 bps gross edge we hoped to see. So on live data the raw signal is underperforming expectations, not just failing to cover costs.

**What changed vs last time:** Little. We added a handful of trades; the picture is essentially the same 'negative but noisy' read, so the alert stays at **watch**.

**What the numbers do and don't tell us:** 18 trades is a *tiny* sample for a signal whose edge was only ~4 bps to begin with. The result is heavily distorted by one outlier — the 2026-07-31 trade lost **-61 bps** by itself. Remove that single bet and the remaining 17 are close to gross-breakeven. That's exactly the tail-risk we warned about: one trend day can bury dozens of small wins. The recent 11-bet window (-2.2 bps gross) tells the same inconclusive story.

**Honest bottom line:** This was always flagged as a *marginal* candidate unlikely to be net-profitable after realistic costs (breakeven ~3.9 bps, edge search survivors = 0). Live data so far is consistent with 'no reliable net edge,' but the sample is too thin and too outlier-driven to declare a definitive breakdown. Keep watching; do not expect profit.
