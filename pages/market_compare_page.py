import streamlit as st 
import yfinance as yf
import pandas as pd
from currency_converter import CurrencyConverter
from pages.tools.market import get_market_data, options_map, period_options 

st.title("Market Dashboard")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Market A")
    category1 = st.selectbox("Select Category", options_map.keys(), key="cat1")
    market1 = st.selectbox("Select Market", options_map[category1].keys(), key="market1")
    period1 = st.selectbox("Select Period", period_options.keys(), key="period1")
    

with col2:
    st.subheader("Market B")
    category2 = st.selectbox("Select Category", options_map.keys(), key="cat2")
    market2 = st.selectbox("Select Market", options_map[category2].keys(), key="market2")
    period2 = st.selectbox("Select Period", period_options.keys(), key="period2")

_, center, _ = st.columns((1, 0.5, 1))
c = CurrencyConverter()
selected_currency=None
with center:
    if st.button("Comparison Graphs"):
        ticker1 = options_map[category1][market1]
        data1 = get_market_data(ticker1, period=period_options[period1])
        ticker_obj1 = yf.Ticker(ticker1)
        info1 = ticker_obj1.info
        currency1 = info1.get('currency')
        
        st.session_state['currency1'] = currency1
        st.session_state['data1'] = data1
        st.session_state['mkt1_name'] = market1
        
        ticker2 = options_map[category2][market2]
        data2 = get_market_data(ticker2, period=period_options[period2])
        ticker_obj2 = yf.Ticker(ticker2)
        info2 = ticker_obj2.info
        currency2 = info2.get('currency')
        
        st.session_state['currency2'] = currency2
        st.session_state['data2'] = data2
        st.session_state['mkt2_name'] = market2

if 'currency1' in st.session_state and 'currency2' in st.session_state:
    currency1 = st.session_state['currency1']
    currency2 = st.session_state['currency2']
    
    currency_options = sorted(list(set([
        currency1, currency2, 
        "USD", "EUR", "GBP", "INR", "CAD", "JPY", 
        "HKD", "CNY", "AUD", "BRL", "ZAR"
    ])))

    selected_currency = st.selectbox(
        "Select the Currency for the chart:",
        currency_options
    )    

    st.write(f"## Comparison in {selected_currency}")

    try:
        rate1 = float(c.convert(1, currency1, selected_currency))
        rate2 = float(c.convert(1, currency2, selected_currency))
    except:
        rate1, rate2 = 1.0, 1.0

    mode = st.selectbox(
        "Comparison Mode",
        [
            "Absolute Price",
            "Normalized (Base = 100)",
            "Percentage Change (%)"
        ]
    )

    df1 = st.session_state['data1'][['Close']] * rate1
    df2 = st.session_state['data2'][['Close']] * rate2

    df1.columns = [st.session_state['mkt1_name']]
    df2.columns = [st.session_state['mkt2_name']]

    df_final = pd.concat([df1, df2], axis=1)
    df_final = df_final.sort_index().ffill().bfill()

    if mode == "Normalized (Base = 100)":
        df_final = (df_final / df_final.iloc[0]) * 100
        st.caption("Prices normalized to 100 at the starting point")

    elif mode == "Percentage Change (%)":
        df_final = df_final.pct_change() * 100
        st.caption("Percentage change from previous period")

    else:
        st.caption(f"Absolute prices in {selected_currency}")

    st.line_chart(df_final, color=["#FF0000", "#FFD700"])

