import streamlit as st

# This is the FIRST thing Streamlit reads
# It configures the entire app globally
st.set_page_config(
    page_title="CricketAI Analyst",
    page_icon="🏏",
    layout="wide"          # uses full screen width
)

# --- Navigation ---
# st.navigation tells Streamlit what pages exist
# Each st.Page points to a file

pg = st.navigation([
    st.Page("pages/ai_analyst.py",    title="AI Cricket Analyst", icon="🤖"),
    st.Page("pages/data_explorer.py", title="Data Explorer",      icon="📊"),
])

pg.run()   # runs whichever page user clicked