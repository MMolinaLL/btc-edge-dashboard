# 🟢 30 trades, net -1.0 bps/bet (total -31.3); unchanged vs last check. Marginal as expected; signal flat at 0.

_Updated 2026-09-26 10:56 UTC · model claude-opus-4-8_

**Regime:** BTC ~$84.2k after a large run-up from the low-$63k range seen in mid-August; volatility has been high and choppy. Signal is currently 0 (no live position).

**How it's doing:** The full live ledger still shows 30 resolved trades, win rate 40%, averaging **-1.0 bps per bet** for a cumulative **-31.3 bps**. That is essentially unchanged from the prior check — no new trades have resolved, so nothing material has moved.

**What the numbers do and don't tell us:** A slightly negative average is exactly what we'd expect from a strategy whose gross edge (~4 bps) sits right at its breakeven cost (~3.9 bps). At 30 trades the result is dominated by a handful of outliers: single wins of +49, +26 and +25 bps, and losses of -28 and -13 bps. With that much dispersion, 30 samples cannot distinguish 'small real edge' from 'no edge' — the confidence band easily spans both sides of zero. The rolling 6-bet window (+5.1 bps net, 67% win) is far too small to read as improvement.

**Context:** The independent edge search still finds **zero survivors** at a 5 bps cost bar across both venues — consistent with this being marginal-at-best after realistic costs.

**Bottom line:** Behaving as expected for a marginal, likely-not-net-profitable signal. Nothing here warrants an alert, but nothing suggests a durable edge either. This remains a research candidate, not a green light. We need many more resolved trades before drawing any conclusion.
