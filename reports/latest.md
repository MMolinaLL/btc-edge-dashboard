# 🟡 Flat (signal=0); 16-bet window negative — gross -15.4 bps / net -18.4 bps after 3 bps cost; BTC ~$60.5k

_Updated 2026-06-27 17:45 UTC · model claude-opus-4-8_

> **WATCH:** Rolling window negative even before costs (gross -15.4 bps over 16 bets), but sample is too small to be conclusive.

**Regime:** Strategy is idle (signal=0, no open position) with BTC near $60,500. The short rolling window is negative before costs — an early caution flag, not yet a confirmed breakdown given the tiny sample.

**Status:** The strategy is currently doing nothing — `signal=0`, no open position — with BTC around $60,500. It only trades on rare extremes (~1-2% of candles), so quiet stretches are normal.

**The numbers:** The rolling window now covers **16 bets** with a **31% win rate**, a **gross** result of **-15.4 bps** and a **net** of **-18.4 bps** after 3 bps costs. The live ledger remains empty (0 resolved trades), so this window is the only read we have.

**What changed vs last time:** The picture got modestly worse. Previously we saw 20 bets at gross -10.1 / net -13.1 bps; now it's a smaller, more negative window (gross -15.4). The fact that the result is negative *even before costs* is the part worth watching — this strategy's edge was always thin (~4 bps gross, ~3.9 bps breakeven), so it has little cushion.

**What this does and doesn't tell us:** 16 bets is far too few to draw firm conclusions — a handful of bad fades can easily produce numbers like these by chance. It is a yellow flag, not proof the edge is gone. Separately, the independent edge search produced **0 survivors** at a stricter 5 bps cost bar, consistent with this being a marginal signal.

**Bottom line:** Honestly marginal and currently leaning negative, but the sample is too thin to conclude breakdown. Keep watching; no profit is implied or guaranteed.
