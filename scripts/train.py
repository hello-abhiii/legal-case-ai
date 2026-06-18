import pickle
import sys
import warnings
from pathlib import Path

import faiss
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.svm import SVC

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.text_processing import combine_case_fields

warnings.filterwarnings("ignore")


def build_texts(df):
    return [
        combine_case_fields(row["facts"], row["section"], row["court"])
        for _, row in df.iterrows()
    ]


prediction_cases = pd.read_csv("data/cases.csv")
all_cases = pd.read_csv("data/cleaned_cases.csv")
print(f"Prediction cases: {len(prediction_cases)} | Search cases: {len(all_cases)}")

prediction_vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True,
)
X = prediction_vectorizer.fit_transform(build_texts(prediction_cases))
y = prediction_cases["outcome"]

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = {
    "LogisticRegression": LogisticRegression(
        max_iter=5000,
        solver="saga",
        C=1.0,
        class_weight="balanced",
        random_state=42,
    ),
    "RandomForest": RandomForestClassifier(
        n_estimators=250,
        class_weight="balanced",
        random_state=42,
    ),
    "SVM": SVC(
        kernel="rbf",
        class_weight="balanced",
        probability=True,
        random_state=42,
    ),
}

results = []
for name, model in models.items():
    f1_scores = cross_val_score(model, X, y, cv=cv, scoring="f1_weighted")
    acc_scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    results.append((name, model, f1_scores.mean(), acc_scores.mean()))
    print(
        f"{name}: weighted F1 {f1_scores.mean()*100:.2f}% "
        f"(+/- {f1_scores.std()*100:.2f}%) | accuracy {acc_scores.mean()*100:.2f}%"
    )

best_name, best_model, best_f1, best_acc = max(results, key=lambda result: (result[2], result[3]))
best_model.fit(X, y)
print(f"\nSelected model: {best_name}")
print(classification_report(y, best_model.predict(X), zero_division=0))

search_vectorizer = TfidfVectorizer(
    max_features=8000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True,
)
X_search = search_vectorizer.fit_transform(build_texts(all_cases)).toarray().astype("float32")
index = faiss.IndexFlatL2(X_search.shape[1])
index.add(X_search)

with open("models/prediction_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(prediction_vectorizer, f)

with open("models/search_vectorizer.pkl", "wb") as f:
    pickle.dump(search_vectorizer, f)

faiss.write_index(index, "models/case_index.faiss")
print(
    f"Done! Prediction: {best_acc*100:.2f}% accuracy / {best_f1*100:.2f}% weighted F1 "
    f"| Search index: {index.ntotal} cases"
)
