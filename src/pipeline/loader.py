import pandas as pd
import yaml
from tqdm import tqdm
import sqlite3
from pathlib import Path
from datetime import datetime
from pipeline.transform import create_match_df, create_ball_df
from config.constants import DB_PATH, RAW_DATA_PATH







def load_dataset():

    


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 🔹 2. Get already processed matches
    processed_matches_df = pd.read_sql_query(
        "SELECT match_id FROM processed_matches;", conn
    )
    processed_matches = set(processed_matches_df['match_id'])

    # 🔹 3. Get files
    # base_path = Path.cwd()
    data_path = RAW_DATA_PATH
    files = list(data_path.glob('*.yaml'))

    # 🔹 4. Loop through files
    for file in tqdm(files):

        match_id = file.name.split('.')[0]

        # Skip already processed
        if match_id in processed_matches:
            continue

        try:
            # 🔹 Read YAML
            with open(file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # 🔹 Create DataFrames
            match_df = pd.DataFrame([create_match_df(data, file)])
            ball_df = pd.DataFrame(create_ball_df(data, file))

            # 🔹 Store in DB
            match_df.to_sql('matches', conn, if_exists='append', index=False)
            ball_df.to_sql('deliveries', conn, if_exists='append', index=False)

            # 🔹 Mark as processed (IMPORTANT: inside loop)
            cursor.execute("""
                INSERT INTO processed_matches (match_id, processed_at)
                VALUES (?, ?)
            """, (match_id, datetime.now().isoformat()))

            # 🔹 Commit per match (safer)
            conn.commit()

            
            processed_matches.add(match_id)

        except Exception as e:
            print(f"{file.name} Error: {e}")

    # 🔹 5. Close connection
    conn.close()
