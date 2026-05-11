import sqlite3
import pandas as pd
# from feature  import deli
from config.constants import DB_PATH, RAW_DATA_PATH

from feature import apply_features



conn = sqlite3.connect(DB_PATH)

matches = pd.read_sql("SELECT * FROM matches", conn)
deliveries = pd.read_sql("SELECT * FROM deliveries", conn)


deliveries = deliveries.sort_values(
    ['match_id', 'innings', 'over'])



deli = apply_features(deliveries)
# print(list(deliveries.columns))
deli = deli.merge(
    matches[
        ['match_id', 'match_date', 'venue']
    ],
    on='match_id',
    how='left'
)

a = deli[[
    'match_id',
    'innings',
    'over',
    'batsman_runs',
    'total_runs',
    'wicket',
    'extra_type',
    'phase',
    'is_boundary',
    'is_dot_ball',
    'is_legal_ball',
    'batsman_ball_faced',
    'is_bowler_wicket',
    'cumulative_runs',
    'cumulative_wickets',
    'cumulative_legal_balls'
]].head(20)

# print(a)

matches['match_date'] = pd.to_datetime(
    matches['match_date']
)

deli['match_date'] = pd.to_datetime(
    deli['match_date'])

# print(
#     deli[['over', 'phase']].head(100)
# )


# sample = deli[
#     (deli['match_id'] == deli['match_id'].iloc[0]) &
#     (deli['innings'] == deli['innings'].iloc[0])
# ]

# print(
#     sample[
#         ['over', 'total_runs', 'cumulative_runs']
#     ].head(20)
# )

print(matches.columns)
top_bowlers = (
    deli[
        deli['match_date'].dt.year.isin([2023, 2024, 2025,2022,2021,2020,2019])
    ]
    .groupby('bowler')['is_bowler_wicket']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# print(matches.columns)

print(top_bowlers)