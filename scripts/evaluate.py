import sys
import warnings
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.svm import SVC

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.text_processing import combine_case_fields

warnings.filterwarnings("ignore")

print("=" * 55)
print("  LEGAL CASE AI — MODEL EVALUATION REPORT")
print("=" * 55)

all_cases = pd.read_csv("data/cleaned_cases.csv")
df = all_cases[all_cases["case_id"] <= 66].copy()
print(f"Evaluating prediction model on {len(df)} clean curated cases")

texts = [
    combine_case_fields(row["facts"], row["section"], row["court"])
    for _, row in df.iterrows()
]
y = df["outcome"]

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True,
)
X = vectorizer.fit_transform(texts)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=5000,
        solver="saga",
        C=1.0,
        class_weight="balanced",
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=250,
        class_weight="balanced",
        random_state=42,
    ),
    "SVM (RBF)": SVC(
        kernel="rbf",
        class_weight="balanced",
        probability=True,
        random_state=42,
    ),
}

best_model, best_score = None, 0

for name, model in models.items():
    acc = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    f1 = cross_val_score(model, X, y, cv=cv, scoring="f1_weighted")
    print(f"\n  {name}")
    print(f"   CV Accuracy : {acc.mean()*100:.2f}% +/- {acc.std()*100:.2f}%")
    print(f"   F1 Score    : {f1.mean()*100:.2f}% +/- {f1.std()*100:.2f}%")
    if f1.mean() > best_score:
        best_score, best_model = f1.mean(), (name, model)

print(f"\nBest Model: {best_model[0]} ({best_score*100:.2f}% weighted F1)")

best_model[1].fit(X, y)
y_pred = best_model[1].predict(X)

print("\nCLASSIFICATION REPORT")
print(classification_report(y, y_pred, zero_division=0))

print("CONFUSION MATRIX")
labels_order = ["Conviction", "Acquittal"]
cm = pd.DataFrame(
    confusion_matrix(y, y_pred, labels=labels_order),
    index=[f"Actual {label}" for label in labels_order],
    columns=labels_order,
)
print(cm.to_string())
