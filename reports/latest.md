# 🟢 27 resolved trades, net -2.1 bps/bet (-56.1 bps total); recent 8-bet window +11.9 bps net. Sample still too thin to judge.

_Updated 2026-09-16 10:58 UTC · model claude-opus-4-8_

**Regime:** BTC ~$75.8k, holding the higher-price band (~$76-81k) where recent fills skew positive; the deep-losing cluster sits earlier at $63-66k. Signal is currently flat (0).

**How it's doing.** Over all 27 resolved live trades the strategy is *net negative*: −2.1 bps per bet, −56.1 bps cumulative, winning only 37% of the time. That is worse than the ~4 bps gross edge we expected — but 27 trades is a tiny sample for a signal this noisy, so this number carries huge error bars and shouldn't be read as proof of anything.

**What changed vs last time.** Essentially nothing. No new trades resolved since the prior check; the ledger, the −2.1 bps mean, and the flat signal are unchanged. The most recent 8-bet window remains positive (+11.9 bps net, 62.5% wins), consistent with the earlier note that fills in the higher $76–81k band have behaved better than the earlier $63–66k losers.

**What the numbers do and don't tell us.** They *do* show the live results have been unimpressive and lumpy — a handful of large hits (+49, +25 bps) and misses (−28, −13 bps) dominate, which is exactly what tiny selective samples look like. They *don't* tell us the edge is broken, because at ~1–2% of candles trading, we can't distinguish a marginal edge from zero at this size. Note also the standing caveat: gross edge (~4 bps) barely clears breakeven (~3.9 bps), and the broader edge search still finds **0 survivors** at a 5 bps cost bar.

**Bottom line.** Marginal, unproven, and likely not net-profitable after realistic costs. Not degrading enough to flag — just too thin to judge. Keep collecting data; do not size up.
