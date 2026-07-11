# 🟢 Idle (signal=0); still just 1 resolved trade (-13 bps); sample far too thin to judge; BTC ~$64.1k

_Updated 2026-07-11 07:57 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $64,111, essentially unchanged from the last check (~$64,068). With only a single resolved trade, nothing here is statistically meaningful.

**How it's doing:** The strategy is currently idle — `signal=0`, meaning no position is open and it's waiting for the extreme conditions it fades. That's normal: this signal only trades ~1-2% of candles, so long quiet stretches are expected.

**What changed vs last time:** Essentially nothing. Price is ~$64,111, a few dollars above the prior ~$64,068. The ledger still shows exactly **1 resolved trade**, the same single short from July 6 that lost **-13.0 bps** (a ~-10 bps adverse move plus 3 bps cost). No new trades have resolved.

**What the numbers do and don't tell us:** They tell us the one and only completed trade lost money. They tell us essentially **nothing** about whether the edge is holding. One trade cannot distinguish a broken strategy from ordinary bad luck — a strategy with a genuine ~4 bps edge will still lose on plenty of individual bets. We'd need dozens of resolved trades before any rolling net figure is worth reading.

**Context worth remembering:** Even in validation this was a *marginal* candidate — gross edge ~4 bps vs a ~3.9 bps breakeven cost, and here modeled cost is 3 bps. It may well not be net-profitable after realistic costs. Separately, the edge-search shows **0 survivors** clearing the stricter two-venue bar.

**Bottom line:** Nothing actionable. Too thin to judge; keep collecting data. No profit is promised or implied.
