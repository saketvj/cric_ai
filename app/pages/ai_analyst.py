import streamlit as st
import sys
import os
import pandas as pd

DEV_MODE = False
fake_df = pd.DataFrame({
    "batsman": [
        "Virat Kohli",
        "SKY",
        "Buttler"
    ],
    "runs": [720, 650, 610]
})
fake_insight = """
Virat Kohli dominated the last 3 IPL seasons
with exceptional consistency.
"""
# Tell Python where to find your src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from ai.query_router import run_query
from ai.insights import generate_insight


# ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="AI Cricket Analyst",
#     page_icon="🏏",
#     layout="wide"
# )

st.title("🏏 AI Cricket Analyst")
st.markdown("Ask anything about IPL — batting, bowling, phases, seasons.")


# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- DISPLAY OLD CHAT ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":
            st.write(message["content"])

        else:

            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📊 Results")
                st.dataframe(
                    message["df"],
                    use_container_width=True
                )

            with col2:
                st.subheader("💡 Insight")
                st.info(message["insight"])

            # Chart
            try:
                numeric_cols = message["df"].select_dtypes(
                    include=['int64', 'float64']
                ).columns

                if len(numeric_cols) > 0:

                    chart_col = numeric_cols[0]

                    st.subheader("📈 Visual")

                    st.bar_chart(
                        message["df"].set_index(
                            message["df"].columns[0]
                        )[chart_col]
                    )

            except:
                pass


# ---------------- CHAT INPUT ----------------
user_query = st.chat_input(
    "Ask me anything... e.g. top 5 death bowlers in 2024"
)


# ---------------- HANDLE NEW QUERY ----------------
if user_query:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_query)

    try:

        with st.chat_message("assistant"):

            with st.spinner("Analyzing..."):

                if DEV_MODE:

                    df = fake_df
                    insight = fake_insight

                else:

                    df = run_query(user_query)
                    insight = generate_insight(user_query, df)

            # Layout
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📊 Results")
                st.dataframe(df, use_container_width=True)

            with col2:
                st.subheader("💡 Insight")
                st.info(insight)

            # Chart
            try:
                numeric_cols = df.select_dtypes(
                    include=['int64', 'float64']
                ).columns

                if len(numeric_cols) > 0:

                    chart_col = numeric_cols[0]

                    st.subheader("📈 Visual")

                    st.bar_chart(
                        df.set_index(df.columns[0])[chart_col]
                    )

            except:
                pass

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "insight": insight,
            "df": df
        })

    except Exception as e:

        st.error(f"Error: {e}")