import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

sys.path.append(str(SRC_DIR))


import streamlit as st
from pathlib import Path
from config.constants import DB_PATH

if not Path(DB_PATH).exists():
    from pipeline.db import init_db
    from pipeline.loader import load_dataset
    from pipeline.load_features import load_deliveries
    init_db()
    load_dataset()
    load_deliveries()  

st.set_page_config(
    page_title="CricketAI Analyst",
    page_icon="🏏",
    layout="wide"          
)



pg = st.navigation([
    st.Page("pages/ai_analyst.py",    title="AI Cricket Analyst", icon="🤖"),
    st.Page("pages/data_explorer.py", title="Data Explorer",      icon="📊"),
])

pg.run()   