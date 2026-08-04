# 🟢 Signal flat (0); 8 resolved trades net -121.5 bps, but one -61 bps loser dominates — still too thin to judge. BTC ~$64.0k

_Updated 2026-08-04 16:12 UTC · model claude-opus-4-8_

**Regime:** No live exposure right now (signal=0). This marginal mean-reversion fade has a ~4 bps expected gross edge that is dwarfed by single-trade swings of 20-60 bps, so a handful of losers can't yet be distinguished from noise.

**How it's doing.** The signal is currently flat (no position). The live ledger has 8 resolved trades, of which only 1 won (12.5% win rate), for a cumulative -121.5 bps and a mean of -15.2 bps/trade. On the surface that looks ugly, but the result is heavily distorted by a single -60.9 bps trade on 2026-07-31 — remove it and the other 7 trades sum to roughly -60.6 bps, still negative but far less dramatic.

**What changed vs last time.** Essentially nothing. Same 8 resolved trades, same dominant outlier, signal still 0. The separate rolling 'window' stat (13 bets) shows gross +0.46 bps and net -2.54 bps after 3 bps cost — i.e. gross edge near zero, consistent with a marginal strategy losing to costs.

**What the numbers do and don't tell us.** With only 8-13 observations and per-trade swings of 20-60 bps against a claimed ~4 bps edge, this sample has almost no statistical power. A run of losers this size is entirely compatible with either genuine degradation or plain bad luck. We simply cannot separate the two yet. Separately, the edge search found **0 survivors** at a 5 bps cost bar — a reminder this was marginal from the start.

**Bottom line.** Discouraging but inconclusive. No evidence of profit, no confirmed breakdown. Keep collecting data; do not act on this sample. This strategy was never expected to be reliably net-profitable after costs.
