# 🟢 Signal flat (0); ledger still -121.5 bps over 8 trades — poor, but sample far too thin to judge. BTC ~$64.8k

_Updated 2026-08-06 08:37 UTC · model claude-opus-4-8_

**Regime:** No live exposure right now (signal=0). Expected gross edge is only ~4 bps/bet, yet single trades swing -60 to +6 bps, so 8 fills are dominated by noise rather than signal.

**How it's doing:** No change worth alarm since last check. The signal is currently flat (0), so there's no live position. The running ledger shows 8 resolved trades, only 1 winner (12.5% win rate), averaging **-15.2 bps** each for **-121.5 bps** total. That looks bad on its face.

**What changed:** Essentially nothing new versus the prior read — same 8-trade ledger, same tiny sample. A separate rolling window reports 10 bets at 70% win and only -1.0 bps net, so even the short-horizon picture is mixed, not uniformly negative.

**What the numbers do and don't tell us:** They do show recent fills have been unlucky/ugly — one -60.9 bps trade (2026-07-31) alone accounts for half the ledger loss. They do *not* let us conclude the edge is broken. With an expected gross edge near ~4 bps and a ~3.9 bps breakeven cost, this strategy was always marginal and likely not net-profitable after costs. Individual trades swinging ±20-60 bps mean 8 samples can't be statistically separated from random. One outlier dominates the total.

**Bottom line:** Too thin to judge, and honestly this candidate was flagged from the start as marginal — the current edge search found **0 survivors** clearing the bar. Don't read profit into it, and don't panic-pause on 8 trades either. Keep logging; a genuine verdict needs dozens of trades. Staying at **none**, but the ledger deserves a closer look if the loss streak persists past ~25-30 fills.
