INTERPRETATIONS = {

    "Log Return": {
        "stable": "Log returns are tightly distributed around zero, indicating stable price behavior with no strong directional bias.",
        "volatile": "Log returns show wide dispersion, reflecting increased uncertainty and elevated short-term risk."
    },

    "Support": {
        "near": "Price is trading close to support, suggesting potential downside exhaustion or bounce conditions.",
        "broken": "Price has moved below support, indicating a possible bearish breakdown.",
        "neutral": "Price is comfortably above support, indicating no immediate downside pressure."
    },

    "Resistance": {
        "near": "Price is trading close to resistance, indicating possible supply pressure or profit-taking.",
        "broken": "Price has broken above resistance, suggesting bullish continuation potential.",
        "neutral": "Price remains below resistance with no immediate breakout signal."
    },

    "Rolling Extereme": {
        "new_high": "Price is registering a rolling high, indicating strong bullish momentum or breakout conditions.",
        "new_low": "Price is registering a rolling low, signaling bearish pressure or downside breakout risk.",
        "neutral": "Price remains within recent extremes, indicating consolidation."
    },

    "Rate Of Change (Daily)": {
        "low": "Daily Rate of Change is close to zero, indicating weak short-term momentum and mean-reverting behavior.",
        "positive": "Positive daily Rate of Change indicates short-term upward momentum.",
        "negative": "Negative daily Rate of Change reflects short-term downward momentum.",
        "shock": "Extreme daily Rate of Change suggests abnormal market movement driven by external events."
    },

    "Rate Of Change (Weekly)": {
        "low": "Weekly Rate of Change is muted, indicating lack of sustained momentum.",
        "positive": "Positive weekly Rate of Change reflects medium-term bullish momentum.",
        "negative": "Negative weekly Rate of Change reflects medium-term bearish momentum.",
        "shock": "Extreme weekly Rate of Change indicates strong momentum or structural price shift."
    },

    "Rate Of Change (Monthly)": {
        "low": "Monthly Rate of Change is weak, indicating long-term consolidation.",
        "positive": "Positive monthly Rate of Change suggests long-term bullish trend.",
        "negative": "Negative monthly Rate of Change suggests long-term bearish trend.",
        "shock": "Extreme monthly Rate of Change signals a major long-term regime change."
    },

    "Volitility": {
        "low": "Low volatility indicates market stability and reduced uncertainty.",
        "high": "Elevated volatility reflects increased risk and unstable price behavior.",
        "clustered": "Volatility clustering suggests regime-dependent risk rather than random price movement."
    },

    "Volitility Ratio": {
        "expanding": "Volatility ratio above normal levels indicates expanding risk and possible regime transition.",
        "contracting": "Volatility contraction suggests normalization following a high-risk period.",
        "neutral": "Volatility ratio remains stable, indicating no significant regime change."
    },

    "Moving Average Distance": {
        "trend_strong": "Price is far from its moving average, indicating a strong directional trend.",
        "trend_weak": "Price is close to its moving average, suggesting weak or no trend."
    },

    "Moving Average Slope": {
        "uptrend": "Positive moving average slope indicates a sustained upward trend.",
        "downtrend": "Negative moving average slope suggests a sustained downward trend.",
        "flat": "Flat moving average slope indicates sideways movement or trend exhaustion."
    },

    "Moving Average Convergence Divergence (MACD)": {
        "bullish": "MACD above the signal line indicates bullish momentum.",
        "bearish": "MACD below the signal line reflects bearish momentum.",
        "neutral": "MACD near equilibrium suggests weak or transitioning momentum."
    },

    "Moving Average Convergence Divergence (Single Line)": {
        "positive": "MACD line above zero indicates overall bullish momentum.",
        "negative": "MACD line below zero indicates overall bearish momentum.",
        "neutral": "MACD line near zero suggests absence of strong momentum."
    },

    "Moving Average Convergence Divergence (Histogram)": {
        "expanding": "Expanding MACD histogram indicates strengthening momentum.",
        "contracting": "Contracting MACD histogram signals weakening momentum.",
        "neutral": "Flat MACD histogram suggests momentum equilibrium."
    }
}


def interpret_log_return(series):
    if series.std() > series.mean() * 3:
        return "volatile"
    return "stable"

def interpret_support(series,price):
    support = series.iloc[-1]
    dist = abs(price - support) / price

    if dist < 0.01:
        return "near"
    elif price < support:
        return "broken"
    return "neutral"

def interpret_resistance(series,price):
    resistance = series.iloc[-1]
    dist = abs(resistance - price) / price

    if dist < 0.01:
        return "near"
    elif price > resistance:
        return "broken"
    return "neutral"


def interpret_rolling_extreme(series):
    v = series.iloc[-1]

    if v >= series.max():
        return "new_high"
    elif v <= series.min():
        return "new_low"
    return "neutral"


def interpret_roc(roc_series):
    latest = roc_series.iloc[-1]

    if abs(latest) > 0.08:
        return "shock"
    elif latest > 0:
        return "positive"
    elif latest < 0:
        return "negative"
    return "low"

def interpret_volatility(vol_series):
    recent = vol_series.iloc[-1]
    mean = vol_series.mean()

    if recent > 2 * mean:
        return "high"
    elif vol_series.autocorr() > 0.5:
        return "clustered"
    return "low"

def interpret_vol_ratio(vol_ratio_series):
    latest = vol_ratio_series.iloc[-1]

    if latest > 1.5:
        return "expanding"
    elif latest < 0.7:
        return "contracting"
    return "neutral"

def interpret_mad(mad_series):
    if abs(mad_series.iloc[-1]) > mad_series.std():
        return "trend_strong"
    return "trend_weak"

def interpret_mas(mas_series):
    latest = mas_series.iloc[-1]

    if latest > 0:
        return "uptrend"
    elif latest < 0:
        return "downtrend"
    return "flat"

def interpret_macd(macd, signal):
    diff = macd.iloc[-1] - signal.iloc[-1]

    if diff > 0:
        return "bullish"
    elif diff < 0:
        return "bearish"
    return "neutral"

def interpret_macd_single(series):
    v = series.iloc[-1]

    if v > 0:
        return "positive"
    elif v < 0:
        return "negative"
    return "neutral"


def interpret_macd_hist(hist):
    delta = hist.diff().iloc[-1]

    if delta > 0:
        return "expanding"
    elif delta < 0:
        return "contracting"
    return "neutral"

FN_METRIC_MAP = {

    "Log Return": interpret_log_return,

    "Support": interpret_support,

    "Resistance": interpret_resistance,

    "Rolling Extereme": interpret_rolling_extreme,

    "Rate Of Change (Daily)": interpret_roc,
    "Rate Of Change (Weekly)": interpret_roc,
    "Rate Of Change (Monthly)": interpret_roc,

    "Volitility": interpret_volatility,

    "Volitility Ratio": interpret_vol_ratio,

    "Moving Average Distance": interpret_mad,

    "Moving Average Slope": interpret_mas,

    "Moving Average Convergence Divergence (MACD)": interpret_macd,

    "Moving Average Convergence Divergence (Single Line)": interpret_macd_single,

    "Moving Average Convergence Divergence (Histogram)": interpret_macd_hist
}

def interpret_metric(metric_name, series, price=0):
    fn = FN_METRIC_MAP[metric_name]
    regime = fn(series, price=0)
    return INTERPRETATIONS[metric_name][regime]
