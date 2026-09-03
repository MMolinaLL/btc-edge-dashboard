# 🟢 Unchanged: 24 resolved trades, -2.7 bps/trade (-64.4 total); sample still too thin to judge. Signal flat.

_Updated 2026-09-03 10:48 UTC · model claude-opus-4-8_

**Regime:** BTC ~$77.5k, still well above the $63-66k band where most ledger trades were struck; no new fills since last update and the signal is currently flat (0).

**What changed:** Essentially nothing since the last check. The ledger still shows **24 resolved trades**, a **37.5% win rate**, and a mean of **-2.685 bps/trade (-64.4 bps cumulative)**. No new fills have landed; BTC drifted from ~$77.3k to **~$77.5k** and the signal is currently **flat (0)**.

**What the numbers say:** On paper the live results are slightly negative. At the 3 bps cost assumed here, a -2.685 bps net average implies gross of only ~+0.3 bps/bet — below the ~4 bps gross edge we expected in validation, and below the ~3.9 bps breakeven cost. So live performance is *soft*.

**What they don't say:** With just 24 trades, this is far too thin to conclude the edge is broken. A couple of large losers (e.g. -60.9 and -28.1 bps) dominate the total, while a few big winners (+48.7, +25.3 bps) offset. That is exactly the high-variance, small-sample picture we warned about. The recent -7.6 bps over 9 bets is likewise noise-dominated.

**Bottom line:** This strategy was always marginal — best candidate found, but likely **not net-profitable after realistic costs** (note: `edge_search_survivors` = 0 at the 5 bps bar). Live data so far is mildly disappointing but statistically inconclusive. No alert warranted; keep collecting trades before drawing any conclusion. No profit is implied or guaranteed.
