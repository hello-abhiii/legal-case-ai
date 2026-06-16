import pandas as pd
import psycopg2
import os

df = pd.read_csv("data/cleaned_cases.csv")

conn = psycopg2.connect(
    host="localhost",
    database="legal_ai",
    user=os.environ.get("USER"),
    password=""
)
cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO cases (title, facts, section, court, outcome)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['title'], row['facts'], row['section'], row['court'], row['outcome']))

conn.commit()
cur.close()
conn.close()
print(f"✅ {len(df)} cases imported into PostgreSQL!")
