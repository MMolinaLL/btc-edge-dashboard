# 🟢 Idle (signal=0); 7-bet window net -6.9 bps, sample far too thin to judge; BTC ~$62.6k

_Updated 2026-07-09 16:28 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $62,612, down roughly $315 (~0.5%) since the last check around $62,926. With only a 7-bet rolling window, this remains statistical noise, not signal.

**Status: idle and inconclusive.** The strategy currently holds no position (signal=0), so nothing is at risk right now. BTC sits at ~$62,612 on Coinbase, slightly lower (~0.5%) than the ~$62,926 seen last check.

**What changed:** The rolling window shrank from 9 bets to 7 bets and now shows net **-6.9 bps** per bet (gross -3.9 bps, minus 3.0 bps cost). The one fully resolved ledger trade — a short from 2026-07-06 that went against us by ~10 bps gross, ~13 bps after cost — remains the only closed data point.

**What the numbers do and don't tell us:** They tell us recent bets have leaned negative. They do **not** tell us the edge is broken. Seven bets (and effectively one resolved trade) is nowhere near enough to distinguish a real problem from ordinary variance. Recall this signal was always marginal: expected gross edge ~4 bps against a ~3.9 bps breakeven cost, meaning it may not be net-profitable even when working as designed. A handful of losing bets is fully consistent with that razor-thin, coin-flip-ish profile.

**Bottom line:** No action warranted. The strategy is behaving within the range of noise you'd expect from a marginal, highly selective signal. This is not evidence of edge, nor of breakdown — just too little data. Keep collecting resolved trades; we need dozens before any judgment. No profit is promised or implied.
