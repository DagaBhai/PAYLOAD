import streamlit as st 
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

_, center, _ = st.columns((1, 0.5   , 1))
with center:
    if st.button("Comparison Graphs"):
            ticker1 = options_map[category1][market1]
            data1 = get_market_data(ticker1, period=period_options[period1])
            st.session_state['data1'] = data1
            st.session_state['mkt1_name'] = market1
            ticker2 = options_map[category2][market2]
            data2 = get_market_data(ticker2, period=period_options[period2])
            st.session_state['data2'] = data2
            st.session_state['mkt2_name'] = market2

st.divider()
res_col1, res_col2 = st.columns(2)

if 'data1' in st.session_state:
      with res_col1:
            st.subheader(f"{st.session_state['mkt1_name']} Data")
            st.line_chart(st.session_state['data1']['Close'])
if 'data2' in st.session_state:
      with res_col2:
            st.subheader(f"{st.session_state['mkt2_name']} Data")
            st.line_chart(st.session_state['data2']['Close'])