# 🟢 Idle (signal=0); 9-bet window net +2.24 bps — positive but far too thin to mean anything; BTC ~$63.1k

_Updated 2026-07-04 17:41 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $63,097, up roughly $600 since the last check. The rolling window holds just 9 bets — statistically meaningless.

**Status:** The strategy is sitting on its hands — `signal=0`, no open position. That's normal for a selective mean-reversion system that only trades ~1-2% of candles.

**What changed vs last time:** The rolling window shrank from 16 bets to just 9, and the reported net flipped from roughly flat (-0.07 bps) to slightly positive (+2.24 bps net, +5.24 gross at an assumed 3.0 bps cost, 78% win rate). Do not read anything into this swing — with only 9 observations, a couple of trades dominate the average. BTC ticked up to ~$63,097 from ~$62,462.

**What the numbers do and don't tell us:** They tell us the system is alive, idle, and hasn't blown up. They tell us essentially *nothing* about whether the edge is holding. Nine bets cannot distinguish a real +2 bps edge from pure luck, especially when the validated gross edge is only ~4 bps against a ~3.9 bps breakeven cost. Note the assumed 3.0 bps cost here is below that breakeven — at realistic costs this window would be near zero. The persistent ledger still shows 0 resolved trades, so there's no live track record yet. `edge_search_survivors=0` is a reminder that nothing has cleared the stricter dual-venue 5 bps bar.

**Bottom line:** No edge confirmed, no degradation detected — just not enough data. This remains a marginal, likely-not-net-profitable candidate. Keep collecting; judge nothing until dozens of resolved trades accumulate.
