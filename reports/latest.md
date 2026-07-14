# 🟢 Idle (signal=0); window 12 bets net +4.8 bps, 1 ledger trade -13 bps; sample far too thin; BTC ~$64.2k

_Updated 2026-07-14 15:24 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $64,241, up roughly $1,758 from the prior check (~$62,483). No meaningful regime shift; the actually-traded sample remains tiny.

**Status: idle and unproven.** The strategy is currently flat (signal=0), so there's no open risk right now. BTC sits at ~$64,241 on Coinbase, up about $1,758 since the last check — a modest drift, nothing that changes the picture.

**What the numbers say (and don't):**
- The rolling *window* shows 12 bets, 83% wins, +7.8 bps gross / +4.8 bps net at an assumed 3 bps cost. That looks fine on the surface, but 12 bets is far too few to trust — this is noise-range, not evidence of edge.
- The *live ledger* has just **1 resolved trade**, and it lost: a short on 2026-07-06 that went against us for -10 bps gross, -13 bps net. One losing trade tells us essentially nothing.
- Recall the validated backtest edge was only ~4 bps/bet gross against a ~3.9 bps breakeven cost — i.e. marginal, and likely **not net-profitable after realistic costs**. Nothing here changes that.

**Worth noting:** the independent edge search now shows **0 survivors** against the stricter bar (net-positive on both venues at 5 bps cost). That reinforces the prior caution that a durable, cost-robust edge has not been confirmed.

**Bottom line:** Too thin to judge, exactly as before. No degradation alert is warranted, but neither is any confidence that this makes money. Keep collecting data; don't read anything into the single -13 bps loss or the flattering 12-bet window. No guarantee of profit here.
