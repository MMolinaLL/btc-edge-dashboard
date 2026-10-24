# 🟢 32 resolved trades, net -1.0 bps/bet (-32.5 total); 9-bet window -0.4 bps — thin and basically flat vs last check.

_Updated 2026-10-24 00:19 UTC · model claude-opus-4-8_

**Regime:** BTC ~$80.8k, still chopping in the low-$80ks after August's run up from the $60ks. Signal is flat (0) and the ledger is essentially unchanged since last check — no new resolved trades, just the rolling window shifting by one.

**What's happening:** The strategy has now logged 32 resolved trades, with a mean of **-1.0 bps/bet** and a cumulative **-32.5 bps**. Only 37.5% of trades win. The most recent rolling window (9 bets) is **-0.42 bps net** — gross +2.58 bps eaten by ~3 bps of assumed cost. The live signal is currently flat (0).

**What changed vs last time:** Essentially nothing. The ledger totals (32 trades, -1.0 bps/bet, -32.5 total, 37.5% win) are identical to the prior check; the rolling window just ticked from 8 to 9 bets. No new trades have resolved, so this is the same picture with marginally more context.

**What the numbers do and don't tell us:** 32 trades is still a *tiny* sample for a signal whose entire expected edge is ~4 bps/bet against a ~3.9 bps breakeven. Individual trades swing from +49 bps to -28 bps, so a handful of outcomes dominate the average — the -1 bps mean is well within noise and tells us little with confidence. Separately, the independent edge-search found **0 survivors** at a 5 bps cost bar on both venues, which is consistent with this being a marginal, probably-not-net-profitable signal rather than a broken one.

**Bottom line:** No degradation alarm — the live result (slightly negative, thin) is roughly what you'd expect from a marginal edge after costs. This was never a sure thing, and nothing here suggests guaranteed profit. Keep collecting data; a few dozen more resolved trades are needed before any real conclusion.
