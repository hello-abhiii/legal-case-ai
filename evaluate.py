import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  LEGAL CASE AI — MODEL EVALUATION REPORT")
print("=" * 55)

df = pd.read_csv("data/cleaned_cases.csv")
orig = df[df['case_id'] <= 66].copy()

orig['combined'] = (
    orig['facts'].fillna('') + ' ' +
    orig['section'].fillna('') + ' ' +
    orig['court'].fillna('')
)

vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1,2), sublinear_tf=True)
X = vectorizer.fit_transform(orig['combined'])
y = orig['outcome']

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(max_iter=5000, solver='saga', C=1.0, class_weight='balanced', random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
    "SVM (RBF)":           SVC(kernel='rbf', class_weight='balanced', probability=True, random_state=42),
}

best_model, best_score = None, 0

for name, model in models.items():
    acc = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    f1  = cross_val_score(model, X, y, cv=cv, scoring='f1_weighted')
    print(f"\n  {name}")
    print(f"   CV Accuracy : {acc.mean()*100:.2f}% +/- {acc.std()*100:.2f}%")
    print(f"   F1 Score    : {f1.mean()*100:.2f}% +/- {f1.std()*100:.2f}%")
    if acc.mean() > best_score:
        best_score, best_model = acc.mean(), (name, model)

print(f"\nBest Model: {best_model[0]} ({best_score*100:.2f}%)")

best_model[1].fit(X, y)
y_pred = best_model[1].predict(X)

print("\nCLASSIFICATION REPORT")
print(classification_report(y, y_pred, zero_division=0))

print("CONFUSION MATRIX")
labels_order = ['Conviction', 'Acquittal']
cm = pd.DataFrame(
    confusion_matrix(y, y_pred, labels=labels_order),
    index=[f"Actual {l}" for l in labels_order],
    columns=labels_order
)
print(cm.to_string())
