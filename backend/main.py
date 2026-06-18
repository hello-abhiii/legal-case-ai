from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import pandas as pd
import pickle
import numpy as np
import faiss

app = FastAPI(title="Legal Case AI", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading models...")
try:
    df = pd.read_csv("data/cleaned_cases.csv")

    with open("models/prediction_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("models/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    with open("models/search_vectorizer.pkl", "rb") as f:
        search_vectorizer = pickle.load(f)

    faiss_index = faiss.read_index("models/case_index.faiss")

    print(f"Models loaded! Cases in DB: {len(df)} | FAISS index: {faiss_index.ntotal}")

except Exception as e:
    print(f"ERROR loading models: {e}")
    raise RuntimeError(f"Failed to load models: {e}")

VALID_SECTIONS = [
    "IPC 302", "IPC 304", "IPC 307", "IPC 376", "IPC 379",
    "IPC 380", "IPC 392", "IPC 395", "IPC 420", "IPC 498A",
    "IPC 506", "IPC 34"
]

VALID_COURTS = [
    "Sessions Court", "High Court", "Supreme Court",
    "District Court", "Magistrate Court"
]

class CaseInput(BaseModel):
    facts: str
    section: str
    court: str

    @validator('facts')
    def facts_must_be_meaningful(cls, v):
        if not v or len(v.strip()) < 20:
            raise ValueError('Facts must be at least 20 characters long')
        return v.strip()

    @validator('section')
    def section_must_be_valid(cls, v):
        if v not in VALID_SECTIONS:
            raise ValueError(f'Invalid section. Must be one of: {", ".join(VALID_SECTIONS)}')
        return v

    @validator('court')
    def court_must_be_valid(cls, v):
        if v not in VALID_COURTS:
            raise ValueError(f'Invalid court. Must be one of: {", ".join(VALID_COURTS)}')
        return v

def predict_outcome(case_text: str):
    vec = vectorizer.transform([case_text])
    prediction = model.predict(vec)[0]
    probabilities = model.predict_proba(vec)[0]
    confidence = round(float(max(probabilities)) * 100, 2)
    return prediction, confidence

def find_similar_cases(case_text: str, top_k: int = 3):
    query_vec = search_vectorizer.transform([case_text]).toarray().astype('float32')
    distances, indices = faiss_index.search(query_vec, top_k)
    results = []
    for idx in indices[0]:
        if idx < len(df):
            row = df.iloc[idx]
            results.append({
                "title":   str(row.get('title', 'Unknown')),
                "section": str(row.get('section', '')),
                "outcome": str(row.get('outcome', '')),
                "facts":   str(row.get('facts', ''))[:300] + "..."
            })
    return results

@app.get("/")
def home():
    return {
        "message": "Legal Case AI is running!",
        "version": "2.0",
        "total_cases": len(df),
        "valid_sections": VALID_SECTIONS,
        "valid_courts": VALID_COURTS
    }

@app.post("/analyze")
def analyze_case(case: CaseInput):
    try:
        combined = f"{case.facts} {case.section} {case.court}".lower()
        prediction, confidence = predict_outcome(combined)
        similar = find_similar_cases(combined)
        explanation = [
            f"Similar to '{c['title']}' which ended in {c['outcome']}"
            for c in similar
        ]
        return {
            "predicted_outcome": prediction,
            "confidence": f"{confidence}%",
            "similar_cases": similar,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/cases")
def get_all_cases():
    try:
        return df[['case_id', 'title', 'section', 'outcome']].to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch cases: {str(e)}")

@app.get("/sections")
def get_valid_sections():
    return {"sections": VALID_SECTIONS}

@app.get("/courts")
def get_valid_courts():
    return {"courts": VALID_COURTS}

@app.get("/history")
def get_history():
    return {"message": "History available in local version with PostgreSQL"}
