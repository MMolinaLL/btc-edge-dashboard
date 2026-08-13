# 🟢 Flat (signal 0); 13-trade ledger nets -8.9 bps/bet, 11-bet window gross ~0 bps — still too thin to judge. BTC ~$63.5k

_Updated 2026-08-13 22:42 UTC · model claude-opus-4-8_

**Regime:** BTC keeps chopping in the low-to-mid $60k range with no signal active right now. Losses remain driven by a few large outlier trades rather than a broad, confirmed edge breakdown.

**Status: idle.** No signal is firing right now (`signal 0`), and the strategy trades rarely by design (~1–2% of candles), so the live sample grows slowly.

**The numbers.** The full ledger now has 13 resolved trades: win rate 31%, mean **-8.9 bps/bet**, cumulative **-115 bps**. The rolling 11-bet window looks less grim — gross **-0.08 bps** (essentially breakeven before costs), net **-3.1 bps** after an assumed 3 bps cost. That gap tells the real story: the strategy's *gross* result is roughly flat-to-slightly-negative, and the modeled trading cost is what pushes it into the red — consistent with the pre-validated view that this signal is marginal and probably not net-profitable after realistic costs.

**What changed.** One more trade since last time, plus a couple of recent small wins (+10.2, +5.0, +1.5 bps). The ugly ledger average is still dominated by a handful of outliers — a single -60.9 bps trade (2026-07-31) plus -22.8 and -18.2 — not a steady bleed.

**What this does and doesn't tell us.** With only 13 trades, results are noise-dominated; a couple of outliers swing the average wildly. This is far too small to confirm either edge or breakdown. Separately, the edge-search found **0 survivors** clearing the honest bar (net positive on both venues at 5 bps cost).

**Bottom line.** No cause to pause, but no evidence of profitable edge either. Marginal-at-best, sample-too-thin. Keep collecting data; don't over-read early losses.
