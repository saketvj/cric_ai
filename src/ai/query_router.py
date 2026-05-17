import os
import json
import re
from openai import OpenAI
from ai.insights import generate_insight
import streamlit as st
from analytics.bowling import (
    get_top_bowlers,
    get_top_economical_bowlers,
    get_top_dot_ball_bowlers,
    get_best_phasewise_bowlers
)
from analytics.batting import (
    get_top_batsmen,
    get_best_strike_rate_batsmen,
    get_best_boundary_batsmen,
    get_best_average_batsmen
)
from pipeline.load_features import load_deliveries

deliveries = load_deliveries()

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_PAT") or st.secrets.get("GITHUB_PAT"),
)

prompt = """
You are an Cricket analytics router.
Your task:
Convert user query into JSON.
Available functions:
1. get_top_bowlers: returns bowlers with highest wickets
2. get_top_economical_bowlers : returns bowlers with best economy rate
3. get_top_dot_ball_bowlers : returns bowlers with highest dot ball percentage
4. get_best_phasewise_bowlers : returns best bowlers phase-wise using wickets and economy
5. get_top_batsmen : returns batsmen with highest runs scored
6. get_best_strike_rate_batsmen : returns batsmen with highest strike rate
7. get_best_boundary_batsmen : returns batsmen with highest boundary percentage
8. get_best_average_batsmen : returns batsmen with highest batting average
Available phases:
- powerplay
- middle
- death
For relative periods like:
- last 1 year 
- last 2 years
- last 3 years
calculate years relative to current year = 2025.
-last 1 year => [2025]
-last 2 years => [2024, 2025]
-last 3 years => [2023, 2024, 2025]
Rules:
- Extract years
- Extract phase
- Extract top_n if mentioned
- If top_n not mentioned, use 10
- if years not mentioned, use all years as empty list
- years must ALWAYS be a list of integers e.g. [2024] never a string
Return ONLY valid JSON.
{
    "function_name": "get_top_bowlers",
    "years": [2025],
    "phase": "death",
    "top_n": 5
}
"""

function_map = {
    "get_top_bowlers": get_top_bowlers,
    "get_top_economical_bowlers": get_top_economical_bowlers,
    "get_top_dot_ball_bowlers": get_top_dot_ball_bowlers,
    "get_best_phasewise_bowlers": get_best_phasewise_bowlers,
    "get_top_batsmen": get_top_batsmen,
    "get_best_strike_rate_batsmen": get_best_strike_rate_batsmen,
    "get_best_boundary_batsmen": get_best_boundary_batsmen,
    "get_best_average_batsmen": get_best_average_batsmen,
}

def run_query(user_query):
    # Error 1: LLM API call failure
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user",   "content": user_query},
            ],
            model="openai/gpt-4o",
            temperature=1,
            max_tokens=400,
            top_p=1
        )
    except Exception as e:
        raise ConnectionError(f"LLM API call failed: {e}")

    raw = response.choices[0].message.content.strip()
    print(raw)

    # Error 2: JSON parsing failure
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        clean = match.group() if match else raw
        result = json.loads(clean)
    except (json.JSONDecodeError, AttributeError) as e:
        raise ValueError(f"LLM returned invalid JSON: {raw}")

    # Error 3: Unknown function name
    function_name = result.get('function_name')
    if function_name not in function_map:
        raise KeyError(f"Unknown function returned by LLM: {function_name}")

    # Error 4: years cleanup — handle string or int from LLM
    years = result.get('years', [])
    if isinstance(years, str):
        years = [int(years)]
    elif isinstance(years, int):
        years = [years]
    else:
        years = [int(y) for y in years]

    # Error 5: Analytics function failure
    try:
        func = function_map[function_name]
        df = func(deliveries, years, result.get('phase'), int(result.get('top_n', 10)))
    except Exception as e:
        raise RuntimeError(f"Analytics function failed: {e}")

    # Error 6: Empty result
    if df is None or df.empty:
        raise ValueError("No data found for this query. Try different filters.")

    return df


if __name__ == "__main__":
    user_query = "top 5 boundary hitter in death overs in last 3 years in ipl"
    try:
        df = run_query(user_query)
        print(df)
        insight = generate_insight(user_query, df)
        print(insight)
    except Exception as e:
        print(f"Error: {e}")