# 🟢 Signal flat (0), no new fills; ledger still -121.5 bps over just 8 trades — poor but far too thin. BTC ~$64.3k

_Updated 2026-08-07 07:16 UTC · model claude-opus-4-8_

**Regime:** No live exposure right now (signal=0). With expected gross edge only ~4 bps/bet, a single trade swinging from -61 to +6 bps means 8 fills are dominated by noise, not signal.

**What changed:** Nothing material since last check. Price is ~$64,286, the signal is flat (0), so there's no live position, and no new trades have resolved. The ledger is unchanged at 8 resolved trades.

**The numbers:** Across those 8 trades the strategy is net **-121.5 bps total** (mean **-15.2 bps/trade**) with only **1 of 8 winning (12.5%)**. That looks ugly, but note how lopsided it is: one trade lost -60.9 bps and another -22.8 bps, dragging the whole set down. The embedded 'window' stat (8 bets, +1.8 net bps) counts things differently and shouldn't be over-read either.

**What this does and doesn't tell us:** With a gross edge of only ~4 bps/bet and a breakeven cost near 3.9 bps, this strategy was always marginal — likely *not* net-profitable after realistic fees. A handful of trades cannot confirm or reject a 4-bps edge; the outcome here is dominated by one or two large adverse fills, i.e. noise. It is genuinely too thin to judge. Separately, the fresh edge-search found **0 survivors** at the 5-bps, both-venues, no-look-ahead bar — a reminder the underlying edge is fragile.

**Bottom line:** No action; no live exposure anyway. Results are weak-to-negative but statistically meaningless at n=8. Keep collecting data — I'd want dozens of trades before drawing conclusions, and even then expect this to be, at best, a marginal edge. No guarantee of profit.
