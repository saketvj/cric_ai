import os
import json
import re
from openai import OpenAI
from analytics.bowling import *
from analytics.batting import *
from insights import generate_insight


client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_PAT"],
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
current year  = 2025
Rules:
- Extract years
- Extract phase
- Extract top_n if mentioned
- If top_n not mentioned, use 10
Return ONLY valid JSON.
{
    "function_name": "get_top_bowlers",
    "years": [2025],
    "phase": "death",
    "top_n": 5
}
"""

user_query = "top 5 boundary hitter in death overs in last 3 years in ipl"

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": user_query,
        }
    ],
    model="openai/gpt-4o",
    temperature=1,
    max_tokens=4096,
    top_p=1
)

raw = response.choices[0].message.content.strip()
print(raw)

# Extract JSON from anywhere in the response
match = re.search(r'\{.*\}', raw, re.DOTALL)
clean = match.group() if match else raw
result = json.loads(clean)

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

func = function_map[result['function_name']]
df = func(deliveries, result['years'], result.get('phase'), result.get('top_n', 10))
print(df)


insights = generate_insight(user_query,df)
print(insights)