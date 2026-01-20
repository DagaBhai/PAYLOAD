import streamlit as st
import pandas as pd
from pages.tools.market import get_market_data
from pages.tools.metrics import metrics_lst,log_ret, support_n_resistance, rolling_etx, ROC, MAS, MAD, vol, vol_ratio, MACD
from pages.tools.Interpretation import interpret_metric

def plot_graph_n_intertation(metrics_lst,graph_metrics,market_price):
    for idx,metrics in enumerate(metrics_lst):
            st.subheader(f"{metrics}")
            st.line_chart(graph_metrics[metrics])
            interpretation = interpret_metric(
                 metric_name=metrics,
                 series=graph_metrics[metrics],
                 price=market_price
            )
            st.write(f"### Interpretation: {interpretation}")
            if idx>1:
                st.divider()

if "market_ticker" in st.session_state and st.session_state["market_ticker"] is not None:
    st.title("Quantitative Metrics")

    market_ticker = st.session_state["market_ticker"]
    name = st.session_state["market_name"]
    period = st.session_state["market_period"]
    data=get_market_data(market_ticker,period=period)
    print(data.columns)
    close=data["Close"]
    price=close.iloc[-1]
    selected_metrics = st.multiselect("Select the metrics to view:", metrics_lst, default=None, key="metric_multiselect")
    resistance, support = support_n_resistance(close)
    macd , single_line_macd, hist_macd = MACD(close)


    df_metrics = pd.DataFrame(
        {
        "Log Return": log_ret(close),
        "Support": support,
        "Resistance": resistance,
        "Rolling Extereme": rolling_etx(close),
        "Rate Of Change (Daily)": ROC(close, 1),
        "Rate Of Change (Weekly)": ROC(close, 5),
        "Rate Of Change (Monthly)": ROC(close, 21),
        "Volitility": vol(close),
        "Volitility Ratio":vol_ratio(close),
        "Moving Average Distance": MAD(close),
        "Moving Average Slope": MAS(close),
        "Moving Average Convergence Divergence (MACD)": macd,
        "Moving Average Convergence Divergence (Single Line)": single_line_macd,
        "Moving Average Convergence Divergence (Histogram)": hist_macd
        }
    )

    df_metrics.index = df_metrics.index.date

    if selected_metrics:
        display_df=df_metrics[selected_metrics]

        st.header(f"Financial Metrics: {name}")
        st.dataframe(display_df.style.format(precision=4), width="content")
        
        if st.button("Interpert Using Our AI"):
            st.session_state["Selected_metrics"] = df_metrics[selected_metrics]
            st.switch_page("pages/ask_ai_page.py")

        st.title(f"Interperation of the Metrics for {st.session_state['market_name']}")
        graph_selected_metrics = st.session_state["Selected_metrics"] 
        metrics_lst_of_graph = graph_selected_metrics.columns  
        
        plot_graph_n_intertation(metrics_lst_of_graph,graph_selected_metrics,price)
    
    else:
        st.info("Please select at least one metric.")

else:
    st.warning("No market selected yet.")
    st.write("Select the market")
    if st.button("Markets"):
        st.switch_page("pages/market_page.py")

