import streamlit as st 
from time import sleep
from tools.market import get_market_data, options_map, period_options
from tools.metrics import log_ret, support_n_resistance, rolling_etx, ROC, MAS

st.title("Market Dashboard")

if 'charts' not in st.session_state:
    st.session_state.charts = []

with st.expander("Add New Market Chart", expanded=True):
    category = st.selectbox("Select Category", options_map.keys())
    market_name = st.selectbox("Select Market", options_map[category].keys())
    ticker = options_map[category][market_name]
    period = st.selectbox("Select Period", period_options.keys())

    if st.button("Add to Dashboard"):
        new_chart = {
            "name": market_name,
            "ticker": ticker,
            "period": period_options[period],
            "period_label": period
        }
        st.session_state.charts.append(new_chart)

if st.button("Clear All Charts"):
    st.session_state.charts = []
    st.rerun()

st.divider()

for idx, chart_info in enumerate(st.session_state.charts):
    data = get_market_data(chart_info['ticker'], period=chart_info['period'])
    row , col = data.shape

    st.subheader(f"{chart_info['name']} ({chart_info['period_label']})")
    st.line_chart(data['Close'])
    
    remove_col , info_col, forecast_col =st.columns((1,3.5,0.9))
    with remove_col:
        if st.button(f"Remove {chart_info['name']}",key=f"rembtn_{chart_info['ticker']}_{idx}"):
            st.session_state.charts.pop(idx)
            st.session_state["market_name"]=None
            st.session_state["market_ticker"]=None
            st.session_state["market_period"]=None
            st.rerun()

    with info_col:
        if st.button("View Quant Metrics",key=f"infobtn_{chart_info['ticker']}_{idx}"):
            st.session_state["market_name"] = chart_info["name"]
            st.session_state["market_ticker"] = chart_info["ticker"]
            st.session_state["market_period"] = chart_info["period"]   
            
            st.write("Redirecting...")
            st.switch_page("pages/metrics_page.py")
    
    with forecast_col:
        if st.button("Forecast the Market", key=f"for   tn_{chart_info['ticker']}_{idx}"):
            st.session_state["market_name"] = chart_info["name"]
            st.session_state["market_ticker"] = chart_info["ticker"]
            st.session_state["market_period"] = chart_info["period"]

            st.write("Redirecting...")
            st.switch_page("pages/forecasting_page.py")