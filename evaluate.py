import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score,
    confusion_matrix, classification_report
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("=" * 50)
print("   LEGAL CASE AI — MODEL EVALUATION REPORT")
print("=" * 50)

df = pd.read_csv("data/cleaned_cases.csv")
texts = (df['facts'] + " " + df['section'] + " " + df['court']).str.lower()
labels = df['outcome']

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=1000)

# 5-Fold Cross Validation — more realistic than single split
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

acc_scores  = cross_val_score(model, X, labels, cv=cv, scoring='accuracy')
prec_scores = cross_val_score(model, X, labels, cv=cv, scoring='precision_weighted')
rec_scores  = cross_val_score(model, X, labels, cv=cv, scoring='recall_weighted')
f1_scores   = cross_val_score(model, X, labels, cv=cv, scoring='f1_weighted')

print(f"\n📊 CROSS-VALIDATED METRICS (5-Fold)")
print(f"─────────────────────────────────────")
print(f"  Accuracy  : {acc_scores.mean()*100:.2f}% (± {acc_scores.std()*100:.2f}%)")
print(f"  Precision : {prec_scores.mean()*100:.2f}% (± {prec_scores.std()*100:.2f}%)")
print(f"  Recall    : {rec_scores.mean()*100:.2f}% (± {rec_scores.std()*100:.2f}%)")
print(f"  F1 Score  : {f1_scores.mean()*100:.2f}% (± {f1_scores.std()*100:.2f}%)")

print(f"\n📈 PER-FOLD ACCURACY BREAKDOWN")
print(f"─────────────────────────────────────")
for i, score in enumerate(acc_scores):
    bar = "█" * int(score * 20)
    print(f"  Fold {i+1}: {score*100:.2f}%  {bar}")

# Final model trained on all data for classification report
model.fit(X, labels)
y_pred = model.predict(X)

print(f"\n📋 CLASSIFICATION REPORT (Full Data)")
print(f"─────────────────────────────────────")
print(classification_report(labels, y_pred, zero_division=0))

print(f"\n🔲 CONFUSION MATRIX")
print(f"─────────────────────────────────────")
labels_order = ['Conviction', 'Acquittal']
cm_df = pd.DataFrame(
    confusion_matrix(labels, y_pred, labels=labels_order),
    index=[f"Actual {l}" for l in labels_order],
    columns=labels_order
)
print(cm_df.to_string())

print(f"\n💡 INTERPRETATION")
print(f"─────────────────────────────────────")
avg_acc = acc_scores.mean() * 100
if avg_acc >= 85:
    print(f"  ✅ Excellent! Model exceeds 85% target accuracy.")
elif avg_acc >= 70:
    print(f"  ✅ Good! Model meets the 70-85% target accuracy.")
else:
    print(f"  ⚠️  Below target. More training data recommended.")

print(f"\n  📌 Note: Accuracy will improve significantly")
print(f"     with real court judgment datasets from")
print(f"     Indian Kanoon or Supreme Court records.")
print(f"\n{'=' * 50}")
