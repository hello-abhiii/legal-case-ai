import json
import pickle
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import faiss
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.svm import SVC

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.text_processing import combine_case_fields

warnings.filterwarnings("ignore")


def build_texts(df):
    return [
        combine_case_fields(row["facts"], row["section"], row["court"])
        for _, row in df.iterrows()
    ]


prediction_cases = pd.read_csv("data/cleaned_cases.csv")
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
    results.append((name, model, f1_scores.mean(), acc_scores.mean(), acc_scores))
    print(
        f"{name}: weighted F1 {f1_scores.mean()*100:.2f}% "
        f"(+/- {f1_scores.std()*100:.2f}%) | accuracy {acc_scores.mean()*100:.2f}%"
    )

best_name, best_model, best_f1, best_acc, best_fold_accuracies = max(
    results, key=lambda result: (result[2], result[3])
)
best_model.fit(X, y)
print(f"\nSelected model: {best_name}")
print(classification_report(y, best_model.predict(X), zero_division=0))

# Out-of-fold predictions give an honest (non-overfit) precision/recall/F1
# for the chosen model, using the same CV split as the accuracy scores above.
oof_predictions = cross_val_predict(best_model, X, y, cv=cv)
oof_precision, oof_recall, oof_f1, _ = precision_recall_fscore_support(
    y, oof_predictions, average="weighted", zero_division=0
)

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

# --- Export metrics for the frontend/backend to consume dynamically ---
outcome_counts = prediction_cases["outcome"].value_counts().to_dict()

section_counts = prediction_cases["section"].value_counts()
top_sections = section_counts.head(6)
other_count = int(section_counts.iloc[6:].sum()) if len(section_counts) > 6 else 0
section_distribution = {str(k): int(v) for k, v in top_sections.items()}
if other_count:
    section_distribution["Other"] = other_count

metrics = {
    "model_name": best_name,
    "accuracy": round(float(best_acc) * 100, 2),
    "precision": round(float(oof_precision) * 100, 2),
    "recall": round(float(oof_recall) * 100, 2),
    "f1_score": round(float(oof_f1) * 100, 2),
    "cv_fold_accuracies": [round(float(s) * 100, 2) for s in best_fold_accuracies],
    "total_cases": int(len(all_cases)),
    "prediction_cases": int(len(prediction_cases)),
    "ipc_sections": int(prediction_cases["section"].nunique()),
    "outcome_distribution": {str(k): int(v) for k, v in outcome_counts.items()},
    "section_distribution": section_distribution,
    "trained_at": datetime.now(timezone.utc).isoformat(),
}

with open("models/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(
    f"Done! Prediction: {best_acc*100:.2f}% accuracy / {best_f1*100:.2f}% weighted F1 "
    f"| Search index: {index.ntotal} cases"
)
print(f"Metrics written to models/metrics.json: {metrics}")

