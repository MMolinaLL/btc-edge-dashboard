# 🟢 No live signal. 24-trade ledger still net -2.7 bps/trade (-64.4 total); rolling 9-bet window +13.7 bps on recent shorts.

_Updated 2026-08-24 06:59 UTC · model claude-opus-4-8_

**Regime:** BTC has re-rated to ~$77.5k from the $63-66k range that generated most of the ledger. The recent winning streak is a handful of shorts that fired during the Aug 21-23 pullback — regime-favorable, not proven durable edge.

**How it's doing.** No trade is live right now (signal = 0). The strategy is deliberately picky, so the sample builds slowly — 24 resolved trades total, which is still far too few to draw firm conclusions.

**The headline numbers, and what they mean.** Across all 24 trades the strategy is net **-2.7 bps per trade** (-64.4 bps cumulative) with only a 37.5% win rate. That's consistent with what we already knew: this signal's gross edge (~4 bps) is razor-thin versus its breakeven cost (~3.9 bps), so it is marginal and likely not net-profitable after realistic fees.

**What changed vs last time.** Little of substance. The rolling window narrowed to 9 bets and is a perfect 9/9 win, +13.7 bps net. Looks great — but read it carefully: nearly all recent wins are **short** trades that paid off during the Aug 21-23 dip while BTC was pulling back from ~$78.6k. That's the regime doing the work, not proof the edge has strengthened. A 9-bet streak is easily noise.

**What the numbers don't tell us.** With two dozen trades, neither the negative full-sample nor the positive recent window is statistically meaningful. Note also `edge_search_survivors = 0`: no variant clears the honest bar (net-positive on both venues at 5 bps cost).

**Bottom line.** No degradation to flag, but no confirmed edge either. Treat as a marginal, likely-unprofitable strategy under monitoring. Keep collecting data; don't act on the hot streak.
