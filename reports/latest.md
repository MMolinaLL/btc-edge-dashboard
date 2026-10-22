# 🟢 32 trades, net -1.0 bps/bet (-32.5 total); recent 13-bet window softer at -8.4 bps — thin, roughly as expected.

_Updated 2026-10-22 11:18 UTC · model claude-opus-4-8_

**Regime:** BTC ~$81.9k, still chopping in the low-to-mid $80ks after August's run from the $60ks. Signal is flat (0); the rolling 13-bet window is weaker than the full ledger but remains well within noise for a strategy with huge per-trade dispersion.

**What's happening.** The full live ledger is unchanged in shape: 32 resolved trades, 37.5% win rate, averaging **-1.0 bps/bet** (-32.5 bps cumulative). That is essentially what we expected — this signal was flagged up front as *marginal and likely not net-profitable* after realistic costs (~4 bps gross edge vs ~3.9 bps breakeven). Losing a hair per bet is consistent with that prior, not a surprise.

**What changed.** The dashboard now surfaces a rolling 13-bet window at **-8.4 bps/bet net (-5.4 gross, 30.8% win)**. That's softer than the full-history -1.0, and the gross number being negative means the raw signal (before costs) underperformed in this slice. Worth noting — but 13 bets is a tiny sample, and per-trade outcomes here swing wildly (individual trades range from about -28 bps to +52 bps). A couple of bad fades (e.g. the -28 and -13 bps shorts) dominate the window. The standard error on 13 such bets is large enough that -8.4 is not statistically distinguishable from zero.

**What the numbers don't tell us.** With only 32 lifetime trades and ~1-2% of candles trading, we still can't confirm or reject the edge. The offline edge search also found **zero survivors** at a stricter 5 bps cost bar — reinforcing that this is at best a razor-thin effect.

**Bottom line.** No action needed. Performance is in line with a known-marginal strategy; the recent window is weaker but too small to call degradation. Keep watching — if the negative drift persists over several dozen more trades, escalate to watch/alert. No profit is implied or guaranteed.
