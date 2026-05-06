from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / 'data' / 'db' / 'ipl.db'
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw' / 'ipl'