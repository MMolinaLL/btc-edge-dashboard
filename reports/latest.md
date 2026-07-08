# 🟢 Idle (signal=0); 12-bet window net -13.5 bps but far too thin to judge; BTC ~$62.3k

_Updated 2026-07-08 23:08 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no live position) with BTC near $62,264, up about $580 (~0.9%) since the last check around $61,682. The rolling window is a mere 12 bets — nowhere near enough to distinguish real edge from random noise.

**Status:** The strategy is sitting on its hands right now (signal = 0, no open position). BTC is around $62,264 on Coinbase, up roughly 0.9% from last check.

**What changed:** The rolling window shrank from 17 bets to 12 (older trades aged out), and its net result is -13.47 bps (gross -10.47 bps, ~3 bps cost). The separate ledger still shows just 1 fully resolved live trade — a short on 2026-07-06 that lost 13 bps when price ticked up against it.

**What the numbers tell us:** Almost nothing yet, honestly. With only 12 bets (and a single resolved ledger trade), a -13 bps average is well within the range of pure luck. A couple of unlucky fades can drag a tiny sample deeply negative without saying anything about the underlying edge. A ~42% win rate on 12 bets is statistically indistinguishable from a coin flip.

**What they don't tell us:** Whether the edge is actually broken. Recall this signal was only ever marginal — ~4 bps gross per bet against a ~3.9 bps breakeven cost — so it may not be net-profitable even when working as designed. The current negative print is consistent both with 'no real edge' and with 'normal noise.' Also note: the broader edge search now shows 0 survivors clearing the strict two-venue, 5-bps-cost bar.

**Bottom line:** Too thin to judge. No action warranted — this is not evidence of profit, nor yet evidence of breakdown. Keep collecting trades.
