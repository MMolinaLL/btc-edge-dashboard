# 🟢 Idle (signal=0); 4-bet window net +5.1 bps — still far too thin to judge; BTC ~$59.2k

_Updated 2026-06-30 10:42 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $59,200, down roughly $1k since last check. The rolling window now spans just 4 bets, which carries essentially no statistical weight.

**Status: quiet and inconclusive — exactly as expected for a selective strategy.**

Right now the strategy holds no position (signal = 0). Since it only acts on ~1–2% of candles, long idle stretches are normal and not a problem.

**What the numbers say.** The rolling window shows 4 bets, all winners (100%), averaging +5.1 bps net after an assumed 3.0 bps cost (+8.1 bps gross). That looks nice on the surface — but with only 4 trades it tells us almost nothing. A single bet can swing these figures wildly, and a 100% win rate over 4 tries is well within pure luck. The persistent trade ledger still shows 0 resolved trades, so there is no durable track record yet.

**What changed vs last time.** One more bet has been added (3 → 4), and the window net ticked up from ~+0.4 to +5.1 bps. BTC slipped about $1k to ~$59,230. None of this is statistically meaningful.

**Important context.** This signal was the best candidate found, but its validated edge is only ~4 bps/bet against a ~3.9 bps breakeven cost — marginal, and likely NOT net-profitable after realistic trading costs. Note too that `edge_search_survivors = 0`: nothing cleared the stricter 5 bps two-venue bar.

**Bottom line.** Too thin to judge. The early window leans positive, but that is noise, not proof. No degradation signal, no reason to act. We need dozens of resolved trades before drawing any conclusion — and even then, expect this edge to be fragile, not a money machine.
