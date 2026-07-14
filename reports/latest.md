# 🟢 Idle (signal=0); window 12 bets net +3.6 bps, 1 ledger trade -13 bps; sample far too thin; BTC ~$62.5k

_Updated 2026-07-14 08:06 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $62,483, up about $595 from the prior check (~$61,888). No meaningful regime shift; the tradeable sample remains tiny.

**Status: idle and inconclusive.** The strategy currently has no position (signal=0). BTC sits at ~$62,483 on Coinbase, up roughly $595 since the last check (~$61,888) — a small move, no regime change worth flagging.

**What the numbers say (and don't).** The rolling window shows 12 bets, 83% wins, and +3.6 bps net after 3 bps costs. That looks fine on the surface, but 12 bets is far too few to mean anything — a single trade can swing these figures. Separately, the live ledger has just **1 resolved trade**, a short entered/exited on 2026-07-06 that lost 13.0 bps (a 10 bps adverse move plus 3 bps cost). One losing trade is noise, not evidence of breakdown.

**Context you must keep in mind.** This signal's validated gross edge is only ~4 bps/bet against a ~3.9 bps breakeven cost — it is marginal and likely NOT net-profitable after realistic costs. The edge search still shows **0 survivors** at the stricter 5 bps, two-venue bar, consistent with a thin-to-nonexistent net edge.

**Bottom line.** Nothing actionable. The strategy is behaving as expected for a highly selective signal: it rarely trades, so the sample grows slowly. We cannot confirm or reject its edge yet — neither the +3.6 bps window nor the -13 bps single trade is enough to judge. No profit is implied or guaranteed. Keep collecting data; revisit once dozens of independent trades accrue.
