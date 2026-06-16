import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ── Step 1: Load cleaned data ──
df = pd.read_csv("data/cleaned_cases.csv")
print("Loaded", len(df), "cases")

# ── Step 2: Prepare features and labels ──
X = df['combined_text']
y = df['outcome']

print("Labels:", y.unique())

# ── Step 3: Convert text to numbers using TF-IDF ──
vectorizer = TfidfVectorizer(max_features=500)
X_vec = vectorizer.fit_transform(X)
print("Feature shape:", X_vec.shape)

# ── Step 4: Split into train and test ──
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)
print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# ── Step 5: Train the model ──
print("\nTraining model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Training done!")

# ── Step 6: Evaluate ──
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {round(acc * 100, 2)}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# ── Step 7: Save model and vectorizer ──
with open("models/prediction_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model saved to models/prediction_model.pkl")
print("Vectorizer saved to models/vectorizer.pkl")

# ── Step 8: Test a prediction ──
def predict_outcome(case_text):
    vec = vectorizer.transform([case_text])
    prediction = model.predict(vec)[0]
    probabilities = model.predict_proba(vec)[0]
    confidence = round(max(probabilities) * 100, 2)
    return prediction, confidence

print("\n── Test Predictions ──")
test_cases = [
    "accused stole a mobile phone from a shop ipc 379 district court",
    "accused assaulted a person during dispute ipc 323 district court",
    "accused forged bank documents to get loan ipc 467 high court"
]

for case in test_cases:
    outcome, confidence = predict_outcome(case)
    print(f"\nCase   : {case}")
    print(f"Outcome: {outcome}")
    print(f"Confidence: {confidence}%")
