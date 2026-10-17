# 🟢 31 resolved trades, net -1.03 bps/bet (-31.8 total), win 38.7% — thin sample, marginal edge; signal flat.

_Updated 2026-10-17 23:48 UTC · model claude-opus-4-8_

**Regime:** BTC ~$81.3k, consolidating in the low-$80ks after August's surge from the $60ks. Signal is flat (0) and the ledger is unchanged since 2026-10-04 — no new resolved trades this check.

**What's happening.** Nothing new has resolved since the last check (2026-10-04). The ledger still shows **31 trades, all resolved**, with a mean of **-1.03 bps/bet** and a cumulative **-31.8 bps**. Win rate is **38.7%**. The live signal is currently **0** (no position), and price sits around **$81.3k**.

**What the numbers say.** On the surface this looks negative: the strategy is slightly under water net of an assumed 3.0 bps cost. But back out the cost and gross is roughly **+2 bps/bet**, which is *below* the ~4 bps gross edge seen in validation and right around the ~3.9 bps breakeven — exactly the 'marginal, probably not net-profitable after realistic costs' picture we were warned about.

**What they don't say.** 31 trades is a **tiny sample**. With bets this selective (~1–2% of candles) and per-trade outcomes ranging from -28 to +52 bps, a handful of trades swings the whole average. The last 5-trade window (net -2.9 bps, 60% win) is pure noise. We genuinely **cannot distinguish 'no edge' from 'small edge plus bad luck'** at this size — dozens more trades are needed.

**Bottom line.** Results are mildly disappointing but fully consistent with a known-marginal strategy on a thin sample. No evidence of a *sustained* breakdown worth pausing over, and no reason to expect guaranteed profit either. Keep collecting data; revisit if the net stays clearly negative over a materially larger sample.
