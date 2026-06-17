# 🟢 Still too thin to judge (10 bets); rolling window negative but pure noise at this size

_Updated 2026-06-17 21:31 UTC · model claude-opus-4-8_

**Regime:** No signal active right now (signal=0), BTC near $64.2k. Quiet regime; the selective sample remains tiny and the rolling window actually shrank to 10 bets vs 14 last check.

**How it's doing:** Effectively unchanged and still un-judgeable. The rolling window now shows just **10 bets**, with a **50% win rate**, **gross -1.13 bps**, and **net -4.13 bps** after assumed 3 bps costs. No signal is firing right now (signal=0), and the persistent ledger has **0 resolved trades** — so there's no durable track record yet.

**What changed vs last time:** The window got *smaller* (10 vs 14 bets), which means old bets aged out faster than new ones came in — exactly what you'd expect from a strategy that trades only ~1-2% of candles. The rolling net is still negative, but on a different (and tinier) sample, so it's not a meaningful trend.

**What the numbers do and don't tell us:** With only 10 outcomes, a single trade swings the average by tens of bps. A negative reading here is statistically indistinguishable from luck — it tells us essentially nothing about whether the edge is holding. Recall the validated reality: the gross edge is only ~4 bps/bet against a ~3.9 bps breakeven, so this signal was always marginal and likely **not net-profitable after real costs**. Note also that the broader edge search currently has **0 survivors** clearing the stricter 5 bps two-venue bar.

**Bottom line:** Too thin to conclude anything — no alert warranted, but no encouragement either. This was a borderline candidate by design; keep accumulating bets and don't read into a 10-sample negative blip. No guarantee of profit at any point.
