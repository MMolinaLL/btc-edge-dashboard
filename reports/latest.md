# 🟢 27 trades net -2.1 bps/bet (-56.1 bps total); last-7 window +14 bps net. Still too thin to judge.

_Updated 2026-09-17 11:08 UTC · model claude-opus-4-8_

**Regime:** BTC ~$76.3k, sitting in the upper $76-81k band where recent shorts have resolved well; the loss-heavy cluster sits earlier at $63-66k. Signal is flat (0), so nothing is live right now.

**How it's doing.** Over the full live ledger of 27 resolved trades, the strategy is running slightly *negative*: mean net **-2.08 bps/bet**, totaling **-56.1 bps**, with a 37% win rate. That's below the ~4 bps gross / ~3.9 bps breakeven we already flagged as marginal. But the most recent 7-trade window looks much better: **+14.0 bps net/bet** at 71% wins, driven by a few large winning shorts in the $77-81k band ($21.30/8/23, $9/3: gross up to +51, +29 bps).

**What changed vs last time.** Nothing material — the numbers are identical to the prior read. No new trades have resolved and the signal is flat.

**What the numbers do and don't tell us.** With only 27 trades, and a small handful of big moves swinging the total, none of this is statistically meaningful. A single -28 bps or +49 bps outcome dominates the mean. The recent positive window and the earlier negative total are both consistent with *pure noise* around a near-zero true edge. Note also `edge_search_survivors: 0` — no variant cleared the honest bar (net-positive on both venues at 5 bps cost).

**Bottom line.** This is a marginal, likely-not-net-profitable signal being tracked on a sample far too small to judge. No degradation alarm is warranted, but neither is optimism about the recent hot streak. Keep collecting data; don't size up on 7 good trades.
