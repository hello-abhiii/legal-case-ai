import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

from backend.text_processing import combine_case_fields

app = FastAPI(title="Legal Case AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading models...")
df = pd.read_csv("data/cleaned_cases.csv")
prediction_df = pd.read_csv("data/cases.csv")
VALID_COURTS = set(df["court"].dropna().unique())

with open("models/prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Precompute all case vectors for similarity search
all_texts = [
    combine_case_fields(row["facts"], row["section"], row["court"])
    for _, row in df.iterrows()
]
all_vectors = vectorizer.transform(all_texts)

print("All models loaded!")

class CaseInput(BaseModel):
    facts: str
    section: str
    court: str

    @field_validator("facts")
    @classmethod
    def facts_must_be_substantial(cls, value: str) -> str:
        if len(value.strip()) < 20:
            raise ValueError("Facts must be at least 20 characters long.")
        return value.strip()

    @field_validator("section")
    @classmethod
    def section_must_look_like_ipc(cls, value: str) -> str:
        section = value.strip().upper()
        if not re.fullmatch(r"IPC\s+\d+[A-Z]?", section):
            raise ValueError("Section must use the format 'IPC 302'.")
        return section

    @field_validator("court")
    @classmethod
    def court_must_be_known(cls, value: str) -> str:
        court = value.strip()
        if court not in VALID_COURTS:
            allowed = ", ".join(sorted(VALID_COURTS))
            raise ValueError(f"Court must be one of: {allowed}.")
        return court

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
    combined = combine_case_fields(case.facts, case.section, case.court)
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

@app.get("/stats")
def get_stats():
    return {
        "prediction_cases": len(prediction_df),
        "ipc_sections": prediction_df["section"].nunique(),
        "search_cases": len(df),
        "outcomes": prediction_df["outcome"].value_counts().to_dict(),
    }

@app.get("/history")
def get_history():
    return {"message": "History available in local version with PostgreSQL"}
