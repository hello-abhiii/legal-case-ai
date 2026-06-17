from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

# Precompute all case vectors for similarity search
all_texts = (df['facts'] + " " + df['section'] + " " + df['court']).str.lower()
all_vectors = vectorizer.transform(all_texts)

print("All models loaded!")

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
    query_vec = vectorizer.transform([case_text])
    similarities = cosine_similarity(query_vec, all_vectors)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    results = []
    for idx in top_indices:
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
def get_history():
    return {"message": "History available in local version with PostgreSQL"}
