"""
autocorr_lagged.py — family: autocorrelation / lagged-return structure.

Hypothesis space: 5-minute BTC returns carry weak linear structure (sign
persistence or sign reversal) that can be read from the autocorrelation of the
return series and from weighted sums of recent returns. If a real (capturable)
edge exists, it must survive on BOTH a thin book (Binance.US) and a deep book
(Coinbase) — pure bid-ask bounce shows up as strong lag-1 negative autocorr on
the thin book and evaporates on the deep one, so the cross-venue filter is the
honest test.

All signals are strictly causal: signal[i] uses returns through row i only.
We use df["close"].diff() (== close[i]-close[i-1], a PAST quantity at row i),
rolling/expanding windows, and .shift(+k). The evaluator forms the outcome as
close.shift(-1)/close-1, which we never touch.

STRATEGIES exposed:
  ac_lag1_adaptive   — trade lag-1 autocorr sign, direction learned causally
  ac_lag_combo       — combine sign of several lag autocorrelations (PACF-ish)
  weighted_momo_sign — sign of exponentially-weighted sum of last-k returns
  pacf_resid_lag2    — lag-2 signal on the part of r not explained by lag-1
  ac_regime_switch   — momentum vs mean-revert chosen by recent lag-1 autocorr
  ar1_forecast_sign  — sign of a rolling AR(1) one-step forecast of the return
"""
import numpy as np
import pandas as pd


def _ret(df):
    """Past log-ish return at each row: r[i] = close[i] - close[i-1] (known at i)."""
    return df["close"].diff()


def _logret(df):
    return np.log(df["close"]).diff()


def _causal_autocorr(r, lag, win):
    """
    Rolling Pearson autocorrelation of series r at the given lag, computed over
    a trailing window of `win` points and ENDING at each row (causal).
    Returns a pd.Series aligned to r.index. Value at row i uses r[i] and earlier.
    """
    r0 = r
    rl = r.shift(lag)
    # rolling mean / std over trailing window (min_periods keeps it causal-safe)
    mp = max(win // 2, 10)
    m0 = r0.rolling(win, min_periods=mp).mean()
    ml = rl.rolling(win, min_periods=mp).mean()
    cov = (r0 * rl).rolling(win, min_periods=mp).mean() - m0 * ml
    s0 = r0.rolling(win, min_periods=mp).std()
    sl = rl.rolling(win, min_periods=mp).std()
    denom = (s0 * sl).replace(0.0, np.nan)
    return cov / denom


# ---------------------------------------------------------------------------
# 1. Lag-1 autocorrelation, adaptive direction.
#    If recent returns are positively autocorrelated, follow the last move
#    (momentum); if negatively autocorrelated, fade it (mean-revert). The
#    autocorr is measured on a trailing window, so the rule adapts causally.
# ---------------------------------------------------------------------------
def ac_lag1_adaptive(df, win=288):
    r = _ret(df)
    ac1 = _causal_autocorr(r, 1, win)
    last = np.sign(r).fillna(0.0)
    # follow when ac1>0, fade when ac1<0
    direction = np.sign(ac1).fillna(0.0)
    sig = (direction * last)
    return np.sign(sig).fillna(0.0).astype(int).values


# ---------------------------------------------------------------------------
# 2. Combination of several lag autocorrelations (a crude PACF read).
#    Build a score = sum_k acf_k * sign(r[i-k+1]) i.e. each lag votes in the
#    direction its own autocorrelation implies, weighted by autocorr strength.
# ---------------------------------------------------------------------------
def ac_lag_combo(df, win=288, lags=(1, 2, 3)):
    r = _ret(df)
    score = pd.Series(0.0, index=df.index)
    for lag in lags:
        ac = _causal_autocorr(r, lag, win)
        # the return that lag relates the *next* step to is r shifted by (lag-1)
        contrib = ac.fillna(0.0) * np.sign(r.shift(lag - 1)).fillna(0.0)
        score = score + contrib
    return np.sign(score).fillna(0.0).astype(int).values


# ---------------------------------------------------------------------------
# 3. Sign of an exponentially weighted sum of the last k returns.
#    A weighted-momentum / weighted-reversal read: recent returns weigh more.
#    Sign of the EWMA of returns -> momentum direction.
# ---------------------------------------------------------------------------
def weighted_momo_sign(df, span=12):
    r = _ret(df)
    ew = r.ewm(span=span, adjust=False, min_periods=span).mean()
    return np.sign(ew).fillna(0.0).astype(int).values


# ---------------------------------------------------------------------------
# 4. PACF-style lag-2 signal: regress out lag-1 dependence, trade the residual
#    relationship at lag 2. We approximate the partial autocorr by using the
#    sign of r two steps back, gated by a causal lag-2 autocorr estimate that
#    is itself adjusted for the lag-1 autocorr (Yule-Walker 2-term).
# ---------------------------------------------------------------------------
def pacf_resid_lag2(df, win=288):
    r = _ret(df)
    a1 = _causal_autocorr(r, 1, win)
    a2 = _causal_autocorr(r, 2, win)
    # partial autocorr at lag 2 (Yule-Walker): (a2 - a1^2) / (1 - a1^2)
    denom = (1.0 - a1 * a1).replace(0.0, np.nan)
    pac2 = (a2 - a1 * a1) / denom
    direction = np.sign(pac2).fillna(0.0)
    contrib = direction * np.sign(r.shift(1)).fillna(0.0)  # r two-steps-ago vs next
    return np.sign(contrib).fillna(0.0).astype(int).values


# ---------------------------------------------------------------------------
# 5. Regime switch: pick momentum or mean-reversion based on whether the
#    trailing lag-1 autocorrelation is currently above/below zero by a margin.
#    Only bet when the regime is clear (|ac1| over a threshold).
# ---------------------------------------------------------------------------
def ac_regime_switch(df, win=288, thresh=0.05):
    r = _ret(df)
    ac1 = _causal_autocorr(r, 1, win)
    last = np.sign(r).fillna(0.0)
    sig = pd.Series(0.0, index=df.index)
    mom = ac1 > thresh          # follow last move
    rev = ac1 < -thresh         # fade last move
    sig = sig.mask(mom, last)
    sig = sig.mask(rev, -last)
    return np.sign(sig).fillna(0.0).astype(int).values


# ---------------------------------------------------------------------------
# 6. Rolling AR(1) one-step forecast: forecast r_next = phi * r_now using a
#    causal rolling estimate of phi (= lag-1 autocorr scaled by vol ratio,
#    which for equal-vol windows is just the lag-1 autocorrelation). Bet the
#    sign of the forecast.
# ---------------------------------------------------------------------------
def ar1_forecast_sign(df, win=288):
    r = _ret(df)
    a1 = _causal_autocorr(r, 1, win)
    forecast = a1.fillna(0.0) * r          # phi * r_now
    return np.sign(forecast).fillna(0.0).astype(int).values


STRATEGIES = {
    "ac_lag1_adaptive": ac_lag1_adaptive,
    "ac_lag_combo": ac_lag_combo,
    "weighted_momo_sign": weighted_momo_sign,
    "pacf_resid_lag2": pacf_resid_lag2,
    "ac_regime_switch": ac_regime_switch,
    "ar1_forecast_sign": ar1_forecast_sign,
}
