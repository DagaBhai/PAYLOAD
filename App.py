import streamlit as st
import dotenv

dotenv.load_dotenv()

# Set page config (only once, at the top)
st.set_page_config(
    page_title="BEST QUANTIFIER",
    page_icon="👋",
    layout="wide"
)

# Home page function
def home_page():
    st.markdown("<h1 style='text-align: center;'>Welcome to BEST QUANTIFIER! 👋</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>What would you like to achieve today?</h3>", unsafe_allow_html=True)
    left_co, cent_co, last_co = st.columns([1, 2, 1])

    with cent_co:
        # use_container_width=True makes buttons uniform and centered in the column
        if st.button("📈 CHECK OUT THE MARKET", use_container_width=True):
            st.write("Redirecting...")
            st.switch_page("pages/market_page.py")

        if st.button("⚖️ COMPARE THE MARKETS", use_container_width=True):
            st.write("Redirecting...")
            st.switch_page("pages/metrics_compare_page.py")

# Define pages
home = st.Page(
    home_page,
    title="Home",
    icon="🏠",
    default=True  # This makes Home the default landing page
)

Chart = st.Page(
    "pages/market_page.py",
    title="Market Chart",
    icon="📊"
)

Chart_Compare = st.Page(
    "pages/market_compare_page.py",
    title="Market Comparision",
    icon="🔍"
)

Metrics = st.Page(
    "pages/metrics_page.py",
    title="Metrics",
    icon="📈"
)

visual_metrics_interpertation_page = st.Page(
    "pages/visual_metrics_page.py",
    title="Visual Metrics and interpertation",
    icon="📈"
)

ask_ai_page = st.Page(
    "pages/ask_ai_page.py",
    title="Stock Market Expert Chatbot",
    icon="🤖"
)

# Group pages: create the "Reports" section header
pages = {
    "Market Report": [Chart, Chart_Compare, Metrics,visual_metrics_interpertation_page, ask_ai_page]
}

# Create navigation with Home at the top + Reports section
pg = st.navigation(
    {
        "": [home],        # Empty key = no section header, just Home at top
        "Market Report": [Chart, Chart_Compare, Metrics,visual_metrics_interpertation_page, ask_ai_page]
    }
)

# Run the selected page
pg.run()