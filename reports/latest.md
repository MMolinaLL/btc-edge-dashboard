# 🟢 30 resolved trades, net -1.0 bps/bet (total -31.3); last-6 window +6.5 bps. Signal flat at 0; sample still thin.

_Updated 2026-09-28 20:24 UTC · model claude-opus-4-8_

**Regime:** BTC ~$83.4k, still well above the low-$63k mid-August prints after a sharp step-up; action remains choppy and high-vol. Signal is 0, so no live position right now.

**How it's doing.** Over 30 resolved live trades the strategy averages **-1.0 bps per bet** (total **-31.3 bps**), with a 40% win rate. The most recent 6-bet window is **+6.5 bps net** (+9.5 gross vs 3 bps assumed cost), so recent bets have leaned positive even as the full-sample average sits slightly negative.

**What changed vs last time.** Essentially nothing material. The headline numbers are unchanged, the signal is still flat at 0 (no open position), and no new alert conditions have triggered.

**What the numbers do and don't tell us.** This was always a *marginal* signal: ~4 bps gross edge against a ~3.9 bps breakeven cost, so it is likely not net-profitable after realistic fees. A -1.0 bps/bet result over 30 trades is fully consistent with that marginal-to-slightly-negative expectation — it is **not** proof of a broken edge, but also **not** evidence of a working one. The individual trades are extremely noisy (single bets range from -28 to +49 bps), so 30 samples cannot distinguish a small real edge from zero. Separately, the offline edge search found **0 survivors** at a 5 bps cost bar on both venues — a reminder the underlying edge is fragile.

**Bottom line.** No degradation alarm: results are within the range expected for a marginal strategy, and the sample is too thin to conclude much. Keep collecting data; do not treat recent positive windows as a profit signal. Realistically this remains a research candidate that is unlikely to clear real-world costs.
