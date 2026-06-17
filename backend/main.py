from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Legal Case AI", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading models...")
df = pd.read_csv("data/cleaned_cases.csv")
model = pickle.load(open("models/prediction_model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
search_vectorizer = pickle.load(open("models/search_vectorizer.pkl", "rb"))

all_texts = (df["facts"] + " " + df["section"] + " " + df["court"]).str.lower().fillna("")
all_vectors = search_vectorizer.transform(all_texts)
print(f"Loaded! Pred features: {len(vectorizer.vocabulary_)} | Search cases: {all_vectors.shape[0]}")

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
    query_vec = search_vectorizer.transform([case_text])
    similarities = cosine_similarity(query_vec, all_vectors)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    results = []
    for idx in top_indices:
        results.append({
            "title": df["title"].iloc[idx],
            "section": df["section"].iloc[idx],
            "outcome": df["outcome"].iloc[idx],
            "facts": df["facts"].iloc[idx],
        })
    return results

@app.get("/")
def home():
    return {"message": "Legal Case AI v2.0 is running!"}

@app.post("/analyze")
def analyze_case(case: CaseInput):
    combined = f"{case.facts} {case.section} {case.court}".lower()
    prediction, confidence = predict_outcome(combined)
    similar = find_similar_cases(combined)
    explanation = [f"Similar to {c['title']} which ended in {c['outcome']}" for c in similar]
    return {
        "predicted_outcome": prediction,
        "confidence": f"{confidence}%",
        "similar_cases": similar,
        "explanation": explanation,
    }

@app.get("/cases")
def get_all_cases():
    return df[["case_id", "title", "section", "outcome"]].to_dict(orient="records")

@app.get("/history")
def get_history():
    return {"message": "History available in local version with PostgreSQL"}
