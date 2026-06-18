<<<<<<< Updated upstream
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

from backend.text_processing import combine_case_fields

app = FastAPI(title="Legal Case AI", version="1.0")
=======
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import pandas as pd
import pickle
import numpy as np
import faiss

app = FastAPI(title="Legal Case AI", version="2.0")
>>>>>>> Stashed changes

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load models ---
print("Loading models...")
<<<<<<< Updated upstream
df = pd.read_csv("data/cleaned_cases.csv")
prediction_df = pd.read_csv("data/cases.csv")
VALID_COURTS = set(df["court"].dropna().unique())
=======
try:
    df = pd.read_csv("data/cleaned_cases.csv")
>>>>>>> Stashed changes

    with open("models/prediction_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("models/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

<<<<<<< Updated upstream
# Precompute all case vectors for similarity search
all_texts = [
    combine_case_fields(row["facts"], row["section"], row["court"])
    for _, row in df.iterrows()
]
all_vectors = vectorizer.transform(all_texts)
=======
    with open("models/search_vectorizer.pkl", "rb") as f:
        search_vectorizer = pickle.load(f)
>>>>>>> Stashed changes

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

# --- Input schema with validation ---
class CaseInput(BaseModel):
    facts: str
    section: str
    court: str

<<<<<<< Updated upstream
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
=======
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

# --- Core functions ---
def predict_outcome(case_text: str):
>>>>>>> Stashed changes
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

# --- Routes ---
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
<<<<<<< Updated upstream
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
=======
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
>>>>>>> Stashed changes

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
