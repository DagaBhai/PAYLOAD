import streamlit as st
import pandas as pd
import asyncio
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- Configuration ---
st.set_page_config(page_title="Market AI", layout="wide")
st.title("Ask AI about your Metrics")

APP_NAME = "market_app"
USER_ID = "default_user"
SESSION_ID = "default_session"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# --- Agent Factory ---
def init_agent_components():
    """Initializes the runner and session service."""
    metrics_data = st.session_state.get("Selected_metrics", None)
    market_name = st.session_state.get("market_name", "the market")
    
    agent_description = (
        "You are a stock market expert. Your job is to answer questions "
        "about the stock markets around the world only. Do not talk about anything else. "
        "Your primary task is to understand the data and give its interpretation. "
        "Use `Google Search()` for missing info and cite it. If unknown, say you don't know."
    )
    
    if metrics_data is not None:
        data_str = metrics_data.to_string() if isinstance(metrics_data, pd.DataFrame) else str(metrics_data)
        agent_description += f"\n\nMarket Data for {market_name}:\n{data_str}\n"

    market_agent = LlmAgent(
        name="market_expert",
        model=Gemini(
            model='gemini-2.5-flash',
            retry_options=retry_config
        ),
        description=agent_description,
        tools=[google_search]
    )
    
    session_service = InMemorySessionService()
    runner = Runner(agent=market_agent, app_name=APP_NAME, session_service=session_service)
    return runner, session_service

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    if "Selected_metrics" in st.session_state:
         st.session_state.messages.append({"role": "assistant", "content": "I have analyzed the metrics. What would you like to know?"})

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Core Async Execution ---
async def run_agent_logic(prompt_text: str):
    """
    Handles session retrieval/creation and agent execution in one loop context.
    """
    runner_instance, session_service = init_agent_components()
    
    # Robust Session Handling: Try to get, if None, then create
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    
    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
    
    query = types.Content(role="user", parts=[types.Part(text=prompt_text)])
    response_text = ""
    
    # Stream and aggregate response
    async for event in runner_instance.run_async(
        user_id=USER_ID, session_id=session.id, new_message=query
    ):
        if event.content and event.content.parts:
            text_part = event.content.parts[0].text
            if text_part and text_part != "None":
                response_text += text_part
    
    return response_text

# --- UI Input and Interaction ---
if prompt := st.chat_input("Ask about the metrics..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Use asyncio.run to ensure a fresh, isolated loop for this turn
                answer = asyncio.run(run_agent_logic(prompt))
                
                if not answer:
                    answer = "The agent did not return a response."
                    
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})