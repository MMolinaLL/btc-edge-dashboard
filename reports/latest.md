# 🟢 29 trades net -1.5 bps/bet (total -44.9); recent 7-bet window +8.4 net but tiny. Marginal as expected. Short signal live.

_Updated 2026-09-25 11:20 UTC · model claude-opus-4-8_

**Regime:** BTC ~$85.1k in an elevated, choppy regime that is not especially friendly to a mean-reversion fade. Signal is currently -1 (a live short/fade position).

**How it's doing.** Over the full live ledger, 29 resolved trades average **-1.5 bps/bet** (total **-44.9 bps**) with a **37.9%** win rate. The most recent 7-bet window looks better — **+8.4 bps/bet net**, 71% wins — but that's only seven trades and is dominated by a couple of large winners (e.g. +48.7 and +25.9 bps). Single outliers swing these averages hard.

**What changed vs last time.** Essentially nothing material. Total net moved from -44.9 to... still -44.9; the recent-window net ticked up as the reported cost assumption dropped to 3.0 bps. The strategy is now showing a live **short (signal -1)** rather than sitting flat.

**What the numbers do and don't tell us.** They confirm the prior finding: this is a **marginal** signal. Gross edge was only ~4 bps/bet in validation against a ~3.9 bps breakeven, so a slightly-negative live net is exactly what you'd expect from a strategy that probably doesn't clear realistic costs. Crucially, ~29 trades is **far too few** to distinguish 'no edge' from 'small edge plus noise' — the win rate and P&L are both within normal small-sample scatter. Note also **edge_search_survivors = 0**: nothing cleared the stricter 5-bps two-venue bar.

**Bottom line.** No new alarm and no cause for excitement. Performance is consistent with a marginal, likely-not-net-profitable signal. Keep logging; do not scale up. There is **no evidence of guaranteed profit** here.
