# 🟢 31 trades, net -1.03 bps/bet (-31.8 total), win 38.7%; no change since last check — still too thin to judge.

_Updated 2026-10-12 01:03 UTC · model claude-opus-4-8_

**Regime:** BTC ~$83.9k, chopping in the low-$80ks after August's climb from the low-$60ks. Signal is 0 (no live position), and per-trade outcomes remain very wide (roughly -28 to +49 bps).

**What the numbers say.** The live ledger is unchanged from last check: 31 resolved trades, averaging **-1.03 bps per bet** (-31.8 bps cumulative), with a **38.7% win rate**. The recent rolling window of 6 bets is slightly negative too (net -1.01 bps, gross 1.99 vs 3.0 cost). No new trades have resolved, and there's no open position right now (signal 0).

**What changed.** Essentially nothing since the prior update — same trade count, same P&L. This is expected: the strategy is selective (only ~1-2% of candles trade), so the sample grows slowly.

**What this does and doesn't tell us.** A -1 bps average on 31 trades sounds bad, but it is well within noise for a signal whose *gross* edge was only ~4 bps and whose breakeven cost is ~3.9 bps. With per-trade outcomes swinging from about -28 to +49 bps, 31 trades simply cannot distinguish 'no edge' from 'tiny edge eaten by costs.' Separately, the edge-search found **0 survivors** that clear a positive net result on both venues at 5 bps cost — a reminder this candidate was always marginal.

**Bottom line.** Performing roughly as a marginal, likely-not-net-profitable strategy would. Nothing here warrants an alert, but nothing suggests a reliable edge either. Keep accumulating trades before drawing conclusions, and don't expect profit.
