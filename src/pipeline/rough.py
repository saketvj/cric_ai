import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/ipl.db")

matches = pd.read_sql("SELECT COUNT(*) as cnt FROM matches", conn)
deliveries = pd.read_sql("SELECT COUNT(*) as cnt FROM deliveries", conn)
processed = pd.read_sql("SELECT COUNT(*) as cnt FROM processed_matches", conn)

# print(matches)
# print(deliveries)
# print(processed)


t1 = pd.read_sql("""
SELECT COUNT(*) 
FROM deliveries 
WHERE total_runs IS NULL
""", conn)

t2 = pd.read_sql("""
SELECT batsman, SUM(batsman_runs) as runs
FROM deliveries
GROUP BY batsman
ORDER BY runs DESC
LIMIT 5
""", conn)

# print(t1)
print(t2)