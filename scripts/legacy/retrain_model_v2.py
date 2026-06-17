import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import hstack
import faiss
import re

# ── Load dataset ──────────────────────────────────────────────────────────────
df = pd.read_csv('data/cleaned_cases.csv')
print(f"✅ Loaded {len(df)} cases")

# ── Feature Engineering ───────────────────────────────────────────────────────
print("\n⏳ Engineering features...")

# 1. Clean facts text
def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text.strip()

df['facts_clean'] = df['facts'].apply(clean_text)

# 2. Court seniority (higher court = more acquittals typically)
court_rank = {
    'Supreme Court'    : 4,
    'High Court'       : 3,
    'Sessions Court'   : 2,
    'District Court'   : 1,
    'Magistrate Court' : 0,
}
df['court_rank'] = df['court'].map(court_rank).fillna(2)

# 3. Severity score from IPC section
severe_sections = ['302', '376', '363', '392', '384', '307', '304']
moderate_sections = ['379', '380', '420', '468', '506', '323', '325']

def severity_score(section):
    if not isinstance(section, str):
        return 1
    for s in severe_sections:
        if s in section:
            return 3
    for s in moderate_sections:
        if s in section:
            return 2
    return 1

df['severity'] = df['section'].apply(severity_score)

# 4. Text length (longer facts = more evidence = more conviction)
df['facts_len'] = df['facts_clean'].str.len().fillna(0)
df['facts_words'] = df['facts_clean'].str.split().str.len().fillna(0)

# 5. Keyword features
conviction_words = ['caught', 'witnessed', 'evidence', 'recovered', 'arrested',
                    'confessed', 'identified', 'cctv', 'fingerprint', 'stolen']
acquittal_words  = ['doubt', 'alibi', 'contradictory', 'inconsistent', 'lack',
                    'insufficient', 'no evidence', 'false', 'delay', 'unreliable']

def keyword_score(text, keywords):
    if not isinstance(text, str):
        return 0
    text = text.lower()
    return sum(1 for kw in keywords if kw in text)

df['conviction_keywords'] = df['facts_clean'].apply(lambda x: keyword_score(x, conviction_words))
df['acquittal_keywords']  = df['facts_clean'].apply(lambda x: keyword_score(x, acquittal_words))
df['keyword_diff']        = df['conviction_keywords'] - df['acquittal_keywords']

print("✅ Features engineered!")
print(f"   Numeric features: court_rank, severity, facts_len, facts_words, keyword scores")

# ── TF-IDF on combined text ───────────────────────────────────────────────────
df['combined_text'] = (
    df['facts_clean'] + ' ' +
    df['section'].fillna('') + ' ' +
    df['court'].fillna('')
)

print("\n⏳ Training TF-IDF...")
vectorizer = TfidfVectorizer(
    max_features=8000,
    ngram_range=(1, 3),
    stop_words='english',
    min_df=2,
    sublinear_tf=True   # dampens high frequency terms
)
X_tfidf = vectorizer.fit_transform(df['combined_text'])
print(f"✅ TF-IDF done — vocab: {len(vectorizer.vocabulary_)}")

# ── Combine TF-IDF + numeric features ────────────────────────────────────────
from scipy.sparse import csr_matrix
numeric_cols = ['court_rank', 'severity', 'facts_len',
                'facts_words', 'conviction_keywords',
                'acquittal_keywords', 'keyword_diff']
X_numeric = csr_matrix(df[numeric_cols].values.astype(float))
X_combined = hstack([X_tfidf, X_numeric])
print(f"✅ Combined feature matrix: {X_combined.shape}")

y = df['outcome']

# ── Train models ──────────────────────────────────────────────────────────────
print("\n⏳ Training models...")

lr  = LogisticRegression(max_iter=1000, C=2.0, class_weight='balanced', random_state=42)
svm = LinearSVC(max_iter=2000, C=1.0, class_weight='balanced', random_state=42)

# Voting ensemble (LR + SVM)
from sklearn.calibration import CalibratedClassifierCV
svm_cal = CalibratedClassifierCV(svm, cv=3)

ensemble = VotingClassifier(
    estimators=[('lr', lr), ('svm', svm_cal)],
    voting='soft'
)
ensemble.fit(X_combined, y)
print("✅ Ensemble model trained!")

# ── Cross validation ──────────────────────────────────────────────────────────
print("\n⏳ Running 5-Fold Cross Validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

lr_scores  = cross_val_score(lr,       X_combined, y, cv=cv, scoring='accuracy')
svm_scores = cross_val_score(svm_cal,  X_combined, y, cv=cv, scoring='accuracy')
ens_scores = cross_val_score(ensemble, X_combined, y, cv=cv, scoring='accuracy')

print(f"\n📊 Model Comparison:")
print(f"   Logistic Regression : {lr_scores.mean()*100:.2f}% (+/- {lr_scores.std()*100:.2f}%)")
print(f"   SVM (Calibrated)    : {svm_scores.mean()*100:.2f}% (+/- {svm_scores.std()*100:.2f}%)")
print(f"   Ensemble (LR+SVM)   : {ens_scores.mean()*100:.2f}% (+/- {ens_scores.std()*100:.2f}%)")

# ── Pick best model ───────────────────────────────────────────────────────────
best_score  = max(lr_scores.mean(), svm_scores.mean(), ens_scores.mean())
if best_score == ens_scores.mean():
    best_model, best_name = ensemble, "Ensemble (LR+SVM)"
elif best_score == svm_scores.mean():
    best_model, best_name = svm_cal, "SVM"
else:
    best_model, best_name = lr, "Logistic Regression"

print(f"\n🏆 Best model: {best_name} at {best_score*100:.2f}%")

# Full report
best_model.fit(X_combined, y)
y_pred = best_model.predict(X_combined)
print("\n📊 Classification Report:")
print(classification_report(y, y_pred))
cm = confusion_matrix(y, y_pred, labels=['Conviction', 'Acquittal'])
print(f"Confusion Matrix:")
print(f"                   Conviction  Acquittal")
print(f"Actual Conviction    {cm[0][0]:>6}      {cm[0][1]:>6}")
print(f"Actual Acquittal     {cm[1][0]:>6}      {cm[1][1]:>6}")

# ── Build FAISS index ─────────────────────────────────────────────────────────
print("\n⏳ Building FAISS index...")
X_faiss = X_tfidf.toarray().astype('float32')
index = faiss.IndexFlatL2(X_faiss.shape[1])
index.add(X_faiss)
print(f"✅ FAISS index: {index.ntotal} vectors")

# ── Save ──────────────────────────────────────────────────────────────────────
print("\n⏳ Saving models...")
with open('models/prediction_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# Save numeric feature config too
feature_config = {
    'numeric_cols'        : numeric_cols,
    'court_rank_map'      : court_rank,
    'severe_sections'     : severe_sections,
    'moderate_sections'   : moderate_sections,
    'conviction_words'    : conviction_words,
    'acquittal_words'     : acquittal_words,
}
with open('models/feature_config.pkl', 'wb') as f:
    pickle.dump(feature_config, f)

faiss.write_index(index, 'models/case_index.faiss')

print("✅ Saved: prediction_model.pkl, vectorizer.pkl, feature_config.pkl, case_index.faiss")
print(f"\n🎉 Done! Best CV accuracy: {best_score*100:.2f}%")
