import streamlit as st 
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from tools.market import get_market_data, options_map, period_options 

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

_, center, _ = st.columns((1, 0.5   , 1))
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

st.divider()
res_col1, res_col2 = st.columns(2)

if 'currency1' in st.session_state and 'currency2' in st.session_state:

    mkt1 = st.session_state['mkt1_name']
    mkt2 = st.session_state['mkt2_name']
    cur1 = st.session_state['currency1']
    cur2 = st.session_state['currency2']

    df1 = st.session_state['data1'][['Close']].rename(columns={'Close': mkt1})
    df2 = st.session_state['data2'][['Close']].rename(columns={'Close': mkt2})

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df1.index,
            y=df1[mkt1],
            name=f"{mkt1} ({cur1})",
            yaxis="y1",
            line=dict(color="#FF0000", width=2)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df2.index,
            y=df2[mkt2],
            name=f"{mkt2} ({cur2})",
            yaxis="y2",
            line=dict(color="#FFD700", width=2)
        )
    )

    fig.update_layout(
        title="Market Comparison",
        xaxis=dict(title="Date"),
        yaxis=dict(
            title=f"{mkt1} ({cur1})",
            side="left"
        ),
        yaxis2=dict(
            title=f"{mkt2} ({cur2})",
            overlaying="y",
            side="right"
        ),
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)
