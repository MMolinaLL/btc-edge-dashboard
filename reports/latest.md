# 🟢 Idle (signal=0); 20-bet window net +1.37 bps — marginally positive but far too thin to judge; BTC ~$61.7k

_Updated 2026-07-02 19:02 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $61,661, up from ~$60,378 last check. The rolling window ticked up to 20 bets — still statistically negligible.

## Status
The strategy is currently **idle** (signal=0) — it sees no extreme setup worth fading right now. That's normal: this signal only fires on ~1–2% of candles, so long quiet stretches are expected.

## What changed vs last time
- Rolling window grew from 18 to **20 bets**.
- Window net edge improved slightly to **+1.37 bps/bet** (from +0.86), with a 60% win rate; gross is 4.37 bps against an assumed 3.0 bps cost.
- BTC rose to ~$61,661 from ~$60,378.
- The live ledger still shows **0 resolved trades** — the window stats are a backtest/rolling proxy, not accumulated live P&L.

## What the numbers do and don't tell us
With only 20 bets, a +1.37 bps average is **statistical noise**, not evidence of an edge. At ~4 bps gross with a ~3.9 bps breakeven cost, this strategy was always marginal and likely not net-profitable after realistic fees. A single win or loss swings this small sample meaningfully. Note the window uses a 3.0 bps cost assumption, which is *below* the ~3.9 bps breakeven — so even the mildly positive figure flatters the case.

Also worth flagging: the edge-search found **0 survivors** at the stricter 5 bps two-venue bar, reinforcing that no configuration clears realistic costs.

## Bottom line
No degradation, no edge confirmed — just too little data. Nothing here warrants action or excitement. Keep collecting; dozens of *resolved live* trades are needed before any conclusion. No profit is implied or guaranteed.
