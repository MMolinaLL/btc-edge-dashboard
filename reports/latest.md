# 🟢 No live signal. 24-trade ledger nets -2.7 bps/trade (-64.4 total); rolling-10 window -2.6 bps. Still too thin to judge.

_Updated 2026-08-29 17:32 UTC · model claude-opus-4-8_

**Regime:** BTC ~$78k, well above the $63-66k range where most ledger trades were placed. The recent winning shorts came from fading the Aug 21-23 spike into the mid-$70ks — good timing in a fast tape, not proof of durable edge.

**How it's doing.** No trade signal right now (`signal=0`). The full ledger stands at 24 resolved trades, winning 37.5% and averaging **-2.7 bps/trade** (-64.4 bps cumulative). The rolling last-10 window is net **-2.6 bps** with a 50% win rate; its gross edge is just **+0.39 bps**, far short of the ~3.9 bps needed to cover realistic costs.

**What changed vs last time.** Essentially nothing — same 24-trade ledger, same broad picture. Price is ~$78k, roughly where it was last check.

**What the numbers do and don't tell us.** They confirm what backtesting warned: this signal is marginal, and net-of-cost results are negative so far. But 24 trades is a *tiny* sample — a few outliers dominate. Two big losers (-61 and -28 bps in fast trends) and a couple of big winners (+49, +25 bps fading the Aug spike) swing the whole tally. That's exactly the noise you'd expect at this size; it is not enough to prove the edge is broken *or* intact.

**Bottom line.** Consistent with expectations for a strategy whose gross edge (~4 bps) barely beats its breakeven cost (~3.9 bps): likely not net-profitable, and the live data can't yet confirm otherwise. No degradation *beyond* what was already known, so no alert — but no evidence of a live money-making edge either. Keep accumulating trades before drawing conclusions. Note: the independent edge search still finds **zero survivors** at a 5 bps cost bar.
