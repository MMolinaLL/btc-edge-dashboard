# 🟡 34-trade ledger at -1.06 bps/bet (-35.9 total); gross edge ~+1.9 bps, below the ~4 expected and under cost. Still thin.

_Updated 2026-11-01 00:44 UTC · model claude-opus-4-8_

> **WATCH:** Gross edge running below the ~4 bps target and net-negative after costs over 34 trades; keep monitoring, sample still too small to pause on.

**Regime:** BTC ~$77.5k, chopping in the high-$70s/low-$80s after August's run up from the $60s; no signal currently active. This two-sided, volatile tape is what the fade is built for, so soft gross numbers are worth watching.

**How it's doing.** The full live ledger now shows 34 resolved trades at an average of **-1.06 bps each**, totaling **-35.9 bps**, with a **38% win rate**. Backing out the ~3 bps cost, gross edge is running around **+1.9 bps/bet** — positive, but roughly half the ~4 bps the strategy needs, and not enough to clear realistic trading costs. So net-negative, as the honest baseline always warned.

**What changed vs last time.** The rolling window shrank from 15 to **9 bets** and its win rate looks nice (67%), but gross is essentially flat at **-0.06 bps** — meaning the entire **-3.06 bps** net loss there is just cost. A high win rate with near-zero gross tells you the recent wins are small and the occasional losses are large (classic mean-reversion payoff shape).

**What the numbers do and don't tell us.** They confirm the strategy is behaving as a marginal, cost-sensitive signal — consistent with prior validation. They do **not** prove degradation: 34 trades, with individual outcomes ranging from -28 to +52 bps, is far too few to distinguish a weak-but-real edge from noise. One or two big fades dominate the total.

**Bottom line.** No surprises and no edge to get excited about. It remains marginal and, after costs, not net-profitable on this sample. Note the edge-search found **0 survivors** at the 5 bps bar — reinforcing that this is research, not a deployable moneymaker. Keep watching; don't pause yet.
