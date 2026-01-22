import streamlit as st
import pandas as pd
from tools.Interpretation import interpret_metric

def plot_graph_n_intertation(metrics_lst,graph_metrics):
    for idx,metrics in enumerate(metrics_lst):
            st.subheader(f"{metrics}")
            st.line_chart(graph_metrics[metrics])
            interpretation = interpret_metric(
                 metric_name=metrics,
                 series=graph_metrics[metrics]
            )
            st.write(f"### Interpretation: {interpretation}")
            if idx>1:
                st.divider()

if "Selected_metrics" in st.session_state and st.session_state["Selected_metrics"] is not None:
    name=st.session_state['market_name']

    st.title(f"Interperation of the Metrics for {name}")

    graph_selected_metrics = st.session_state["Selected_metrics"] 
    metrics_lst_of_graph = graph_selected_metrics.columns  
    
    plot_graph_n_intertation(metrics_lst_of_graph,graph_selected_metrics)

else:
    st.warning("No Metrics selected yet.")
    st.write("Select the Metrics")
    if st.button("Metrics"):
        st.switch_page("pages/metrics_page.py")
