import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import linregress

metrics_lst=[
    "Log Return",
    "Support",
    "Resistance",
    "Rolling Extereme",
    "Rate Of Change (Daily)",
    "Rate Of Change (Weekly)",
    "Rate Of Change (Monthly)",
    "Volitility",
    "Volitility Ratio",
    "Moving Average Distance",
    "Moving Average Slope",
    "Moving Average Convergence Divergence (MACD)",
    "Moving Average Convergence Divergence (Single Line)",
    "Moving Average Convergence Divergence (Histogram)"
]

def log_ret(close):
    return np.log(close / close.shift(1))

def support_n_resistance(close):
    return close.rolling(20).max(), close.rolling(20).min()

def rolling_etx(close):
    support, resistance = support_n_resistance(close)
    return (close - resistance) / (support - resistance)

def ROC(close,n):
    return close.pct_change(n)

def MAS(close):
    ma = close.rolling(20).mean()
    ma_slope = ma.diff()
    return ma_slope

def MAD(close):
    ma_short = close.rolling(20).mean()
    ma_long = close.rolling(50).mean()
    return (ma_short - ma_long) / (ma_long + 1e-8)

def vol(close, window=20):
    returns = close.pct_change()
    return returns.rolling(window).std()

def vol_ratio(close):
    short_window = 20
    long_window = 50

    returns = close.pct_change()
    vol_short = returns.rolling(short_window).std()
    vol_long = returns.rolling(long_window).std()

    return vol_short / (vol_long + 1e-8)

def MACD(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()

    macd = ema_fast - ema_slow
    single_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - single_line

    return macd, single_line, hist