# 🟢 Idle (signal=0); 6-bet window net -2.96 bps — flipped negative but far too thin to judge; BTC ~$62.6k

_Updated 2026-07-05 17:45 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $62,552. The rolling window still holds only 6 bets — statistically meaningless noise.

**Status:** The strategy is doing nothing right now — `signal=0`, no open position. It's a selective signal that only trades ~1-2% of candles, so quiet stretches are normal.

**What changed vs last time:** The 6-bet rolling window swung from **+3.27 bps net** to **-2.96 bps net**. That sounds like a reversal, but it's the same tiny 6-bet sample re-measured — a single bet moving in or out flips the sign. Gross edge shows as **+0.04 bps** against an assumed **3.0 bps** cost, so net is negative purely because costs swamp a near-zero gross number. Win rate is 4/6 (66.7%), which is meaningless at this size.

**What the numbers do and don't tell us:** They tell us the strategy is behaving as designed (rarely trading) and that BTC is roughly flat (~$62.6k). They tell us **nothing** about edge — 6 bets cannot distinguish skill from luck. The persistent ledger shows **0 resolved trades**, so there's no durable track record yet. The edge search still finds **0 survivors** that clear the stricter 5 bps two-venue bar, consistent with this being a marginal, likely-not-net-profitable candidate.

**Honest bottom line:** Nothing actionable. This is not degradation — it's noise on a sample far too small to judge. No alert warranted. Recall the validated reality: gross edge ~4 bps vs ~3.9 bps breakeven cost, meaning even a 'working' version is marginal at best. We need dozens of resolved trades before drawing any conclusion.
