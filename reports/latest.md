# 🟢 Idle (signal=0); 14-bet window net -12.2 bps, gross -9.2 bps \u2014 negative but still too thin to judge; BTC ~$62.0k

_Updated 2026-07-06 12:28 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no live position) with BTC near $62,000. The rolling window has grown to 14 bets \u2014 still a very small sample where noise dominates.

**Status:** The strategy is currently idle (signal=0), consistent with its selective design that only trades ~1-2% of candles. No open or resolved ledger trades exist yet.

**What changed:** The rolling window doubled from 6 to 14 bets. Net result slipped from -2.96 bps to **-12.24 bps** (gross -9.24 bps, cost 3.0 bps), with a 57% win rate. Notably, the *gross* figure is now negative \u2014 meaning these recent bets lost money even before trading costs.

**What the numbers do and don't tell us:** They are consistent with the known weak profile \u2014 this signal was only ever a marginal candidate (~4 bps gross edge vs ~3.9 bps breakeven cost), so it is expected to hover near or below zero. But 14 bets is **statistically meaningless**: one or two moves can swing the average by many bps. A -12 bps window at this size is well within normal noise and does not confirm any breakdown. Separately, the edge search now shows **0 survivors** at the 5 bps two-venue bar \u2014 a reminder no robustly net-profitable variant currently clears the honest hurdle.

**Bottom line:** Nothing here changes the prior honest read: this is a fragile, likely-not-net-profitable signal on a sample far too small to judge. The negative drift is worth watching but not actionable. No alert. Wait for dozens more resolved bets before drawing conclusions. This is not a signal to expect profit.
