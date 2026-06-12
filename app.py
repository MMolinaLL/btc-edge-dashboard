"""
Trading-research dashboard (Streamlit + Plotly).

Run:  streamlit run app.py
Pure-Python stack (no Node needed). Visualizes every dataset we collect plus the
honest backtests, weather-market convergence, the edge-search leaderboard, and
the forward paper-trading ledger.
"""
import json
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import eval_engine as ee
from weather_backtest import parse_datecode, in_bucket

st.set_page_config(page_title="Edge Research", layout="wide",
                   initial_sidebar_state="collapsed")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# ------------------------------ loaders -----------------------------------
@st.cache_data(show_spinner=False)
def load_parquet(path):
    return pd.read_parquet(path) if os.path.exists(path) else None


@st.cache_data(show_spinner=False)
def leaderboard(path, cost_bps):
    df = pd.read_parquet(path)
    return ee.run_all(df, cost_bps)


@st.cache_data(show_spinner=False)
def equity_for(path, strategy, cost_bps):
    df = pd.read_parquet(path)
    sig = np.asarray(ee.ALL_STRATEGIES[strategy](df))
    res = ee.evaluate_spot(df, sig, cost_bps)
    eq = res["equity"]
    # downsample for plotting
    step = max(1, len(eq) // 4000)
    return eq.iloc[::step], res, df.index[int(len(df) * 0.7)]


def fmt_pct(x):
    return "—" if pd.isna(x) else f"{x*100:.2f}%"


@st.cache_data(ttl=60, show_spinner=False)
def fetch_live_candles():
    """Recent 5m BTC candles from a live, US-reachable source — no local PC needed."""
    import requests
    from datetime import datetime, timedelta, timezone
    try:  # Binance.US: one request, ~3.5 days
        r = requests.get("https://api.binance.us/api/v3/klines",
                         params={"symbol": "BTCUSDT", "interval": "5m", "limit": 1000},
                         timeout=12)
        if r.ok and r.json():
            df = pd.DataFrame(r.json(), columns=["t", "open", "high", "low", "close",
                                                 "volume", *[f"_{i}" for i in range(6)]])
            df["time"] = pd.to_datetime(df["t"], unit="ms", utc=True)
            for c in ["open", "high", "low", "close", "volume"]:
                df[c] = pd.to_numeric(df[c])
            return df.set_index("time")[["open", "high", "low", "close", "volume"]], "Binance.US"
    except Exception:
        pass
    try:  # Coinbase fallback: paginate ~3 days
        end = datetime.now(timezone.utc); cur = end - timedelta(days=3); out = []
        while cur < end:
            we = min(cur + timedelta(seconds=300 * 300), end)
            rr = requests.get("https://api.exchange.coinbase.com/products/BTC-USD/candles",
                              params={"granularity": 300, "start": cur.isoformat(),
                                      "end": we.isoformat()},
                              headers={"User-Agent": "dash"}, timeout=12)
            if rr.ok:
                out += rr.json()
            cur = we
        df = pd.DataFrame(out, columns=["t", "low", "high", "open", "close", "volume"])
        df["time"] = pd.to_datetime(df["t"], unit="s", utc=True)
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = pd.to_numeric(df[c])
        return df.set_index("time").sort_index()[
            ["open", "high", "low", "close", "volume"]], "Coinbase"
    except Exception:
        return None, None


@st.cache_data(ttl=60, show_spinner="Fetching live BTC data…")
def live_forward(cost_bps):
    df, src = fetch_live_candles()
    if df is None or len(df) < 100:
        return None
    sig = np.asarray(ee.ALL_STRATEGIES["composite_score"](df))
    res = ee.evaluate_spot(df, sig, cost_bps)
    eq = res["equity"]
    step = max(1, len(eq) // 2000)
    return {"src": src, "res": res, "signal": int(sig[-2]),
            "price": float(df["close"].iloc[-1]),
            "t0": df.index[0], "t1": df.index[-1], "equity": eq.iloc[::step]}


@st.cache_data(ttl=60, show_spinner=False)
def live_market():
    """Recent BTC price for the friendly Live tab: current price, 24h move, chart."""
    df, src = fetch_live_candles()
    if df is None or len(df) < 50:
        return None
    close = df["close"]
    last = float(close.iloc[-1])
    back24 = close.iloc[-min(288, len(close))]          # ~24h ago (288 5-min candles)
    window = close.iloc[-min(288, len(close)):]
    chart = close.iloc[-min(576, len(close)):]          # ~48h chart
    step = max(1, len(chart) // 1500)
    return {"src": src, "price": last,
            "chg24": (last / back24 - 1) * 100,
            "high24": float(window.max()), "low24": float(window.min()),
            "series": chart.iloc[::step]}


# ------------------------------ header ------------------------------------
st.title("🤖 Bitcoin Bot — Live")
st.caption("A bot making tiny **practice** bets on Bitcoin's next move with fake money — "
           "built to honestly test whether a strategy actually works before risking real cash. "
           "The **Live** tab is your home; the rest is the technical research behind it.")

# auto-refresh the page so live data stays current (every minute)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60_000, key="auto_refresh")
except Exception:
    pass

tab_live, tab_over, tab_btc, tab_wx, tab_search, tab_paper = st.tabs(
    ["🟢 Live", "Overview", "Strategy lab", "Weather", "Strategy search", "Bot details"])


# ================================ LIVE ====================================
with tab_live:
    st.caption("This bot makes tiny **practice** bets (fake money) on whether Bitcoin will tick "
               "up or down over the next 5 minutes — to test a strategy before anyone risks real "
               "cash. Here's what's happening right now (updates every minute).")

    mk = live_market()
    if mk is None:
        st.error("Couldn't reach a live price feed right now — it retries automatically.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("₿ Bitcoin price (live)", f"${mk['price']:,.0f}",
                  f"{mk['chg24']:+.2f}% (24h)")
        c2.metric("24h high", f"${mk['high24']:,.0f}")
        c3.metric("24h low", f"${mk['low24']:,.0f}")
        s = mk["series"]
        up = s.iloc[-1] >= s.iloc[0]
        pfig = go.Figure(go.Scatter(x=s.index, y=s.values, mode="lines",
                         line=dict(width=2, color="#16a34a" if up else "#dc2626")))
        pfig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10),
                           yaxis_title="USD")
        pfig.update_yaxes(range=[s.min() * 0.999, s.max() * 1.001])
        st.plotly_chart(pfig, use_container_width=True)
        st.caption(f"Live Bitcoin price, last ~{len(s)//12 or 1}h · source {mk['src']}.")

    st.divider()
    st.subheader("🤖 What the bot is doing right now")
    lf = live_forward(3.0)
    if lf is not None:
        sig = lf["signal"]
        if sig == 1:
            st.success("**Betting UP** — it thinks Bitcoin will tick **up** in the next 5 minutes.")
        elif sig == -1:
            st.error("**Betting DOWN** — it thinks Bitcoin will tick **down** in the next 5 minutes.")
        else:
            st.info("**Watching, not betting.** The bot is picky — it only bets when the price "
                    "looks unusually stretched. Most of the time (like now) it sits out. "
                    "That's on purpose — fewer, higher-quality bets.")

    st.divider()
    st.subheader("💰 Pretend-money scoreboard")
    stake = st.slider("Fake money to bet per play", 10, 1000, 100, 10, format="$%d")
    live_ledger = os.path.join(DATA, "live_ledger.csv")
    done = pd.DataFrame()
    if os.path.exists(live_ledger):
        ll = pd.read_csv(live_ledger, parse_dates=["entry_time", "resolve_time"])
        done = ll.dropna(subset=["pnl_bps"]).copy()
    START = 1000.0
    if len(done):
        done["dollars"] = done["pnl_bps"] / 10000 * stake
        done["balance"] = START + done["dollars"].cumsum()
        cur = float(done["balance"].iloc[-1])
        a, b, cc, d = st.columns(4)
        a.metric("Balance now", f"${cur:,.2f}", f"{cur - START:+,.2f}")
        b.metric("Plays made", f"{len(done)}")
        cc.metric("Won", f"{int((done['dollars'] > 0).sum())} / {len(done)}")
        d.metric("Started with", f"${START:,.0f}")
        bfig = go.Figure(go.Scatter(x=done["resolve_time"], y=done["balance"], mode="lines",
                         line=dict(width=2, color="#16a34a" if cur >= START else "#dc2626")))
        bfig.add_hline(y=START, line_dash="dash", line_color="#aaa")
        bfig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="USD")
        st.plotly_chart(bfig, use_container_width=True)
        st.caption("Fake money, real prices. The moves are small because the edge is small — "
                   "that's the honest reality this project is testing. Drag the slider to see how "
                   "a bigger bet size would scale it.")
        st.markdown("**Recent plays**")
        for _, r in done.tail(8)[::-1].iterrows():
            dirn = "UP" if r["signal"] == 1 else "DOWN"
            won = r["dollars"] > 0
            t = pd.Timestamp(r["resolve_time"]).strftime("%b %d, %I:%M %p")
            st.write(f"{'✅' if won else '❌'} {t} — bet **{dirn}**, "
                     f"{'won' if won else 'lost'} **${abs(r['dollars']):.2f}**")
    else:
        st.info("No completed plays yet. The bot is selective — it only bets a few times a day, "
                "and each bet takes 5 minutes to settle. This fills in over the coming hours.")

    st.divider()
    sp = os.path.join(DATA, "..", "reports", "state.json")
    rp = os.path.join(DATA, "..", "reports", "latest.md")
    if os.path.exists(sp):
        with open(sp) as f:
            ms = json.load(f)
        badge = {"none": "🟢", "watch": "🟡", "alert": "🔴"}.get(ms.get("alert_level"), "⚪")
        st.subheader(f"{badge} What the AI watchdog says")
        if os.path.exists(rp):
            with open(rp, encoding="utf-8") as f:
                st.markdown(f.read())
        st.caption(f"Written by Claude · {ms.get('updated','')} · refreshes a few times a day.")
    else:
        st.subheader("🤖 AI watchdog")
        st.info("Claude writes a plain-English assessment a few times a day — it'll appear here "
                "automatically once the monitor has run.")


# ============================== OVERVIEW ==================================
with tab_over:
    st.subheader("What we've collected")
    files = [
        ("btc_5m.parquet", "BTC 5m candles — Binance.US (2 yr)"),
        ("btc_5m_coinbase.parquet", "BTC 5m candles — Coinbase (1 yr, deep book)"),
        ("kalshi_kxhighny_60m.parquet", "Kalshi NYC high-temp markets + hourly prices"),
        ("obs_nyc_1min.parquet", "Central Park 1-minute temperature observations"),
    ]
    cols = st.columns(len(files))
    for c, (fn, desc) in zip(cols, files):
        df = load_parquet(f"{DATA}/{fn}")
        c.metric(desc.split(" — ")[0], f"{len(df):,}" if df is not None else "—",
                 help=desc)
        c.caption(desc)

    st.divider()
    st.markdown("""
**Findings so far (all honestly validated):**

| Strategy | Verdict | Barrier |
|---|---|---|
| BTC 5-min up/down (momentum / mean-reversion / RSI) | not viable | **Cost** — the edge is bid-ask bounce, 30–200× smaller than fees |
| Kalshi weather intraday-convergence | not viable on free data | **Data resolution** — 1–2°F buckets are finer than our ±1.5°F measurement |

The dashboard lets you re-run these yourself, slide the cost assumption, and watch
where thin edges appear and disappear. The **Edge search** tab holds the broader
automated hunt; **Paper trading** logs forward, out-of-sample results so we learn
from reality rather than from a curve-fit.
    """)


# ============================== BTC ======================================
with tab_btc:
    c1, c2, c3 = st.columns([1.2, 1.2, 2])
    venue = c1.selectbox("Venue", ["Binance.US", "Coinbase"])
    path = f"{DATA}/btc_5m.parquet" if venue == "Binance.US" \
        else f"{DATA}/btc_5m_coinbase.parquet"
    cost_bps = c2.slider("Cost per bet (bps, round-trip)", 0.0, 60.0, 5.0, 0.5,
                         help="Maker ~2-4 bps · Kraken taker ~52 · Coinbase taker ~120")
    df = load_parquet(path)
    if df is None:
        st.warning(f"Missing {path} — run fetch_data.py first.")
    else:
        lb = leaderboard(path, cost_bps)
        st.markdown(f"**Leaderboard** — {len(df):,} candles, "
                    f"{df.index[0]:%Y-%m-%d} → {df.index[-1]:%Y-%m-%d}. "
                    f"Sorted by out-of-sample net edge (`net_bps_test`).")
        show = lb.copy()
        for col in ["win_train", "win_test"]:
            if col in show:
                show[col] = show[col].map(fmt_pct)
        st.dataframe(show, use_container_width=True, hide_index=True)

        pick = c3.selectbox("Inspect a strategy",
                            [s for s in lb["strategy"] if s in ee.ALL_STRATEGIES])
        eq, res, cut_t = equity_for(path, pick, cost_bps)

        m = st.columns(4)
        m[0].metric("Win % (test)", fmt_pct(res["test"]["win"]))
        m[1].metric("Gross bps/bet (test)", f"{res['test']['gross_bps']:+.2f}")
        m[2].metric("Net bps/bet (test)", f"{res['test']['net_bps']:+.2f}",
                    help="After the cost slider. This is the number that matters.")
        m[3].metric("Bets (test)", f"{res['test']['bets']:,}")

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[.45, .55],
                            vertical_spacing=0.05,
                            subplot_titles=("BTC price", f"{pick} — cumulative net P&L (bps)"))
        pr = df["close"].iloc[::max(1, len(df)//4000)]
        fig.add_trace(go.Scatter(x=pr.index, y=pr.values, name="BTC",
                                 line=dict(width=1, color="#888")), row=1, col=1)
        color = "#16a34a" if res["test"]["net_bps"] > 0 else "#dc2626"
        fig.add_trace(go.Scatter(x=eq.index, y=eq.values, name="equity (bps)",
                                 line=dict(width=1.5, color=color)), row=2, col=1)
        fig.add_vline(x=cut_t, line_dash="dash", line_color="#3b82f6",
                      annotation_text="train ▸ test", row=2, col=1)
        fig.add_hline(y=0, line_color="#aaa", row=2, col=1)
        fig.update_layout(height=560, margin=dict(l=10, r=10, t=40, b=10),
                          legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The dashed line splits in-sample (left) from out-of-sample (right). "
                   "A real edge keeps climbing **after** the split. A flat/declining "
                   "right half = the in-sample slope was curve-fit or pure cost drag.")


# ============================== WEATHER ===================================
with tab_wx:
    mkt = load_parquet(f"{DATA}/kalshi_kxhighny_60m.parquet")
    obs = load_parquet(f"{DATA}/obs_nyc_1min.parquet")
    if mkt is None:
        st.warning("Missing Kalshi weather data — run fetch_kalshi_weather.py.")
    else:
        mkt = mkt.dropna(subset=["mid"]).copy()
        mkt["dt"] = pd.to_datetime(mkt["ts"], unit="s", utc=True)
        mkt["mdate"] = mkt["date"].map(parse_datecode)
        days = sorted(mkt["mdate"].unique())
        day = st.select_slider("Trading day", days, value=days[len(days)//2],
                               format_func=lambda d: d.strftime("%Y-%m-%d"))
        gd = mkt[mkt["mdate"] == day]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for tk, g in gd.groupby("ticker"):
            g = g.sort_values("dt")
            won = (g["result"].iloc[0] == "yes")
            fig.add_trace(go.Scatter(
                x=g["dt"], y=g["mid"], name=f"{g['lo'].iloc[0]:.0f}-{g['hi'].iloc[0]:.0f}°"
                + (" ✅" if won else ""),
                line=dict(width=3 if won else 1)), secondary_y=False)
        if obs is not None:
            obs = obs.copy()
            obs["local"] = pd.to_datetime(obs["valid"])
            od = obs[obs["local"].dt.date == day].sort_values("local")
            if not od.empty:
                od_utc = od["local"].dt.tz_localize("America/New_York").dt.tz_convert("UTC")
                fig.add_trace(go.Scatter(
                    x=od_utc, y=od["tmpf"].cummax(), name="running high °F",
                    line=dict(width=2, color="black", dash="dot")), secondary_y=True)
        fig.update_yaxes(title_text="market price (= P(bucket))", range=[0, 1],
                         secondary_y=False)
        fig.update_yaxes(title_text="temperature °F", secondary_y=True)
        fig.update_layout(height=480, margin=dict(l=10, r=10, t=30, b=10),
                          legend=dict(orientation="h"),
                          title=f"NYC high-temp buckets — {day:%Y-%m-%d} "
                                f"(✅ = settled winner)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Watch the winning bucket (bold) converge to $1 as the day's running "
                   "high (dotted) locks in. The strategy question: does the price lag the "
                   "thermometer enough to beat costs? Diagnostics say no — buckets are "
                   "finer than free data can resolve.")

        # resolution diagnostic
        st.markdown("**Resolution barrier** — can free data even place the high in the right bucket?")
        rows = []
        for feed, fpath in [("Hourly METAR", f"{DATA}/obs_nyc.parquet"),
                            ("1-minute ASOS", f"{DATA}/obs_nyc_1min.parquet")]:
            o = load_parquet(fpath)
            if o is None:
                continue
            o = o.copy(); o["valid"] = pd.to_datetime(o["valid"]); o["d"] = o["valid"].dt.date
            errs = []
            for d, g in mkt.groupby("mdate"):
                yes = g[g["result"] == "yes"]; od = o[o["d"] == d]
                if yes.empty or od.empty:
                    continue
                yb = yes.iloc[0]; mx = od["tmpf"].max()
                hit = in_bucket(mx, yb["lo"], yb["hi"], yb["kind"])
                errs.append(hit)
            if errs:
                rows.append({"feed": feed, "days": len(errs),
                             "exact bucket hit": f"{np.mean(errs)*100:.1f}%"})
        if rows:
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


# ============================== SEARCH ====================================
with tab_search:
    sp = f"{DATA}/search_results.json"
    if not os.path.exists(sp):
        st.info("No search results yet. The automated edge-search writes "
                "`data/search_results.json`. Once it runs, the leaderboard appears here.")
    else:
        with open(sp) as f:
            res = json.load(f)
        rows = res.get("results", [])
        st.caption(f"Edge search — {res.get('generated','')} · "
                   f"{res.get('n_tested', len(rows))} hypotheses tested · "
                   f"bar: {res.get('bar','')}")

        # best candidate = highest worst-venue gross (breakeven cost)
        scored = [r for r in rows if "min_net_2bps" in r and not r.get("error")]
        scored.sort(key=lambda r: r.get("min_net_2bps", -1e9), reverse=True)
        if scored:
            best = scored[0]
            breakeven = best["min_net_2bps"] + 2.0   # gross = net + cost
            c = st.columns(4)
            c[0].metric("Best candidate", best["strategy"])
            c[1].metric("Worst-venue net @2bps", f"{best['min_net_2bps']:+.2f}")
            c[2].metric("Breakeven cost", f"~{breakeven:.1f} bps",
                        help="Gross edge on the weaker venue. Below this round-trip "
                             "cost it is net-positive OOS on BOTH venues.")
            c[3].metric("Clears 5 bps bar?",
                        "yes" if best.get("survives") else "no")
            if breakeven > 2:
                st.info(f"**{best['strategy']}** is the closest to a real edge: "
                        f"net-positive out-of-sample on *both* venues at ≤2 bps "
                        f"(breakeven ≈ {breakeven:.1f} bps), so it's **not** a "
                        f"bid-ask-bounce artifact. But ~{breakeven:.1f} bps is still "
                        f"below realistic retail crypto round-trip costs (~10–40 bps), "
                        f"so it isn't net-profitable *yet*. It's being forward-tested "
                        f"in the **Paper trading** tab.")

        surv5 = [r for r in rows if r.get("survives")]
        # test-positive on BOTH venues at an optimistic 2 bps (out-of-sample)
        cand2 = [r for r in rows if r.get("min_net_2bps", -1e9) > 0]
        # the strict bar also needs in-sample agreement on both venues
        strict2 = [r for r in rows if r.get("survives_2bps") and not r.get("lookahead_flag")]
        if surv5:
            st.success(f"{len(surv5)} strategy(ies) clear the strict 5 bps bar.")
        elif cand2:
            st.warning(f"0 clear the 5 bps bar. **{len(cand2)}** are net-positive "
                       f"*out-of-sample* on both venues at an optimistic 2 bps — real, "
                       f"but thin. None ({len(strict2)}) also clear the bar *in-sample* "
                       f"on the deep venue, so even these are marginal. The honest "
                       f"frontier is **driving cost below ~4 bps**, not finding more signal.")
        else:
            st.warning("No strategy is net-positive cross-venue even at 2 bps. "
                       "Honest result — the hunt continues.")

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ============================== PAPER =====================================
with tab_paper:
    # --- AI monitor assessment (written by the GitHub Actions monitor) ---
    state_path = os.path.join(DATA, "..", "reports", "state.json")
    report_path = os.path.join(DATA, "..", "reports", "latest.md")
    if os.path.exists(state_path):
        with open(state_path) as f:
            mstate = json.load(f)
        badge = {"none": "🟢", "watch": "🟡", "alert": "🔴"}.get(mstate.get("alert_level"), "⚪")
        st.subheader(f"{badge} AI monitor")
        if mstate.get("alert_level") == "alert":
            st.error(f"**ALERT:** {mstate.get('alert_message','')}")
        elif mstate.get("alert_level") == "watch":
            st.warning(f"**WATCH:** {mstate.get('alert_message','')}")
        if os.path.exists(report_path):
            with st.expander(f"📋 {mstate.get('headline','Latest assessment')}",
                             expanded=True):
                with open(report_path, encoding="utf-8") as f:
                    st.markdown(f.read())
        st.caption(f"Written by Claude ({mstate.get('model','')}) · {mstate.get('updated','')} "
                   "· runs automatically a few times a day.")
        st.divider()

    # --- persisted forward ledger (committed by GitHub Actions — no PC) ---
    live_ledger = os.path.join(DATA, "live_ledger.csv")
    if os.path.exists(live_ledger):
        ll = pd.read_csv(live_ledger, parse_dates=["entry_time", "resolve_time"])
        done = ll.dropna(subset=["pnl_bps"])
        st.subheader("Persisted forward ledger (serverless, no PC)")
        cc = st.columns(4)
        cc[0].metric("Logged trades", f"{len(ll):,}")
        cc[1].metric("Resolved", f"{len(done):,}")
        if len(done):
            cc[2].metric("Win %", fmt_pct((done["pnl_bps"] > 0).mean()))
            cc[3].metric("Net bps/trade", f"{done['pnl_bps'].mean():+.2f}")
            eqfig = go.Figure(go.Scatter(x=done["resolve_time"], y=done["pnl_bps"].cumsum(),
                              line=dict(width=2,
                                        color="#16a34a" if done["pnl_bps"].mean() > 0 else "#dc2626")))
            eqfig.add_hline(y=0, line_color="#aaa")
            eqfig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10),
                                title="Forward equity (bps) — accumulated by GitHub Actions")
            st.plotly_chart(eqfig, use_container_width=True)
        else:
            st.caption("Ledger created; waiting for the first trades to resolve "
                       "(composite_score is selective, so this fills slowly).")
        st.divider()

    st.subheader("Live forward test — composite_score")
    st.caption("Recomputed from the latest **real** BTC 5-minute data on every refresh "
               "(the cloud fetches it directly — no PC required). The strategy uses fixed "
               "rules built on older data, so this recent window is out-of-sample. "
               "Page auto-refreshes every 5 minutes.")
    lf = live_forward(3.0)
    if lf is None:
        st.error("Couldn't reach a live BTC data source right now — it retries on the "
                 "next refresh.")
    else:
        allp = lf["res"]["all"]
        sigtxt = {1: "▲ betting UP", -1: "▼ betting DOWN",
                  0: "— no bet right now"}[lf["signal"]]
        c = st.columns(5)
        c[0].metric("Live signal", sigtxt)
        c[1].metric("BTC price", f"${lf['price']:,.0f}")
        c[2].metric("Trades in window", f"{allp['bets']:,}")
        c[3].metric("Win %", fmt_pct(allp["win"]))
        c[4].metric("Net bps/trade", f"{allp['net_bps']:+.2f}",
                    help="At 3 bps assumed cost. Positive = edge holding on live data.")
        eq = lf["equity"]
        color = "#16a34a" if allp["net_bps"] > 0 else "#dc2626"
        fig = go.Figure(go.Scatter(x=eq.index, y=eq.values,
                                   line=dict(width=2, color=color)))
        fig.add_hline(y=0, line_color="#aaa")
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=34, b=10),
                          title=f"Live rolling equity (bps) · {lf['src']} · "
                                f"{lf['t0']:%b %d %H:%M} → {lf['t1']:%b %d %H:%M} UTC")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Small sample — `composite_score` is selective (~1–2% of candles), so "
                   "single-window numbers are noisy. The signal is worth ~4 bps gross; net "
                   "depends entirely on keeping trading cost low.")

    # persisted local ledger — only present when your PC's scheduled task is running
    lp = os.path.join(DATA, "paper_ledger.csv")
    if os.path.exists(lp):
        st.divider()
        st.subheader("Persisted ledger (from your PC's scheduled task)")
        led = pd.read_csv(lp, parse_dates=["entry_time", "resolve_time"])
        done = led.dropna(subset=["pnl_bps"])
        cc = st.columns(3)
        cc[0].metric("Logged trades", f"{len(led):,}")
        cc[1].metric("Resolved", f"{len(done):,}")
        if len(done):
            cc[2].metric("Net bps/trade", f"{done['pnl_bps'].mean():+.2f}")
        st.dataframe(led.tail(30), use_container_width=True, hide_index=True)
