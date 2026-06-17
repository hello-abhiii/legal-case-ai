import psycopg2
import os

conn = psycopg2.connect(
    host="localhost",
    database="legal_ai",
    user=os.environ.get("USER"),
    password=""
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cases (
    case_id     SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    facts       TEXT NOT NULL,
    section     TEXT NOT NULL,
    court       TEXT NOT NULL,
    outcome     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id                 SERIAL PRIMARY KEY,
    facts              TEXT NOT NULL,
    section            TEXT NOT NULL,
    court              TEXT NOT NULL,
    predicted_outcome  TEXT NOT NULL,
    confidence         TEXT NOT NULL,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cur.close()
conn.close()
print("✅ Tables created successfully!")
