import json
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_PAT"],
)

def generate_insight(user_query, df):   # ← receives both as parameters
    
    insight_prompt = """
    You are an IPL cricket analyst.
    You will be given a user query and data results.
    Generate a clear specific insight based on the data.
    Return ONLY valid JSON.
    {
        "insight": "your insight here"
    }
    """

    insight_query = f"""
    User asked: {user_query}

    Here are the results:
    {df.to_string(index=False)}

    Generate insight based on these results.
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": insight_prompt},
            {"role": "user",   "content": insight_query},
        ],
        model="openai/gpt-4o",
        temperature=0,
        max_tokens=500,
        top_p=1,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content.strip()
    result = json.loads(raw)
    return result["insight"]