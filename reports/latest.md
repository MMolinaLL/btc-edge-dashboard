# 🟢 Idle (signal=0); 2-bet window net -2.4 bps — far too thin to judge; BTC ~$59.3k

_Updated 2026-06-29 13:56 UTC · model claude-opus-4-8_

**Regime:** Strategy is flat (signal=0, no open position) with BTC near $59,300. The rolling window now spans just 2 bets, so it carries essentially no statistical information either way.

**How it's doing:** The strategy is currently sitting on its hands — `signal=0`, no open position, nothing in the resolved ledger (0 trades). BTC is around $59,328.

**What changed vs last time:** The prior snapshot showed a tiny 4-bet window at +12.0 bps net. This update shows a 2-bet window at **-2.37 bps net** (gross +0.63 bps, minus 3.0 bps cost). That looks like a swing from positive to negative, but it's really just the rolling window rolling over — we're comparing 2 coin-flips to 4 coin-flips. Neither tells us anything reliable.

**What the numbers do and don't tell us:** With only 2 bets, win-rate (100%) and net bps are pure noise; you'd need dozens of resolved trades before any pattern means something. The gross of +0.63 bps here is well below the strategy's validated ~4 bps gross edge, and below the ~3.9 bps breakeven cost — consistent with this being a marginal signal that is likely not net-profitable after realistic costs. Separately, `edge_search_survivors=0`: nothing cleared the strict bar (net positive on both venues at 5 bps cost), which reinforces that no robust, cost-proof edge has been demonstrated.

**Bottom line:** Nothing alarming and nothing encouraging — the live sample is far too thin to judge. No degradation signal, but also no evidence of a durable edge. Keep collecting data; don't read into 2 bets, and don't expect guaranteed profit from a signal this marginal.
