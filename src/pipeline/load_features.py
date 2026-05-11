from config.constants import DB_PATH, RAW_DATA_PATH
import numpy as np
import sqlite3
import pandas as pd
from pipeline.feature import apply_features


with sqlite3.connect(DB_PATH) as conn:
    matches = pd.read_sql("SELECT * FROM matches", conn)
    deliveries = pd.read_sql("SELECT * FROM deliveries", conn)


deliveries = deliveries.sort_values(
    ['match_id', 'innings', 'over'])


deliveries = apply_features(deliveries)
deliveries = deliveries.merge(
    matches[
        ['match_id', 'match_date', 'venue']
    ],
    on='match_id',
    how='left'
)
deliveries['match_date'] = pd.to_datetime(deliveries['match_date'])

