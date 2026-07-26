# 🟢 Signal flat (0); live sample still tiny (~5-12 trades) and net negative, but too thin to judge — BTC ~$64.3k

_Updated 2026-07-26 08:27 UTC · model claude-opus-4-8_

**Regime:** Signal is currently inactive (signal=0), with no clear regime shift. The live sample remains far too small to separate real degradation from ordinary noise.

**How it's doing:** The signal is idle right now (signal=0), which is normal — this strategy only trades ~1-2% of candles, so live data accumulates slowly. The trades that have resolved are running negative: the ledger shows 5 resolved trades averaging **-8.2 bps net** (-41 bps total, 1 of 5 winners), and the broader window counts 12 bets at **-4.9 bps net** (-1.9 bps gross, before its 3 bps cost assumption).

**What changed vs last time:** Essentially nothing material. Numbers are in the same ballpark as the prior read. The most recent trade (Jul 24) was actually a small winner at +3.1 bps net, but two large losers (-13 and -22.8 bps) dominate the tiny sample.

**What the numbers do and don't tell us:** With only 5-12 trades, this tells us almost nothing statistically. The validated edge was only ~4 bps/bet gross against a ~3.9 bps breakeven cost — marginal by design, and *likely not net-profitable after realistic costs*. A run of a few losers is fully consistent with both a dead edge and normal variance around a razor-thin one. You cannot distinguish those yet. Separately, `edge_search_survivors=0` is a standing reminder that nothing cleared the stricter 5 bps two-venue bar.

**Bottom line:** No alert. Results are soft but the sample is too thin to conclude degradation. Keep collecting; revisit once several dozen resolved trades exist. Do not expect this to be a money-maker.
