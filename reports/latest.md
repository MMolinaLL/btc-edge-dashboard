# 🟡 38 live bets net -1.66 bps/bet (gross ~1.3 vs ~4 expected); last-13 window flipped positive. Thin, marginal.

_Updated 2026-11-23 17:33 UTC · model claude-opus-4-8_

> **WATCH:** Full-sample gross edge (~1.3 bps) running well below the ~4 bps spec; still too few trades to confirm breakdown.

**Regime:** BTC has dropped to ~$61.7k from mid-$80s Sept/Oct highs — a sharp trend-down leg that is structurally hostile to a mean-reversion fade. Signal is currently flat (0).

**How it's doing.** Across all 38 resolved live bets the strategy is net **-1.66 bps/bet** (total **-63 bps**), winning just **36.8%** of the time. Even before costs the gross edge is only ~1.3 bps/bet — well short of the ~4 bps/bet the backtest led us to expect. So on the full live sample it is underperforming its own (already marginal) spec.

**What changed vs last time.** The most recent rolling window of 13 bets actually looks *better*: **+5.2 bps net** (gross ~8.2 bps) with a 61.5% win rate. That's a genuine improvement over the prior read, but 13 trades is tiny and easily explained by a couple of lucky fades (e.g. the +48.7 and +24.3 bps winners). Don't over-weight it.

**What the numbers do and don't tell us.** They tell us the signal remains *marginal* and, over its full live history, net-negative after a realistic 3 bps cost — consistent with the original finding that breakeven cost (~3.9 bps) sits right at the edge. The separate edge search still returns **0 survivors** at a 5 bps cost bar on both venues, reinforcing that no robust net edge has been demonstrated. What they *don't* tell us: 38 trades can't distinguish 'dead' from 'noisy marginal,' and the recent down-trend is a known-bad regime for fading.

**Bottom line.** Behaving as feared: a thin, marginal signal that is not reliably net-profitable. No evidence of profit, but no clean breakdown either. Keep it on watch, keep collecting trades, don't deploy real size.
