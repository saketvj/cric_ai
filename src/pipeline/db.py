import sqlite3
from pathlib import Path
from config.constants import DB_PATH


def init_db():


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # MATCHES table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id TEXT PRIMARY KEY,
        match_date TEXT,
        venue TEXT,
        toss TEXT,
        toss_decision TEXT,
        team1 TEXT,
        team2 TEXT,
        winner TEXT
    );
    """)

    # DELIVERIES table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT,
        innings TEXT,
        over REAL,
        batting_team TEXT,
        bowling_team TEXT,
        non_striker TEXT,
        bowler TEXT,
        batsman TEXT,
        wicket INTEGER,
        wicket_kind TEXT,
        fielders TEXT,
        player_out TEXT,
        batsman_runs INTEGER,
        extra_runs INTEGER,
        total_runs INTEGER,
        extra_type TEXT
    );
    """)

    # PROCESSED MATCHES table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_matches (
        match_id TEXT PRIMARY KEY,
        processed_at TEXT
    );
    """)

    conn.commit()
    conn.close()