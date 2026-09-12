# 🟢 26 trades, mean -2.0 bps net (-51.8 bps total); last 7 bets +8.3 bps net. Still too thin to judge. Signal flat.

_Updated 2026-09-12 10:13 UTC · model claude-opus-4-8_

**Regime:** BTC ~$77.4k, well above the $63-66k band where the early losing cluster occurred; trades since late August (higher-price regime) skew positive. Live signal is flat (0) now.

**How it's doing.** Over the full live ledger of 26 resolved trades, the strategy is net *negative*: mean -2.0 bps/bet, -51.8 bps cumulative, winning only 38% of the time. That's below the ~4 bps gross edge we expected and, after costs, unprofitable so far. However, the most recent 7 bets look better: 71% wins, +11.3 bps gross / +8.3 bps net at an assumed 3 bps cost.

**What changed vs last time.** Very little. The rolling recent window is still modestly positive (was +6.7 bps over 9 bets, now +8.3 over 7), and the full-ledger mean is essentially unchanged. The signal is flat right now.

**What the numbers do and don't tell us.** They don't tell us much yet — 26 trades is a tiny sample, and the recent gain is driven by a handful of profitable shorts during the late-August/September higher-price regime, including a couple of large winners (+48, +26, +28 bps). The early losses clustered in the $63-66k band. This split could be genuine regime dependence or just noise; we can't distinguish with this few trades. Note the window assumes 3 bps cost, but breakeven is ~3.9 bps, so under realistic costs the recent edge shrinks. Separately, the edge search still finds **zero** survivors passing the 5 bps two-venue bar.

**Bottom line.** Marginal at best, cumulatively unprofitable, sample too thin to conclude anything. No degradation alert, but no evidence of durable profit either. Keep monitoring; do not scale up.
