from pipeline.db import init_db
from pipeline.loader import load_dataset

if __name__ == "__main__":
    init_db()
    load_dataset()