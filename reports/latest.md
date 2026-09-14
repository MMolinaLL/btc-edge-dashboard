# 🟢 26 resolved trades still net -2.0 bps/bet (-51.8 bps total); no new fills since prior. Sample thin, signal flat.

_Updated 2026-09-14 19:04 UTC · model claude-opus-4-8_

**Regime:** BTC ~$79.1k, still in the higher-price band (~$77-81k) where recent trades skewed positive, versus the earlier losing cluster at $63-66k. Live signal is flat (0), so nothing is trading right now.

**How it's doing.** No change since the last check: the ledger still shows 26 resolved trades, a 38.5% win rate, and a mean of **-1.99 bps per trade** (**-51.8 bps cumulative**). No new fills have landed, and the current signal is **0** (flat), so nothing is being traded at the moment.

**What changed.** Essentially nothing — same trade count, same totals. The short 'last-3' window sits at -0.84 bps net, which is just noise at that size.

**What the numbers do and don't tell us.** This strategy was always marginal: a modeled gross edge of only ~4 bps against a ~3.9 bps breakeven cost, meaning it was never expected to be reliably net-profitable after real costs. A negative running total is consistent with that. But 26 trades is still far **too few** to distinguish 'the edge broke' from ordinary bad luck — individual trades swing from **+48.7 to -60.9 bps**, so a handful of outcomes dominate the total. Notably, the earlier losses clustered around $63-66k while the recent higher-price band ($77-81k) trades have skewed positive; that could be regime, or coincidence.

**Bottom line.** Performance is soft and negative, exactly in line with a strategy that may not clear costs — but the sample is too thin to call it a breakdown, and it isn't trading right now. No action warranted; keep logging. Also worth flagging: the fresh edge search found **0 survivors** at the 5 bps two-venue bar, reinforcing that no clearly profitable variant exists here. No profit should be assumed.
