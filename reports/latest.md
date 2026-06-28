# 🟡 Flat (signal=0); 9-bet window negative — gross -25.3 bps / net -28.3 bps after 3 bps cost; BTC ~$60.1k

_Updated 2026-06-28 08:36 UTC · model claude-opus-4-8_

> **WATCH:** Rolling window negative again, but sample is tiny (9 bets) — early caution, not a confirmed breakdown.

**Regime:** Strategy is idle (signal=0, no open position) with BTC near $60,100. The short rolling window remains negative even before costs, which is a mild caution flag rather than evidence of a real breakdown.

**Status:** The strategy is sitting on its hands — `signal=0`, no open position, nothing in the formal ledger (0 resolved trades). It's being appropriately selective, so live trades accumulate slowly.

**The numbers:** The short rolling window covers just **9 bets**, with a **33% win rate**, **gross -25.3 bps** and **net -28.3 bps** after 3 bps cost. That's negative both before and after costs.

**What changed vs last time:** Last update we had a 16-bet window at gross -15.4 / net -18.4 bps. The current window is *smaller* (9 bets) and *more negative*. That's not a reassuring drift, but a 9-bet window is essentially noise — one or two bad fades dominate the average, and the count actually shrank, so we're not comparing apples to apples.

**What this does and doesn't tell us:** With only 9 observations, these figures carry huge error bars. We cannot distinguish 'edge gone' from 'normal bad streak.' Recall the validated edge was only ~4 bps gross against a ~3.9 bps breakeven — marginal at best and probably not net-profitable live. The latest edge search found **0 survivors** clearing the stricter bar, reinforcing that any edge is fragile.

**Bottom line:** Negative window plus zero search survivors keeps this at **watch**, not alert — the sample is far too thin to declare a breakdown, and the strategy isn't even trading right now. No profit is implied or expected; treat this as a marginal signal under scrutiny. Revisit once a few dozen resolved trades exist.
