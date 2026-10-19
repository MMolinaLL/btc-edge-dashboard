# 🟢 32 resolved trades, net -1.02 bps/bet (-32.5 total), win 37.5% — flat vs last check; thin and marginal.

_Updated 2026-10-19 19:41 UTC · model claude-opus-4-8_

**Regime:** BTC ~$81.9k, still chopping in the low-$80ks after August's run from the $60ks. Signal is flat (0) and no new resolved trades since the prior check.

**What's happening:** Nothing new has resolved since the last check. The ledger still shows **32 trades, 37.5% win rate, -1.02 bps per trade (-32.5 bps cumulative)**. The signal is currently flat (0), so the strategy isn't in a position. Price has drifted slightly to ~$81.9k from ~$82.4k, still range-bound in the low-$80ks.

**What the numbers do tell us:** The live record is modestly negative, which is *consistent with expectations* — we flagged from the start that this signal's gross edge (~4 bps) barely clears realistic trading costs (~3.9 bps breakeven). A net result hovering near or just below zero after costs is exactly what a marginal strategy looks like. The shorter 11-bet rolling window is roughly breakeven (net -0.35 bps), not a cliff.

**What they don't tell us:** 32 trades is still a tiny sample. Individual outcomes swing wildly (from -28 to +49 bps), so the mean is dominated by a handful of trades and could move several bps in either direction with just a few more results. We cannot distinguish "small real negative edge" from "zero edge plus noise" at this size. Separately, the independent edge search found **zero survivors** at a 5 bps cost bar — a reminder that no robust net-profitable variant has been confirmed.

**Bottom line:** Behaving as a marginal, likely-not-net-profitable strategy, as warned. No degradation alarm, but no evidence of real profit either. Keep watching; don't deploy real capital on this as-is.
