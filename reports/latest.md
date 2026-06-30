# 🟢 Idle (signal=0); 8-bet window net +3.7 bps — still far too thin to judge; BTC ~$58.6k

_Updated 2026-06-30 20:33 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $58,600, down roughly $600 since last check. The rolling window has doubled to 8 bets but still carries essentially no statistical weight.

## Status

The strategy is currently **idle** (signal=0) — no position open, which is normal given it only trades ~1-2% of candles. BTC sits at **$58,574**, down about $600 since the prior check (~$59.2k).

## What changed

The rolling window grew from 4 to **8 bets**. Over those 8: win rate 0.875, gross +6.7 bps, minus 3.0 bps assumed cost = **net +3.7 bps/bet**. The persistent ledger still shows **0 resolved trades** (0.0 total bps), so the live, fully-tracked record is effectively empty.

## What the numbers do and don't tell us

A +3.7 bps net over 8 bets *looks* consistent with the validated ~4 bps gross edge — but 8 observations is statistically meaningless. A win rate of 87.5% on 8 bets is just 7 wins; one or two different outcomes would swing the average wildly. We cannot distinguish skill from luck here. Also note the window assumes a **3.0 bps cost**, while honest breakeven is ~3.9 bps — at realistic costs this signal is marginal and likely **not net-profitable**.

Separately, `edge_search_survivors = 0`: no candidate cleared the stricter 5 bps two-venue bar, reinforcing that any edge is fragile.

## Bottom line

Nothing alarming, nothing to celebrate. The sample is **far too thin to judge**. No degradation signal, but also no confirmation of edge. Keep accumulating resolved trades before drawing any conclusion. No implication of guaranteed profit.
