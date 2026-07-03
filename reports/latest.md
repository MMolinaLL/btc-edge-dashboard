# 🟢 Idle (signal=0); 14-bet window net +0.05 bps — flat and far too thin to judge; BTC ~$62.2k

_Updated 2026-07-03 18:47 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $62,173, up slightly from ~$61.6k last check. The rolling window is still a negligible 14 bets — no statistical signal.

## How it's doing

The strategy is currently **idle** — signal is 0, meaning no trade is open. Nothing is at risk right now.

The rolling window shows **14 bets**, win rate 50%, with a gross edge of ~3.05 bps and modeled costs of 3.0 bps, netting a razor-thin **+0.05 bps** per bet. In plain terms: after trading costs, this is essentially breakeven — not a profit signal, not a loss signal.

## What changed vs last time

Very little. Price ticked up modestly from ~$61.6k to ~$62.2k. The bet count is unchanged at 14, so no new trades have resolved since the prior check. The persistent, tracked ledger still shows **0 resolved trades** — the strategy hasn't logged a real out-of-sample fill yet.

## What the numbers do and don't tell us

- **Do:** confirm the strategy is behaving as designed — highly selective, trading rarely.
- **Don't:** tell us anything about edge. Fourteen bets is statistical noise; you could get +0.05 or -5 bps purely by chance. We need dozens more resolved trades before any read is meaningful.

Separately, the edge search found **0 survivors** at the stricter 5-bps, two-venue bar — a reminder this candidate is marginal by construction.

## Bottom line

Nothing alarming, nothing encouraging. Too thin to judge, exactly as expected. Keep collecting data; no action warranted.
