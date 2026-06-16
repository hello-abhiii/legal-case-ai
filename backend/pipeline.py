import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# ── Load everything ──
df = pd.read_csv("data/cleaned_cases.csv")

with open("models/prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

index = faiss.read_index("models/case_index.faiss")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

print("All models loaded successfully!")

# ── Similar Case Search ──
def find_similar_cases(query_text, top_k=3):
    query_vec = embedder.encode([query_text]).astype('float32')
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

# ── Outcome Prediction ──
def predict_outcome(case_text):
    vec = vectorizer.transform([case_text])
    prediction = model.predict(vec)[0]
    probabilities = model.predict_proba(vec)[0]
    confidence = round(max(probabilities) * 100, 2)
    return prediction, confidence

# ── Full Pipeline ──
def analyze_case(case_text):
    print("\n" + "="*50)
    print("LEGAL CASE ANALYSIS")
    print("="*50)
    print(f"Input: {case_text}")

    prediction, confidence = predict_outcome(case_text)
    print(f"\nPredicted Outcome : {prediction}")
    print(f"Confidence        : {confidence}%")

    similar = find_similar_cases(case_text)
    print(f"\nTop {len(similar)} Similar Cases:")
    for i, case in enumerate(similar):
        print(f"\n  {i+1}. {case['title']}")
        print(f"     Section : {case['section']}")
        print(f"     Outcome : {case['outcome']}")
        print(f"     Facts   : {case['facts']}")

    print("\nExplanation:")
    for i, case in enumerate(similar):
        print(f"  {i+1}. Similar to {case['title']} which ended in {case['outcome']}")

    print("="*50)

# ── Test Cases ──
analyze_case("accused stole a bike from parking lot ipc 379 district court")
analyze_case("accused cheated people with fake investment scheme ipc 420 high court")
