from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import faiss
import pickle
import psycopg2
import os
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Legal Case AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading models...")
df = pd.read_csv("data/cleaned_cases.csv")

with open("models/prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

index = faiss.read_index("models/case_index.faiss")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
print("All models loaded!")

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="legal_ai",
        user=os.environ.get("USER"),
        password=""
    )

class CaseInput(BaseModel):
    facts: str
    section: str
    court: str

def predict_outcome(case_text):
    vec = vectorizer.transform([case_text])
    prediction = model.predict(vec)[0]
    probabilities = model.predict_proba(vec)[0]
    confidence = round(max(probabilities) * 100, 2)
    return prediction, confidence

def find_similar_cases(case_text, top_k=3):
    query_vec = embedder.encode([case_text]).astype('float32')
    distances, indices = index.search(query_vec, top_k)
    results = []
    for idx in indices[0]:
        results.append({
            "title": df['title'][idx],
            "section": df['section'][idx],
            "outcome": df['outcome'][idx],
            "facts": df['facts'][idx]
        })
    return results

@app.get("/")
def home():
    return {"message": "Legal Case AI is running!"}

@app.post("/analyze")
def analyze_case(case: CaseInput):
    combined = f"{case.facts} {case.section} {case.court}".lower()
    prediction, confidence = predict_outcome(combined)
    similar = find_similar_cases(combined)
    explanation = [
        f"Similar to {c['title']} which ended in {c['outcome']}"
        for c in similar
    ]

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO predictions (facts, section, court, predicted_outcome, confidence)
            VALUES (%s, %s, %s, %s, %s)
        """, (case.facts, case.section, case.court, prediction, f"{confidence}%"))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB error: {e}")

    return {
        "predicted_outcome": prediction,
        "confidence": f"{confidence}%",
        "similar_cases": similar,
        "explanation": explanation
    }

@app.get("/cases")
def get_all_cases():
    return df[['case_id', 'title', 'section', 'outcome']].to_dict(orient="records")

@app.get("/history")
def get_prediction_history():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT facts, section, court, predicted_outcome, confidence, created_at
            FROM predictions
            ORDER BY created_at DESC
            LIMIT 20;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "facts": r[0],
                "section": r[1],
                "court": r[2],
                "predicted_outcome": r[3],
                "confidence": r[4],
                "timestamp": str(r[5])
            }
            for r in rows
        ]
    except Exception as e:
        return {"error": str(e)}
