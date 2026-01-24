import streamlit as st
import pandas as pd
from tools.lstm_model import fullmodel
from tools.market import get_market_data,options_map,period_options

st.warning(
"⚠️ **Market Volatility Warning**\n\n"
"Stock markets are inherently volatile and influenced by unpredictable economic, political, and global factors.\n\n"
"The predictions shown here are **best suited for short-term analysis only**, ideally for a period of **7–14 days*.\n\n"
"These forecasts should not be considered financial advice and are intended for educational purposes only."
)

category = st.selectbox("Select Category", options_map.keys())
market_name = st.selectbox("Select Market", options_map[category].keys())
ticker = options_map[category][market_name]
period = st.selectbox("Select Period", period_options.keys())

st.caption(f"Using historical data: **{period_options[period]}**")

prediction_days = st.slider(
"Prediction Horizon (days)",
min_value=7,
max_value=14,
value=7
)   

st.caption(f"Forecasting of {market_name} for **{prediction_days} days** ahead")

if st.button("Run Forecast"):
    with st.spinner("Running LSTM model..."):
        data = get_market_data(ticker, period_options[period])
        old_data, new_data = fullmodel(data)
        full_df = pd.concat([old_data,new_data])
    st.success("Forecast completed ✔️")
    st.line_chart(full_df) 