# 🟢 Idle (signal=0); window 10 bets net +3.6 bps, 1 ledger trade -13 bps; still far too thin; BTC ~$63.0k

_Updated 2026-07-13 09:29 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $63,038, down modestly from the prior check (~$63,683). No meaningful regime shift; sample remains tiny.

**Status:** The strategy is sitting on its hands (signal = 0), which is normal — it only trades ~1-2% of candles by design. BTC is ~$63,038, slightly lower than last check (~$63,683).

**What changed:** The rolling window ticked up from 7 to 10 bets, with net +3.6 bps and an 80% win rate (gross +6.6 bps, cost 3 bps). The independent ledger still shows just **1 resolved trade**: a short on 2026-07-06 that lost -13 bps as price rose against it.

**What the numbers do and don't tell us:** Almost nothing conclusive yet. Ten window bets and a single ledger trade are statistically meaningless — one bad fill can swing these figures wildly, and one good streak can flatter them. The window's +3.6 bps looks fine, but that's roughly in line with the strategy's razor-thin validated edge (~4 bps gross vs ~3.9 bps breakeven cost). This was never a high-conviction, clearly net-profitable signal; it's marginal at best.

Note also `edge_search_survivors = 0`: no candidate currently clears the stricter bar (net positive on both venues at 5 bps cost, no look-ahead). That's a standing caution, not new degradation.

**Bottom line:** No edge confirmation and no evidence of breakdown — the data is simply too thin to judge either way. Keep collecting resolved trades; a fair read needs dozens, not a handful. Do not read the +3.6 bps as proof of profit, nor the -13 bps ledger trade as proof of failure.
