# 🟡 37 live bets net -2.36 bps/bet (gross ~0.6 vs ~4 expected); recent 6-bet window +16.9 but tiny noise. Still degraded.

_Updated 2026-11-19 02:57 UTC · model claude-opus-4-8_

> **WATCH:** Full-sample net edge remains clearly negative (-2.36 bps/bet over 37 trades); recent positive blip is too small to reverse the call.

**Regime:** BTC ~$62.5k, continuing its slide from mid-$80s Sept/Oct peaks with violent 5-min swings. Signal is flat right now; earlier dip-buying (long) entries got repeatedly run over by the falling market.

**How it's doing.** Over the full live ledger of 37 resolved bets, the strategy is losing: win rate 35%, averaging **-2.36 bps per bet** for a cumulative **-87 bps**. Backing out the 3 bps cost, that's only ~0.6 bps gross edge — versus the ~4 bps gross we expected in validation. So the raw signal is performing well below its (already marginal) design spec.

**What changed vs last time.** Not much materially. The recent rolling window shows 6 bets, 67% wins, **+16.9 bps net** — which looks great, but 6 trades is pure noise and cannot overturn a 37-trade negative record. A single lucky short on an 80k+ spike (e.g. +48 bps) can dominate a window this small. Treat the green window with skepticism.

**What the numbers do and don't tell us.** They do tell us the full-sample edge is negative and the strategy would not have paid its way at realistic costs. They don't yet give a statistically clean verdict — 37 bets is thin, and this was always a marginal candidate (gross edge ~4 bps, breakeven ~3.9 bps). Note also the edge re-search found **zero survivors** passing the two-venue, 5-bps-cost bar.

**Honest bottom line.** No evidence of a durable, net-profitable edge; the live record is mildly negative and consistent with a signal that doesn't clear costs. This is not a crisis warranting panic, but it is not working as hoped. Keep monitoring; do not deploy real capital on this as-is.
