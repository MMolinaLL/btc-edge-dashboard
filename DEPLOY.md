# Deploy the dashboard to Streamlit Community Cloud (free, always-on)

The repo is already committed locally. You just need to put it on GitHub, then
point Streamlit Cloud at it. ~10 minutes. No API keys or secrets required — the
app fetches public BTC data itself, so it stays live **without your PC on**.

> Heads-up: the free tier needs a **public** repo, so the code + the bundled
> price data become publicly viewable. There are no secrets in here (just public
> market data and research), so that's fine — but know it before you push.

## 1. Put the code on GitHub

1. Make a free account at <https://github.com> if you don't have one.
2. Click **+ → New repository**. Name it e.g. `btc-edge-dashboard`, set it
   **Public**, do **NOT** add a README/.gitignore (we already have them), Create.
3. GitHub shows a URL like `https://github.com/YOURNAME/btc-edge-dashboard.git`.
   In a terminal, from `C:\Users\MatMolina\CODE STUFF\btc-bot`, run:

   ```powershell
   git remote add origin https://github.com/YOURNAME/btc-edge-dashboard.git
   git push -u origin main
   ```

   The first push opens a browser to log into GitHub — approve it once. (If it
   asks on the command line instead, a GitHub Personal Access Token works as the
   password.)

## 2. Deploy on Streamlit Cloud

1. Go to <https://share.streamlit.io> and **Sign in with GitHub**.
2. Click **Create app → Deploy a public app from GitHub**.
3. Fill in:
   - **Repository:** `YOURNAME/btc-edge-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**. First build takes ~2–4 minutes (installing packages +
   loading the data). You'll get a public URL like
   `https://YOURNAME-btc-edge-dashboard.streamlit.app`.

That URL is your live webpage. Share it, open it on your phone, anything.

## What's live vs. static on the hosted site

- **Live (recomputed every load, ~5-min auto-refresh):** the *Paper trading* tab —
  the cloud fetches recent real BTC candles (Coinbase/Binance.US) and re-runs
  `composite_score`. No PC required.
- **Static (from the bundled data):** BTC backtest leaderboard, weather-market
  convergence, the edge-search results. These don't change unless you re-run the
  fetch scripts locally and `git push` updated data.

## Updating the site later

```powershell
git add -A
git commit -m "update data / app"
git push
```
Streamlit Cloud auto-redeploys on every push to `main`.

## Notes

- Free apps **sleep after inactivity** and wake on the next visit (a few seconds).
- Your local `BTC-PaperTrader` scheduled task keeps building the *persisted*
  ledger on your PC; the hosted site shows the *live recomputed* view instead, so
  the two are independent and neither needs the other.
