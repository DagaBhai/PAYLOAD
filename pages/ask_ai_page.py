import streamlit as st
import pandas as pd
import asyncio
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

st.title("Ask AI about your Metrics")

# Constants
APP_NAME = "market_app"
USER_ID = "default"
SESSION_ID = "default"

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

def init_agent():
    # Retrieve metrics data from session state
    metrics_data = st.session_state.get("Selected_metrics", None)
    market_name = st.session_state.get("market_name", None)
    
    agent_description = """You are a stock market 
    expert your job is to answer questions about the stock markets around the world only.
    Do not talk about anything else.
    Your primary task to understand the data give its interpretation.

    Use the `google_search()` to find information about the market if it is not available in
    the given data. when you use google tell the user that this information is from google. 
    If you are unable to find the correct answers then say you don't know the answer.
    """
    
    if metrics_data is not None:
        if isinstance(metrics_data, pd.DataFrame):
             data_str = metrics_data.to_string()
        else:
             data_str = str(metrics_data)
             
        agent_description += f"\n\nHere is the financial metrics data of {market_name} you need to analyze, Please interpret this data for the user. :\n{data_str}\n\n"

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

# Initialize runner and session service in session state
if "runner" not in st.session_state:
    st.session_state.runner, st.session_state.session_service = init_agent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Optional: Add an initial greeting from the AI based on the data
    if "Selected_metrics" in st.session_state:
         st.session_state.messages.append({"role": "assistant", "content": "I have analyzed the metrics you selected. What would you like to know?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Async function to run the agent
async def run_agent_async(prompt_text: str):
    runner_instance = st.session_state.runner
    session_service = st.session_state.session_service
    
    # Get or create session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
    
    # Convert query to ADK Content format
    query = types.Content(role="user", parts=[types.Part(text=prompt_text)])
    
    # Collect all response parts
    response_text = ""
    
    # Stream the agent's response
    async for event in runner_instance.run_async(
        user_id=USER_ID, session_id=session.id, new_message=query
    ):
        if event.content and event.content.parts:
            if event.content.parts[0].text and event.content.parts[0].text != "None":
                response_text += event.content.parts[0].text
    
    return response_text

# React to user input
if prompt := st.chat_input("Ask about the metrics..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Run the agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Get or create event loop
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_closed():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Run the async function
                answer = loop.run_until_complete(run_agent_async(prompt))
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"An error occurred: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
