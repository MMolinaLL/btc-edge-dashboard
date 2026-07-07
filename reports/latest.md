# 🟢 Idle (signal=0); 16-bet window net -15.1 bps, gross -12.1 bps — negative but far too thin to judge; BTC ~$63.2k

_Updated 2026-07-07 09:43 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no live position) with BTC near $63,200, down slightly from ~$64,200 last check. The rolling window holds just 16 bets — a tiny sample where a couple of trades dominate the average, so this is noise territory, not evidence of edge decay.

**Status:** No live position right now (signal = 0). BTC is trading around $63,200.

**What changed vs last time:** The rolling window grew from 13 to 16 bets — three more resolved bets since the prior check. Net performance is essentially unchanged: -15.1 bps (was -15.2), gross -12.1 bps (was -12.2), at an assumed 3.0 bps cost. Win rate sits at 37.5%.

**What the numbers do tell us:** Recent bets have leaned negative, and the single fully-logged ledger trade lost -13.0 bps (a short that got run over as price rose ~10 bps in 5 minutes). Both gross and net are underwater over this window.

**What they do NOT tell us:** Basically anything conclusive. This strategy was always expected to be marginal — roughly 4 bps gross edge against a ~3.9 bps breakeven cost — and it only trades ~1-2% of candles. Sixteen bets is far too few to distinguish a real edge from random scatter; one or two trades swing the whole average. A negative gross reading here is well within normal noise for a sample this small. Separately, the independent edge search still finds 0 survivors that clear a positive net bar on both venues at 5 bps — a reminder this signal is likely not net-profitable after realistic costs.

**Bottom line:** Nothing to act on. Numbers are soft but the sample is too thin to judge, and this was never a guaranteed winner. Keep collecting data; revisit once dozens of resolved trades accumulate.
